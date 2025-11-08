"""Async Postgres helpers."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional, Tuple

import asyncpg

from .config import settings
from .models import PhotoPayload, TelemetryPayload

_pool: Optional[asyncpg.pool.Pool] = None
_pool_lock = asyncio.Lock()


async def get_pool() -> asyncpg.pool.Pool:
    global _pool
    if _pool:
        return _pool
    async with _pool_lock:
        if not _pool:
            _pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)
    return _pool


async def upsert_device(conn: asyncpg.Connection, payload: TelemetryPayload) -> None:
    await conn.execute(
        """
        INSERT INTO devices (device_id, hardware_rev, firmware_version, last_seen_at)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (device_id) DO UPDATE SET
            hardware_rev = EXCLUDED.hardware_rev,
            firmware_version = EXCLUDED.firmware_version,
            last_seen_at = EXCLUDED.last_seen_at;
        """,
        payload.device_id,
        payload.hardware,
        payload.firmware,
        payload.recorded_at(),
    )


async def insert_photo(conn: asyncpg.Connection, payload: TelemetryPayload, photo: PhotoPayload) -> Dict[str, Any]:
    row = await conn.fetchrow(
        """
        INSERT INTO photos (photo_id, device_id, size_bytes, crc32, storage_url, taken_at, backend_status)
        VALUES ($1, $2, $3, $4, $5, $6, 'pending')
        ON CONFLICT (photo_id) DO UPDATE SET
            size_bytes = EXCLUDED.size_bytes,
            crc32 = EXCLUDED.crc32,
            storage_url = EXCLUDED.storage_url,
            taken_at = EXCLUDED.taken_at,
            backend_status = 'pending'
        RETURNING photo_id, storage_url, backend_status;
        """,
        photo.id,
        payload.device_id,
        photo.size,
        photo.crc32,
        photo.storage_url,
        payload.recorded_at(),
    )
    return dict(row)


async def insert_telemetry(payload: TelemetryPayload) -> Tuple[int, Optional[Dict[str, Any]]]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await upsert_device(conn, payload)
            raw_payload = payload.model_dump()
            row = await conn.fetchrow(
                """
                INSERT INTO telemetry_events (
                    device_id,
                    recorded_at,
                    raw_payload,
                    battery_percent,
                    mic_level,
                    ambient_lux,
                    button_state,
                    quat,
                    accel
                )
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                RETURNING id;
                """,
                payload.device_id,
                payload.recorded_at(),
                raw_payload,
                payload.battery,
                payload.mic_level,
                payload.ambient_lux,
                payload.button,
                payload.quat,
                payload.accel,
            )
            photo_meta = None
            if payload.photo:
                photo_meta = await insert_photo(conn, payload, payload.photo)
    return row["id"], photo_meta
