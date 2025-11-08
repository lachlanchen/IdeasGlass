BEGIN;

CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    hardware_rev TEXT,
    firmware_version TEXT,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE TABLE IF NOT EXISTS telemetry_events (
    id BIGSERIAL PRIMARY KEY,
    device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    recorded_at TIMESTAMPTZ NOT NULL,
    raw_payload JSONB NOT NULL,
    battery_percent SMALLINT,
    mic_level REAL,
    ambient_lux REAL,
    button_state BOOLEAN,
    quat REAL[],
    accel REAL[],
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS telemetry_device_time_idx
    ON telemetry_events (device_id, recorded_at DESC);

CREATE TABLE IF NOT EXISTS photos (
    photo_id TEXT PRIMARY KEY,
    device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    size_bytes INTEGER NOT NULL,
    crc32 BIGINT,
    storage_url TEXT,
    backend_status TEXT NOT NULL DEFAULT 'pending',
    taken_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMIT;
