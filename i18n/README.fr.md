[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)


# IdeasGlass

*Un wearable IA qui transforme les idées en actions, en revenus et en élan créatif.*

> Pipeline wearable orienté voix : capture depuis des lunettes ESP32, traitement dans FastAPI, et supervision/contrôle via un tableau de bord PWA en temps réel.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Piste | Objectif |
|---|---|
| 🎙️ Capture wearable | Les lunettes ESP32 envoient audio, photos et télémétrie quasi en temps réel |
| 🧠 Intelligence backend | FastAPI ingère les flux, transcrit, segmente et persiste les métadonnées |
| 🖥️ Tableau de bord | Le PWA affiche l'onde, les transcriptions et l'état du périphérique/compte |

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
  <sub>UI de l'application (gauche) · Matériel (droite)</sub>
</div>

Explorez les expériences communautaires sur <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Aperçu

IdeasGlass est un système wearable IA d'abord pensé pour la capture et l'exécution d'idées par la voix. Dans ce dépôt, le chemin d'exécution principal est :

- `backend/glass/` pour les API FastAPI, l'ingestion WebSocket, la transcription basée sur Whisper et le tableau de bord PWA installable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` pour le firmware XIAO ESP32S3 qui envoie télémétrie/audio/photos.

Si vous découvrez ce dépôt, commencez par là.

### En bref

| Domaine | Emplacement principal | Fonctions |
|---|---|---|
| API backend + PWA | `backend/glass/` | Endpoints FastAPI, ingestion/fanout WebSocket, transcription, tableau de bord |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Client de capture/streaming ESP32 |
| Notes de bridge | `references/ideasglass_bridge.md` | Notes de fiabilité TLS/WAN et conseils de déploiement terrain |
| Traductions README | `i18n/` | Documentation multilingue synchronisée depuis le README canonique |

## ✨ Pourquoi IdeasGlass

IdeasGlass est un wearable IA pensé pour les personnes qui évoluent dans des flux d'idées. Il capture, traduit, organise et transforme la créativité au moment de l'inspiration, que vous récitiez un concept en mouvement ou animiez une session en direct.

## 🧩 Fonctionnalités

### Fonctionnalités de la vision produit

- **Matériel natif pour la création** – lunettes légères et entrées wearables, optimisées pour la capture vocale et les raccourcis gestuels discrets.
- **Traduction instantanée** – détection/traduction de langue en temps réel pour collaborer entre équipes ou publics sans changer d'outil.
- **Co-pilote EchoMind** – couplage serré avec `chat.lazying.art` pour le brain storming, la rédaction de scripts et l'accompagnement multilingue de contenu.
- **Pilotage automatique des canaux** – crée des plans, scripts longs, accroches courtes et planifie les uploads sur YouTube ou d'autres flux.
- **Temps forts et reels** – sélectionne automatiquement les moments, génère miniatures, sous-titres et clips prêts pour les réseaux.
- **Couche revenus** – se connecte à LazyingArt Coin pour les pourboires, le paiement de crédits et la conversion vers des actifs on-chain.
- **Suivi des dépenses et focus** – suit les dépenses opérationnelles, met en avant les formats rentables et synthétise vos points forts pour les prochains projets.

### Fonctionnalités dépôt/runtime

- Backend FastAPI avec endpoints REST + WebSocket pour ingestion (`/api/v1/audio`, `/ws/audio-ingest`) et fanout de flux en direct (`/ws/stream`).
- Segmentation audio déterministe (par défaut ~15 s avec recouvrement) vers `backend/glass/audio_segments/`.
- Transcriptions streaming openai-whisper optionnelles avec seuils de latence configurables.
- Persistance Postgres optionnelle (`DATABASE_URL`) pour messages, photos, chunks, segments et transcriptions.
- Tableau de bord PWA avec forme d'onde live, mises à jour de transcription et support d'installation desktop/mobile.
- Support firmware Arduino pour les flux caméra + micro XIAO ESP32S3 Sense.

## 🔄 Flux de travail

