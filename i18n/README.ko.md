[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)


# IdeasGlass

*아이디어를 행동, 수익, 창작 모멘텀으로 바꾸는 웨어러블 AI 글래스.*

> 음성 우선 웨어러블 AI 파이프라인: ESP32 글래스로 캡처하고, FastAPI에서 처리한 뒤, 실시간 PWA 대시보드로 모니터링/제어합니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| 구분 | 목적 |
|---|---|
| 🎙️ 웨어러블 캡처 | ESP32 글래스가 오디오, 사진, 텔레메트리를 거의 실시간으로 전송 |
| 🧠 백엔드 인텔리전스 | FastAPI가 스트림을 수신해 전사, 세그먼트화, 메타데이터 저장 |
| 🖥️ 대시보드 | PWA에서 실시간 파형, 전사 텍스트, 디바이스/계정 상태 표시 |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>앱 UI (왼쪽) · 하드웨어 (오른쪽)</sub>
</div>

<a href="https://onlyideas.art">onlyideas.art</a>에서 커뮤니티 실험을 살펴보세요.

## 🚀 개요

IdeasGlass는 아이디어를 음성으로 빠르게 캡처하고 실행할 수 있도록 설계된 AI 우선 웨어러블 시스템입니다. 이 저장소의 핵심 런타임 경로는 다음과 같습니다.

- `backend/glass/` — FastAPI API, WebSocket 수집, Whisper 기반 전사, 설치 가능한 PWA 대시보드.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` — 텔레메트리/오디오/사진을 실시간으로 스트리밍하는 XIAO ESP32S3 펌웨어.

이 저장소가 처음이라면 위 항목부터 확인하세요.

### 한눈에 보기

| 영역 | 주요 위치 | 역할 |
|---|---|---|
| 백엔드 API + PWA | `backend/glass/` | FastAPI 엔드포인트, WebSocket 수집/전파, 전사, 대시보드 |
| 펌웨어 | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | ESP32 캡처/스트리밍 클라이언트 |
| 브리지 노트 | `references/ideasglass_bridge.md` | TLS/WAN 안정성 및 배포 현장 가이드 |
| README 번역 | `i18n/` | 정식 README를 기반으로 동기화된 다국어 문서 |

## ✨ IdeasGlass가 필요한 이유

IdeasGlass는 떠오르는 아이디어 속에서 살아가는 사람들을 위한 AI 중심 웨어러블입니다. 동작 중에 개념을 말로 설명하든, 라이브 세션에서 구상하든 아이디어가 떠오르는 즉시 창의력을 캡처하고 번역·정리·실행합니다.

## 🧩 기능

### 제품 비전 기능

- **창작 친화형 하드웨어** — 경량 글래스와 착용형 입력 장치로, 음성 우선 캡처와 미세한 제스처 단축키에 맞게 최적화.
- **즉시 번역** — 실시간 언어 감지/번역으로 도구를 바꾸지 않고도 팀이나 청중 간에 아이디어를 공유.
- **EchoMind 코-파일럿** — `chat.lazying.art`와 긴밀히 연동되어 브레인스토밍, 대본 초안 작성, 다국어 콘텐츠 코칭을 지원.
- **채널 자동 조종** — 아웃라인, 장문 스크립트, 쇼츠 훅(hook), 업로드 일정까지 자동으로 생성해 YouTube 등 채널에 배포.
- **하이라이트 및 릴스 제작** — 핵심 장면을 자동 선택해 썸네일, 자막, 소셜 게시용 클립을 생성.
- **수익화 계층** — LazyingArt Coin을 통해 후원, 크레딧 정산, 온체인 자산 전환을 연결.
- **지출·집중 분석** — 운영비를 추적하고 수익성이 높은 포맷을 강조하며, 다음 프로젝트를 위한 강점을 정리.

### 저장소/런타임 기능

- FastAPI 백엔드는 REST + WebSocket 엔드포인트(`/api/v1/audio`, `/ws/audio-ingest`)로 수집하고, 실시간 스트림 팬아웃(`/ws/stream`)을 제공합니다.
- 오디오를 결정론적으로 세그먼트화(기본 ~15초, overlap 적용)하여 `backend/glass/audio_segments/`에 저장.
- 선택적으로 openai-whisper 스트리밍 전사를 사용하며 지연 임계값을 조정 가능.
- 선택적으로 Postgres 영속성(`DATABASE_URL`)을 사용해 메시지·사진·청크·세그먼트·전사 데이터를 저장.
- 실시간 파형, 전사 갱신, 데스크톱/모바일 설치 가능한 PWA 대시보드.
- XIAO ESP32S3 Sense 카메라 + 마이크 플로우를 지원하는 Arduino 펌웨어.

## 🔄 샘플 워크플로우

1. **캡처** — 아이디어를 말하거나 스케치합니다. IdeasGlass가 즉시 전사·번역·의도 태깅.
2. **공동 창작** — EchoMind가 아이디어를 다듬고 대본을 초안화하며 플랫폼별 CTA를 제안.
3. **발행** — 채널 에이전트가 하이라이트 영상, 갤러리 이미지 등을 자동 제작해 메타데이터와 함께 업로드.
4. **수익화** — 크레딧이 LazyingArt Coin(`coin.lazying.art`)으로 연결되고, 지급은 선호 지갑과 동기화.
5. **회고** — 지출, 도달 범위, 참여도 대시보드를 통해 다음 액션을 결정.

## 🗂️ 프로젝트 구조

```text
IdeasGlass/
├── README.md
├── i18n/                                  # README 번역
├── backend/
│   ├── glass/                             # Primary FastAPI + PWA 백엔드
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # 보조/병렬 ingest 백엔드 경로
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # 브리지 및 배포 참고사항
├── docs/                                  # 추가 사이트/문서 자산
├── development_plan/
├── app/
├── ops/observability/
├── figs/
└── seeed_studio_xiao_esp32s3_dev/
```

## 🧰 사전 요구사항

- Python 3.10+
- `pip` (또는 호환 가능한 Python이 설치된 conda 환경)
- 선택 사항: 빠른 Whisper 추론을 위한 NVIDIA GPU + CUDA/cuDNN
- 선택 사항: 영속성 저장용 PostgreSQL
- 펌웨어: Arduino IDE 또는 `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM 활성화

