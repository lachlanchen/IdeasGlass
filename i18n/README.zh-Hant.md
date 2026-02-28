[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*一款可穿戴 AI 眼鏡，能將想法轉化為行動、收益與創作動能。*

> 以語音為先的可穿戴 AI 流水線：來自 ESP32 眼鏡的擷取、後端處理，以及透過即時 PWA 儀表板進行監控與控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| 通道 | 用途 |
|---|---|
| 🎙️ 可穿戴擷取 | ESP32 眼鏡準即時傳送音訊、照片與遙測資料 |
| 🧠 後端智慧 | FastAPI 接收串流、轉譯、分段並持久化中繼資料 |
| 🖥️ 儀表板 | PWA 即時顯示波形、轉錄文字與設備/帳號狀態 |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>生態</b><br/>
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
  <sub>App UI（左） · 硬體（右）</sub>
</div>

在 <a href="https://onlyideas.art">onlyideas.art</a> 探索社群實驗。

## 🚀 概覽

IdeasGlass 是一個以 AI 為先的可穿戴系統，用於語音優先的靈感擷取與落地執行。在這個倉庫裡，主要運行路徑為：

- `backend/glass/`：FastAPI API、WebSocket 接收、基於 Whisper 的轉錄，以及可安裝的 PWA 儀表板。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：XIAO ESP32S3 固件，負責串流遙測/音訊/照片。

如果你是第一次接觸本倉庫，建議先從這裡開始。

### 一覽

| 區域 | 主要位置 | 職責 |
|---|---|---|
| 後端 API 與 PWA | `backend/glass/` | FastAPI 端點、WebSocket 接收/推播、轉錄、儀表板 |
| 韌體 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 擷取與串流用戶端 |
| 橋接說明 | `references/ideasglass_bridge.md` | TLS/WAN 穩定性說明及部署現場建議 |
| README 多語言版本 | `i18n/` | 由英文 README 版主版本同步維護的多語文件 |

## ✨ 為何選擇 IdeasGlass

IdeasGlass 是為想法不斷湧現的人而生的 AI 可穿戴設備。無論你是邊走邊口述構想，還是在直播中靈光乍現，它都能在同一瞬間捕捉、轉譯、整理並推進創作落地。

## 🧩 功能

### 產品願景功能

- **創作原生硬體**：輕量化眼鏡與可穿戴輸入，專為語音優先擷取設計，並支援微妙手勢捷徑。
- **即時翻譯**：即時語言偵測與翻譯，讓你在不同團隊或受眾間協作時無需切換工具。
- **EchoMind 副駕駛**：與 `chat.lazying.art` 深度配對，用於腦力激盪、腳本起草與多語內容指導。
- **頻道自動駕駛**：自動生成大綱、長篇腳本、短片開場鉤子，並將上傳排程到 YouTube 或其他渠道。
- **重點片段與短影片**：自動擷取高光時刻，生成縮圖、字幕與社群可用短片。
- **收益層**：連接 LazyingArt Coin，提供打賞、點數派發與鏈上資產轉換。
- **支出與專注**：追蹤營運花費，揭示高轉化格式，並將你的個人強項濃縮為下一個專案方向。

### 倉庫與運行特性

- FastAPI 後端提供 REST 與 WebSocket 端點，用於接入（`/api/v1/audio`、`/ws/audio-ingest`）與即時串流推播（`/ws/stream`）。
- 將音訊做決定性分段（預設約 15 秒，含重疊）並儲存到 `backend/glass/audio_segments/`。
- 可選的 openai-whisper 串流轉錄，具備可設定延遲門檻。
- 可選 PostgreSQL 持久化（`DATABASE_URL`）用於訊息、照片、音訊區塊、片段與轉錄紀錄。
- PWA 儀表板支援即時波形、轉錄更新，並可在桌面與行動端安裝。
- 支援 Seeed XIAO ESP32S3 Sense 相機與麥克風的 Arduino 固件。

## 🔄 範例流程

1. **擷取**：說出或速寫構想，IdeasGlass 會轉錄、翻譯並標記意圖。
2. **共同創作**：EchoMind 提煉想法、起草腳本，並針對各平台提供 CTA 建議。
3. **發布**：頻道代理自動產生精華影片、圖庫圖片並附帶中繼資料上傳。
4. **變現**：點數透過 LazyingArt Coin（`coin.lazying.art`）流轉，並與你偏好的錢包進行結算同步。
5. **回顧**：支出、觸及與互動儀表板顯示下一步加碼重點。

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

## 🧰 先決條件

- Python 3.10+
- `pip`（或具備相容 Python 的 conda 環境）
- 可選：NVIDIA GPU + CUDA/cuDNN，用於加速 Whisper 推理
- 可選：PostgreSQL，用於持久化儲存
- 韌體側：Arduino IDE 或 `arduino-cli`、Seeed XIAO ESP32S3 Sense、啟用 PSRAM

| 元件 | 要求 | 說明 |
|---|---|---|
| 後端執行環境 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可選） | NVIDIA + CUDA/cuDNN | 降低 Whisper 延遲 |
| 持久化（可選） | PostgreSQL | 透過 `DATABASE_URL` 啟用 |
| 韌體工具鏈 | Arduino IDE / `arduino-cli` | 使用啟用 PSRAM 的 XIAO ESP32S3 設定 |

## ⚙️ 安裝

### 後端依賴

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 韌體先決條件

- 將 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 複製為 `wifi_credentials.h`（建議）並填入 SSID 與密碼。
- 在 Arduino IDE 中選擇開發板 `ESP32 -> XIAO_ESP32S3`，並設定 `PSRAM: OPI PSRAM`。
- 分區方案：`Default with spiffs (3MB APP/1.5MB SPIFFS)`，或在不需要檔案系統時使用 `Maximum APP`。

## ▶️ 使用方法

### 啟動後端（uvicorn）

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### 啟動後端（輔助）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 開啟儀表板

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| 介面 | 用途 |
|---|---|
| `/` | 主儀表板（支援 PWA） |
| `/healthz` | 後端存活性檢查 |
| `/ws/audio-ingest` | 設備擷取 WebSocket |
| `/ws/stream` | 即時串流推播至儀表板客戶端 |

### 登入並綁定設備

1. 在儀表板的「設定/帳號」區域註冊或登入。
2. 在 `Bind device` 欄位綁定你的設備 ID。
3. 只有已綁定的設備會串流到你的帳號。

產生設備 ID 與 QR 圖片：

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

確認目前帳號與已綁定設備：

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

可選遷移（將歷史資料重新命名到新設備 ID）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 韌體編譯/上傳（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

若序列埠被佔用：`fuser -k /dev/ttyACM0`。
若出現權限不足：執行 `sudo usermod -aG dialout $USER` 後重新登入（或暫時執行 `sudo chmod a+rw /dev/ttyACM0`）。

### 韌體電源互動（XIAO ESP32S3）

- 開機時長按約 0.8 秒啟動。
- 運行中長按約 2.5 秒進入深度睡眠。
- 運行中短按仍可觸發擷取。

## 🛠️ 設定

### 核心環境變數

- `DATABASE_URL`：可選的 Postgres DSN，用於持久化存儲。
- `IDEASGLASS_WHISPER_MODEL`：`base`（預設）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU 安全模式。
- `IDEASGLASS_TRANSCRIBE`：`1`（預設）啟用轉錄，`0` 停用轉錄。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滾動轉錄間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：逗號分隔的閾值（預設 `3000,6000,15000`）。

| 變數 | 預設/選項 | 效果 |
|---|---|---|
| `DATABASE_URL` | 預設未設定 | 為帳號/設備資料啟用 Postgres 永久儲存 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（含 `small`、`medium`、`large-v3`、`large-v3-turbo`） | 控制精準度與延遲平衡 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` 或 `cpu` | 推論後端 |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU），`0`（CPU 安全） | 混合精度控制 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 切換轉錄流程 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 運行時設定 | 滾動轉錄推送間隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 漸進式轉錄輸出閾值 |

安全的 `DATABASE_URL` 範例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（本機/peer 認證）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（密碼認證）

### 音訊增益與分段參數

- `IDEASGLASS_GAIN_TARGET`（預設 `0.032`）
- `IDEASGLASS_GAIN_MAX`（預設 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（預設 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（預設 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（預設 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（預設 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（預設 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（預設繼承區塊增益目標）

| 音訊參數 | 預設值 | 用途 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 目標 RMS 正規化 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 增益放大上限 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 避免放大近乎靜音區段 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 語音活動 RMS 基準 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 語音閾值邊界緩衝 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 分段目標長度 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 透過重疊保留連續性 |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | 繼承區塊增益 | 分段層級正規化目標 |

### 模型預先載入（可選）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 範例

### 產生並綁定設備 ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

接著在以下檔案設定 `kDeviceId`：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

儀表板流程：

1. 在「設定」中註冊/登入。
2. 在「帳號」面板綁定設備。
3. 只有已綁定的設備才會向你的帳號推送串流。

### REST 接口範例

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

## 🧭 開發說明

### 重點方向

此倉庫包含多條後端路徑。除非另有要求，當前貢獻者指引與主要運行重點為 `backend/glass/`。

### 靜態/語法檢查

```bash
python -m compileall backend/glass/app.py
```

### 開發文件

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 註：在目前的倉庫快照中，上述部分歷史連結可能已移動（例如橋接說明目前位於 `references/ideasglass_bridge.md`）。原始連結仍保留為英文 README 的標準內容。

### 快速設備綁定（保留流程）

- 產生 ID（在 conda `glass`）：`python backend/glass/tools/generate_device_id.py`
- 在韌體中設定：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 啟動後端並開啟 `http://localhost:8765`，註冊/登入後在帳號面板綁定設備 ID

## 🆘 疑難排解

- **埠已被佔用：** 將後端改在其他埠執行，並更新客戶端設定。
- **序列埠忙碌：** `fuser -k /dev/ttyACM0`。
- **Linux 序列埠權限不足：** `sudo usermod -aG dialout $USER` 後重新登入。
- **Postgres 不可用：** 後端可在無資料庫情況下部分運作；請檢查 `DATABASE_URL` 並重啟。
- **Whisper 效能問題：** 使用較小的模型（`base`/`small`）或透過 `IDEASGLASS_TRANSCRIBE=0` 停用轉錄。
- **ESP32 TLS/時間同步不穩定：** 檢查 Wi-Fi、NTP 可用性（UDP/123）及憑證/主機設定；參閱 `references/ideasglass_bridge.md` 的現場說明。
- **即時波形無更新：** 檢查後端日誌與瀏覽器主控台中的 `[IdeasGlass][wave]` 追蹤，並確認 `/ws/stream` 連線是否正常。

## 🌐 生態鏈接

🧠 **EchoMind** — 多語學習與創作輔助 AI 助手。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 研究到產品轉化的勇敢創意社群。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 將小成果自動轉化為收入的自動化流程。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理與化學課程與筆記本。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 將靈感轉為草稿、任務與貼文的助理。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 擷取、翻譯並自動生成精華短片。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 將貢獻與鏈上價值連接的獎勵與結算體系。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究筆記與文章彙刊。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — 承載 OnlyIdeas、EchoMind、LazyEdit 與 IdeasGlass 的工作室。  
[lazying.art](https://lazying.art)

## 🙏 感謝

我們立足於眾多優秀的開源專案，特別感謝：

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **推薦方案**：使用優惠碼 `LazyingArt` 可節省 10%（累積販售 10 件後解鎖 30% 回饋）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 路線圖

- 加強並記錄跨 WAN/TLS 環境下的端到端音訊串流路徑。
- 持續改善轉錄品質與延遲權衡（模型/設備/閾值預設）。
- 擴充設備管理與帳號級多設備協作工作流程。
- 對齊或整合遺留/平行後端路徑（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）至主路徑 `backend/glass`。
- 在 `i18n/` 下維護並更新多語 README 版本。

## 🤝 貢獻

歡迎參與貢獻。關於倉庫層級流程，請遵循 `AGENTS.md`。

建議在提交 PR 前做本機驗證：

```bash
python -m compileall backend/glass/app.py
```

提交變更時：

- 保持提交標題簡潔且以動作為導向（使用現在式）。
- 當行為受相關環境變數影響時，在 PR 說明中註明（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）。
- 提供測試證據（後端日誌、儀表板行為、韌體輸出）。
- 切勿提交機密資訊（例如 `DATABASE_URL`、API token、憑證檔）。

## 📄 授權

此倉庫快照中尚未偵測到頂層 `LICENSE` 檔案。在正式加入明確授權檔前，請將使用與再散布行為視為需取得維護者授權。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
