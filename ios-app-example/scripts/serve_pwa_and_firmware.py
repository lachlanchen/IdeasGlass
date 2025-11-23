#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import tornado.autoreload
import tornado.ioloop
import tornado.web


def pick_static_root(cwd: Path) -> Path:
    candidates = [
        cwd / 'LightMind' / 'pwa_app',
        cwd / 'apps' / 'pwa_app',
        cwd / 'apps' / 'lightmind' / 'pwa_app',
        cwd / 'OmiReference' / 'web',
    ]
    for c in candidates:
        if c.exists() and (c / 'index.html').exists():
            return c
    # Fallback to a simple empty directory
    fallback = cwd / 'pwa_app'
    fallback.mkdir(parents=True, exist_ok=True)
    if not (fallback / 'index.html').exists():
        (fallback / 'index.html').write_text("<html><body><h1>LightMind PWA</h1><p>No app found.</p></body></html>")
    return fallback


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *_):
        self.set_status(204)
        self.finish()


class HealthHandler(BaseHandler):
    def get(self):
        self.write({"ok": True, "ts": int(time.time())})


class ListHandler(BaseHandler):
    def initialize(self, dist_root: Path):
        self.dist_root = dist_root

    def get(self):
        files = []
        for p in sorted(self.dist_root.rglob('*')):
            if p.is_file():
                rel = p.relative_to(self.dist_root)
                rel_str = str(rel).replace(os.sep, '/')
                files.append({
                    'name': rel_str,
                    'bytes': p.stat().st_size,
                    'modified': datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
                    'url': f"/downloads/{rel_str}",
                })
        self.write({'files': files})


class ZipRequestHandler(BaseHandler):
    def initialize(self, dist_root: Path):
        self.dist_root = dist_root

    def post(self):
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.set_status(400)
            return self.finish({'error': 'invalid JSON'})

        source = body.get('source')
        name = body.get('name', 'firmware.zip')
        if not source:
            self.set_status(400)
            return self.finish({'error': 'source is required'})

        src_path = Path(source).expanduser().resolve()
        if not src_path.exists():
            self.set_status(404)
            return self.finish({'error': f'source not found: {src_path}'})

        self.dist_root.mkdir(parents=True, exist_ok=True)
        # If the source is a file, put it into a temp dir then zip the dir, so clients
        # always receive a zip with one or more files inside.
        if src_path.is_file():
            tmp_dir = self.dist_root / f"_tmp_{int(time.time())}"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, tmp_dir / src_path.name)
            base_name = (self.dist_root / (Path(name).stem))
            archive_path = shutil.make_archive(str(base_name), 'zip', str(tmp_dir))
            shutil.rmtree(tmp_dir, ignore_errors=True)
        else:
            base_name = (self.dist_root / (Path(name).stem))
            archive_path = shutil.make_archive(str(base_name), 'zip', str(src_path))

        rel = os.path.basename(archive_path)
        self.write({'ok': True, 'zip': f"/downloads/{rel}"})


