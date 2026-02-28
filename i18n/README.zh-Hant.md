[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*一款可穿戴 AI 眼鏡，將想法轉化為行動、收入與創作動能。*

> 以語音為先的可穿戴 AI 管線：從 ESP32 眼鏡採集，在 FastAPI 中處理，並透過即時 PWA 儀表盤監控與控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>生態系</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>支持 IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>App UI（左）· 硬體（右）</sub>
</div>

在 <a href="https://onlyideas.art">onlyideas.art</a> 探索社群實驗。

## 🚀 概覽

IdeasGlass 是一個以 AI 為核心、以語音互動為優先的可穿戴系統，用於捕捉並執行想法。在本倉庫中，主要執行路徑是：

- `backend/glass/`：提供 FastAPI API、WebSocket 接入、基於 Whisper 的轉錄，以及可安裝的 PWA 儀表盤。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：用於 XIAO ESP32S3 韌體，負責流式傳輸遙測/音訊/照片。

如果你是第一次接觸此倉庫，請先從這兩處開始。

### 快速一覽

| 區域 | 主要位置 | 作用 |
|---|---|---|
| 後端 API + PWA | `backend/glass/` | FastAPI 端點、WebSocket 接入/分發、轉錄、儀表盤 |
| 韌體 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 採集/流式客戶端 |
| 網橋說明 | `references/ideasglass_bridge.md` | TLS/WAN 穩定性說明與部署實戰建議 |
| README 翻譯 | `i18n/` | 與規範英文 README 同步的多語言文件 |

## ✨ 為什麼是 IdeasGlass

IdeasGlass 是一款面向“持續湧現創意人群”的 AI 可穿戴設備。無論你是在移動中口述概念，還是正在進行直播，它都能在靈感出現的瞬間完成捕捉、翻譯、整理並推動執行。

## 🧩 功能

### 產品願景功能

- **創作原生硬體**：輕量眼鏡與可穿戴輸入，圍繞語音優先捕捉與細微手勢快捷操作設計。
- **即時翻譯**：即時語言檢測/翻譯，讓你在跨團隊或跨受衆創作時無需切換工具。
- **EchoMind 副駕**：與 `chat.lazying.art` 深度聯動，用於頭腦風暴、腳本草擬與多語言內容輔導。
- **頻道自動駕駛**：自動生成大綱、長影片腳本、短內容鉤點，並安排發佈到 YouTube 或其他渠道。
- **高光與短片**：自動挑選精彩片段，生成縮略圖、字幕與可直接發佈到社交平台的短影片。
- **收入層**：連接 LazyingArt Coin，實現打賞、積分結算與鏈上資產轉換。
- **支出與專注**：跟蹤運營支出，識別高收益內容形式，並提煉你的個人優勢用於下一輪項目。

### 倉庫/執行時功能

- FastAPI 後端，提供 REST + WebSocket 端點用於接入（`/api/v1/audio`, `/ws/audio-ingest`）與即時流分發（`/ws/stream`）。
- 具可預期行為的音訊分段（預設約 15 秒，帶重疊）並寫入 `backend/glass/audio_segments/`。
- 可選 openai-whisper 流式轉錄，支持可配置的延遲閾值。
- 可選 Postgres 持久化（`DATABASE_URL`），覆蓋消息、照片、音訊塊、分段、轉錄資料。
- PWA 儀表盤支持即時波形、轉錄更新，並可在桌面/移動端安裝。
- 支持 XIAO ESP32S3 Sense 攝像頭 + 麥克風流程的 Arduino 韌體。

## 🔄 範例工作流程

1. **捕捉**：口述或勾勒一個概念；IdeasGlass 會轉錄、翻譯並標註意圖。
2. **共創**：EchoMind 打磨想法，生成腳本，並給出面向不同平台的 CTA 建議。
3. **發佈**：頻道代理自動產出高光影片、圖集素材，並附帶元資料上傳。
4. **變現**：積分透過 LazyingArt Coin（`coin.lazying.art`）流轉，收益同步到你偏好的錢包。
5. **覆盤**：支出、觸達與互動儀表盤幫助你識別下一步該重點加碼的方向。

## 🗂️ 項目結構

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

## 🧰 前置條件

- Python 3.10+
- `pip`（或帶兼容 Python 的 conda 環境）
- 可選：NVIDIA GPU + CUDA/cuDNN（用於更快的 Whisper 推理）
- 可選：PostgreSQL（用於持久化）
- 韌體側：Arduino IDE 或 `arduino-cli`、Seeed XIAO ESP32S3 Sense，且啓用 PSRAM

| 組件 | 要求 | 說明 |
|---|---|---|
| 後端執行時 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可選） | NVIDIA + CUDA/cuDNN | 提升 Whisper 延遲表現 |
| 持久化（可選） | PostgreSQL | 透過 `DATABASE_URL` 啓用 |
| 韌體工具鏈 | Arduino IDE / `arduino-cli` | 使用 XIAO ESP32S3 配置並啓用 PSRAM |

## ⚙️ 安裝

### 後端依賴

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 韌體前置準備

- 將 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 複製為 `wifi_credentials.h`（推薦），並填寫 SSID/密碼。
- 在 Arduino IDE 中選擇開發板 `ESP32 -> XIAO_ESP32S3`，並設置 `PSRAM: OPI PSRAM`。
- 分區方案：`Default with spiffs (3MB APP/1.5MB SPIFFS)`；若不需要檔案系統可使用 `Maximum APP`。

## ▶️ 使用

### 執行後端（uvicorn）

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### 執行後端（輔助腳本）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 打開儀表盤

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | 用途 |
|---|---|
| `/` | 主儀表盤（支持 PWA 安裝） |
| `/healthz` | 後端存活檢查 |
| `/ws/audio-ingest` | 設備接入 WebSocket |
| `/ws/stream` | 面向儀表盤客戶端的即時流分發 |

### 登錄並綁定設備

1. 在儀表盤的 Settings/Account 區域註冊或登錄。
2. 在 `Bind device` 欄位中綁定你的設備 ID。
3. 只有已綁定設備會向你的帳號推流。

生成設備 ID + 二維碼圖像：

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

透過 API 綁定（需要 cookie 會話）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

驗證當前帳號與已綁定設備：

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

可選遷移（將歷史資料重命名到新設備 ID）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 韌體建構/上傳（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

若連接埠被佔用：`fuser -k /dev/ttyACM0`。
若權限不足：`sudo usermod -aG dialout $USER` 後重新登錄（或臨時執行 `sudo chmod a+rw /dev/ttyACM0`）。

### 韌體電源互動（XIAO ESP32S3）

- 上電時長按按鈕約 0.8 秒啟動。
- 執行中長按約 2.5 秒進入深度睡眠。
- 執行中短按仍會觸發採集。

## 🛠️ 配置

### 核心環境變量

- `DATABASE_URL`：可選的 Postgres DSN，用於持久化存儲。
- `IDEASGLASS_WHISPER_MODEL`：`base`（預設）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU 模式。
- `IDEASGLASS_TRANSCRIBE`：`1`（預設）啓用轉錄，`0` 關閉。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滾動轉錄推送間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：逗號分隔閾值（預設 `3000,6000,15000`）。

| Variable | Default / options | Effect |
|---|---|---|
| `DATABASE_URL` | unset by default | Enables Postgres persistence for account/device data |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Controls accuracy vs latency |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` or `cpu` | Inference backend |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | Mixed precision control |
| `IDEASGLASS_TRANSCRIBE` | `1` | Toggle transcription pipeline |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | runtime configured | Rolling transcript push interval |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Progressive transcript emission thresholds |

安全的 `DATABASE_URL` 範例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local auth）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（password auth）

### 音訊增益與分段參數

- `IDEASGLASS_GAIN_TARGET`（預設 `0.032`）
- `IDEASGLASS_GAIN_MAX`（預設 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（預設 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（預設 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（預設 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（預設 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（預設 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（預設繼承 chunk gain target）

| Audio knob | Default | Purpose |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Target RMS normalization |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Upper clamp for gain amplification |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Floor to avoid amplifying near-silence |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Speech activity RMS baseline |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Margin around speech threshold |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Segment length target |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Segment overlap for continuity |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | inherits chunk gain | Segment-level normalization target |

### 模型預拉取（可選）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 範例

### 生成並綁定設備 ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

然後在下列文件中設置 `kDeviceId`：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

儀表盤流程：

1. 在 Settings 中註冊/登錄。
2. 在 Account 面板綁定設備。
3. 只有已綁定設備會向你的帳號推流。

### REST 接入範例

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

## 🧭 開發說明

### 重點區域

本倉庫包含多條後端路線。當前貢獻與執行重點為 `backend/glass/`，除非另有說明。

### 靜態/語法檢查

```bash
python -m compileall backend/glass/app.py
```

### 開發者文件

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 註：在當前倉庫快照中，上述部分歷史連結似乎已移動（例如，bridge 說明現在位於 `references/ideasglass_bridge.md`）。原始連結作為規範 README 內容已保留。

### 快速設備綁定（保留流程）

- 生成 ID（在 conda `glass` 中）：`python backend/glass/tools/generate_device_id.py`
- 在韌體中設置：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 執行後端並打開 `http://localhost:8765`，註冊/登錄，然後在 Account 面板綁定設備 ID

## 🆘 故障排查

- **連接埠已被佔用：** 改用其他連接埠啟動後端，並更新客戶端設置。
- **串口被佔用：** `fuser -k /dev/ttyACM0`。
- **Linux 串口權限不足：** `sudo usermod -aG dialout $USER`，然後重新登錄。
- **Postgres 不可用：** 後端可在無 DB 模式下提供部分功能；請檢查 `DATABASE_URL` 並重新啟動。
- **Whisper 性能問題：** 使用更小模型（`base`/`small`），或透過 `IDEASGLASS_TRANSCRIBE=0` 關閉轉錄。
- **ESP32 TLS/時間同步不穩定：** 檢查 Wi-Fi、NTP 可用性（UDP/123）及證書/主機配置；詳見 `references/ideasglass_bridge.md`。
- **即時波形無更新：** 檢查後端日誌和瀏覽器控制檯中的 `[IdeasGlass][wave]`，並確認 `/ws/stream` 連接狀態。

## 🌐 生態連結

🧠 **EchoMind** — 面向學習與創作的多語言 AI 夥伴。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 將大膽概念轉化為產品的研究社群。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 將小勝轉化為收入的自動化工具。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理與化學學習路徑及筆記。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 將想法轉化為草稿、任務與貼文發佈的代理。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 捕捉、翻譯並自動生成高光短片。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 連接貢獻回報與鏈上價值的獎勵/結算系統。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究筆記與隨筆文集。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas、EchoMind、LazyEdit 與 IdeasGlass 背後的工作室。  
[lazying.art](https://lazying.art)

## ❤️ 支持與聯繫

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持將幫助我們推進硬體、AI 工作流程與生態建設，向社群持續開放。
- Your support keeps the wearable, agent, and ecosystem roadmap moving.

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

- 合作請發送郵件至 **contact@lazying.art**，郵件主題為 `IdeasGlass`。

IdeasGlass 讓 AI 可穿戴設備不止於“傾聽”，而是開始與你一起“建構”。

## 🙏 致謝

我們站在優秀開源項目的肩膀上，特別感謝：

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

## 🛣️ 路線圖

- 強化並文件化 WAN/TLS 場景下端到端音訊流路徑。
- 持續優化轉錄質量與延遲權衡（模型/設備/閾值預設）。
- 在儀表盤中擴展設備管理與帳號級多設備工作流程。
- 將遺留/並行後端路線（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）與主線路 `backend/glass` 對齊或整合。
- 維護並持續更新 `i18n/` 下的多語言 README 版本。

## 🤝 貢獻

歡迎貢獻。倉庫特定流程請遵循 `AGENTS.md`。

建議在提交 PR 前進行本地驗證：

```bash
python -m compileall backend/glass/app.py
```

提交變更時：

- Commit 標題保持簡短、動作導向（現在時）。
- 當行為依賴環境變量時，在 PR 說明中寫明相關變量（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）。
- 附上測試證據（後端日誌、儀表盤行為、韌體輸出）。
- 嚴禁提交密鑰（`DATABASE_URL`、API token、憑證文件）。

## 📄 許可證

當前倉庫快照中未檢測到頂層 `LICENSE` 文件。在明確許可證文件添加之前，請將使用與再分發視為需要維護者批准。
