"""Pydantic models shared by handlers and database logic."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import (
    BaseModel,
    Field,
    conint,
    confloat,
    conlist,
    constr,
)


class PhotoPayload(BaseModel):
    id: constr(min_length=3, max_length=64)
    size: conint(gt=0)
    crc32: Optional[conint(ge=0)]
    storage_url: Optional[str] = None


class TelemetryPayload(BaseModel):
    device_id: constr(min_length=3, max_length=64)
    ts: conint(ge=0) = Field(default_factory=lambda: int(datetime.now(tz=timezone.utc).timestamp()))
    firmware: Optional[str] = None
    hardware: Optional[str] = None
    battery: Optional[conint(ge=0, le=100)] = None
    voltage: Optional[confloat(ge=0)] = None
    ambient_lux: Optional[confloat(ge=0)] = None
    mic_level: Optional[confloat(ge=0)] = None
    button: Optional[bool] = None
    quat: Optional[conlist(float, min_length=4, max_length=4)] = None
    accel: Optional[conlist(float, min_length=3, max_length=3)] = None
    photo: Optional[PhotoPayload] = None
    extras: Dict[str, Any] = Field(default_factory=dict)

    def recorded_at(self) -> datetime:
        return datetime.fromtimestamp(self.ts, tz=timezone.utc)


class WebsocketEnvelope(BaseModel):
    type: str
    payload: Dict[str, Any]