1. **Capture** – Parlez ou esquissez une idée ; IdeasGlass transcrit, traduit et étiquette l'intention.
2. **Co-création** – EchoMind affine l'idée, rédige des scripts et suggère des CTA adaptés à chaque plateforme.
3. **Publication** – L'agent de canal génère automatiquement des vidéos en highlights, des images de galerie et les publie avec métadonnées.
4. **Monétisation** – Les crédits transitent via LazyingArt Coin (`coin.lazying.art`) et les paiements se synchronisent avec vos wallets.
5. **Réflexion** – Les tableaux de bord de dépenses, portée et engagement révèlent ce sur quoi doubler vos efforts.

## 🗂️ Structure du projet

```text
IdeasGlass/
├── README.md
├── i18n/                                  # Traductions du README
├── backend/
│   ├── glass/                             # Backend FastAPI + PWA principal
│   │   ├── app.py
│   │   ├── serve.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   ├── tools/
│   │   └── audio_segments/
│   ├── tornado_app/                       # Chemin d'ingestion backend secondaire/parallèle
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/IdeasGlassClient.ino
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Notes Bridge + déploiement
├── docs/                                  # Ressources docs/site supplémentaires
├── development_plan/
├── app/
├── ops/observability/
├── figs/
└── seeed_studio_xiao_esp32s3_dev/
```

## 🧰 Prérequis

- Python 3.10+
- `pip` (ou environnement conda avec version Python compatible)
- Optionnel : GPU NVIDIA + CUDA/cuDNN pour une inférence Whisper plus rapide
- Optionnel : PostgreSQL pour la persistance
- Pour le firmware : Arduino IDE ou `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM activée

| Composant | Exigence | Notes |
|---|---|---|
| Runtime backend | Python 3.10+, `pip` | Utiliser venv ou conda (`glass`) |
| Accélération GPU (optionnel) | NVIDIA + CUDA/cuDNN | Améliore la latence Whisper |
| Persistance (optionnel) | PostgreSQL | Activée via `DATABASE_URL` |
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

- Copiez `IdeaGlass/firmware/ideasglass_arduino/wifi_credentials.example.h` vers `wifi_credentials.h` (recommandé) et configurez SSID/mot de passe.
- Dans Arduino IDE, utilisez la carte `ESP32 -> XIAO_ESP32S3` avec `PSRAM: OPI PSRAM`.
- Schéma de partition : `Default with spiffs (3MB APP/1.5MB SPIFFS)` ou `Maximum APP` quand le système de fichiers n'est pas nécessaire.

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

| Endpoint | Objet |
|---|---|
| `/` | Dashboard principal (UI compatible PWA) |
| `/healthz` | Vérification de vivacité backend |
| `/ws/audio-ingest` | WebSocket d'ingestion device |
| `/ws/stream` | Fanout de flux en direct vers les clients dashboard |

### Connexion et liaison de votre appareil

1. Inscrivez-vous ou connectez-vous depuis les paramètres/compte du tableau de bord.
2. Liez votre device ID dans le champ `Bind device`.
3. Seuls les appareils liés vont diffuser vers votre compte.

Générez un ID appareil + une image QR :

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Liez via l'API (session cookie requise) :

```bash
curl -X POST http://localhost:8765/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"<your-device-id>"}' \
  -b cookies.txt -c cookies.txt
```

Vérifiez le compte courant et les appareils liés :

```bash
curl -s http://localhost:8765/api/v1/auth/me -b cookies.txt -c cookies.txt | jq
```

Migration optionnelle (renommer les données historiques vers un nouvel ID appareil) :

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

Si le port est occupé : `fuser -k /dev/ttyACM0`.
Si l'autorisation est refusée : `sudo usermod -aG dialout $USER` puis reconnectez-vous (ou temporairement `sudo chmod a+rw /dev/ttyACM0`).

### UX d'alimentation firmware (XIAO ESP32S3)

- Maintenez le bouton ~0.8 s à la mise sous tension pour démarrer.
- Maintenez ~2.5 s en fonctionnement pour entrer en veille profonde.
- Une pression courte en fonctionnement déclenche toujours la capture.

## 🛠️ Configuration

### Variables d'environnement principales

- `DATABASE_URL` : DSN Postgres optionnel pour le stockage persistant.
- `IDEASGLASS_WHISPER_MODEL` : `base` (par défaut), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE` : `cuda` ou `cpu`.
- `IDEASGLASS_WHISPER_FP16` : `1` pour precision mixte GPU, `0` pour CPU.
- `IDEASGLASS_TRANSCRIBE` : `1` (par défaut) pour activer la transcription, `0` pour la désactiver.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` : intervalle roulant des transcriptions.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` : seuils séparés par virgules (par défaut `3000,6000,15000`).

