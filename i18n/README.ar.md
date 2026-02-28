[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*نظّارة ذكاء اصطناعي قابلة للارتداء تحوّل الأفكار إلى تنفيذ، دخل، وزخم إبداعي.*

> مسار ذكاء اصطناعي قابل للارتداء قائم على الصوت أولًا: التقاط من نظارة ESP32، معالجة عبر FastAPI، ومراقبة/تحكم عبر لوحة PWA مباشرة.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>المنظومة</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>ادعم IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>واجهة التطبيق (يسار) · العتاد (يمين)</sub>
</div>

استكشف تجارب المجتمع على <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 نظرة عامة

IdeasGlass نظام قابل للارتداء مبني على الذكاء الاصطناعي وبمنهجية الصوت أولًا لالتقاط الأفكار وتنفيذها. في هذا المستودع، مسار التشغيل الأساسي هو:

- `backend/glass/` لواجهات FastAPI، وإدخال WebSocket، والتفريغ المعتمد على Whisper، ولوحة PWA القابلة للتثبيت.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` لبرمجية XIAO ESP32S3 التي تبث القياسات/الصوت/الصور.

إذا كنت جديدًا على هذا المستودع، ابدأ من هذين المسارين أولًا.

### لمحة سريعة

| المجال | الموقع الأساسي | ماذا يفعل |
|---|---|---|
| Backend API + PWA | `backend/glass/` | نقاط نهاية FastAPI، إدخال/توزيع WebSocket، تفريغ صوتي، لوحة تحكم |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | عميل ESP32 لالتقاط/بث البيانات |
| ملاحظات الجسر | `references/ideasglass_bridge.md` | ملاحظات موثوقية TLS/WAN ونصائح نشر ميدانية |
| ترجمات README | `i18n/` | مستندات متعددة اللغات متزامنة مع README الأساسي |

## ✨ لماذا IdeasGlass

IdeasGlass جهاز قابل للارتداء قائم على الذكاء الاصطناعي ومصمم لمن يعيشون في تدفّق مستمر من الأفكار. يلتقط الإبداع ويترجمه وينظمه وينفّذه لحظة الإلهام، سواء كنت تُملي فكرة أثناء الحركة أو تدير جلسة مباشرة.

## 🧩 الميزات

### ميزات رؤية المنتج

- **عتاد موجّه للإبداع** – نظارة خفيفة ومدخلات قابلة للارتداء، مضبوطة لالتقاط صوتي أولًا مع اختصارات إيماءات بسيطة.
- **ترجمة فورية** – كشف/ترجمة لغوية آنية لتفكير جماعي أو عروض لجمهور متعدد دون تبديل الأدوات.
- **مساعد EchoMind** – تكامل وثيق مع `chat.lazying.art` للعصف الذهني، وصياغة السكربتات، والتوجيه متعدد اللغات للمحتوى.
- **طيار آلي للقنوات** – يصوغ مخططات، نصوص طويلة، خطافات قصيرة، ويجدول الرفع إلى YouTube أو منصات أخرى.
- **اللقطات الأبرز والمقاطع القصيرة** – يختار اللحظات تلقائيًا، ويولّد صورًا مصغرة، وترجمات، ومقاطع جاهزة للنشر الاجتماعي.
- **طبقة الدخل** – يتصل بـ LazyingArt Coin للإكراميات، ودفع الأرصدة، والتحويل إلى أصول على السلسلة.
- **الإنفاق والتركيز** – يتتبع الإنفاق التشغيلي، ويبرز الصيغ الأكثر ربحية، ويستخلص نقاط قوتك لمشاريعك التالية.

### ميزات المستودع/التشغيل

- Backend بـ FastAPI مع REST + WebSocket للإدخال (`/api/v1/audio`, `/ws/audio-ingest`) وتوزيع البث الحي (`/ws/stream`).
- تقسيم صوتي حتمي (افتراضيًا ~15 ثانية مع تداخل) إلى `backend/glass/audio_segments/`.
- تفريغ بث اختياري عبر openai-whisper مع عتبات كمون قابلة للضبط.
- حفظ اختياري في Postgres (`DATABASE_URL`) للرسائل والصور والقطع الصوتية والمقاطع والتفريغ النصي.
- لوحة PWA مع موجة صوت حية، وتحديثات تفريغ، ودعم التثبيت على سطح المكتب/الهاتف.
- دعم Firmware لـ Arduino مع مسارات كاميرا + ميكروفون XIAO ESP32S3 Sense.

## 🔄 سير عمل نموذجي

1. **الالتقاط** – تحدث أو ارسم فكرة؛ يقوم IdeasGlass بالتفريغ والترجمة ووضع الوسوم على النية.
2. **الإنشاء المشترك** – يقوم EchoMind بتنقيح الفكرة، وصياغة السكربتات، واقتراح CTAs مناسبة لكل منصة.
3. **النشر** – وكيل القناة ينتج تلقائيًا فيديوهات لقطات مميزة، وصور معرض، ويرفعها مع البيانات الوصفية.
4. **تحقيق الدخل** – تُوجَّه الأرصدة عبر LazyingArt Coin (`coin.lazying.art`) وتُزامَن المدفوعات مع محافظك المفضلة.
5. **المراجعة** – لوحات الإنفاق والوصول والتفاعل تُظهر ما يستحق التركيز عليه لاحقًا.

## 🗂️ هيكل المشروع

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

## 🧰 المتطلبات المسبقة

- Python 3.10+
- `pip` (أو بيئة conda مع إصدار Python متوافق)
- اختياري: NVIDIA GPU + CUDA/cuDNN لتسريع استدلال Whisper
- اختياري: PostgreSQL للحفظ الدائم
- للـ Firmware: Arduino IDE أو `arduino-cli`، جهاز Seeed XIAO ESP32S3 Sense، مع تفعيل PSRAM

| المكوّن | المتطلب | ملاحظات |
|---|---|---|
| تشغيل Backend | Python 3.10+, `pip` | استخدم venv أو conda (`glass`) |
| تسريع GPU (اختياري) | NVIDIA + CUDA/cuDNN | يحسن كمون Whisper |
| الحفظ الدائم (اختياري) | PostgreSQL | يُفعّل عبر `DATABASE_URL` |
| سلسلة أدوات Firmware | Arduino IDE / `arduino-cli` | استخدم إعداد XIAO ESP32S3 مع PSRAM |

## ⚙️ التثبيت

### تبعيات Backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### متطلبات Firmware

- انسخ `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` إلى `wifi_credentials.h` (موصى به) ثم اضبط SSID/password.
- في Arduino IDE، استخدم اللوحة `ESP32 -> XIAO_ESP32S3` مع `PSRAM: OPI PSRAM`.
- مخطط التقسيم: `Default with spiffs (3MB APP/1.5MB SPIFFS)` أو `Maximum APP` إذا لم تكن بحاجة لنظام الملفات.

## ▶️ الاستخدام

### تشغيل Backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### تشغيل Backend (أداة مساعدة)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### فتح لوحة التحكم

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | الغرض |
|---|---|
| `/` | لوحة التحكم الرئيسية (واجهة تدعم PWA) |
| `/healthz` | فحص جاهزية Backend |
| `/ws/audio-ingest` | WebSocket إدخال الجهاز |
| `/ws/stream` | توزيع البث الحي إلى عملاء لوحة التحكم |

### تسجيل الدخول وربط جهازك

1. سجّل حسابًا أو سجّل الدخول من قسم Settings/Account في لوحة التحكم.
2. اربط معرّف جهازك في حقل `Bind device`.
3. الأجهزة المرتبطة فقط هي التي تبث إلى حسابك.

توليد معرّف جهاز + صورة QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

الربط عبر API (يتطلب جلسة cookie):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

التحقق من الحساب الحالي والأجهزة المرتبطة:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

ترحيل اختياري (إعادة تسمية البيانات التاريخية إلى معرّف جهاز جديد):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### بناء/رفع Firmware (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

إذا كان المنفذ مشغولًا: `fuser -k /dev/ttyACM0`.
إذا ظهرت مشكلة صلاحيات: `sudo usermod -aG dialout $USER` ثم أعد تسجيل الدخول (أو مؤقتًا `sudo chmod a+rw /dev/ttyACM0`).

### تجربة طاقة Firmware (XIAO ESP32S3)

- اضغط مطولًا على الزر ~0.8 ثانية عند التشغيل للإقلاع.
- اضغط مطولًا ~2.5 ثانية أثناء التشغيل للدخول في النوم العميق.
- ضغطة قصيرة أثناء التشغيل ما تزال تفعّل الالتقاط.

## 🛠️ الإعداد

### متغيرات البيئة الأساسية

- `DATABASE_URL`: DSN اختياري لـ Postgres من أجل التخزين الدائم.
- `IDEASGLASS_WHISPER_MODEL`: `base` (افتراضي)، `small`، `medium`، `large-v3`، `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` أو `cpu`.
- `IDEASGLASS_WHISPER_FP16`: القيمة `1` لدقة مختلطة على GPU، أو `0` لـ CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (افتراضي) لتفعيل التفريغ النصي، `0` للتعطيل.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: فترة التحديث المتحرك للتفريغ.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: عتبات مفصولة بفواصل (افتراضي `3000,6000,15000`).

| المتغير | الافتراضي / الخيارات | التأثير |
|---|---|---|
| `DATABASE_URL` | غير مضبوط افتراضيًا | يفعّل حفظ Postgres لبيانات الحساب/الأجهزة |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | يضبط الدقة مقابل الكمون |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` أو `cpu` | محرك الاستدلال |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU، `0` آمن لـ CPU | التحكم بالدقة المختلطة |
| `IDEASGLASS_TRANSCRIBE` | `1` | تشغيل/إيقاف مسار التفريغ |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | يُضبط وقت التشغيل | فترة دفع التفريغ المتحرك |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | عتبات إصدار تدريجي للتفريغ |

أمثلة آمنة لـ `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (مصادقة peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (مصادقة بكلمة مرور)

### إعدادات كسب الصوت والتقسيم

- `IDEASGLASS_GAIN_TARGET` (افتراضي `0.032`)
- `IDEASGLASS_GAIN_MAX` (افتراضي `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (افتراضي `0.008`)
- `IDEASGLASS_SPEECH_RMS` (افتراضي `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (افتراضي `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (افتراضي `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (افتراضي `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (يفتراضيًا يرث هدف كسب القطعة)

| إعداد الصوت | الافتراضي | الغرض |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | تطبيع RMS المستهدف |
| `IDEASGLASS_GAIN_MAX` | `1.8` | حد أعلى لتكبير الكسب |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | حد أدنى لتجنب تضخيم شبه الصمت |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | خط أساس RMS لنشاط الكلام |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | هامش حول عتبة الكلام |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | طول المقطع المستهدف |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | تداخل المقاطع للاستمرارية |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | يرث كسب القطعة | هدف التطبيع على مستوى المقطع |

### جلب النماذج مسبقًا (اختياري)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 أمثلة

### توليد وربط معرّف جهاز

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

ثم اضبط `kDeviceId` في:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

تدفق لوحة التحكم:

1. أنشئ حسابًا/سجّل الدخول من Settings.
2. اربط الجهاز من لوحة Account.
3. فقط الأجهزة المرتبطة تبث إلى حسابك.

### أمثلة REST ingest

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

## 🧭 ملاحظات التطوير

### منطقة التركيز

يحتوي هذا المستودع على عدة مسارات Backend. توجيه المساهمة الحالي وتركيز التشغيل هو `backend/glass/` ما لم يُطلب غير ذلك.

### فحص ثابت/نحوي

```bash
python -m compileall backend/glass/app.py
```

### مستندات المطور

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> ملاحظة: في لقطة المستودع الحالية، يبدو أن بعض الروابط التاريخية أعلاه قد تغيّرت (مثلًا، ملاحظات الجسر موجودة الآن في `references/ideasglass_bridge.md`). تم الإبقاء على الروابط الأصلية كمحتوى README مرجعي.

### ربط سريع للجهاز (تدفق محفوظ)

- توليد المعرّف (ضمن conda `glass`): `python backend/glass/tools/generate_device_id.py`
- ضبطه في Firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- شغّل Backend وافتح `http://localhost:8765`، ثم أنشئ حسابًا/سجّل الدخول، وبعدها اربط معرّف الجهاز في لوحة Account

## 🆘 استكشاف الأخطاء وإصلاحها

- **المنفذ مستخدم مسبقًا:** شغّل Backend على منفذ آخر وحدّث إعدادات العميل.
- **منفذ Serial مشغول:** `fuser -k /dev/ttyACM0`.
- **رفض صلاحية Serial على Linux:** `sudo usermod -aG dialout $USER` ثم أعد تسجيل الدخول.
- **Postgres غير متاح:** يمكن تشغيل Backend بدون قاعدة بيانات مع وظائف جزئية؛ تحقّق من `DATABASE_URL` ثم أعد التشغيل.
- **مشاكل أداء Whisper:** استخدم نماذج أصغر (`base`/`small`) أو عطّل التفريغ عبر `IDEASGLASS_TRANSCRIBE=0`.
- **عدم استقرار TLS/مزامنة الوقت على ESP32:** تحقّق من Wi-Fi، وتوفّر NTP (UDP/123)، وإعدادات الشهادة/المضيف؛ راجع `references/ideasglass_bridge.md` لملاحظات ميدانية مفصلة.
- **لا توجد تحديثات لموجة الصوت المباشرة:** افحص سجلات Backend ووحدة تحكم المتصفح لآثار `[IdeasGlass][wave]` وتأكد من اتصال `/ws/stream`.

## 🌐 روابط المنظومة

🧠 **EchoMind** — مساعد ذكاء اصطناعي متعدد اللغات للتعلّم والإبداع.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — مجتمع يحوّل الأبحاث إلى منتجات لمفاهيم جريئة.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — أتمتة لتحويل الإنجازات الصغيرة إلى دخل.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — مسارات ودفاتر للفيزياء والكيمياء.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — وكيل يحوّل الأفكار إلى مسودات ومهام ومنشورات.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — التقاط، ترجمة، وإنتاج تلقائي للمقاطع الأبرز.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — مكافآت ومدفوعات تربط المساهمات بالقيمة على السلسلة.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — دفتر لملاحظات الأبحاث والمقالات.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — الاستوديو وراء OnlyIdeas وEchoMind وLazyEdit وIdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ الدعم والتواصل

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- دعمك يحافظ على تقدّم خارطة طريق الأجهزة القابلة للارتداء والوكلاء والمنظومة.

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

- للشراكات، راسل **contact@lazying.art** بعنوان `IdeasGlass`.

IdeasGlass هو المكان الذي تتوقف فيه الأجهزة القابلة للارتداء عن الاستماع فقط وتبدأ بالبناء معك.

## 🙏 الشكر والتقدير

نقف على أكتاف مشاريع مفتوحة عظيمة، شكرًا إلى:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — استخدم القسيمة `LazyingArt` لتوفير 10% (تُفتح عمولة 30% بعد 10 مبيعات).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ خارطة الطريق

- تعزيز وتوثيق مسار بث الصوت من الطرف إلى الطرف عبر بيئات WAN/TLS.
- الاستمرار في تحسين مفاضلة جودة/كمون التفريغ (إعدادات النموذج/الجهاز/العتبات).
- توسيع إدارة الأجهزة وسير العمل متعدد الأجهزة المرتبط بالحساب داخل لوحة التحكم.
- مواءمة أو دمج مسارات Backend القديمة/الموازية (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) مع المسار الأساسي `backend/glass`.
- صيانة وتحديث نسخ README متعددة اللغات تحت `i18n/`.

## 🤝 المساهمة

المساهمات مرحب بها. لإرشادات سير العمل الخاصة بهذا المستودع، اتبع `AGENTS.md`.

التحقق المحلي الموصى به قبل فتح PR:

```bash
python -m compileall backend/glass/app.py
```

عند إرسال التغييرات:

- اجعل عناوين الـ commit قصيرة وموجّهة للفعل (بصيغة المضارع).
- اذكر متغيرات البيئة ذات الصلة (مثل `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) في ملاحظات PR عندما يعتمد السلوك عليها.
- أدرج أدلة الاختبار (سجلات Backend، سلوك لوحة التحكم، مخرجات Firmware).
- لا تقم أبدًا بإيداع الأسرار (`DATABASE_URL`، رموز API، ملفات بيانات الاعتماد).

## 📄 الترخيص

لم يتم اكتشاف ملف `LICENSE` في جذر هذا المستودع في هذه اللقطة. حتى إضافة ملف ترخيص صريح، اعتبر الاستخدام وإعادة التوزيع خاضعين لموافقة المشرفين.
