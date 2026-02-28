[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*Un wearable de IA que convierte ideas en acciones, ingresos y empuje creativo.*

> Pipeline de IA wearable centrada en voz: captura desde gafas ESP32, procesa en FastAPI y supervisa/controla mediante un dashboard PWA en vivo.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Carril | Propósito |
|---|---|
| 🎙️ Captura wearable | Las gafas ESP32 envían audio, fotos y telemetría en casi tiempo real |
| 🧠 Inteligencia del backend | FastAPI ingiere streams, transcribe, segmenta y persiste metadatos |
| 🖥️ Dashboard | PWA muestra forma de onda en vivo, transcripciones y estado del dispositivo/cuenta |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Ecosistema</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Apoya IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>UI de la app (izquierda) · Hardware (derecha)</sub>
</div>

Explora los experimentos comunitarios en <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Visión general

IdeasGlass es un sistema wearable AI-first para captura y ejecución de ideas con enfoque de voz. En este repositorio, la ruta de ejecución principal es:

- `backend/glass/` para APIs FastAPI, ingesta WebSocket, transcripción con Whisper y el dashboard PWA instalable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` para firmware de XIAO ESP32S3 que transmite telemetría/audio/fotos.

Si eres nuevo en este repositorio, empieza por ahí.

### En un vistazo

| Área | Ubicación principal | Qué hace |
|---|---|---|
| API + PWA del backend | `backend/glass/` | Endpoints FastAPI, ingesta/distribución por WebSocket, transcripción, dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Cliente de captura/streaming de ESP32 |
| Notas del bridge | `references/ideasglass_bridge.md` | Notas de fiabilidad TLS/WAN y despliegue en campo |
| Traducciones del README | `i18n/` | Documentación multilingüe sincronizada desde el README canónico |

## ✨ Por qué IdeasGlass

IdeasGlass es un wearable AI-first pensado para personas que viven en un flujo de ideas constante. Captura, traduce, organiza y ejecuta la creatividad en el momento en que surge la inspiración, ya sea que describas un concepto en movimiento o dirijas una sesión en vivo.

## 🧩 Características

### Funciones de visión de producto

- **Hardware nativo de creación** – gafas ligeras y entradas wearables, optimizadas para captura por voz y atajos de gesto discretos.
- **Traducción instantánea** – detección y traducción de idioma en tiempo real para idear en equipos o audiencias sin cambiar de herramienta.
- **Copiloto EchoMind** – integración estrecha con `chat.lazying.art` para lluvias de ideas, redacción de guiones y coaching de contenido multilingüe.
- **Autopiloto de canal** – genera esquemas, guiones largos, ganchos cortos y programa publicaciones en YouTube u otros canales.
- **Highlights y reels** – selecciona momentos automáticamente, genera miniaturas, subtítulos y clips listos para redes.
- **Capa de ingresos** – conecta con LazyingArt Coin para propinas, pagos por créditos y conversión a activos on-chain.
- **Control de gasto y foco** – rastrea el gasto operativo, destaca formatos rentables y sintetiza tus fortalezas en próximos proyectos.

### Funciones del repositorio/runtime

- Backend FastAPI con endpoints REST + WebSocket para ingesta (`/api/v1/audio`, `/ws/audio-ingest`) y fanout de stream en vivo (`/ws/stream`).
- Segmentación de audio determinística (15 s por defecto con solapamiento) en `backend/glass/audio_segments/`.
- Transcripción de streaming opcional con openai-whisper y latencias configurables por umbral.
- Persistencia opcional en Postgres (`DATABASE_URL`) para mensajes, fotos, chunks, segmentos y transcripciones.
- Dashboard PWA con forma de onda en vivo, actualizaciones de transcripción y soporte de instalación en desktop/mobile.
- Soporte de firmware Arduino para flujos de cámara y micrófono de XIAO ESP32S3 Sense.

## 🔄 Flujo de trabajo de muestra

1. **Capture** – Habla o dibuja un concepto; IdeasGlass transcribe, traduce y etiqueta la intención.
2. **Co-create** – EchoMind refina la idea, redacta guiones y sugiere CTAs adaptados a cada plataforma.
3. **Publish** – El agente de canal auto-produce videos destacados, imágenes de galería y los sube con metadatos.
4. **Monetize** – Los créditos se enrutan por LazyingArt Coin (`coin.lazying.art`) y los pagos se sincronizan con tus wallets preferidas.
5. **Reflect** – Los paneles de gasto, alcance y engagement muestran en qué conviene enfocarse a continuación.

## 🗂️ Estructura del proyecto

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

## 🧰 Requisitos previos

- Python 3.10+
- `pip` (o entorno conda con Python compatible)
- Opcional: GPU NVIDIA + CUDA/cuDNN para inferencia Whisper más rápida
- Opcional: PostgreSQL para persistencia
- Para firmware: Arduino IDE o `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM habilitada

| Component | Requirement | Notes |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | Usa venv o conda (`glass`) |
| GPU acceleration (optional) | NVIDIA + CUDA/cuDNN | Mejora la latencia de Whisper |
| Persistence (optional) | PostgreSQL | Habilitado mediante `DATABASE_URL` |
| Firmware toolchain | Arduino IDE / `arduino-cli` | Usa el perfil XIAO ESP32S3 con PSRAM |

## ⚙️ Instalación

### Backend dependencies

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Firmware prerequisites

- Copia `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` a `wifi_credentials.h` (recomendado) y configura SSID/contraseña.
- En Arduino IDE, usa la placa `ESP32 -> XIAO_ESP32S3` con `PSRAM: OPI PSRAM`.
- Esquema de partición: `Default with spiffs (3MB APP/1.5MB SPIFFS)` o `Maximum APP` cuando no se necesite filesystem.

## ▶️ Usage

### Ejecutar backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Ejecutar backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Abrir dashboard

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Propósito |
|---|---|
| `/` | Dashboard principal (UI compatible con PWA) |
| `/healthz` | Comprobación de vida del backend |
| `/ws/audio-ingest` | WebSocket de ingesta del dispositivo |
| `/ws/stream` | Fanout de stream en vivo para clientes del dashboard |

### Inicia sesión y vincula tu dispositivo

1. Regístrate o inicia sesión desde `Settings/Account` en el dashboard.
2. Asocia tu ID de dispositivo en el campo `Bind device`.
3. Solo los dispositivos asociados harán streaming a tu cuenta.

Genera un ID de dispositivo y una imagen QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Vincular mediante API (requiere sesión por cookie):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Verifica la cuenta actual y los dispositivos vinculados:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Migración opcional (renombrar datos históricos a un nuevo ID de dispositivo):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Compilar/subir firmware (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

If port is busy: `fuser -k /dev/ttyACM0`.
If permission denied: `sudo usermod -aG dialout $USER` then re-login (or temporary `sudo chmod a+rw /dev/ttyACM0`).

### UX de encendido del firmware (XIAO ESP32S3)

- Mantén presionado el botón ~0.8 s al encender para arrancar.
- Mantén presionado ~2.5 s mientras está en funcionamiento para entrar en deep sleep.
- Una pulsación corta durante el funcionamiento sigue iniciando captura.

## 🛠️ Configuración

### Variables de entorno principales

- `DATABASE_URL`: DSN de Postgres opcional para almacenamiento persistente.
- `IDEASGLASS_WHISPER_MODEL`: `base` (predeterminado), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` o `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` para precisión mixta en GPU, `0` para CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (predeterminado) para habilitar transcripción, `0` para desactivarla.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: intervalo de transcripción en curso.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: umbrales separados por comas (valor predeterminado `3000,6000,15000`).

| Variable | Default / options | Effect |
|---|---|---|
| `DATABASE_URL` | unset by default | Habilita persistencia en Postgres para datos de cuenta/dispositivo |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Controla la precisión frente a la latencia |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` o `cpu` | Motor de inferencia |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | Control de precisión mixta |
| `IDEASGLASS_TRANSCRIBE` | `1` | Activa o desactiva el pipeline de transcripción |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configurado en runtime | Intervalo de envío de transcripción en continuo |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Umbrales de emisión progresiva de transcripción |

Safe `DATABASE_URL` examples:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (autenticación peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (autenticación por contraseña)

### Ajustes de ganancia y segmentación de audio

- `IDEASGLASS_GAIN_TARGET` (predeterminado `0.032`)
- `IDEASGLASS_GAIN_MAX` (predeterminado `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (predeterminado `0.008`)
- `IDEASGLASS_SPEECH_RMS` (predeterminado `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (predeterminado `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (predeterminado `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (predeterminado `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (hereda el objetivo de ganancia de chunk)

| Audio knob | Default | Purpose |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Normalización RMS objetivo |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Límite superior para la amplificación |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Umbral mínimo para evitar amplificar casi silencio |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Umbral base de actividad de voz en RMS |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Margen alrededor del umbral de voz |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Duración objetivo del segmento |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Solapamiento de segmentos para continuidad |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hereda del chunk | Objetivo de normalización a nivel de segmento |

### Precarga de modelo (opcional)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Ejemplos

### Generar y vincular un ID de dispositivo

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Luego configura `kDeviceId` en:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Flujo del dashboard:

1. Regístrate/inicia sesión en Settings.
2. Vincula el dispositivo en el panel de Account.
3. Solo los dispositivos vinculados envían stream a tu cuenta.

### Ejemplos de ingesta REST

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
    "photo_base64":"'"$(base64 -w0 sample.jpg)'"",
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
    "audio_base64":"'"$(base64 -w0 temp.raw)'""
  }'
```

```bash
curl http://localhost:8765/api/v1/audio/segments | jq '.[0]'
curl -o latest.wav http://localhost:8765/api/v1/audio/segments/<segment-id>
```

## 🧭 Notas de desarrollo

### Área de enfoque

Este repositorio contiene varias trazas de backend. La guía para contribuyentes y el foco de runtime actual es `backend/glass/` salvo que se solicite otra cosa.

### Verificación estática/sintaxis

```bash
python -m compileall backend/glass/app.py
```

### Documentación para desarrolladores

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Nota: En la instantánea actual del repositorio, algunos enlaces históricos parecen haberse movido (por ejemplo, las notas de bridge ahora están en `references/ideasglass_bridge.md`). Los enlaces originales se mantienen como contenido canónico del README.

### Enlace rápido de dispositivo (flujo preservado)

- Genera un ID (en conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Configúralo en firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Ejecuta backend y abre `http://localhost:8765`, regístrate/inicia sesión, luego vincula el ID del dispositivo en el panel de Account

## 🆘 Solución de problemas

- **Puerto ya en uso:** ejecuta el backend en otro puerto y actualiza la configuración del cliente.
- **Puerto serial ocupado:** `fuser -k /dev/ttyACM0`.
- **Permisos de serial en Linux denegados:** `sudo usermod -aG dialout $USER` y vuelve a iniciar sesión.
- **Postgres no disponible:** el backend puede funcionar sin DB para funcionalidad parcial; verifica `DATABASE_URL` y reinicia.
- **Problemas de rendimiento de Whisper:** usa modelos más pequeños (`base`/`small`) o desactiva la transcripción con `IDEASGLASS_TRANSCRIBE=0`.
- **Inestabilidad de TLS/sincronización horaria en ESP32:** verifica Wi-Fi, disponibilidad de NTP (UDP/123) y ajustes de certificado/host; consulta `references/ideasglass_bridge.md` para notas de campo detalladas.
- **No llegan actualizaciones de onda en vivo:** revisa logs del backend y consola del navegador para ver trazas `[IdeasGlass][wave]` y confirma conectividad en `/ws/stream`.

## 🌐 Enlaces del ecosistema

🧠 **EchoMind** — Compañía de IA multilingüe para aprender y crear.
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Comunidad de research-to-product para ideas audaces.
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatizaciones para convertir pequeñas victorias en ingresos.
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Rutas y cuadernos de física y química.
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agente que convierte ideas en borradores, tareas y publicaciones.
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Captura, traduce y auto-produce reels destacados.
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Recompensas y pagos que conectan contribuciones con valor on-chain.
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Cuaderno de notas de investigación y ensayos.
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Estudio detrás de OnlyIdeas, EchoMind, LazyEdit y IdeasGlass.
[lazying.art](https://lazying.art)

## 🙏 Agradecimientos

Nos apoyamos en proyectos open source excelentes — gracias a:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Programa de referidos** — Usa el cupón `LazyingArt` para ahorrar 10% (desbloquea 30% de comisión tras 10 ventas).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Hoja de ruta

- Reforzar y documentar el camino end-to-end de streaming de audio en entornos WAN/TLS.
- Seguir mejorando los trade-offs de calidad/latencia de transcripción (preajustes de modelo/dispositivo/umbrales).
- Expandir la gestión de dispositivos y flujos multi-dispositivo por cuenta en el dashboard.
- Alinear o consolidar tracks legacy/paralelos de backend (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) con la ruta principal `backend/glass`.
- Mantener y actualizar las variantes multilingües del README bajo `i18n/`.

## 🤝 Contribución

Las contribuciones son bienvenidas. Para la guía específica del repositorio, sigue `AGENTS.md`.

Validación local recomendada antes de abrir un PR:

```bash
python -m compileall backend/glass/app.py
```

Al enviar cambios:

- Mantén asuntos de commit cortos y orientados a acción (tiempo presente).
- Menciona variables de entorno relevantes (por ejemplo `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) en las notas de PR cuando el comportamiento dependa de ellas.
- Incluye evidencia de pruebas (logs del backend, comportamiento del dashboard, salida del firmware).
- Nunca subas secretos (`DATABASE_URL`, tokens de API, archivos de credenciales).

## 📄 Licencia

No se detectó un archivo `LICENSE` de nivel superior en esta instantánea del repositorio. Hasta que se añada un archivo de licencia explícito, trata el uso y redistribución como que requieren aprobación del mantenedor.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
