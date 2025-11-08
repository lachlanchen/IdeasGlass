#from
from __future__ import annotations

import asyncio
import base64
import json
import os
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Coroutine, Dict, List, Optional
import wave

import asyncpg
from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import webrtcvad

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
AUDIO_SEGMENTS_DIR = BASE_DIR / "audio_segments"
AUDIO_SEGMENT_URL_PREFIX = "/api/v1/audio/segments"
FALLBACK_RMS_THRESHOLD = float(os.getenv("IDEASGLASS_VAD_FALLBACK", "0.02"))
SEGMENT_TARGET_MS = int(os.getenv("IDEASGLASS_SEGMENT_TARGET_MS", "60000"))
SEGMENT_MAX_MS = int(os.getenv("IDEASGLASS_SEGMENT_MAX_MS", "90000"))
MIN_SEGMENT_MS = int(os.getenv("IDEASGLASS_SEGMENT_MIN_MS", "1500"))
SILENCE_HANGOVER_MS = int(os.getenv("IDEASGLASS_VAD_HANGOVER_MS", "1200"))
SILENCE_FORCE_FLUSH_MS = int(os.getenv("IDEASGLASS_VAD_FORCE_MS", "2200"))
SEGMENT_IDLE_FLUSH_MS = int(os.getenv("IDEASGLASS_SEGMENT_IDLE_FLUSH_MS", "4000"))
VAD_FRAME_MS = 30
VAD_AGGRESSIVENESS = int(os.getenv("IDEASGLASS_VAD_LEVEL", "2"))


class MessageIn(BaseModel):
    device_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4096)
    meta: Dict[str, str] | None = None
    photo_base64: Optional[str] = Field(default=None, description="JPEG payload encoded as Base64")
    photo_mime: Optional[str] = Field(default="image/jpeg")


class MessageOut(BaseModel):
    id: str
    device_id: str
    message: str
    meta: Dict[str, str] | None
    received_at: str
    photo_url: Optional[str] = None


class AudioChunkIn(BaseModel):
    device_id: str = Field(min_length=1, max_length=128)
    sample_rate: int = Field(default=16000, ge=8000, le=48000)
    bits_per_sample: int = Field(default=16, ge=8, le=32)
    duration_ms: int = Field(default=250, ge=10, le=10000)
    rms: float = Field(ge=0.0)
    audio_base64: str = Field(min_length=1)
    mime: str = Field(default="audio/pcm")


class AudioChunkOut(BaseModel):
    id: str
    device_id: str
    sample_rate: int
    bits_per_sample: int
    duration_ms: int
    rms: float
    created_at: str
    audio_url: Optional[str] = None
    speech_detected: bool = False


class AudioSegmentOut(BaseModel):
    id: str
    device_id: str
    sample_rate: int
    bits_per_sample: int
    duration_ms: int
    rms: float
    started_at: str
    ended_at: str
    file_path: Optional[str] = None
    file_url: Optional[str] = None


@dataclass
class AudioSegmentBuffer:
    device_id: str
    sample_rate: int
    bits_per_sample: int
    started_at: datetime
    segment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    buffer: bytearray = field(default_factory=bytearray)
    duration_ms: int = 0
    rms_accumulator: float = 0.0
    rms_count: int = 0
    last_chunk_at: Optional[datetime] = None
    last_voice_at: Optional[datetime] = None


@dataclass
class AudioSegmentRecord:
    id: str
    device_id: str
    sample_rate: int
    bits_per_sample: int
    duration_ms: int
    rms: float
    started_at: datetime
    ended_at: datetime
    file_path: Optional[str] = None


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self._connections:
                self._connections.remove(websocket)

    async def broadcast(self, data: dict) -> None:
        async with self._lock:
            targets = list(self._connections)
        for ws in targets:
            try:
                await ws.send_json(data)
            except Exception:
                await self.disconnect(ws)


app = FastAPI(title="IdeasGlass Ngrok Bridge")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()
message_store: deque[MessageOut] = deque(maxlen=200)
audio_store: deque[AudioChunkOut] = deque(maxlen=200)
audio_segment_store: deque[AudioSegmentOut] = deque(maxlen=50)
DATABASE_URL = os.getenv("DATABASE_URL")
db_pool: asyncpg.pool.Pool | None = None
vad_detector = webrtcvad.Vad(max(0, min(3, VAD_AGGRESSIVENESS)))
segment_states: Dict[str, AudioSegmentBuffer] = {}
segment_lock = asyncio.Lock()
segment_cleanup_task: asyncio.Task | None = None
SUPPORTED_VAD_RATES = {8000, 16000, 32000, 48000}


