"""Application settings for the IdeasGlass Tornado stack."""

from __future__ import annotations

import json
from typing import Dict

from pydantic import BaseModel, Field, HttpUrl, PostgresDsn, model_validator


class Settings(BaseModel):
    debug: bool = Field(default=False, validation_alias="DEBUG")
    api_prefix: str = Field(default="/api/v1", validation_alias="API_PREFIX")
    postgres_dsn: PostgresDsn = Field(
        default="postgresql://lachlan@localhost/ideasglass_db",
        validation_alias="POSTGRES_DSN",
    )
    listen_host: str = Field(default="0.0.0.0", validation_alias="LISTEN_HOST")
    listen_port: int = Field(default=8081, validation_alias="LISTEN_PORT")
    telemetry_retention_days: int = Field(
        default=30, validation_alias="TELEMETRY_RETENTION_DAYS"
    )
    device_secret_header: str = Field(
        default="X-Device-Secret", validation_alias="DEVICE_SECRET_HEADER"
    )
    device_secrets_raw: str = Field(
        default="{}", validation_alias="DEVICE_SECRETS"
    )  # JSON string
    upload_base_url: HttpUrl = Field(
        default="https://ideasglass.local/uploads", validation_alias="UPLOAD_BASE_URL"
    )

    device_secrets: Dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _parse_secrets(self) -> "Settings":
        try:
            secrets = json.loads(self.device_secrets_raw)
            if not isinstance(secrets, dict):
                raise ValueError("DEVICE_SECRETS must decode to an object")
            self.device_secrets = {str(k): str(v) for k, v in secrets.items()}
        except json.JSONDecodeError as exc:  # pragma: no cover - config only
            raise ValueError(f"Invalid DEVICE_SECRETS JSON: {exc}") from exc
        return self


settings = Settings()
