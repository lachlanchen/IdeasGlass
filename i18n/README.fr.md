[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/logos/banner.png" alt="LazyingArt banner" />
</p>

# IdeasGlass

*Des lunettes IA portables qui transforment les idées en actions, revenus et élan créatif.*

> Pipeline IA portable orienté voix : capture depuis des lunettes ESP32, traitement dans FastAPI, et supervision/contrôle via un tableau de bord PWA en direct.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-dashboard-5A0FC8?logo=pwa&logoColor=white)

<table>
  <tr>
    <td align="center" style="padding:6px 10px;">
      <b>Écosystème</b><br/>
      <a href="https://lazying.art">LazyingArt</a>
      · <a href="https://onlyideas.art">OnlyIdeas</a>
      · <a href="https://chat.lazying.art">EchoMind</a>
      · <a href="https://coin.lazying.art">LazyingArt Coin</a>
    </td>
    <td align="center" style="padding:6px 10px;">
      <b>Soutenir IdeasGlass</b><br/>
      <a href="https://chat.lazying.art/donate"><img src="figs/donate_button.svg" alt="Donate" height="32" style="vertical-align: middle;"/></a>
    </td>
  </tr>
</table>

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>Interface de l'app (gauche) · Matériel (droite)</sub>
</div>

Explorez les expérimentations de la communauté sur <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Vue d'ensemble

IdeasGlass est un système portable orienté IA conçu pour la capture et l'exécution d'idées à la voix. Dans ce dépôt, le chemin d'exécution principal est :

- `backend/glass/` pour les API FastAPI, l'ingestion WebSocket, la transcription basée sur Whisper et le tableau de bord PWA installable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` pour le firmware XIAO ESP32S3 qui diffuse télémétrie/audio/photos.

Si vous découvrez ce dépôt, commencez par là.

### En un coup d'œil

| Zone | Emplacement principal | Rôle |
|---|---|---|
| API backend + PWA | `backend/glass/` | Endpoints FastAPI, ingestion/diffusion WebSocket, transcription, tableau de bord |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Client ESP32 de capture/streaming |
| Notes bridge | `references/ideasglass_bridge.md` | Notes de fiabilité TLS/WAN et conseils de déploiement terrain |
| Traductions du README | `i18n/` | Documentation multilingue synchronisée depuis le README canonique |

## ✨ Pourquoi IdeasGlass

IdeasGlass est un wearable orienté IA, conçu pour les personnes qui vivent dans des flux d'idées. Il capture, traduit, organise et exécute la créativité au moment même où l'inspiration surgit, que vous décriviez un concept en mouvement ou animiez une session en direct.

## 🧩 Fonctionnalités

### Fonctionnalités de vision produit

- **Matériel natif pour la création** – lunettes légères et entrées portables, optimisées pour la capture vocale avec raccourcis gestuels discrets.
- **Traduction instantanée** – détection/traduction de langue en temps réel pour idéer entre équipes ou publics sans changer d'outil.
- **Co-pilote EchoMind** – intégration étroite avec `chat.lazying.art` pour le brainstorming, la rédaction de scripts et l'accompagnement de contenu multilingue.
- **Pilote automatique des canaux** – rédige des plans, scripts longs, accroches courtes et planifie les publications sur YouTube ou d'autres flux.
- **Highlights & reels** – sélectionne automatiquement les moments, génère miniatures, sous-titres et clips prêts pour les réseaux.
- **Couche revenus** – connexion à LazyingArt Coin pour pourboires, paiements de crédits et conversion en actifs on-chain.
- **Dépenses & focus** – suit les coûts opérationnels, met en avant les formats rentables et synthétise vos forces personnelles pour les prochains projets.

### Fonctionnalités du dépôt/runtime

