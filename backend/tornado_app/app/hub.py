"""In-memory websocket hub to fan out device updates."""

from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import DefaultDict, Set

from tornado.websocket import WebSocketHandler


class WebsocketHub:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._clients: DefaultDict[str, Set[WebSocketHandler]] = defaultdict(set)

    async def register(self, device_id: str, handler: WebSocketHandler) -> None:
        async with self._lock:
            self._clients[device_id].add(handler)

    async def unregister(self, device_id: str, handler: WebSocketHandler) -> None:
        async with self._lock:
            if device_id in self._clients and handler in self._clients[device_id]:
                self._clients[device_id].remove(handler)
                if not self._clients[device_id]:
                    del self._clients[device_id]

    async def broadcast(self, device_id: str, message: dict) -> None:
        payload = json.dumps(message)
        async with self._lock:
            clients = list(self._clients.get(device_id, set()))
        for client in clients:
            try:
                client.write_message(payload)
            except Exception:
                pass