async def init_db() -> None:
    if not db_pool:
        return
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_messages (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                message TEXT NOT NULL,
                meta JSONB,
                received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_photos (
                id TEXT PRIMARY KEY,
                message_id TEXT REFERENCES ig_messages(id) ON DELETE CASCADE,
                mime_type TEXT NOT NULL,
                data BYTEA NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_audio_chunks (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                sample_rate INT NOT NULL,
                bits_per_sample INT NOT NULL,
                duration_ms INT NOT NULL,
                rms REAL NOT NULL,
                data BYTEA NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                speech BOOLEAN NOT NULL DEFAULT FALSE
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_audio_segments (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                sample_rate INT NOT NULL,
                bits_per_sample INT NOT NULL,
                duration_ms INT NOT NULL,
                rms REAL NOT NULL,
                data BYTEA NOT NULL,
                started_at TIMESTAMPTZ NOT NULL,
                ended_at TIMESTAMPTZ NOT NULL,
                file_path TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            "ALTER TABLE ig_audio_chunks ADD COLUMN IF NOT EXISTS speech BOOLEAN NOT NULL DEFAULT FALSE;"
        )
        await conn.execute(
            "ALTER TABLE ig_audio_segments ADD COLUMN IF NOT EXISTS file_path TEXT;"
        )


@app.on_event("startup")
async def startup_event():
    global db_pool, segment_cleanup_task
    AUDIO_SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    if not DATABASE_URL:
        print("[DB] DATABASE_URL not set; running in in-memory mode.")
    else:
        try:
            db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
            await init_db()
            print("[DB] Connected to Postgres and ensured tables exist.")
        except Exception as exc:
            print(f"[DB] Failed to initialize Postgres: {exc}")
            db_pool = None
    if not segment_cleanup_task:
        segment_cleanup_task = asyncio.create_task(segment_housekeeper())


@app.on_event("shutdown")
async def shutdown_event():
    global db_pool, segment_cleanup_task
    await flush_idle_segments(force=True)
    if db_pool:
        await db_pool.close()
        db_pool = None
    if segment_cleanup_task:
        segment_cleanup_task.cancel()
        try:
            await segment_cleanup_task
        except asyncio.CancelledError:
            pass
        segment_cleanup_task = None


def _make_entry(payload: MessageIn) -> MessageOut:
    now = datetime.now(tz=timezone.utc)
    entry = MessageOut(
        id=str(uuid.uuid4()),
        device_id=payload.device_id,
        message=payload.message,
        meta=payload.meta or {},
        received_at=now.isoformat(),
    )
    return entry


async def persist_entry(
    entry: MessageOut,
    photo_bytes: Optional[bytes],
    photo_mime: Optional[str],
    photo_id: Optional[str],
) -> None:
    if not db_pool:
        return
    dt = datetime.fromisoformat(entry.received_at)
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO ig_messages (id, device_id, message, meta, received_at)
            VALUES ($1,$2,$3,$4,$5)
            ON CONFLICT (id) DO NOTHING;
            """,
            entry.id,
            entry.device_id,
            entry.message,
            json.dumps(entry.meta or {}),
            dt,
        )
        if photo_bytes and photo_id:
            await conn.execute(
                """
                INSERT INTO ig_photos (id, message_id, mime_type, data)
                VALUES ($1,$2,$3,$4)
                ON CONFLICT (id) DO NOTHING;
                """,
                photo_id,
                entry.id,
                photo_mime or "image/jpeg",
                photo_bytes,
            )


async def fetch_messages(limit: int = 100, before: Optional[datetime] = None) -> List[MessageOut]:
    if not db_pool:
        data = list(message_store)
        if before:
            data = [
                m for m in data if datetime.fromisoformat(m.received_at) < before
            ]
        return data[:limit]
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT m.id,
                   m.device_id,
                   m.message,
                   m.meta,
                   m.received_at,
                   p.id as photo_id
            FROM ig_messages m
            LEFT JOIN ig_photos p ON p.message_id = m.id
            WHERE ($2::timestamptz IS NULL OR m.received_at < $2)
            ORDER BY m.received_at DESC
            LIMIT $1;
            """,
            limit,
            before,
        )
    entries: List[MessageOut] = []
    for row in rows:
        meta_payload = row["meta"]
        if isinstance(meta_payload, str):
            try:
                meta_payload = json.loads(meta_payload)
            except Exception:
                meta_payload = {}
        entries.append(
            MessageOut(
                id=row["id"],
                device_id=row["device_id"],
                message=row["message"],
                meta=meta_payload or {},
                received_at=row["received_at"].isoformat(),
                photo_url=f"/api/v1/photos/{row['photo_id']}" if row["photo_id"] else None,
            )
        )
    return entries


async def persist_audio_chunk(
    chunk: AudioChunkOut,
    raw_bytes: bytes,
) -> None:
    if not db_pool:
        return
    dt = datetime.fromisoformat(chunk.created_at)
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO ig_audio_chunks (
                id, device_id, sample_rate, bits_per_sample,
                duration_ms, rms, data, created_at, speech
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ON CONFLICT (id) DO NOTHING;
            """,
            chunk.id,
            chunk.device_id,
            chunk.sample_rate,
            chunk.bits_per_sample,
            chunk.duration_ms,
            chunk.rms,
            raw_bytes,
            dt,
            chunk.speech_detected,
        )


async def fetch_audio_chunks(limit: int = 60, before: Optional[datetime] = None) -> List[AudioChunkOut]:
    if not db_pool:
        data = list(audio_store)
        if before:
            data = [
                c for c in data if datetime.fromisoformat(c.created_at) < before
            ]
        return data[:limit]
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id,
                   device_id,
                   sample_rate,
                   bits_per_sample,
                   duration_ms,
                   rms,
                   created_at,
                   speech
            FROM ig_audio_chunks
            WHERE ($2::timestamptz IS NULL OR created_at < $2)
            ORDER BY created_at DESC
            LIMIT $1;
            """,
            limit,
            before,
        )
    chunks: List[AudioChunkOut] = []
    for row in rows:
        chunks.append(
            AudioChunkOut(
                id=row["id"],
                device_id=row["device_id"],
                sample_rate=row["sample_rate"],
                bits_per_sample=row["bits_per_sample"],
                duration_ms=row["duration_ms"],
                rms=row["rms"],
                created_at=row["created_at"].isoformat(),
                audio_url=f"/api/v1/audio/{row['id']}",
                speech_detected=row.get("speech") or False,
            )
        )
    return chunks


async def fetch_audio_segments(limit: int = 20, before: Optional[datetime] = None) -> List[AudioSegmentOut]:
    if not db_pool:
        data = list(audio_segment_store)
        if before:
            data = [
                seg for seg in data if datetime.fromisoformat(seg.ended_at) < before
            ]
        return data[:limit]
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id,
                   device_id,
                   sample_rate,
                   bits_per_sample,
                   duration_ms,
                   rms,
                   started_at,
                   ended_at,
                   file_path
            FROM ig_audio_segments
            WHERE ($2::timestamptz IS NULL OR ended_at < $2)
            ORDER BY ended_at DESC
            LIMIT $1;
            """,
            limit,
            before,
        )
    return [row_to_segment_out(row) for row in rows]


def pcm_to_wav(raw_bytes: bytes, sample_rate: int, bits_per_sample: int) -> bytes:
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(bits_per_sample // 8)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(raw_bytes)
    return buffer.getvalue()


def detect_speech(
    raw_audio: bytes,
    sample_rate: int,
    bits_per_sample: int,
    fallback_rms: float,
) -> bool:
    if bits_per_sample == 16 and sample_rate in SUPPORTED_VAD_RATES:
        frame_bytes = int(sample_rate * (VAD_FRAME_MS / 1000.0)) * 2
        if frame_bytes > 0 and len(raw_audio) >= frame_bytes:
            for offset in range(0, len(raw_audio) - frame_bytes + 1, frame_bytes):
                frame = raw_audio[offset : offset + frame_bytes]
                if vad_detector.is_speech(frame, sample_rate):
                    return True
            return False
    return fallback_rms >= FALLBACK_RMS_THRESHOLD


def row_to_segment_out(row) -> AudioSegmentOut:
    file_path = row["file_path"] if "file_path" in row else None
    return AudioSegmentOut(
        id=row["id"],
        device_id=row["device_id"],
        sample_rate=row["sample_rate"],
        bits_per_sample=row["bits_per_sample"],
        duration_ms=row["duration_ms"],
        rms=row["rms"],
        started_at=row["started_at"].isoformat(),
        ended_at=row["ended_at"].isoformat(),
        file_path=file_path,
        file_url=f"{AUDIO_SEGMENT_URL_PREFIX}/{row['id']}",
    )


def _silence_duration_ms(state: AudioSegmentBuffer, now: datetime) -> float:
    if state.last_voice_at:
        return (now - state.last_voice_at).total_seconds() * 1000
    return float(state.duration_ms)


def _should_finalize_segment(
    state: AudioSegmentBuffer,
    now: datetime,
    speech_detected: bool,
) -> bool:
    if not state.buffer:
        return False
    silence_ms = _silence_duration_ms(state, now)
    if state.duration_ms >= SEGMENT_MAX_MS:
        return True
    if state.duration_ms >= SEGMENT_TARGET_MS and silence_ms >= SILENCE_HANGOVER_MS:
        return True
    if (
        not speech_detected
        and state.duration_ms >= MIN_SEGMENT_MS
        and silence_ms >= SILENCE_FORCE_FLUSH_MS
    ):
        return True
    return False


async def persist_audio_segment(
    segment: AudioSegmentRecord,
    wav_bytes: bytes,
    file_path: Optional[str],
) -> None:
    if not db_pool:
        return
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO ig_audio_segments (
                id, device_id, sample_rate, bits_per_sample,
                duration_ms, rms, data, started_at, ended_at, file_path
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
            ON CONFLICT (id) DO NOTHING;
            """,
            segment.id,
            segment.device_id,
            segment.sample_rate,
            segment.bits_per_sample,
            segment.duration_ms,
            segment.rms,
            wav_bytes,
            segment.started_at,
            segment.ended_at,
            file_path,
        )


async def _flush_segment_state(state: AudioSegmentBuffer) -> None:
    if not state.buffer:
        return
    ended_at = state.last_chunk_at or state.started_at
    avg_rms = state.rms_accumulator / max(1, state.rms_count)
    wav_payload = pcm_to_wav(bytes(state.buffer), state.sample_rate, state.bits_per_sample)
    record = AudioSegmentRecord(
        id=state.segment_id,
        device_id=state.device_id,
        sample_rate=state.sample_rate,
        bits_per_sample=state.bits_per_sample,
        duration_ms=state.duration_ms,
        rms=avg_rms,
        started_at=state.started_at,
        ended_at=ended_at,
    )
    filename = f"{record.id}.wav"
    disk_path = AUDIO_SEGMENTS_DIR / filename
    try:
        disk_path.write_bytes(wav_payload)
    except Exception as exc:
        print(f"[Audio] Failed to write segment {record.id} to disk: {exc}")
    relative_path = _relativize_path(disk_path)
    record.file_path = relative_path
    await persist_audio_segment(record, wav_payload, relative_path)
    print(
        f"[Audio] Saved segment {record.id} for {record.device_id} "
        f"({record.duration_ms} ms, avg RMS {record.rms:.3f})"
    )
    segment_out = segment_record_to_out(record)
    audio_segment_store.append(segment_out)
    await manager.broadcast({"type": "audio_segment", "payload": segment_out.model_dump()})


async def append_audio_to_segment_buffers(
    chunk: AudioChunkOut,
    raw_audio: bytes,
    speech_detected: bool,
) -> None:
    now = datetime.fromisoformat(chunk.created_at)
    segments_to_flush: List[AudioSegmentBuffer] = []
    async with segment_lock:
        state = segment_states.get(chunk.device_id)
        if (
            not state
            or state.sample_rate != chunk.sample_rate
            or state.bits_per_sample != chunk.bits_per_sample
        ):
            if state and state.buffer:
                segments_to_flush.append(segment_states.pop(chunk.device_id))
            state = AudioSegmentBuffer(
                device_id=chunk.device_id,
                sample_rate=chunk.sample_rate,
                bits_per_sample=chunk.bits_per_sample,
                started_at=now,
            )
            segment_states[chunk.device_id] = state

        state.buffer.extend(raw_audio)
        state.duration_ms += chunk.duration_ms
        state.rms_accumulator += chunk.rms
        state.rms_count += 1
        state.last_chunk_at = now
        if speech_detected:
            state.last_voice_at = now

        if _should_finalize_segment(state, now, speech_detected):
            segments_to_flush.append(segment_states.pop(chunk.device_id, None))

        idle_candidates = []
        for device_id, candidate in segment_states.items():
            if not candidate.last_chunk_at or candidate is state:
                continue
            idle_ms = (now - candidate.last_chunk_at).total_seconds() * 1000
            if idle_ms >= SEGMENT_IDLE_FLUSH_MS and candidate.duration_ms >= MIN_SEGMENT_MS:
                idle_candidates.append(device_id)
        for device_id in idle_candidates:
            candidate = segment_states.pop(device_id, None)
            if candidate:
                segments_to_flush.append(candidate)

    for segment in segments_to_flush:
        if segment:
            await _flush_segment_state(segment)


async def flush_idle_segments(force: bool = False) -> None:
    now = datetime.now(tz=timezone.utc)
    to_flush: List[AudioSegmentBuffer] = []
    async with segment_lock:
        for device_id, state in list(segment_states.items()):
            if not state.last_chunk_at:
                continue
            idle_ms = (now - state.last_chunk_at).total_seconds() * 1000
            if force or (
                idle_ms >= SEGMENT_IDLE_FLUSH_MS and state.duration_ms >= MIN_SEGMENT_MS
            ):
                to_flush.append(segment_states.pop(device_id, None))
    for segment in to_flush:
        if segment:
            await _flush_segment_state(segment)


async def segment_housekeeper():
    while True:
        await asyncio.sleep(2)
        await flush_idle_segments()


@app.post("/api/v1/messages", response_model=MessageOut)
async def ingest_message(payload: MessageIn):
    entry = _make_entry(payload)
    photo_bytes: Optional[bytes] = None
    photo_id: Optional[str] = None

    if payload.photo_base64:
        try:
            photo_bytes = base64.b64decode(payload.photo_base64.encode(), validate=True)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid photo_base64 data: {exc}") from exc
        photo_id = str(uuid.uuid4())
        entry.photo_url = f"/api/v1/photos/{photo_id}"

    message_store.append(entry)
    await persist_entry(entry, photo_bytes, payload.photo_mime, photo_id)
    await manager.broadcast({"type": "message", "payload": entry.model_dump()})
    return entry


@app.get("/api/v1/messages", response_model=List[MessageOut])
async def list_messages(limit: int = 50, before: Optional[str] = None):
    capped = max(1, min(limit, 200))
    before_dt: Optional[datetime] = None
    if before:
        try:
            before_dt = datetime.fromisoformat(before)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'before' timestamp")
    return await fetch_messages(limit=capped, before=before_dt)


@app.post("/api/v1/audio", response_model=AudioChunkOut)
async def ingest_audio_chunk(payload: AudioChunkIn):
    try:
        raw_audio = base64.b64decode(payload.audio_base64.encode(), validate=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid audio_base64 data: {exc}") from exc

    speech_detected = detect_speech(
        raw_audio,
        payload.sample_rate,
        payload.bits_per_sample,
        payload.rms,
    )
    chunk_id = str(uuid.uuid4())
    now = datetime.now(tz=timezone.utc)
    chunk = AudioChunkOut(
        id=chunk_id,
        device_id=payload.device_id,
        sample_rate=payload.sample_rate,
        bits_per_sample=payload.bits_per_sample,
        duration_ms=payload.duration_ms,
        rms=payload.rms,
        created_at=now.isoformat(),
        audio_url=f"/api/v1/audio/{chunk_id}",
        speech_detected=speech_detected,
    )

    audio_store.append(chunk)
    schedule_background(
        persist_audio_chunk(chunk, raw_audio),
        "persist_audio_chunk",
    )
    schedule_background(
        append_audio_to_segment_buffers(chunk, raw_audio, speech_detected),
        "segment_buffer",
    )
    print(
        "[Audio] Forward chunk "
        f"{chunk.device_id}#{chunk.id} rms={chunk.rms:.4f} speech={speech_detected}"
    )
    await manager.broadcast({"type": "audio_chunk", "payload": chunk.model_dump()})
    return chunk


@app.get("/api/v1/audio", response_model=List[AudioChunkOut])
async def list_audio(limit: int = 60, before: Optional[str] = None):
    capped = max(1, min(limit, 200))
    before_dt: Optional[datetime] = None
    if before:
        try:
            before_dt = datetime.fromisoformat(before)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'before' timestamp")
    return await fetch_audio_chunks(limit=capped, before=before_dt)


@app.get("/api/v1/audio/segments", response_model=List[AudioSegmentOut])
async def list_audio_segments(limit: int = 20, before: Optional[str] = None):
    capped = max(1, min(limit, 100))
    before_dt: Optional[datetime] = None
    if before:
        try:
            before_dt = datetime.fromisoformat(before)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'before' timestamp")
    return await fetch_audio_segments(limit=capped, before=before_dt)


@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        history = await fetch_messages(limit=50)
        await websocket.send_json({"type": "history_messages", "data": [m.model_dump() for m in history]})
        audio_history = await fetch_audio_chunks(limit=60)
        await websocket.send_json({"type": "history_audio", "data": [c.model_dump() for c in audio_history]})
        segment_history = await fetch_audio_segments(limit=20)
        await websocket.send_json({"type": "history_audio_segments", "data": [s.model_dump() for s in segment_history]})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.get("/api/v1/photos/{photo_id}")
async def get_photo(photo_id: str):
    if not db_pool:
        raise HTTPException(status_code=404, detail="Photo storage disabled (DATABASE_URL not set).")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT data, mime_type FROM ig_photos WHERE id=$1",
            photo_id,
        )
    if not row:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return Response(content=bytes(row["data"]), media_type=row["mime_type"])


@app.get("/api/v1/audio/{audio_id}")
async def get_audio(audio_id: str):
    if not db_pool:
        raise HTTPException(status_code=404, detail="Audio storage disabled (DATABASE_URL not set).")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT data, sample_rate, bits_per_sample FROM ig_audio_chunks WHERE id=$1",
            audio_id,
        )
    if not row:
        raise HTTPException(status_code=404, detail="Audio not found.")
    pcm_bytes: bytes = bytes(row["data"])
    sample_rate = row["sample_rate"]
    bits_per_sample = row["bits_per_sample"]
    wav_payload = pcm_to_wav(pcm_bytes, sample_rate, bits_per_sample)
    return Response(content=wav_payload, media_type="audio/wav")


