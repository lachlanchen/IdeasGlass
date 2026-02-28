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
| 🖥️ Dashboard | La PWA muestra forma de onda en vivo, transcripciones y estado del dispositivo/cuenta |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="Interfaz de la app IdeasGlass" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="Hardware de IdeasGlass" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>UI de la app (izquierda) · Hardware (derecha)</sub>
</div>

Explora los experimentos de la comunidad en <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Visión general

IdeasGlass es un sistema wearable AI-first para captura y ejecución de ideas con enfoque de voz. En este repositorio, la ruta principal de ejecución es:

- `backend/glass/` para APIs de FastAPI, ingesta WebSocket, transcripción con Whisper y el dashboard PWA instalable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` para firmware de XIAO ESP32S3 que transmite telemetría/audio/fotos.

Si eres nuevo en este repositorio, comienza ahí.

## 📚 Índice

- [🚀 Visión general](#-visión-general)
- [✨ Por qué IdeasGlass](#-por-qué-ideasglass)
- [🧩 Características](#-características)
- [🔄 Flujo de trabajo de ejemplo](#-flujo-de-trabajo-de-ejemplo)
- [🗂️ Estructura del proyecto](#-estructura-del-proyecto)
- [🧰 Requisitos previos](#-requisitos-previos)
- [⚙️ Instalación](#️-instalación)
- [▶️ Uso](#️-uso)
- [🛠️ Configuración](#️-configuración)
- [🧪 Ejemplos](#-ejemplos)
- [🧭 Notas de desarrollo](#-notas-de-desarrollo)
- [🆘 Solución de problemas](#️-solución-de-problemas)
- [🌐 Enlaces del ecosistema](#-enlaces-del-ecosistema)
- [🙏 Agradecimientos](#-agradecimientos)
- [🛣️ Hoja de ruta](#️-hoja-de-ruta)
- [🤝 Contribución](#-contribución)
- [❤️ Soporte](#-soporte)
- [📄 Licencia](#-licencia)

### A primera vista

| Área | Ubicación principal | Qué hace |
|---|---|---|
| API del backend + PWA | `backend/glass/` | Endpoints FastAPI, ingesta/distribución por WebSocket, transcripción, dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Cliente de captura/streaming de ESP32 |
| Notas del bridge | `references/ideasglass_bridge.md` | Notas de fiabilidad TLS/WAN y consejos de despliegue |
| Traducciones del README | `i18n/` | Documentación multilingüe sincronizada desde el README canónico |

## ✨ Por qué IdeasGlass

IdeasGlass es un wearable AI-first creado para quienes viven en un flujo continuo de ideas. Captura, traduce, organiza y ejecuta la creatividad en el momento en que surge la inspiración, ya sea que estés narrando un concepto en movimiento o liderando una sesión en vivo.

## 🧩 Características

### Funciones de visión de producto

- **Hardware nativo de creación** – gafas ligeras y entradas vestibles, optimizadas para captura por voz y atajos de gesto sutiles.
- **Traducción instantánea** – detección y traducción de idioma en tiempo real para idear en equipos o audiencias sin cambiar de herramientas.
- **Copiloto EchoMind** – integración estrecha con `chat.lazying.art` para lluvia de ideas, redacción de guiones y coaching de contenido multilingüe.
- **Piloto automático de canal** – genera outlines, guiones largos, hooks cortos y programa subidas a YouTube u otros canales.
- **Highlights y reels** – selecciona momentos automáticamente, genera miniaturas, subtítulos y clips listos para redes.
- **Capa de ingresos** – conecta con LazyingArt Coin para propinas, pagos por créditos y conversión a activos on-chain.
- **Control de gasto y enfoque** – rastrea el gasto operativo, resalta formatos rentables y resume tus fortalezas en futuros proyectos.

### Funciones del repositorio/runtime

- Backend FastAPI con endpoints REST + WebSocket para ingesta (`/api/v1/audio`, `/ws/audio-ingest`) y fanout de stream en vivo (`/ws/stream`).
- Segmentación de audio determinística (15 s por defecto con solapamiento) en `backend/glass/audio_segments/`.
- Transcripciones en streaming con openai-whisper (opcional) con umbrales de latencia configurables.
- Persistencia opcional en Postgres (`DATABASE_URL`) para mensajes, fotos, chunks, segmentos y transcripciones.
- Dashboard PWA con forma de onda en vivo, actualizaciones de transcripción y soporte de instalación en escritorio/móvil.
- Soporte de firmware Arduino para flujos de cámara y micrófono de XIAO ESP32S3 Sense.

## 🔄 Flujo de trabajo de ejemplo

1. **Captura** – Habla o dibuja un concepto; IdeasGlass transcribe, traduce y etiqueta la intención.
2. **Co-creación** – EchoMind refina la idea, redacta guiones y sugiere CTAs adaptados a cada plataforma.
3. **Publicación** – El agente del canal auto-produce videos destacados, imágenes de galería y los sube con metadatos.
4. **Monetización** – Los créditos se enrutan por LazyingArt Coin (`coin.lazying.art`) y los pagos se sincronizan con tus wallets preferidas.
5. **Reflexión** – Los paneles de gasto, alcance y engagement muestran en qué conviene doblar el foco.

## 🗂️ Estructura del proyecto

```text
IdeasGlass/
├── README.md
├── i18n/                                  # Traducciones del README
├── backend/
│   ├── glass/                             # Backend principal FastAPI + PWA
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # Ruta secundaria/paralela de ingesta backend
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Notas de bridge y despliegue
├── docs/                                  # Assets adicionales de sitio/documentación
├── development_plan/
├── app/
├── ops/observability/
├── ios-app-example/
├── figs/
├── seeed_studio_xiao_esp32s3_dev/
└── .auto-readme-work/
```

## 🧰 Requisitos previos

- Python 3.10+
- `pip` (o entorno conda con Python compatible)
- Opcional: GPU NVIDIA + CUDA/cuDNN para inferencia Whisper más rápida
- Opcional: PostgreSQL para persistencia
- Para firmware: Arduino IDE o `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM habilitada

