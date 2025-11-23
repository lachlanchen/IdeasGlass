#!/usr/bin/env python3
import argparse
import os

import uvicorn


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve Memo backend (alias of IdeasGlass) on an alternate port")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8875")))
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args, _ = parser.parse_known_args()

    uvicorn.run(
        "backend.memo.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
