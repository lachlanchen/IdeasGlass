[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*アイデアを行動・収益・創造の勢いへと変えるウェアラブルAIグラス。*

> 音声ファーストのウェアラブルAIパイプライン。ESP32グラスから収録し、FastAPIで処理し、ライブPWAダッシュボードで監視・操作します。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| レーン | 用途 |
|---|---|
| 🎙️ ウェアラブル収集 | ESP32グラスが音声・写真・テレメトリをほぼリアルタイムで送信 |
| 🧠 バックエンドの知能 | FastAPIがストリームを受け取り、文字起こしし、セグメント化し、メタデータを保存 |
| 🖥️ ダッシュボード | PWAでライブ波形、文字起こし、デバイス/アカウント状態を表示 |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>エコシステム</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>IdeasGlassを支援</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>アプリUI（左）· ハードウェア（右）</sub>
</div>

コミュニティ実験は <a href="https://onlyideas.art">onlyideas.art</a> でご覧ください。

## 🚀 概要

IdeasGlassは、音声ファーストでアイデアをキャプチャし実行へつなぐAIファーストのウェアラブルです。本リポジトリの主要なランタイム経路は次のとおりです。

- `backend/glass/`：FastAPI API、WebSocket取り込み、Whisperベースの文字起こし、インストール可能なPWAダッシュボード。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`：XIAO ESP32S3 ファームウェア（テレメトリ/音声/写真）をストリーミング。

このリポジトリが初めての方は、まずここから始めてください。

### ひと目で把握

| エリア | 主な場所 | 機能 |
|---|---|---|
| バックエンドAPI + PWA | `backend/glass/` | FastAPIエンドポイント、WebSocket取り込み/配信、文字起こし、ダッシュボード |
| ファームウェア | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32キャプチャ/ストリーミングクライアント |
| ブリッジノート | `references/ideasglass_bridge.md` | TLS/WAN信頼性メモとデプロイ時の現場ノウハウ |
| README翻訳 | `i18n/` | 正本READMEから同期される多言語ドキュメント |

## ✨ IdeasGlassの意義

IdeasGlassは、アイデアが絶えず湧く人向けのAIファーストウェアラブルです。移動中にコンセプトを話しているときでも、ライブ配信をしているときでも、ひらめいた瞬間にクリエイティブを文字起こし・翻訳・整理・実行までつなげます。

## 🧩 機能

### 製品ビジョン機能

- **制作ネイティブなハードウェア** – 軽量なグラスとウェアラブル入力を採用し、音声ファースト収集と微細なジェスチャーショートカット向けに最適化。
- **即時翻訳** – リアルタイムの言語検出・翻訳により、ツールを切り替えることなく、チームや視聴者を跨いだアイデア発想が可能。
- **EchoMindコパイロット** – `chat.lazying.art` と緊密に連携し、ブレインストーミング、台本作成、マルチリンガル・コンテンツコーチングを支援。
- **チャンネル自動運転** – アウトライン、長尺台本、短尺フックを下書きし、YouTubeなどへアップロードをスケジュール。
- **ハイライト＆リール** – 重要シーンを自動選別し、サムネイル・字幕・SNS配信用クリップを生成。
- **収益層** – LazyingArt Coinと接続して、投げ銭、クレジット支払い、オンチェーン資産への変換を実現。
- **支出と集中力** – 運用コストを追跡し、収益性の高いフォーマットを可視化し、次のプロジェクト候補を強みベースで抽出。

### リポジトリ/ランタイム機能

- FastAPIバックエンド（REST + WebSocket）で取り込み（`/api/v1/audio`, `/ws/audio-ingest`）とライブストリーム配信（`/ws/stream`）を提供。
- 決定論的な音声セグメント化（デフォルト約15秒、オーバーラップ付き）を `backend/glass/audio_segments/` に保存。
- オプションの openai-whisper ストリーミング文字起こし（レイテンシ閾値を設定可能）。
- オプションのPostgreSQL永続化（`DATABASE_URL`）によるメッセージ、写真、チャンク、セグメント、文字起こしの保存。
- ライブ波形、文字起こし更新、デスクトップ/モバイル向けインストール対応を備えたPWAダッシュボード。
- XIAO ESP32S3 Sense のカメラ + マイクフロー向け Arduino ファームウェア対応。

## 🔄 サンプルワークフロー

1. **キャプチャ** – コンセプトを話す、または描写する。IdeasGlassが文字起こし・翻訳・意図タグ付けを実行。
2. **共創** – EchoMindがアイデアを洗練し、台本を作成し、プラットフォーム別のCTAを提案。
3. **公開** – チャンネルエージェントがハイライト動画やギャラリー画像を自動生成し、メタデータ付きでアップロード。
4. **収益化** – クレジットはLazyingArt Coin（`coin.lazying.art`）を経由し、希望のウォレットへ支払いが同期されます。
5. **振り返り** – 支出、リーチ、エンゲージメントのダッシュボードから次に注力すべき施策を抽出。

## 🗂️ プロジェクト構成

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

## 🧰 前提条件

- Python 3.10+
- `pip`（または互換Pythonを持つconda環境）
- 任意: Whisper推論を高速化するNVIDIA GPU + CUDA/cuDNN
- 任意: PostgreSQL（永続化）
- ファームウェア: Arduino IDEまたは `arduino-cli`、Seeed XIAO ESP32S3 Sense、PSRAM有効化

| コンポーネント | 要件 | メモ |
|---|---|---|
| バックエンド実行環境 | Python 3.10+, `pip` | venvまたはconda（`glass`） |
| GPU加速（任意） | NVIDIA + CUDA/cuDNN | Whisper推論のレイテンシ改善 |
| 永続化（任意） | PostgreSQL | `DATABASE_URL` で有効化 |
| ファームウェアツールチェーン | Arduino IDE / `arduino-cli` | PSRAM有効のXIAO ESP32S3プロファイルを使用 |

## ⚙️ インストール

### バックエンド依存関係

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ファームウェアの前提条件

- `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` を（推奨）`wifi_credentials.h` にコピーし、SSID/パスワードを設定。
- Arduino IDE ではボードを `ESP32 -> XIAO_ESP32S3`、`PSRAM: OPI PSRAM` に設定。
- パーティション構成: `Default with spiffs (3MB APP/1.5MB SPIFFS)` または、ファイルシステムが不要なら `Maximum APP`。

## ▶️ 使い方

### バックエンド起動（uvicorn）

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### バックエンド起動（ヘルパー）

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### ダッシュボードを開く

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| エンドポイント | 目的 |
|---|---|
| `/` | メインダッシュボード（PWA対応UI） |
| `/healthz` | バックエンド死活監視 |
| `/ws/audio-ingest` | デバイス取り込みWebSocket |
| `/ws/stream` | ダッシュボードクライアントへのライブ配信 |

### ログインしてデバイスを紐付ける

1. ダッシュボードの Settings/Account から登録またはログインします。
2. `Bind device` 欄にデバイスIDを入力します。
3. 紐付け済みデバイスのみ、あなたのアカウントへストリーミングされます。

デバイスIDとQR画像の生成:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

APIでの紐付け（cookieセッションが必要）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

現在のアカウントと紐付けデバイスの確認:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

過去データを新デバイスIDに移行する（任意）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### ファームウェアのビルド/アップロード（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

ポートが使用中: `fuser -k /dev/ttyACM0`。
権限エラー時: `sudo usermod -aG dialout $USER` を実行し再ログイン（または一時的に `sudo chmod a+rw /dev/ttyACM0`）。

### ファームウェア電源UX（XIAO ESP32S3）

- 起動時は約0.8秒長押しして起動。
- 動作中に約2.5秒長押しでディープスリープへ。
- 動作中の短押しは引き続きキャプチャを開始。

## 🛠️ 設定

### 主な環境変数

- `DATABASE_URL`: 永続化用Postgres DSN（任意）。
- `IDEASGLASS_WHISPER_MODEL`: `base`（既定）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` または `cpu`。
- `IDEASGLASS_WHISPER_FP16`: GPUでは `1`、CPUでは `0`。
- `IDEASGLASS_TRANSCRIBE`: 文字起こしを有効化する場合 `1`（既定）、無効化する場合 `0`。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: ローリング文字起こし間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: カンマ区切りの閾値（既定 `3000,6000,15000`）。

| 変数 | 既定値 / 選択肢 | 効果 |
|---|---|---|
| `DATABASE_URL` | 既定未設定 | アカウント/デバイス情報のPostgres永続化を有効化 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（`small`、`medium`、`large-v3`、`large-v3-turbo`） | 精度とレイテンシのトレードオフを制御 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` または `cpu` | 推論バックエンド |
| `IDEASGLASS_WHISPER_FP16` | `1`（GPU）/`0`（CPUセーフ） | 混合精度制御 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 文字起こしパイプラインを切替 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 実行時設定 | ローリング文字起こし送信間隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 段階的文字起こし通知の閾値 |

安全な `DATABASE_URL` の例:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local認証）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（パスワード認証）

### 音声ゲインとセグメント分割の調整

- `IDEASGLASS_GAIN_TARGET`（既定 `0.032`）
- `IDEASGLASS_GAIN_MAX`（既定 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（既定 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（既定 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（既定 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（既定 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（既定 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（既定はチャンクのゲイン目標を継承）

| 音声調整項目 | 既定値 | 用途 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | RMS 正規化の目標 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | ゲイン増幅の上限クリップ |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 無音に近い領域の過増幅を防止 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 音声活動判定のRMS基準 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 音声しきい値の余裕 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | セグメント長の目標 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 連続性を保つための重なり |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | チャンクゲインを継承 | セグメント単位の正規化目標 |

### モデル事前取得（任意）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 例

### デバイスIDの生成と紐付け

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

次に `kDeviceId` を以下に設定します。

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

ダッシュボード手順:

1. Settingsで登録/ログインします。
2. Accountパネルでデバイスを紐付けます。
3. 紐付け済みデバイスのみ、あなたのアカウントにストリーミングされます。

### REST取り込み例

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

## 🧭 開発メモ

### 注力領域

このリポジトリには複数のバックエンドトラックがあります。現時点でのコントリビューター向けガイダンスと実行の主軸は、別途指定がない限り `backend/glass/` です。

### 静的/構文チェック

```bash
python -m compileall backend/glass/app.py
```

### 開発者向けドキュメント

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 注: 現在のリポジトリスナップショットでは、上記の一部リンクが移動している可能性があります（例: ブリッジノートは現在 `references/ideasglass_bridge.md` にあります）。元リンクは正本READMEの内容として保持しています。

### クイックデバイス紐付け（保存済みワークフロー）

- ID生成（conda `glass`）: `python backend/glass/tools/generate_device_id.py`
- ファームウェア側へ設定: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- バックエンド起動後、`http://localhost:8765` を開き、登録/ログインしてからAccountパネルでデバイスIDを紐付け

## 🆘 トラブルシューティング

- **ポートが既に使用中:** バックエンドを別ポートで起動し、クライアント設定も更新してください。
- **シリアルポートが使用中:** `fuser -k /dev/ttyACM0`。
- **Linuxでシリアル権限拒否:** `sudo usermod -aG dialout $USER` で再ログイン。
- **Postgresが利用不可:** DBなしでも一部機能は動作します。`DATABASE_URL` を確認して再起動。
- **Whisper性能の問題:** 小さいモデル（`base`/`small`）を使用するか、`IDEASGLASS_TRANSCRIBE=0` で文字起こしを無効化。
- **ESP32のTLS/時刻同期の不安定:** Wi-Fi、NTP（UDP/123）、証明書/ホスト設定を確認。詳細は `references/ideasglass_bridge.md`。
- **ライブ波形更新なし:** バックエンドログとブラウザコンソールの `[IdeasGlass][wave]` トレースを確認し、`/ws/stream` 接続を検証。

## 🌐 エコシステムリンク

🧠 **EchoMind** — 学習と制作のための多言語AIコンパニオン。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 研究からプロダクト化へつなぐコミュニティ。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 小さな成果を収益化するための自動化。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理・化学のトラックやノート。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — アイデアを下書き・タスク・投稿へ変換するエージェント。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 収集・翻訳・ハイライト自動生成を行うウェアラブル。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 貢献とオンチェーン価値を橋渡しする報酬・支払基盤。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究ノートとエッセイのノートブック。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas、EchoMind、LazyEdit、IdeasGlassを支えるスタジオ。  
[lazying.art](https://lazying.art)

## 🙏 謝辞

優れたオープンソースプロジェクトの成果の上に成り立っています。以下に感謝します。

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **紹介プログラム** — クーポン `LazyingArt` を使うと10%割引（10件販売で30%コミッション解放）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ ロードマップ

- WAN/TLS環境にまたがるエンドツーエンドの音声ストリーミング経路を強化し、文書化を進める。
- 文字起こし品質とレイテンシのトレードオフ（モデル/デバイス/閾値プリセット）を継続改善。
- ダッシュボード上のデバイス管理とアカウント単位のマルチデバイス運用フローを拡張。
- レガシー/並行バックエンド（`tornado_app`、`memo`、`memo_legacy`、`ngrok_bridge`）を主要 `backend/glass` パスへ調整・統合。
- `i18n/` 配下の多言語README変種を維持・更新。

## 🤝 コントリビューション

コントリビューション歓迎。リポジトリ固有のワークフローは `AGENTS.md` を参照してください。

PR提出前の推奨ローカル検証:

```bash
python -m compileall backend/glass/app.py
```

変更提出時:

- コミット文は短く行動ベース（現在形）で。
- 振る舞いが環境変数に依存する場合、関連変数（例: `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）をPRノートに記載。
- テスト根拠（バックエンドログ、ダッシュボード挙動、ファームウェア出力）を添付。
- 秘密情報（`DATABASE_URL`、APIトークン、認証ファイル）は決してコミットしない。

## 📄 ライセンス

このリポジトリのトップレベルには `LICENSE` が検出されていません。明示的なライセンスファイルが追加されるまで、利用・再配布はメンテナ承認が必要であるものとして扱ってください。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
