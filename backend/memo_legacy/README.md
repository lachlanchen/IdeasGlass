# AI Memo Backend (alias of IdeasGlass)

This is a thin wrapper around the main IdeasGlass FastAPI app so you can run a second instance on a different port while sharing the same database (`ideasglass_db`) and media paths.

## Run

```bash
DATABASE_URL="postgresql://lachlan:the11thfzpe.g.@localhost/ideasglass_db" \
IDEASGLASS_WHISPER_MODEL=large-v3-turbo \
IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.memo.app:app --host 0.0.0.0 --port 8875 --proxy-headers --forwarded-allow-ips="*" --reload
```

Or via the helper:
```bash
python backend/memo/serve.py --port 8875 --host 0.0.0.0 --reload
```

Everything else (routes, static assets, media storage) matches `backend/glass`.
