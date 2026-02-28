[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*Kính AI đeo được biến ý tưởng thành hành động, thu nhập và động lực sáng tạo.*

> Dòng chảy AI đeo được ưu tiên giọng nói: thu âm từ kính ESP32, xử lý trong FastAPI, và giám sát/điều khiển qua dashboard PWA thời gian thực.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Lane | Purpose |
|---|---|
| 🎙️ Wearable capture | ESP32 glasses send audio, photos, and telemetry in near-real-time |
| 🧠 Backend intelligence | FastAPI ingests streams, transcribes, segments, and persists metadata |
| 🖥️ Dashboard | PWA shows live waveform, transcripts, and device/account status |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Ecosystem</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Support IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>Giao diện app (trái) · Phần cứng (phải)</sub>
</div>

Khám phá các thí nghiệm cộng đồng tại <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Tổng quan

IdeasGlass là hệ thống đeo được ưu tiên AI cho việc ghi nhận và triển khai ý tưởng theo hướng nói trước. Trong repository này, luồng chạy chính là:

- `backend/glass/` cho API FastAPI, WebSocket ingest, phiên âm bằng Whisper và dashboard PWA có thể cài đặt.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` cho firmware XIAO ESP32S3 truyền telemetry/audio/photos.

Nếu bạn mới bắt đầu với repo này, hãy bắt đầu từ đây.

### At a glance

| Khu vực | Vị trí chính | Chức năng |
|---|---|---|
| Backend API + PWA | `backend/glass/` | Endpoint FastAPI, WebSocket ingest/fanout, phiên âm, dashboard |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Client ESP32 cho thu và phát luồng |
| Bridge notes | `references/ideasglass_bridge.md` | Ghi chú độ tin cậy TLS/WAN và mẹo triển khai thực tế |
| Bản dịch README | `i18n/` | Tài liệu đa ngôn ngữ đồng bộ từ README chính |

## ✨ Tại sao chọn IdeasGlass

IdeasGlass là sản phẩm đeo được ưu tiên AI dành cho người làm việc trong dòng chảy ý tưởng liên tục. Nó ghi nhận, dịch, sắp xếp và triển khai sự sáng tạo ngay khi cảm hứng đến, dù bạn đang thuyết minh ý tưởng khi di chuyển hoặc đang dẫn một phiên trực tiếp.

## 🧩 Tính năng

### Tính năng theo tầm nhìn sản phẩm

- **Phần cứng tạo nên từ quá trình tạo ra** – kính nhẹ và các đầu vào đeo được, tối ưu cho ghi âm theo giọng nói cùng phím tắt cử chỉ tinh gọn.
- **Dịch tức thì** – nhận diện và dịch ngôn ngữ thời gian thực để bạn có thể sáng tạo cùng nhóm hoặc khán giả đa ngôn ngữ mà không cần đổi công cụ.
- **Đồng lái EchoMind** – tích hợp chặt chẽ với `chat.lazying.art` để động não, phác thảo kịch bản và huấn luyện nội dung đa ngôn ngữ.
- **Chế độ tự động hóa kênh** – tạo dàn bài, kịch bản dài, hook ngắn và lập lịch đăng lên YouTube hoặc các kênh khác.
- **Highlights & reels** – tự chọn khoảnh khắc nổi bật, sinh thumbnail, phụ đề và clip sẵn sàng đăng mạng xã hội.
- **Lớp tạo thu nhập** – kết nối với LazyingArt Coin cho tip, thanh toán tín dụng, và chuyển đổi thành tài sản on-chain.
- **Chi tiêu & tập trung** – theo dõi chi phí vận hành, làm nổi bật định dạng sinh lợi, và tinh luyện điểm mạnh của bạn thành dự án kế tiếp.

### Tính năng theo mức repo/runtime

- Backend FastAPI với endpoint REST + WebSocket cho ingest (`/api/v1/audio`, `/ws/audio-ingest`) và fanout luồng trực tiếp (`/ws/stream`).
- Phân đoạn âm thanh xác định (mặc định khoảng 15 giây có chồng lấp) vào `backend/glass/audio_segments/`.
- Transcript streaming tùy chọn bằng openai-whisper với ngưỡng trễ cấu hình được.
- Lưu trữ Postgres tùy chọn (`DATABASE_URL`) cho tin nhắn, ảnh, chunk, segment và transcript.
- Dashboard PWA với waveform thời gian thực, cập nhật transcript, và hỗ trợ cài đặt trên desktop/mobile.
- Hỗ trợ firmware Arduino cho luồng camera + mic của XIAO ESP32S3 Sense.

## 🔄 Quy trình mẫu

1. **Ghi nhận** – Nói hoặc phác thảo ý tưởng; IdeasGlass phiên âm, dịch và gắn nhãn ý định.
2. **Phối hợp sáng tạo** – EchoMind tinh chỉnh ý tưởng, viết thảo bản kịch bản, và gợi ý CTA phù hợp từng nền tảng.
3. **Xuất bản** – Agent kênh tự tạo video điểm nổi bật, ảnh gallery, và upload kèm metadata.
4. **Kiếm tiền** – Tín dụng đi qua LazyingArt Coin (`coin.lazying.art`) và payout đồng bộ với ví ưa thích của bạn.
5. **Đánh giá lại** – Dashboard về chi tiêu, tệp và mức độ tương tác cho biết điều gì cần đầu tư tiếp theo.

## 🗂️ Cấu trúc dự án

```text
IdeasGlass/
├── README.md
├── i18n/                                  # Bản dịch README
├── backend/
│   ├── glass/                             # Backend FastAPI + PWA chính
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # Đường truyền ingest song song/đi sau
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Ghi chú Bridge + triển khai
├── docs/                                  # Tài nguyên site/docs bổ sung
├── development_plan/
├── app/
├── ops/observability/
├── figs/
└── seeed_studio_xiao_esp32s3_dev/
```

## 🧰 Yêu cầu

- Python 3.10+
- `pip` (hoặc môi trường conda có Python tương thích)
- Tùy chọn: NVIDIA GPU + CUDA/cuDNN cho suy luận Whisper nhanh hơn
- Tùy chọn: PostgreSQL cho lưu trữ
- Với firmware: Arduino IDE hoặc `arduino-cli`, Seeed XIAO ESP32S3 Sense, bật PSRAM

| Thành phần | Yêu cầu | Ghi chú |
|---|---|---|
| Backend runtime | Python 3.10+, `pip` | Dùng venv hoặc conda (`glass`) |
| Tăng tốc GPU (tùy chọn) | NVIDIA + CUDA/cuDNN | Giảm trễ Whisper |
| Lưu trữ (tùy chọn) | PostgreSQL | Bật qua `DATABASE_URL` |
| Công cụ firmware | Arduino IDE / `arduino-cli` | Dùng profile XIAO ESP32S3 có PSRAM |

## ⚙️ Cài đặt

### Phụ thuộc backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Yêu cầu firmware

- Sao chép `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` thành `wifi_credentials.h` (đề xuất) và điền SSID/password.
- Trong Arduino IDE, chọn board `ESP32 -> XIAO_ESP32S3` với `PSRAM: OPI PSRAM`.
- Partition scheme: `Default with spiffs (3MB APP/1.5MB SPIFFS)` hoặc `Maximum APP` khi không cần filesystem.

## ▶️ Cách sử dụng

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
| `/` | Dashboard chính (UI có khả năng PWA) |
| `/healthz` | Kiểm tra trạng thái backend |
| `/ws/audio-ingest` | WebSocket ingest từ thiết bị |
| `/ws/stream` | Live fanout cho client dashboard |

### Đăng nhập và liên kết thiết bị của bạn

1. Đăng ký hoặc đăng nhập từ phần Settings/Account của dashboard.
2. Liên kết device ID trong trường `Bind device`.
3. Chỉ các thiết bị đã liên kết mới có thể stream về tài khoản của bạn.

Tạo device ID + ảnh QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Liên kết qua API (yêu cầu cookie session):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Xác thực tài khoản hiện tại và thiết bị đã liên kết:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Di chuyển dữ liệu lịch sử (đổi tên dữ liệu cũ sang device ID mới) (tùy chọn):

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

Nếu cổng đang bận: `fuser -k /dev/ttyACM0`.
Nếu bị từ chối quyền: chạy `sudo usermod -aG dialout $USER` rồi đăng nhập lại (hoặc tạm thời `sudo chmod a+rw /dev/ttyACM0`).

### Tương tác nguồn điện firmware (XIAO ESP32S3)

- Giữ nút khoảng ~0.8 giây khi bật nguồn để khởi động.
- Giữ ~2.5 giây khi đang chạy để vào deep sleep.
- Nhấn ngắn khi đang chạy vẫn khởi tạo capture.

## 🛠️ Cấu hình

### Biến môi trường cốt lõi

- `DATABASE_URL`: DSN Postgres tùy chọn cho lưu trữ bền vững.
- `IDEASGLASS_WHISPER_MODEL`: `base` (mặc định), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` hoặc `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` cho mixed precision trên GPU, `0` cho CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (mặc định) để bật phiên âm, `0` để tắt.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: khoảng thời gian cuộn transcript.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: các ngưỡng tách bằng dấu phẩy (mặc định `3000,6000,15000`).

| Biến | Mặc định / tùy chọn | Tác động |
|---|---|---|
| `DATABASE_URL` | không đặt mặc định | Bật lưu trữ Postgres cho dữ liệu account/device |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Cân bằng độ chính xác và độ trễ |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` hoặc `cpu` | Backend suy luận |
| `IDEASGLASS_WHISPER_FP16` | `1` cho GPU, `0` an toàn CPU | Điều khiển mixed precision |
| `IDEASGLASS_TRANSCRIBE` | `1` | Bật/tắt pipeline transcript |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | theo runtime | Chu kỳ đẩy transcript cuộn |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Ngưỡng emit transcript theo từng mức |

Các ví dụ an toàn `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (xác thực peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (xác thực mật khẩu)

### Audio gain và các knob phân đoạn

- `IDEASGLASS_GAIN_TARGET` (mặc định `0.032`)
- `IDEASGLASS_GAIN_MAX` (mặc định `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (mặc định `0.008`)
- `IDEASGLASS_SPEECH_RMS` (mặc định `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (mặc định `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (mặc định `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (mặc định `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (mặc định theo chunk gain)

| Audio knob | Mặc định | Mục đích |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Chuẩn hóa RMS mục tiêu |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Giới hạn trên cho khuếch đại gain |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Ngưỡng tránh khuếch đại đoạn gần im lặng |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Mốc RMS hoạt động nói |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Khoảng dự trữ quanh ngưỡng phát hiện giọng |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Độ dài segment mục tiêu |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Độ chồng lấp segment để đảm bảo liên tục |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | kế thừa chunk gain | Mục tiêu chuẩn hóa theo segment |

### Model prefetch (tùy chọn)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Ví dụ

### Sinh và liên kết device ID

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Sau đó đặt `kDeviceId` trong:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Luồng dashboard:

1. Đăng ký/đăng nhập trong Settings.
2. Liên kết thiết bị ở bảng Account.
3. Chỉ thiết bị đã liên kết mới stream vào tài khoản của bạn.

### Ví dụ ingest REST

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

Repo này chứa nhiều nhánh backend. Hướng dẫn đóng góp hiện tại và trọng tâm runtime là `backend/glass/`, trừ khi có yêu cầu khác.

### Kiểm tra tĩnh/cú pháp

```bash
python -m compileall backend/glass/app.py
```

### Tài liệu cho nhà phát triển

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Lưu ý: Trong snapshot repo hiện tại, một số liên kết lịch sử có vẻ đã thay đổi (ví dụ bridge notes hiện ở `references/ideasglass_bridge.md`). Các liên kết gốc vẫn được giữ như nội dung chuẩn của README.

### Quy trình liên kết thiết bị nhanh (được giữ nguyên)

- Tạo ID (trong conda `glass`): `python backend/glass/tools/generate_device_id.py`
- Đặt vào firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Chạy backend và mở `http://localhost:8765`, đăng ký/đăng nhập, sau đó liên kết device ID ở panel Account

## 🆘 Xử lý sự cố

- **Port đã được dùng:** chạy backend trên cổng khác và cập nhật cấu hình client.
- **Cổng serial bận:** `fuser -k /dev/ttyACM0`.
- **Linux không đủ quyền serial:** `sudo usermod -aG dialout $USER` rồi đăng nhập lại.
- **Postgres không sẵn sàng:** backend vẫn chạy mà không cần DB cho một số chức năng; kiểm tra lại `DATABASE_URL` và khởi động lại.
- **Vấn đề hiệu năng Whisper:** dùng model nhỏ hơn (`base`/`small`) hoặc tắt transcript bằng `IDEASGLASS_TRANSCRIBE=0`.
- **Tính ổn định TLS/đồng bộ thời gian trên ESP32:** kiểm tra Wi-Fi, khả dụng NTP (UDP/123), và cấu hình chứng chỉ/host; xem `references/ideasglass_bridge.md` cho ghi chú hiện trường chi tiết.
- **Không thấy cập nhật waveform theo thời gian thực:** kiểm tra backend logs và console trình duyệt để tìm dấu vết `[IdeasGlass][wave]`, xác nhận kết nối `/ws/stream`.

## 🌐 Liên kết hệ sinh thái

🧠 **EchoMind** — Người bạn đồng hành AI đa ngôn ngữ cho học tập và sáng tạo.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Cộng đồng nghiên cứu-to-product cho ý tưởng đậm nét.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Tự động hóa giúp biến thắng nhỏ thành thu nhập.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Các tuyến Physics & chemistry và notebook học tập.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent biến ý tưởng thành bản nháp, nhiệm vụ và bài đăng.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Ghi nhận, dịch, và tự động sản xuất highlight reel.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Phần thưởng và payout nối đóng góp vào giá trị on-chain.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Sổ tay ghi chú nghiên cứu và bài luận.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio đứng sau OnlyIdeas, EchoMind, LazyEdit, và IdeasGlass.  
[lazying.art](https://lazying.art)

## 🙏 Lời cảm ơn

Chúng tôi xây dựng trên nền tảng của nhiều dự án mã mở tuyệt vời — cảm ơn mọi người đã đóng góp:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Chương trình giới thiệu** — Dùng mã coupon `LazyingArt` để tiết kiệm 10% (hoa hồng 30% mở khóa sau 10 đơn hàng).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Lộ trình

- Củng cố và tài liệu hóa toàn bộ đường truyền streaming âm thanh end-to-end trong môi trường WAN/TLS.
- Tiếp tục cải thiện tradeoff chất lượng/độ trễ transcript (model/device/ngưỡng preset).
- Mở rộng quản lý thiết bị và quy trình dashboard cho nhiều thiết bị theo account.
- Đồng bộ hoặc hợp nhất các track backend cũ/song song (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) với đường truyền chính `backend/glass`.
- Duy trì và cập nhật các phiên bản README đa ngôn ngữ trong `i18n/`.

## 🤝 Đóng góp

Đóng góp luôn được chào đón. Để biết quy trình làm việc cụ thể cho repo, hãy theo `AGENTS.md`.

Khuyến nghị xác minh cục bộ trước khi mở PR:

```bash
python -m compileall backend/glass/app.py
```

Khi gửi thay đổi:

- Giữ tiêu đề commit ngắn gọn, hướng hành động (thì hiện tại).
- Nêu các biến môi trường liên quan (ví dụ `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) trong ghi chú PR khi hành vi phụ thuộc vào chúng.
- Kèm minh chứng kiểm thử (backend logs, hành vi dashboard, đầu ra firmware).
- Không bao giờ commit secrets (`DATABASE_URL`, API tokens, file credentials).

## 📄 Giấy phép

Không có tệp `LICENSE` cấp cao nhất nào trong snapshot repository này. Cho đến khi file giấy phép rõ ràng được thêm vào, hãy xem việc sử dụng và phân phối như cần phê duyệt từ người bảo trì.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
