[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*Unas gafas wearables con IA que convierten ideas en acciones, ingresos e impulso creativo.*

> Pipeline de IA wearable con enfoque de voz: captura desde gafas ESP32, procesa en FastAPI y monitoriza/controla desde un dashboard PWA en vivo.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

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

Explora experimentos de la comunidad en <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Descripción general

IdeasGlass es un sistema wearable AI-first para captura y ejecución de ideas con enfoque de voz. En este repositorio, la ruta principal de ejecución es:

- `backend/glass/` para APIs FastAPI, ingesta WebSocket, transcripción basada en Whisper y el dashboard PWA instalable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` para firmware de XIAO ESP32S3 que transmite telemetría/audio/fotos.

Si eres nuevo en este repositorio, empieza por ahí.

### Resumen rápido

| Área | Ubicación principal | Qué hace |
|---|---|---|
| Backend API + PWA | `backend/glass/` | Endpoints FastAPI, ingesta/distribución por WebSocket, transcripción, dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Cliente ESP32 de captura/streaming |
| Notas del bridge | `references/ideasglass_bridge.md` | Notas de fiabilidad TLS/WAN y consejos de despliegue en campo |
| Traducciones del README | `i18n/` | Documentación multilingüe sincronizada desde el README canónico |

## ✨ Por qué IdeasGlass

IdeasGlass es un wearable AI-first pensado para personas que viven en un flujo constante de ideas. Captura, traduce, organiza y ejecuta la creatividad justo cuando llega la inspiración, tanto si narras un concepto en movimiento como si diriges una sesión en vivo.

## 🧩 Funciones

### Funciones de visión de producto

- **Hardware nativo para creación** – gafas ligeras e inputs wearables, ajustados para captura por voz y atajos gestuales sutiles.
- **Traducción instantánea** – detección/traducción de idioma en tiempo real para idear con equipos o audiencias sin cambiar de herramienta.
- **Copiloto EchoMind** – integración estrecha con `chat.lazying.art` para brainstorming, redacción de guiones y coaching de contenido multilingüe.
- **Autopilot de canal** – redacta esquemas, guiones largos, hooks cortos y programa publicaciones en YouTube u otros canales.
- **Highlights y reels** – selecciona momentos automáticamente, genera miniaturas, subtítulos y clips listos para redes.
- **Capa de ingresos** – conecta con LazyingArt Coin para propinas, pagos por créditos y conversión a activos on-chain.
- **Gasto y enfoque** – rastrea el gasto operativo, muestra formatos rentables y destila tus fortalezas personales hacia próximos proyectos.

### Funciones del repositorio/runtime

- Backend FastAPI con endpoints REST + WebSocket para ingesta (`/api/v1/audio`, `/ws/audio-ingest`) y distribución de stream en vivo (`/ws/stream`).
- Segmentación de audio determinista (por defecto ~15 s con solapamiento) en `backend/glass/audio_segments/`.
- Transcripciones streaming opcionales con openai-whisper y umbrales de latencia configurables.
- Persistencia opcional en Postgres (`DATABASE_URL`) para mensajes, fotos, chunks, segmentos y transcripciones.
- Dashboard PWA con forma de onda en vivo, actualizaciones de transcripción y soporte de instalación en desktop/móvil.
- Soporte de firmware Arduino para flujos de cámara + micrófono de XIAO ESP32S3 Sense.

## 🔄 Flujo de trabajo de ejemplo

1. **Captura** – Habla o bosqueja un concepto; IdeasGlass transcribe, traduce y etiqueta la intención.
2. **Co-crea** – EchoMind refina la idea, redacta guiones y sugiere CTAs adaptadas a cada plataforma.
3. **Publica** – El agente del canal autoproduce videos destacados, imágenes de galería y los sube con metadatos.
4. **Monetiza** – Los créditos pasan por LazyingArt Coin (`coin.lazying.art`) y los pagos se sincronizan con tus wallets preferidas.
5. **Reflexiona** – Los paneles de gasto, alcance e interacción muestran qué conviene potenciar después.

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
│   ├── tornado_app/                       # Ruta secundaria/paralela de backend de ingesta
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Notas de bridge + despliegue
├── docs/                                  # Recursos adicionales de sitio/docs
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
- Para firmware: Arduino IDE o `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM activada

| Componente | Requisito | Notas |
|---|---|---|
| Runtime backend | Python 3.10+, `pip` | Usa venv o conda (`glass`) |
| Aceleración GPU (opcional) | NVIDIA + CUDA/cuDNN | Mejora la latencia de Whisper |
| Persistencia (opcional) | PostgreSQL | Se habilita con `DATABASE_URL` |
| Toolchain firmware | Arduino IDE / `arduino-cli` | Usa el perfil XIAO ESP32S3 con PSRAM |

## ⚙️ Instalación

### Dependencias del backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Requisitos del firmware

- Copia `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` a `wifi_credentials.h` (recomendado) y configura SSID/contraseña.
- En Arduino IDE, usa la placa `ESP32 -> XIAO_ESP32S3` con `PSRAM: OPI PSRAM`.
- Esquema de partición: `Default with spiffs (3MB APP/1.5MB SPIFFS)` o `Maximum APP` cuando no se necesita filesystem.

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
| `/healthz` | Verificación de vida del backend |
| `/ws/audio-ingest` | WebSocket de ingesta del dispositivo |
| `/ws/stream` | Distribución de stream en vivo para clientes del dashboard |

### Inicia sesión y vincula tu dispositivo

1. Regístrate o inicia sesión desde el área Settings/Account del dashboard.
2. Vincula tu ID de dispositivo en el campo `Bind device`.
3. Solo los dispositivos vinculados transmitirán a tu cuenta.

Genera un ID de dispositivo + imagen QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Vincular por API (requiere sesión por cookie):

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

Si el puerto está ocupado: `fuser -k /dev/ttyACM0`.
Si aparece permiso denegado: `sudo usermod -aG dialout $USER` y vuelve a iniciar sesión (o temporalmente `sudo chmod a+rw /dev/ttyACM0`).

### UX de energía del firmware (XIAO ESP32S3)

- Mantén pulsado el botón ~0.8 s al encender para arrancar.
- Mantén ~2.5 s durante ejecución para entrar en deep sleep.
- Una pulsación corta durante ejecución sigue activando la captura.

## 🛠️ Configuración

### Variables de entorno principales

- `DATABASE_URL`: DSN de Postgres opcional para almacenamiento persistente.
- `IDEASGLASS_WHISPER_MODEL`: `base` (por defecto), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` o `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` para precisión mixta en GPU, `0` para CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (por defecto) para habilitar transcripción, `0` para deshabilitar.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: intervalo de transcripción continua.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: umbrales separados por comas (por defecto `3000,6000,15000`).

| Variable | Valores por defecto / opciones | Efecto |
|---|---|---|
| `DATABASE_URL` | sin valor por defecto | Habilita persistencia Postgres para datos de cuenta/dispositivo |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Controla precisión vs latencia |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` o `cpu` | Backend de inferencia |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` seguro para CPU | Control de precisión mixta |
| `IDEASGLASS_TRANSCRIBE` | `1` | Activa/desactiva el pipeline de transcripción |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configurado en runtime | Intervalo de envío de transcripción continua |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Umbrales progresivos de emisión de transcripción |

Ejemplos seguros de `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (autenticación peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (autenticación por contraseña)

### Controles de ganancia y segmentación de audio

- `IDEASGLASS_GAIN_TARGET` (por defecto `0.032`)
- `IDEASGLASS_GAIN_MAX` (por defecto `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (por defecto `0.008`)
- `IDEASGLASS_SPEECH_RMS` (por defecto `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (por defecto `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (por defecto `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (por defecto `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (por defecto usa el objetivo de ganancia del chunk)

| Control de audio | Valor por defecto | Propósito |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Normalización RMS objetivo |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Límite superior para amplificación de ganancia |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Piso para evitar amplificar casi silencio |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Línea base RMS para actividad de voz |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Margen alrededor del umbral de voz |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Duración objetivo del segmento |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Solapamiento entre segmentos para continuidad |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hereda la ganancia del chunk | Objetivo de normalización a nivel segmento |

### Prefetch de modelos (opcional)

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

Después configura `kDeviceId` en:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Flujo en dashboard:

1. Regístrate/inicia sesión en Settings.
2. Vincula el dispositivo en el panel Account.
3. Solo los dispositivos vinculados transmiten a tu cuenta.

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

## 🧭 Notas de desarrollo

### Área de enfoque

Este repositorio contiene varias líneas de backend. La guía actual para contribuidores y el foco de runtime es `backend/glass/`, salvo que se indique lo contrario.

### Verificación estática/sintaxis

```bash
python -m compileall backend/glass/app.py
```

### Documentación para desarrolladores

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Nota: En el snapshot actual del repositorio, algunos enlaces históricos de arriba parecen haberse movido (por ejemplo, las notas del bridge ahora existen en `references/ideasglass_bridge.md`). Los enlaces originales se conservan como contenido canónico del README.

### Vinculación rápida de dispositivo (flujo preservado)

- Genera ID (en conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Configúralo en firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Ejecuta backend y abre `http://localhost:8765`, regístrate/inicia sesión, luego vincula el ID de dispositivo en el panel Account

## 🆘 Resolución de problemas

- **Puerto ya en uso:** ejecuta el backend en otro puerto y actualiza la configuración del cliente.
- **Puerto serie ocupado:** `fuser -k /dev/ttyACM0`.
- **Permiso denegado en puerto serie (Linux):** `sudo usermod -aG dialout $USER` y vuelve a iniciar sesión.
- **Postgres no disponible:** el backend puede ejecutarse sin DB con funcionalidad parcial; verifica `DATABASE_URL` y reinicia.
- **Problemas de rendimiento con Whisper:** usa modelos más pequeños (`base`/`small`) o desactiva transcripción con `IDEASGLASS_TRANSCRIBE=0`.
- **Inestabilidad TLS/sincronización de hora en ESP32:** verifica Wi-Fi, disponibilidad de NTP (UDP/123) y configuración de certificado/host; revisa `references/ideasglass_bridge.md` para notas detalladas de campo.
- **Sin actualizaciones de forma de onda en vivo:** revisa logs del backend y consola del navegador buscando trazas `[IdeasGlass][wave]` y confirma conectividad con `/ws/stream`.

## 🌐 Enlaces del ecosistema

🧠 **EchoMind** — Compañero de IA multilingüe para aprendizaje y creación.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Comunidad de investigación a producto para conceptos audaces.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatizaciones para convertir pequeñas victorias en ingresos.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Rutas y cuadernos de física y química.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agente que convierte ideas en borradores, tareas y publicaciones.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Captura, traduce y autoproduce reels destacados.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Recompensas y pagos que conectan contribuciones con valor on-chain.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Cuaderno de notas de investigación y ensayos.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Estudio detrás de OnlyIdeas, EchoMind, LazyEdit e IdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ Soporte y contacto

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- Tu apoyo mantiene en marcha la hoja de ruta del wearable, los agentes y el ecosistema.

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

- Para alianzas, escribe a **contact@lazying.art** con el asunto `IdeasGlass`.

IdeasGlass es donde los wearables con IA dejan de solo escuchar y empiezan a construir contigo.

## 🙏 Agradecimientos

Nos apoyamos en grandes proyectos open source. Gracias a:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Programa de referidos** — Usa el cupón `LazyingArt` para ahorrar 10% (la comisión del 30% se desbloquea después de 10 ventas).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Hoja de ruta

- Reforzar y documentar la ruta de streaming de audio end-to-end en entornos WAN/TLS.
- Seguir mejorando el equilibrio calidad/latencia de transcripción (presets de modelo/dispositivo/umbrales).
- Ampliar la gestión de dispositivos y los flujos multi-dispositivo por cuenta en el dashboard.
- Alinear o consolidar líneas de backend legacy/paralelas (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) con la ruta principal `backend/glass`.
- Mantener y actualizar las variantes multilingües del README en `i18n/`.

## 🤝 Contribución

Las contribuciones son bienvenidas. Para la guía de flujo específica del repositorio, sigue `AGENTS.md`.

Validación local recomendada antes de abrir un PR:

```bash
python -m compileall backend/glass/app.py
```

Al enviar cambios:

- Mantén los asuntos de commit cortos y orientados a acciones (tiempo presente).
- Menciona variables de entorno relevantes (por ejemplo, `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) en las notas del PR cuando el comportamiento dependa de ellas.
- Incluye evidencia de pruebas (logs backend, comportamiento del dashboard, salida de firmware).
- Nunca subas secretos (`DATABASE_URL`, tokens de API, archivos de credenciales).

## 📄 Licencia

No se detectó un archivo `LICENSE` en la raíz en este snapshot del repositorio. Hasta que se añada una licencia explícita, considera que el uso y la redistribución requieren aprobación del mantenedor.
