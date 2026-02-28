[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*一种可穿戴 AI 眼镜，将想法转化为行动、收益与持续创作动能。*

> 以语音优先的可穿戴 AI 流水线：由 ESP32 眼镜采集，后端处理，并通过实时 PWA 仪表盘进行监控与控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| 通道 | 用途 |
|---|---|
| 🎙️ 可穿戴采集 | ESP32 眼镜近实时发送音频、照片和遥测数据 |
| 🧠 后端智能 | FastAPI 接收流、转写、分段并持久化元数据 |
| 🖥️ 仪表盘 | PWA 显示实时波形、转录文本和设备/账户状态 |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>应用界面（左） · 硬件（右）</sub>
</div>

在 <a href="https://onlyideas.art">onlyideas.art</a> 上探索社区实验。

## 🚀 概览

IdeasGlass 是一个以 AI 为先的可穿戴系统，专注于语音优先的灵感捕获与执行。本仓库的主要运行路径是：

- `backend/glass/`：FastAPI API、WebSocket 接入、基于 Whisper 的转写，以及可安装的 PWA 仪表盘。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：用于 XIAO ESP32S3 的固件，负责遥测/音频/照片流式上报。

如果你是第一次进入本仓库，请先从这里开始。

## 📚 目录

- [🚀 概览](#-概览)
- [✨ 为什么选择 IdeasGlass](#-为什么选择-ideasglass)
- [🧩 功能](#-功能)
- [🔄 示例工作流](#-示例工作流)
- [🗂️ 项目结构](#-项目结构)
- [🧰 先决条件](#-先决条件)
- [⚙️ 安装](#️-安装)
- [▶️ 使用方法](#-使用方法)
- [🛠️ 配置](#️-配置)
- [🧪 示例](#-示例)
- [🧭 开发说明](#-开发说明)
- [🆘 故障排查](#️-故障排查)
- [🌐 生态链接](#-生态链接)
- [🙏 致谢](#-致谢)
- [🛣️ 路线图](#️-路线图)
- [🤝 贡献](#-贡献)
- [❤️ Support](#-support)
- [📄 许可证](#-许可证)

### 一览

| 区域 | 主要位置 | 职能 |
|---|---|---|
| 后端 API + PWA | `backend/glass/` | FastAPI 接口、WebSocket 接收/分发、转录、仪表盘 |
| 固件 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 采集/流式客户端 |
| 桥接说明 | `references/ideasglass_bridge.md` | TLS/WAN 可靠性与部署现场技巧 |
| README 翻译 | `i18n/` | 与规范英文 README 同步的多语言文档 |

## ✨ 为什么选择 IdeasGlass

IdeasGlass 是为灵感不断涌现的人群设计的 AI 可穿戴产品。无论你是在运动中口述概念，还是在直播中做头脑风暴，它都能在灵感出现的瞬间捕捉、翻译、整理并推动创作执行。

## 🧩 功能

### 产品愿景功能

- **原生创作硬件**：轻量化眼镜与可穿戴输入，针对语音优先采集进行了调优，并支持精细手势快捷操作。
- **即时翻译**：实时语言识别和翻译，让你无需切换工具即可在团队或受众间跨语协作。
- **EchoMind 副驾驶**：与 `chat.lazying.art` 深度联动，用于头脑风暴、脚本起草与多语内容教练。
- **频道自动驾驶**：自动生成提纲、长篇脚本、短内容钩子，并将内容上传到 YouTube 或其他频道。
- **精彩片段与剪辑**：自动选取高光时刻，生成缩略图、字幕和可发布社交短片。
- **收益层**：对接 LazyingArt Coin，实现打赏、积分支付和与链上资产的兑换。
- **支出与专注**：跟踪运营支出，识别高收益内容形态，并提炼你的个人优势用于下一批项目。

### 仓库/运行特性

- FastAPI 后端提供 REST 与 WebSocket 接口：接入端点（`/api/v1/audio`, `/ws/audio-ingest`）与实时流分发端点（`/ws/stream`）。
- 确定性的音频分段（默认约 15 秒并带重叠）保存到 `backend/glass/audio_segments/`。
- 可选的 openai-whisper 流式转录，支持可配置延迟阈值。
- 可选的 Postgres 持久化（`DATABASE_URL`）用于消息、照片、音频块、片段和转录文本。
- PWA 仪表盘支持实时波形、转录更新，并支持桌面端/移动端安装。
- Arduino 固件支持 XIAO ESP32S3 Sense 的相机与麦克风数据流。

## 🔄 示例工作流

1. **采集**——说出或草拟一个概念；IdeasGlass 进行转录、翻译并标记意图。
2. **共同创作**——EchoMind 优化创意、起草脚本，并为各平台建议 CTA。
3. **发布**——频道代理自动生成亮点视频、图库图片，并带元数据上传。
4. **变现**——积分通过 LazyingArt Coin（`coin.lazying.art`）流转，并与首选钱包同步提现。
5. **复盘**——支出、触达和参与度看板告诉你下一步应加码的方向。

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

## 🧰 先决条件

- Python 3.10+
- `pip`（或使用兼容版本 Python 的 conda 环境）
- 可选：NVIDIA GPU + CUDA/cuDNN，用于更快的 Whisper 推理
- 可选：PostgreSQL 持久化
- 固件侧：Arduino IDE 或 `arduino-cli`，Seeed XIAO ESP32S3 Sense，启用 PSRAM

| 组件 | 要求 | 说明 |
|---|---|---|
| 后端运行环境 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可选） | NVIDIA + CUDA/cuDNN | 改善 Whisper 延迟 |
| 持久化（可选） | PostgreSQL | 通过 `DATABASE_URL` 启用 |
| 固件工具链 | Arduino IDE / `arduino-cli` | 使用启用 PSRAM 的 XIAO ESP32S3 配置 |

## ⚙️ 安装

### 后端依赖

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 固件前置条件

- 建议将 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 复制为 `wifi_credentials.h`，并填写 SSID 与密码。
- 在 Arduino IDE 中，选择开发板 `ESP32 -> XIAO_ESP32S3`，并将 `PSRAM` 设置为 `OPI PSRAM`。
- 分区方案：`Default with spiffs (3MB APP/1.5MB SPIFFS)`，或在不需要文件系统时使用 `Maximum APP`。

## ▶️ 使用方法

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

### 运行后端（辅助命令）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 打开仪表盘

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| 接口 | 用途 |
|---|---|
| `/` | 主仪表盘（PWA 兼容界面） |
| `/healthz` | 后端健康检查 |
| `/ws/audio-ingest` | 设备接入 WebSocket |
| `/ws/stream` | 实时流推送到仪表盘客户端 |

### 登录并绑定设备

1. 在仪表盘的设置/账户区域注册或登录。
2. 在 `Bind device` 字段绑定你的设备 ID。
3. 只有已绑定设备才会把数据流推送到你的账户。

生成设备 ID 与二维码：

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

验证当前账户与已绑定设备：

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

可选迁移（将历史数据重命名为新的设备 ID）：

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 固件编译/上传（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

如果端口被占用：`fuser -k /dev/ttyACM0`。
如果权限不足：`sudo usermod -aG dialout $USER` 后重新登录（或临时执行 `sudo chmod a+rw /dev/ttyACM0`）。

### 固件电源交互（XIAO ESP32S3）

- 开机时长按约 0.8 秒进入启动。
- 运行中长按约 2.5 秒进入深度睡眠。
- 运行中短按仍可触发采集。

## 🛠️ 配置

### 核心环境变量

- `DATABASE_URL`：可选的 Postgres DSN，用于持久化存储。
- `IDEASGLASS_WHISPER_MODEL`：`base`（默认）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU。
- `IDEASGLASS_TRANSCRIBE`：`1`（默认）启用转录，`0` 停用转录。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滚动转录间隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：逗号分隔阈值（默认 `3000,6000,15000`）。

| 变量 | 默认值 / 选项 | 作用 |
|---|---|---|
| `DATABASE_URL` | 默认未设置 | 为账户/设备数据开启 Postgres 持久化 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（`small`、`medium`、`large-v3`、`large-v3-turbo`） | 控制准确率与延迟平衡 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` 或 `cpu` | 推理后端 |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU），`0`（CPU 安全） | 混合精度控制 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 转录流水线开关 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 运行时配置 | 滚动转录推送间隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 分级转录触发阈值 |

`DATABASE_URL` 安全示例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local 认证）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（密码认证）

### 音频增益与分段参数

- `IDEASGLASS_GAIN_TARGET`（默认 `0.032`）
- `IDEASGLASS_GAIN_MAX`（默认 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（默认 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（默认 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（默认 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（默认 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（默认 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（默认为块增益目标）

| 音频参数 | 默认值 | 作用 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 目标 RMS 归一化 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 增益放大上限 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 避免放大近乎静音的片段 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 语音活动 RMS 基线 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 语音阈值边界缓冲 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 目标片段长度 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 为连续性保留的片段重叠 |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | 继承块级增益目标 | 片段级归一化目标 |

### 模型预加载（可选）

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

然后在以下文件设置 `kDeviceId`：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

仪表盘流程：

1. 在“设置”中注册或登录。
2. 在“账户”面板绑定设备。
3. 只有已绑定设备会向你的账户发送流。

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

## 🧭 开发说明

### 关注方向

该仓库包含多条后端线路。当前贡献和运行重点在 `backend/glass/`，除非另有要求。

### 静态/语法检查

```bash
python -m compileall backend/glass/app.py
```

### 开发文档

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 说明：在当前仓库快照中，上述部分历史链接可能已迁移（例如，桥接说明现在位于 `references/ideasglass_bridge.md`）。原始链接作为规范版 README 内容保留。

### 快速设备绑定（保留流程）

- 生成 ID（在 conda `glass` 环境）：`python backend/glass/tools/generate_device_id.py`
- 在固件中设置：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 运行后端并打开 `http://localhost:8765`，注册/登录后在账户面板绑定设备 ID

## 🆘 故障排查

- **端口已占用：** 在其他端口运行后端并更新客户端设置。
- **串口忙：** `fuser -k /dev/ttyACM0`。
- **Linux 串口权限不足：** `sudo usermod -aG dialout $USER` 并重新登录。
- **Postgres 不可用：** 后端在无数据库时仍可运行部分功能；请确认 `DATABASE_URL` 并重启服务。
- **Whisper 性能问题：** 使用更小模型（`base`/`small`）或设置 `IDEASGLASS_TRANSCRIBE=0` 关闭转录。
- **ESP32 TLS/时间同步不稳定：** 检查 Wi-Fi、NTP 可用性（UDP/123）和证书/主机设置；详见 `references/ideasglass_bridge.md` 的现场说明。
- **实时波形无更新：** 检查后端日志和浏览器控制台中的 `[IdeasGlass][wave]` 追踪，并确认 `/ws/stream` 连接正常。

## 🌐 生态链接

| 品牌 | 用途 | 链接 |
|---|---|---|
| 🧠 EchoMind | 支持学习与创作的多语言 AI 同伴 | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | 从研究到产品的社区，专注大胆创意 | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | 将小突破自动转化为收益的自动化流程 | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | 物理与化学课程和实验记录 | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | 将想法变为草稿、任务和发布内容的代理 | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | 采集、翻译并自动生成高光片段 | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | 将贡献和链上价值连接的奖励与结算体系 | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | 研究笔记和论文集合 | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | 支撑 OnlyIdeas、EchoMind、LazyEdit 与 IdeasGlass 的工作室 | [lazying.art](https://lazying.art) |

## 🙏 致谢

本项目基于许多优秀开源项目，感谢：

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **推荐计划**：使用优惠码 `LazyingArt` 可节省 10%（售出 10 件后可解锁 30% 佣金）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 路线图

- 强化并记录 WAN/TLS 场景下的端到端音频流。
- 持续优化转录质量与延迟之间的平衡（模型/设备/阈值预设）。
- 扩展仪表盘中的设备管理与账号级多设备工作流。
- 与主路径 `backend/glass` 对齐或合并遗留并行后端（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）。
- 在 `i18n/` 下持续维护和更新多语言 README。

## 🤝 贡献

欢迎贡献代码。仓库级流程请遵循 `AGENTS.md`。

提交 PR 前建议做本地校验：

```bash
python -m compileall backend/glass/app.py
```

提交改动时：

- 保持提交标题简短且动作导向（现在时）。
- 当行为依赖环境变量时，在 PR 说明中注明（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）。
- 附上测试证据（后端日志、仪表盘行为、固件输出）。
- 不要提交密钥（如 `DATABASE_URL`、API token、凭据文件）。

## 📄 许可证

在本仓库快照中未检测到顶层 `LICENSE` 文件。在正式添加许可文件前，请将使用和再分发视为需要仓库维护者批准。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
