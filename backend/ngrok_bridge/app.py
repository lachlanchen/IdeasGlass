#from
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import base64
import json
import os
import uuid
from array import array
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from io import BytesIO
from pathlib import Path
import site
import ctypes
from typing import Any, Coroutine, Dict, List, Optional
import wave
import math
import numpy as np

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
from pydantic import BaseModel, Field, ValidationError
import webrtcvad
def _inject_cudnn_library_path() -> None:
    if os.name != "posix":
        return
    search_roots: List[str] = []
    try:
        search_roots.extend(site.getsitepackages())
    except Exception:
        pass
    try:
        user_site = site.getusersitepackages()
        if user_site:
            search_roots.append(user_site)
    except Exception:
        pass
    if not search_roots:
        return
    candidate_paths: List[str] = []
    for root in search_roots:
        cudnn_dir = Path(root) / "nvidia" / "cudnn" / "lib"
        if cudnn_dir.exists() and cudnn_dir.is_dir():
            candidate_paths.append(str(cudnn_dir))
    if not candidate_paths:
        return
    existing = os.environ.get("LD_LIBRARY_PATH", "")
    updated_parts: List[str] = []
    for path in candidate_paths:
        if path and path not in existing:
            updated_parts.append(path)
    if not updated_parts:
        return
    if existing:
        updated_parts.append(existing)
    os.environ["LD_LIBRARY_PATH"] = ":".join(updated_parts)
    # Proactively load cuDNN libs so the dynamic linker sees them even if LD_LIBRARY_PATH was read earlier.
    for base_path in candidate_paths:
        libdir = Path(base_path)
        for lib_name in (
            "libcudnn.so.9",
            "libcudnn_adv.so.9",
            "libcudnn_ops.so.9",
            "libcudnn_cnn.so.9",
            "libcudnn_graph.so.9",
            "libcudnn_heuristic.so.9",
            "libcudnn_engines_precompiled.so.9",
            "libcudnn_engines_runtime_compiled.so.9",
        ):
            lib_path = libdir / lib_name
            if not lib_path.exists():
                continue
            try:
                ctypes.CDLL(str(lib_path))
            except OSError as exc:
                print(f"[Transcription] Warning: failed to preload {lib_path}: {exc}")


_inject_cudnn_library_path()

try:
    import torch
except Exception:  # pragma: no cover - optional dependency
    torch = None

try:
    import whisper  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    whisper = None

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
AUDIO_SEGMENTS_DIR = BASE_DIR / "audio_segments"
AUDIO_SEGMENTS_WORK_DIR = AUDIO_SEGMENTS_DIR / "in_progress"
AUDIO_SEGMENT_URL_PREFIX = "/api/v1/audio/segments"
PHOTO_STORAGE_DIR = STATIC_DIR / "photos"
PHOTO_STORAGE_URL_PREFIX = "/static/photos"
FALLBACK_RMS_THRESHOLD = float(os.getenv("IDEASGLASS_VAD_FALLBACK", "0.02"))
SEGMENT_TARGET_MS = int(os.getenv("IDEASGLASS_SEGMENT_TARGET_MS", "15000"))
SEGMENT_MAX_MS = int(os.getenv("IDEASGLASS_SEGMENT_MAX_MS", "18000"))
MIN_SEGMENT_MS = int(os.getenv("IDEASGLASS_SEGMENT_MIN_MS", "5000"))
SILENCE_HANGOVER_MS = int(os.getenv("IDEASGLASS_VAD_HANGOVER_MS", "1200"))
SILENCE_FORCE_FLUSH_MS = int(os.getenv("IDEASGLASS_VAD_FORCE_MS", "5000"))
SEGMENT_IDLE_FLUSH_MS = int(os.getenv("IDEASGLASS_SEGMENT_IDLE_FLUSH_MS", "5000"))
VAD_FRAME_MS = 30
VAD_AGGRESSIVENESS = int(os.getenv("IDEASGLASS_VAD_LEVEL", "2"))
AUDIO_GAIN_TARGET_RMS = float(os.getenv("IDEASGLASS_GAIN_TARGET", "0.032"))
AUDIO_GAIN_MAX = float(os.getenv("IDEASGLASS_GAIN_MAX", "1.8"))
AUDIO_GAIN_MIN_RMS = float(os.getenv("IDEASGLASS_GAIN_MIN_RMS", "0.008"))
SPEECH_RMS_THRESHOLD = float(os.getenv("IDEASGLASS_SPEECH_RMS", "0.03"))
AUDIO_GAIN_FALSE_POSITIVE_MARGIN = float(os.getenv("IDEASGLASS_SPEECH_MARGIN", "0.005"))
TRANSCRIPTION_ENABLED = os.getenv("IDEASGLASS_TRANSCRIBE", "1").lower() not in {"0", "false"}
WHISPER_DEVICE_DEFAULT = "cuda" if torch and torch.cuda.is_available() else "cpu"
WHISPER_DEVICE = os.getenv("IDEASGLASS_WHISPER_DEVICE", WHISPER_DEVICE_DEFAULT)
WHISPER_MODEL_NAME = os.getenv("IDEASGLASS_WHISPER_MODEL", "base")
WHISPER_FP16 = os.getenv("IDEASGLASS_WHISPER_FP16", "1").lower() not in {"0", "false"}
WHISPER_STREAM_INTERVAL_MS = int(os.getenv("IDEASGLASS_TRANSCRIPT_INTERVAL_MS", "3000"))
WHISPER_STREAM_THRESHOLDS = os.getenv("IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS", "3000,6000,15000")
if TRANSCRIPTION_ENABLED and not whisper:
    TRANSCRIPTION_ENABLED = False
    print("[Transcription] openai-whisper not available; disabling automatic transcription.")
