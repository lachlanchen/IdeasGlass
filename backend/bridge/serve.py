#!/usr/bin/env python3
import argparse
import os
import uvicorn


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve IdeasGlass backend with optional Whisper overrides")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8765")))
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # Whisper overrides
    parser.add_argument("--whisper-model", default=os.getenv("IDEASGLASS_WHISPER_MODEL", "base"))
    parser.add_argument("--whisper-device", default=os.getenv("IDEASGLASS_WHISPER_DEVICE", "cuda"))
    parser.add_argument(
        "--whisper-fp16",
        type=int,
        choices=(0, 1),
        default=int((os.getenv("IDEASGLASS_WHISPER_FP16", "1").lower() not in {"0", "false"})),
        help="Use FP16 (1) or FP32 (0)",
    )

    args, _ = parser.parse_known_args()

    # Export to env that app.py reads
    os.environ["IDEASGLASS_WHISPER_MODEL"] = str(args.whisper_model)
    os.environ["IDEASGLASS_WHISPER_DEVICE"] = str(args.whisper_device)
    os.environ["IDEASGLASS_WHISPER_FP16"] = "1" if int(args.whisper_fp16) == 1 else "0"

    uvicorn.run(
        "backend.bridge.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
