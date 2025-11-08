"""HTTP + WebSocket handlers for the IdeasGlass Tornado app."""

from __future__ import annotations

import json
from typing import Any, Dict

import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop

from .config import Settings, settings as app_settings
from .db import insert_telemetry
from .hub import WebsocketHub
from .models import TelemetryPayload, WebsocketEnvelope


class BaseHandler(tornado.web.RequestHandler):
    @property
    def app_settings(self) -> Settings:
        return self.application.settings["app_settings"]

    @property
    def hub(self) -> WebsocketHub:
        return self.application.settings["ws_hub"]


class HealthHandler(BaseHandler):
    async def get(self):
        self.write({"status": "ok", "name": self.app_settings.api_prefix})


class IngestHandler(BaseHandler):
    async def post(self):
        try:
            body = json.loads(self.request.body or "{}")
        except json.JSONDecodeError:
            raise tornado.web.HTTPError(400, reason="Invalid JSON")

        payload = TelemetryPayload.model_validate(body)
        header_name = self.app_settings.device_secret_header
        provided_secret = self.request.headers.get(header_name, "")
        expected_secret = self.app_settings.device_secrets.get(payload.device_id)

        if expected_secret and expected_secret != provided_secret:
            raise tornado.web.HTTPError(401, reason="Invalid device secret")

        telemetry_id, photo_meta = await insert_telemetry(payload)

        response: Dict[str, Any] = {
            "telemetry_id": telemetry_id,
            "recorded_at": payload.recorded_at().isoformat(),
        }

        if payload.photo:
            upload_url = (
                f"{self.app_settings.upload_base_url.rstrip('/')}/{payload.photo.id}"
            )
            response["upload_url"] = upload_url

        envelope = WebsocketEnvelope(
            type="telemetry",
            payload={
                "device_id": payload.device_id,
                "ts": payload.ts,
                "battery": payload.battery,
                "ambient_lux": payload.ambient_lux,
                "mic_level": payload.mic_level,
                "photo": payload.photo.model_dump() if payload.photo else None,
            },
        )
        IOLoop.current().spawn_callback(
            self.hub.broadcast, payload.device_id, envelope.model_dump()
        )

        self.write(response)


class DeviceSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, hub: WebsocketHub, app_settings: Settings):
        self.hub = hub
        self.app_settings = app_settings
        self.device_id: str | None = None

    def check_origin(self, origin: str) -> bool:  # noqa: D401
        """Allow cross-origin requests so the Flutter PWA can connect."""
        return True

    async def open(self, device_id: str):
        self.device_id = device_id
        await self.hub.register(device_id, self)
        self.write_message({"type": "connected", "device_id": device_id})

    async def on_close(self):
        if self.device_id:
            await self.hub.unregister(self.device_id, self)

    async def on_message(self, message: str):
        # Commands from apps can be forwarded to the wearable here.
        self.write_message({"type": "ack", "echo": message})