- Backend FastAPI avec endpoints REST + WebSocket pour l'ingestion (`/api/v1/audio`, `/ws/audio-ingest`) et la diffusion live (`/ws/stream`).
- Segmentation audio déterministe (par défaut ~15 s avec recouvrement) vers `backend/glass/audio_segments/`.
- Transcriptions streaming openai-whisper optionnelles avec seuils de latence configurables.
- Persistance Postgres optionnelle (`DATABASE_URL`) pour messages, photos, chunks, segments et transcriptions.
- Tableau de bord PWA avec forme d'onde live, mises à jour de transcription et installation desktop/mobile.
- Support firmware Arduino pour les flux caméra + micro XIAO ESP32S3 Sense.

## 🔄 Exemple de workflow

1. **Capture** – Parlez ou esquissez un concept ; IdeasGlass transcrit, traduit et étiquette l'intention.
2. **Co-création** – EchoMind affine l'idée, rédige des scripts et suggère des CTA adaptés à chaque plateforme.
3. **Publication** – L'agent de canal produit automatiquement des vidéos highlight, des images de galerie et les met en ligne avec les métadonnées.
4. **Monétisation** – Les crédits transitent via LazyingArt Coin (`coin.lazying.art`) et les paiements se synchronisent avec vos wallets préférés.
5. **Analyse** – Les tableaux de bord de dépenses, portée et engagement montrent où investir vos prochains efforts.

## 🗂️ Structure du projet

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

## 🧰 Prérequis

- Python 3.10+
- `pip` (ou environnement conda avec une version de Python compatible)
- Optionnel : GPU NVIDIA + CUDA/cuDNN pour accélérer l'inférence Whisper
- Optionnel : PostgreSQL pour la persistance
- Pour le firmware : Arduino IDE ou `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM activée

| Composant | Exigence | Notes |
|---|---|---|
| Exécution backend | Python 3.10+, `pip` | Utiliser venv ou conda (`glass`) |
| Accélération GPU (optionnelle) | NVIDIA + CUDA/cuDNN | Améliore la latence Whisper |
| Persistance (optionnelle) | PostgreSQL | Activée via `DATABASE_URL` |
| Toolchain firmware | Arduino IDE / `arduino-cli` | Utiliser le profil XIAO ESP32S3 avec PSRAM |

## ⚙️ Installation

### Dépendances backend

```bash
cd backend/glass
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Prérequis firmware

- Copiez `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` vers `wifi_credentials.h` (recommandé) et définissez SSID/mot de passe.
- Dans Arduino IDE, utilisez la carte `ESP32 -> XIAO_ESP32S3` avec `PSRAM: OPI PSRAM`.
- Schéma de partition : `Default with spiffs (3MB APP/1.5MB SPIFFS)` ou `Maximum APP` si le système de fichiers n'est pas nécessaire.

## ▶️ Utilisation

### Lancer le backend (uvicorn)

```bash
IDEASGLASS_WHISPER_MODEL=base IDEASGLASS_WHISPER_DEVICE=cuda \
uvicorn backend.glass.app:app \
  --host 0.0.0.0 \
  --port 8765 \
  --proxy-headers \
  --forwarded-allow-ips="*" \
  --reload
```

### Lancer le backend (helper)

```bash
python backend/glass/serve.py --whisper-model base --whisper-device cuda --reload
```

### Ouvrir le tableau de bord

- `http://localhost:8765/`
- `http://localhost:8765/healthz`

| Endpoint | Usage |
|---|---|
| `/` | Tableau de bord principal (UI compatible PWA) |
| `/healthz` | Vérification de disponibilité du backend |
| `/ws/audio-ingest` | WebSocket d'ingestion appareil |
| `/ws/stream` | Diffusion en direct vers les clients du tableau de bord |

### Connexion et association de votre appareil

1. Inscrivez-vous ou connectez-vous depuis la zone Settings/Account du tableau de bord.
2. Associez votre ID appareil dans le champ `Bind device`.
3. Seuls les appareils associés diffusent vers votre compte.

Générer un ID appareil + une image QR :

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Associer via l'API (session cookie requise) :

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Vérifier le compte courant et les appareils associés :

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Migration optionnelle (renommer les données historiques vers un nouvel ID appareil) :

