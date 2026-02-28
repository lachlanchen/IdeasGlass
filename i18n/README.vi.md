[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*Kính AI đeo được, biến ý tưởng thành hành động, thu nhập và động lực sáng tạo.*

> Quy trình AI đeo được ưu tiên giọng nói: thu từ kính ESP32, xử lý trong FastAPI, giám sát/điều khiển qua bảng điều khiển PWA thời gian thực.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Hệ sinh thái</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Ủng hộ IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>Giao diện ứng dụng (trái) · Phần cứng (phải)</sub>
</div>

Khám phá các thử nghiệm cộng đồng tại <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Tổng quan

IdeasGlass là hệ thống đeo được ưu tiên AI, tối ưu cho ghi nhận và thực thi ý tưởng bằng giọng nói. Trong kho mã này, luồng runtime chính là:

- `backend/glass/` cho API FastAPI, ingest WebSocket, phiên âm dựa trên Whisper và bảng điều khiển PWA có thể cài đặt.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` cho firmware XIAO ESP32S3 truyền telemetry/audio/ảnh.

Nếu bạn mới vào repo này, hãy bắt đầu từ hai phần trên.

### Tóm tắt nhanh

| Khu vực | Vị trí chính | Chức năng |
|---|---|---|
| Backend API + PWA | `backend/glass/` | Endpoint FastAPI, ingest/fanout WebSocket, phiên âm, dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Client ESP32 thu thập/truyền dữ liệu |
| Ghi chú bridge | `references/ideasglass_bridge.md` | Ghi chú độ ổn định TLS/WAN và mẹo triển khai thực địa |
| Bản dịch README | `i18n/` | Tài liệu đa ngôn ngữ đồng bộ từ README gốc |

## ✨ Vì sao IdeasGlass

IdeasGlass là thiết bị đeo ưu tiên AI dành cho những người luôn sống trong dòng chảy ý tưởng. Nó ghi nhận, dịch, tổ chức và thực thi sáng tạo ngay khi cảm hứng xuất hiện, dù bạn đang thuyết minh ý tưởng khi di chuyển hay đang dẫn một phiên live.

## 🧩 Tính năng

### Tính năng theo tầm nhìn sản phẩm

- **Phần cứng sinh ra để sáng tạo** – kính nhẹ và thiết bị đeo đầu vào, tối ưu cho ghi âm bằng giọng nói kèm phím tắt cử chỉ tinh gọn.
- **Dịch tức thì** – nhận diện/dịch ngôn ngữ thời gian thực để bạn brainstorm xuyên nhóm hoặc xuyên đối tượng mà không cần đổi công cụ.
- **Đồng lái EchoMind** – tích hợp chặt với `chat.lazying.art` cho brainstorming, phác thảo kịch bản và coaching nội dung đa ngôn ngữ.
- **Kênh autopilot** – soạn dàn ý, kịch bản dài, hook ngắn và lên lịch đăng YouTube hoặc các kênh khác.
- **Highlights & reels** – tự chọn khoảnh khắc, tạo thumbnail, phụ đề và clip sẵn sàng cho mạng xã hội.
- **Lớp thu nhập** – kết nối LazyingArt Coin để tip, chi trả credit và chuyển đổi sang tài sản on-chain.
- **Chi tiêu & tập trung** – theo dõi chi phí vận hành, làm nổi bật định dạng có lợi nhuận, và chắt lọc điểm mạnh cá nhân thành dự án tiếp theo.

### Tính năng ở mức repo/runtime

- Backend FastAPI với endpoint REST + WebSocket cho ingest (`/api/v1/audio`, `/ws/audio-ingest`) và fanout live stream (`/ws/stream`).
- Phân đoạn audio tất định (mặc định ~15 giây có overlap) vào `backend/glass/audio_segments/`.
- Tùy chọn transcript streaming bằng openai-whisper với ngưỡng độ trễ cấu hình được.
- Tùy chọn lưu trữ Postgres (`DATABASE_URL`) cho messages, photos, chunks, segments, transcripts.
- Dashboard PWA với waveform trực tiếp, cập nhật transcript và hỗ trợ cài đặt trên desktop/mobile.
- Hỗ trợ firmware Arduino cho luồng camera + mic của XIAO ESP32S3 Sense.

## 🔄 Quy trình mẫu

1. **Thu nhận** – Nói hoặc phác thảo ý tưởng; IdeasGlass phiên âm, dịch và gắn thẻ ý định.
2. **Đồng sáng tạo** – EchoMind tinh chỉnh ý tưởng, soạn kịch bản và gợi ý CTA theo từng nền tảng.
3. **Xuất bản** – Agent kênh tự tạo video highlight, ảnh gallery và tải lên kèm metadata.
4. **Kiếm tiền** – Credit đi qua LazyingArt Coin (`coin.lazying.art`) và đồng bộ chi trả với ví bạn chọn.
5. **Phản tư** – Dashboard chi tiêu, độ phủ và tương tác cho biết phần nào cần nhân rộng tiếp theo.

## 🗂️ Cấu trúc dự án

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

## 🧰 Điều kiện tiên quyết

- Python 3.10+
- `pip` (hoặc môi trường conda với phiên bản Python tương thích)
- Tùy chọn: NVIDIA GPU + CUDA/cuDNN để Whisper suy luận nhanh hơn
- Tùy chọn: PostgreSQL để lưu trữ bền vững
- Với firmware: Arduino IDE hoặc `arduino-cli`, Seeed XIAO ESP32S3 Sense, bật PSRAM

| Thành phần | Yêu cầu | Ghi chú |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | Dùng venv hoặc conda (`glass`) |
| GPU acceleration (tùy chọn) | NVIDIA + CUDA/cuDNN | Cải thiện độ trễ Whisper |
| Persistence (tùy chọn) | PostgreSQL | Bật qua `DATABASE_URL` |
| Firmware toolchain | Arduino IDE / `arduino-cli` | Dùng profile XIAO ESP32S3 với PSRAM |

## ⚙️ Cài đặt

### Phụ thuộc backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Điều kiện firmware

- Sao chép `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` thành `wifi_credentials.h` (khuyến nghị) và đặt SSID/password.
- Trong Arduino IDE, dùng board `ESP32 -> XIAO_ESP32S3` với `PSRAM: OPI PSRAM`.
- Partition scheme: `Default with spiffs (3MB APP/1.5MB SPIFFS)` hoặc `Maximum APP` nếu không cần filesystem.

## ▶️ Sử dụng

### Chạy backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Chạy backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Mở dashboard

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Mục đích |
|---|---|
| `/` | Dashboard chính (UI có thể dùng như PWA) |
| `/healthz` | Kiểm tra backend còn sống |
| `/ws/audio-ingest` | WebSocket ingest từ thiết bị |
| `/ws/stream` | Fanout live stream đến client dashboard |

### Đăng nhập và liên kết thiết bị

1. Đăng ký hoặc đăng nhập từ khu vực Settings/Account trên dashboard.
2. Liên kết device ID của bạn ở trường `Bind device`.
3. Chỉ thiết bị đã liên kết mới stream vào tài khoản của bạn.

Tạo device ID + ảnh QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Liên kết qua API (cần cookie session):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Xác minh tài khoản hiện tại và thiết bị đã liên kết:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Migration tùy chọn (đổi tên dữ liệu lịch sử sang device ID mới):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Build/upload firmware (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Nếu cổng bị chiếm: `fuser -k /dev/ttyACM0`.
Nếu bị từ chối quyền: `sudo usermod -aG dialout $USER` rồi đăng nhập lại (hoặc tạm thời `sudo chmod a+rw /dev/ttyACM0`).

### Trải nghiệm nguồn firmware (XIAO ESP32S3)

- Giữ nút ~0.8 giây lúc cấp nguồn để khởi động.
- Giữ ~2.5 giây khi đang chạy để vào deep sleep.
- Bấm ngắn khi đang chạy vẫn kích hoạt thu nhận.

## 🛠️ Cấu hình

### Biến môi trường cốt lõi

- `DATABASE_URL`: DSN Postgres tùy chọn cho lưu trữ bền vững.
- `IDEASGLASS_WHISPER_MODEL`: `base` (mặc định), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` hoặc `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` cho mixed precision GPU, `0` cho CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (mặc định) để bật phiên âm, `0` để tắt.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: khoảng thời gian transcript cuốn chiếu.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: ngưỡng phân tách bằng dấu phẩy (mặc định `3000,6000,15000`).

| Biến | Mặc định / tùy chọn | Tác động |
|---|---|---|
| `DATABASE_URL` | mặc định không đặt | Bật lưu trữ Postgres cho dữ liệu tài khoản/thiết bị |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Điều khiển cân bằng độ chính xác và độ trễ |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` hoặc `cpu` | Backend suy luận |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` an toàn cho CPU | Kiểm soát mixed precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Bật/tắt pipeline phiên âm |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | cấu hình theo runtime | Khoảng đẩy transcript cuốn chiếu |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Ngưỡng phát transcript tăng dần |

Ví dụ `DATABASE_URL` an toàn:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (peer/local auth)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (password auth)

### Tinh chỉnh gain và phân đoạn audio

- `IDEASGLASS_GAIN_TARGET` (mặc định `0.032`)
- `IDEASGLASS_GAIN_MAX` (mặc định `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (mặc định `0.008`)
- `IDEASGLASS_SPEECH_RMS` (mặc định `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (mặc định `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (mặc định `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (mặc định `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (mặc định theo chunk gain target)

| Audio knob | Mặc định | Mục đích |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Mục tiêu chuẩn hóa RMS |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Trần giới hạn khuếch đại gain |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Sàn để tránh khuếch đại gần-im-lặng |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Đường cơ sở RMS hoạt động giọng nói |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Biên quanh ngưỡng giọng nói |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Mục tiêu độ dài phân đoạn |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Chồng lấp phân đoạn để liên tục |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | kế thừa chunk gain | Mục tiêu chuẩn hóa cấp phân đoạn |

### Prefetch model (tùy chọn)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Ví dụ

### Tạo và liên kết device ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Sau đó đặt `kDeviceId` trong:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Quy trình trên dashboard:

1. Đăng ký/đăng nhập trong Settings.
2. Liên kết thiết bị trong bảng Account.
3. Chỉ thiết bị đã liên kết mới stream vào tài khoản của bạn.

### Ví dụ REST ingest

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

## 🧭 Ghi chú phát triển

### Khu vực trọng tâm

Repo này chứa nhiều track backend. Hướng dẫn đóng góp hiện tại và trọng tâm runtime là `backend/glass/`, trừ khi có yêu cầu khác.

### Kiểm tra static/syntax

```bash
python -m compileall backend/glass/app.py
```

### Tài liệu cho developer

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Lưu ý: Trong snapshot repo hiện tại, một số liên kết lịch sử bên trên có vẻ đã được chuyển vị trí (ví dụ, ghi chú bridge hiện nằm ở `references/ideasglass_bridge.md`). Các liên kết gốc vẫn được giữ nguyên như nội dung README chuẩn.

### Liên kết thiết bị nhanh (quy trình được giữ lại)

- Tạo ID (trong conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Đặt ID vào firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Chạy backend và mở `http://localhost:8765`, đăng ký/đăng nhập, sau đó liên kết device ID trong bảng Account

## 🆘 Khắc phục sự cố

- **Cổng đã được dùng:** chạy backend trên cổng khác và cập nhật cấu hình client.
- **Cổng serial bị chiếm:** `fuser -k /dev/ttyACM0`.
- **Linux từ chối quyền serial:** `sudo usermod -aG dialout $USER` và đăng nhập lại.
- **Postgres không khả dụng:** backend vẫn chạy được với chức năng một phần; kiểm tra `DATABASE_URL` rồi khởi động lại.
- **Hiệu năng Whisper kém:** dùng model nhỏ hơn (`base`/`small`) hoặc tắt phiên âm qua `IDEASGLASS_TRANSCRIBE=0`.
- **TLS/đồng bộ thời gian không ổn định trên ESP32:** kiểm tra Wi-Fi, NTP (UDP/123), cài đặt cert/host; xem `references/ideasglass_bridge.md` để có ghi chú thực địa chi tiết.
- **Không có cập nhật waveform trực tiếp:** kiểm tra log backend và console trình duyệt cho trace `[IdeasGlass][wave]`, đồng thời xác nhận kết nối `/ws/stream`.

## 🌐 Liên kết hệ sinh thái

🧠 **EchoMind** — Bạn đồng hành AI đa ngôn ngữ cho học tập và sáng tạo.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Cộng đồng nghiên cứu thành sản phẩm cho các ý tưởng táo bạo.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Tự động hóa để biến các thắng lợi nhỏ thành thu nhập.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Lộ trình và sổ tay vật lý & hóa học.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent biến ý tưởng thành bản nháp, tác vụ và bài đăng.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Thu nhận, dịch và tự động tạo highlight reels.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Cơ chế thưởng và chi trả kết nối đóng góp với giá trị on-chain.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Sổ tay ghi chú nghiên cứu và bài luận.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio đứng sau OnlyIdeas, EchoMind, LazyEdit và IdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ Hỗ trợ & Liên hệ

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- Sự ủng hộ của bạn giúp lộ trình thiết bị đeo, agent và hệ sinh thái tiếp tục tiến lên.

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

- Với hợp tác đối tác, hãy gửi email tới **contact@lazying.art** với tiêu đề `IdeasGlass`.

IdeasGlass là nơi thiết bị đeo AI không chỉ lắng nghe mà còn bắt đầu cùng bạn xây dựng.

## 🙏 Lời cảm ơn

Chúng tôi đứng trên vai những dự án mã nguồn mở tuyệt vời — xin cảm ơn:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — Dùng mã `LazyingArt` để giảm 10% (mở khóa hoa hồng 30% sau 10 đơn).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Lộ trình

- Gia cố và tài liệu hóa đường truyền audio end-to-end trong môi trường WAN/TLS.
- Tiếp tục cải thiện đánh đổi chất lượng/độ trễ transcript (preset model/device/threshold).
- Mở rộng quản lý thiết bị và quy trình nhiều thiết bị theo phạm vi tài khoản trong dashboard.
- Đồng bộ hoặc hợp nhất các track backend legacy/song song (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) với luồng chính `backend/glass`.
- Duy trì và làm mới các biến thể README đa ngôn ngữ trong `i18n/`.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón. Với hướng dẫn quy trình theo repo, hãy theo `AGENTS.md`.

Khuyến nghị xác thực cục bộ trước khi mở PR:

```bash
python -m compileall backend/glass/app.py
```

Khi gửi thay đổi:

- Giữ tiêu đề commit ngắn gọn, thiên về hành động (thì hiện tại).
- Nêu rõ biến môi trường liên quan (ví dụ `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) trong ghi chú PR nếu hành vi phụ thuộc vào chúng.
- Bao gồm bằng chứng kiểm thử (log backend, hành vi dashboard, output firmware).
- Không bao giờ commit bí mật (`DATABASE_URL`, API token, file thông tin xác thực).

## 📄 Giấy phép

Không phát hiện file `LICENSE` ở cấp cao nhất trong snapshot repo hiện tại. Cho tới khi có file giấy phép rõ ràng, hãy coi việc sử dụng và phân phối lại cần sự chấp thuận của maintainer.
