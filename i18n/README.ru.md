[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*Носимые AI-очки, которые превращают идеи в действия, доход и творческий импульс.*

> Голосовой пайплайн: запись с очков ESP32, обработка в FastAPI и мониторинг/управление через живую PWA-дашборд.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Направление | Назначение |
|---|---|
| 🎙️ Захват с носимых устройств | Очки ESP32 отправляют аудио, фото и телеметрию почти в реальном времени |
| 🧠 Интеллект бэкенда | FastAPI принимает потоки, транскрибирует, сегментирует и хранит метаданные |
| 🖥️ Дашборд | PWA показывает живую волну звука, транскрипты, а также статус устройства и аккаунта |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>Интерфейс приложения (слева) · Оборудование (справа)</sub>
</div>

Исследуйте эксперименты сообщества на <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Обзор

IdeasGlass — AI-first носимая система для захвата и реализации идей в голосовом режиме. В этом репозитории основной путь выполнения следующий:

- `backend/glass/` для API FastAPI, приема WebSocket-потока, транскрипции на базе Whisper и installable PWA-дашборда.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` для прошивки XIAO ESP32S3, которая стримит телеметрию, аудио и фото.

Если вы только начали работу с этим репозиторием, начните с этого пути.

## 📚 Оглавление

- [🚀 Обзор](#-обзор)
- [✨ Почему IdeasGlass](#-почему-ideasglass)
- [🧩 Возможности](#-возможности)
- [🔄 Пример рабочего процесса](#-пример-рабочего-процесса)
- [🗂️ Структура проекта](#-структура-проекта)
- [🧰 Требования](#-требования)
- [⚙️ Установка](#️-установка)
- [▶️ Использование](#️-использование)
- [🛠️ Конфигурация](#️-конфигурация)
- [🧪 Примеры](#-примеры)
- [🧭 Заметки по разработке](#-заметки-по-разработке)
- [🆘 Устранение неполадок](#️-устранение-неполадок)
- [🌐 Ссылки экосистемы](#-ссылки-экосистемы)
- [🙏 Благодарности](#-благодарности)
- [🛣️ Дорожная карта](#️-дорожная-карта)
- [🤝 Участие](#-участие)
- [❤️ Support](#-support)
- [📄 Лицензия](#-лицензия)

### На первый взгляд

| Область | Основное место | Назначение |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPI endpoints, WebSocket ingest/fanout, транскрипция, дашборд |
| Прошивка | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Клиент для захвата/стриминга на ESP32 |
| Записки по мосту | `references/ideasglass_bridge.md` | Заметки по надежности TLS/WAN и советам по деплою |
| Переводы README | `i18n/` | Мультиязычная документация, синхронизированная с каноническим README |

## ✨ Почему IdeasGlass

IdeasGlass — носимая система, ориентированная на AI, для людей, живущих в потоке идей. Она захватывает, переводит, структурирует и реализует творческие идеи в момент вдохновения, будь то голосовой рассказ во время движения или проведение живой сессии.

## 🧩 Возможности

### Функции продуктового видения

- **Creation-native hardware** — легкие очки и носимые входы, настроенные под голосовой захват и скрытые жестовые шорткаты.
- **Мгновенный перевод** — детекция языка и перевод в реальном времени, чтобы можно было генерировать идеи в разных командах или для разных аудиторий без смены инструментов.
- **Co-pilot EchoMind** — плотная интеграция с `chat.lazying.art` для мозгового штурма, черновиков сценариев и многоязыкового контент-наставничества.
- **Автопилот канала** — создает черновики структуры, длинных сценариев, коротких хуков и планирует загрузки на YouTube или другие каналы.
- **Highlights & reels** — автоматически выбирает важные моменты, генерирует обложки, субтитры и клипы, готовые для соцсетей.
- **Слой монетизации** — связывается с LazyingArt Coin для донатов, выплат в кредитах и конверсии в on-chain активы.
- **Траты и фокус** — отслеживает операционные расходы, выделяет прибыльные форматы и преобразует ваши сильные стороны в следующие проекты.

### Функции репозитория и рантайма

- FastAPI backend с REST + WebSocket endpoint'ами для ingest (`/api/v1/audio`, `/ws/audio-ingest`) и live stream fanout (`/ws/stream`).
- Детерминированная сегментация аудио (по умолчанию ~15 с с перекрытием) в `backend/glass/audio_segments/`.
- Опциональная потоковая транскрипция openai-whisper с настраиваемыми порогами задержки.
- Опциональное хранение в Postgres (`DATABASE_URL`) для сообщений, фото, чанков, сегментов и транскриптов.
- PWA-дашборд с живой формой сигнала, обновлениями расшифровки и поддержкой установки на desktop/mobile.
- Поддержка прошивки Arduino для pipelines камеры и микрофона XIAO ESP32S3 Sense.

## 🔄 Пример рабочего процесса

1. **Захват** — Говорите или набросайте идею; IdeasGlass транскрибирует, переводит и помечает намерение.
2. **Совместное создание** — EchoMind уточняет идею, готовит черновики сценариев и подбирает CTA для каждой платформы.
3. **Публикация** — агент канала автоматически создает короткие видео, изображения галереи и загружает их с метаданными.
4. **Монетизация** — кредиты проходят через LazyingArt Coin (`coin.lazying.art`), а выплаты синхронизируются с выбранными кошельками.
5. **Рефлексия** — дашборды трат, охвата и вовлеченности показывают, на чем стоит делать ставку дальше.

## 🗂️ Структура проекта

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
│   ├── IdeasGlassClient/
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Bridge + deployment notes
├── docs/                                  # Additional site/docs assets
├── development_plan/
├── app/
├── ops/observability/
├── ios-app-example/
├── figs/
├── seeed_studio_xiao_esp32s3_dev/
└── .auto-readme-work/
```

## 🧰 Требования

- Python 3.10+
- `pip` (или conda-окружение с совместимой версией Python)
- Опционально: NVIDIA GPU + CUDA/cuDNN для ускоренного вывода Whisper
- Опционально: PostgreSQL для персистентности
- Для прошивки: Arduino IDE или `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM включен

| Компонент | Требование | Примечания |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | Используйте venv или conda (`glass`) |
| GPU acceleration (optional) | NVIDIA + CUDA/cuDNN | Уменьшает задержку Whisper |
| Persistent storage (optional) | PostgreSQL | Включается через `DATABASE_URL` |
| Firmware toolchain | Arduino IDE / `arduino-cli` | Используйте профиль XIAO ESP32S3 с PSRAM |

## ⚙️ Установка

### Зависимости backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Требования к прошивке

- Скопируйте `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` в `wifi_credentials.h` (рекомендуется) и укажите SSID/пароль.
- В Arduino IDE используйте плату `ESP32 -> XIAO_ESP32S3` с `PSRAM: OPI PSRAM`.
- Схема разделов: `Default with spiffs (3MB APP/1.5MB SPIFFS)` или `Maximum APP`, если файловая система не нужна.

## ▶️ Использование

### Запустить backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Запустить backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Открыть дашборд

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Назначение |
|---|---|
| `/` | Основной дашборд (UI с поддержкой PWA) |
| `/healthz` | Проверка доступности backend |
| `/ws/audio-ingest` | WebSocket ingest с устройства |
| `/ws/stream` | Live stream fanout для клиентов дашборда |

### Вход и привязка устройства

1. Зарегистрируйтесь или войдите через раздел Settings/Account.
2. Привяжите ID устройства в поле `Bind device`.
3. Только привязанные устройства будут стримить на ваш аккаунт.

Сгенерировать device ID + QR-изображение:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Привязка через API (требуется cookie-сессия):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Проверить текущий аккаунт и привязанные устройства:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Опциональная миграция (переименование исторических данных на новый ID устройства):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Сборка/загрузка прошивки (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Если порт занят: `fuser -k /dev/ttyACM0`.
Если permission denied: `sudo usermod -aG dialout $USER`, затем повторный вход (или временно `sudo chmod a+rw /dev/ttyACM0`).

### Управление питанием прошивки (XIAO ESP32S3)

- Удерживайте кнопку ~0.8 с при включении питания, чтобы загрузиться.
- Удерживайте ~2.5 с во время работы, чтобы войти в глубокий сон.
- Короткое нажатие во время работы по-прежнему запускает захват.

## 🛠️ Конфигурация

### Ключевые переменные окружения

- `DATABASE_URL`: необязательный DSN Postgres для постоянного хранения.
- `IDEASGLASS_WHISPER_MODEL`: `base` (по умолчанию), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` или `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` для mixed precision на GPU, `0` для CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (по умолчанию) для включения транскрипции, `0` для отключения.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: интервал «rolling» транскрипции.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: пороги через запятую (по умолчанию `3000,6000,15000`).

| Variable | Default / options | Effect |
|---|---|---|
| `DATABASE_URL` | по умолчанию не задано | Включает персистентное хранение данных аккаунта и устройств в Postgres |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Влияет на баланс точности и задержки |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` или `cpu` | Бекенд инференса |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | Управление mixed precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Переключатель транскрипционного пайплайна |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | runtime configured | Интервал отправки rolling-транскриптов |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Пороговые уровни прогрессивной выдачи транскрипта |

Примеры `DATABASE_URL` с безопасными значениями:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (peer/local auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (password auth)

### Параметры усиления и сегментации звука

- `IDEASGLASS_GAIN_TARGET` (по умолчанию `0.032`)
- `IDEASGLASS_GAIN_MAX` (по умолчанию `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (по умолчанию `0.008`)
- `IDEASGLASS_SPEECH_RMS` (по умолчанию `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (по умолчанию `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (по умолчанию `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (по умолчанию `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (по умолчанию наследуется от чанка)

| Параметр аудио | Default | Назначение |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Нормализация целевого RMS |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Верхний лимит усиления |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Пол для подавления усиления почти тишины |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Базовый RMS порога речевой активности |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Допуск вокруг порога речи |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Целевая длина сегмента |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Перекрытие сегментов для непрерывности |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | наследуется от chunk | Целевая нормализация на уровне сегмента |

### Предзагрузка модели (опционально)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Примеры

### Сгенерировать и привязать device ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Затем укажите `kDeviceId` в:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Сценарий работы дашборда:

1. Зарегистрируйтесь/войдите в Settings.
2. Привяжите устройство в блоке Account.
3. К вашему аккаунту будут стримить только привязанные устройства.

### REST ingest-примеры

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

## 🧭 Заметки по разработке

### Фокус

В этом репозитории есть несколько backend-треков. Основной рабочий фокус и runtime-приоритет — `backend/glass/`, если не указано иное.

### Проверка синтаксиса

```bash
python -m compileall backend/glass/app.py
```

### Документация для разработчиков

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Примечание: в текущем снапшоте репозитория некоторые исторические ссылки выше могли быть перемещены (например, заметки моста теперь находятся в `references/ideasglass_bridge.md`). Оригинальные ссылки сохранены как канонический контент README.

### Быстрая привязка устройства (сохраняемый workflow)

- Сгенерируйте ID (в conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Укажите его в прошивке: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Запустите backend и откройте `http://localhost:8765`, затем зарегистрируйтесь/войдите и привяжите device ID в панели Account

## 🆘 Устранение неполадок

- **Порт занят:** запустите backend на другом порту и обновите настройки клиента.
- **Serial-порт занят:** `fuser -k /dev/ttyACM0`.
- **Нет доступа к serial в Linux:** `sudo usermod -aG dialout $USER` и заново войдите.
- **Postgres недоступен:** backend может частично работать без БД; проверьте `DATABASE_URL` и перезапустите.
- **Проблемы с производительностью Whisper:** используйте меньшие модели (`base`/`small`) или отключите транскрипцию через `IDEASGLASS_TRANSCRIBE=0`.
- **Нестабильность TLS/time sync на ESP32:** проверьте Wi-Fi, доступность NTP (UDP/123), cert/host-настройки; см. `references/ideasglass_bridge.md`.
- **Нет обновлений live waveform:** проверьте логи backend и консоль браузера на наличие трасс `[IdeasGlass][wave]`, убедитесь в связности `/ws/stream`.

## 🌐 Ссылки экосистемы

| Бренд | Назначение | Ссылка |
|---|---|---|
| 🧠 EchoMind | Многоязычный AI-ассистент для обучения и создания | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | Сообщество research-to-product для смелых идей | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | Автоматизация превращения маленьких побед в доход | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | Курсы и тетради по физике и химии | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | Агент, который превращает идеи в черновики, задачи и посты | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | Захват, перевод и автоматическое создание highlight-reels | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | Награды и выплаты: связка вклада с on-chain стоимостью | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | Блокнот с заметками и эссе | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | Студия за OnlyIdeas, EchoMind, LazyEdit и IdeasGlass | [lazying.art](https://lazying.art) |

## 🙏 Благодарности

Мы опираемся на отличные открытые проекты — благодарим их:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — используйте купон `LazyingArt` для скидки 10% (комиссия 30% открывается после 10 продаж).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Дорожная карта

- Ужесточить и задокументировать сквозной путь потокового аудио в WAN/TLS-средах.
- Продолжать улучшать качество/задержку транскрипции (настройки модели, устройства и порогов).
- Расширять управление устройствами и рабочие процессы с несколькими устройствами в рамках аккаунта в дашборде.
- Упорядочить и/или объединить legacy/parallel backend-треки (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) с основным путем `backend/glass`.
- Поддерживать и обновлять мультиязычные версии README в `i18n/`.

## 🤝 Участие

Вклады приветствуются. Для рабочих инструкций репозитория используйте `AGENTS.md`.

Рекомендуемая локальная проверка перед открытием PR:

```bash
python -m compileall backend/glass/app.py
```

При отправке изменений:

- Держите заголовки коммитов короткими и ориентированными на действие (настоящее время).
- Указывайте соответствующие переменные окружения (например, `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) в описании PR, если поведение зависит от них.
- Добавляйте доказательства проверки (логи backend, поведение дашборда, вывод firmware).
- Никогда не коммитьте секреты (`DATABASE_URL`, API-токены, файлы с учетными данными).

## 📄 Лицензия

В текущем снимке репозитория отсутствует файл `LICENSE` на верхнем уровне. Пока явный файл лицензии не добавлен, используйте и распространяйте только после согласования с мейнтейнером.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
