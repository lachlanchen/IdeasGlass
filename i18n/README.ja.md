[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*アイデアを行動・収益・創作の勢いへ変える、ウェアラブル AI グラス。*

> 音声ファーストのウェアラブル AI パイプライン: ESP32 グラスで取得し、FastAPI で処理し、ライブ PWA ダッシュボードで監視・制御します。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

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
      <b>IdeasGlass を支援</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>アプリ UI（左）・ハードウェア（右）</sub>
</div>

コミュニティ実験は <a href="https://onlyideas.art">onlyideas.art</a> で確認できます。

## 🚀 概要

IdeasGlass は、音声ファーストのアイデア取得と実行のために設計された AI ファーストのウェアラブルシステムです。本リポジトリにおける主要な実行経路は次のとおりです。

- `backend/glass/` : FastAPI API、WebSocket 取り込み、Whisper ベースの文字起こし、インストール可能な PWA ダッシュボード。
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` : テレメトリ/音声/写真をストリーミングする XIAO ESP32S3 ファームウェア。

このリポジトリが初めての場合は、まずここから確認してください。

### 一目でわかる構成

| 領域 | 主要パス | 役割 |
|---|---|---|
| バックエンド API + PWA | `backend/glass/` | FastAPI エンドポイント、WebSocket 取り込み/配信、文字起こし、ダッシュボード |
| ファームウェア | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 取得/ストリーミングクライアント |
| ブリッジノート | `references/ideasglass_bridge.md` | TLS/WAN 信頼性メモとデプロイ現場向けヒント |
| README 翻訳 | `i18n/` | 正本 README と同期された多言語ドキュメント |

## ✨ IdeasGlass を使う理由

IdeasGlass は、アイデアが次々に湧く人のために作られた AI ファーストのウェアラブルです。移動中にコンセプトを語るときも、ライブ配信を行うときも、ひらめいた瞬間に創造性を取得・翻訳・整理・実行へつなげます。

## 🧩 機能

### プロダクトビジョン機能

- **創作ネイティブなハードウェア** - 軽量グラスとウェアラブル入力により、音声中心の取得とさりげないジェスチャーショートカットを実現。
- **即時翻訳** - リアルタイム言語検出/翻訳により、ツールを切り替えずにチームや視聴者をまたいで発想可能。
- **EchoMind コパイロット** - `chat.lazying.art` と密に連携し、ブレインストーミング、台本下書き、多言語コンテンツ支援を提供。
- **チャンネル自動運転** - 構成案、長尺台本、短尺フックを作成し、YouTube などへの投稿スケジュールを自動化。
- **ハイライト＆リール** - 見どころを自動抽出し、サムネイル・字幕・SNS 用クリップを生成。
- **収益レイヤー** - LazyingArt Coin と接続し、投げ銭、クレジット支払い、オンチェーン資産への変換に対応。
- **支出と集中** - 運用コストを追跡し、利益につながる形式を可視化し、次プロジェクトの強みを抽出。

### リポジトリ/ランタイム機能

- FastAPI バックエンドによる REST + WebSocket エンドポイント（取り込み: `/api/v1/audio`, `/ws/audio-ingest`、ライブ配信: `/ws/stream`）。
- 決定論的な音声セグメンテーション（既定約 15 秒 + オーバーラップ）を `backend/glass/audio_segments/` に保存。
- 遅延しきい値を設定可能な openai-whisper ストリーミング文字起こし（任意）。
- Postgres 永続化（`DATABASE_URL`、メッセージ/写真/チャンク/セグメント/トランスクリプト）（任意）。
- デスクトップ/モバイルにインストール可能な PWA ダッシュボード（ライブ波形、文字起こし更新を表示）。
- XIAO ESP32S3 Sense のカメラ + マイクフローを対象とした Arduino ファームウェア対応。

## 🔄 サンプルワークフロー

1. **取得** - コンセプトを話す/スケッチすると、IdeasGlass が文字起こし・翻訳・意図タグ付けを実行。
2. **共創** - EchoMind がアイデアを洗練し、台本を下書きし、各プラットフォーム向け CTA を提案。
3. **公開** - チャンネルエージェントがハイライト動画、ギャラリー画像、メタデータ付きアップロードを自動生成。
4. **収益化** - クレジットは LazyingArt Coin（`coin.lazying.art`）経由で流れ、希望ウォレットへ支払いを同期。
5. **振り返り** - 支出・到達率・エンゲージメントのダッシュボードで次に伸ばすべき点を可視化。

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
- `pip`（または互換 Python の conda 環境）
- 任意: Whisper 推論高速化のための NVIDIA GPU + CUDA/cuDNN
- 任意: 永続化用 PostgreSQL
- ファームウェア向け: Arduino IDE または `arduino-cli`、Seeed XIAO ESP32S3 Sense、PSRAM 有効化

| コンポーネント | 要件 | メモ |
|---|---|---|
| バックエンド実行環境 | Python 3.10+, `pip` | venv または conda（`glass`）推奨 |
| GPU アクセラレーション（任意） | NVIDIA + CUDA/cuDNN | Whisper の遅延改善 |
| 永続化（任意） | PostgreSQL | `DATABASE_URL` で有効化 |
| ファームウェアツールチェーン | Arduino IDE / `arduino-cli` | PSRAM 有効の XIAO ESP32S3 プロファイルを使用 |

## ⚙️ インストール

### バックエンド依存関係

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ファームウェア前提条件

- `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` を `wifi_credentials.h` にコピー（推奨）し、SSID/パスワードを設定。
- Arduino IDE では `ESP32 -> XIAO_ESP32S3`、`PSRAM: OPI PSRAM` を使用。
- パーティションスキーム: `Default with spiffs (3MB APP/1.5MB SPIFFS)`、またはファイルシステム不要時は `Maximum APP`。

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
| `/` | メインダッシュボード（PWA 対応 UI） |
| `/healthz` | バックエンド生存確認 |
| `/ws/audio-ingest` | デバイス取り込み WebSocket |
| `/ws/stream` | ダッシュボードクライアントへのライブ配信 |

### ログインしてデバイスを紐付ける

1. ダッシュボードの Settings/Account から登録またはログイン。
2. `Bind device` フィールドにデバイス ID を設定。
3. 紐付け済みデバイスのみ、あなたのアカウントへストリームされます。

デバイス ID + QR 画像を生成:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

API から紐付け（cookie セッション必須）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

現在のアカウントと紐付けデバイスを確認:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

任意の移行（過去データを新しいデバイス ID へ改名）:

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### ファームウェアのビルド/書き込み（Arduino CLI）

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

ポート使用中: `fuser -k /dev/ttyACM0`。  
権限エラー: `sudo usermod -aG dialout $USER` 後に再ログイン（または一時的に `sudo chmod a+rw /dev/ttyACM0`）。

### ファームウェア電源 UX（XIAO ESP32S3）

- 電源投入時にボタンを約 0.8 秒長押しして起動。
- 動作中に約 2.5 秒長押しでディープスリープへ移行。
- 動作中の短押しは引き続きキャプチャをトリガー。

## 🛠️ 設定

### 主要な環境変数

- `DATABASE_URL`: 永続ストレージ向け Postgres DSN（任意）。
- `IDEASGLASS_WHISPER_MODEL`: `base`（既定）、`small`、`medium`、`large-v3`、`large-v3-turbo`。
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` または `cpu`。
- `IDEASGLASS_WHISPER_FP16`: GPU 混合精度 `1`、CPU では `0`。
- `IDEASGLASS_TRANSCRIBE`: 文字起こし有効 `1`（既定）、無効 `0`。
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: ローリング文字起こし間隔。
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: カンマ区切りしきい値（既定 `3000,6000,15000`）。

| 変数 | 既定値 / 選択肢 | 効果 |
|---|---|---|
| `DATABASE_URL` | 既定は未設定 | アカウント/デバイスデータの Postgres 永続化を有効化 |
| `IDEASGLASS_WHISPER_MODEL` | `base`（`small`, `medium`, `large-v3`, `large-v3-turbo`） | 精度と遅延のバランスを制御 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` または `cpu` | 推論バックエンド |
| `IDEASGLASS_WHISPER_FP16` | GPU `1`、CPU 安全 `0` | 混合精度制御 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 文字起こしパイプラインの有効/無効 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 実行時設定 | ローリング文字起こし配信間隔 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 段階的文字起こし出力しきい値 |

安全な `DATABASE_URL` 例:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"`（peer/local 認証）
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"`（パスワード認証）

### 音声ゲインとセグメンテーション調整

- `IDEASGLASS_GAIN_TARGET`（既定 `0.032`）
- `IDEASGLASS_GAIN_MAX`（既定 `1.8`）
- `IDEASGLASS_GAIN_MIN_RMS`（既定 `0.008`）
- `IDEASGLASS_SPEECH_RMS`（既定 `0.03`）
- `IDEASGLASS_SPEECH_MARGIN`（既定 `0.005`）
- `IDEASGLASS_SEGMENT_TARGET_MS`（既定 `15000`）
- `IDEASGLASS_SEGMENT_OVERLAP_MS`（既定 `2000`）
- `IDEASGLASS_SEGMENT_GAIN_TARGET`（既定はチャンク側ゲイン目標を継承）

| 音声ノブ | 既定値 | 目的 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | RMS 正規化の目標値 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | ゲイン増幅の上限クランプ |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 無音近傍の過増幅を防ぐ下限 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 音声活動判定の RMS 基準 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 音声しきい値周辺のマージン |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | セグメント長の目標 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 連続性確保のための重なり |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | チャンクゲインを継承 | セグメント単位の正規化目標 |

### モデル事前取得（任意）

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 例

### デバイス ID を生成して紐付け

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

続いて `kDeviceId` を次に設定:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

ダッシュボード手順:

1. Settings で登録/ログイン。
2. Account パネルでデバイスを紐付け。
3. 紐付け済みデバイスのみ、あなたのアカウントへストリーム。

### REST 取り込み例

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

## 🧭 開発ノート

### 注力領域

このリポジトリには複数のバックエンド系統があります。特に指定がない限り、現在のコントリビューター向けガイダンスと実行対象は `backend/glass/` です。

### 静的/構文チェック

```bash
python -m compileall backend/glass/app.py
```

### 開発者向けドキュメント

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 注: 現在のリポジトリスナップショットでは、上記の履歴的リンクの一部が移動しているようです（例: ブリッジノートは現在 `references/ideasglass_bridge.md` に存在）。元のリンクは正本 README の内容として保持しています。

### デバイスのクイック紐付け（保持されたワークフロー）

- ID 生成（conda `glass`）: `python backend/glass/tools/generate_device_id.py`
- ファームウェアへ設定: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`（`kDeviceId`）
- バックエンドを起動して `http://localhost:8765` を開き、登録/ログイン後、Account パネルでデバイス ID を紐付け

## 🆘 トラブルシューティング

- **ポート使用中:** 別ポートでバックエンドを起動し、クライアント設定も更新。
- **シリアルポート使用中:** `fuser -k /dev/ttyACM0`。
- **Linux でシリアル権限拒否:** `sudo usermod -aG dialout $USER` 実行後に再ログイン。
- **Postgres 未接続:** DB なしでも一部機能で起動可能。`DATABASE_URL` を確認して再起動。
- **Whisper 性能問題:** 小さいモデル（`base`/`small`）を使うか、`IDEASGLASS_TRANSCRIBE=0` で文字起こしを無効化。
- **ESP32 で TLS/時刻同期が不安定:** Wi-Fi、NTP（UDP/123）、証明書/ホスト設定を確認。詳細は `references/ideasglass_bridge.md`。
- **ライブ波形が更新されない:** バックエンドログとブラウザコンソールの `[IdeasGlass][wave]` を確認し、`/ws/stream` 接続を検証。

## 🌐 エコシステムリンク

🧠 **EchoMind** — 学習と創作のための多言語 AI コンパニオン。  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 大胆なコンセプトを育てるリサーチ to プロダクトのコミュニティ。  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 小さな成果を収益化する自動化。  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 物理・化学の学習トラックとノート。  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — アイデアを下書き・タスク・投稿に変えるエージェント。  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 取得・翻訳・ハイライト自動制作を行うウェアラブル。  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 貢献に対する報酬と支払いをオンチェーン価値へ接続。  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 研究ノートとエッセイのノートブック。  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas、EchoMind、LazyEdit、IdeasGlass を運営するスタジオ。  
[lazying.art](https://lazying.art)

## ❤️ 支援と連絡先

- あなたの支援は IdeasGlass のハードウェア試作と運用を加速し、より多くのクリエイターへの還元につながります。
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

- 提携に関する連絡先: 件名を `IdeasGlass` にして **contact@lazying.art** へメールしてください。

IdeasGlass は、AI ウェアラブルが「聞くだけ」から「あなたと一緒に作る」へ進化する場所です。

## 🙏 謝辞

偉大なオープンプロジェクトの成果に支えられています。感謝します。

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — クーポン `LazyingArt` で 10% オフ（10 件販売後に 30% コミッションが有効化）。

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ ロードマップ

- WAN/TLS 環境をまたぐエンドツーエンド音声ストリーミング経路を強化し、文書化を拡充。
- 文字起こし品質と遅延のトレードオフを継続改善（model/device/threshold プリセット）。
- ダッシュボードでのデバイス管理と、アカウント単位の複数デバイス運用フローを拡張。
- レガシー/並行バックエンド系統（`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`）を主要な `backend/glass` 経路へ整合・統合。
- `i18n/` 配下の多言語 README を保守・更新。

## 🤝 コントリビューション

コントリビューションを歓迎します。リポジトリ固有のワークフローガイドは `AGENTS.md` を参照してください。

PR 作成前の推奨ローカル検証:

```bash
python -m compileall backend/glass/app.py
```

変更提出時のポイント:

- コミット件名は短く、行動中心（現在形）で。
- 振る舞いが環境変数に依存する場合、PR ノートに関連変数（例: `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`）を記載。
- テスト証跡（バックエンドログ、ダッシュボード挙動、ファームウェア出力）を添付。
- 秘密情報（`DATABASE_URL`、API トークン、認証ファイル）は絶対にコミットしない。

## 📄 ライセンス

このリポジトリの現在のスナップショットでは、トップレベル `LICENSE` ファイルは検出されませんでした。明示的なライセンスファイルが追加されるまで、利用および再配布にはメンテナー承認が必要として扱ってください。
