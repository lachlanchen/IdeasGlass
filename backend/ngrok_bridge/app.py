#from
from __future__ import annotations

import asyncio
import base64
import json
import os
import uuid
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

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

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


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
DATABASE_URL = os.getenv("DATABASE_URL")
db_pool: asyncpg.pool.Pool | None = None


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


@app.on_event("startup")
async def startup_event():
    global db_pool
    if not DATABASE_URL:
        print("[DB] DATABASE_URL not set; running in in-memory mode.")
        return
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
        await init_db()
        print("[DB] Connected to Postgres and ensured tables exist.")
    except Exception as exc:
        print(f"[DB] Failed to initialize Postgres: {exc}")
        db_pool = None


@app.on_event("shutdown")
async def shutdown_event():
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None


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


async def fetch_messages(limit: int = 100) -> List[MessageOut]:
    if not db_pool:
        return list(message_store)
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
            ORDER BY m.received_at DESC
            LIMIT $1;
            """,
            limit,
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
    await manager.broadcast(entry.model_dump())
    return entry


@app.get("/api/v1/messages", response_model=List[MessageOut])
async def list_messages():
    return await fetch_messages()


@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send recent history upon connection
        history = await fetch_messages(limit=50)
        await websocket.send_json({"type": "history", "data": [m.model_dump() for m in history]})
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


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok", "messages": len(message_store)}


@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