| 구성 요소 | 요구사항 | 비고 |
|---|---|---|
| 백엔드 런타임 | Python 3.10+, `pip` | venv 또는 conda(`glass`) 사용 |
| GPU 가속 (선택) | NVIDIA + CUDA/cuDNN | Whisper 지연 시간 개선 |
| 영속성 (선택) | PostgreSQL | `DATABASE_URL`로 활성화 |
| 펌웨어 툴체인 | Arduino IDE / `arduino-cli` | XIAO ESP32S3 프로파일 사용 및 PSRAM 활성화 |

## ⚙️ 설치

### 백엔드 종속성

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 펌웨어 사전 조건

- `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h`을 `wifi_credentials.h`로 복사(권장) 후 SSID/비밀번호를 설정합니다.
- Arduino IDE에서 보드를 `ESP32 -> XIAO_ESP32S3`로 설정하고 `PSRAM: OPI PSRAM`을 선택합니다.
- 파티션 스키마: `Default with spiffs (3MB APP/1.5MB SPIFFS)` 또는 파일시스템이 필요 없으면 `Maximum APP`.

## ▶️ 사용법

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

### 백엔드 실행 (헬퍼)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### 대시보드 실행

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| 엔드포인트 | 용도 |
|---|---|
| `/` | 메인 대시보드 (PWA 지원 UI) |
| `/healthz` | 백엔드 정상 동작 확인 |
| `/ws/audio-ingest` | 디바이스 수집 WebSocket |
| `/ws/stream` | 대시보드 클라이언트 실시간 스트림 팬아웃 |

### 로그인 및 디바이스 바인딩