| Componente | Requisito | Notas |
|---|---|---|
| Runtime del backend | Python 3.10+, `pip` | Usa venv o conda (`glass`) |
| Aceleración por GPU (opcional) | NVIDIA + CUDA/cuDNN | Mejora la latencia de Whisper |
| Persistencia (opcional) | PostgreSQL | Habilitada mediante `DATABASE_URL` |
| Cadena de herramientas de firmware | Arduino IDE / `arduino-cli` | Usa el perfil XIAO ESP32S3 con PSRAM |

## ⚙️ Instalación

### Dependencias del backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Requisitos previos de firmware

- Copia `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` a `wifi_credentials.h` (recomendado) y configura SSID/contraseña.
- En Arduino IDE, usa la placa `ESP32 -> XIAO_ESP32S3` con `PSRAM: OPI PSRAM`.
- Esquema de partición: `Default with spiffs (3MB APP/1.5MB SPIFFS)` o `Maximum APP` cuando no se necesite filesystem.

## ▶️ Uso

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

### Iniciar sesión y vincular tu dispositivo

1. Regístrate o inicia sesión desde Configuración/Cuenta del dashboard.
2. Enlaza tu ID de dispositivo en el campo `Bind device`.
3. Solo los dispositivos enlazados harán streaming a tu cuenta.

Genera un ID de dispositivo + imagen QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Vincular por API (requiere sesión con cookies):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Verifica la cuenta actual y dispositivos enlazados:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Migración opcional (renombrar datos históricos a un ID de dispositivo nuevo):

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

Si el puerto está ocupado: `fuser -k /dev/ttyACM0`.
Si aparece "permission denied": `sudo usermod -aG dialout $USER` y vuelve a iniciar sesión (o temporalmente `sudo chmod a+rw /dev/ttyACM0`).

### UX de encendido del firmware (XIAO ESP32S3)

- Mantén pulsado el botón ~0.8 s al encender para iniciar.
- Mantén pulsado ~2.5 s mientras está en funcionamiento para entrar en deep sleep.
- Una pulsación corta durante funcionamiento sigue iniciando captura.

## 🛠️ Configuración

### Variables de entorno principales

- `DATABASE_URL`: DSN de Postgres opcional para almacenamiento persistente.
- `IDEASGLASS_WHISPER_MODEL`: `base` (predeterminado), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` o `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` para precisión mixta en GPU, `0` para CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (predeterminado) para habilitar transcripción, `0` para desactivarla.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: intervalo de transcripción en curso.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: umbrales separados por comas (predeterminado `3000,6000,15000`).

| Variable | Predeterminado / opciones | Efecto |
|---|---|---|
| `DATABASE_URL` | sin establecer por defecto | Habilita persistencia en Postgres para datos de cuenta/dispositivo |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Controla precisión frente a latencia |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` o `cpu` | Motor de inferencia |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` seguro para CPU | Control de precisión mixta |
| `IDEASGLASS_TRANSCRIBE` | `1` | Activa o desactiva el pipeline de transcripción |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configurado en runtime | Intervalo de emisión continua de transcripción |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Umbrales progresivos de emisión de transcripción |

Ejemplos seguros de `DATABASE_URL`:

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
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (hereda el objetivo de ganancia del chunk)

| Control de audio | Predeterminado | Propósito |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Normalización RMS objetivo |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Tope superior para amplificación |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Límite inferior para evitar amplificar casi silencio |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Umbral base de actividad de voz en RMS |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Margen alrededor del umbral de voz |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Duración objetivo de segmento |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Solapamiento de segmento para continuidad |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hereda el objetivo del chunk | Objetivo de normalización a nivel de segmento |

### Precarga de modelo (opcional)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Ejemplos

### Generar y enlazar un ID de dispositivo

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
    "audio_base64":"'"$(base64 -w0 temp.raw)'"'
  }'
```