| Variable | Valeur par défaut / options | Effet |
|---|---|---|
| `DATABASE_URL` | non défini par défaut | Active la persistance Postgres pour les données compte/appareil |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Contrôle le compromis précision/latence |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` ou `cpu` | Moteur d'inférence |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU | Contrôle de la précision mixte |
| `IDEASGLASS_TRANSCRIBE` | `1` | Active/désactive le pipeline de transcription |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configuré à l'exécution | Intervalle d'envoi de transcription en continu |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Seuils d'émission progressive de la transcription |

Exemples sûrs pour `DATABASE_URL` :

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (authentification peer/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (authentification par mot de passe)

### Réglages de gain et segmentation audio

- `IDEASGLASS_GAIN_TARGET` (par défaut `0.032`)
- `IDEASGLASS_GAIN_MAX` (par défaut `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (par défaut `0.008`)
- `IDEASGLASS_SPEECH_RMS` (par défaut `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (par défaut `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (par défaut `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (par défaut `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (par défaut : cible de gain par chunk)

| Réglage audio | Valeur par défaut | Objet |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Normalisation RMS cible |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Limite haute d'amplification du gain |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Seuil minimum pour éviter d'amplifier le quasi-silence |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Référence RMS de détection de parole |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Marge autour du seuil de parole |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Durée cible de segment |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Recouvrement de segment pour la continuité |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hérite du gain chunk | Cible de normalisation au niveau segment |

### Préchargement du modèle (optionnel)

```bash
python backend/glass/tools/prefetch_whisper_models.py \
  --models tiny,base,small,medium,large-v3 \
  --device cuda \
  --fp16 1
```

## 🧪 Exemples

### Générer et lier un ID appareil

```bash
python backend/glass/tools/generate_device_id.py --out logs/device-id.png
```

Puis définissez `kDeviceId` dans :

- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino`

Parcours dashboard :

1. Inscrivez-vous/connectez-vous dans Settings.
2. Liez l'appareil dans le panneau Account.
3. Seuls les appareils liés diffusent vers votre compte.

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
    "photo_base64":"'"$(base64 -w0 sample.jpg)'",
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
    "audio_base64":"'"$(base64 -w0 temp.raw)'"
  }'
```

```bash
curl http://localhost:8765/api/v1/audio/segments | jq '.[0]'
curl -o latest.wav http://localhost:8765/api/v1/audio/segments/<segment-id>
```

## 🧭 Notes de développement

### Zone de focus

Ce dépôt contient plusieurs pistes backend. L'orientation actuelle pour les contributeurs et l'exécution est `backend/glass/`, sauf demande contraire.

### Vérification statique/syntaxique

```bash
python -m compileall backend/glass/app.py
```

### Docs développeur

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Multi-platform App / PWA Plan](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Note : dans l'instantané actuel du dépôt, certains liens historiques ci-dessus semblent avoir été déplacés (par exemple, les notes de bridge existent désormais dans `references/ideasglass_bridge.md`). Les liens d'origine sont conservés comme contenu canonical du README.

### Workflow de liaison appareil (conservé)

- Générez un ID (dans conda `glass`) : `python backend/glass/tools/generate_device_id.py`
- Positionnez-le dans le firmware : `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Lancez le backend puis ouvrez `http://localhost:8765`, inscrivez-vous/connectez-vous, puis liez l'ID appareil dans le panneau Account

## 🆘 Dépannage

- **Port déjà utilisé :** lancez le backend sur un autre port et mettez à jour les paramètres du client.
- **Port série occupé :** `fuser -k /dev/ttyACM0`.
- **Permission série Linux refusée :** `sudo usermod -aG dialout $USER` et reconnectez-vous.
- **Postgres indisponible :** le backend peut fonctionner sans base pour une fonctionnalité partielle ; vérifiez `DATABASE_URL` puis redémarrez.
- **Problèmes de performance Whisper :** utilisez des modèles plus petits (`base`/`small`) ou désactivez la transcription via `IDEASGLASS_TRANSCRIBE=0`.
- **Instabilité TLS/synchronisation temporelle sur ESP32 :** vérifiez Wi-Fi, disponibilité NTP (UDP/123), et les réglages cert/host ; voir `references/ideasglass_bridge.md` pour notes terrain détaillées.
- **Aucun rafraîchissement d'onde en direct :** vérifiez les logs backend et la console navigateur pour les traces `[IdeasGlass][wave]` et confirmez la connectivité `/ws/stream`.

## 🌐 Liens de l'écosystème

🧠 **EchoMind** — Compagnon IA multilingue pour apprendre et créer.  
[chat.lazying.art](https://chat.lazying.art)

🌱 **OnlyIdeas** — Communauté de recherche-to-produit pour des concepts audacieux.  
[onlyideas.art](https://onlyideas.art)

💸 **LazyEarn** — Automatisations pour transformer de petites victoires en revenus.  
[earn.lazying.art](https://earn.lazying.art)

📚 **LazyLearn** — Parcours de physique et chimie, et carnets de notes.  
[learn.lazying.art](https://learn.lazying.art)

🤖 **IdeasRobot** — Agent qui transforme idées en drafts, tâches et posts.  
[robot.lazying.art](https://robot.lazying.art)

👓 **IdeasGlass** — Capture, traduit et produit automatiquement des highlights reels.  
[glass.lazying.art](https://glass.lazying.art)

🪙 **LazyingArt Coin** — Récompenses et paiements reliant contributions et valeur on-chain.  
[coin.lazying.art](https://coin.lazying.art)

🧪 **IDEAS** — Carnet de notes et d'essais de recherche.  
[ideas.onlyideas.art](https://ideas.onlyideas.art)

🎨 **LazyingArt** — Studio derrière OnlyIdeas, EchoMind, LazyEdit et IdeasGlass.  
[lazying.art](https://lazying.art)

## 🙏 Remerciements

Nous nous appuyons sur d'excellents projets open source — merci à :

- <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass (BasedHardware)</a>
  - **Programme de parrainage** — Utilisez le coupon `LazyingArt` pour économiser 10% (commission de 30% débloquée après 10 ventes).

    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.3rem 0;">
      <a href="https://www.omi.me/?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1.1rem;border-radius:999px;background:#111827;color:#ffffff;font-weight:700;text-decoration:none;">Get OmiGlass with LazyingArt</a>
      <a href="https://discord.com/invite/8MP3b9ymvx?ref=LazyingArt" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#2563eb;color:#ffffff;font-weight:700;text-decoration:none;">Join Omi Discord</a>
      <a href="https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;padding:0.45rem 1rem;border-radius:999px;background:#059669;color:#ffffff;font-weight:700;text-decoration:none;">Buy Seeed XIAO BLE Sense</a>
    </div>
- OpenAI Whisper: https://github.com/openai/whisper
- WhisperX: https://github.com/m-bain/whisperX
- Ollama: https://github.com/ollama/ollama

## 🛣️ Feuille de route

- Renforcer et documenter le flux audio de bout en bout dans des environnements WAN/TLS.
- Continuer à améliorer le compromis qualité/latence des transcriptions (préréglages modèle/appareil/seuils).
- Étendre la gestion d'appareils et les workflows multi-appareils par compte dans le dashboard.
- Aligner ou consolider les pistes backend historiques/parallèles (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) avec le chemin principal `backend/glass`.
- Maintenir et actualiser les variantes multilingues du README sous `i18n/`.

## 🤝 Contribution

Les contributions sont bienvenues. Pour les instructions de workflow propres au dépôt, suivez `AGENTS.md`.

Validation locale recommandée avant d'ouvrir une PR :

```bash
python -m compileall backend/glass/app.py
```

Lorsque vous soumettez des changements :

- Conservez des sujets de commit courts et orientés action (temps présent).
- Mentionnez les variables d'environnement pertinentes (par exemple `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) dans les notes de PR quand le comportement en dépend.
- Incluez des preuves de test (logs backend, comportement dashboard, sortie firmware).
- Ne commettez jamais de secrets (`DATABASE_URL`, jetons API, fichiers d'identifiants).

## 📄 Licence

Aucun fichier `LICENSE` de niveau racine n'a été détecté dans cet instantané du dépôt. Tant qu'un fichier de licence explicite n'est pas ajouté, considérez que l'usage et la redistribution nécessitent l'approbation du mainteneur.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
