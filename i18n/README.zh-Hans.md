[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*一款可穿戴 AI 眼镜，将想法转化为行动、收入与创作动能。*

> 以语音为先的可穿戴 AI 管线：从 ESP32 眼镜采集，在 FastAPI 中处理，并通过实时 PWA 仪表盘监控与控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>生态系统</b><br/>
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
  <sub>App UI（左）· 硬件（右）</sub>
</div>

在 <a href="https://onlyideas.art">onlyideas.art</a> 探索社区实验。

## 🚀 概览

IdeasGlass 是一个以 AI 为核心、以语音交互为优先的可穿戴系统，用于捕捉并执行想法。在本仓库中，主要运行路径是：

- `backend/glass/`：提供 FastAPI API、WebSocket 接入、基于 Whisper 的转录，以及可安装的 PWA 仪表盘。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：用于 XIAO ESP32S3 固件，负责流式传输遥测/音频/照片。

如果你是第一次接触此仓库，请先从这两处开始。

### 快速一览

| 区域 | 主要位置 | 作用 |
|---|---|---|
| 后端 API + PWA | `backend/glass/` | FastAPI 端点、WebSocket 接入/分发、转录、仪表盘 |
| 固件 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 采集/流式客户端 |
| 网桥说明 | `references/ideasglass_bridge.md` | TLS/WAN 稳定性说明与部署实战建议 |
| README 翻译 | `i18n/` | 与规范英文 README 同步的多语言文档 |

## ✨ 为什么是 IdeasGlass

IdeasGlass 是一款面向“持续涌现创意人群”的 AI 可穿戴设备。无论你是在移动中口述概念，还是正在进行直播，它都能在灵感出现的瞬间完成捕捉、翻译、整理并推动执行。

## 🧩 功能

### 产品愿景功能

- **创作原生硬件**：轻量眼镜与可穿戴输入，围绕语音优先捕捉与细微手势快捷操作设计。
- **即时翻译**：实时语言检测/翻译，让你在跨团队或跨受众创作时无需切换工具。
- **EchoMind 副驾**：与 `chat.lazying.art` 深度联动，用于头脑风暴、脚本草拟与多语言内容辅导。
- **频道自动驾驶**：自动生成大纲、长视频脚本、短内容钩子，并安排发布到 YouTube 或其他渠道。
- **高光与短片**：自动挑选精彩片段，生成缩略图、字幕与可直接发布到社交平台的短视频。
- **收入层**：连接 LazyingArt Coin，实现打赏、积分结算与链上资产转换。
- **支出与专注**：跟踪运营支出，识别高收益内容形式，并提炼你的个人优势用于下一轮项目。

### 仓库/运行时功能

- FastAPI 后端，提供 REST + WebSocket 端点用于接入（`/api/v1/audio`, `/ws/audio-ingest`）与实时流分发（`/ws/stream`）。
- 可确定行为的音频分段（默认约 15 秒，带重叠）并写入 `backend/glass/audio_segments/`。
- 可选 openai-whisper 流式转录，支持可配置的延迟阈值。
- 可选 Postgres 持久化（`DATABASE_URL`），覆盖消息、照片、音频块、分段、转录数据。
- PWA 仪表盘支持实时波形、转录更新，并可在桌面/移动端安装。
- 支持 XIAO ESP32S3 Sense 摄像头 + 麦克风流程的 Arduino 固件。

## 🔄 示例工作流

1. **捕捉**：口述或勾勒一个概念；IdeasGlass 会转录、翻译并标注意图。
2. **共创**：EchoMind 打磨想法，生成脚本，并给出面向不同平台的 CTA 建议。
3. **发布**：频道代理自动产出高光视频、图集素材，并附带元数据上传。
4. **变现**：积分通过 LazyingArt Coin（`coin.lazying.art`）流转，收益同步到你偏好的钱包。
5. **复盘**：支出、触达与互动仪表盘帮助你识别下一步该重点加码的方向。

## 🗂️ 项目结构

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

## 🧰 前置条件

- Python 3.10+
- `pip`（或带兼容 Python 的 conda 环境）
- 可选：NVIDIA GPU + CUDA/cuDNN（用于更快的 Whisper 推理）
- 可选：PostgreSQL（用于持久化）
- 固件侧：Arduino IDE 或 `arduino-cli`、Seeed XIAO ESP32S3 Sense，且启用 PSRAM

| 组件 | 要求 | 说明 |
|---|---|---|
| 后端运行时 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可选） | NVIDIA + CUDA/cuDNN | 提升 Whisper 延迟表现 |
| 持久化（可选） | PostgreSQL | 通过 `DATABASE_URL` 启用 |
| 固件工具链 | Arduino IDE / `arduino-cli` | 使用 XIAO ESP32S3 配置并启用 PSRAM |

## ⚙️ 安装

### 后端依赖

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 固件前置准备

- 将 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 复制为 `wifi_credentials.h`（推荐），并填写 SSID/密码。
- 在 Arduino IDE 中选择开发板 `ESP32 -> XIAO_ESP32S3`，并设置 `PSRAM: OPI PSRAM`。
- 分区方案：`Default with spiffs (3MB APP/1.5MB SPIFFS)`；若不需要文件系统可使用 `Maximum APP`。

## ▶️ 使用

### 运行后端（uvicorn）

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### 运行后端（辅助脚本）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 打开仪表盘

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | 用途 |
|---|---|
| `/` | 主仪表盘（支持 PWA 安装） |
| `/healthz` | 后端存活检查 |
| `/ws/audio-ingest` | 设备接入 WebSocket |
| `/ws/stream` | 面向仪表盘客户端的实时流分发 |

### 登录并绑定设备

1. 在仪表盘的 Settings/Account 区域注册或登录。
2. 在 `Bind device` 字段中绑定你的设备 ID。
3. 只有已绑定设备会向你的账号推流。

生成设备 ID + 二维码图像：

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

通过 API 绑定（需要 cookie 会话）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

验证当前账号与已绑定设备：

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

可选迁移（将历史数据重命名到新设备 ID）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 固件构建/上传（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

若端口被占用：`fuser -k /dev/ttyACM0`。
若权限不足：`sudo usermod -aG dialout $USER` 后重新登录（或临时执行 `sudo chmod a+rw /dev/ttyACM0`）。

### 固件电源交互（XIAO ESP32S3）

- 上电时长按按钮约 0.8 秒启动。
- 运行中长按约 2.5 秒进入深度睡眠。
- 运行中短按仍会触发采集。

## 🛠️ 配置

### 核心环境变量

- `DATABASE_URL`：可选的 Postgres DSN，用于持久化存储。
- `IDEASGLASS_WHISPER_MODEL`：`base`（默认）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU 模式。
- `IDEASGLASS_TRANSCRIBE`：`1`（默认）启用转录，`0` 关闭。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滚动转录推送间隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：逗号分隔阈值（默认 `3000,6000,15000`）。

| Variable | Default / options | Effect |
|---|---|---|
| `DATABASE_URL` | unset by default | Enables Postgres persistence for account/device data |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Controls accuracy vs latency |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` or `cpu` | Inference backend |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | Mixed precision control |
| `IDEASGLASS_TRANSCRIBE` | `1` | Toggle transcription pipeline |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | runtime configured | Rolling transcript push interval |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Progressive transcript emission thresholds |

安全的 `DATABASE_URL` 示例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local auth）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（password auth）

### 音频增益与分段参数

- `IDEASGLASS_GAIN_TARGET`（默认 `0.032`）
- `IDEASGLASS_GAIN_MAX`（默认 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（默认 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（默认 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（默认 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（默认 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（默认 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（默认继承 chunk gain target）

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

### 模型预拉取（可选）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 示例

### 生成并绑定设备 ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

然后在下列文件中设置 `kDeviceId`：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

仪表盘流程：

1. 在 Settings 中注册/登录。
2. 在 Account 面板绑定设备。
3. 只有已绑定设备会向你的账号推流。

### REST 接入示例

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

## 🧭 开发说明

### 重点区域

本仓库包含多条后端路线。当前贡献与运行时重点为 `backend/glass/`，除非另有说明。

### 静态/语法检查

```bash
python -m compileall backend/glass/app.py
```

### 开发者文档

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 注：在当前仓库快照中，上述部分历史链接似乎已移动（例如，bridge 说明现在位于 `references/ideasglass_bridge.md`）。原始链接作为规范 README 内容已保留。

### 快速设备绑定（保留流程）

- 生成 ID（在 conda `glass` 中）：`python backend/glass/tools/generate_device_id.py`
- 在固件中设置：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 运行后端并打开 `http://localhost:8765`，注册/登录，然后在 Account 面板绑定设备 ID

## 🆘 故障排查

- **端口已被占用：** 改用其他端口启动后端，并更新客户端设置。
- **串口被占用：** `fuser -k /dev/ttyACM0`。
- **Linux 串口权限不足：** `sudo usermod -aG dialout $USER`，然后重新登录。
- **Postgres 不可用：** 后端可在无 DB 模式下提供部分功能；请检查 `DATABASE_URL` 并重启。
- **Whisper 性能问题：** 使用更小模型（`base`/`small`），或通过 `IDEASGLASS_TRANSCRIBE=0` 关闭转录。
- **ESP32 TLS/时间同步不稳定：** 检查 Wi-Fi、NTP 可用性（UDP/123）及证书/主机配置；详见 `references/ideasglass_bridge.md`。
- **实时波形无更新：** 检查后端日志和浏览器控制台中的 `[IdeasGlass][wave]`，并确认 `/ws/stream` 连接状态。

## 🌐 生态链接

🧠 **EchoMind** — 面向学习与创作的多语言 AI 伙伴。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 将大胆概念转化为产品的研究社区。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 将小胜转化为收入的自动化工具。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理与化学学习路径及笔记。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 将想法转化为草稿、任务与帖子发布的代理。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 捕捉、翻译并自动生成高光短片。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 连接贡献回报与链上价值的奖励/结算系统。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究笔记与随笔文集。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas、EchoMind、LazyEdit 与 IdeasGlass 背后的工作室。  
[lazying.art](https://lazying.art)

## ❤️ 支持与联系

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
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

- 合作请发送邮件至 **contact@lazying.art**，邮件主题为 `IdeasGlass`。

IdeasGlass 让 AI 可穿戴设备不止于“倾听”，而是开始与你一起“构建”。

## 🙏 致谢

我们站在优秀开源项目的肩膀上，特别感谢：

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

## 🛣️ 路线图

- 强化并文档化 WAN/TLS 场景下端到端音频流路径。
- 持续优化转录质量与延迟权衡（模型/设备/阈值预设）。
- 在仪表盘中扩展设备管理与账号级多设备工作流。
- 将遗留/并行后端路线（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）与主线路 `backend/glass` 对齐或整合。
- 维护并持续更新 `i18n/` 下的多语言 README 版本。

## 🤝 贡献

欢迎贡献。仓库特定流程请遵循 `AGENTS.md`。

建议在提交 PR 前进行本地验证：

```bash
python -m compileall backend/glass/app.py
```

提交变更时：

- Commit 标题保持简短、动作导向（现在时）。
- 当行为依赖环境变量时，在 PR 说明中写明相关变量（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）。
- 附上测试证据（后端日志、仪表盘行为、固件输出）。
- 严禁提交密钥（`DATABASE_URL`、API token、凭证文件）。

## 📄 许可证

当前仓库快照中未检测到顶层 `LICENSE` 文件。在明确许可证文件添加之前，请将使用与再分发视为需要维护者批准。
