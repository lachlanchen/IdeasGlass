[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*نظارة AI قابلة للارتداء تحول الأفكار إلى أفعال ودخل وزخم إبداعي متواصل.*

> خط إنتاج AI يبدأ بالصوت أولًا: التقاط من نظارات ESP32، معالجة في FastAPI، ومراقبة/تحكم عبر لوحة PWA حيّة.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| المسار | الهدف |
|---|---|
| 🎙️ الالتقاط القابل للارتداء | ترسل نظارات ESP32 الصوت والصور وبيانات التتبع بشكل شبه لحظي |
| 🧠 ذكاء الخلفية | تستهلك FastAPI البث، وتحوّل الصوت إلى نص، وتقسمه، وتحفظ البيانات الوصفية |
| 🖥️ لوحة التحكم | تعرض لوحة PWA الموجة الصوتية الحيّة والتفريغ والنشاط الخاص بالجهاز والحساب |

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>النظام البيئي</b><br/>
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
  <sub>واجهة التطبيق (اليسار) · العتاد (اليمين)</sub>
</div>

استكشف تجارب المجتمع في <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 النظرة العامة

IdeasGlass هو نظام AI-first للبسّ القابل للارتداء يركّز على التقاط الأفكار صوتيًا وتنفيذها. في هذا المستودع، المسار التشغيلي الأساسي هو:

- `backend/glass/` لواجهات FastAPI وعمليات WebSocket ingest، تفريغ Whisper، ولوحة PWA القابلة للتثبيت.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` لبرمجية XIAO ESP32S3 التي تبث بيانات الاستشعار والصوت والصور.

إذا كانت هذه أول مرة تتعامل مع هذا المستودع، ابدأ من هنا أولًا.

### لمحة سريعة

| المجال | الموقع الأساسي | الوظيفة |
|---|---|---|
| Backend API + PWA | `backend/glass/` | نقاط نهاية FastAPI، استقبال وتوزيع WebSocket، تفريغ، لوحة تحكم |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | عميل ESP32 لالتقاط وبث البيانات |
| ملاحظات الجسر | `references/ideasglass_bridge.md` | ملاحظات موثوقية TLS/WAN ونصائح النشر الميداني |
| ترجمات README | `i18n/` | مستندات متعددة اللغات مزامنة من النسخة الأساسية |

## ✨ لماذا IdeasGlass

IdeasGlass هو جهاز AI-first قابل للارتداء صُمم للأشخاص الذين يعملون داخل تدفق مستمر من الأفكار. يلتقط الإبداع، ويترجمه، ويُنظّمه، وينفّذه لحظة الإلهام، سواءً كنت تُملي فكرة أثناء الحركة أو تدير جلسة مباشرة.

## 🧩 الميزات

### ميزات الرؤية

- **عتاد مخصص للإبداع** – نظارات خفيفة ومدخلات ارتداء مريحة، مُحسّنة لالتقاط الصوت أولًا مع اختصارات إيماءات دقيقة.
- **الترجمة الفورية** – كشف وترجمة فورية للغة كي تستطيع العصف الذهني عبر الفرق أو الجمهور دون تغيير الأدوات.
- **مساعد EchoMind** – تكامل قوي مع `chat.lazying.art` للعصف الذهني، صياغة النصوص، وتوجيه المحتوى متعدد اللغات.
- **التحكم التلقائي بالقنوات** – توليد مخططات، نصوص طويلة، مقاطع قصيرة، وجدولة النشر على YouTube أو أي منصة أخرى.
- **اللحظات البارزة والمقاطع القصيرة** – اختيار اللحظات تلقائيًا، وتوليد صور مصغرة، ترجمات، ومقاطع جاهزة للمنصات الاجتماعية.
- **طبقة الدخل** – اتصال بـ LazyingArt Coin للتبرعات والإكراميات، ودفع الائتمان، والتحويل إلى أصول على الشبكة.
- **تحسين الإنفاق والتركيز** – تتبّع الإنفاق التشغيلي، إبراز الصيغ المربحة، وتحويل نقاط قوتك إلى مشاريع لاحقة.

### ميزات التشغيل والمستودع

- FastAPI backend مع نقاط REST + WebSocket للاستقبال (`/api/v1/audio`, `/ws/audio-ingest`) والتوزيع المباشر للبث (`/ws/stream`).
- تقسيم صوتي حتمي (الافتراضي `~15` ثانية مع تداخل) داخل `backend/glass/audio_segments/`.
- تفريغ صوتي تدريجي عبر openai-whisper اختيارى مع عتبات زمنية قابلة للضبط.
- تخزين اختياري في Postgres (`DATABASE_URL`) للرسائل والصور والقطع الصوتية والمقاطع النصية.
- لوحة PWA تعرض شكل الموجة الصوتية الحية، وتحديثات النص الفوري، ودعم التثبيت على سطح المكتب/الجوال.
- دعم firmware لـ Arduino مع مسارات كاميرا + ميكروفون XIAO ESP32S3 Sense.

## 🔄 مسار العمل النموذجي

1. **الالتقاط** – تحدّث أو ارسم الفكرة؛ يقوم IdeasGlass بتفريغها وترجمتها ووضع علامة على النية.
2. **المشاركة الإبداعية** – يقوم EchoMind بتنقيح الفكرة وصياغة النصوص واقتراح CTAs مناسبة لكل منصة.
3. **النشر** – ينتج وسيط القناة مقاطع مميزة، وصور معرض، ويرفعها مع البيانات الوصفية.
4. **تحقيق الدخل** – تمرر الاعتمادات عبر LazyingArt Coin (`coin.lazying.art`) وتُزامَن عمليات السحب إلى محافظك المفضلة.
5. **المراجعة** – تعرض لوحات الإنفاق والوصول والمشاركة ما يجب تكثيفه بعد ذلك.

## 🗂️ هيكلة المشروع

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
- `pip` (أو بيئة conda مع نسخة Python متوافقة)
- اختياري: NVIDIA GPU + CUDA/cuDNN لاشتقاق Whisper أسرع
- اختياري: PostgreSQL للحفظ الدائم
- للـ firmware: Arduino IDE أو `arduino-cli`، Seeed XIAO ESP32S3 Sense، وتمكين PSRAM

| المكوّن | المتطلب | ملاحظات |
|---|---|---|
| تشغيل Backend | Python 3.10+, `pip` | استخدم venv أو conda (`glass`) |
| تسريع GPU (اختياري) | NVIDIA + CUDA/cuDNN | يخفف زمن الكمون في Whisper |
| تخزين دائم (اختياري) | PostgreSQL | يُفعّل عبر `DATABASE_URL` |
| سلسلة أدوات Firmware | Arduino IDE / `arduino-cli` | استخدم ملف تعريف XIAO ESP32S3 مع PSRAM |

## ⚙️ التثبيت

### تبعيات Backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### متطلبات Firmware

- انسخ `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` إلى `wifi_credentials.h` (مُستحسن) وحدد SSID وpassword.
- في Arduino IDE استخدم اللوحة `ESP32 -> XIAO_ESP32S3` مع `PSRAM: OPI PSRAM`.
- مخطط التقسيم: `Default with spiffs (3MB APP/1.5MB SPIFFS)` أو `Maximum APP` إذا لم تكن الملفات مطلوبة.

## ▶️ الاستخدام

### تشغيل backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### تشغيل backend (أداة مساعد)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### فتح لوحة التحكم

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| المسار | الغرض |
|---|---|
| `/` | اللوحة الرئيسية (واجهة PWA) |
| `/healthz` | فحص نشاط الخادم |
| `/ws/audio-ingest` | WebSocket استقبال الجهاز |
| `/ws/stream` | توزيع البث الحي إلى عملاء لوحة التحكم |

### تسجيل الدخول وربط جهازك

1. أنشئ حسابًا أو سجّل الدخول من Settings / Account.
2. اربط `device_id` في حقل `Bind device`.
3. فقط الأجهزة المربوطة ستبث إلى حسابك.

إنشاء معرف الجهاز + صورة QR:

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

الربط عبر API (يحتاج جلسة cookie):

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

الترحيل الاختياري (إعادة تسمية بيانات تاريخية إلى معرف جديد):

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

إذا كان المنفذ مشغولاً: `fuser -k /dev/ttyACM0`.
إذا ظهرت مشكلة صلاحية: `sudo usermod -aG dialout $USER` ثم أعد تسجيل الدخول (أو مؤقتًا `sudo chmod a+rw /dev/ttyACM0`).

### تجربة الطاقة في Firmware (XIAO ESP32S3)

- اضغط الزر ~0.8 ثانية عند التشغيل للإقلاع.
- اضغط ~2.5 ثانية أثناء التشغيل للدخول في وضع النوم العميق.
- الضغط القصير أثناء التشغيل ما زال يفعّل الالتقاط.

## 🛠️ الإعداد

### متغيرات البيئة الأساسية

- `DATABASE_URL`: DSN اختياري لـ Postgres للتخزين الدائم.
- `IDEASGLASS_WHISPER_MODEL`: `base` (الافتراضي)، `small`، `medium`، `large-v3`، `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE`: `cuda` أو `cpu`.
- `IDEASGLASS_WHISPER_FP16`: `1` للدقة المختلطة على GPU، و`0` لـ CPU.
- `IDEASGLASS_TRANSCRIBE`: `1` (افتراضي) لتفعيل التفريغ النصي، `0` لتعطيله.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS`: فاصل النص المتجدّد.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`: عتبات مفصولة بفواصل (الافتراضي `3000,6000,15000`).

| المتغير | الافتراضي / الخيارات | التأثير |
|---|---|---|
| `DATABASE_URL` | غير مضبوط افتراضيًا | يفعّل حفظ Postgres لبيانات الحساب والجهاز |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | يوازن بين الدقة والكمون |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` أو `cpu` | محرك الاستنتاج |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU، `0` آمن للـ CPU | التحكم في الدقة المختلطة |
| `IDEASGLASS_TRANSCRIBE` | `1` | تشغيل/إيقاف خط التفريغ |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | مضبوط حسب التشغيل | فاصل دفع النص المتجدّد |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | عتبات إصدار النص تدريجيًا |

أمثلة آمنة لـ `DATABASE_URL`:

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (مصادقة peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (مصادقة بكلمة مرور)

### ضبط الكسب والتقسيم الصوتي

- `IDEASGLASS_GAIN_TARGET` (الافتراضي `0.032`)
- `IDEASGLASS_GAIN_MAX` (الافتراضي `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (الافتراضي `0.008`)
- `IDEASGLASS_SPEECH_RMS` (الافتراضي `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (الافتراضي `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (الافتراضي `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (الافتراضي `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (يُفترض أنه نفس هدف الكسب للجزء)

| إعداد الصوت | الافتراضي | الغرض |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | تطبيع RMS إلى الهدف |
| `IDEASGLASS_GAIN_MAX` | `1.8` | حد أعلى لتضخيم الكسب |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | حد أدنى لمنع تضخيم الصمت شبه التام |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | خط أساس RMS لنشاط الكلام |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | هامش حول عتبة الكلام |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | طول المقطع الهدف |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | تداخل المقاطع لضمان الاستمرارية |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | يرث قيمة كسب الجزء | هدف التطبيع على مستوى المقطع |

### استرجاع النماذج مسبقًا (اختياري)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 أمثلة

### إنشاء وربط معرف جهاز

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

ثم حدّث `kDeviceId` في:

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

تدفق لوحة التحكم:

1. أنشئ حسابًا / سجّل الدخول من Settings.
2. اربط الجهاز من لوحة Account.
3. لا تبث الأجهزة غير المربوطة إلى حسابك.

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

يحتوي هذا المستودع على مسارات backend متعددة. الإرشاد الحالي للمساهمين والتركيز التشغيلي هو `backend/glass/` ما لم يُطلب غير ذلك.

### فحص ثابت/تركيبي

```bash
python -m compileall backend/glass/app.py
```

### مستندات المطور

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> ملاحظة: في لقطة المستودع الحالية، تظهر بعض الروابط التاريخية بأنها قد تكون تغيرت (مثلًا توجد الآن ملاحظات الجسر في `references/ideasglass_bridge.md`). تم الإبقاء على الروابط الأصلية كنص توثيقي canonical داخل README.

### ربط سريع للجهاز (workflow محفوظ)

- إنشاء المعرف (داخل conda `glass`): `python backend/glass/tools/generate_device_id.py`
- تعيينه داخل Firmware: `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- شغّل Backend وافتح `http://localhost:8765`، ثم سجّل/ادخل، وربط معرف الجهاز ضمن لوحة Account.

## 🆘 استكشاف الأخطاء وإصلاحها

- **المنفذ مستخدم مسبقًا:** شغّل backend على منفذ آخر وحدث إعدادات العميل.
- **المنفذ التسلسلي مشغول:** `fuser -k /dev/ttyACM0`.
- **رفض صلاحية المنفذ على Linux:** `sudo usermod -aG dialout $USER` وأعد تسجيل الدخول.
- **Postgres غير متاح:** يمكن تشغيل backend بدون DB لوظائف جزئية؛ تحقق من `DATABASE_URL` وأعد التشغيل.
- **مشاكل أداء Whisper:** استخدم نماذج أصغر (`base`/`small`) أو عطّل التفريغ عبر `IDEASGLASS_TRANSCRIBE=0`.
- **عدم استقرار TLS/مزامنة الوقت على ESP32:** تحقق من Wi-Fi، توفر NTP (UDP/123)، وإعدادات الشهادة/المضيف؛ راجع `references/ideasglass_bridge.md` لملاحظات ميدانية مفصّلة.
- **لا توجد تحديثات لموجة الصوت الحية:** افحص سجلات backend ووحدة تحكم المتصفح لآثار `[IdeasGlass][wave]` وتأكد من اتصال `/ws/stream`.

## 🌐 روابط النظام البيئي

🧠 **EchoMind** — رفيق AI متعدد اللغات للتعلم والإبداع.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — مجتمع يربط البحث بالمنتج للأفكار الجريئة.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — أوتوماتيكيات لتحويل الإنجازات الصغيرة إلى دخل.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — مسارات ودفاتر للفيزياء والكيمياء.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — وكيل يحول الأفكار إلى مسودات، مهام، ومنشورات.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — التقاط، ترجمة، وإنتاج تلقائي لــ reels مميزة.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — مكافآت ودفع وصل بين المساهمات والقيمة على السلسلة.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — دفتر ملاحظات بحث ومقالات.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — استوديو خلف OnlyIdeas وEchoMind وLazyEdit وIdeasGlass.  
[lazying.art](https://lazying.art)

## 🙏 الشكر والتقدير

نقف على أكتاف مشاريع مفتوحة عظيمة — شكرًا لهم جميعًا:

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — استخدم قسيمة `LazyingArt` لتوفير 10% (سيُفتح 30% من العمولة بعد 10 مبيعات).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ خارطة الطريق

- تقوية وتوثيق مسار بث الصوت من النهاية إلى النهاية عبر بيئات WAN/TLS.
- استمرار تحسين توازن جودة/زمن التفريغ (إعدادات النموذج/الجهاز/العتبات).
- توسيع إدارة الأجهزة وسير العمل متعدد الأجهزة ضمن الحساب في لوحة التحكم.
- توحيد أو دمج مسارات backend القديمة/الموازية (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) مع المسار الأساسي `backend/glass`.
- الحفاظ على تحديث نسخ README متعددة اللغات داخل `i18n/`.

## 🤝 المساهمة

المساهمات مرحب بها. لإرشادات سير العمل الخاصة بهذا المستودع، اتبع `AGENTS.md`.

موصى به للتحقق محليًا قبل فتح PR:

```bash
python -m compileall backend/glass/app.py
```

عند إرسال التغييرات:

- اجعل عناوين الالتزام قصيرة وموجهة للفعل (صيغة الحاضر).
- اذكر متغيرات البيئة ذات الصلة (مثل `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) في ملاحظات PR عندما يؤثر سلوكها.
- أدرج أدلة اختبار (سجلات backend، سلوك لوحة التحكم، مخرجات firmware).
- لا تُخزّن أسرارًا (`DATABASE_URL`، توكنات API، ملفات الاعتمادات).

## 📄 الترخيص

لم يتم الكشف عن ملف `LICENSE` في جذر هذا المستودع ضمن لقطة العمل الحالية. حتى إضافة ملف ترخيص رسمي، اعتبر أن الاستخدام وإعادة التوزيع يتطلبان موافقة صريحة من المشرف.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