1. 대시보드의 Settings/Account 영역에서 회원가입 또는 로그인.
2. `Bind device` 필드에 디바이스 ID 입력.
3. 바인딩된 디바이스만 계정에 스트림을 전송.

디바이스 ID + QR 이미지를 생성합니다.

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

기존 데이터를 새 디바이스 ID로 이동(선택):

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

포트가 점유 중인 경우: `fuser -k /dev/ttyACM0`.
권한 부족 시: `sudo usermod -aG dialout $USER` 후 재로그인(또는 임시로 `sudo chmod a+rw /dev/ttyACM0`).

### 펌웨어 전원 UX (XIAO ESP32S3)

- 전원 인가 후 약 0.8초 동안 버튼을 눌러 부팅.
- 동작 중 약 2.5초 동안 눌러 두어 절전 모드 진입.
- 동작 중 짧게 한 번 누르면 계속 캡처 동작.

## 🛠️ 설정

### 핵심 환경 변수

- `DATABASE_URL`: 메시지 영속성용 선택적 Postgres DSN.
- `IDEASGLASS_WHISPER_MODEL`: `base`(기본), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` 또는 `cpu`.
- `IDEASGLASS_WHISPER_FP16`: GPU 혼합 정밀도 `1`, CPU용 `0`.
- `IDEASGLASS_TRANSCRIBE`: 전사 활성화 `1`(기본), 비활성화 `0`.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: 롤링 전사 업데이트 간격.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: 쉼표 구분 임계값(기본 `3000,6000,15000`).

| 변수 | 기본값/옵션 | 효과 |
|---|---|---|
| `DATABASE_URL` | 기본 미설정 | 계정/디바이스 데이터 영속성을 위해 Postgres 활성화 |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | 정확도와 지연의 균형을 조절 |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` 또는 `cpu` | 추론 백엔드 |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | 혼합 정밀도 제어 |
| `IDEASGLASS_TRANSCRIBE` | `1` | 전사 파이프라인 토글 |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | 런타임 설정값 | 롤링 전사 푸시 간격 |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | 단계적 전사 발행 임계값 |

안전한 `DATABASE_URL` 예시:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (peer/local 인증)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (비밀번호 인증)

### 오디오 이득 및 세그먼트 조절