def render_downloads_index(dist_root: Path) -> str:
    rows = []
    for p in sorted(dist_root.rglob('*')):
        if p.is_file():
            rel = p.relative_to(dist_root)
            name = str(rel).replace(os.sep, '/')
            size = p.stat().st_size
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            rows.append(f"<tr><td><a href='/downloads/{name}'>{name}</a></td><td>{size:,}</td><td>{mtime}</td></tr>")
    rows_html = "\n".join(rows) or "<tr><td colspan='3'>(no files)</td></tr>"
    return f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <meta name='theme-color' content='#f9fafb'>
    <title>LightMind Downloads</title>
    <link rel='manifest' href='/manifest.webmanifest'>
    <style>
      :root {{
        --bg: #f9fafb;
        --card-bg: #ffffff;
        --card-border: #e5e7eb;
        --accent: #2563eb;
        --accent-soft: rgba(37,99,235,0.08);
        --text-main: #111827;
        --text-muted: #6b7280;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        padding: 24px;
        background: radial-gradient(circle at top left, #e5f0ff, #ffffff);
        color: var(--text-main);
      }}
      a {{ text-decoration: none; color: var(--accent); }}
      table {{
        border-collapse: collapse;
        width: 100%;
        max-width: 880px;
        background: var(--card-bg);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--card-border);
        box-shadow: 0 14px 30px rgba(15,23,42,0.12);
      }}
      th, td {{ padding: 10px 14px; text-align: left; font-size: 14px; }}
      thead tr {{ background: #f3f4ff; }}
      tbody tr:nth-child(even) {{ background: #f9fafb; }}
      tbody tr:hover {{ background: var(--accent-soft); }}
      .crumbs a {{ color: var(--text-muted); font-size: 13px; }}
      .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 11px;
        font-weight: 600;
        margin-left: 4px;
      }}
    </style>
    <script>
      if ('serviceWorker' in navigator) {{
        window.addEventListener('load', () => {{
          navigator.serviceWorker.register('/service-worker.js').catch(() => {{}});
        }});
      }}
    </script>
  </head>
  <body>
    <div class='crumbs'><a href='/'>Home</a> / Downloads</div>
    <h1>Downloads <span class='badge'>PWA</span></h1>
    <table>
      <thead><tr><th>Name</th><th>Bytes</th><th>Modified</th></tr></thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </body>
 </html>
"""


class DownloadsIndexHandler(BaseHandler):
    def initialize(self, dist_root: Path):
        self.dist_root = dist_root

    def get(self):
        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.finish(render_downloads_index(self.dist_root))


def render_home(static_root: Path, dist_root: Path) -> str:
    # Pick a likely PWA entry
    app_url = "/app/"
    # Quick link to a commonly named firmware zip if it exists
    featured = None
    for cand in ["lightmind-dk2-uf2.zip", "firmware.zip", "dfu_application.zip"]:
        if (dist_root / cand).exists():
            featured = cand
            break
    featured_html = f"<p><strong>Latest:</strong> <a href='/downloads/{featured}'>{featured}</a></p>" if featured else ""
    return f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <meta name='theme-color' content='#f9fafb'>
    <title>LightMind Server</title>
    <link rel='manifest' href='/manifest.webmanifest'>
    <style>
      :root {{
        --bg: #f9fafb;
        --card-bg: #ffffff;
        --card-border: #e5e7eb;
        --accent: #2563eb;
        --accent-soft: rgba(37,99,235,0.08);
        --text-main: #111827;
        --text-muted: #6b7280;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        padding: 24px;
        background: radial-gradient(circle at top left, #e5f0ff, #ffffff);
        color: var(--text-main);
      }}
      a {{ text-decoration: none; color: var(--accent); }}
      .card {{
        max-width: 860px;
        padding: 16px 20px;
        border: 1px solid var(--card-border);
        border-radius: 10px;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #ffffff, #f5f5ff);
        box-shadow: 0 14px 30px rgba(15,23,42,0.12);
      }}
      h1 {{ margin-bottom: 6px; }}
      .muted {{ color: var(--text-muted); font-size: 14px; }}
      .tag {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 11px;
        font-weight: 600;
        margin-left: 6px;
      }}
    </style>
    <script>
      if ('serviceWorker' in navigator) {{
        window.addEventListener('load', () => {{
          navigator.serviceWorker.register('/service-worker.js').catch(() => {{}});
        }});
      }}
    </script>
  </head>
  <body>
    <h1>LightMind Local Server <span class='tag'>PWA</span></h1>
    <p class='muted'>PWA shell + firmware downloads for the DK2 OTA pipeline.</p>

    <div class='card'>
      <h2>PWA</h2>
      <p><a href='{app_url}'>Open LightMind PWA</a></p>
    </div>

    <div class='card'>
      <h2>Downloads</h2>
      <p><a href='/downloads/'>Browse downloads</a></p>
      {featured_html}
    </div>
  </body>
 </html>
"""


class HomeHandler(BaseHandler):
    def initialize(self, static_root: Path, dist_root: Path):
        self.static_root = static_root
        self.dist_root = dist_root

    def get(self):
        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.finish(render_home(self.static_root, self.dist_root))


class FaviconHandler(BaseHandler):
    def get(self):
        # No favicon packaged; return 204 to avoid log spam
        self.set_status(204)
        self.finish()


class ManifestHandler(BaseHandler):
    def get(self):
        manifest = {
            "name": "LightMind Firmware Server",
            "short_name": "LightMind OTA",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0f172a",
            "theme_color": "#0f172a",
            "icons": [],
        }
        self.set_header("Content-Type", "application/manifest+json")
        self.finish(json.dumps(manifest))


class ServiceWorkerHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/javascript; charset=utf-8")
        sw = r"""
const CACHE_NAME = 'lightmind-fw-v2';
const CORE_URLS = ['/'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(CORE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // For /downloads/, always go to network first so new firmware files appear
  // immediately, falling back to cache only when offline.
  if (url.pathname.startsWith('/downloads/')) {
    event.respondWith(
      fetch(req).catch(() => caches.match(req))
    );
    return;
  }
  event.respondWith(
    caches.match(req).then(resp => resp || fetch(req))
  );
});
"""
        self.finish(sw)


def make_app(static_root: Path, dist_root: Path):
    return tornado.web.Application([
        (r"/api/health", HealthHandler),
        (r"/api/list", ListHandler, {"dist_root": dist_root}),
        (r"/api/zip", ZipRequestHandler, {"dist_root": dist_root}),
        (r"/downloads/?", DownloadsIndexHandler, {"dist_root": dist_root}),
        (r"/downloads/(.*)", tornado.web.StaticFileHandler, {"path": str(dist_root)}),
        (r"/app/(.*)", tornado.web.StaticFileHandler, {"path": str(static_root), "default_filename": "index.html"}),
        (r"/favicon.ico", FaviconHandler),
        (r"/manifest.webmanifest", ManifestHandler),
        (r"/service-worker.js", ServiceWorkerHandler),
        (r"/", HomeHandler, {"static_root": static_root, "dist_root": dist_root}),
    ], debug=False)


def main():
    parser = argparse.ArgumentParser(description="Serve LightMind PWA and firmware downloads")
    parser.add_argument('--port', type=int, default=8787)
    parser.add_argument('--static-root', default=None, help='Directory containing PWA index.html (default auto)')
    parser.add_argument('--dist-root', default='dist', help='Directory to write/serve ZIPs (default ./dist)')
    args = parser.parse_args()

    cwd = Path.cwd()
    static_root = Path(args.static_root).resolve() if args.static_root else pick_static_root(cwd)
    dist_root = Path(args.dist_root).resolve()
    dist_root.mkdir(parents=True, exist_ok=True)

    app = make_app(static_root, dist_root)
    app.listen(args.port)
    # Auto-reload when code or dist contents change.
    tornado.autoreload.watch(__file__)
    tornado.autoreload.watch(str(dist_root))
    tornado.autoreload.start()
    print(f"Serving PWA from: {static_root}")
    print(f"Serving downloads from: {dist_root}")
    print(f"Listening on http://127.0.0.1:{args.port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down.")
