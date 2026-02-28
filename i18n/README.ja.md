[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*アイデアを行動へ、収益へ、創造的な勢いへ変える、ウェアラブルAI。*

> 音声ファーストのウェアラブルAIパイプラインです。ESP32のグラスから音声を取り込み、FastAPIで処理し、ライブPWAダッシュボードで監視・操作できます。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| レーン | 用途 |
|---|---|
| 🎙️ ウェアラブル収集 | ESP32グラスが音声、写真、テレメトリをほぼリアルタイムで送信 |
| 🧠 バックエンドの知能 | FastAPIがストリームを取り込み、文字起こしを行い、セグメント化してメタデータを保存 |
| 🖥️ ダッシュボード | PWAがライブ波形、文字起こし、デバイス/アカウント状態を表示 |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlassアプリUI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlassハードウェア" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>アプリUI（左） · ハードウェア（右）</sub>
</div>

コミュニティの実験は <a href="https://onlyideas.art">onlyideas.art</a> でご確認ください。

## 🚀 Overview

IdeasGlassは、音声ファーストでアイデアをキャプチャして実行につなぐAIファーストのウェアラブルシステムです。主な実行パスは次のとおりです。

- `backend/glass/` はFastAPI API、WebSocket取り込み、Whisperベースの文字起こし、およびインストール可能なPWAダッシュボード。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` はXIAO ESP32S3ファームウェアで、テレメトリ、音声、写真をストリーミングします。

リポジトリを初めて使う場合は、まずここから始めてください。

## 📚 Table of Contents

- [🚀 Overview](#-overview)
- [✨ Why IdeasGlass](#-why-ideasglass)
- [🧩 Features](#-features)
- [🔄 Sample Workflow](#-sample-workflow)
- [🗂️ Project Structure](#-project-structure)
- [🧰 Prerequisites](#-prerequisites)
- [⚙️ Installation](#️-installation)
- [▶️ Usage](#️-usage)
- [🛠️ Configuration](#️-configuration)
- [🧪 Examples](#-examples)
- [🧭 Development Notes](#-development-notes)
- [🆘 Troubleshooting](#️-troubleshooting)
- [🌐 Ecosystem Links](#-ecosystem-links)
- [🙏 Acknowledgements](#-acknowledgements)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contribution](#-contribution)
- [❤️ Support](#-support)
- [📄 License](#-license)

### At a glance

| エリア | 主な場所 | 機能 |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPIエンドポイント、WebSocket取り込み/配信、文字起こし、ダッシュボード |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32キャプチャ/ストリーミングクライアント |
| Bridge notes | `references/ideasglass_bridge.md` | TLS/WAN信頼性ノートとデプロイ時の現場向けヒント |
| README translations | `i18n/` | 正規READMEから同期された多言語ドキュメント |

## ✨ Why IdeasGlass

IdeasGlassは、アイデアが絶えず湧く人向けに作られたAIファーストなウェアラブルです。移動しながらコンセプトを口述したりライブ配信をしたりしているときでも、着想した瞬間にクリエイティビティを文字起こし・翻訳・整理・実行へと接続します。

## 🧩 Features

### Product vision features

- **Creation-native hardware** – 軽量なグラスとウェアラブル入力により、音声ファーストの収集とジェスチャーショートカットを前提に設計。
- **Instant translation** – リアルタイム言語検出・翻訳で、ツール切替なしにチームや視聴者間でアイデアを発想。
- **EchoMind co-pilot** – `chat.lazying.art` と緊密に連携し、ブレインストーミング、台本作成、多言語コンテンツコーチングを支援。
- **Channel autopilot** – アウトライン、長編台本、ショート向けフックを下書きし、YouTubeなどへのアップロードをスケジュール。
- **Highlights & reels** – ハイライトシーンを自動選定し、サムネイル、字幕、SNS対応クリップを生成。
- **Income layer** – LazyingArt Coinと連携して投げ銭、クレジット決済、オンチェーン資産変換を実現。
- **Spending & focus** – 運用費用を追跡し、収益性の高いフォーマットを可視化、次プロジェクトの強みを抽出。

### Repository/runtime features

- FastAPIバックエンドではREST + WebSocket（`/api/v1/audio`, `/ws/audio-ingest`）の取り込みと（`/ws/stream`）ライブ配信を提供。
- 決定論的な音声セグメント（既定は約15秒・オーバーラップ付き）を `backend/glass/audio_segments/` に保存。
- openai-whisper のストリーミング文字起こし（レイテンシ閾値設定可能）。
- 任意のPostgreSQL永続化（`DATABASE_URL`）でメッセージ、写真、チャンク、セグメント、文字起こしを保存。
- ライブ波形、文字起こし更新、デスクトップ/モバイル対応インストールを持つPWAダッシュボード。
- XIAO ESP32S3 Senseのカメラ＋マイクフロー用Arduinoファームウェア。

## 🔄 Sample Workflow

1. **Capture** – アイデアを話す、あるいは図に描く。IdeasGlassが文字起こし、翻訳、意図タグ付けを実行。
2. **Co-create** – EchoMindがアイデアを洗練し、台本を起草して、各プラットフォーム向けCTAを提案。
3. **Publish** – チャンネルエージェントがハイライト動画やギャラリー画像を自動生成し、メタデータ付きでアップロード。
4. **Monetize** – クレジットはLazyingArt Coin（`coin.lazying.art`）を経由して処理され、希望するウォレットに支払いが同期されます。
5. **Reflect** – 支出、リーチ、エンゲージメントダッシュボードから次に集中すべき点を見極めます。

## 🗂️ Project Structure

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

## 🧰 Prerequisites

- Python 3.10+
- `pip`（または互換Pythonのあるconda環境）
- 任意: Whisper推論高速化のためのNVIDIA GPU + CUDA/cuDNN
- 任意: PostgreSQL（永続化）
- ファームウェア: Arduino IDE または `arduino-cli`、Seeed XIAO ESP32S3 Sense、PSRAM有効

| コンポーネント | 要件 | メモ |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | venv または conda（`glass`） |
| GPU acceleration（任意） | NVIDIA + CUDA/cuDNN | Whisperのレイテンシ改善 |
| Persistence（任意） | PostgreSQL | `DATABASE_URL` で有効化 |
| Firmware toolchain | Arduino IDE / `arduino-cli` | PSRAM有効のXIAO ESP32S3プロファイルを使用 |

## ⚙️ Installation

### Backend dependencies

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Firmware prerequisites

- `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` を（推奨）`wifi_credentials.h` にコピーし、SSID/パスワードを設定します。
- Arduino IDE でボードを `ESP32 -> XIAO_ESP32S3`、`PSRAM: OPI PSRAM` に設定します。
- パーティションは `Default with spiffs (3MB APP/1.5MB SPIFFS)`、またはファイルシステムが不要なら `Maximum APP` を選択します。

## ▶️ Usage

### Run backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Run backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Open dashboard

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| エンドポイント | 目的 |
|---|---|
| `/` | メインダッシュボード（PWA対応UI） |
| `/healthz` | バックエンドの生存確認 |
| `/ws/audio-ingest` | デバイス取り込みWebSocket |
| `/ws/stream` | ダッシュボードクライアントへのライブ配信 |

### Login and bind your device

1. ダッシュボードのSettings/Accountで新規登録またはログインします。
2. `Bind device` フィールドにデバイスIDを入力します。
3. デバイス紐付けされたものだけがアカウントにストリーミングされます。

デバイスIDとQR画像の生成:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

API経由で紐付け（cookieセッションが必要）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

現在のアカウントと紐付け済みデバイスを確認:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

過去データを新しいデバイスIDへ移行する（任意）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Firmware build/upload (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

ポートが使用中の場合: `fuser -k /dev/ttyACM0`。
権限拒否の場合: `sudo usermod -aG dialout $USER` の後に再ログイン（または一時的に `sudo chmod a+rw /dev/ttyACM0`）。

### Firmware power UX (XIAO ESP32S3)

- 起動時に約0.8秒長押しして起動します。
- 動作中に約2.5秒長押しするとディープスリープになります。
- 動作中の短押しでもキャプチャは引き続き起動します。

## 🛠️ Configuration

### Core environment variables

- `DATABASE_URL`: 永続化用のPostgres DSN（任意）。
- `IDEASGLASS_WHISPER_MODEL`: `base`（既定）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` または `cpu`。
- `IDEASGLASS_WHISPER_FP16`: GPUでは `1`、CPUでは `0`。
- `IDEASGLASS_TRANSCRIBE`: `1` で文字起こし有効（既定）、`0` で無効。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: ローリング文字起こし間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: カンマ区切りの閾値（既定値 `3000,6000,15000`）。

| 変数 | 既定値 / 選択肢 | 効果 |
|---|---|---|
| `DATABASE_URL` | 既定未設定 | アカウント/デバイスデータのPostgres永続化を有効化 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（`small`、`medium`、`large-v3`、`large-v3-turbo`） | 精度とレイテンシのトレードオフを制御 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` または `cpu` | 推論バックエンド |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU）/`0`（CPUセーフ） | 混合精度制御 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 文字起こしパイプラインを切り替え |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 実行時設定 | ローリング文字起こし送信間隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 段階的な文字起こし出力の閾値 |

安全な `DATABASE_URL` の例:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local認証）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（パスワード認証）

### Audio gain and segmentation knobs

- `IDEASGLASS_GAIN_TARGET`（既定 `0.032`）
- `IDEASGLASS_GAIN_MAX`（既定 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（既定 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（既定 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（既定 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（既定 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（既定 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（既定はチャンクゲインターゲットを継承）

| 音声設定項目 | 既定値 | 用途 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | RMS正規化の目標値 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | ゲイン増幅の上限クランプ |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 無音に近い領域を過度に増幅しないための下限 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 音声活動のRMS基準値 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 音声しきい値の余白 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | セグメント長の目標 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 継続性を保つための重なり |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | チャンクゲインを継承 | セグメント単位の正規化目標 |

### Model prefetch (optional)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Examples

### Generate and bind a device ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

次に、`IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` の `kDeviceId` を設定します。

ダッシュボード操作手順:

1. Settingsで登録/ログインします。
2. Accountパネルでデバイスを紐付けます。
3. 紐付け済みデバイスのみ、あなたのアカウントにストリーミングされます。

### REST ingest examples

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
    "photo_base64":"'"$(base64 -w0 sample.jpg)'"',
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

## 🧭 Development Notes

### Focus area

このリポジトリには複数のバックエンドトラックがあります。現時点でのコントリビューター向け指針と実行の主軸は、特に指定がない限り `backend/glass/` です。

### Static/syntax check

```bash
python -m compileall backend/glass/app.py
```

### Developer docs

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Note: In the current repository snapshot, some historical links above appear to have moved (for example, bridge notes now exist at `references/ideasglass_bridge.md`). The original links are preserved as canonical README content.

### Quick device binding (preserved workflow)

- Generate ID (in conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Set it in firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Run backend and open `http://localhost:8765`, register/login, then bind the device ID in the Account panel

## 🆘 Troubleshooting

- **Port already in use:** run backend on another port and update client settings.
- **Serial port busy:** `fuser -k /dev/ttyACM0`.
- **Linux serial permission denied:** `sudo usermod -aG dialout $USER` and re-login.
- **Postgres unavailable:** backend can run without DB for partial functionality; verify `DATABASE_URL` and restart.
- **Whisper performance issues:** use smaller models (`base`/`small`) or disable transcription via `IDEASGLASS_TRANSCRIBE=0`.
- **TLS/time sync instability on ESP32:** verify Wi-Fi, NTP availability (UDP/123), and cert/host settings; see `references/ideasglass_bridge.md` for detailed field notes.
- **No live waveform updates:** check backend logs and browser console for `[IdeasGlass][wave]` traces and confirm `/ws/stream` connectivity.

## 🌐 Ecosystem Links

| Brand | Purpose | Link |
|---|---|---|
| 🧠 EchoMind | 学習と制作のための多言語AIコンパニオン | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | 研究からプロダクト化へのコミュニティ | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | 小さな勝利を収益化する自動化 | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | 物理と化学のトラック・ノートブック | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | アイデアを下書き、タスク、投稿へ変換するエージェント | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | 収集、翻訳、ハイライト自動生成の統合 | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | 貢献とオンチェーン価値をつなぐ報酬・決済基盤 | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | 研究ノートやエッセイのノートブック | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | OnlyIdeas、EchoMind、LazyEdit、IdeasGlassを支えるスタジオ | [lazying.art](https://lazying.art) |

## 🙏 Acknowledgements

優れたオープンソースプロジェクトの上に成り立っています。感謝します。

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — クーポン `LazyingArt` を使うと10%割引（10件販売で30%コミッション開放）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Roadmap

- WAN/TLS環境を跨ぐエンドツーエンド音声ストリーミング経路の堅牢化と文書化を進めます。
- 文字起こし品質とレイテンシのトレードオフ（モデル/デバイス/閾値プリセット）を継続改善します。
- ダッシュボードでのデバイス管理とアカウント単位のマルチデバイス運用フローを拡張します。
- レガシー/並列バックエンド（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）を主要な `backend/glass` パスに整合・統合します。
- `i18n/` 配下の多言語READMEバリアントを維持・更新します。

## 🤝 Contribution

コントリビューションは歓迎です。リポジトリ固有のワークフローは `AGENTS.md` を参照してください。

PR提出前の推奨ローカル検証:

```bash
python -m compileall backend/glass/app.py
```

変更提出時:

- コミットメッセージは短く、実行動詞ベースで（現在形）。
- 挙動が環境変数に依存する場合は、関連変数（例: `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）をPRノートに記載します。
- テスト根拠（バックエンドログ、ダッシュボード挙動、ファームウェア出力）を添付します。
- 秘密情報（`DATABASE_URL`、APIトークン、資格情報ファイル）は決してコミットしないでください。

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License

このリポジトリのトップレベルには `LICENSE` ファイルが検出されていません。明示的なライセンスファイルが追加されるまで、利用・再配布はメンテナーの承認が必要とみなしてください。
