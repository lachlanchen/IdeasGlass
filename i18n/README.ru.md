[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)


# IdeasGlass

*Носимые AI-очки, которые превращают идеи в действия, доход и творческую динамику.*

> Голосовой пайплайн для wearable-устройств: захват с очков на ESP32, обработка в FastAPI и мониторинг/управление через живую PWA-дашборд.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Направление | Цель |
|---|---|
| 🎙️ Захват с носимых устройств | Очки ESP32 передают аудио, фото и телеметрию в почти реальном времени |
| 🧠 Интеллект бэкенда | FastAPI принимает потоки, расшифровывает, сегментирует и сохраняет метаданные |
| 🖥️ Дашборд | PWA показывает живую волну, расшифровки и статус устройства/аккаунта |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Экосистема</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Поддержать IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>UI приложения (слева) · Аппаратура (справа)</sub>
</div>

Изучайте эксперименты сообщества на <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Обзор

IdeasGlass — это AI-first wearable-система для голосового захвата идей и их реализации. Основной рабочий путь в этом репозитории:

- `backend/glass/` — FastAPI API, WebSocket ingest, транскрибация на Whisper и устанавливаемая PWA-дашборд.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` — прошивка XIAO ESP32S3 для потоковой передачи телеметрии/аудио/фото.

Если вы только знакомы с этим репозиторием, начните отсюда.

### Взгляд с высоты

| Область | Основное место | Что делает |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPI endpoint'ы, WebSocket ingest/fanout, транскрибация, дашборд |
| Прошивка | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Клиент захвата и стриминга на ESP32 |
| Записка-мост | `references/ideasglass_bridge.md` | Заметки по TLS/WAN надежности и рекомендациям деплоя |
| Переводы README | `i18n/` | Многоязычная документация, синхронизируемая с основным README |

## ✨ Почему IdeasGlass

IdeasGlass — это wearable, построенный вокруг AI, для людей, живущих в потоке идей. Он захватывает, переводит, структурирует и помогает реализовывать креатив в момент вдохновения: будь то рассказ идеи на ходу или проведение живой сессии.

## 🧩 Функции

### Функции продуктового видения

- **Аппаратно ориентированное создание** — лёгкие очки и интерфейсы ввода, оптимизированные под голосовой захват и незаметные жестовые шорткаты.
- **Мгновенный перевод** — детекция и перевод в реальном времени, чтобы работать с идеями в разных командах и аудиториях без смены инструментов.
- **Co-pilot EchoMind** — плотная связка с `chat.lazying.art` для мозгового штурма, черновиков сценариев и многъязыкового творческого коучинга.
- **Автопилот канала** — черновики планов, длинных скриптов, коротких hook и планирование публикаций в YouTube и другие каналы.
- **Highlights & reels** — автоматический выбор моментов, генерация обложек, субтитров и клипов для соцсетей.
- **Слой монетизации** — связка с LazyingArt Coin для донатов, выплат в кредитах и конверсии в on-chain активы.
- **Финансы и фокус** — учёт расходов, выделение прибыльных форматов и сводка сильных сторон в следующие проекты.

### Функции репозитория и рантайма

- FastAPI backend с REST + WebSocket endpoint'ами для ingest (`/api/v1/audio`, `/ws/audio-ingest`) и живой рассылки потока (`/ws/stream`).
- Детеминированная сегментация аудио (по умолчанию ~15 с с перекрытием) в `backend/glass/audio_segments/`.
- Опциональные стримовые транскрипты на openai-whisper с настраиваемой задержкой.
- Опциональное хранение в Postgres (`DATABASE_URL`) для сообщений, фото, чанков, сегментов и транскриптов.
- PWA-дашборд с живой волной, обновлениями текста и поддержкой установки на desktop/mobile.
- Поддержка Arduino для XIAO ESP32S3 Sense в сценарии камеры + микрофона.

## 🔄 Пример рабочего цикла

1. **Захват** — Говорите или набросайте идею; IdeasGlass расшифровывает, переводит и помечает намерение.
2. **Совместное создание** — EchoMind дорабатывает идею, пишет черновик сценариев и предлагает CTA, адаптированные под каждую платформу.
3. **Публикация** — агент канала автоматически создает шорт-ролики/клипы, изображения галереи и публикует с метаданными.
4. **Монетизация** — кредиты идут через LazyingArt Coin (`coin.lazying.art`), а выплаты синхронизируются с выбранными кошельками.
5. **Рефлексия** — дашборды затрат, охвата и вовлеченности подсказывают, на чем усиливаться дальше.

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

## 🧰 Требования

- Python 3.10+
- `pip` (или conda-окружение с совместимой версией Python)
- По желанию: NVIDIA GPU + CUDA/cuDNN для более быстрого вывода Whisper
- По желанию: PostgreSQL для хранения данных
- Для firmware: Arduino IDE или `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM включён