```bash
curl -X POST http://localhost:8765/api/v1/devices/rename \
  -H 'Content-Type: application/json' \
  -d '{"from_id":"old-id","to_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

### Compilation/upload firmware (Arduino CLI)

```bash
FQBN='esp32:esp32:XIAO_ESP32S3:PartitionScheme=default_8MB,PSRAM=opi'
SKETCH='IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient'
PORT='/dev/ttyACM0'

bin/arduino-cli compile --fqbn "$FQBN" "$SKETCH"
bin/arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH"
```

Si le port est occupé : `fuser -k /dev/ttyACM0`.
Si permission refusée : `sudo usermod -aG dialout $USER` puis reconnectez-vous (ou temporairement `sudo chmod a+rw /dev/ttyACM0`).

### UX d'alimentation firmware (XIAO ESP32S3)

- Maintenez le bouton ~0,8 s au démarrage pour amorcer.
- Maintenez ~2,5 s pendant l'exécution pour passer en veille profonde.
- Un appui court pendant l'exécution déclenche toujours la capture.

## 🛠️ Configuration

### Variables d'environnement principales

- `DATABASE_URL` : DSN Postgres optionnel pour le stockage persistant.
- `IDEASGLASS_WHISPER_MODEL` : `base` (par défaut), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE` : `cuda` ou `cpu`.
- `IDEASGLASS_WHISPER_FP16` : `1` pour précision mixte GPU, `0` pour CPU.
- `IDEASGLASS_TRANSCRIBE` : `1` (par défaut) pour activer la transcription, `0` pour la désactiver.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` : intervalle de transcription glissant.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` : seuils séparés par virgule (par défaut `3000,6000,15000`).

| Variable | Valeur par défaut / options | Effet |
|---|---|---|
| `DATABASE_URL` | non défini par défaut | Active la persistance Postgres pour les données compte/appareil |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Contrôle précision vs latence |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` ou `cpu` | Backend d'inférence |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` sûr CPU | Contrôle de précision mixte |
| `IDEASGLASS_TRANSCRIBE` | `1` | Active/désactive le pipeline de transcription |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configuré à l'exécution | Intervalle de push de transcription glissante |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Seuils d'émission progressive de transcription |

