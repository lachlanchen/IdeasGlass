[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*一种可穿戴 AI 眼镜，帮助你把想法转化为行动、收益与创作势能。*

> 以语音为先的可穿戴 AI 流水线：来自 ESP32 眼镜的采集，后端处理，以及通过实时 PWA 仪表盘进行监控与控制。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| 通道 | 用途 |
|---|---|
| 🎙️ 可穿戴采集 | ESP32 眼镜准实时发送音频、图片与遥测数据 |
| 🧠 后端智能 | FastAPI 接收流、转写、分段并持久化元数据 |
| 🖥️ 仪表盘 | PWA 实时展示波形、转录文本与设备/账户状态 |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>生态</b><br/>
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
  <sub>应用界面（左） · 硬件（右）</sub>
</div>

在 <a href="https://onlyideas.art">onlyideas.art</a> 探索社区实验。

## 🚀 概览

IdeasGlass 是一个以 AI 为先的可穿戴系统，用于语音优先的灵感捕获与执行。在本仓库中，主要运行路径为：

- `backend/glass/`：FastAPI API、WebSocket 接收、基于 Whisper 的转录，以及可安装的 PWA 仪表盘。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：XIAO ESP32S3 固件，用于流式传输遥测/音频/照片。

如果你是第一次接触本仓库，请先从这里开始。

### 一览

| 区域 | 主要位置 | 职责 |
|---|---|---|
| 后端 API 与 PWA | `backend/glass/` | FastAPI 接口、WebSocket 接收/分发、转录、仪表盘 |
| 固件 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 采集与流传输客户端 |
| 桥接说明 | `references/ideasglass_bridge.md` | TLS/WAN 可靠性说明及部署现场建议 |
| README 多语言 | `i18n/` | 从规范英文 README 同步维护的多语文档 |

## ✨ 为什么是 IdeasGlass

IdeasGlass 是为“想法一直在流动”人群打造的 AI 可穿戴设备。无论你是在运动中口述一个概念，还是在直播中灵感迸发，它都能在那一刻捕获、转译、整理并推动想法落地。

## 🧩 特性

### 产品愿景特性

- **原生创作硬件**：轻量级眼镜和可穿戴输入，面向语音优先采集，并支持细腻手势快捷操作。
- **即时翻译**：实时语言检测与翻译，让你无需切换工具即可跨团队、跨受众进行创意协作。
- **EchoMind 副驾驶**：与 `chat.lazying.art` 深度配合，用于头脑风暴、脚本起草与多语内容辅导。
- **频道自动驾驶**：自动生成提纲、长文脚本、短视频钩子，并将内容发布到 YouTube 等平台。
- **精彩片段与短视频**：自动筛选高光时刻，生成缩略图、字幕和社媒友好的短片。
- **收益层**：连接 LazyingArt Coin，支持打赏、信用奖励和向链上资产转换。
- **支出与专注**：追踪运营成本，识别高转化形态，并提炼你的个人优势为下一步项目选题。

### 仓库与运行特性

- FastAPI 后端提供 REST 与 WebSocket 接口，用于接入（`/api/v1/audio`、`/ws/audio-ingest`）和实时流分发（`/ws/stream`）。
- 将音频做确定性分段（默认约 15 秒并带重叠）保存到 `backend/glass/audio_segments/`。
- 可选的 openai-whisper 流式转录，支持可配置延迟阈值。
- 可选 PostgreSQL 持久化（`DATABASE_URL`）用于消息、照片、音频块、片段和转录记录。
- PWA 仪表盘支持实时波形、转录更新，以及桌面/移动端安装。
- 支持 Seeed XIAO ESP32S3 Sense 摄像头+麦克风的 Arduino 固件。

## 🔄 示例工作流

1. **采集**：讲述或速写一个概念；IdeasGlass 会转录、翻译并标注意图。
2. **共同创作**：EchoMind 优化想法、起草脚本，并针对不同平台给出 CTA 建议。
3. **发布**：频道代理自动生成高光视频、作品图，并附带元数据上传。
4. **变现**：积分通过 LazyingArt Coin（`coin.lazying.art`）流转，与偏好的钱包结算同步。
5. **复盘**：花费、触达与互动数据仪表盘显示下一步重点方向。

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

## 🧰 先决条件

- Python 3.10+
- `pip`（或具有兼容 Python 的 conda 环境）
- 可选：NVIDIA GPU + CUDA/cuDNN，用于加速 Whisper 推理
- 可选：PostgreSQL，用于持久化存储
- 固件侧：Arduino IDE 或 `arduino-cli`，Seeed XIAO ESP32S3 Sense，开启 PSRAM

| 组件 | 要求 | 说明 |
|---|---|---|
| 后端运行环境 | Python 3.10+, `pip` | 使用 venv 或 conda（`glass`） |
| GPU 加速（可选） | NVIDIA + CUDA/cuDNN | 降低 Whisper 延迟 |
| 持久化（可选） | PostgreSQL | 通过 `DATABASE_URL` 开启 |
| 固件工具链 | Arduino IDE / `arduino-cli` | 使用带 PSRAM 的 XIAO ESP32S3 配置 |

## ⚙️ 安装

### 后端依赖

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 固件先决条件

- 将 `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` 复制为 `wifi_credentials.h`（推荐），并填写 SSID 与密码。
- 在 Arduino IDE 中，选择开发板 `ESP32 -> XIAO_ESP32S3`，并设置 `PSRAM: OPI PSRAM`。
- 分区方案：`Default with spiffs (3MB APP/1.5MB SPIFFS)` 或在不需要文件系统时使用 `Maximum APP`。

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

### 运行后端（辅助方式）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 打开仪表盘

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| 接口 | 用途 |
|---|---|
| `/` | 主仪表盘（支持 PWA） |
| `/healthz` | 后端存活性检查 |
| `/ws/audio-ingest` | 设备采集 WebSocket |
| `/ws/stream` | 实时流分发到客户端 |

### 登录并绑定设备

1. 在仪表盘的“设置/账户”区域注册或登录。
2. 在 `Bind device` 输入框中绑定你的设备 ID。
3. 只有绑定的设备才会向你的账户推送流。

生成设备 ID 与二维码图像：

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

查看当前账户与已绑定设备：

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

### 固件编译/上传（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

若串口被占用：`fuser -k /dev/ttyACM0`。
若提示权限不足：执行 `sudo usermod -aG dialout $USER` 并重新登录（或临时执行 `sudo chmod a+rw /dev/ttyACM0`）。

### 固件电源交互（XIAO ESP32S3）

- 上电约 0.8 秒长按启动。
- 运行时长按约 2.5 秒进入深度睡眠。
- 运行时短按仍会触发采集。

## 🛠️ 配置

### 核心环境变量

- `DATABASE_URL`：可选的 Postgres DSN，用于持久化存储。
- `IDEASGLASS_WHISPER_MODEL`：`base`（默认）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`：`cuda` 或 `cpu`。
- `IDEASGLASS_WHISPER_FP16`：`1` 表示 GPU 混合精度，`0` 表示 CPU 模式。
- `IDEASGLASS_TRANSCRIBE`：`1`（默认）启用转录，`0` 停用转录。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`：滚动转录间隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`：逗号分隔阈值（默认 `3000,6000,15000`）。

| 变量 | 默认值/选项 | 作用 |
|---|---|---|
| `DATABASE_URL` | 默认未设置 | 为账户/设备数据启用 Postgres 持久化 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（含 `small`、`medium`、`large-v3`、`large-v3-turbo`） | 控制精度与延迟平衡 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` 或 `cpu` | 推理后端 |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU），`0`（CPU 安全） | 混合精度控制 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 转录流水线开关 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 运行时配置 | 滚动转录推送间隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 阶梯式转录输出阈值 |

安全的 `DATABASE_URL` 示例：

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（本地/peer 认证）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（密码认证）

### 音频增益与分段参数

- `IDEASGLASS_GAIN_TARGET`（默认 `0.032`）
- `IDEASGLASS_GAIN_MAX`（默认 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（默认 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（默认 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（默认 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（默认 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（默认 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（默认继承分段增益目标）

| 音频参数 | 默认值 | 作用 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 目标 RMS 归一化 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 增益放大上限 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 避免放大近静音段 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 语音活动 RMS 基线 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 语音阈值边界冗余 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 分段目标长度 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 分段重叠保证连续性 |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | 继承块级增益 | 分段级归一化目标 |

### 模型预取（可选）

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

然后设置 `kDeviceId` 为：

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

仪表盘流程：

1. 在“设置”中注册/登录。
2. 在“账户”面板绑定设备。
3. 只有已绑定设备才会向你的账户推送流。

### REST 接口示例

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

### 重点方向

这个仓库包含多条后端线路。除非另有说明，否则当前贡献建议与运行重点为 `backend/glass/`。

### 静态/语法检查

```bash
python -m compileall backend/glass/app.py
```

### 开发文档

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 说明：在当前仓库快照中，上述部分历史链接可能已迁移（例如桥接说明现在位于 `references/ideasglass_bridge.md`）。原始链接仍保留为英文 README 的规范内容。

### 快速设备绑定（保留流程）

- 生成 ID（在 conda `glass` 中）：`python backend/glass/tools/generate_device_id.py`
- 在固件中设置：`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- 启动后端并打开 `http://localhost:8765`，注册/登录，再在账户面板绑定设备 ID

## 🆘 故障排查

- **端口被占用：** 在其他端口启动后端，并更新客户端设置。
- **串口忙：** `fuser -k /dev/ttyACM0`。
- **Linux 串口权限不足：** `sudo usermod -aG dialout $USER` 后重新登录。
- **Postgres 不可用：** 后端可在无数据库情况下运行部分功能；请检查 `DATABASE_URL` 并重启服务。
- **Whisper 性能问题：** 使用更小模型（`base`/`small`）或通过 `IDEASGLASS_TRANSCRIBE=0` 关闭转录。
- **ESP32 TLS/时间同步不稳定：** 检查 Wi-Fi、NTP 可用性（UDP/123）与证书/主机设置；详见 `references/ideasglass_bridge.md` 的现场说明。
- **实时波形无更新：** 检查后端日志与浏览器控制台中的 `[IdeasGlass][wave]` 追踪，并确认 `/ws/stream` 连接正常。

## 🌐 生态链接

🧠 **EchoMind** — 多语学习与创作辅助 AI 同行。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 从研究到产品的大胆创意社区。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 将小成果自动转化为收入的自动化流程。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理与化学课程与笔记。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 将灵感变为草稿、任务与发布内容的助手。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 采集、翻译并自动生成高光短片。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 将贡献与链上价值连接的奖励与结算体系。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究笔记与文章合集。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — 承载 OnlyIdeas、EchoMind、LazyEdit 与 IdeasGlass 的工作室。  
[lazying.art](https://lazying.art)

## 🙏 致谢

我们的工作站在许多优秀的开源项目上。特别感谢：

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **推荐计划**：使用优惠码 `LazyingArt` 可节省 10%（售出 10 件后可解锁 30% 返佣）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 路线图

- 加固并记录 WAN/TLS 场景下端到端音频流路径。
- 持续优化转录质量与延迟的平衡（模型/设备/阈值预设）。
- 扩展设备管理与账户级多设备协同工作流。
- 对齐或整合遗留/并行后端路线（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）与主路径 `backend/glass`。
- 在 `i18n/` 下维护并更新多语言 README。

## 🤝 贡献

欢迎参与贡献。仓库级工作流请遵循 `AGENTS.md`。

建议在提 PR 前进行本地校验：

```bash
python -m compileall backend/glass/app.py
```

提交变更时：

- 保持提交标题简洁且动作导向（现在时）。
- 当行为受相关环境变量影响时，在 PR 说明中注明（例如 `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）。
- 提供测试证据（后端日志、仪表盘行为、固件输出）。
- 切勿提交秘密信息（如 `DATABASE_URL`、API token、凭据文件）。

## 📄 许可证

此仓库快照中未检测到顶层 `LICENSE` 文件。在正式添加许可文件前，请将使用和再分发行为视为需要维护者批准。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