SEGMENT_GAIN_TARGET_RMS = float(
    os.getenv("IDEASGLASS_SEGMENT_GAIN_TARGET", str(AUDIO_GAIN_TARGET_RMS))
)


def _parse_thresholds(raw: str) -> List[int]:
    values: List[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ms = int(part)
        except ValueError:
            continue
        if ms <= 0:
            continue
        values.append(ms)
    if not values:
        values = [WHISPER_STREAM_INTERVAL_MS, SEGMENT_TARGET_MS]
    values = sorted(set(values))
    if values[-1] < SEGMENT_TARGET_MS:
        values.append(SEGMENT_TARGET_MS)
    return values


WHISPER_THRESHOLD_VALUES = _parse_thresholds(WHISPER_STREAM_THRESHOLDS)


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
    segment_duration_ms: Optional[int] = None
    active_segment_id: Optional[str] = None


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


class TranscriptChunk(BaseModel):
    speaker: str
    text: str
    start: float
    end: float


class AudioTranscriptOut(BaseModel):
    segment_id: str
    device_id: str
    started_at: str
    ended_at: str
    chunks: List[TranscriptChunk]
    is_final: bool = False


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
    temp_path: Optional[Path] = None


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


@dataclass
class SegmentAppendResult:
    segment_id: Optional[str] = None
    duration_ms: Optional[int] = None


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
audio_transcript_store: deque[AudioTranscriptOut] = deque(maxlen=20)
DATABASE_URL = os.getenv("DATABASE_URL")
db_pool: asyncpg.pool.Pool | None = None
vad_detector = webrtcvad.Vad(max(0, min(3, VAD_AGGRESSIVENESS)))
segment_states: Dict[str, List[AudioSegmentBuffer]] = {}
segment_lock = asyncio.Lock()
segment_cleanup_task: asyncio.Task | None = None
SUPPORTED_VAD_RATES = {8000, 16000, 32000, 48000}
SEGMENT_OVERLAP_MS = int(os.getenv("IDEASGLASS_SEGMENT_OVERLAP_MS", "2000"))
SEGMENT_LOOKBACK_MS = max(0, min(SEGMENT_OVERLAP_MS, SEGMENT_TARGET_MS // 2))


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
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ig_audio_transcripts (
                segment_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                transcript JSONB NOT NULL,
                started_at TIMESTAMPTZ NOT NULL,
                ended_at TIMESTAMPTZ NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )


@app.on_event("startup")
async def startup_event():
    global db_pool, segment_cleanup_task
    AUDIO_SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_SEGMENTS_WORK_DIR.mkdir(parents=True, exist_ok=True)
    PHOTO_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    # Be generous in threading for blocking work offloaded via asyncio.to_thread
    try:
        cpu = os.cpu_count() or 4
        default_workers = max(32, cpu * 8)
        max_workers = int(os.getenv("IDEASGLASS_THREADPOOL_WORKERS", str(default_workers)))
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=max_workers))
        print(f"[ThreadPool] Default executor workers set to {max_workers}")
    except Exception as exc:
        print(f"[ThreadPool] Failed to set default executor: {exc}")
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
        data.sort(
            key=lambda m: datetime.fromisoformat(m.received_at),
            reverse=True,
        )
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


async def fetch_audio_transcripts(limit: int = 20, before: Optional[datetime] = None) -> List[AudioTranscriptOut]:
    if not db_pool:
        data = list(audio_transcript_store)
        if before:
            data = [
                seg
                for seg in data
                if datetime.fromisoformat(seg.ended_at) < before
            ]
        data.sort(
            key=lambda seg: datetime.fromisoformat(seg.ended_at),
            reverse=True,
        )
        return data[:limit]
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT segment_id, device_id, transcript, started_at, ended_at
            FROM ig_audio_transcripts
            WHERE ($2::timestamptz IS NULL OR ended_at < $2)
            ORDER BY ended_at DESC
            LIMIT $1;
            """,
            limit,
            before,
        )
    results: List[AudioTranscriptOut] = []
    for row in rows:
        payload = row["transcript"]
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                payload = {}
        elif payload is None:
            payload = {}
        results.append(
            AudioTranscriptOut(
                segment_id=row["segment_id"],
                device_id=row["device_id"],
                started_at=row["started_at"].isoformat(),
                ended_at=row["ended_at"].isoformat(),
                chunks=payload.get("chunks", []),
                is_final=payload.get("is_final", True),
            )
        )
    return results


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
    if fallback_rms < SPEECH_RMS_THRESHOLD:
        return False
    if bits_per_sample == 16 and sample_rate in SUPPORTED_VAD_RATES:
        frame_bytes = int(sample_rate * (VAD_FRAME_MS / 1000.0)) * 2
        if frame_bytes > 0 and len(raw_audio) >= frame_bytes:
            saw_frame = False
            for offset in range(0, len(raw_audio) - frame_bytes + 1, frame_bytes):
                frame = raw_audio[offset : offset + frame_bytes]
                saw_frame = True
                if vad_detector.is_speech(frame, sample_rate):
                    return True
            if saw_frame:
                return False
    return fallback_rms >= (
        SPEECH_RMS_THRESHOLD + AUDIO_GAIN_FALSE_POSITIVE_MARGIN
    )


def process_pcm_chunk(raw_audio: bytes) -> tuple[bytes, float]:
    if not raw_audio:
        return raw_audio, 0.0
    samples = array("h")
    samples.frombytes(raw_audio)
    length = len(samples)
    if length == 0:
        return raw_audio, 0.0
    sum_sq = 0.0
    for sample in samples:
        sum_sq += (sample / 32768.0) ** 2
    orig_rms = math.sqrt(sum_sq / length)
    final_rms = orig_rms
    if orig_rms >= AUDIO_GAIN_MIN_RMS and orig_rms < AUDIO_GAIN_TARGET_RMS:
        gain = min(AUDIO_GAIN_MAX, AUDIO_GAIN_TARGET_RMS / max(orig_rms, 1e-6))
        if abs(gain - 1.0) > 1e-3:
            sum_sq_out = 0.0
            for idx, sample in enumerate(samples):
                amplified = int(sample * gain)
                if amplified > 32767:
                    amplified = 32767
                elif amplified < -32768:
                    amplified = -32768
                samples[idx] = amplified
                sum_sq_out += (amplified / 32768.0) ** 2
            final_rms = math.sqrt(sum_sq_out / length)
    else:
        final_rms = orig_rms
    return samples.tobytes(), final_rms


def _bytes_per_ms(sample_rate: int, bits_per_sample: int) -> float:
    bytes_per_sample = max(1, bits_per_sample // 8)
    return (sample_rate * bytes_per_sample) / 1000.0


def _ms_to_bytes(duration_ms: int, sample_rate: int, bits_per_sample: int) -> int:
    return int(duration_ms * _bytes_per_ms(sample_rate, bits_per_sample))


def _bytes_to_ms(byte_count: int, sample_rate: int, bits_per_sample: int) -> int:
    bytes_per_ms = _bytes_per_ms(sample_rate, bits_per_sample)
    if bytes_per_ms <= 0:
        return 0
    return int(round(byte_count / bytes_per_ms))


def compute_rms_from_pcm(raw_audio: bytes, bits_per_sample: int) -> float:
    if bits_per_sample != 16 or not raw_audio:
        return 0.0
    samples = array("h")
    samples.frombytes(raw_audio)
    if not samples:
        return 0.0
    sum_sq = 0.0
    for sample in samples:
        sum_sq += (sample / 32768.0) ** 2
    return math.sqrt(sum_sq / len(samples))


def enhance_segment_pcm(
    raw_audio: bytes,
    sample_rate: int,
    bits_per_sample: int,
) -> tuple[bytes, float]:
    if bits_per_sample != 16 or not raw_audio:
        return raw_audio, compute_rms_from_pcm(raw_audio, bits_per_sample)
    samples = array("h")
    samples.frombytes(raw_audio)
    if not samples:
        return raw_audio, 0.0
    sum_sq = 0.0
    for sample in samples:
        sum_sq += (sample / 32768.0) ** 2
    orig_rms = math.sqrt(sum_sq / len(samples))
    target = max(SEGMENT_GAIN_TARGET_RMS, AUDIO_GAIN_TARGET_RMS)
    if orig_rms >= target or orig_rms <= 1e-6:
        return raw_audio, orig_rms
    gain = min(AUDIO_GAIN_MAX, target / orig_rms)
    if abs(gain - 1.0) <= 1e-3:
        return raw_audio, orig_rms
    sum_sq_out = 0.0
    for idx, sample in enumerate(samples):
        amplified = int(sample * gain)
        if amplified > 32767:
            amplified = 32767
        elif amplified < -32768:
            amplified = -32768
        samples[idx] = amplified
        sum_sq_out += (amplified / 32768.0) ** 2
    final_rms = math.sqrt(sum_sq_out / len(samples))
    return samples.tobytes(), final_rms


def _start_segment_state(
    device_id: str,
    sample_rate: int,
    bits_per_sample: int,
    started_at: datetime,
) -> AudioSegmentBuffer:
    state = AudioSegmentBuffer(
        device_id=device_id,
        sample_rate=sample_rate,
        bits_per_sample=bits_per_sample,
        started_at=started_at,
    )
    temp_path = AUDIO_SEGMENTS_WORK_DIR / f"{state.segment_id}.raw"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    if temp_path.exists():
        temp_path.unlink()
    state.temp_path = temp_path
    return state


def _extract_overlap_payload(state: AudioSegmentBuffer) -> bytes:
    if not state.buffer or SEGMENT_LOOKBACK_MS <= 0:
        return b""
    overlap_bytes = _ms_to_bytes(SEGMENT_LOOKBACK_MS, state.sample_rate, state.bits_per_sample)
    if overlap_bytes <= 0:
        return b""
    return bytes(state.buffer[-overlap_bytes:])


def _photo_extension(mime: Optional[str]) -> str:
    if not mime:
        return ".jpg"
    lowered = mime.lower()
    if "png" in lowered:
        return ".png"
    if "webp" in lowered:
        return ".webp"
    if "bmp" in lowered:
        return ".bmp"
    return ".jpg"


async def save_photo_to_disk(photo_id: str, photo_bytes: bytes, mime: Optional[str]) -> str:
    ext = _photo_extension(mime)
    filename = f"{photo_id}{ext}"
    disk_path = PHOTO_STORAGE_DIR / filename
    await asyncio.to_thread(disk_path.write_bytes, photo_bytes)
    return f"{PHOTO_STORAGE_URL_PREFIX}/{filename}"


async def persist_transcript_record(transcript: AudioTranscriptOut) -> None:
    if not db_pool:
        return
    payload = transcript.model_dump()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO ig_audio_transcripts (segment_id, device_id, transcript, started_at, ended_at)
            VALUES ($1,$2,$3::jsonb,$4,$5)
            ON CONFLICT (segment_id) DO UPDATE SET transcript = EXCLUDED.transcript,
                started_at = EXCLUDED.started_at,
                ended_at = EXCLUDED.ended_at;
            """,
            transcript.segment_id,
            transcript.device_id,
            json.dumps(payload),
            datetime.fromisoformat(transcript.started_at),
            datetime.fromisoformat(transcript.ended_at),
        )


