#!/usr/bin/env python3
"""
Prefetch Whisper models (e.g., medium, large-v3) and run a quick load test.

Usage examples:
  source ~/miniconda3/bin/activate glass
  python backend/ngrok_bridge/tools/prefetch_whisper_models.py --models medium,large-v3 --device cuda --fp16 1
  python backend/ngrok_bridge/tools/prefetch_whisper_models.py --models base,small --device cpu --fp16 0

This will download the specified models into the standard cache (usually ~/.cache/whisper),
then load each model and run a tiny encode pass to confirm it works on the chosen device.
"""

import argparse
import sys

try:
    import torch
    import numpy as np
    import whisper  # openai/whisper
except Exception as exc:
    print("This script requires torch, numpy and openai-whisper (pip install torch numpy git+https://github.com/openai/whisper)")
    raise


def test_model(model, device: str) -> None:
    # 1 second of silence at 16 kHz
    audio = np.zeros(16000, dtype=np.float32)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(device)
    with torch.no_grad():
        _ = model.encode(mel)


def main() -> int:
    ap = argparse.ArgumentParser(description="Prefetch Whisper models and run a quick encode test")
    ap.add_argument("--models", default="medium,large-v3", help="Comma-separated list, e.g. tiny,base,small,medium,large-v3")
    ap.add_argument("--device", default="cuda", choices=("cpu", "cuda"))
    ap.add_argument("--fp16", type=int, default=1, choices=(0, 1), help="Use FP16 when 1 and device=cuda")
    args = ap.parse_args()

    names = [m.strip() for m in args.models.split(",") if m.strip()]
    print(f"[Prefetch] Models: {names} | device={args.device} fp16={args.fp16}")

    if args.device == "cuda" and not torch.cuda.is_available():
        print("[Prefetch] CUDA not available; falling back to CPU")
        args.device = "cpu"

    for name in names:
        print(f"[Prefetch] Loading '{name}' …")
        model = whisper.load_model(name, device=args.device)
        if args.device == "cuda" and args.fp16:
            # Nothing extra to do; whisper uses fp16 automatically on cuda.
            pass
        else:
            # Force fp32 on CPU or when fp16 is disabled.
            for p in model.parameters():
                p.data = p.data.float()
        print(f"[Prefetch] Running encode test on '{name}' …")
        test_model(model, args.device)
        print(f"[Prefetch] OK: {name} on {args.device}")
    print("[Prefetch] All done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