| Компонент | Требование | Примечание |
|---|---|---|
| Рантайм бэкенда | Python 3.10+, `pip` | Используйте venv или conda (`glass`) |
| Ускорение GPU (опционально) | NVIDIA + CUDA/cuDNN | Ускоряет латентность Whisper |
| Хранение данных (опционально) | PostgreSQL | Включается через `DATABASE_URL` |
| Инструментарий прошивки | Arduino IDE / `arduino-cli` | Используйте профиль XIAO ESP32S3 с PSRAM |

## ⚙️ Установка

### Зависимости для backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Требования к прошивке

- Скопируйте `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` в `wifi_credentials.h` (рекомендуется) и укажите SSID/пароль.
- В Arduino IDE выберите плату `ESP32 -> XIAO_ESP32S3` с `PSRAM: OPI PSRAM`.
- Схема разделов: `Default with spiffs (3MB APP/1.5MB SPIFFS)` или `Maximum APP`, если файловая система не нужна.

## ▶️ Использование

### Запуск backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Запуск backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Открыть дашборд

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Назначение |
|---|---|
| `/` | Главный дашборд (PWA-совместимый UI) |
| `/healthz` | Проверка работоспособности backend |
| `/ws/audio-ingest` | WebSocket ingest с устройства |
| `/ws/stream` | Живая fanout-рассылка для клиентов дашборда |

### Вход и привязка устройства

1. Зарегистрируйтесь или войдите в раздел Settings/Account.
2. Привяжите ID устройства в поле `Bind device`.
3. К вашему аккаунту будут стримить только привязанные устройства.

Сгенерируйте device ID и QR-картинку:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Привязка через API (нужна cookie-сессия):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Проверьте текущий аккаунт и привязанные устройства:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Необязательная миграция (переименовать старые данные на новый ID устройства):

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
Если `permission denied`: `sudo usermod -aG dialout $USER`, затем повторный вход (или временно `sudo chmod a+rw /dev/ttyACM0`).

### Управление питанием прошивки (XIAO ESP32S3)

- Удерживайте кнопку ~0,8 с при подаче питания, чтобы загрузиться.
- Удерживайте ~2,5 с во время работы для входа в глубокий сон.
- Короткое нажатие во время работы по-прежнему запускает захват.

## 🛠️ Конфигурация

### Ключевые переменные окружения

