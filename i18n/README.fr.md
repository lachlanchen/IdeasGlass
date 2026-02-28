[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)



[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# IdeasGlass

*Un wearable IA qui transforme les idées en actions, revenus et dynamique créative.*

> Pipeline wearable centré sur la voix : capture depuis des lunettes ESP32, traitement dans FastAPI, et supervision/contrôle via un tableau de bord PWA en temps réel.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white&style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-XIAO__ESP32S3-111111?logo=espressif&logoColor=white&style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Dashboard-5A0FC8?logo=pwa&logoColor=white&style=flat-square)
![Streaming](https://img.shields.io/badge/Streaming-WebSocket%20%2B%20Whisper-0EA5E9?style=flat-square)
![Locale](https://img.shields.io/badge/Localized-i18n-0F766E?style=flat-square)

| Voie | Objectif |
|---|---|
| 🎙️ Capture wearable | Les lunettes ESP32 envoient audio, photos et télémétrie quasi en temps réel |
| 🧠 Intelligence backend | FastAPI ingère les flux, transcrit, segmente et persiste les métadonnées |
| 🖥️ Tableau de bord | Le PWA affiche l'onde live, les transcriptions et le statut appareil/compte |

<div align="center">
  <img src="figs/ideas.lazying.art_main.png" alt="IdeasGlass App UI" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <img src="figs/ideasglass_hardware.png" alt="IdeasGlass hardware" width="49%" style="max-width:49%;display:inline-block;vertical-align:middle;"/>
  <br/>
  <sub>UI de l'application (gauche) · Matériel (droite)</sub>
</div>

Explorez les expériences communautaires sur <a href="https://onlyideas.art">onlyideas.art</a>.

## 🚀 Aperçu

IdeasGlass est un système wearable IA pensé pour la capture et l'exécution d'idées par la voix. Dans ce dépôt, le chemin d'exécution principal est :

- `backend/glass/` pour les API FastAPI, l'ingestion WebSocket, la transcription basée sur Whisper et le tableau de bord PWA installable.
- `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` pour le firmware XIAO ESP32S3 qui stream audio, photos et télémétrie.

Si vous découvrez ce dépôt, commencez par là.

## 📚 Table des matières

- [🚀 Aperçu](#-aperçu)
- [✨ Pourquoi IdeasGlass](#-pourquoi-ideasglass)
- [🧩 Fonctionnalités](#-fonctionnalités)
- [🔄 Workflow d'exemple](#-workflow-dexemple)
- [🗂️ Structure du projet](#️-structure-du-projet)
- [🧰 Prérequis](#-prérequis)
- [⚙️ Installation](#️-installation)
- [▶️ Utilisation](#️-utilisation)
- [🛠️ Configuration](#️-configuration)
- [🧪 Exemples](#-exemples)
- [🧭 Notes de développement](#-notes-de-développement)
- [🆘 Dépannage](#️-dépannage)
- [🌐 Liens d'écosystème](#-liens-décosystème)
- [🙏 Remerciements](#-remerciements)
- [🛣️ Feuille de route](#️-feuille-de-route)
- [🤝 Contribution](#-contribution)
- [❤️ Support](#-support)
- [📄 Licence](#-licence)

### En bref

| Domaine | Emplacement principal | Ce que ça fait |
|---|---|---|
| API backend + PWA | `backend/glass/` | Endpoints FastAPI, ingestion/fanout WebSocket, transcription, tableau de bord |
| Firmware | `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/` | Client de capture/streaming ESP32 |
| Notes de bridge | `references/ideasglass_bridge.md` | Notes de fiabilité TLS/WAN et conseils de déploiement terrain |
| Traductions README | `i18n/` | Documentation multilingue synchronisée depuis le README canonique |

## ✨ Pourquoi IdeasGlass

IdeasGlass est un wearable IA conçu pour les personnes qui vivent au rythme d'un flux d'idées. Il capture, traduit, organise et exécute la créativité au moment où l'inspiration surgit, que vous racontiez un concept en mouvement ou animiez une session en direct.

## 🧩 Fonctionnalités

### Fonctionnalités de la vision produit

- **Matériel natif de création** – lunettes légères et entrées wearables, optimisés pour la capture vocale avec raccourcis gestuels discrets.
- **Traduction instantanée** – détection/traduction de langue en temps réel pour co-créer entre équipes ou publics sans changer d'outils.
- **Co-pilote EchoMind** – association étroite avec `chat.lazying.art` pour le brainstorming, la rédaction de scripts et le coaching de contenu multilingue.
- **Pilotage automatique des canaux** – rédige des plans, scripts long format, hooks courts et planifie les publications sur YouTube ou d'autres flux.
- **Temps forts et reels** – sélectionne automatiquement des moments, génère miniatures, sous-titres et extraits prêts pour les réseaux.
- **Couche revenus** – connecte LazyingArt Coin pour les pourboires, la conversion de crédits et la conversion en actifs on-chain.
- **Suivi des dépenses et de la concentration** – suit les coûts opérationnels, met en avant les formats rentables et synthétise vos forces dans les prochains projets.

### Fonctionnalités dépôt/runtime

- Backend FastAPI avec endpoints REST + WebSocket pour l'ingestion (`/api/v1/audio`, `/ws/audio-ingest`) et la diffusion en temps réel (`/ws/stream`).
- Segmentation audio déterministe (par défaut ~15 s avec recouvrement) vers `backend/glass/audio_segments/`.
- Transcriptions en streaming openai-whisper optionnelles avec seuils de latence configurables.
- Persistance Postgres optionnelle (`DATABASE_URL`) pour messages, photos, chunks, segments, transcriptions.
- Tableau de bord PWA avec waveform live, mises à jour de transcription et support d'installation desktop/mobile.
- Support firmware Arduino pour les flux caméra + micro XIAO ESP32S3 Sense.

## 🔄 Workflow d'exemple

1. **Capture** – Parlez ou esquissez un concept; IdeasGlass transcrit, traduit et étiquette l'intention.
2. **Co-création** – EchoMind affine l'idée, rédige des scripts et suggère des CTA adaptés à chaque plateforme.
3. **Publication** – L'agent de chaîne auto-produise des moments forts, des images de galerie, puis les publie avec métadonnées.
4. **Monétisation** – Les crédits passent via LazyingArt Coin (`coin.lazying.art`) et les paiements sont synchronisés avec vos wallets préférés.
5. **Réflexion** – Les tableaux de bord des dépenses, portée et engagement indiquent sur quoi miser ensuite.

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
│   ├── tornado_app/                       # Chemin backend d'ingestion secondaire/parallèle
│   ├── memo/
│   ├── memo_legacy/
│   └── ngrok_bridge/
├── IdeaGlass/firmware/ideasglass_arduino/
│   ├── IdeasGlassClient/
│   ├── config.h
│   ├── WifiTest/WifiTest.ino
│   ├── wifi_credentials.example.h
│   └── README.md
├── references/ideasglass_bridge.md        # Notes de bridge + déploiement
├── docs/                                  # Assets docs/site supplémentaires
├── development_plan/
├── app/
├── ops/observability/
├── ios-app-example/
├── figs/
├── seeed_studio_xiao_esp32s3_dev/
└── .auto-readme-work/
```

## 🧰 Prérequis

- Python 3.10+
- `pip` (ou environnement conda avec Python compatible)
- Optionnel : GPU NVIDIA + CUDA/cuDNN pour une inférence Whisper plus rapide
- Optionnel : PostgreSQL pour la persistance
- Pour le firmware : Arduino IDE ou `arduino-cli`, Seeed XIAO ESP32S3 Sense, PSRAM activée

| Composant | Exigence | Notes |
|---|---|---|
| Runtime backend | Python 3.10+, `pip` | Utilisez venv ou conda (`glass`) |
| Accélération GPU (optionnel) | NVIDIA + CUDA/cuDNN | Réduit la latence de Whisper |
| Persistance (optionnel) | PostgreSQL | Activée via `DATABASE_URL` |
| Chaîne d'outillage firmware | Arduino IDE / `arduino-cli` | Utilisez le profil XIAO ESP32S3 avec PSRAM |

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
- Schéma de partition : `Default with spiffs (3MB APP/1.5MB SPIFFS)` ou `Maximum APP` quand le système de fichiers n'est pas requis.

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
| `/healthz` | Contrôle de santé backend |
| `/ws/audio-ingest` | WebSocket d'ingestion appareil |
| `/ws/stream` | Fanout de flux en direct vers les clients dashboard |

### Se connecter et lier votre appareil

1. Inscrivez-vous ou connectez-vous depuis Paramètres/Compte du tableau de bord.
2. Liez votre ID d'appareil dans le champ `Bind device`.
3. Seuls les appareils liés diffusent vers votre compte.

Générez un ID appareil + image QR :

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

Migration optionnelle (renommer des données historiques vers un nouvel ID appareil) :

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
Si la permission est refusée : `sudo usermod -aG dialout $USER` puis reconnectez-vous (ou temporairement `sudo chmod a+rw /dev/ttyACM0`).

### UX d'alimentation firmware (XIAO ESP32S3)

- Maintenez le bouton ~0,8 s au démarrage pour démarrer.
- Maintenez ~2,5 s en fonctionnement pour entrer en veille profonde.
- Une pression courte en fonctionnement déclenche toujours la capture.

## 🛠️ Configuration

### Variables d'environnement principales

- `DATABASE_URL` : DSN Postgres optionnel pour le stockage persistant.
- `IDEASGLASS_WHISPER_MODEL` : `base` (défaut), `small`, `medium`, `large-v3`, `large-v3-turbo`.
- `IDEASGLASS_WHISPER_DEVICE` : `cuda` ou `cpu`.
- `IDEASGLASS_WHISPER_FP16` : `1` pour précision mixte GPU, `0` pour CPU.
- `IDEASGLASS_TRANSCRIBE` : `1` (défaut) pour activer la transcription, `0` pour la désactiver.
- `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` : intervalle rolling des transcriptions.
- `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` : seuils séparés par virgules (défaut `3000,6000,15000`).

| Variable | Défaut/options | Effet |
|---|---|---|
| `DATABASE_URL` | non défini par défaut | Active la persistance Postgres pour données compte/appareil |
| `IDEASGLASS_WHISPER_MODEL` | `base` (`small`, `medium`, `large-v3`, `large-v3-turbo`) | Contrôle précision vs latence |
| `IDEASGLASS_WHISPER_DEVICE` | `cuda` ou `cpu` | Backend d'inférence |
| `IDEASGLASS_WHISPER_FP16` | `1` GPU, `0` CPU-safe | Contrôle de précision mixte |
| `IDEASGLASS_TRANSCRIBE` | `1` | Active ou désactive la pipeline de transcription |
| `IDEASGLASS_TRANSCRIPT_INTERVAL_MS` | configuré à l'exécution | Intervalle de push rolling de transcription |
| `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS` | `3000,6000,15000` | Seuils de sortie progressive des transcriptions |

Exemples de `DATABASE_URL` sûrs :

- `export DATABASE_URL="postgresql://<db_user>@localhost/ideasglass_db"` (authentification pair/local)
- `export DATABASE_URL="postgresql://<db_user>:<db_password>@localhost/ideasglass_db"` (authentification par mot de passe)

### Paramètres de gain et segmentation audio

- `IDEASGLASS_GAIN_TARGET` (défaut `0.032`)
- `IDEASGLASS_GAIN_MAX` (défaut `1.8`)
- `IDEASGLASS_GAIN_MIN_RMS` (défaut `0.008`)
- `IDEASGLASS_SPEECH_RMS` (défaut `0.03`)
- `IDEASGLASS_SPEECH_MARGIN` (défaut `0.005`)
- `IDEASGLASS_SEGMENT_TARGET_MS` (défaut `15000`)
- `IDEASGLASS_SEGMENT_OVERLAP_MS` (défaut `2000`)
- `IDEASGLASS_SEGMENT_GAIN_TARGET` (par défaut: cible de gain du chunk)

| Réglage audio | Défaut | Rôle |
|---|---|---|
| `IDEASGLASS_GAIN_TARGET` | `0.032` | Normalisation RMS cible |
| `IDEASGLASS_GAIN_MAX` | `1.8` | Limite supérieure d'amplification |
| `IDEASGLASS_GAIN_MIN_RMS` | `0.008` | Plancher pour éviter d'amplifier un quasi-silence |
| `IDEASGLASS_SPEECH_RMS` | `0.03` | Seuil RMS de référence pour la parole |
| `IDEASGLASS_SPEECH_MARGIN` | `0.005` | Marge autour du seuil de parole |
| `IDEASGLASS_SEGMENT_TARGET_MS` | `15000` | Durée cible d'un segment |
| `IDEASGLASS_SEGMENT_OVERLAP_MS` | `2000` | Recouvrement de segment pour continuité |
| `IDEASGLASS_SEGMENT_GAIN_TARGET` | hérité du gain du chunk | Cible de normalisation au niveau segment |

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

Flux tableau de bord :

1. Inscrivez-vous/connectez-vous dans Paramètres.
2. Liez l'appareil dans le panneau Compte.
3. Seuls les appareils liés sont diffusés vers votre compte.

### Exemples REST ingest

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

## 🧭 Notes de développement

### Axe de focus

Ce dépôt contient plusieurs pistes backend. La priorité actuelle des contributions et du runtime est `backend/glass/` sauf indication contraire.

### Vérification static/syntaxe

```bash
python -m compileall backend/glass/app.py
```

### Documentation développeur

- [IdeasGlass Object Analysis](OmiGlass/docs/ideasglass_analysis.mdx)
- [Arduino Hardware Blueprint](OmiGlass/docs/ideasglass_arduino_hardware.md)
- [Plan Multi-platform App / PWA](OmiGlass/docs/ideasglass_pwa_plan.md)
- [Bridge & Arduino HTTPS Client](docs/ideasglass_bridge.md)

> Note : dans l'état actuel du dépôt, certains liens historiques semblent déplacés (par exemple, les notes de bridge sont désormais dans `references/ideasglass_bridge.md`). Les liens originaux sont conservés comme contenu canonique du README.

### Lier un appareil rapidement (workflow préservé)

- Générer un ID (dans conda `glass`) : `python backend/glass/tools/generate_device_id.py`
- Le définir dans firmware : `IdeaGlass/firmware/ideasglass_arduino/IdeasGlassClient/IdeasGlassClient.ino` (`kDeviceId`)
- Lancer le backend et ouvrir `http://localhost:8765`, puis inscrire/se connecter et lier l'ID appareil dans le panneau Compte

## 🆘 Dépannage

- **Port déjà utilisé :** lancez le backend sur un autre port et mettez à jour la configuration de l'appareil.
- **Port série occupé :** `fuser -k /dev/ttyACM0`.
- **Permission série Linux refusée :** `sudo usermod -aG dialout $USER` puis reconnectez-vous.
- **Postgres indisponible :** le backend peut fonctionner sans DB avec une fonctionnalité partielle ; vérifiez `DATABASE_URL` et redémarrez.
- **Problèmes de perf Whisper :** utilisez des modèles plus petits (`base`/`small`) ou désactivez la transcription via `IDEASGLASS_TRANSCRIBE=0`.
- **Instabilité TLS/synchronisation temps sur ESP32 :** vérifiez Wi-Fi, disponibilité NTP (UDP/123), et paramètres cert/host ; consultez `references/ideasglass_bridge.md` pour des notes terrain détaillées.
- **Aucune mise à jour de waveform live :** consultez les logs backend et la console navigateur pour les traces `[IdeasGlass][wave]` et confirmez la connectivité `/ws/stream`.

## 🌐 Liens d'écosystème

| Marque | Objectif | Lien |
|---|---|---|
| 🧠 EchoMind | Compagnon IA multilingue pour apprendre et créer | [chat.lazying.art](https://chat.lazying.art) |
| 🌱 OnlyIdeas | Communauté Recherche → Produit pour des concepts ambitieux | [onlyideas.art](https://onlyideas.art) |
| 💸 LazyEarn | Automatisations pour transformer de petites victoires en revenus | [earn.lazying.art](https://earn.lazying.art) |
| 📚 LazyLearn | Parcours de physique & chimie, et cahiers | [learn.lazying.art](https://learn.lazying.art) |
| 🤖 IdeasRobot | Agent qui transforme idées en brouillons, tâches et posts | [robot.lazying.art](https://robot.lazying.art) |
| 👓 IdeasGlass | Capture, traduction, et auto-production de reels | [glass.lazying.art](https://glass.lazying.art) |
| 🪙 LazyingArt Coin | Récompenses et paiements reliant contributions et valeur on-chain | [coin.lazying.art](https://coin.lazying.art) |
| 🧪 IDEAS | Cahier de notes de recherche et d'essais | [ideas.onlyideas.art](https://ideas.onlyideas.art) |
| 🎨 LazyingArt | Studio derrière OnlyIdeas, EchoMind, LazyEdit et IdeasGlass | [lazying.art](https://lazying.art) |

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

- Renforcer et documenter le flux audio de bout en bout sur des environnements WAN/TLS.
- Continuer à améliorer le compromis qualité/latence de transcription (préréglages modèle/appareil/seuil).
- Étendre la gestion d'appareils et les workflows multi-appareils par compte dans le tableau de bord.
- Aligners ou consolider les pistes backend legacy/parallèles (`tornado_app`, `memo`, `memo_legacy`, `ngrok_bridge`) avec le chemin principal `backend/glass`.
- Maintenir et actualiser les versions README multilingues sous `i18n/`.

## 🤝 Contribution

Les contributions sont les bienvenues. Pour les consignes de workflow propres au dépôt, suivez `AGENTS.md`.

Validation locale recommandée avant ouverture d'une PR :

```bash
python -m compileall backend/glass/app.py
```

Lors de la soumission :

- Gardez des sujets de commit courts et orientés action (temps présent).
- Mentionnez les variables d'environnement pertinentes (par exemple `IDEASGLASS_TRANSCRIPT_THRESHOLDS_MS`) dans les notes de PR quand un comportement en dépend.
- Incluez des preuves de test (logs backend, comportement du dashboard, sortie firmware).
- Ne commettez jamais de secrets (`DATABASE_URL`, tokens API, fichiers d'identifiants).

## 📄 Licence

Aucun fichier `LICENSE` de niveau supérieur n'a été détecté dans cet instantané du dépôt. Jusqu'à l'ajout d'un fichier de licence explicite, considérez l'usage et la redistribution comme nécessitant l'approbation du mainteneur.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
