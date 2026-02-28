[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*一款可穿戴式 AI 眼鏡，能將想法轉化為行動、收入與創作動能。*

> 以語音為先的可穿戴 AI 流程：由 ESP32 眼鏡擷取、後端處理，並透過即時 PWA 儀表板進行監控與控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| 通道 | 用途 |
|---|---|
| 🎙️ 可穿戴擷取 | ESP32 眼鏡以接近即時方式傳送音訊、照片與遙測資料 |
| 🧠 後端智慧 | FastAPI 接收串流、轉錄、分段並保存中繼資料 |
| 🖥️ 儀表板 | PWA 即時顯示波形、逐字稿與設備/帳號狀態 |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass 應用介面" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass 硬體" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>應用介面（左） · 硬體（右）</sub>
</div>

到 <a href="https://onlyideas.art">onlyideas.art</a> 探索社群實驗。

## 🚀 概覽

IdeasGlass 是一個以 AI 為先的可穿戴系統，適合以語音為主的想法擷取與執行。在這個儲存庫中，主要運行路徑為：

- `backend/glass/`：提供 FastAPI API、WebSocket 接收、基於 Whisper 的轉錄，以及可安裝的 PWA 儀表板。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：XIAO ESP32S3 韌體，負責傳輸遙測、音訊與照片。

若你是第一次使用本儲存庫，請先從這裡開始。

## 📚 目錄

- [🚀 概覽](#-概覽)
- [✨ 為何選擇 IdeasGlass](#-為何選擇-ideasglass)
- [🧩 功能](#-功能)
- [🔄 範例工作流程](#-範例工作流程)
- [🗂️ 專案結構](#️-專案結構)
- [🧰 先決條件](#-先決條件)
- [⚙️ 安裝](#️-安裝)
- [▶️ 使用方式](#️-使用方式)
- [🛠️ 設定](#️-設定)
- [🧪 範例](#-範例)
- [🧭 開發說明](#-開發說明)
- [🆘 疑難排解](#️-疑難排解)
- [🌐 生態系連結](#-生態系連結)
- [🙏 感謝](#-感謝)
- [🛣️ 路線圖](#️-路線圖)
- [🤝 貢獻](#-貢獻)
- [❤️ Support](#-support)
- [📄 授權](#-授權)

### 一眼看全

| 區域 | 主要位置 | 功能 |
|---|---|---|
| 後端 API + PWA | `backend/glass/` | FastAPI 端點、WebSocket 接收/廣播、逐字稿與儀表板 |
| 韌體 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 擷取/串流用戶端 |
| 橋接說明 | `references/ideasglass_bridge.md` | TLS/WAN 穩定性說明與部署現場建議 |
| README 多語版本 | `i18n/` | 從主 README 同步維護的多語文件 |

## ✨ 為何選擇 IdeasGlass

IdeasGlass 是為了在想法連續湧現的情境打造的 AI 可穿戴裝置。無論你是在移動中口述一個概念，或正在主持直播，它都能在靈感出現的瞬間擷取、翻譯、整理，並推動創意落地。

## 🧩 功能

### 產品願景功能

- **創作原生硬體**：輕量眼鏡與可穿戴輸入，針對語音優先擷取最佳化，並支援微妙手勢快速操作。
- **即時翻譯**：即時語言偵測與翻譯，讓你在不同團隊或受眾間共同構思時，不必切換工具。
- **EchoMind 副駕駛**：與 `chat.lazying.art` 深度整合，用於腦力激盪、腳本草擬與多語內容指引。
- **頻道自動駕駛**：自動產生大綱、長篇腳本、短版開場鉤子，並安排上傳到 YouTube 或其他頻道。
- **重點片段與短片**：自動挑選精華時刻，產生縮圖、字幕與可直接發佈的社群短片。
- **收益層**：接上 LazyingArt Coin，支援小費、點數支付與轉換為鏈上資產。
- **支出與專注**：追蹤營運成本，突顯最能帶來回報的內容型態，並將你的個人優勢萃取成下一步計畫。

### 倉庫 / 執行功能

- FastAPI 後端提供 REST 與 WebSocket 端點：資料接入（`/api/v1/audio`、`/ws/audio-ingest`）與即時串流推播（`/ws/stream`）。
- 將音訊進行確定性切段（預設約 15 秒，含重疊），儲存於 `backend/glass/audio_segments/`。
- 可選的 openai-whisper 串流逐字稿，支援可設定的延遲門檻。
- 可選 Postgres 持久化（`DATABASE_URL`）儲存訊息、照片、音訊區塊、片段與逐字稿。
- PWA 儀表板提供即時波形、逐字稿更新，並可在桌機與行動裝置上安裝。
- 提供 XIAO ESP32S3 Sense 相機與麥克風的 Arduino 韌體支援。

## 🔄 範例工作流程

1. **擷取**：說出或速寫一個想法；IdeasGlass 會幫你轉錄、翻譯，並標註意圖。
2. **共同創作**：EchoMind 精煉想法、草擬腳本，並依每個平台建議 CTA。
3. **發布**：頻道代理會自動產出精華影片、圖庫圖片，並附上中繼資料上傳。
4. **變現**：點數透過 LazyingArt Coin（`coin.lazying.art`）流轉，並與你偏好的錢包同步撥款。
5. **回顧**：支出、觸及與互動儀表板顯示下一步要加碼的方向。

## 🗂️ 專案結構

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

## 🧰 先決條件

- Python 3.10+
- `pip`（或可使用相容 Python 的 conda 環境）
- 可選：NVIDIA GPU + CUDA/cuDNN，可加快 Whisper 推論
- 可選：PostgreSQL 用於資料持久化
- 韌體端：Arduino IDE 或 `arduino-cli`、Seeed XIAO ESP32S3 Sense、啟用 PSRAM

| 元件 | 需求 | 備註 |
|---|---|---|
| 後端執行環境 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可選） | NVIDIA + CUDA/cuDNN | 降低 Whisper 延遲 |
| 持久化（可選） | PostgreSQL | 透過 `DATABASE_URL` 啟用 |
| 韌體工具鏈 | Arduino IDE / `arduino-cli` | 使用啟用 PSRAM 的 XIAO ESP32S3 設定 |

## ⚙️ 安裝

### 後端相依套件

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 韌體前置條件

- 建議將 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 複製成 `wifi_credentials.h`，並設定 SSID 與密碼。
- 在 Arduino IDE 中選擇開發板 `ESP32 -> XIAO_ESP32S3`，並將 `PSRAM: OPI PSRAM` 設為啟用。
- 分割區設定：`Default with spiffs (3MB APP/1.5MB SPIFFS)`，若不需要檔案系統可改用 `Maximum APP`。

## ▶️ 使用方式

### 開啟後端（uvicorn）

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### 開啟後端（輔助）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 開啟儀表板

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| 端點 | 用途 |
|---|---|
| `/` | 主儀表板（PWA 相容介面） |
| `/healthz` | 後端健康檢查 |
| `/ws/audio-ingest` | 裝置接入 WebSocket |
| `/ws/stream` | 即時串流推播到儀表板用戶端 |

### 登入並綁定你的裝置

1. 在儀表板「設定 / 帳號」區域註冊或登入。
2. 在 `Bind device` 欄位綁定你的裝置 ID。
3. 只有已綁定的裝置才會串流到你的帳號。

產生裝置 ID 與 QR 圖片：

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

透過 API 綁定（需要 cookie 工作階段）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

檢查目前帳號與已綁定裝置：

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

選用資料遷移（將歷史資料重命名為新裝置 ID）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 韌體編譯與上傳（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

若通訊埠被占用：`fuser -k /dev/ttyACM0`。
若出現權限不足：先執行 `sudo usermod -aG dialout $USER` 後重新登入（或暫時執行 `sudo chmod a+rw /dev/ttyACM0`）。

### 韌體電源操作（XIAO ESP32S3）

- 開機時長按約 0.8 秒可開機。
- 運行中長按約 2.5 秒進入深度睡眠。
- 運行中短按仍可觸發擷取。

## 🛠️ 設定

### 核心環境變數

- `DATABASE_URL`：可選的 Postgres DSN，用於持久化存放。
- `IDEASGLASS_WHISPER_MODEL`：`base`（預設）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU。
- `IDEASGLASS_TRANSCRIBE`：`1`（預設）啟用轉錄，`0` 停用轉錄。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滾動式逐字稿間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：以逗號分隔的門檻值（預設 `3000,6000,15000`）。

| 變數 | 預設 / 選項 | 效果 |
|---|---|---|
| `DATABASE_URL` | 預設未設定 | 啟用 Postgres 持久化帳號/裝置資料 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（`small`、`medium`、`large-v3`、`large-v3-turbo`） | 控制精準度與延遲平衡 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` 或 `cpu` | 推論後端 |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU）、`0`（CPU 安全模式） | 混合精度控制 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 開關轉錄流程 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 運行時設定 | 逐字稿滾動推送間隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 逐步推送逐字稿門檻值 |

安全的 `DATABASE_URL` 範例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local 驗證）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（密碼驗證）

### 音訊增益與切段參數

- `IDEASGLASS_GAIN_TARGET`（預設 `0.032`）
- `IDEASGLASS_GAIN_MAX`（預設 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（預設 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（預設 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（預設 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（預設 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（預設 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（預設沿用區塊增益目標）

| 音訊參數 | 預設值 | 用途 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 目標 RMS 正規化 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 增益放大上限 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 避免放大近乎無聲的片段 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 語音活動 RMS 基準 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 語音門檻緩衝區 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 切段目標長度 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 用於連續性的重疊長度 |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | 沿用區塊增益目標 | 切段層級正規化目標 |

### 模型預載（可選）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 範例

### 產生並綁定裝置 ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

接著在下方檔案設定 `kDeviceId`：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

儀表板流程：

1. 在設定中註冊/登入。
2. 在帳號面板綁定裝置。
3. 僅已綁定的裝置才會向你的帳號推送串流。

### REST 接收範例

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
    "photo_base64":"'"$(base64 -w0 sample.jpg)'",
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
    "audio_base64":"'"$(base64 -w0 temp.raw)'"
  }'
```

```bash
curl http://localhost:8765/api/v1/audio/segments | jq '.[0]'
curl -o latest.wav http://localhost:8765/api/v1/audio/segments/<segment-id>
```

## 🧭 開發說明

### 工作重點

本儲存庫包含多條後端路徑，除非另有要求，目前建議的貢獻與執行重點為 `backend/glass/`。

### 靜態/語法檢查

```bash
python -m compileall backend/glass/app.py
```

### 開發文件

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 注意：在目前儲存庫快照中，上述歷史連結有些可能已搬移（例如，橋接說明目前位於 `references/ideasglass_bridge.md`）。原始連結保留作為英文 README 的標準內容。

### 快速裝置綁定（保留流程）

- 產生 ID（在 conda `glass`）：`python backend/glass/tools/generate_device_id.py`
- 在韌體中設定：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 開啟後端，訪問 `http://localhost:8765`，註冊/登入後在「帳號」面板綁定裝置 ID

## 🆘 疑難排解

- **通訊埠已被佔用：** 請改在其他埠啟動後端並更新用戶端設定。
- **序列埠忙碌：** `fuser -k /dev/ttyACM0`。
- **Linux 序列埠權限不足：** `sudo usermod -aG dialout $USER`，重新登入即可。
- **Postgres 無法使用：** 後端可在無資料庫情況下保持部分功能，請確認 `DATABASE_URL` 後重啟。
- **Whisper 效能問題：** 改用較小模型（`base` / `small`）或以 `IDEASGLASS_TRANSCRIBE=0` 停用轉錄。
- **ESP32 TLS/時間同步不穩：** 檢查 Wi-Fi、NTP 可用性（UDP/123）與憑證/主機設定，詳見 `references/ideasglass_bridge.md` 現場備註。
- **即時波形無更新：** 檢查後端日誌與瀏覽器主控台中的 `[IdeasGlass][wave]` 追蹤，並確認 `/ws/stream` 連線。

## 🌐 生態系連結

| 品牌 | 用途 | 連結 |
|---|---|---|
| 🧠 EchoMind | 多語言學習與創作夥伴式 AI 助理 | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | 研究到產品化的社群，聚焦大膽創意 | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | 將小勝利自動轉成收入的自動化流程 | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | 物理與化學教材與筆記本 | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | 將想法轉成草稿、任務與貼文的代理 | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | 擷取、翻譯並自動製作精華短片 | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | 連結貢獻與鏈上價值的獎勵與撥款系統 | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | 研究筆記與文章庫 | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | 支撐 OnlyIdeas、EchoMind、LazyEdit 與 IdeasGlass 的工作室 | [lazying.art](https://lazying.art) |

## 🙏 感謝

本專案建立在優秀的開源專案基礎上，特別感謝：

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **推薦方案**：使用優惠碼 `LazyingArt` 可省 10%（完成 10 筆銷售後解鎖 30% 回饋）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 路線圖

- 強化並記錄跨 WAN/TLS 場景中的端到端音訊串流路徑。
- 持續改善轉錄品質與延遲平衡（模型/裝置/門檻預設值）。
- 擴充儀表板的裝置管理與帳戶範圍多裝置工作流程。
- 將既有的平行/遺留後端路徑（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）與主線 `backend/glass` 對齊或整合。
- 在 `i18n/` 中維持並更新多語 README 版本。

## 🤝 貢獻

歡迎任何貢獻。關於本儲存庫的工作流程，請依照 `AGENTS.md`。

建議提交 PR 前先做本機驗證：

```bash
python -m compileall backend/glass/app.py
```

提交變更時：

- 保持提交主題簡短、行動導向（現在式）。
- 當行為受環境變數影響時（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`），請在 PR 說明中註明。
- 提供測試證據（後端日誌、儀表板行為、韌體輸出）。
- 不要提交機密資訊（如 `DATABASE_URL`、API 權杖、憑證檔）。

## 📄 授權

此儲存庫快照尚未偵測到頂層 `LICENSE` 檔案。在正式加入明確授權檔之前，請將使用與再分發視為需先取得維護者核准。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
