[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*Eine tragbare KI-Brille, die Ideen in Aktionen, Einkommen und kreative Dynamik verwandelt.*

> Voice-first Wearable-KI-Pipeline: Erfassen mit ESP32-Brillen, Verarbeitung in FastAPI und Überwachung/Steuerung über ein Live-PWA-Dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Lane | Zweck |
|---|---|
| 🎙️ Wearable capture | ESP32-Brillen übertragen Audio, Fotos und Telemetrie nahezu in Echtzeit |
| 🧠 Backend intelligence | FastAPI verarbeitet Streams, transkribiert, segmentiert und speichert Metadaten |
| 🖥️ Dashboard | PWA zeigt Live-Wellenform, Transkripte und Geräte-/Kontostatus |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Ecosystem</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Support IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>App-UI (links) · Hardware (rechts)</sub>
</div>

Erkunde Community-Experimente unter <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Überblick

IdeasGlass ist ein KI-zentriertes Wearable-System für sprachzentrierte Ideenerfassung und -umsetzung. In diesem Repository ist der primäre Laufzeitpfad:

- `backend/glass/` für FastAPI-APIs, WebSocket-Ingest, Whisper-basierte Transkription und das installierbare PWA-Dashboard.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` für XIAO ESP32S3-Firmware mit Streaming von Telemetrie, Audio und Fotos.

Wenn du neu im Repository bist, starte hier.

### Auf einen Blick

| Bereich | Primärer Ort | Funktion |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPI-Endpunkte, WebSocket-Ingest/Fanout, Transkription, Dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 Capture-/Streaming-Client |
| Bridge-Hinweise | `references/ideasglass_bridge.md` | TLS/WAN-Notes und Deployment-Tipps für den Feldbetrieb |
| README-Übersetzungen | `i18n/` | Mehrsprachige Docs, synchronisiert vom kanonischen README |

## ✨ Warum IdeasGlass

IdeasGlass ist ein KI-zentriertes Wearable für Menschen, die in einem Strom von Ideen leben. Es erfasst, übersetzt, organisiert und setzt Kreativität genau in dem Moment um, in dem die Inspiration zuschlägt – ob du ein Konzept im Gehen beschreibst oder eine Live-Session moderierst.

## 🧩 Funktionen

### Produktvision

- **Creation-native Hardware** – leichte Brille und Wearable-Eingaben, optimiert für sprachzentrierte Erfassung plus subtile Gesten-Abkürzungen.
- **Sofortige Übersetzung** – Echtzeit-Sprach- und Übersetzungserkennung, damit Teams oder Zielgruppen nahtlos zusammenarbeiten können.
- **EchoMind-Co-Pilot** – eng gekoppelt mit `chat.lazying.art` für Brainstorming, Skriptentwürfe und mehrsprachiges Content-Coaching.
- **Channel-Autopilot** – erstellt Outline, Long-Form-Skripte, Short-Form-Hooks und plant Uploads zu YouTube oder anderen Feeds.
- **Highlights & Reels** – wählt automatisch Moments aus, generiert Miniaturen, Untertitel und social-ready Clips.
- **Income-Layer** – verbindet mit LazyingArt Coin für Tipping, Kredit-Auszahlungen und Umwandlung in On-Chain-Assets.
- **Spending & Focus** – trackt operative Kosten, zeigt profitable Formate und destilliert Stärken für nächste Projekte.

### Repository-/Runtime-Funktionen

- FastAPI-Backend mit REST + WebSocket-Endpunkten für Ingest (`/api/v1/audio`, `/ws/audio-ingest`) und Live-Stream-Fanout (`/ws/stream`).
- Deterministische Audio-Segmentierung (Standard ~15 s mit Überlappung) in `backend/glass/audio_segments/`.
- Optionales openai-whisper Streaming-Transkription mit konfigurierbaren Latenz-Schwellen.
- Optionale Postgres-Persistenz (`DATABASE_URL`) für Nachrichten, Fotos, Chunks, Segmente, Transkripte.
- PWA-Dashboard mit Live-Wellenform, Transkript-Updates und Installationssupport auf Desktop/Mobile.
- Arduino-Firmware-Support für XIAO ESP32S3 Sense Kamera- und Mikrofon-Pipelines.

## 🔄 Beispiel-Workflow

1. **Erfassen** – Sprich oder skizziere eine Idee; IdeasGlass transkribiert, übersetzt und ordnet die Intention.
2. **Gemeinsam erstellen** – EchoMind verfeinert die Idee, erstellt Skripte und schlägt je Plattform passende CTAs vor.
3. **Publizieren** – Der Channel-Agent erzeugt automatisch Highlights, Galeriebilder und lädt sie mit Metadaten hoch.
4. **Monetarisieren** – Credits laufen über LazyingArt Coin (`coin.lazying.art`), Auszahlungen synchronisieren sich mit deinen bevorzugten Wallets.
5. **Reflektieren** – Ausgaben-, Reichweiten- und Engagement-Dashboards zeigen, worin du als Nächstes investieren solltest.

## 🗂️ Projektstruktur

```text
IdeasGlass/
├── README.md
├── i18n/                                  # README translations
├── backend/
│   ├── glass/                             # Primary FastAPI + PWA backend
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # Secondary/parallel ingest backend path
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Bridge + deployment notes
├── docs/                                  # Additional site/docs assets
├── development_plan/
├── app/
├── ops/observability/
├── figs/
└── seeed_studio_xiao_esp32s3_dev/
```

## 🧰 Voraussetzungen

- Python 3.10+
- `pip` (oder conda-Umgebung mit kompatiblem Python)
- Optional: NVIDIA GPU + CUDA/cuDNN für schnellere Whisper-Inferenz
- Optional: PostgreSQL für Persistenz
- Für Firmware: Arduino IDE oder `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM aktiviert

| Komponente | Anforderung | Hinweise |
|---|---|---|
| Backend-Laufzeit | Python 3.10+, `pip` | Nutze venv oder conda (`glass`) |
| GPU-Beschleunigung (optional) | NVIDIA + CUDA/cuDNN | Verbessert Whisper-Latenz |
| Persistenz (optional) | PostgreSQL | Aktivierung über `DATABASE_URL` |
| Firmware-Toolchain | Arduino IDE / `arduino-cli` | XIAO ESP32S3-Profil mit PSRAM |

## ⚙️ Installation

### Backend-Abhängigkeiten

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Firmware-Voraussetzungen

- Kopiere `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` nach `wifi_credentials.h` (empfohlen) und setze SSID/Passwort.
- In der Arduino IDE wähle Board `ESP32 -> XIAO_ESP32S3` mit `PSRAM: OPI PSRAM`.
- Partitionierung: `Default with spiffs (3MB APP/1.5MB SPIFFS)` oder `Maximum APP`, wenn kein Dateisystem benötigt wird.

## ▶️ Nutzung

### Backend starten (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Backend starten (Hilfsprogramm)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Dashboard öffnen

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Zweck |
|---|---|
| `/` | Hauptdashboard (PWA-fähige UI) |
| `/healthz` | Liveness-Check des Backends |
| `/ws/audio-ingest` | Geräte-Ingest-WebSocket |
| `/ws/stream` | Live-Stream-Fanout für Dashboard-Clients |

### Login und Gerätebindung

1. Registriere dich oder melde dich im Dashboard unter Einstellungen/Konto an.
2. Binde deine Device-ID im Feld `Bind device`.
3. Nur gebundene Geräte streamen in deinem Konto.

Geräte-ID + QR-Bild generieren:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Binden per API (Cookie-Session erforderlich):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Aktuelles Konto und gebundene Geräte prüfen:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Optionale Migration (historische Daten auf neue Geräte-ID umbenennen):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Firmware bauen/hochladen (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Wenn der Port belegt ist: `fuser -k /dev/ttyACM0`.
Bei Berechtigungsproblemen: `sudo usermod -aG dialout $USER`, anschließend neu anmelden (oder temporär `sudo chmod a+rw /dev/ttyACM0`).

### Firmware-Power-UX (XIAO ESP32S3)

- Bei Einschalten ca. 0,8 s halten, um zu starten.
- Während des Betriebs ca. 2,5 s halten, um in den Deep Sleep zu gehen.
- Kurzer Druck im Betrieb startet weiterhin die Aufzeichnung.

## 🛠️ Konfiguration

### Kern-Umgebungsvariablen

- `DATABASE_URL`: optionale Postgres-DSN für persistente Speicherung.
- `IDEASGLASS_WHISPER_MODEL`: `base` (Standard), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` oder `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` für GPU-Mixed-Precision, `0` für CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (Standard) aktiviert Transkription, `0` deaktiviert sie.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: laufender Transkript-Abstand.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: kommagetrennte Schwellen (Standard `3000,6000,15000`).

| Variable | Default / Optionen | Wirkung |
|---|---|---|
| `DATABASE_URL` | Standardmäßig nicht gesetzt | Aktiviert Postgres-Persistenz für Konten-/Gerätedaten |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Steuert Genauigkeit vs. Latenz |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` oder `cpu` | Inferenz-Backend |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-sicher | Kontrolle der gemischten Präzision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Schaltet die Transkriptions-Pipeline ein |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | zur Laufzeit konfiguriert | Intervall zum Senden laufender Transkripte |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Progressive Schwellen für Transkript-Ausgabe |

Sichere Beispiele für `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (Peer/Local Auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (Passwort-Auth)

### Gain- und Segmentierungs-Parameter

- `IDEASGLASS_GAIN_TARGET` (Standard `0.032`)
- `IDEASGLASS_GAIN_MAX` (Standard `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (Standard `0.008`)
- `IDEASGLASS_SPEECH_RMS` (Standard `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (Standard `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (Standard `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (Standard `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (Standard: Chunk-Gain-Ziel)

| Audio-Parameter | Standard | Zweck |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Ziel der RMS-Normalisierung |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Obergrenze für Gain-Verstärkung |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Mindestwert, um fast Stille nicht unnötig zu verstärken |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | RMS-Basis für Sprachaktivität |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Puffer um die Sprachschwelle |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Zielsegmentlänge |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Segmentüberlappung für Kontinuität |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | übernimmt Chunk-Gain | Ziel für Segment-Normalisierung |

### Model-Prefetch (optional)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Beispiele

### Geräte-ID generieren und binden

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Danach `kDeviceId` in:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` setzen.

Dashboard-Ablauf:

1. In Einstellungen registrieren/einloggen.
2. Gerät im Account-Bereich binden.
3. Nur gebundene Geräte werden an dein Konto gestreamt.

### REST-Ingest-Beispiele

```bash
curl -X POST http://localhost:8765/api/v1/messages \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"dev-001","message":"hello from curl"}'
```

```bash
curl -X POST http://localhost:8765/api/v1/messages \
  -H 'Content-Type: application/json' \
  -d '{
    "device_id":"dev-001",
    "message":"photo demo",
    "photo_base64":"'"$(base64 -w0 sample.jpg)"'",
    "photo_mime":"image/jpeg"
  }'
```

```bash
rec --bits 16 --channels 1 --rate 16000 -c 1 -b 16 -e signed-integer temp.raw trim 0 0.25
curl -X POST http://localhost:8765/api/v1/audio \
  -H 'Content-Type: application/json' \
  -d '{
    "device_id":"dev-001",
    "sample_rate":16000,
    "bits_per_sample":16,
    "duration_ms":250,
    "rms":0.05,
    "audio_base64":"'"$(base64 -w0 temp.raw)"'"
  }'
```

```bash
curl http://localhost:8765/api/v1/audio/segments | jq '.[0]'
curl -o latest.wav http://localhost:8765/api/v1/audio/segments/<segment-id>
```

## 🧭 Entwicklungshinweise

### Fokusbereich

Dieses Repository enthält mehrere Backend-Pfade. Die aktuelle Empfehlung für Beitragende und Laufzeitfokus liegt auf `backend/glass/`, sofern nicht anders gefordert.

### Static/syntax check

```bash
python -m compileall backend/glass/app.py
```

### Entwickler-Dokumentation

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Hinweis: Im aktuellen Repository-Snapshot sind einige der oben genannten historischen Links offenbar verschoben (etwa sind Bridge-Hinweise jetzt unter `references/ideasglass_bridge.md`). Die Original-Links bleiben als kanonischer README-Inhalt erhalten.

### Schneller Gerätebindungsablauf (erhaltener Workflow)

- ID generieren (im conda-Environment `glass`): `python backend/glass/tools/generate_device_id.py`
- In Firmware setzen: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Backend starten und `http://localhost:8765` öffnen, registrieren/anmelden und die Device-ID im Account-Panel binden

## 🆘 Fehlerbehebung

- **Port bereits belegt:** Backend auf einem anderen Port starten und Client-Einstellungen aktualisieren.
- **Serieller Port belegt:** `fuser -k /dev/ttyACM0`.
- **Linux-Serien-Port-Rechte verweigert:** `sudo usermod -aG dialout $USER` und neu anmelden.
- **Postgres nicht verfügbar:** Backend läuft ohne DB mit eingeschränkter Funktion; `DATABASE_URL` prüfen und neu starten.
- **Whisper-Performance-Probleme:** kleinere Modelle (`base`/`small`) nutzen oder Transkription via `IDEASGLASS_TRANSCRIBE=0` deaktivieren.
- **TLS-/Zeit-Synchronisationsprobleme auf ESP32:** Wi-Fi, NTP (UDP/123) und Zertifikat-/Host-Konfiguration prüfen; siehe `references/ideasglass_bridge.md` für Feldhinweise.
- **Keine Live-Wellenform-Updates:** Backend-Logs und Browserkonsole auf `[IdeasGlass][wave]`-Spuren prüfen und `/ws/stream`-Konnektivität bestätigen.

## 🌐 Ecosystem-Links

🧠 **EchoMind** — Mehrsprachiger KI-Begleiter für Lernen und Kreation.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Community für Research-to-Product-konzeptionelle Ideen.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatisierungen, die kleine Erfolge in Einkommen verwandeln.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Physik- und Chemiepfade sowie Notebooks.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent, der Ideen in Entwürfe, Aufgaben und Posts verwandelt.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Erfassen, Übersetzen und automatische Highlight-Reels-Produktion.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Rewards und Auszahlungen, die Beiträge in on-chain Wert überführen.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Forschungsnotizen- und Essay-Sammlung.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio hinter OnlyIdeas, EchoMind, LazyEdit und IdeasGlass.  
[lazying.art](https://lazying.art)

## 🙏 Danksagung

Wir bauen auf großartigen Open-Source-Projekten auf — vielen Dank an:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — Nutze den Code `LazyingArt`, um 10% zu sparen (30% Provision nach 10 Verkäufen freigeschaltet).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Roadmap

- Die End-to-End-Audiostreaming-Pipeline über WAN/TLS-Umgebungen härten und dokumentieren.
- Transkriptqualität und -latenz weiter verbessern (Model-/Device-/Threshold-Voreinstellungen).
- Device-Management und kontoorientierte Multi-Device-Workflows im Dashboard erweitern.
- Legacy-/Parallel-Backend-Pfade (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) mit dem primären Pfad `backend/glass` angleichen oder konsolidieren.
- Mehrsprachige README-Varianten unter `i18n/` pflegen.

## 🤝 Beitrag

Beiträge sind willkommen. Für repository-spezifische Ablaufregeln siehe `AGENTS.md`.

Empfohlene lokale Validierung vor dem Öffnen eines PR:

```bash
python -m compileall backend/glass/app.py
```

Beim Einreichen von Änderungen:

- Nutze kurze, handlungsorientierte Commit-Betreffzeilen (Präsens).
- Erwähne relevante Umgebungsvariablen (z. B. `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) in den PR-Notizen, wenn das Verhalten davon abhängt.
- Füge Testnachweise hinzu (Backend-Logs, Dashboard-Verhalten, Firmware-Output).
- Nie Secrets committen (`DATABASE_URL`, API-Tokens, Zugangsdaten-Dateien).

## 📄 Lizenz

Im aktuellen Repository-Snapshot wurde keine Top-Level-`LICENSE`-Datei gefunden. Bis eine explizite Lizenzdatei ergänzt wird, sollte die Nutzung und Weiterverbreitung mit der Zustimmung der Maintainer erfolgen.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