@app.get("/api/v1/audio/segments/{segment_id}")
async def get_audio_segment(segment_id: str):
    if not db_pool:
        raise HTTPException(status_code=404, detail="Audio storage disabled (DATABASE_URL not set).")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT data, file_path FROM ig_audio_segments WHERE id=$1",
            segment_id,
        )
    if not row:
        raise HTTPException(status_code=404, detail="Segment not found.")
    file_path = row.get("file_path")
    if file_path:
        disk_path = BASE_DIR / file_path
        if disk_path.exists():
            return FileResponse(disk_path, media_type="audio/wav", filename=f"{segment_id}.wav")
    return Response(content=bytes(row["data"]), media_type="audio/wav")


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok", "messages": len(message_store)}


@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
def _relativize_path(path: Path) -> str:
    try:
        return str(path.relative_to(BASE_DIR))
    except ValueError:
        return str(path)


def schedule_background(coro: Coroutine, label: str) -> None:
    task = asyncio.create_task(coro)

    def _log_result(t: asyncio.Task) -> None:
        try:
            t.result()
        except Exception as exc:  # pragma: no cover - best effort logging
            print(f"[AsyncTask] {label} failed: {exc}")

    task.add_done_callback(_log_result)


def segment_record_to_out(record: AudioSegmentRecord) -> AudioSegmentOut:
    return AudioSegmentOut(
        id=record.id,
        device_id=record.device_id,
        sample_rate=record.sample_rate,
        bits_per_sample=record.bits_per_sample,
        duration_ms=record.duration_ms,
        rms=record.rms,
        started_at=record.started_at.isoformat(),
        ended_at=record.ended_at.isoformat(),
        file_path=record.file_path,
        file_url=f"{AUDIO_SEGMENT_URL_PREFIX}/{record.id}",
    )
