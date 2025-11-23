# IdeasGlass

> Real-time capture, stream, and recall across audio + photos — tuned for ESP32-S3 glasses and a FastAPI backend.

<style>
:root {
  --bg: #0c1117;
  --card: #111826;
  --muted: #9fb3c8;
  --accent: #7dd3fc;
  --accent-strong: #22d3ee;
  --radius: 14px;
  --shadow: 0 18px 50px rgba(0,0,0,0.35);
  --border: 1px solid rgba(255,255,255,0.06);
}
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #f8fafc;
  background: linear-gradient(145deg, #0c1117, #0f172a 55%, #0b1220);
  margin: 0;
  padding: 0;
}
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 18px 80px;
}
.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  align-items: center;
}
.hero-card, .card {
  background: var(--card);
  border: var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 22px 24px;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(125, 211, 252, 0.12);
  color: var(--accent);
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.02em;
}
.buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.08);
  color: #0b1220;
  background: linear-gradient(120deg, #7dd3fc, #22d3ee);
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 12px 30px rgba(34, 211, 238, 0.25);
  transition: transform 120ms ease, box-shadow 120ms ease;
}
.btn:hover { transform: translateY(-1px); box-shadow: 0 16px 35px rgba(34, 211, 238, 0.3); }
.btn.ghost {
  background: rgba(255,255,255,0.04);
  color: #e5e7eb;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: none;
}
.muted { color: var(--muted); font-size: 14px; }
.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  margin-top: 18px;
}
.list { margin: 10px 0 0; padding-left: 18px; color: var(--muted); }
.img-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-top: 14px; }
.img-card { background: var(--card); border: var(--border); border-radius: var(--radius); padding: 12px; box-shadow: var(--shadow); }
.img-card img { width: 100%; border-radius: 10px; display: block; }
.small { font-size: 13px; }
</style>

<div class="page">
  <div class="hero">
    <div class="hero-card">
      <div class="badge">ESP32-S3 · FastAPI · PWA</div>
      <h1 style="margin:10px 0 8px;">IdeasGlass</h1>
      <p class="muted">Capture audio + photos from glasses, stream to FastAPI, and review in a modern PWA. Tuned for low-latency WebSocket ingest with HTTP fallbacks and safe-area mobile UX.</p>
      <div class="buttons">
        <a class="btn" href="https://ideas.lazying.art" target="_blank" rel="noopener">Launch App</a>
        <a class="btn ghost" href="https://github.com/lazyingart/IdeasGlass" target="_blank" rel="noopener">View on GitHub</a>
      </div>
      <div class="buttons" style="margin-top:8px;">
        <a class="btn ghost" href="https://github.com/lazyingart/IdeasGlass/blob/main/README.md" target="_blank" rel="noopener">Setup Guide</a>
        <a class="btn ghost" href="https://github.com/lazyingart/IdeasGlass/tree/main/IdeaGlass/firmware/ideasglass_arduino" target="_blank" rel="noopener">Firmware</a>
        <a class="btn ghost" href="https://github.com/lazyingart/IdeasGlass/tree/main/references" target="_blank" rel="noopener">Reference Docs</a>
      </div>
    </div>
    <div class="img-grid">
      <div class="img-card"><img src="/figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI"/></div>
      <div class="img-card"><img src="/figs/ideasglass_hardware.png" alt="IdeasGlass hardware"/></div>
    </div>
  </div>

  <div class="section-grid" style="margin-top:26px;">
    <div class="card">
      <h3>Backend (FastAPI)</h3>
      <p class="muted">Endpoints for audio/photo ingest, settings, auth, and media browsing. Media stored under date/hour folders.</p>
      <ul class="list">
        <li>Run: <code>uvicorn backend.bridge.app:app --host 0.0.0.0 --port 8765 --reload</code></li>
        <li>Audio: <code>/ws/audio-ingest</code> (WS) + <code>/api/v1/audio</code> fallback</li>
        <li>Photos: <code>/ws/photo-ingest</code> (WS) + <code>/api/v1/messages</code> fallback</li>
      </ul>
    </div>
    <div class="card">
      <h3>Firmware (ESP32-S3)</h3>
      <p class="muted">Arduino sketch streaming PCM + JPEG. Long-press to sleep; optional boot-hold; Wi‑Fi tuned for low latency.</p>
      <ul class="list">
        <li>Board: <code>XIAO_ESP32S3:PSRAM=opi,Partition=default_8MB</code></li>
        <li>Compile: <code>bin/arduino-cli compile --fqbn "$FQBN" IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient</code></li>
        <li>Upload: <code>bin/arduino-cli upload -p /dev/ttyACM0 --fqbn "$FQBN" ...</code></li>
      </ul>
    </div>
    <div class="card">
      <h3>PWA</h3>
      <p class="muted">Live tab for streaming; Ideas/Goal/Creation tabs for planning; Settings for device and language.</p>
      <ul class="list">
        <li>Mobile-safe header, offline manifest, install prompt</li>
        <li>Battery pill, gallery microrefresh, transcript playback</li>
        <li>Language picker + persisted UI language</li>
      </ul>
    </div>
  </div>

  <div class="card" style="margin-top:22px;">
    <h3>Quick Start</h3>
    <ol class="list">
      <li>Clone repo; create and activate <code>glass</code> Conda env; install backend deps with <code>pip install -r backend/bridge/requirements.txt</code>.</li>
      <li>Flash firmware via Arduino IDE or <code>bin/arduino-cli</code>; set Wi‑Fi credentials in <code>wifi_credentials.h</code>.</li>
      <li>Run backend; open <code>https://ideas.lazying.art</code> (or your tunnel) to view Live.</li>
      <li>Use Ideas/Goal/Creation tabs to seed sample data and explore the UX.</li>
    </ol>
    <p class="small muted">Legacy deep-dive docs are preserved under <code>/references</code>.</p>
  </div>
</div>
