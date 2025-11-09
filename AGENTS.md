# Repository Guidelines

## Project Structure & Module Organization
- `backend/bridge/` — FastAPI app (`app.py`), static dashboard assets, audio-processing scripts, and requirements. Audio segments land under `audio_segments/`.
- `IdeaGlass/firmware/ideasglass_arduino/` — ESP32 firmware streaming PCM chunks to the backend.
- `docs/` — Technical write-ups (`ideasglass_bridge.md`) describing deployment details.
- Root-level `README.md` plus supporting directories (`app/`, `private/`, etc.) hold ancillary experiments; focus your contributions on `backend/bridge/` unless otherwise requested.

## Build, Test, and Development Commands
- **Install deps:** `cd backend/bridge && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- **Run backend:** `uvicorn backend.bridge.app:app --host 0.0.0.0 --port 8765 --reload`.
- **Firmware build:** open the Arduino sketch in `IdeaGlass/.../IdeasGlassClient.ino` and flash with PSRAM enabled.
- **Static checks:** `python -m compileall backend/bridge/app.py` is used to confirm syntax before committing.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation, type hints, and descriptive helper names (`whisper_stream_manager`, `flush_idle_segments`). Follow FastAPI conventions for route handlers and schemas (Pydantic models in PascalCase).
- JavaScript favors modern ES modules with camelCase functions and concise helpers; keep DOM IDs and CSS class names descriptive (`transcriptPanel`, `.transcript-live-text`).
- C++/Arduino code uses mixed camelCase with explicit `const` values; keep pin definitions and Wi-Fi constants in `config.h`.

## Testing Guidelines
- No formal unit-test harness exists; rely on `python -m compileall` for syntax validation and manual end-to-end tests (backend + firmware + WebSocket dashboard).
- When changing audio flows, tail the backend logs and confirm WebSocket events render correctly in the browser console (`[IdeasGlass][wave] …` traces).

## Commit & Pull Request Guidelines
- Commits follow short, action-driven subjects (`Add streaming Whisper layer`, `Preload cuDNN for WhisperX`). Use present tense and keep scope focused.
- **Always commit and push after each change.** Keep the history linear and easy to bisect; avoid stacking unpushed work.
- PRs should describe the feature/fix, mention relevant env vars (e.g., `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`), and include testing notes (backend logs, dashboard screenshots, firmware output).
- Link issues or TODOs when applicable, and call out any required secrets (ngrok domain, Hugging Face token) in the PR body.

## Security & Configuration Tips
- Store secrets in the environment (`DATABASE_URL`, `IDEASGLASS_WHISPER_MODEL`, `HUGGINGFACE_TOKEN`); never commit them.
- CUDA/cuDNN libraries are auto-detected, but ensure the backend runs inside the `glass` conda env to pick up Whisper/FastAPI dependencies.
