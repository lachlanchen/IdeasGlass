"""Tornado application factory."""

from __future__ import annotations

import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.web

from .config import settings
from .handlers import DeviceSocketHandler, HealthHandler, IngestHandler
from .hub import WebsocketHub


def make_app(hub: WebsocketHub | None = None) -> tornado.web.Application:
    ws_hub = hub or WebsocketHub()
    return tornado.web.Application(
        [
            (r"/healthz", HealthHandler),
            (rf"{settings.api_prefix}/ingest", IngestHandler),
            (r"/ws/devices/(?P<device_id>[^/]+)", DeviceSocketHandler, dict(hub=ws_hub, app_settings=settings)),
        ],
        debug=settings.debug,
        app_settings=settings,
        ws_hub=ws_hub,
    )


async def _main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(settings.listen_port, address=settings.listen_host)
    server.start()
    print(f"[IdeasGlass Tornado] Listening on {settings.listen_host}:{settings.listen_port}")
    await asyncio.Event().wait()


def run():
    asyncio.run(_main())


if __name__ == "__main__":
    run()