```bash
curl http://localhost:8765/api/v1/audio/segments | jq '.[0]'
curl -o latest.wav http://localhost:8765/api/v1/audio/segments/<segment-id>
```

## 🧭 Notas de desarrollo

### Área de enfoque

Este repositorio contiene múltiples tracks de backend. La guía de contribución y el foco de ejecución actual está en `backend/glass/`, salvo petición en contrario.

### Verificación estática/sintaxis

```bash
python -m compileall backend/glass/app.py
```

### Documentación de desarrolladores

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Nota: En la instantánea actual del repositorio, algunos enlaces históricos parecen haberse movido (por ejemplo, las notas de bridge ahora existen en `references/ideasglass_bridge.md`). Los enlaces originales se conservan como contenido canónico del README.

### Enlace rápido de enlazado de dispositivo (flujo preservado)

- Genera un ID (en conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Configúralo en firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Ejecuta el backend y abre `http://localhost:8765`, regístrate/inicia sesión y luego enlaza el ID del dispositivo en el panel de Account

## 🆘 Solución de problemas

- **Puerto en uso:** ejecuta el backend en otro puerto y actualiza la configuración del cliente.
- **Puerto serial ocupado:** `fuser -k /dev/ttyACM0`.
- **Permisos de serial denegados en Linux:** `sudo usermod -aG dialout $USER` y vuelve a iniciar sesión.
- **Postgres no disponible:** el backend puede funcionar sin BD para funcionalidad parcial; verifica `DATABASE_URL` y reinicia.
- **Problemas de rendimiento de Whisper:** usa modelos más pequeños (`base`/`small`) o desactiva la transcripción con `IDEASGLASS_TRANSCRIBE=0`.
- **Inestabilidad de TLS/sincronización horaria en ESP32:** verifica Wi-Fi, disponibilidad de NTP (UDP/123) y configuración de certificado/host; consulta `references/ideasglass_bridge.md` para notas de campo detalladas.
- **No llegan actualizaciones de forma de onda en vivo:** revisa los logs del backend y la consola del navegador para ver trazas `[IdeasGlass][wave]` y confirma conectividad en `/ws/stream`.

## 🌐 Enlaces del ecosistema

| Marca | Propósito | Enlace |
|---|---|---|
| 🧠 EchoMind | Compañía AI multilingüe para aprendizaje y creación | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | Comunidad research-to-product para conceptos ambiciosos | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | Automatizaciones para convertir pequeñas victorias en ingresos | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | Rutas y cuadernos de física y química | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | Agente que transforma ideas en borradores, tareas y publicaciones | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | Captura, traduce y auto-produce reels destacados | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | Recompensas y pagos que conectan contribuciones y valor on-chain | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | Cuaderno de notas de investigación y ensayos | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | Estudio detrás de OnlyIdeas, EchoMind, LazyEdit e IdeasGlass | [lazying.art](https://lazying.art) |

## 🙏 Agradecimientos

Nos apoyamos en proyectos open source excelentes — gracias a:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Programa de referidos** — Usa el cupón `LazyingArt` para ahorrar un 10% (desbloquea 30% de comisión tras 10 ventas).

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
- Seguir mejorando el equilibrio calidad/latencia de transcripción (preajustes de modelo/dispositivo/umbrales).
- Expandir la gestión de dispositivos y flujos multi-dispositivo por cuenta en el dashboard.
- Alinear o consolidar tracks legacy/paralelos de backend (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) con la ruta principal `backend/glass`.
- Mantener y refrescar las variantes multilingües del README bajo `i18n/`.

## 🤝 Contribución

Las contribuciones son bienvenidas. Para la guía de flujo del repositorio, sigue `AGENTS.md`.

Validación local recomendada antes de abrir un PR:

```bash
python -m compileall backend/glass/app.py
```

Al enviar cambios:

- Mantén asuntos de commits cortos y orientados a acción (tiempo presente).
- Menciona variables de entorno relevantes (por ejemplo `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) en las notas de PR cuando el comportamiento dependa de ellas.
- Incluye evidencia de pruebas (logs del backend, comportamiento del dashboard, salida del firmware).
- Nunca subas secretos (`DATABASE_URL`, tokens de API, archivos de credenciales).

## ❤️ Soporte

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 Licencia

No se detectó un archivo `LICENSE` a nivel superior en esta instantánea del repositorio. Hasta que se añada un archivo de licencia explícito, trata el uso y la redistribución como sujetos a aprobación del mantenedor.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