- `DATABASE_URL`: необязательный DSN Postgres для персистентного хранения.
- `IDEASGLASS_WHISPER_MODEL`: `base` (по умолчанию), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` или `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` для mixed precision на GPU, `0` для CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (по умолчанию), чтобы включить транскрибацию; `0`, чтобы отключить.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: интервал обновления текущей транскрипции.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: пороги через запятую (по умолчанию `3000,6000,15000`).

| Переменная | Значение по умолчанию / варианты | Что делает |
|---|---|---|
| `DATABASE_URL` | не задано по умолчанию | Включает хранение данных аккаунта/устройства в Postgres |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Баланс точности и задержки |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` или `cpu` | Backend для инференса |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` безопасно для CPU | Управление mixed precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Включение/выключение пайплайна транскрипции |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | задано в runtime | Интервал публикации rolling-транскрипций |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Пороговые уровни прогрессивной выдачи транскрипции |

Безопасные примеры `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (аутентификация peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (аутентификация с паролем)

### Параметры усиления и сегментации аудио

- `IDEASGLASS_GAIN_TARGET` (по умолчанию `0.032`)
- `IDEASGLASS_GAIN_MAX` (по умолчанию `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (по умолчанию `0.008`)
- `IDEASGLASS_SPEECH_RMS` (по умолчанию `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (по умолчанию `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (по умолчанию `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (по умолчанию `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (по умолчанию наследуется от чанков)

| Регулятор аудио | По умолчанию | Назначение |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Нормализация целевого RMS |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Верхний предел усиления |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Пол для подавления усиления почти тишины |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Базовый RMS порога речевой активности |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Запас вокруг речевого порога |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Целевая длина сегмента |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Наложение сегментов для непрерывности |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | наследуется от чанка | Целевая нормализация на уровне сегмента |

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

Затем установите `kDeviceId` в:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Процесс для дашборда:

1. Зарегистрируйтесь/войдите в Settings.
2. Привяжите устройство в блоке Account.
3. К вашему аккаунту будут стримить только привязанные устройства.

### REST-примеры ingest

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

## 🧭 Заметки по разработке

### Фокус

В этом репозитории есть несколько backend-треков. Если не оговорено иначе, основные приоритеты и фокус выполнения — `backend/glass/`.

### Проверка синтаксиса

```bash
python -m compileall backend/glass/app.py
```

### Документация для разработчиков

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Примечание: в текущем снимке репозитория некоторые исторические ссылки выше могли быть перемещены (например, заметки о мосте теперь находятся в `references/ideasglass_bridge.md`). Оригинальные ссылки сохранены как канонический контент README.

### Быстрая привязка устройства (сохраняемый workflow)

- Сгенерируйте ID (в conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Укажите его в прошивке: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Запустите backend и откройте `http://localhost:8765`, зарегистрируйтесь/войдите, затем привяжите ID устройства в панели Account

## 🆘 Устранение неполадок

- **Порт занят:** запустите backend на другом порту и обновите настройки клиента.
- **Серийный порт занят:** `fuser -k /dev/ttyACM0`.
- **Нет прав доступа к serial в Linux:** `sudo usermod -aG dialout $USER` и переавторизуйтесь.
- **Postgres недоступен:** backend может частично работать без БД; проверьте `DATABASE_URL` и перезапустите.
- **Проблемы с производительностью Whisper:** используйте меньшие модели (`base`/`small`) или выключите транскрипцию через `IDEASGLASS_TRANSCRIBE=0`.
- **Нестабильность TLS/времени на ESP32:** проверьте Wi-Fi, доступность NTP (UDP/123), настройки cert/host; подробности в `references/ideasglass_bridge.md`.
- **Нет обновлений live waveform:** проверьте логи backend и консоль браузера на наличие трейс-сообщений `[IdeasGlass][wave]`, а также убедитесь в соединении `/ws/stream`.

## 🌐 Ссылки экосистемы

🧠 **EchoMind** — Многоязычный AI-компаньон для обучения и творчества.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Сообщество research-to-product для смелых концепций.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Автоматизации для превращения маленьких побед в доход.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Курсы и конспекты по физике и химии.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Агент, который превращает идеи в черновики, задачи и посты.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Захват, перевод и автоматическое создание шортов/реверов.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Награды и выплаты, связывающие вклад и on-chain value.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Блокнот исследовательских заметок и эссе.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Студия behind OnlyIdeas, EchoMind, LazyEdit и IdeasGlass.  
[lazying.art](https://lazying.art)

## 🙏 Благодарности

Мы стоим на плечах отличных открытых проектов — спасибо им:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Реферальная программа** — используйте купон `LazyingArt` для скидки 10% (после 10 продаж открывается 30% комиссии).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Дорожная карта

- Повысить надежность и документировать end-to-end путь потокового аудио в WAN/TLS-средах.
- Продолжить улучшение соотношения качества/задержки транскрипции (пресеты модели/устройства/порогов).
- Расширять управление устройствами и рабочие процессы с несколькими устройствами в рамках аккаунта на дашборде.
- Согласовать и/или консолидировать legacy/parallel backend-треки (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) с основным путём `backend/glass`.
- Поддерживать и обновлять мультиязычные варианты README в `i18n/`.

## 🤝 Вклад

Приветствуются любые вклады. Для рабочих инструкций по репозиторию используйте `AGENTS.md`.

Рекомендуемая локальная проверка перед открытием PR:

```bash
python -m compileall backend/glass/app.py
```

При подаче изменений:

- Держите темы коммитов короткими и ориентированными на действие (настоящее время).
- Указывайте релевантные env vars (например, `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) в заметках к PR, если поведение зависит от них.
- Добавляйте подтверждение проверки (логи backend, поведение дашборда, вывод firmware).
- Никогда не коммитьте секреты (`DATABASE_URL`, API токены, файлы с учётными данными).

## 📄 Лицензия

В снимке этого репозитория `LICENSE` на верхнем уровне не обнаружен. До появления явного файла лицензии использование и распространение требуют одобрения мейнтейнера.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
