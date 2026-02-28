[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*아이디어를 행동, 수익, 그리고 창작의 추진력으로 바꾸는 웨어러블 AI 글래스.*

> 음성 우선 웨어러블 AI 파이프라인: ESP32 글래스에서 수집하고, FastAPI에서 처리하며, 실시간 PWA 대시보드로 모니터링/제어합니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>에코시스템</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>IdeasGlass 후원</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>앱 UI(왼쪽) · 하드웨어(오른쪽)</sub>
</div>

커뮤니티 실험은 <a href="https://onlyideas.art">onlyideas.art</a>에서 확인할 수 있습니다.

## 🚀 개요

IdeasGlass는 음성 기반 아이디어 캡처와 실행을 위한 AI-우선 웨어러블 시스템입니다. 이 저장소에서 주요 런타임 경로는 다음과 같습니다.

- FastAPI API, WebSocket ingest, Whisper 기반 전사, 설치형 PWA 대시보드: `backend/glass/`
- 텔레메트리/오디오/사진 스트리밍용 XIAO ESP32S3 펌웨어: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/`

이 저장소가 처음이라면 위 두 경로부터 확인하세요.

### 한눈에 보기

| 영역 | 주요 위치 | 역할 |
|---|---|---|
| Backend API + PWA | `backend/glass/` | FastAPI 엔드포인트, WebSocket ingest/fanout, 전사, 대시보드 |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 캡처/스트리밍 클라이언트 |
| Bridge notes | `references/ideasglass_bridge.md` | TLS/WAN 신뢰성 노트 및 배포 현장 팁 |
| README translations | `i18n/` | 정본 README와 동기화되는 다국어 문서 |

## ✨ IdeasGlass가 필요한 이유

IdeasGlass는 끊임없이 아이디어가 흐르는 사람들을 위해 만들어진 AI-우선 웨어러블입니다. 이동 중에 개념을 말로 설명하든 라이브 세션을 진행하든, 영감이 떠오르는 즉시 창의성을 캡처하고, 번역하고, 정리하고, 실행으로 연결합니다.

## 🧩 기능

### 제품 비전 기능

- **창작 네이티브 하드웨어**: 경량 글래스와 웨어러블 입력 장치, 음성 우선 캡처와 자연스러운 제스처 단축에 최적화.
- **즉시 번역**: 실시간 언어 감지/번역으로 도구 전환 없이 팀/청중 간 아이데이션 가능.
- **EchoMind 코파일럿**: `chat.lazying.art`와 긴밀히 연동되어 브레인스토밍, 스크립트 초안, 다국어 콘텐츠 코칭 지원.
- **채널 오토파일럿**: 개요, 롱폼 스크립트, 숏폼 훅을 자동으로 만들고 YouTube 등 채널 업로드 일정까지 관리.
- **하이라이트 & 릴스**: 핵심 순간 자동 선별, 썸네일/자막/소셜 업로드용 클립 생성.
- **수익 레이어**: LazyingArt Coin과 연결해 팁, 크레딧 정산, 온체인 자산 전환 지원.
- **지출 & 집중**: 운영 지출 추적, 수익성 높은 포맷 제시, 다음 프로젝트에 반영할 개인 강점 정리.

### 저장소/런타임 기능

- FastAPI 백엔드 REST + WebSocket 엔드포인트: ingest (`/api/v1/audio`, `/ws/audio-ingest`) 및 실시간 fanout (`/ws/stream`).
- 결정론적 오디오 세그먼트 분할(기본 약 15초 + 오버랩) 결과를 `backend/glass/audio_segments/`에 저장.
- 지연 임계값을 조정 가능한 openai-whisper 스트리밍 전사(선택 사항).
- 선택적 Postgres 영속화(`DATABASE_URL`): 메시지, 사진, 청크, 세그먼트, 전사 데이터 저장.
- 라이브 파형/전사 업데이트 및 데스크톱/모바일 설치를 지원하는 PWA 대시보드.
- XIAO ESP32S3 Sense 카메라 + 마이크 플로우용 Arduino 펌웨어 지원.

## 🔄 샘플 워크플로

1. **Capture**: 개념을 말하거나 스케치하면 IdeasGlass가 전사/번역 후 의도를 태깅합니다.
2. **Co-create**: EchoMind가 아이디어를 다듬고 스크립트를 작성하며 플랫폼별 CTA를 제안합니다.
3. **Publish**: 채널 에이전트가 하이라이트 영상, 갤러리 이미지 생성 후 메타데이터와 함께 업로드합니다.
4. **Monetize**: 크레딧이 LazyingArt Coin(`coin.lazying.art`)을 통해 흐르고 정산은 선호 지갑과 동기화됩니다.
5. **Reflect**: 지출/도달/참여 대시보드로 다음에 집중할 영역을 확인합니다.

## 🗂️ 프로젝트 구조

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

## 🧰 사전 요구사항

- Python 3.10+
- `pip` (또는 호환 Python이 있는 conda 환경)
- 선택 사항: 더 빠른 Whisper 추론을 위한 NVIDIA GPU + CUDA/cuDNN
- 선택 사항: 영속화를 위한 PostgreSQL
- 펌웨어용: Arduino IDE 또는 `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM 활성화

| 구성 요소 | 요구사항 | 참고 |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | venv 또는 conda(`glass`) 사용 |
| GPU acceleration (optional) | NVIDIA + CUDA/cuDNN | Whisper 지연 시간 개선 |
| Persistence (optional) | PostgreSQL | `DATABASE_URL`로 활성화 |
| Firmware toolchain | Arduino IDE / `arduino-cli` | PSRAM 활성화된 XIAO ESP32S3 프로필 사용 |

## ⚙️ 설치

### 백엔드 의존성

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 펌웨어 사전 준비

- `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h`를 `wifi_credentials.h`로 복사(권장)하고 SSID/비밀번호를 설정합니다.
- Arduino IDE에서 보드를 `ESP32 -> XIAO_ESP32S3`로 선택하고 `PSRAM: OPI PSRAM`을 사용합니다.
- 파티션 스킴: `Default with spiffs (3MB APP/1.5MB SPIFFS)` 또는 파일시스템이 불필요하면 `Maximum APP`.

## ▶️ 사용 방법

### 백엔드 실행 (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### 백엔드 실행 (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 대시보드 열기

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | 목적 |
|---|---|
| `/` | 메인 대시보드(PWA 지원 UI) |
| `/healthz` | 백엔드 생존 확인 |
| `/ws/audio-ingest` | 디바이스 ingest WebSocket |
| `/ws/stream` | 대시보드 클라이언트용 실시간 스트림 fanout |

### 로그인 및 디바이스 바인딩

1. 대시보드의 Settings/Account 영역에서 회원가입 또는 로그인합니다.
2. `Bind device` 필드에 디바이스 ID를 바인딩합니다.
3. 바인딩된 디바이스만 내 계정으로 스트리밍됩니다.

디바이스 ID + QR 이미지 생성:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

API로 바인딩(쿠키 세션 필요):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

현재 계정과 바인딩된 디바이스 확인:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

선택적 마이그레이션(기존 데이터를 새 디바이스 ID로 변경):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### 펌웨어 빌드/업로드 (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

포트가 점유 중이면: `fuser -k /dev/ttyACM0`.
권한 거부면: `sudo usermod -aG dialout $USER` 후 재로그인(또는 임시로 `sudo chmod a+rw /dev/ttyACM0`).

### 펌웨어 전원 UX (XIAO ESP32S3)

- 전원 인가 시 버튼을 약 0.8초 길게 눌러 부팅.
- 동작 중 약 2.5초 길게 눌러 딥슬립 진입.
- 동작 중 짧게 누르면 계속 캡처 트리거.

## 🛠️ 설정

### 핵심 환경 변수

- `DATABASE_URL`: 영구 저장용 선택적 Postgres DSN.
- `IDEASGLASS_WHISPER_MODEL`: `base`(기본), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` 또는 `cpu`.
- `IDEASGLASS_WHISPER_FP16`: GPU 혼합 정밀도 `1`, CPU 사용 시 `0`.
- `IDEASGLASS_TRANSCRIBE`: 전사 활성화 `1`(기본), 비활성화 `0`.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: 롤링 전사 간격.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: 쉼표 구분 임계값(기본 `3000,6000,15000`).

| Variable | Default / options | Effect |
|---|---|---|
| `DATABASE_URL` | 기본 unset | 계정/디바이스 데이터 Postgres 영속화 활성화 |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | 정확도와 지연 시간 균형 조절 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` or `cpu` | 추론 백엔드 |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | 혼합 정밀도 제어 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 전사 파이프라인 on/off |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | runtime configured | 롤링 전사 푸시 간격 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 단계적 전사 전송 임계값 |

안전한 `DATABASE_URL` 예시:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (peer/local auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (password auth)

### 오디오 게인 및 세그멘테이션 조정값

- `IDEASGLASS_GAIN_TARGET` (기본 `0.032`)
- `IDEASGLASS_GAIN_MAX` (기본 `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (기본 `0.008`)
- `IDEASGLASS_SPEECH_RMS` (기본 `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (기본 `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (기본 `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (기본 `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (기본적으로 chunk gain target 상속)

| Audio knob | Default | Purpose |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 목표 RMS 정규화 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 게인 증폭 상한 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 무음에 가까운 구간 과증폭 방지 하한 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 음성 활동 RMS 기준선 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 음성 임계값 주변 마진 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 세그먼트 목표 길이 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 연속성 확보용 세그먼트 오버랩 |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | inherits chunk gain | 세그먼트 레벨 정규화 목표 |

### 모델 사전 다운로드 (선택 사항)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 예시

### 디바이스 ID 생성 및 바인딩

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

그다음 아래 파일에서 `kDeviceId`를 설정하세요.

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

대시보드 흐름:

1. Settings에서 회원가입/로그인.
2. Account 패널에서 디바이스 바인딩.
3. 바인딩된 디바이스만 계정으로 스트리밍.

### REST ingest 예시

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

## 🧭 개발 노트

### 집중 영역

이 저장소에는 여러 백엔드 트랙이 함께 있습니다. 별도 요청이 없다면 현재 기여 가이드와 런타임의 중심 경로는 `backend/glass/`입니다.

### 정적/문법 검사

```bash
python -m compileall backend/glass/app.py
```

### 개발자 문서

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 참고: 현재 저장소 스냅샷에서는 위의 일부 과거 링크가 이동된 것으로 보입니다(예: bridge 노트는 현재 `references/ideasglass_bridge.md`에도 존재). 원문 README의 정본 내용을 보존하기 위해 기존 링크를 그대로 유지했습니다.

### 빠른 디바이스 바인딩 (기존 워크플로 보존)

- ID 생성(conda `glass`): `python backend/glass/tools/generate_device_id.py`
- 펌웨어에 설정: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- 백엔드를 실행하고 `http://localhost:8765`를 연 뒤 회원가입/로그인 후 Account 패널에서 디바이스 ID 바인딩

## 🆘 문제 해결

- **포트가 이미 사용 중**: 다른 포트로 백엔드를 실행하고 클라이언트 설정도 함께 변경하세요.
- **시리얼 포트 사용 중**: `fuser -k /dev/ttyACM0`.
- **Linux 시리얼 권한 거부**: `sudo usermod -aG dialout $USER` 실행 후 재로그인.
- **Postgres 사용 불가**: DB 없이도 일부 기능으로 백엔드 실행 가능. `DATABASE_URL` 확인 후 재시작하세요.
- **Whisper 성능 이슈**: 작은 모델(`base`/`small`)을 쓰거나 `IDEASGLASS_TRANSCRIBE=0`으로 전사를 끄세요.
- **ESP32 TLS/시간 동기화 불안정**: Wi-Fi, NTP(UDP/123), 인증서/호스트 설정을 확인하세요. 상세 현장 노트는 `references/ideasglass_bridge.md` 참고.
- **라이브 파형이 갱신되지 않음**: 백엔드 로그와 브라우저 콘솔의 `[IdeasGlass][wave]` 트레이스를 확인하고 `/ws/stream` 연결 상태를 점검하세요.

## 🌐 에코시스템 링크

🧠 **EchoMind** — 학습과 창작을 위한 다국어 AI 동반자.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 대담한 개념을 제품으로 연결하는 리서치-투-프로덕트 커뮤니티.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 작은 성과를 수익으로 전환하는 자동화.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 물리/화학 학습 트랙과 노트북.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 아이디어를 초안, 작업, 게시물로 전환하는 에이전트.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 아이디어를 캡처하고 번역해 하이라이트 릴스로 자동 제작.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 기여 보상과 정산을 온체인 가치와 연결.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 연구 노트와 에세이 아카이브.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas, EchoMind, LazyEdit, IdeasGlass를 만드는 스튜디오.  
[lazying.art](https://lazying.art)

## ❤️ 후원 및 문의

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- 여러분의 후원은 웨어러블, 에이전트, 에코시스템 로드맵을 지속적으로 전진시킵니다.

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

- 제휴 문의는 제목을 `IdeasGlass`로 하여 **contact@lazying.art**로 보내주세요.

IdeasGlass는 AI 웨어러블이 단순히 듣는 단계를 넘어, 함께 만드는 단계로 나아가는 지점입니다.

## 🙏 감사의 말

훌륭한 오픈소스 프로젝트들의 기반 위에서 발전하고 있습니다. 다음 프로젝트들에 감사드립니다.

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — 쿠폰 `LazyingArt` 사용 시 10% 할인 (10건 판매 후 30% 커미션 해제).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 로드맵

- WAN/TLS 환경 전반에서 엔드투엔드 오디오 스트리밍 경로를 강화하고 문서화.
- 전사 품질/지연 시간의 균형 개선(model/device/threshold 프리셋).
- 대시보드에서 디바이스 관리 및 계정 단위 멀티 디바이스 워크플로 확대.
- 레거시/병렬 백엔드 트랙(`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`)을 주 경로 `backend/glass`와 정렬 또는 통합.
- `i18n/` 아래 다국어 README 변형을 유지/갱신.

## 🤝 기여

기여를 환영합니다. 저장소별 워크플로 가이드는 `AGENTS.md`를 따르세요.

PR 전 권장 로컬 검증:

```bash
python -m compileall backend/glass/app.py
```

변경 제출 시:

- 커밋 제목은 짧고 행동 중심(현재형)으로 유지.
- 동작이 환경 변수에 의존하면 PR 노트에 관련 변수(예: `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`)를 명시.
- 테스트 근거(백엔드 로그, 대시보드 동작, 펌웨어 출력) 포함.
- 비밀정보(`DATABASE_URL`, API 토큰, credential 파일) 커밋 금지.

## 📄 라이선스

현재 저장소 스냅샷에서는 최상위 `LICENSE` 파일이 확인되지 않았습니다. 명시적 라이선스 파일이 추가되기 전까지는 사용 및 재배포 시 유지보수자 승인이 필요합니다.
