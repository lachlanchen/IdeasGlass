[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*Eine tragbare KI-Brille, die Ideen in Aktionen, Einkommen und kreative Dynamik verwandelt.*

> Voice-first-Wearable-KI-Pipeline: Erfassung über ESP32-Brillen, Verarbeitung in FastAPI sowie Live-Monitoring/Steuerung über ein PWA-Dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Ökosystem</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>IdeasGlass unterstützen</b><br/>
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

Entdecke Community-Experimente auf <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Überblick

IdeasGlass ist ein KI-zentriertes Wearable-System für Voice-first-Ideenerfassung und -Umsetzung. In diesem Repository ist der primäre Runtime-Pfad:

- `backend/glass/` für FastAPI-APIs, WebSocket-Ingest, Whisper-basierte Transkription und das installierbare PWA-Dashboard.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` für XIAO ESP32S3-Firmware zum Streaming von Telemetrie/Audio/Fotos.

Wenn du neu in diesem Repo bist, starte dort zuerst.

### Auf einen Blick

| Bereich | Primärer Ort | Zweck |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPI-Endpunkte, WebSocket-Ingest/Fanout, Transkription, Dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32-Client für Erfassung/Streaming |
| Bridge-Hinweise | `references/ideasglass_bridge.md` | TLS/WAN-Zuverlässigkeit und praktische Deployment-Tipps |
| README-Übersetzungen | `i18n/` | Mehrsprachige Doku, synchronisiert mit dem kanonischen README |

## ✨ Warum IdeasGlass

IdeasGlass ist ein KI-zentriertes Wearable für Menschen, die in einem Strom von Ideen leben. Es erfasst, übersetzt, organisiert und setzt Kreativität in dem Moment um, in dem Inspiration aufkommt, egal ob du ein Konzept unterwegs sprichst oder eine Live-Session hostest.

## 🧩 Funktionen

### Funktionen der Produktvision

- **Creation-native Hardware** – leichte Brille und Wearable-Eingaben, optimiert für Voice-first-Erfassung plus subtile Gesten-Shortcuts.
- **Sofortige Übersetzung** – Echtzeit-Spracherkennung/-Übersetzung, damit du ohne Toolwechsel über Teams oder Zielgruppen hinweg Ideen entwickeln kannst.
- **EchoMind Co-Pilot** – enge Integration mit `chat.lazying.art` für Brainstorming, Skriptentwürfe und mehrsprachiges Content-Coaching.
- **Channel Autopilot** – erstellt Gliederungen, Long-form-Skripte, Short-form-Hooks und plant Uploads auf YouTube oder andere Feeds.
- **Highlights & Reels** – wählt automatisch Momente aus, erzeugt Thumbnails, Untertitel und Social-ready-Clips.
- **Einkommensschicht** – verbindet mit LazyingArt Coin für Trinkgelder, Credit-Auszahlungen und Konvertierung in On-chain-Assets.
- **Ausgaben & Fokus** – verfolgt operative Kosten, zeigt profitable Formate und verdichtet persönliche Stärken für nächste Projekte.

### Repository-/Runtime-Funktionen

- FastAPI-Backend mit REST- + WebSocket-Endpunkten für Ingest (`/api/v1/audio`, `/ws/audio-ingest`) und Live-Stream-Fanout (`/ws/stream`).
- Deterministische Audiosegmentierung (Standard ~15 s mit Überlappung) nach `backend/glass/audio_segments/`.
- Optionale openai-whisper-Streaming-Transkripte mit konfigurierbaren Latenz-Schwellen.
- Optionale Postgres-Persistenz (`DATABASE_URL`) für Nachrichten, Fotos, Chunks, Segmente, Transkripte.
- PWA-Dashboard mit Live-Wellenform, Transkript-Updates und Installationssupport auf Desktop/Mobile.
- Arduino-Firmware-Unterstützung für XIAO ESP32S3 Sense Kamera- + Mikrofon-Flows.

## 🔄 Beispiel-Workflow

1. **Erfassen** – Sprich oder skizziere ein Konzept; IdeasGlass transkribiert, übersetzt und markiert die Intention.
2. **Gemeinsam erstellen** – EchoMind verfeinert die Idee, erstellt Skripte und schlägt CTAs pro Plattform vor.
3. **Veröffentlichen** – Der Channel-Agent produziert automatisch Highlight-Videos, Galerie-Bilder und lädt sie mit Metadaten hoch.
4. **Monetarisieren** – Credits laufen über LazyingArt Coin (`coin.lazying.art`) und Auszahlungen werden mit deinen bevorzugten Wallets synchronisiert.
5. **Reflektieren** – Dashboards für Ausgaben, Reichweite und Engagement zeigen, worauf du als Nächstes setzen solltest.

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
| Backend-Runtime | Python 3.10+, `pip` | Verwende venv oder conda (`glass`) |
| GPU-Beschleunigung (optional) | NVIDIA + CUDA/cuDNN | Verbessert Whisper-Latenz |
| Persistenz (optional) | PostgreSQL | Aktiviert über `DATABASE_URL` |
| Firmware-Toolchain | Arduino IDE / `arduino-cli` | XIAO ESP32S3-Profil mit PSRAM verwenden |

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
- In der Arduino IDE das Board `ESP32 -> XIAO_ESP32S3` mit `PSRAM: OPI PSRAM` verwenden.
- Partitionsschema: `Default with spiffs (3MB APP/1.5MB SPIFFS)` oder `Maximum APP`, wenn kein Dateisystem benötigt wird.

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

### Backend starten (Helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Dashboard öffnen

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpunkt | Zweck |
|---|---|
| `/` | Haupt-Dashboard (PWA-fähige UI) |
| `/healthz` | Liveness-Check des Backends |
| `/ws/audio-ingest` | Device-Ingest-WebSocket |
| `/ws/stream` | Live-Stream-Fanout an Dashboard-Clients |

### Einloggen und Gerät binden

1. Registriere dich oder logge dich im Dashboard-Bereich Einstellungen/Konto ein.
2. Binde deine Device-ID im Feld `Bind device`.
3. Nur gebundene Geräte streamen in dein Konto.

Device-ID + QR-Bild erzeugen:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Über API binden (Cookie-Session erforderlich):

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

Optionale Migration (historische Daten auf neue Device-ID umbenennen):

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
Bei fehlenden Rechten: `sudo usermod -aG dialout $USER` und danach neu einloggen (oder temporär `sudo chmod a+rw /dev/ttyACM0`).

### Firmware-Power-UX (XIAO ESP32S3)

- Taste beim Einschalten ~0.8 s halten zum Booten.
- Während des Betriebs ~2.5 s halten für Deep Sleep.
- Kurzes Drücken während des Betriebs löst weiterhin Erfassung aus.

## 🛠️ Konfiguration

### Zentrale Umgebungsvariablen

- `DATABASE_URL`: optionale Postgres-DSN für persistente Speicherung.
- `IDEASGLASS_WHISPER_MODEL`: `base` (Standard), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` oder `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` für GPU Mixed Precision, `0` für CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (Standard), um Transkription zu aktivieren, `0`, um sie zu deaktivieren.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: Rolling-Intervall für Transkript-Ausgabe.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: komma-separierte Schwellen (Standard `3000,6000,15000`).

| Variable | Standard / Optionen | Effekt |
|---|---|---|
| `DATABASE_URL` | standardmäßig nicht gesetzt | Aktiviert Postgres-Persistenz für Konto-/Gerätedaten |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Steuert Genauigkeit vs. Latenz |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` oder `cpu` | Inferenz-Backend |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-sicher | Steuerung von Mixed Precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Schaltet die Transkriptions-Pipeline |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | zur Laufzeit konfiguriert | Rolling-Intervall für Transkript-Push |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Progressive Schwellen zur Transkript-Ausgabe |

Sichere `DATABASE_URL`-Beispiele:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (Peer/Lokal-Auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (Passwort-Auth)

### Audio-Gain- und Segmentierungs-Parameter

- `IDEASGLASS_GAIN_TARGET` (Standard `0.032`)
- `IDEASGLASS_GAIN_MAX` (Standard `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (Standard `0.008`)
- `IDEASGLASS_SPEECH_RMS` (Standard `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (Standard `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (Standard `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (Standard `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (standardmäßig Chunk-Gain-Target)

| Audio-Parameter | Standard | Zweck |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Ziel-RMS-Normalisierung |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Obergrenze für Gain-Verstärkung |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Untergrenze, um nahezu Stille nicht zu verstärken |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | RMS-Basis für Sprachaktivität |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Marge um die Sprachschwelle |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Zielwert für Segmentlänge |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Segmentüberlappung für Kontinuität |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | erbt Chunk-Gain | Zielwert für Segment-Normalisierung |

### Model-Prefetch (optional)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Beispiele

### Device-ID erzeugen und binden

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Dann `kDeviceId` setzen in:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Dashboard-Ablauf:

1. In Einstellungen registrieren/einloggen.
2. Gerät im Konto-Panel binden.
3. Nur gebundene Geräte streamen in dein Konto.

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

Dieses Repo enthält mehrere Backend-Tracks. Aktuelle Contributor-Empfehlung und Runtime-Fokus ist `backend/glass/`, sofern nicht anders angefragt.

### Static-/Syntax-Check

```bash
python -m compileall backend/glass/app.py
```

### Entwicklerdokumente

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Hinweis: Im aktuellen Repository-Snapshot scheinen einige historische Links oben verschoben worden zu sein (z. B. liegen Bridge-Hinweise jetzt unter `references/ideasglass_bridge.md`). Die ursprünglichen Links bleiben als kanonischer README-Inhalt erhalten.

### Schnelles Device-Binding (beibehaltener Workflow)

- ID generieren (in conda `glass`): `python backend/glass/tools/generate_device_id.py`
- In der Firmware setzen: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Backend starten und `http://localhost:8765` öffnen, registrieren/einloggen und dann die Device-ID im Konto-Panel binden

## 🆘 Fehlerbehebung

- **Port bereits belegt:** Backend auf einem anderen Port starten und Client-Einstellungen aktualisieren.
- **Serieller Port belegt:** `fuser -k /dev/ttyACM0`.
- **Linux-Seriell-Rechte verweigert:** `sudo usermod -aG dialout $USER` und neu einloggen.
- **Postgres nicht verfügbar:** Backend kann ohne DB mit eingeschränkter Funktion laufen; `DATABASE_URL` prüfen und neu starten.
- **Whisper-Performanceprobleme:** kleinere Modelle (`base`/`small`) nutzen oder Transkription via `IDEASGLASS_TRANSCRIBE=0` deaktivieren.
- **TLS/Zeitsynchronisations-Instabilität auf ESP32:** WLAN, NTP-Verfügbarkeit (UDP/123) sowie Zertifikats-/Host-Einstellungen prüfen; detaillierte Feldnotizen in `references/ideasglass_bridge.md`.
- **Keine Live-Wellenform-Updates:** Backend-Logs und Browser-Konsole auf `[IdeasGlass][wave]`-Traces prüfen und `/ws/stream`-Konnektivität bestätigen.

## 🌐 Ökosystem-Links

🧠 **EchoMind** — Mehrsprachiger KI-Begleiter für Lernen und Kreation.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Research-to-Product-Community für mutige Konzepte.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatisierungen, die kleine Erfolge in Einkommen verwandeln.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Physik- und Chemie-Tracks sowie Notebooks.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent, der Ideen in Entwürfe, Aufgaben und Posts verwandelt.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Erfassen, übersetzen und Highlight-Reels automatisch produzieren.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Rewards und Auszahlungen, die Beiträge mit On-chain-Wert verbinden.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Notizbuch mit Forschungsnotizen und Essays.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio hinter OnlyIdeas, EchoMind, LazyEdit und IdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ Support & Kontakt

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- Deine Unterstützung hält die Roadmap für Wearable, Agenten und Ökosystem in Bewegung.

<div align="center">
<table style="margin:0 auto; text-align:center; border-collapse:collapse;">
  <tr>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;">
      <a href="https://chat.lazying.art/donate">https://chat.lazying.art/donate</a>
    </td>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;">
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="44"></a>
    </td>
  </tr>
  <tr>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;">
      <a href="https://paypal.me/RongzhouChen">
        <img src="https://img.shields.io/badge/PayPal-Donate-003087?logo=paypal&logoColor=white" alt="Donate with PayPal">
      </a>
    </td>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;">
      <a href="https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400">
        <img src="https://img.shields.io/badge/Stripe-Donate-635bff?logo=stripe&logoColor=white" alt="Donate with Stripe">
      </a>
    </td>
  </tr>
  <tr>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;"><strong>WeChat</strong></td>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;"><strong>Alipay</strong></td>
  </tr>
  <tr>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;"><img alt="WeChat QR" src="figs/donate_wechat.png" width="240"/></td>
    <td style="text-align:center; vertical-align:middle; padding:6px 12px;"><img alt="Alipay QR" src="figs/donate_alipay.png" width="240"/></td>
  </tr>
</table>
</div>

- Für Partnerschaften sende eine E-Mail an **contact@lazying.art** mit dem Betreff `IdeasGlass`.

IdeasGlass ist der Ort, an dem KI-Wearables nicht nur zuhören, sondern mit dir bauen.

## 🙏 Danksagung

Wir stehen auf den Schultern großartiger Open-Source-Projekte — danke an:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — Use coupon `LazyingArt` to save 10% (30% commission unlocks after 10 sales).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Roadmap

- End-to-end-Audiostreaming-Pfad über WAN/TLS-Umgebungen hinweg härten und dokumentieren.
- Qualität/Latenz-Trade-offs der Transkription weiter verbessern (Model/Device/Threshold-Presets).
- Device-Management und konto-spezifische Multi-Device-Workflows im Dashboard ausbauen.
- Legacy-/Parallel-Backend-Tracks (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) mit dem primären Pfad `backend/glass` abstimmen oder konsolidieren.
- Mehrsprachige README-Varianten unter `i18n/` pflegen und aktualisieren.

## 🤝 Beitrag

Beiträge sind willkommen. Für repository-spezifische Workflow-Hinweise befolge `AGENTS.md`.

Empfohlene lokale Validierung vor dem Öffnen eines PRs:

```bash
python -m compileall backend/glass/app.py
```

Beim Einreichen von Änderungen:

- Commit-Betreff kurz und handlungsorientiert halten (Präsens).
- Relevante Env-Variablen (z. B. `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) in den PR-Notizen erwähnen, wenn Verhalten davon abhängt.
- Testnachweise einfügen (Backend-Logs, Dashboard-Verhalten, Firmware-Ausgabe).
- Niemals Secrets committen (`DATABASE_URL`, API-Token, Credential-Dateien).

## 📄 Lizenz

In diesem Repository-Snapshot wurde keine `LICENSE`-Datei auf Top-Level gefunden. Bis eine explizite Lizenzdatei ergänzt wird, sollte Nutzung und Weiterverteilung als zustimmungspflichtig durch die Maintainer behandelt werden.
