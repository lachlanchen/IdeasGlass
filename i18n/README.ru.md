[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*Носимые AI-очки, которые превращают идеи в действия, доход и творческий импульс.*

> Носимый AI-пайплайн с голосовым управлением: захват с очков ESP32, обработка в FastAPI и мониторинг/управление через живую PWA-панель.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

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
  <sub>Интерфейс приложения (слева) · Аппаратная часть (справа)</sub>
</div>

Изучайте эксперименты сообщества на <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Обзор

IdeasGlass — носимая AI-система с упором на голосовой захват идей и их реализацию. В этом репозитории основной runtime-путь следующий:

- `backend/glass/` для API FastAPI, WebSocket-ingest, транскрибации на базе Whisper и устанавливаемой PWA-панели.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` для прошивки XIAO ESP32S3, которая стримит телеметрию/аудио/фото.

Если вы впервые в этом репозитории, начните с этих каталогов.

### Кратко

| Область | Основное расположение | Назначение |
|---|---|---|
| Backend API + PWA | `backend/glass/` | Эндпоинты FastAPI, WebSocket ingest/fanout, транскрибация, панель |
| Прошивка | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Клиент захвата/стриминга на ESP32 |
| Заметки по bridge | `references/ideasglass_bridge.md` | Примечания по надежности TLS/WAN и советы по деплою |
| Переводы README | `i18n/` | Мультиязычная документация, синхронизированная с каноническим README |

## ✨ Почему IdeasGlass

IdeasGlass — AI-first носимое устройство для людей, живущих в потоке идей. Оно фиксирует, переводит, структурирует и помогает реализовывать креатив в момент вдохновения — когда вы озвучиваете концепт на ходу или ведете живую сессию.

## 🧩 Возможности

### Возможности на уровне продуктового видения

- **Аппаратная часть, заточенная под создание** – легкие очки и носимые элементы управления, настроенные на voice-first захват и ненавязчивые жесты.
- **Мгновенный перевод** – детекция языка и перевод в реальном времени, чтобы работать с командами и аудиторией без переключения инструментов.
- **Ко-пилот EchoMind** – плотная интеграция с `chat.lazying.art` для брейнсторминга, черновиков сценариев и мультиязычного контент-коучинга.
- **Автопилот каналов** – генерирует планы, длинные сценарии, короткие хук-фрагменты и планирует публикации на YouTube и других платформах.
- **Хайлайты и рилсы** – автоматически выбирает ключевые моменты, создает миниатюры, субтитры и клипы для соцсетей.
- **Слой монетизации** – интеграция с LazyingArt Coin для чаевых, кредитных выплат и конвертации в on-chain активы.
- **Расходы и фокус** – отслеживает операционные затраты, выявляет прибыльные форматы и собирает ваши сильные стороны в следующие проекты.

### Возможности на уровне репозитория/runtime

- FastAPI backend с REST + WebSocket эндпоинтами для ingest (`/api/v1/audio`, `/ws/audio-ingest`) и fanout живого потока (`/ws/stream`).
- Детерминированная сегментация аудио (по умолчанию ~15 с с overlap) в `backend/glass/audio_segments/`.
- Опциональные потоковые транскрипты openai-whisper с настраиваемыми порогами задержки.
- Опциональное сохранение в Postgres (`DATABASE_URL`) для сообщений, фото, chunks, segments, transcripts.
- PWA-панель с живой волной, обновлениями транскрипта и поддержкой установки на desktop/mobile.
- Поддержка Arduino-прошивки для сценариев камеры + микрофона XIAO ESP32S3 Sense.

## 🔄 Пример рабочего процесса

1. **Захват** – произнесите или набросайте идею; IdeasGlass транскрибирует, переводит и помечает намерение.
2. **Со-творчество** – EchoMind дорабатывает идею, пишет черновики сценариев и предлагает CTA под каждую платформу.
3. **Публикация** – агент канала автоматически делает хайлайт-видео, изображения для галереи и загружает их с метаданными.
4. **Монетизация** – кредиты проходят через LazyingArt Coin (`coin.lazying.art`), а выплаты синхронизируются с вашими кошельками.
5. **Рефлексия** – панели с расходами, охватом и вовлеченностью показывают, что стоит масштабировать дальше.

## 🗂️ Структура проекта

```text
IdeasGlass/
├── README.md
├── i18n/                                  # Переводы README
├── backend/
│   ├── glass/                             # Основной backend FastAPI + PWA
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # Вторичный/параллельный путь ingest backend
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Примечания по bridge + деплою
├── docs/                                  # Дополнительные материалы сайта/документации
├── development_plan/
├── app/
├── ops/observability/
├── figs/
└── seeed_studio_xiao_esp32s3_dev/
```

## 🧰 Предварительные требования

- Python 3.10+
- `pip` (или conda-окружение с совместимым Python)
- Опционально: NVIDIA GPU + CUDA/cuDNN для более быстрого инференса Whisper
- Опционально: PostgreSQL для персистентности
- Для прошивки: Arduino IDE или `arduino-cli`, Seeed XIAO ESP32S3 Sense, включенный PSRAM

| Компонент | Требование | Примечания |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | Используйте venv или conda (`glass`) |
| GPU-ускорение (опционально) | NVIDIA + CUDA/cuDNN | Улучшает задержку Whisper |
| Персистентность (опционально) | PostgreSQL | Включается через `DATABASE_URL` |
| Toolchain прошивки | Arduino IDE / `arduino-cli` | Используйте профиль XIAO ESP32S3 с PSRAM |

## ⚙️ Установка

### Зависимости backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Требования для прошивки

- Скопируйте `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` в `wifi_credentials.h` (рекомендуется) и задайте SSID/пароль.
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

### Открыть панель

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Назначение |
|---|---|
| `/` | Основная панель (PWA-совместимый UI) |
| `/healthz` | Проверка доступности backend |
| `/ws/audio-ingest` | WebSocket ingest устройства |
| `/ws/stream` | Fanout живого потока к клиентам панели |

### Вход и привязка устройства

1. Зарегистрируйтесь или войдите через раздел Settings/Account в панели.
2. Привяжите ID вашего устройства в поле `Bind device`.
3. Только привязанные устройства будут стримить в ваш аккаунт.

Сгенерировать ID устройства + QR-изображение:

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

Проверка текущего аккаунта и привязанных устройств:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Опциональная миграция (переименовать исторические данные на новый ID устройства):

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
Если отказано в доступе: `sudo usermod -aG dialout $USER`, затем перелогиньтесь (или временно `sudo chmod a+rw /dev/ttyACM0`).

### UX по питанию прошивки (XIAO ESP32S3)

- Удерживайте кнопку ~0.8 с при включении питания для загрузки.
- Удерживайте ~2.5 с во время работы, чтобы перейти в deep sleep.
- Короткое нажатие во время работы по-прежнему запускает захват.

## 🛠️ Конфигурация

### Основные переменные окружения

- `DATABASE_URL`: опциональный Postgres DSN для постоянного хранения.
- `IDEASGLASS_WHISPER_MODEL`: `base` (по умолчанию), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` или `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` для mixed precision на GPU, `0` для CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (по умолчанию) включает транскрибацию, `0` выключает.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: интервал скользящего транскрипта.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: пороги через запятую (по умолчанию `3000,6000,15000`).

| Переменная | Значение по умолчанию / опции | Эффект |
|---|---|---|
| `DATABASE_URL` | по умолчанию не задана | Включает персистентность Postgres для данных аккаунта/устройства |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Баланс точности и задержки |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` или `cpu` | Backend инференса |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` безопасно для CPU | Управление mixed precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Переключатель пайплайна транскрибации |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | настраивается во время работы | Интервал отправки скользящего транскрипта |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Пороговые значения прогрессивной выдачи транскрипта |

Безопасные примеры `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (peer/local auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (password auth)

### Параметры усиления и сегментации аудио

- `IDEASGLASS_GAIN_TARGET` (по умолчанию `0.032`)
- `IDEASGLASS_GAIN_MAX` (по умолчанию `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (по умолчанию `0.008`)
- `IDEASGLASS_SPEECH_RMS` (по умолчанию `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (по умолчанию `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (по умолчанию `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (по умолчанию `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (по умолчанию наследуется от chunk gain target)

| Параметр аудио | По умолчанию | Назначение |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Целевой RMS для нормализации |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Верхнее ограничение усиления |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Нижний порог, чтобы не усиливать почти тишину |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Базовый RMS-порог речевой активности |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Запас вокруг порога речи |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Целевая длина сегмента |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Перекрытие сегментов для непрерывности |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | наследуется от chunk gain | Цель нормализации на уровне сегмента |

### Предзагрузка моделей (опционально)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Примеры

### Генерация и привязка ID устройства

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Затем задайте `kDeviceId` в:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Поток в панели:

1. Зарегистрируйтесь/войдите в Settings.
2. Привяжите устройство в панели Account.
3. Только привязанные устройства стримят в ваш аккаунт.

### Примеры REST ingest

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

## 🧭 Примечания для разработки

### Область фокуса

В этом репозитории есть несколько backend-направлений. Текущая рекомендация для контрибьюторов и основной runtime-фокус — `backend/glass/`, если не указано иное.

### Статическая/синтаксическая проверка

```bash
python -m compileall backend/glass/app.py
```

### Документация для разработчиков

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Примечание: в текущем snapshot репозитория некоторые исторические ссылки выше, по-видимому, были перемещены (например, заметки по bridge теперь находятся в `references/ideasglass_bridge.md`). Оригинальные ссылки сохранены как каноническое содержимое README.

### Быстрая привязка устройства (сохраненный workflow)

- Сгенерируйте ID (в conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Установите его в прошивке: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Запустите backend и откройте `http://localhost:8765`, зарегистрируйтесь/войдите, затем привяжите ID устройства в панели Account

## 🆘 Устранение неполадок

- **Порт уже занят:** запустите backend на другом порту и обновите настройки клиента.
- **Serial-порт занят:** `fuser -k /dev/ttyACM0`.
- **На Linux отказ в доступе к serial:** `sudo usermod -aG dialout $USER` и перелогиньтесь.
- **Postgres недоступен:** backend может работать без БД с частичной функциональностью; проверьте `DATABASE_URL` и перезапустите.
- **Проблемы с производительностью Whisper:** используйте меньшие модели (`base`/`small`) или выключите транскрибацию через `IDEASGLASS_TRANSCRIBE=0`.
- **Нестабильность TLS/синхронизации времени на ESP32:** проверьте Wi-Fi, доступность NTP (UDP/123) и настройки cert/host; подробности в `references/ideasglass_bridge.md`.
- **Нет обновлений живой waveform:** проверьте логи backend и консоль браузера на наличие трасс `[IdeasGlass][wave]` и убедитесь в подключении к `/ws/stream`.

## 🌐 Ссылки экосистемы

🧠 **EchoMind** — Мультиязычный AI-компаньон для обучения и творчества.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Сообщество "от исследования к продукту" для смелых концепций.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Автоматизации, превращающие небольшие победы в доход.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Треки и тетради по физике и химии.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Агент, превращающий идеи в черновики, задачи и посты.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Захват, перевод и автопроизводство хайлайт-роликов.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Награды и выплаты, связывающие вклад и on-chain ценность.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Блокнот исследовательских заметок и эссе.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Студия, стоящая за OnlyIdeas, EchoMind, LazyEdit и IdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ Поддержка и контакты

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- Ваша поддержка помогает развивать носимое устройство, агентный слой и экосистемную дорожную карту.

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

- По вопросам партнерства пишите на **contact@lazying.art** с темой `IdeasGlass`.

IdeasGlass — это точка, где носимые AI-устройства перестают просто слушать и начинают создавать вместе с вами.

## 🙏 Благодарности

Мы опираемся на выдающиеся open-source проекты — спасибо:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — Используйте купон `LazyingArt`, чтобы получить скидку 10% (30% комиссии открываются после 10 продаж).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Дорожная карта

- Укрепить и задокументировать сквозной путь потокового аудио в средах WAN/TLS.
- Продолжать улучшать компромисс качество/задержка транскрипта (пресеты model/device/threshold).
- Расширить управление устройствами и account-scoped multi-device workflow в панели.
- Выравнивать или консолидировать legacy/parallel backend-направления (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) с основным путем `backend/glass`.
- Поддерживать и обновлять мультиязычные варианты README в `i18n/`.

## 🤝 Вклад

Мы приветствуем вклад. Для репозиторий-специфичного workflow следуйте `AGENTS.md`.

Рекомендуемая локальная проверка перед открытием PR:

```bash
python -m compileall backend/glass/app.py
```

При отправке изменений:

- Держите темы коммитов короткими и ориентированными на действие (в настоящем времени).
- Указывайте релевантные env vars (например, `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) в заметках PR, если поведение от них зависит.
- Добавляйте подтверждения тестирования (логи backend, поведение панели, вывод прошивки).
- Никогда не коммитьте секреты (`DATABASE_URL`, API-токены, файлы credentials).

## 📄 Лицензия

В текущем snapshot репозитория не обнаружен файл `LICENSE` верхнего уровня. Пока явный файл лицензии не добавлен, считайте, что использование и распространение требуют одобрения мейнтейнера.