- `IDEASGLASS_GAIN_TARGET` (기본 `0.032`)
- `IDEASGLASS_GAIN_MAX` (기본 `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (기본 `0.008`)
- `IDEASGLASS_SPEECH_RMS` (기본 `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (기본 `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (기본 `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (기본 `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (청크 이득값 기본값 사용)

| 오디오 조절 항목 | 기본값 | 용도 |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | 목표 RMS 정규화 |
| `IDEASGLASS_GAIN_MAX` | `1.8` | 이득 증폭 상한치 |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | 거의 무음 구간 과증폭 방지 하한 |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | 음성 활동 RMS 기준선 |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | 음성 임계값 여유 구간 |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | 세그먼트 목표 길이 |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | 연속성 유지를 위한 세그먼트 overlap |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | 청크 이득값 상속 | 세그먼트 단위 정규화 목표 |

### 모델 프리패치 (선택)

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

다음 항목의 `kDeviceId`를 설정합니다.

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

## 🧭 개발 노트

### 집중 영역

이 저장소에는 여러 백엔드 트랙이 존재합니다. 현재 기여 가이드 및 런타임 초점은 별도 요청이 없는 한 `backend/glass/`입니다.

### 정적/문법 체크

```bash
python -m compileall backend/glass/app.py
```

### 개발자 문서

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> 참고: 현재 저장소 스냅샷에서는 일부 과거 링크가 이동되어 있을 수 있습니다(예: 브리지 노트는 `references/ideasglass_bridge.md`에 존재). 원래 링크는 정식 README 내용으로 보존되어 있습니다.

### 빠른 디바이스 바인딩(보존된 워크플로우)

- ID 생성( `glass` conda 환경): `python backend/glass/tools/generate_device_id.py`
- 펌웨어에 설정: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- 백엔드 실행 후 `http://localhost:8765` 접속, 가입/로그인, Account 패널에서 디바이스 ID 바인딩

## 🆘 문제 해결

- **포트 사용 중:** 백엔드를 다른 포트로 실행하고 클라이언트 설정 업데이트.
- **시리얼 포트 점유:** `fuser -k /dev/ttyACM0`.
- **Linux 시리얼 권한 거부:** `sudo usermod -aG dialout $USER` 후 재로그인.
- **Postgres 미사용 가능:** 백엔드는 DB 없이도 부분 기능으로 동작 가능; `DATABASE_URL` 확인 후 재시작.
- **Whisper 성능 이슈:** 더 작은 모델(`base`/`small`) 사용 또는 `IDEASGLASS_TRANSCRIBE=0`으로 전사 비활성화.
- **ESP32의 TLS/시간 동기 불안정:** Wi-Fi, NTP(UDP/123), 인증서/호스트 설정 점검; 세부 현장 노트는 `references/ideasglass_bridge.md` 참고.
- **실시간 파형 미반영:** 백엔드 로그와 브라우저 콘솔에서 `[IdeasGlass][wave]` 추적 이벤트를 확인하고 `/ws/stream` 연결 상태 점검.

## 🌐 생태계 링크

🧠 **EchoMind** — 학습과 창작을 위한 다국어 AI 동반자.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — 대담한 콘셉트를 위한 리서치-투-프로덕트 커뮤니티.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — 작은 성과를 수익으로 전환하는 자동화 도구.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — 물리학·화학 트랙과 노트북.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — 아이디어를 초안·작업·게시물로 바꾸는 에이전트.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — 캡처, 번역, 하이라이트 릴 자동 생성.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — 기여와 온체인 가치를 잇는 보상·지급 체계.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — 연구 노트와 에세이의 저장소.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — OnlyIdeas, EchoMind, LazyEdit, IdeasGlass를 지원하는 스튜디오.  
[lazying.art](https://lazying.art)

## 🙏 감사의 말

우리는 훌륭한 오픈 프로젝트의 토대 위에 서 있습니다. 특히 다음에 감사드립니다.

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">OmiGlass 받기 (BasedHardware)</a>
  - **추천 프로그램** — 쿠폰 `LazyingArt` 사용 시 10% 할인(10회 판매 달성 시 30% 수수료 지급).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">LazyingArt와 함께 OmiGlass 구매</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Omi Discord 참여</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Seeed XIAO BLE Sense 구매</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ 로드맵

- WAN/TLS 환경에서 엔드투엔드 오디오 스트리밍 경로를 안정화하고 문서화.
- 전사 품질/지연 트레이드오프(모델/디바이스/임계값 프리셋)를 지속적으로 개선.
- 대시보드에서 디바이스 관리 및 계정 단위 다중 디바이스 워크플로우를 확장.
- 레거시/병렬 백엔드 트랙(`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`)을 `backend/glass` 주경로와 정렬/통합.
- `i18n/` 하위 다국어 README 버전을 정기적으로 유지/갱신.

## 🤝 기여

기여를 환영합니다. 저장소별 작업 안내는 `AGENTS.md`를 따라 주세요.

PR을 열기 전 권장되는 로컬 검증:

```bash
python -m compileall backend/glass/app.py
```

변경 제출 시:

- 커밋 제목은 간결하고 작업 중심으로 유지하세요(현재형).
- 동작에 영향을 미치는 경우 관련 환경 변수(예: `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`)를 PR 노트에 기재.
- 테스트 근거(백엔드 로그, 대시보드 동작, 펌웨어 출력)를 포함.
- 비밀 정보(`DATABASE_URL`, API 토큰, 인증서 파일)는 절대 커밋하지 마세요.

## 📄 라이선스

이 저장소 스냅샷에는 최상위 `LICENSE` 파일이 감지되지 않았습니다. 명시적인 라이선스 파일이 추가될 때까지는 사용 및 재배포 시 유지관리자 승인 필요.




## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
