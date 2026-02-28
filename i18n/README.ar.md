[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*نظارة ذكاء اصطناعي قابلة للارتداء تحوّل الأفكار إلى أفعال ودخل وزخم إبداعي.*

> خط أنابيب AI أولوية فيه الصوت: التقاط من نظارات ESP32، المعالجة في FastAPI، والمراقبة/التحكم عبر لوحة تحكم PWA مباشرة.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| المسار | الغرض |
|---|---|
| 🎙️ الالتقاط القابل للارتداء | ترسل نظارات ESP32 الصوت والصور وقياسات الحالة بتقريبًا في الوقت الفعلي |
| 🧠 ذكاء الخادم الخلفي | تتولى FastAPI استقبال التدفقات، التفريغ/التفريغ النصي (الترميز)، وتقسيم البيانات وتخزين البيانات الوصفية |
| 🖥️ لوحة التحكم | تعرض لوحة PWA الموجة الحية، النصوص، وحالة الجهاز/الحساب |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="واجهة تطبيق IdeasGlass" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="عتاد IdeasGlass" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>واجهة التطبيق (يسار) · العتاد (يمين)</sub>
</div>

استكشف تجارب المجتمع في <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 نظرة عامة

<a id="overview"></a>
IdeasGlass هو نظام ارتداء موجّه بالذكاء الاصطناعي لالتقاط وتنفيذ الأفكار من خلال الصوت أولًا. في هذا المستودع، مسار التشغيل الأساسي هو:

- `backend/glass/` لواجهات FastAPI، استقبال WebSocket، التفريغ النصي باستخدام Whisper، ولوحة PWA القابلة للتثبيت.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` لبرمجيات XIAO ESP32S3 التي تبث قياس الصوت/الصور/التتبع.

إذا كنت جديدًا في هذا المستودع، ابدأ من هناك أولًا.

## 📚 فهرس المحتويات

- [🚀 نظرة عامة](#overview)
- [✨ لماذا IdeasGlass؟](#why-ideasglass)
- [🧩 الميزات](#features)
- [🔄 سير العمل النموذجي](#sample-workflow)
- [🗂️ هيكلة المشروع](#project-structure)
- [🧰 المتطلبات المسبقة](#prerequisites)
- [⚙️ التثبيت](#installation)
- [▶️ طريقة الاستخدام](#usage)
- [🛠️ الإعدادات](#configuration)
- [🧪 الأمثلة](#examples)
- [🧭 ملاحظات التطوير](#development-notes)
- [🆘 استكشاف الأخطاء](#troubleshooting)
- [🌐 روابط النظام البيئي](#ecosystem-links)
- [🙏 الشكر والتقدير](#acknowledgements)
- [🛣️ خارطة الطريق](#roadmap)
- [🤝 المساهمة](#contribution)
- [❤️ الدعم](#support)
- [📄 الترخيص](#license)

### نظرة سريعة

| المجال | الموقع الأساسي | ما يفعله |
|---|---|---|
| واجهة برمجة التطبيقات + PWA | `backend/glass/` | نقاط نهاية FastAPI، استقبال/توزيع WebSocket، التفريغ النصي، لوحة التحكم |
| البرمجيات الثابتة | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | عميل التقاط/بث ESP32 |
| ملاحظات الجسر | `references/ideasglass_bridge.md` | ملاحظات موثوقية TLS/WAN ونصائح نشر ميدانية |
| ترجمات README | `i18n/` | وثائق متعددة اللغات متزامنة مع README القياسي |

## ✨ لماذا IdeasGlass
<a id="why-ideasglass"></a>

IdeasGlass هي نظارة ارتداء مصممة للبشر الذين يعيشون في تيارات أفكارهم. تلتقط الأفكار، تترجمها، تنظمها، وتنفذها فورًا بمجرد أن تطرق لحظة الإلهام، سواءً كنت تروي مفهومًا أثناء الحركة أو تدير جلسة مباشرة.

## 🧩 الميزات

### ميزات رؤية المنتج

- **عتاد أصيل للإنتاج** – نظارات خفيفة وواجهات ارتداء مهيأة لالتقاط الصوت أولًا مع اختصارات حركية دقيقة.
- **ترجمة فورية** – كشف/ترجمة لغة فورية حتى تتمكن من التفكير الإبداعي عبر فرق أو جماهير متعددة دون تبديل الأدوات.
- **مساعد EchoMind** – تكامل قوي مع `chat.lazying.art` للعصف الذهني، إعداد المسودات، وتدريب المحتوى متعدد اللغات.
- **الطيار الآلي للقناة** – إعداد مخططات، سيناريوهات طويلة، نقاط جذب قصيرة، وجدولة نشر المحتوى على YouTube أو موجّهات أخرى.
- **اللحظات المميزة والمقاطع القصيرة** – اختيار اللحظات تلقائيًا، إنشاء صور مصغرة، ترجمات، ومقاطع جاهزة للنشر.
- **طبقة الربح** – اتصال بـ LazyingArt Coin للدعم المالي، دفع الاعتمادات، والتحويل إلى أصول على السلسلة.
- **الإنفاق والتركيز** – تتبع الإنفاق التشغيلي، إبراز الصيغ المربحة، وتلخيص نقاط قوتك لمشاريعك التالية.

### ميزات المستودع/التشغيل

- FastAPI backend بنقاط نهاية REST + WebSocket للاستقبال (`/api/v1/audio`, `/ws/audio-ingest`) وتوزيع البث المباشر (`/ws/stream`).
- تقسيم صوتي حتمي (افتراضيًا ~15 ثانية مع تداخل) إلى `backend/glass/audio_segments/`.
- تفريغ نصي مباشر اختياري باستخدام openai-whisper مع عتبات زمنية قابلة للضبط.
- تخزين دائم اختياري عبر Postgres (`DATABASE_URL`) للرسائل والصور والكتل والأجزاء والنصوص.
- لوحة تحكم PWA بموجة صوتية مباشرة، تحديثات نصية لحظية، ودعم التثبيت على سطح المكتب/الجوال.
- دعم البرامج الثابتة Arduino لعدسة + ميكروفون XIAO ESP32S3 Sense.

## 🔄 سير العمل النموذجي
<a id="sample-workflow"></a>

1. **الالتقاط** – تكلّم أو ارسم فكرة بسرعة؛ يقوم IdeasGlass بتفريغها وترجمتها وتصنيف النية.
2. **المشاركة التعاونية** – تقوم EchoMind بتنقيح الفكرة، إعداد السكربتات، واقتراح CTA مناسبة لكل منصة.
3. **النشر** – يعمل وكيل القناة على إنتاج الفيديوهات المميزة وصور المعرض تلقائيًا ويرفعها مع البيانات الوصفية.
4. **تحقيق الدخل** – تمرر الائتمانات عبر LazyingArt Coin (`coin.lazying.art`) وتزامن الدفعات مع المحافظ المفضلة.
5. **التقييم** – تظهر لك لوحة الإنفاق والوصول والتفاعل ما يجب تعزيزه في الخطوة التالية.

## 🗂️ هيكلة المشروع
<a id="project-structure"></a>

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
│   │   └── README.md
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

## 🧰 المتطلبات المسبقة
<a id="prerequisites"></a>

- Python 3.10+
- `pip` (أو بيئة conda ببايثون متوافق)
- اختياري: NVIDIA GPU + CUDA/cuDNN لرفع سرعة استدلال Whisper
- اختياري: PostgreSQL للتخزين
- للبرمجيات الثابتة: Arduino IDE أو `arduino-cli`، Seeed XIAO ESP32S3 Sense، مع تمكين PSRAM

| المكوّن | المتطلب | ملاحظات |
|---|---|---|
| وقت تشغيل الخادم الخلفي | Python 3.10+, `pip` | استخدم venv أو conda (`glass`) |
| تسريع عبر GPU (اختياري) | NVIDIA + CUDA/cuDNN | يحسن زمن تأخير Whisper |
| التخزين المستمر (اختياري) | PostgreSQL | يُفعّل عبر `DATABASE_URL` |
| سلسلة أدوات البرمجيات الثابتة | Arduino IDE / `arduino-cli` | استخدم ملف تعريف XIAO ESP32S3 مع PSRAM |

## ⚙️ التثبيت
<a id="installation"></a>

### تبعيات الخادم الخلفي

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### متطلبات البرمجيات الثابتة

- انسخ `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` إلى `wifi_credentials.h` (موصى به) ثم عيّن SSID/كلمة المرور.
- في Arduino IDE، اختر اللوحة `ESP32 -> XIAO_ESP32S3` و `PSRAM: OPI PSRAM`.
- مخطط الأقسام: `Default with spiffs (3MB APP/1.5MB SPIFFS)` أو `Maximum APP` عند عدم الحاجة لنظام الملفات.

### بناء/رفع البرمجيات الثابتة (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

إذا كان المنفذ مشغولًا: `fuser -k /dev/ttyACM0`.
إذا رفضت الأذونات: `sudo usermod -aG dialout $USER` ثم أعد تسجيل الدخول (أو مؤقتًا `sudo chmod a+rw /dev/ttyACM0`).

### تجربة الطاقة (XIAO ESP32S3)

- اضغط الزر ~0.8 ثانية أثناء الإقلاع للتمهيد.
- اضغط ~2.5 ثانية أثناء التشغيل للدخول في وضع النوم العميق.
- النبضة القصيرة أثناء التشغيل لا تزال تبدأ الالتقاط.

## ▶️ طريقة الاستخدام
<a id="usage"></a>

### تشغيل الخادم الخلفي (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### تشغيل الخادم الخلفي (مساعد)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### فتح لوحة التحكم

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| نقطة النهاية | الغرض |
|---|---|
| `/` | لوحة التحكم الأساسية (واجهة قابلة للعمل كـ PWA) |
| `/healthz` | فحص صحة الخادم الخلفي |
| `/ws/audio-ingest` | WebSocket استقبال من الجهاز |
| `/ws/stream` | بث مباشر للعملاء على لوحة التحكم |

### تسجيل الدخول وربط جهازك

1. سجّل أو ادخل عبر قسم الإعدادات/الحساب في لوحة التحكم.
2. اربط معرف جهازك في حقل `Bind device`.
3. فقط الأجهزة المرتبطة ستبث إلى حسابك.

توليد معرف جهاز وصورة QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

ربط عبر API (المصادقة عبر ملف تعريف الارتباط مطلوبة):

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

تحقق من الحساب والأجهزة المرتبطة حاليًا:

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

الترحيل الاختياري (إعادة تسمية البيانات التاريخية إلى معرف جهاز جديد):

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

## 🛠️ الإعدادات
<a id="configuration"></a>

### متغيرات البيئة الأساسية

- `DATABASE_URL`: DSN Postgres اختياري للتخزين المستمر.
- `IDEASGLASS_WHISPER_MODEL`: `base` (الافتراضي)، `small`، `medium`، `large-v3`، `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` أو `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` للدقة المختلطة عبر GPU، `0` لــ CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (الافتراضي) لتفعيل التفريغ النصي، `0` لتعطيله.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: فاصل التحديث المستمر للنص.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: عتبات مفصولة بفواصل (الافتراضي `3000,6000,15000`).

| المتغير | القيمة الافتراضية / الخيارات | التأثير |
|---|---|---|
| `DATABASE_URL` | غير مضبوط افتراضيًا | يتيح تخزين بيانات الحساب/الجهاز بشكل دائم |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | يتحكم في الدقة مقابل زمن التأخير |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` أو `cpu` | محرك الاستدلال |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU، `0` آمن لـ CPU | تحكم الدقة المختلطة |
| `IDEASGLASS_TRANSCRIBE` | `1` | تبديل مسار التفريغ النصي |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | مضبوط في وقت التشغيل | فاصل دفع النص المتحرك |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | عتبات إصدار النص التصاعدية |

نماذج آمنة لـ `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (مصادقة peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (مصادقة بكلمة مرور)

### ضبط مكسب الصوت والتجزئة

- `IDEASGLASS_GAIN_TARGET` (الافتراضي `0.032`)
- `IDEASGLASS_GAIN_MAX` (الافتراضي `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (الافتراضي `0.008`)
- `IDEASGLASS_SPEECH_RMS` (الافتراضي `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (الافتراضي `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (الافتراضي `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (الافتراضي `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (الافتراضي مساوي لمكسب الشظية)

| أداة ضبط الصوت | الافتراضي | الغرض |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | معايرة RMS الهدف |
| `IDEASGLASS_GAIN_MAX` | `1.8` | الحد الأعلى لتضخيم المكسب |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | حد أدنى لتجنب تضخيم الصمت شبه المطلق |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | خط أساس RMS لنشاط الكلام |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | هامش حول عتبة الكلام |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | مدة الهدف للتجزئة |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | تداخل التجزئات لثبات الاستمرارية |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | يرث مكسب الشظية | هدف المعايرة على مستوى المقاطع |

### تهيئة النموذج مسبقًا (اختياري)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 الأمثلة
<a id="examples"></a>

### إنشاء وربط معرف جهاز

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

ثم حدّد `kDeviceId` في:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

تدفق لوحة التحكم:

1. سجّل الدخول/أنشئ حسابًا في الإعدادات.
2. اربط الجهاز من لوحة الحساب.
3. فقط الأجهزة المرتبطة تُبث لحسابك.

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

## 🧭 ملاحظات التطوير
<a id="development-notes"></a>

### مجال التركيز

يحتوي هذا المستودع على مسارات خادمية متعددة. الإرشادات الحالية للمساهمين وتركيز التشغيل هو `backend/glass/` ما لم يطلب خلاف ذلك.

### فحص الصياغة

```bash
python -m compileall backend/glass/app.py
```

### وثائق المطور

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> ملاحظة: في لقطة المستودع الحالية، يبدو أن بعض الروابط التاريخية انتقلت (مثل ملاحظات الجسر المتاحة الآن في `references/ideasglass_bridge.md`). الروابط الأصلية محافظة كجزء من محتوى README الأساسي.

### سير عمل سريع لربط الجهاز (محفوظ)

- توليد المعرف (داخل conda `glass`): `python backend/glass/tools/generate_device_id.py`
- تعيينه في البرمجية الثابتة: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- شغّل الخادم وافتح `http://localhost:8765` وسجّل/سجّل الدخول، ثم اربط معرف الجهاز في لوحة الحساب

## 🆘 استكشاف الأخطاء
<a id="troubleshooting"></a>

- **المنفذ مستخدم بالفعل:** شغّل الخادم على منفذ آخر وحدث إعدادات العميل.
- **منفذ تسلسلي مشغول:** `fuser -k /dev/ttyACM0`.
- **رفض صلاحية المنفذ على لينكس:** `sudo usermod -aG dialout $USER` ثم أعد تسجيل الدخول.
- **Postgres غير متاح:** يمكن تشغيل الخادم دون قاعدة بيانات لوظائف جزئية؛ تحقق من `DATABASE_URL` وأعد التشغيل.
- **مشاكل أداء Whisper:** استخدم نماذج أصغر (`base`/`small`) أو عطّل التفريغ النصي عبر `IDEASGLASS_TRANSCRIBE=0`.
- **عدم استقرار TLS/تزامن الوقت على ESP32:** تحقق من Wi-Fi وتوفر NTP (UDP/123) وإعدادات الشهادة/المضيف؛ انظر `references/ideasglass_bridge.md` لملاحظات ميدانية مفصلة.
- **لا توجد تحديثات موجة حية:** افحص سجلات الخادم وخطأ المتصفح للبحث عن آثار `[IdeasGlass][wave]` وتحقق من اتصال `/ws/stream`.

## 🌐 روابط النظام البيئي
<a id="ecosystem-links"></a>

| العلامة | الغرض | الرابط |
|---|---|---|
| 🧠 EchoMind | رفيق ذكاء اصطناعي متعدد اللغات للتعلم والإبداع | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | مجتمع تحويل البحث إلى منتج للأفكار الجريئة | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | أتمتة تحويل الإنجازات الصغيرة إلى دخل | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | مسارات الفيزياء والكيمياء والمدونات | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | وكيل يحول الأفكار إلى مسودات ومهام ومنشورات | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | التقاط، ترجمة، وإنتاج مقاطع مميزة تلقائيًا | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | مكافآت وسداد ربط المساهمات بقيمة على السلسلة | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | دفتر ملاحظات أبحاث ومقالات | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | الاستوديو وراء OnlyIdeas وEchoMind وLazyEdit وIdeasGlass | [lazying.art](https://lazying.art) |

## 🙏 الشكر والتقدير
<a id="acknowledgements"></a>

نقف على أكتاف مشاريع مفتوحة رائعة — شكرًا لها:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">احصل على OmiGlass (BasedHardware)</a>
  - **برنامج الإحالة** — استخدم الكوبون `LazyingArt` لتوفير 10% (عمولة 30% تُفك بعد 10 مبيعات).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">احصل على OmiGlass مع LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">انضم إلى Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">اشترِ Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ خارطة الطريق
<a id="roadmap"></a>

- تعزيز وتوثيق مسار البث الصوتي الكامل عبر بيئات WAN/TLS.
- مواصلة تحسين جودة/زمن تفريغ النص (موازنات نموذج/جهاز/عتبات).
- توسيع إدارة الأجهزة وسير العمل متعدد الأجهزة المرتبطة بالحساب داخل لوحة التحكم.
- موائمة أو توحيد مسارات الخادم الخلفي القديمة/الموازية (`tornado_app`، `memo`، `memo_legacy`، `ngrok_bridge`) مع المسار الأساسي `backend/glass`.
- الحفاظ على تجديد ترجمات README متعددة اللغات ضمن `i18n/`.

## 🤝 المساهمة
<a id="contribution"></a>

المساهمات مرحب بها. للحصول على إرشادات سير العمل الخاصة بالمستودع، اتبع `AGENTS.md`.

التحقق المحلي الموصى به قبل فتح PR:

```bash
python -m compileall backend/glass/app.py
```

عند تقديم التغييرات:

- اجعل عناوين الـ commit قصيرة ودافعة وموجهة بالفعل (صيغة المضارع).
- اذكر متغيرات البيئة ذات الصلة (مثل `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) في ملاحظات PR عندما تتأثر السلوكيات بها.
- تضمين أدلة الاختبار (سجلات الخادم، سلوك لوحة التحكم، مخرجات البرمجيات الثابتة).
- لا ترفع أسرارًا (`DATABASE_URL`، رموز API، ملفات الاعتماد).

## 📄 الترخيص
<a id="license"></a>

لم يتم اكتشاف ملف `LICENSE` في جذر هذا المستودع في لقطة المستودع الحالية. حتى إضافة ملف ترخيص صريح، عُد استخدام المشروع وإعادة توزيعه يتطلب موافقة القائم على الصيانة.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