async def fetch_transcript_by_segment(segment_id: str) -> AudioTranscriptOut | None:
    if not db_pool:
        for entry in audio_transcript_store:
            if entry.segment_id == segment_id:
                return entry
        return None
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT segment_id, device_id, transcript, started_at, ended_at
            FROM ig_audio_transcripts
            WHERE segment_id=$1
            """,
            segment_id,
        )
    if not row:
        for entry in audio_transcript_store:
            if entry.segment_id == segment_id:
                return entry
        return None
    payload = row["transcript"]
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {}
    elif payload is None:
        payload = {}
    return AudioTranscriptOut(
        segment_id=row["segment_id"],
        device_id=row["device_id"],
        started_at=row["started_at"].isoformat(),
        ended_at=row["ended_at"].isoformat(),
        chunks=payload.get("chunks", []),
        is_final=payload.get("is_final", True),
    )


@dataclass
class WhisperStreamState:
    device_id: str
    segment_id: str
    sample_rate: int
    bits_per_sample: int
    started_at: datetime
    buffer: bytearray = field(default_factory=bytearray)
    last_emit_ms: int = 0
    last_chunks: List[TranscriptChunk] = field(default_factory=list)
    threshold_index: int = 0
    active: bool = False
    has_voice_since_emit: bool = False


class WhisperStreamManager:
    def __init__(
        self,
        device: str,
        model_name: str,
        fp16: bool,
        interval_ms: int,
        history_store: deque,
        ws_manager: ConnectionManager,
    ) -> None:
        self.device = device
        self.model_name = model_name
        self.fp16 = fp16 and device.startswith("cuda")
        self.interval_ms = max(500, interval_ms)
        self.thresholds_ms = WHISPER_THRESHOLD_VALUES
        self.history_store = history_store
        self.ws_manager = ws_manager
        self.streams: Dict[str, WhisperStreamState] = {}
        self.model = None
        self.lock = asyncio.Lock()

    def _ensure_model(self):
        if self.model is None:
            self.model = whisper.load_model(self.model_name, device=self.device)

    def _pcm_bytes_to_audio(self, pcm_bytes: bytes) -> np.ndarray:
        if not pcm_bytes:
            return np.zeros(1, dtype=np.float32)
        audio = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        return audio

    def _transcribe_sync(self, audio: np.ndarray) -> List[TranscriptChunk]:
        if audio.size == 0:
            return []
        self._ensure_model()
        audio = whisper.pad_or_trim(audio)
        result = self.model.transcribe(
            audio,
            verbose=False,
            fp16=self.fp16,
            condition_on_previous_text=False,
            temperature=0.0,
        )
        chunks: List[TranscriptChunk] = []
        for seg in result.get("segments", []):
            text = (seg.get("text") or "").strip()
            if not text:
                continue
            chunks.append(
                TranscriptChunk(
                    speaker="Speaker",
                    text=text,
                    start=float(seg.get("start") or 0.0),
                    end=float(seg.get("end") or 0.0),
                )
            )
        return chunks

    async def handle_chunk(
        self,
        device_id: str,
        segment_id: str,
        started_at: datetime,
        sample_rate: int,
        bits_per_sample: int,
        raw_audio: bytes,
        speech_detected: bool,
    ) -> None:
        if not raw_audio:
            return
        async with self.lock:
            stream = self.streams.get(device_id)
            if not stream or stream.segment_id != segment_id:
                stream = WhisperStreamState(
                    device_id=device_id,
                    segment_id=segment_id,
                    sample_rate=sample_rate,
                    bits_per_sample=bits_per_sample,
                    started_at=started_at,
                )
                self.streams[device_id] = stream
            if speech_detected:
                stream.active = True
                stream.has_voice_since_emit = True
            stream.buffer.extend(raw_audio)
            buffer_ms = _bytes_to_ms(len(stream.buffer), sample_rate, bits_per_sample)
            snapshot: Optional[bytes] = None
            silence_progress_ms: Optional[int] = None
            if stream.threshold_index < len(self.thresholds_ms):
                next_threshold = self.thresholds_ms[stream.threshold_index]
                if buffer_ms >= next_threshold:
                    stream.threshold_index += 1
                    stream.last_emit_ms = next_threshold
                    if stream.has_voice_since_emit:
                        snapshot = bytes(stream.buffer)
                        stream.has_voice_since_emit = False
                    else:
                        silence_progress_ms = next_threshold
            if not snapshot and buffer_ms - stream.last_emit_ms >= self.interval_ms:
                stream.last_emit_ms = buffer_ms
                if stream.has_voice_since_emit:
                    snapshot = bytes(stream.buffer)
                    stream.has_voice_since_emit = False
                else:
                    silence_progress_ms = buffer_ms
        if snapshot:
            await self._emit_snapshot(stream, snapshot, is_final=False)
        elif silence_progress_ms is not None:
            await self._emit_silence_progress(stream, silence_progress_ms)

    async def finalize_segment(
        self,
        record: AudioSegmentRecord,
        pcm_payload: bytes,
    ) -> None:
        has_voice = False
        async with self.lock:
            current = self.streams.get(record.device_id)
            if current and current.segment_id == record.id:
                has_voice = current.active
                del self.streams[record.device_id]
        if not has_voice:
            await self._emit_silence(record)
            return
        await self._emit_from_pcm(
            device_id=record.device_id,
            segment_id=record.id,
            started_at=record.started_at,
            ended_at=record.ended_at,
            sample_rate=record.sample_rate,
            bits_per_sample=record.bits_per_sample,
            pcm_payload=pcm_payload,
            is_final=True,
        )

    async def _emit_snapshot(
        self,
        stream: WhisperStreamState,
        pcm_snapshot: bytes,
        is_final: bool,
    ) -> None:
        await self._emit_from_pcm(
            device_id=stream.device_id,
            segment_id=stream.segment_id,
            started_at=stream.started_at,
            ended_at=datetime.now(tz=timezone.utc),
            sample_rate=stream.sample_rate,
            bits_per_sample=stream.bits_per_sample,
            pcm_payload=pcm_snapshot,
            is_final=is_final,
        )

    async def _emit_from_pcm(
        self,
        device_id: str,
        segment_id: str,
        started_at: datetime,
        ended_at: datetime,
        sample_rate: int,
        bits_per_sample: int,
        pcm_payload: bytes,
        is_final: bool,
    ) -> None:
        chunks = await asyncio.to_thread(
            self._transcribe_sync,
            self._pcm_bytes_to_audio(pcm_payload),
        )
        if not chunks:
            return
        transcript = AudioTranscriptOut(
            segment_id=segment_id,
            device_id=device_id,
            started_at=started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            chunks=chunks,
            is_final=is_final,
        )
        if is_final:
            self.history_store.appendleft(transcript)
            await persist_transcript_record(transcript)
        await self.ws_manager.broadcast({"type": "audio_transcript", "payload": transcript.model_dump()})

    async def _emit_silence_progress(
        self,
        stream: WhisperStreamState,
        progress_ms: int,
    ) -> None:
        transcript = AudioTranscriptOut(
            segment_id=stream.segment_id,
            device_id=stream.device_id,
            started_at=stream.started_at.isoformat(),
            ended_at=(stream.started_at + timedelta(milliseconds=progress_ms)).isoformat(),
            chunks=[
                TranscriptChunk(
                    speaker="Silence",
                    text="(silence)",
                    start=0.0,
                    end=progress_ms / 1000.0,
                )
            ],
            is_final=False,
        )
        await self.ws_manager.broadcast({"type": "audio_transcript", "payload": transcript.model_dump()})

    async def _emit_silence(self, record: AudioSegmentRecord) -> None:
        transcript = AudioTranscriptOut(
            segment_id=record.id,
            device_id=record.device_id,
            started_at=record.started_at.isoformat(),
            ended_at=record.ended_at.isoformat(),
            chunks=[
                TranscriptChunk(
                    speaker="Silence",
                    text="(silence)",
                    start=0.0,
                    end=float(record.duration_ms) / 1000.0,
                )
            ],
            is_final=True,
        )
        self.history_store.appendleft(transcript)
        await persist_transcript_record(transcript)
        await self.ws_manager.broadcast({"type": "audio_transcript", "payload": transcript.model_dump()})


whisper_stream_manager: WhisperStreamManager | None = (
    WhisperStreamManager(
        device=WHISPER_DEVICE,
        model_name=WHISPER_MODEL_NAME,
        fp16=WHISPER_FP16,
        interval_ms=WHISPER_STREAM_INTERVAL_MS,
        history_store=audio_transcript_store,
        ws_manager=manager,
    )
    if TRANSCRIPTION_ENABLED and whisper
    else None
)


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
    if not state.buffer and not (state.temp_path and state.temp_path.exists()):
        return False
    silence_ms = _silence_duration_ms(state, now)
    if state.duration_ms >= SEGMENT_MAX_MS or state.duration_ms >= SEGMENT_TARGET_MS:
        return True
    if (
        not speech_detected
        and state.duration_ms >= MIN_SEGMENT_MS
        and silence_ms >= max(SILENCE_FORCE_FLUSH_MS, SEGMENT_TARGET_MS)
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
    buffer_has_data = bool(state.buffer)
    temp_file_bytes = None
    if state.temp_path and state.temp_path.exists():
        try:
            temp_file_bytes = state.temp_path.read_bytes()
        except Exception as exc:
            print(f"[Audio] Failed to read segment temp file {state.segment_id}: {exc}")
        finally:
            try:
                state.temp_path.unlink()
            except FileNotFoundError:
                pass
    if not buffer_has_data and not temp_file_bytes:
        return
    ended_at = state.last_chunk_at or state.started_at
    pcm_payload = temp_file_bytes if temp_file_bytes is not None else bytes(state.buffer)
    if not pcm_payload:
        return
    duration_ms = _bytes_to_ms(len(pcm_payload), state.sample_rate, state.bits_per_sample) or state.duration_ms
    enhanced_pcm, enhanced_rms = enhance_segment_pcm(
        pcm_payload,
        state.sample_rate,
        state.bits_per_sample,
    )
    wav_payload = pcm_to_wav(enhanced_pcm, state.sample_rate, state.bits_per_sample)
    record = AudioSegmentRecord(
        id=state.segment_id,
        device_id=state.device_id,
        sample_rate=state.sample_rate,
        bits_per_sample=state.bits_per_sample,
        duration_ms=duration_ms,
        rms=enhanced_rms,
        started_at=state.started_at,
        ended_at=ended_at,
    )
    filename = f"{record.id}.wav"
    disk_path = AUDIO_SEGMENTS_DIR / filename
    try:
        # Offload final WAV write to thread
        await asyncio.to_thread(disk_path.write_bytes, wav_payload)
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
    if whisper_stream_manager:
        schedule_background(
            whisper_stream_manager.finalize_segment(record, enhanced_pcm),
            "whisper_stream_finalize",
        )
    state.temp_path = None




async def append_audio_to_segment_buffers(
    chunk: AudioChunkOut,
    raw_audio: bytes,
    speech_detected: bool,
) -> SegmentAppendResult:
    now = datetime.fromisoformat(chunk.created_at)
    segments_to_flush: List[AudioSegmentBuffer] = []
    result = SegmentAppendResult()
    transcript_args: Optional[tuple[str, str, datetime, int, int]] = None
    async with segment_lock:
        bucket = segment_states.setdefault(chunk.device_id, [])

        state = bucket[-1] if bucket else None
        if (
            not state
            or state.sample_rate != chunk.sample_rate
            or state.bits_per_sample != chunk.bits_per_sample
        ):
            state = _start_segment_state(
                chunk.device_id,
                chunk.sample_rate,
                chunk.bits_per_sample,
                now,
            )
            bucket.append(state)

        state.buffer.extend(raw_audio)
        await append_chunk_to_file(state, raw_audio)
        state.duration_ms += chunk.duration_ms
        state.rms_accumulator += chunk.rms
        state.rms_count += 1
        state.last_chunk_at = now
        if speech_detected:
            state.last_voice_at = now

        progress_ms = min(state.duration_ms, SEGMENT_TARGET_MS)
        result = SegmentAppendResult(segment_id=state.segment_id, duration_ms=progress_ms)
        transcript_args = (
            state.device_id,
            state.segment_id,
            state.started_at,
            state.sample_rate,
            state.bits_per_sample,
            speech_detected,
        )

        if _should_finalize_segment(state, now, speech_detected):
            segments_to_flush.append(bucket.pop())
            overlap_payload = _extract_overlap_payload(state)
            new_state = _start_segment_state(
                chunk.device_id,
                chunk.sample_rate,
                chunk.bits_per_sample,
                now,
            )
            if overlap_payload:
                new_state.buffer.extend(overlap_payload)
                await append_chunk_to_file(new_state, overlap_payload)
                overlap_ms = _bytes_to_ms(
                    len(overlap_payload),
                    new_state.sample_rate,
                    new_state.bits_per_sample,
                )
                new_state.duration_ms += overlap_ms
                overlap_rms = compute_rms_from_pcm(
                    overlap_payload,
                    new_state.bits_per_sample,
                )
                new_state.rms_accumulator += overlap_rms
                new_state.rms_count += 1
                new_state.last_chunk_at = now
                if speech_detected:
                    new_state.last_voice_at = now
            bucket.append(new_state)

        # Flush idle segments except most recent
        for stale_state in list(bucket[:-1]):
            idle_ms = (
                (now - stale_state.last_chunk_at).total_seconds() * 1000
                if stale_state.last_chunk_at
                else SEGMENT_IDLE_FLUSH_MS + 1
            )
            if idle_ms >= SEGMENT_IDLE_FLUSH_MS:
                bucket.remove(stale_state)
                segments_to_flush.append(stale_state)

        if not bucket:
            segment_states.pop(chunk.device_id, None)

    for segment in segments_to_flush:
        if segment:
            await _flush_segment_state(segment)
    if whisper_stream_manager and transcript_args:
        device_id, segment_id, started_at, sample_rate, bits_per_sample, speech_flag = transcript_args
        schedule_background(
            whisper_stream_manager.handle_chunk(
                device_id,
                segment_id,
                started_at,
                sample_rate,
                bits_per_sample,
                raw_audio,
                speech_flag,
            ),
            "whisper_stream_chunk",
        )
    return result


async def flush_idle_segments(force: bool = False) -> None:
    now = datetime.now(tz=timezone.utc)
    to_flush: List[AudioSegmentBuffer] = []
    async with segment_lock:
        for device_id, bucket in list(segment_states.items()):
            for state in list(bucket):
                if not state.last_chunk_at:
                    continue
                idle_ms = (now - state.last_chunk_at).total_seconds() * 1000
                if force or (
                    idle_ms >= SEGMENT_IDLE_FLUSH_MS and state.duration_ms >= MIN_SEGMENT_MS
                ):
                    bucket.remove(state)
                    to_flush.append(state)
            if not bucket:
                del segment_states[device_id]
    for segment in to_flush:
        if segment:
            await _flush_segment_state(segment)


async def segment_housekeeper():
    while True:
        await asyncio.sleep(2)
        await flush_idle_segments()


def _decode_audio_payload(payload: AudioChunkIn) -> tuple[bytes, float, bool]:
    try:
        raw_audio = base64.b64decode(payload.audio_base64.encode(), validate=True)
    except Exception as exc:
        raise ValueError(f"Invalid audio_base64 data: {exc}") from exc
    raw_audio, computed_rms = process_pcm_chunk(raw_audio)
    speech_detected = detect_speech(
        raw_audio,
        payload.sample_rate,
        payload.bits_per_sample,
        computed_rms,
    )
    return raw_audio, computed_rms, speech_detected


async def process_audio_payload(payload: AudioChunkIn) -> AudioChunkOut:
    raw_audio, computed_rms, speech_detected = _decode_audio_payload(payload)
    chunk_id = str(uuid.uuid4())
    now = datetime.now(tz=timezone.utc)
    chunk = AudioChunkOut(
        id=chunk_id,
        device_id=payload.device_id,
        sample_rate=payload.sample_rate,
        bits_per_sample=payload.bits_per_sample,
        duration_ms=payload.duration_ms,
        rms=round(computed_rms, 4),
        created_at=now.isoformat(),
        audio_url=f"/api/v1/audio/{chunk_id}",
        speech_detected=speech_detected,
    )
    append_result = await append_audio_to_segment_buffers(chunk, raw_audio, speech_detected)
    chunk.segment_duration_ms = append_result.duration_ms
    chunk.active_segment_id = append_result.segment_id

    audio_store.append(chunk)
    schedule_background(
        persist_audio_chunk(chunk, raw_audio),
        "persist_audio_chunk",
    )
    print(
        "[Audio] Forward chunk "
        f"{chunk.device_id}#{chunk.id} rms={chunk.rms:.4f} speech={speech_detected} "
        f"segment={chunk.active_segment_id or 'n/a'} progress={chunk.segment_duration_ms or 0}ms"
    )
    await manager.broadcast({"type": "audio_chunk", "payload": chunk.model_dump()})
    return chunk


async def process_message_payload(payload: MessageIn) -> MessageOut:
    entry = _make_entry(payload)
    photo_bytes: Optional[bytes] = None
    photo_id: Optional[str] = None
    if payload.photo_base64:
        try:
            photo_bytes = base64.b64decode(payload.photo_base64.encode(), validate=True)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid photo_base64 data: {exc}") from exc
        photo_id = str(uuid.uuid4())
        if db_pool:
            entry.photo_url = f"/api/v1/photos/{photo_id}"
        else:
            entry.photo_url = await save_photo_to_disk(photo_id, photo_bytes, payload.photo_mime)

    message_store.append(entry)
    if photo_bytes and db_pool:
        await persist_entry(entry, photo_bytes, payload.photo_mime, photo_id)
    else:
        schedule_background(
            persist_entry(entry, photo_bytes, payload.photo_mime, photo_id),
            "persist_entry",
        )
    await manager.broadcast({"type": "message", "payload": entry.model_dump()})
    return entry


@app.post("/api/v1/messages", response_model=MessageOut)
async def ingest_message(payload: MessageIn):
    return await process_message_payload(payload)


@app.websocket("/ws/photo-ingest")
async def photo_ingest_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text_message = await websocket.receive_text()
            try:
                payload_dict = json.loads(text_message)
            except json.JSONDecodeError as exc:
                print(f"[Photo][WS] Dropping invalid JSON payload: {exc}")
                continue
            try:
                message_payload = MessageIn(**payload_dict)
            except ValidationError as exc:
                print(f"[Photo][WS] Validation failed: {exc}")
                continue
            try:
                await process_message_payload(message_payload)
            except HTTPException as exc:
                print(f"[Photo][WS] Failed to process payload: {exc.detail}")
                continue
    except WebSocketDisconnect:
        pass


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
        chunk = await process_audio_payload(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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
        transcripts_history = await fetch_audio_transcripts(limit=20)
        await websocket.send_json(
            {"type": "history_audio_transcripts", "data": [t.model_dump() for t in transcripts_history]}
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.websocket("/ws/audio-ingest")
async def audio_ingest_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text_message = await websocket.receive_text()
            try:
                payload_dict = json.loads(text_message)
            except json.JSONDecodeError as exc:
                print(f"[Audio][WS] Dropping invalid JSON payload: {exc}")
                continue
            try:
                chunk_payload = AudioChunkIn(**payload_dict)
            except ValidationError as exc:
                print(f"[Audio][WS] Validation failed: {exc}")
                continue
            try:
                await process_audio_payload(chunk_payload)
            except ValueError as exc:
                print(f"[Audio][WS] Failed to process chunk: {exc}")
                continue
    except WebSocketDisconnect:
        pass


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


@app.get("/api/v1/audio/segments/{segment_id}/transcript", response_model=AudioTranscriptOut)
async def get_audio_segment_transcript(segment_id: str):
    transcript = await fetch_transcript_by_segment(segment_id)
    if transcript:
        return transcript
    raise HTTPException(status_code=404, detail="Transcript not found.")


@app.get("/healthz")
async def healthcheck():
    return {
        "status": "ok",
        "messages": len(message_store),
        "segment_target_ms": SEGMENT_TARGET_MS,
        "segment_overlap_ms": SEGMENT_OVERLAP_MS,
    }


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


async def append_chunk_to_file(state: AudioSegmentBuffer, raw_audio: bytes) -> None:
    if not state.temp_path:
        return
    try:
        # Offload disk I/O to thread to avoid blocking the event loop
        def _append(path: Path, data: bytes) -> None:
            with path.open("ab") as temp_file:
                temp_file.write(data)

        await asyncio.to_thread(_append, state.temp_path, raw_audio)
    except Exception as exc:
        print(f"[Audio] Failed to append segment {state.segment_id}: {exc}")
