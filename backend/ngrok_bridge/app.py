from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


class MessageIn(BaseModel):
    device_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4096)
    meta: Dict[str, str] | None = None


class MessageOut(BaseModel):
    id: str
    device_id: str
    message: str
    meta: Dict[str, str] | None
    received_at: str


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


def _make_entry(payload: MessageIn) -> MessageOut:
    now = datetime.now(tz=timezone.utc)
    entry = MessageOut(
        id=f"{payload.device_id}-{int(now.timestamp()*1000)}",
        device_id=payload.device_id,
        message=payload.message,
        meta=payload.meta or {},
        received_at=now.isoformat(),
    )
    return entry


@app.post("/api/v1/messages", response_model=MessageOut)
async def ingest_message(payload: MessageIn):
    entry = _make_entry(payload)
    message_store.append(entry)
    await manager.broadcast(entry.model_dump())
    return entry


@app.get("/api/v1/messages", response_model=List[MessageOut])
async def list_messages():
    return list(message_store)


@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send recent history upon connection
        await websocket.send_json({"type": "history", "data": [m.model_dump() for m in message_store]})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok", "messages": len(message_store)}


@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