Exemples sûrs de `DATABASE_URL` :

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (auth peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (auth par mot de passe)

### Réglages du gain audio et de la segmentation

- `IDEASGLASS_GAIN_TARGET` (par défaut `0.032`)
- `IDEASGLASS_GAIN_MAX` (par défaut `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (par défaut `0.008`)
- `IDEASGLASS_SPEECH_RMS` (par défaut `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (par défaut `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (par défaut `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (par défaut `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (par défaut : cible de gain du chunk)

| Réglage audio | Défaut | Rôle |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Cible de normalisation RMS |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Limite supérieure d'amplification du gain |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Plancher pour éviter d'amplifier le quasi-silence |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Base RMS de détection de parole |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Marge autour du seuil de parole |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Longueur cible des segments |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Recouvrement des segments pour la continuité |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hérite du gain chunk | Cible de normalisation au niveau segment |

### Préchargement de modèles (optionnel)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Exemples

### Générer et associer un ID appareil

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Puis définissez `kDeviceId` dans :

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Flux tableau de bord :

1. Inscription/connexion dans Settings.
2. Association de l'appareil dans le panneau Account.
3. Seuls les appareils associés diffusent vers votre compte.

### Exemples d'ingestion REST

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

## 🧭 Notes de développement

### Zone de focus

Ce dépôt contient plusieurs branches backend. La recommandation actuelle pour les contributeurs et l'exécution est `backend/glass/`, sauf demande contraire.

### Vérification statique/syntaxique

```bash
python -m compileall backend/glass/app.py
```

### Documentation développeur

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Remarque : dans l'état actuel du dépôt, certains liens historiques ci-dessus semblent avoir été déplacés (par exemple, les notes bridge existent maintenant à `references/ideasglass_bridge.md`). Les liens d'origine sont conservés comme contenu canonique du README.

### Association rapide d'appareil (workflow conservé)

- Générer un ID (dans conda `glass`) : `python backend/glass/tools/generate_device_id.py`
- Le définir dans le firmware : `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Lancer le backend et ouvrir `http://localhost:8765`, s'inscrire/se connecter, puis associer l'ID appareil dans le panneau Account

## 🆘 Dépannage

- **Port déjà utilisé :** lancez le backend sur un autre port et mettez à jour les paramètres client.
- **Port série occupé :** `fuser -k /dev/ttyACM0`.
- **Permission série Linux refusée :** `sudo usermod -aG dialout $USER` puis reconnectez-vous.
- **Postgres indisponible :** le backend peut fonctionner sans DB pour des fonctions partielles ; vérifiez `DATABASE_URL` puis redémarrez.
- **Problèmes de performance Whisper :** utilisez des modèles plus petits (`base`/`small`) ou désactivez la transcription via `IDEASGLASS_TRANSCRIBE=0`.
- **Instabilité TLS/synchronisation horaire sur ESP32 :** vérifiez Wi-Fi, disponibilité NTP (UDP/123), et paramètres cert/host ; consultez `references/ideasglass_bridge.md` pour des notes terrain détaillées.
- **Pas de mise à jour live de la forme d'onde :** vérifiez les logs backend et la console navigateur pour les traces `[IdeasGlass][wave]`, puis confirmez la connectivité `/ws/stream`.

## 🌐 Liens de l'écosystème

🧠 **EchoMind** — Compagnon IA multilingue pour l'apprentissage et la création.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Communauté recherche-produit pour des concepts audacieux.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatisations pour transformer de petites victoires en revenus.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Parcours et carnets de physique et de chimie.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent qui transforme les idées en brouillons, tâches et posts.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Capture, traduit et auto-produit des reels de highlights.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Récompenses et paiements reliant contributions et valeur on-chain.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Carnet de notes de recherche et d'essais.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio derrière OnlyIdeas, EchoMind, LazyEdit et IdeasGlass.  
[lazying.art](https://lazying.art)

## ❤️ Support & Contact

- ご支援は IdeasGlass のハードウェア試作・運用を加速させ、多くのクリエイターへ還元されます。
- 你的支持将帮助我们推进硬件、AI 工作流与生态建设，向社区持续开放。
- Votre soutien maintient la feuille de route wearable, agent et écosystème en mouvement.

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

- Pour les partenariats, écrivez à **contact@lazying.art** avec l'objet `IdeasGlass`.

IdeasGlass est l'endroit où les wearables IA cessent d'écouter et commencent à construire avec vous.

## 🙏 Remerciements

Nous nous appuyons sur d'excellents projets open source — merci à :

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Referral Program** — Use coupon `LazyingArt` to save 10% (30% commission unlocks after 10 sales).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Feuille de route

- Renforcer et documenter le chemin complet de streaming audio dans des environnements WAN/TLS.
- Continuer d'améliorer les compromis qualité/latence des transcriptions (presets modèle/appareil/seuil).
- Étendre la gestion d'appareils et les workflows multi-appareils par compte dans le tableau de bord.
- Aligner ou consolider les branches backend historiques/parallèles (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) avec le chemin principal `backend/glass`.
- Maintenir et rafraîchir les variantes multilingues du README sous `i18n/`.

## 🤝 Contribution

Les contributions sont bienvenues. Pour les règles de workflow spécifiques au dépôt, suivez `AGENTS.md`.

Validation locale recommandée avant d'ouvrir une PR :

```bash
python -m compileall backend/glass/app.py
```

Lors de la soumission de changements :

- Gardez des sujets de commit courts et orientés action (présent).
- Mentionnez les variables d'environnement pertinentes (par exemple `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) dans les notes de PR lorsque le comportement en dépend.
- Incluez des preuves de test (logs backend, comportement dashboard, sortie firmware).
- Ne committez jamais de secrets (`DATABASE_URL`, jetons API, fichiers d'identifiants).

## 📄 Licence

Aucun fichier `LICENSE` à la racine n'a été détecté dans cet état du dépôt. Tant qu'un fichier de licence explicite n'est pas ajouté, considérez que l'utilisation et la redistribution nécessitent l'accord du mainteneur.
