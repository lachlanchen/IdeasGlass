const wsStatus = document.getElementById("wsStatus");
const backendStatus = document.getElementById("backendStatus");
const list = document.getElementById("messageList");
const logPanelEl = document.getElementById("logPanel");
const installBtn = document.getElementById("installBtn");
const batteryStatusEl = document.getElementById("batteryStatus");
const waveformBars = document.getElementById("waveformBars");
const waveformEl = document.getElementById("waveform");
const vadStatusEl = document.getElementById("vadStatus");
const audioStatusEl = document.getElementById("audioStatus");
const timerEl = document.getElementById("timer");
const segmentList = document.getElementById("segmentList");
const segmentTranscriptPanel = document.getElementById("segmentTranscriptPanel");
const segmentTranscriptBody = document.getElementById("segmentTranscriptBody");
const loadMoreBtn = document.getElementById("loadMoreBtn");
const transcriptList = document.getElementById("transcriptList");
const transcriptMoreBtn = document.getElementById("transcriptMoreBtn");
const segmentTranscriptClose = document.getElementById("segmentTranscriptClose");
const galleryGrid = document.getElementById("galleryGrid");
const galleryGridCompact = document.getElementById("galleryGridCompact");
const photoModal = document.getElementById("photoModal");
const photoModalClose = document.getElementById("photoModalClose");
const modalImage = document.getElementById("modalImage");
const modalMetaPrimary = document.getElementById("modalMetaPrimary");
const modalMetaSecondary = document.getElementById("modalMetaSecondary");
// Tabs
const bottomNav = document.getElementById("bottomNav");
const tabButtons = bottomNav ? Array.from(bottomNav.querySelectorAll('.tab-btn')) : [];
const liveView = document.getElementById('liveView');
const liveMainView = document.getElementById('liveMainView');
const livePhotosView = document.getElementById('livePhotosView');
const livePhotosBack = document.getElementById('livePhotosBack');
const ideasView = document.getElementById('ideasView');
const creationView = document.getElementById('creationView');
const goalView = document.getElementById('goalView');
const settingsView = document.getElementById('settingsView');
// Auth + binding
const authEmail = document.getElementById("authEmail");
const authPassword = document.getElementById("authPassword");
const authRegisterBtn = document.getElementById("authRegisterBtn");
const authLoginBtn = document.getElementById("authLoginBtn");
const authLogoutBtn = document.getElementById("authLogoutBtn");
const deviceIdInput = document.getElementById("deviceIdInput");
const bindBtn = document.getElementById("bindBtn");
const authStatus = document.getElementById("authStatus");
// Overlay auth elements
const overlayEmail = document.getElementById('overlayEmail');
const overlayPassword = document.getElementById('overlayPassword');
const overlayLoginBtn = document.getElementById('overlayLoginBtn');
const overlayRegisterBtn = document.getElementById('overlayRegisterBtn');
const overlayToSettingsBtn = document.getElementById('overlayToSettingsBtn');
const overlayAuthStatus = document.getElementById('overlayAuthStatus');
const loginOverlay = document.getElementById('loginOverlay');
const liveGalleryOverlay = document.getElementById('liveGalleryOverlay');
const liveGalleryBack = document.getElementById('liveGalleryBack');
const liveTranscriptsView = document.getElementById('liveTranscriptsView');
const liveTranscriptsBack = document.getElementById('liveTranscriptsBack');
// Transcript detail page refs
const liveTranscriptDetailView = document.getElementById('liveTranscriptDetailView');
const liveTranscriptDetailBack = document.getElementById('liveTranscriptDetailBack');
const transcriptDetailAudio = document.getElementById('transcriptDetailAudio');
const transcriptDetailBody = document.getElementById('transcriptDetailBody');
const transcriptCompactList = document.getElementById('transcriptCompactList');
const transcriptsMoreCompactBtn = document.getElementById('transcriptsMoreCompactBtn');
const ideasBackBtn = document.getElementById('ideasBackBtn');
const currentEmail = document.getElementById("currentEmail");
const currentDevices = document.getElementById("currentDevices");
const accountAvatar = document.getElementById("accountAvatar");
// Preferences
const recordLenInput = document.getElementById('recordLenInput');
const recordLenSaveBtn = document.getElementById('recordLenSaveBtn');
const recordLenStatus = document.getElementById('recordLenStatus');

segmentTranscriptClose?.addEventListener("click", () => {
  hideSegmentTranscript();
});
const transcriptPanel = document.getElementById("transcriptPanel");

let deferredPrompt = null;
let socket;
const state = {
  messageOldestTs: null,
  loadingOlder: false,
  reachedEnd: false,
  messageBuffer: [],
  renderedMessages: 0,
  messagePageSize: 5,
  hasManualMessageLoad: false,
  userHasScrolled: false,
  audioHistory: [],
  waveformLimit: 72,
  waveformLevels: [],
  waveBars: [],
  audioSegments: [],
  segmentTargetMs: 15000,
  transcriptSegments: [],
  activeTranscriptSegmentId: null,
  transcriptFinal: false,
  transcriptFeed: [],
  transcriptRendered: 0,
  transcriptPageSize: 5,
  transcriptOldestEndedAt: null,
  lastAudioAt: 0,
  micActive: false,
  vuMode: true, // show uniform VU bars reflecting current volume only
  vuBaseLevel: 0.08,
  vuSpeech: false,
  vuEmaLevel: 0.08,
  waveJitterSeeds: [],
  authed: false,
  lastCompactIds: [],
  transcriptLanguage: null,
};

// Track any programmatic Audio() players to pause on nav
const playingAudios = new Set();

let loadMoreObserver = null;

state.waveformLevels = Array(state.waveformLimit).fill(0);

const AUDIO_LOG_SUPPRESS = true;
function logWave(event, details = {}) {
  if (AUDIO_LOG_SUPPRESS) return;
  // eslint-disable-next-line no-console
  console.log(`[IdeasGlass][wave] ${event}`, details);
}

function updateBatteryStatus(pct, volt) {
  if (!batteryStatusEl) return;
  let text = '--%';
  let title = 'Battery';
  if (typeof pct === 'number' && Number.isFinite(pct)) {
    text = `${Math.max(0, Math.min(100, Math.round(pct)))}%`;
  }
  if (typeof volt === 'number' && Number.isFinite(volt)) {
    title = `${volt.toFixed(2)} V`;
  }
  batteryStatusEl.textContent = `🔋 ${text}`;
  batteryStatusEl.title = title;
}

function tryUpdateBatteryFromMeta(meta) {
  if (!meta) return;
  let pct = null;
  let volt = null;
  try {
    if (typeof meta === 'string') {
      // not structured
      return;
    }
    if (typeof meta === 'object') {
      // Percent can be number or numeric string
      if (typeof meta.battery_pct === 'number') pct = meta.battery_pct;
      else if (typeof meta.battery_pct === 'string') {
        const n = parseInt(meta.battery_pct, 10);
        if (Number.isFinite(n)) pct = n;
      }
      if (typeof meta.battery_percent === 'number') pct = meta.battery_percent;
      else if (typeof meta.battery_percent === 'string') {
        const n = parseInt(meta.battery_percent, 10);
        if (Number.isFinite(n)) pct = n;
      }

      // Voltage can be number or numeric string
      if (typeof meta.battery_v === 'number') volt = meta.battery_v;
      else if (typeof meta.battery_v === 'string') {
        const v = parseFloat(meta.battery_v);
        if (Number.isFinite(v)) volt = v;
      }
      if (typeof meta.battery_voltage === 'number') volt = meta.battery_voltage;
      else if (typeof meta.battery_voltage === 'string') {
        const v = parseFloat(meta.battery_voltage);
        if (Number.isFinite(v)) volt = v;
      }
    }
  } catch {}
  if (pct !== null || volt !== null) updateBatteryStatus(pct, volt);
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js");
}

renderSegments();
clearTranscriptDisplay();

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  installBtn.hidden = false;
});

installBtn?.addEventListener("click", async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  deferredPrompt = null;
  installBtn.hidden = true;
});

loadMoreBtn?.addEventListener("click", () => {
  state.userHasScrolled = true;
  triggerMessageLoad(false);
});

transcriptMoreBtn?.addEventListener("click", () => {
  state.userHasScrolled = true;
  triggerTranscriptLoad(false);
});

// (Mic waveform removed; waveform is driven by backend audio chunks only.)

async function checkBackend() {
  try {
    const res = await fetch("/healthz");
    backendStatus.textContent = res.ok ? "Online" : "Offline";
    backendStatus.className = `status ${
      res.ok ? "status-online" : "status-offline"
    }`;
    if (res.ok) {
      try {
        const data = await res.json();
        if (typeof data?.segment_target_ms === "number") {
          state.segmentTargetMs = data.segment_target_ms;
        }
      } catch (err) {
        console.warn("Failed to parse /healthz payload", err);
      }
    }
  } catch {
    backendStatus.textContent = "Offline";
    backendStatus.className = "status status-offline";
  }
}

function initWaveformBars() {
  if (!waveformBars) return;
  waveformBars.innerHTML = "";
  state.waveBars = [];
  state.waveJitterSeeds = [];
  for (let i = 0; i < state.waveformLimit; i += 1) {
    const bar = document.createElement("div");
    bar.className = "wave-bar";
    bar.style.setProperty("--level", "0");
    waveformBars.appendChild(bar);
    state.waveBars.push(bar);
    // Fixed per-bar seed in [0.9, 1.1] for subtle variance across bars
    const seed = 0.9 + Math.random() * 0.2;
    state.waveJitterSeeds.push(seed);
  }
}

function computeLevel(chunk) {
  const rms = Math.max(0, Number(chunk?.rms || 0));
  // Continuous mapping with speech-aware bands, keeping smooth mid values.
  const floor = 0.012; // room noise
  const ceiling = 0.06; // loud speech
  const span = Math.max(1e-6, ceiling - floor);
  const norm = Math.min(1, Math.max(0, (rms - floor) / span));
  if (chunk?.speech_detected) {
    // Speech: 35%..90%
    return 0.35 + 0.55 * norm;
  }
  // Silence: 03%..12%
  return 0.03 + 0.09 * norm;
}

function updateWaveformBars() {
  if (!state.waveBars.length) {
    initWaveformBars();
  }
  state.waveBars.forEach((bar, idx) => {
    const level = state.waveformLevels[idx] ?? 0;
    bar.style.setProperty("--level", level.toFixed(3));
    if (level > 0.4) {
      bar.classList.add("active");
    } else {
      bar.classList.remove("active");
    }
  });
}

function buildEntryElement(entry) {
  if (!entry || !entry.photo_url) return null;
  const card = document.createElement("div");
  card.className = "gallery-card";
  const img = document.createElement("img");
  img.src = entry.photo_url;
  img.alt = entry.message || "IdeasGlass photo";
  img.loading = "lazy";
  card.appendChild(img);
  const badge = document.createElement("div");
  badge.className = "gallery-badge";
  badge.textContent = new Date(entry.received_at).toLocaleTimeString();
  card.appendChild(badge);
  card.addEventListener("click", () => openPhotoModal(entry));
  return card;
}

function buildMoreCard() {
  const more = document.createElement('div');
  more.className = 'gallery-card gallery-more';
  more.textContent = 'More »';
  more.addEventListener('click', () => openLivePhotosPage());
  return more;
}

function renderCompactGallery() {
  if (!galleryGridCompact) return;
  galleryGridCompact.innerHTML = '';
  // Estimate columns to keep exactly 2 rows visible and place More tile bottom-right
  const cardWidth = 150; // approx min tile width incl gap
  const cols = Math.max(1, Math.floor(galleryGridCompact.clientWidth / cardWidth));
  const limit = Math.max(1, cols * 2 - 1);
  const fragment = document.createDocumentFragment();
  let added = 0;
  for (let i = 0; i < state.messageBuffer.length && added < limit; i += 1) {
    const el = buildEntryElement(state.messageBuffer[i]);
    if (el) {
      fragment.appendChild(el);
      added += 1;
    }
  }
  fragment.appendChild(buildMoreCard());
  galleryGridCompact.appendChild(fragment);
}

function renderEntry(entry, position = "top") {
  if (!entry) return;
  const el = buildEntryElement(entry);
  if (!el) return;
  if (galleryGrid) {
    if (position === "top") galleryGrid.prepend(el);
    else galleryGrid.appendChild(el);
  }
}

function trimToRecentWindow() {
  if (state.hasManualMessageLoad || !galleryGrid) return;
  while (galleryGrid.children.length > state.messagePageSize) {
    galleryGrid.removeChild(galleryGrid.lastElementChild);
  }
  state.renderedMessages = Math.min(
    state.messagePageSize,
    state.messageBuffer.length
  );
}

function renderNextMessageBatch() {
  if (!galleryGrid) return 0;
  if (state.renderedMessages >= state.messageBuffer.length) {
    return 0;
  }
  const start = state.renderedMessages;
  const end = Math.min(
    state.messageBuffer.length,
    start + state.messagePageSize
  );
  const fragment = document.createDocumentFragment();
  for (let i = start; i < end; i += 1) {
    const el = buildEntryElement(state.messageBuffer[i]);
    if (el) fragment.appendChild(el);
  }
  galleryGrid.appendChild(fragment);
  state.renderedMessages = end;
  return end - start;
}

function updateLoadMoreButton() {
  if (!loadMoreBtn) return;
  const hasMessages = state.messageBuffer.length > 0;
  const hasBuffered = state.renderedMessages < state.messageBuffer.length;
  if (!hasMessages) {
    loadMoreBtn.hidden = true;
    return;
  }
  if (hasBuffered) {
    loadMoreBtn.hidden = false;
    loadMoreBtn.disabled = false;
    loadMoreBtn.classList.remove("loading");
    loadMoreBtn.textContent = "Show older photos";
    return;
  }
  if (state.reachedEnd) {
    loadMoreBtn.hidden = true;
    return;
  }
  loadMoreBtn.hidden = false;
  loadMoreBtn.disabled = state.loadingOlder;
  if (state.loadingOlder) {
    loadMoreBtn.classList.add("loading");
    loadMoreBtn.textContent = "Loading…";
  } else {
    loadMoreBtn.classList.remove("loading");
    loadMoreBtn.textContent = "Show older photos";
  }
}

function triggerMessageLoad(autoTriggered = false) {
  if (!state.messageBuffer.length) return;
  if (autoTriggered && !state.userHasScrolled) return;
  state.hasManualMessageLoad = true;
  const added = renderNextMessageBatch();
  updateLoadMoreButton();
  if (added === 0 && !state.reachedEnd && !state.loadingOlder) {
    loadOlderMessages();
  }
}

function handleRealtimeMessage(entry) {
  if (!entry) return;
  state.messageBuffer.unshift(entry);
  renderEntry(entry, "top");
  // Update battery UI if present in meta
  tryUpdateBatteryFromMeta(entry.meta);
  // Keep the compact gallery in sync with the latest items (microrefresh)
  try { renderCompactGallery && renderCompactGallery(); } catch {}
  if (state.hasManualMessageLoad) {
    state.renderedMessages = Math.min(
      state.renderedMessages + 1,
      state.messageBuffer.length
    );
  } else {
    trimToRecentWindow();
  }
  state.messageOldestTs =
    state.messageBuffer[state.messageBuffer.length - 1]?.received_at ||
    entry.received_at;
  updateLoadMoreButton();
}

function maybeLoadMoreViaFallback() {
  if (!loadMoreBtn || state.loadingOlder) return;
  if (logPanelEl) {
    const nearBottom =
      logPanelEl.scrollTop + logPanelEl.clientHeight >=
      logPanelEl.scrollHeight - 150;
    if (nearBottom) triggerMessageLoad(true);
    return;
  }
  const rect = loadMoreBtn.getBoundingClientRect();
  if (rect.top <= window.innerHeight + 100) {
    triggerMessageLoad(true);
  }
}

function handleGlobalScroll() {
  if (!state.userHasScrolled && window.scrollY > 20) {
    state.userHasScrolled = true;
  }
  if (!("IntersectionObserver" in window)) {
    maybeLoadMoreViaFallback();
  }
}

function initLoadMoreObserver() {
  if (!loadMoreBtn || typeof IntersectionObserver === "undefined") {
    return;
  }
  loadMoreObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && state.userHasScrolled) {
          triggerMessageLoad(true);
        }
      });
    },
    { root: logPanelEl || null, rootMargin: "150px" }
  );
  loadMoreObserver.observe(loadMoreBtn);
}

function setActiveTab(tab) {
  const views = { live: liveView, ideas: ideasView, goal: goalView, creation: creationView, settings: settingsView };
  Object.entries(views).forEach(([k, el]) => {
    if (!el) return;
    el.classList.toggle('hidden', k !== tab);
  });
  tabButtons.forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  try {
    localStorage.setItem('ig.selectedTab', tab);
  } catch {}
  updateLoginOverlay();
}

function decorateStatus(connected) {
  wsStatus.textContent = connected ? "Connected" : "Disconnected";
  wsStatus.className = `status ${
    connected ? "status-online" : "status-offline"
  }`;
}

async function loadOlderMessages() {
  if (state.loadingOlder || state.reachedEnd) return;
  if (!state.messageOldestTs) {
    state.reachedEnd = true;
    updateLoadMoreButton();
    return;
  }
  state.loadingOlder = true;
  try {
    const res = await fetch(
      `/api/v1/messages?limit=20&before=${encodeURIComponent(
        state.messageOldestTs
      )}`
    );
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      state.reachedEnd = true;
    } else {
      state.messageBuffer = state.messageBuffer.concat(data);
      state.messageOldestTs =
        data[data.length - 1]?.received_at || state.messageOldestTs;
      if (state.hasManualMessageLoad) {
        renderNextMessageBatch();
      }
    }
  } catch (err) {
    console.error("Failed to load older messages", err);
  } finally {
    state.loadingOlder = false;
    updateLoadMoreButton();
  }
}

function addAudioSample(chunk) {
  if (!chunk) return;
  state.lastAudioAt = Date.now();
  logWave("audio_chunk", {
    id: chunk.id,
    rms: chunk.rms,
    speech: chunk.speech_detected,
    segment_duration_ms: chunk.segment_duration_ms,
    created_at: chunk.created_at,
  });
  state.audioHistory.push(chunk);
  if (state.audioHistory.length > 200) {
    state.audioHistory.shift();
  }
  const level = computeLevel(chunk);
  if (state.vuMode) {
    // Update base VU level and speech flag; per-bar variance animator will render
    state.vuBaseLevel = level;
    state.vuSpeech = Boolean(chunk?.speech_detected);
    // Smooth with an EMA so we get intermediate values, not binary jumps
    const prev = Number.isFinite(state.vuEmaLevel) ? state.vuEmaLevel : level;
    state.vuEmaLevel = Math.min(1, Math.max(0, prev * 0.8 + level * 0.2));
    state.waveformLevels = state.waveformLevels.length
      ? state.waveformLevels
      : Array(state.waveformLimit).fill(level);
    updateWaveformBars();
  } else {
    if (state.waveformLevels.length >= state.waveformLimit) {
      state.waveformLevels.shift();
    }
    state.waveformLevels.push(level);
    updateWaveformBars();
  }
  updateVadStatus(chunk);
  updateRecordingTimer(chunk);
  if (audioStatusEl) {
    const rmsText =
      typeof chunk.rms === "number"
        ? chunk.rms.toFixed(3)
        : Number(chunk.rms || 0).toFixed(3);
    const segmentText =
      typeof chunk.segment_duration_ms === "number"
        ? `Segment ${formatSeconds(chunk.segment_duration_ms)}s`
        : "Segment …";
    audioStatusEl.textContent = `Last chunk ${new Date(
      chunk.created_at
    ).toLocaleTimeString()} · RMS ${rmsText} · ${segmentText}`;
  }
}

function updateVadStatus(chunk) {
  if (!vadStatusEl) return;
  const rms = chunk?.rms ?? 0;
  const isSpeaking = chunk?.speech_detected ?? rms > 0.02;
  if (isSpeaking) {
    vadStatusEl.textContent = "🎙️ SPEAKING";
    vadStatusEl.classList.remove("silence");
    vadStatusEl.classList.add("speaking");
  } else {
    vadStatusEl.textContent = "🔇 SILENCE";
    vadStatusEl.classList.remove("speaking");
    vadStatusEl.classList.add("silence");
  }
  if (waveformEl) {
    waveformEl.classList.toggle("speaking", isSpeaking);
  }
}

function formatSeconds(ms) {
  if (!Number.isFinite(ms)) return "0.0";
  if (ms < 1000) {
    return (ms / 1000).toFixed(1);
  }
  if (ms < 60000) {
    return (ms / 1000).toFixed(1);
  }
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.round((ms % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function updateRecordingTimer(chunk) {
  if (!timerEl) return;
  const targetMs = state.segmentTargetMs || 15000;
  const progressMs =
    typeof chunk?.segment_duration_ms === "number"
      ? Math.max(0, chunk.segment_duration_ms)
      : null;
  if (progressMs !== null && targetMs > 0) {
    const clamped = Math.min(targetMs, progressMs);
    const normalized = Math.min(1, clamped / targetMs);
    // Render label and values separately so we can wrap on small screens
    const current = `${formatSeconds(clamped)}s`;
    const total = `${formatSeconds(targetMs)}s`;
    timerEl.innerHTML = `<span class="timer-label">Recording</span><span class="timer-values">${current} / ${total}</span>`;
    timerEl.style.setProperty("--progress", normalized.toFixed(3));
    timerEl.classList.toggle("complete", normalized >= 0.999);
    return;
  }
  if (chunk?.created_at) {
    timerEl.textContent = new Date(chunk.created_at).toLocaleTimeString();
  } else {
    timerEl.textContent = "LIVE";
  }
  timerEl.classList.remove("complete");
  timerEl.style.setProperty("--progress", "0");
}

function formatDuration(ms) {
  const totalSeconds = Math.max(1, Math.round(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  if (minutes === 0) {
    return `${seconds}s`;
  }
  return `${minutes}m ${seconds.toString().padStart(2, "0")}s`;
}

function renderSegments() {
  if (!segmentList) return;
  segmentList.innerHTML = "";
  if (!state.audioSegments.length) {
    const empty = document.createElement("li");
    empty.className = "segment-empty";
    empty.textContent = "Recordings will appear here once available…";
    segmentList.appendChild(empty);
    return;
  }
  state.audioSegments.slice(0, 6).forEach((segment) => {
    const li = document.createElement("li");
    li.className = "segment-item";
    const meta = document.createElement("div");
    meta.className = "segment-meta";
    const duration = document.createElement("span");
    duration.className = "segment-duration";
    duration.textContent = formatDuration(segment.duration_ms);
    const ts = document.createElement("span");
    ts.textContent = new Date(segment.started_at).toLocaleTimeString();
    meta.append(duration, ts);
    li.appendChild(meta);
    if (segment.file_url) {
      // Play/Pause button
      const playBtn = document.createElement('button');
      playBtn.type = 'button';
      playBtn.className = 'segment-play-btn';
      playBtn.textContent = 'Play';
      let audioEl = null;
      playBtn.addEventListener('click', () => {
        try {
          if (!audioEl) {
            audioEl = new Audio(segment.file_url);
            audioEl.addEventListener('ended', () => { playBtn.textContent = 'Play'; });
          }
          if (audioEl.paused) {
            audioEl.play();
            playBtn.textContent = 'Pause';
          } else {
            audioEl.pause();
            playBtn.textContent = 'Play';
          }
        } catch {}
      });
      li.appendChild(playBtn);

      const link = document.createElement("a");
      link.href = segment.file_url;
      link.target = "_blank";
      link.rel = "noopener";
      link.className = "segment-link";
      link.textContent = "Download";
      li.appendChild(link);
    }
    const transcriptBtn = document.createElement("button");
    transcriptBtn.type = "button";
    transcriptBtn.className = "segment-transcript-btn";
    transcriptBtn.textContent = "Transcript";
    transcriptBtn.addEventListener("click", () => handleSegmentTranscript(segment.id));
    li.appendChild(transcriptBtn);
    segmentList.appendChild(li);
  });
}

function clearTranscriptDisplay(message = "Listening for transcript…") {
  state.transcriptSegments = [];
  state.activeTranscriptSegmentId = null;
  state.transcriptFinal = false;
  if (!transcriptPanel) return;
  transcriptPanel.innerHTML = "";
  const placeholder = document.createElement("div");
  placeholder.className = "transcript-placeholder";
  placeholder.textContent = message;
  transcriptPanel.appendChild(placeholder);
}

function renderTranscript() {
  if (!transcriptPanel) return;
  transcriptPanel.innerHTML = "";
  if (!state.transcriptSegments.length) {
    clearTranscriptDisplay();
    return;
  }
  // Language badge if available
  if (state.transcriptLanguage) {
    const lang = document.createElement('div');
    lang.className = 'transcript-lang-badge';
    lang.textContent = String(state.transcriptLanguage).toUpperCase();
    transcriptPanel.appendChild(lang);
  }
  if (!state.transcriptFinal) {
    const badge = document.createElement("div");
    badge.className = "transcript-placeholder";
    badge.textContent = "Transcribing…";
    transcriptPanel.appendChild(badge);
  }
  state.transcriptSegments.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "transcript-entry";
    const speaker = document.createElement("span");
    speaker.className = "transcript-speaker";
    speaker.textContent = entry.speaker || "Speaker";
    const text = document.createElement("div");
    text.className = "transcript-text";
    const body = document.createElement("p");
    body.textContent = entry.text || "";
    const meta = document.createElement("small");
    const start = Number(entry.start || 0).toFixed(1);
    const end = Number(entry.end || 0).toFixed(1);
    meta.textContent = `${start}s → ${end}s`;
    text.append(body, meta);
    row.append(speaker, text);
    transcriptPanel.appendChild(row);
  });
  if (state.transcriptFinal) {
    const badge = document.createElement("div");
    badge.className = "transcript-placeholder";
    badge.textContent = "Segment complete";
    transcriptPanel.appendChild(badge);
  }
}

function applyTranscript(entry) {
  if (!entry) return;
  state.activeTranscriptSegmentId = entry.segment_id;
  state.transcriptLanguage = entry.language || null;
  state.transcriptSegments = (entry.chunks || []).map((chunk) => ({
    speaker: chunk.speaker || "Speaker",
    text: chunk.text || "",
    start: chunk.start ?? 0,
    end: chunk.end ?? chunk.start ?? 0,
  }));
  state.transcriptFinal = Boolean(entry.is_final);
  renderTranscript();
}

function hideSegmentTranscript() {
  if (segmentTranscriptPanel) {
    segmentTranscriptPanel.classList.add("hidden");
  }
}

function renderSegmentTranscriptPanel(entry, segmentId) {
  if (!segmentTranscriptPanel || !segmentTranscriptBody) return;
  segmentTranscriptPanel.classList.remove("hidden");
  const title = document.getElementById("segmentTranscriptTitle");
  if (title) {
    title.textContent = `Transcript · ${segmentId}`;
  }
  if (!entry || !Array.isArray(entry.chunks) || entry.chunks.length === 0) {
    segmentTranscriptBody.textContent = "No transcript available.";
    return;
  }
  segmentTranscriptBody.innerHTML = "";
  entry.chunks.forEach((chunk) => {
    const row = document.createElement("div");
    row.className = "segment-transcript-entry";
    const text = document.createElement("p");
    text.textContent = chunk.text || "";
    const meta = document.createElement("small");
    const start = Number(chunk.start || 0).toFixed(1);
    const end = Number(chunk.end || chunk.start || 0).toFixed(1);
    meta.textContent = `${chunk.speaker || "Speaker"} · ${start}s → ${end}s`;
    row.append(text, meta);
    segmentTranscriptBody.appendChild(row);
  });
}

async function handleSegmentTranscript(segmentId) {
  if (!segmentId) return;
  if (segmentTranscriptBody) {
    segmentTranscriptBody.textContent = "Loading transcript...";
  }
  segmentTranscriptPanel?.classList.remove("hidden");
  try {
    const res = await fetch(`/api/v1/audio/segments/${segmentId}/transcript`);
    if (!res.ok) {
      throw new Error("Transcript not found");
    }
    const data = await res.json();
    renderSegmentTranscriptPanel(data, segmentId);
  } catch (err) {
    if (segmentTranscriptBody) {
      segmentTranscriptBody.textContent = `Transcript unavailable (${err.message || err})`;
    }
  }
}

function handleHistoryMessages(entries) {
  if (galleryGrid) galleryGrid.innerHTML = "";
  if (galleryGridCompact) galleryGridCompact.innerHTML = '';
  const ordered = Array.isArray(entries) ? entries.slice() : [];
  state.messageBuffer = ordered;
  state.renderedMessages = 0;
  state.hasManualMessageLoad = false;
  state.reachedEnd = false;
  state.loadingOlder = false;
  if (ordered.length) {
    renderNextMessageBatch();
    renderCompactGallery();
    state.messageOldestTs = ordered[ordered.length - 1].received_at;
  } else {
    state.messageOldestTs = null;
  }
  updateLoadMoreButton();
  // Try to seed battery status from latest entries with battery meta
  for (let i = 0; i < state.messageBuffer.length && i < 10; i += 1) {
    const m = state.messageBuffer[i];
    if (m && m.meta) {
      tryUpdateBatteryFromMeta(m.meta);
      break;
    }
  }
}

function handleHistoryAudio(entries) {
  state.audioHistory = [];
  state.waveformLevels = Array(state.waveformLimit).fill(0);
  updateWaveformBars();
  const ordered = entries.slice().reverse();
  logWave("history_audio", { count: ordered.length });
  ordered.forEach(addAudioSample);
}

function handleHistoryAudioSegments(entries) {
  state.audioSegments = entries.slice();
  logWave("history_audio_segments", { count: entries.length });
  renderSegments();
}

function handleAudioSegment(entry) {
  if (!entry) return;
  state.audioSegments.unshift(entry);
  if (state.audioSegments.length > 20) {
    state.audioSegments.pop();
  }
  logWave("audio_segment", {
    id: entry.id,
    duration_ms: entry.duration_ms,
    rms: entry.rms,
    file_url: entry.file_url,
  });
  renderSegments();
  clearTranscriptDisplay("Recording new segment…");
}

function handleHistoryAudioTranscripts(entries) {
  if (!entries || !entries.length) {
    clearTranscriptDisplay();
    return;
  }
  applyTranscript(entries[0]);
  // Populate transcript feed with latest entries
  state.transcriptFeed = (entries || []).slice().map((t) => ({
    segment_id: t.segment_id,
    device_id: t.device_id,
    started_at: t.started_at,
    ended_at: t.ended_at,
    text: (Array.isArray(t.chunks) ? t.chunks.map((c) => c.text).join(" ") : "").trim(),
    is_final: Boolean(t.is_final),
    language: t.language || null,
  }));
  state.transcriptRendered = 0;
  renderNextTranscriptBatch();
  renderCompactTranscripts();
}

function handleAudioTranscript(entry) {
  applyTranscript(entry);
  // When final, prepend to feed
  if (entry && entry.is_final) {
    state.transcriptFeed.unshift({
      segment_id: entry.segment_id,
      device_id: entry.device_id,
      started_at: entry.started_at,
      ended_at: entry.ended_at,
      text: (Array.isArray(entry.chunks) ? entry.chunks.map((c) => c.text).join(" ") : "").trim(),
      is_final: true,
      language: entry.language || null,
    });
    // If we already rendered some, add this one to the top visually
    if (transcriptList) {
      const li = buildTranscriptItem(state.transcriptFeed[0]);
      transcriptList.prepend(li);
      if (state.transcriptRendered < state.transcriptFeed.length) {
        state.transcriptRendered += 1;
      }
      updateTranscriptMoreButton();
    }
    renderCompactTranscripts();
  }
}

function buildTranscriptCompactItem(item) {
  const li = document.createElement('li');
  li.className = 'transcript-compact-item';
  const left = document.createElement('div'); left.className = 'tci-left';
  const text = document.createElement('div'); text.className = 'tci-text'; text.textContent = item.text || '';
  left.append(text);
  left.addEventListener('click', () => openLiveTranscriptDetailPage(item.segment_id));
  const actions = document.createElement('div'); actions.className = 'tci-actions';
  if (item.language) {
    const langEl = document.createElement('div');
    langEl.className = 'tci-lang';
    langEl.textContent = String(item.language).toUpperCase();
    actions.appendChild(langEl);
  }
  const playBtn = document.createElement('button'); playBtn.type = 'button'; playBtn.className = 'tci-play'; playBtn.textContent = 'Play';
  let audioEl = null;
  playBtn.addEventListener('click', () => {
    try {
      const url = `/api/v1/audio/segments/${item.segment_id}`;
      if (!audioEl) {
        audioEl = new Audio(url);
        try { playingAudios.add(audioEl); } catch {}
        audioEl.addEventListener('ended', () => { playBtn.textContent = 'Play'; });
      }
      if (audioEl.paused) { audioEl.play(); playBtn.textContent = 'Pause'; } else { audioEl.pause(); playBtn.textContent = 'Play'; }
    } catch {}
  });
  const time = document.createElement('div');
  time.className = 'tci-time';
  time.textContent = new Date(item.ended_at || item.started_at || Date.now()).toLocaleTimeString();
  // Order: time then play, so Play sits at the right edge
  actions.appendChild(time);
  actions.appendChild(playBtn);
  li.append(left, actions);
  return li;
}

function renderCompactTranscripts() {
  if (!transcriptCompactList) return;
  const items = state.transcriptFeed.slice(0, 5);
  const ids = items.map((it) => it.segment_id);
  // If unchanged, do nothing (microrefresh behavior)
  if (ids.length === state.lastCompactIds.length && ids.every((v, i) => v === state.lastCompactIds[i])) {
    return;
  }
  // Rebuild compact list
  transcriptCompactList.innerHTML = '';
  const frag = document.createDocumentFragment();
  items.forEach((it) => frag.appendChild(buildTranscriptCompactItem(it)));
  transcriptCompactList.appendChild(frag);
  state.lastCompactIds = ids;
  // Subtle flash on the newest item
  const first = transcriptCompactList.firstElementChild;
  if (first) {
    first.classList.add('flash');
    setTimeout(() => first.classList.remove('flash'), 280);
  }
}

function openLiveTranscriptsPage() {
  if (!liveMainView || !liveTranscriptsView) return;
  liveTranscriptsView.classList.remove('hidden');
  liveTranscriptsView.classList.add('slide-in');
  liveMainView.classList.add('hidden');
  setTimeout(() => liveTranscriptsView.classList.remove('slide-in'), 300);
}
function closeLiveTranscriptsPage() {
  if (!liveMainView || !liveTranscriptsView) return;
  pauseAllAudio();
  liveMainView.classList.remove('hidden');
  liveMainView.classList.add('slide-in');
  setTimeout(() => liveMainView.classList.remove('slide-in'), 300);
  liveTranscriptsView.classList.add('hidden');
}
// Use direct lookup to avoid TDZ issues in some caches
document.getElementById('liveTranscriptsBack')?.addEventListener('click', closeLiveTranscriptsPage);
transcriptsMoreCompactBtn?.addEventListener('click', openLiveTranscriptsPage);

function buildTranscriptItem(item) {
  const li = document.createElement('li');
  li.className = 'transcript-item';
  // Left side: text
  const left = document.createElement('div');
  left.className = 'transcript-item-left';
  const text = document.createElement('p');
  text.className = 'transcript-text-inline';
  text.textContent = item.text || '';
  left.appendChild(text);
  left.addEventListener('click', () => openLiveTranscriptDetailPage(item.segment_id));
  // Right side: time + Play
  const right = document.createElement('div');
  right.className = 'transcript-item-right tci-actions';
  if (item.language) {
    const langEl = document.createElement('div');
    langEl.className = 'tci-lang';
    langEl.textContent = String(item.language).toUpperCase();
    right.appendChild(langEl);
  }
  const time = document.createElement('div');
  time.className = 'tci-time';
  time.textContent = new Date(item.ended_at || item.started_at || Date.now()).toLocaleTimeString();
  const playBtn = document.createElement('button');
  playBtn.type = 'button';
  playBtn.className = 'tci-play';
  playBtn.textContent = 'Play';
  let audioEl = null;
  playBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    try {
      const url = `/api/v1/audio/segments/${item.segment_id}`;
      if (!audioEl) {
        audioEl = new Audio(url);
        try { playingAudios.add(audioEl); } catch {}
        audioEl.addEventListener('ended', () => { playBtn.textContent = 'Play'; });
      }
      if (audioEl.paused) { audioEl.play(); playBtn.textContent = 'Pause'; } else { audioEl.pause(); playBtn.textContent = 'Play'; }
    } catch {}
  });
  right.append(time, playBtn);
  li.append(left, right);
  return li;
}

function renderNextTranscriptBatch() {
  if (!transcriptList) return 0;
  const start = state.transcriptRendered;
  const end = Math.min(state.transcriptFeed.length, start + state.transcriptPageSize);
  if (start >= end) return 0;
  const frag = document.createDocumentFragment();
  for (let i = start; i < end; i += 1) {
    frag.appendChild(buildTranscriptItem(state.transcriptFeed[i]));
  }
  transcriptList.appendChild(frag);
  state.transcriptRendered = end;
  // Track oldest ended_at for paging
  if (state.transcriptFeed.length) {
    const last = state.transcriptFeed[state.transcriptFeed.length - 1];
    state.transcriptOldestEndedAt = last.ended_at || last.started_at || null;
  }
  updateTranscriptMoreButton();
  return end - start;
}

function updateTranscriptMoreButton() {
  if (!transcriptMoreBtn) return;
  const hasBuffered = state.transcriptRendered < state.transcriptFeed.length;
  transcriptMoreBtn.hidden = !hasBuffered && !state.transcriptOldestEndedAt;
  transcriptMoreBtn.disabled = false;
  transcriptMoreBtn.textContent = hasBuffered ? "Show older transcripts" : "Load more";
}

async function triggerTranscriptLoad(auto = false) {
  // If we still have buffered items, render them
  const added = renderNextTranscriptBatch();
  if (added > 0) return;
  // Else fetch older segments and pull transcripts
  if (!state.transcriptOldestEndedAt) return;
  try {
    const res = await fetch(`/api/v1/audio/segments?limit=10&before=${encodeURIComponent(state.transcriptOldestEndedAt)}`);
    if (!res.ok) return;
    const segments = await res.json();
    if (!Array.isArray(segments) || segments.length === 0) {
      transcriptMoreBtn && (transcriptMoreBtn.hidden = true);
      return;
    }
    // Fetch transcripts for each segment;
    const older = [];
    for (const seg of segments) {
      try {
        const tRes = await fetch(`/api/v1/audio/segments/${seg.id}/transcript`);
        if (!tRes.ok) continue;
        const t = await tRes.json();
        older.push({
          segment_id: t.segment_id,
          device_id: t.device_id,
          started_at: t.started_at,
          ended_at: t.ended_at,
          text: (Array.isArray(t.chunks) ? t.chunks.map((c) => c.text).join(" ") : "").trim(),
          is_final: Boolean(t.is_final),
          language: t.language || null,
        });
      } catch {}
    }
    // Append older to feed end and render next batch
    if (older.length) {
      state.transcriptFeed = state.transcriptFeed.concat(older);
      renderNextTranscriptBatch();
    } else {
      transcriptMoreBtn && (transcriptMoreBtn.hidden = true);
    }
  } catch {}
}

function connectWs() {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${scheme}://${window.location.host}/ws/stream`);
  socket.addEventListener("open", () => decorateStatus(true));
  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case "history_messages":
        handleHistoryMessages(data.data || []);
        break;
      case "message":
        handleRealtimeMessage(data.payload);
        break;
      case "history_audio":
        handleHistoryAudio(data.data || []);
        break;
      case "history_audio_segments":
        handleHistoryAudioSegments(data.data || []);
        break;
      case "history_audio_transcripts":
        handleHistoryAudioTranscripts(data.data || []);
        break;
      case "audio_chunk":
        addAudioSample(data.payload);
        break;
      case "audio_segment":
        handleAudioSegment(data.payload);
        break;
      case "audio_transcript":
        handleAudioTranscript(data.payload);
        break;
      default:
        break;
    }
  });
  socket.addEventListener("close", () => {
    decorateStatus(false);
    setTimeout(connectWs, 2000);
  });
  socket.addEventListener("error", () => socket.close());
}

initWaveformBars();
checkBackend();
setInterval(checkBackend, 10000);
connectWs();
initLoadMoreObserver();
if (logPanelEl) {
  logPanelEl.addEventListener("scroll", handleGlobalScroll);
} else {
  window.addEventListener("scroll", handleGlobalScroll);
}

// Tabs wiring: default to live
if (tabButtons.length) {
  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => setActiveTab(btn.dataset.tab || 'live'));
  });
  // Restore previously selected tab (default to live)
  let saved = null;
  try { saved = localStorage.getItem('ig.selectedTab'); } catch {}
  const valid = new Set(['live','ideas','goal','creation','settings']);
  setActiveTab(valid.has(saved) ? saved : 'live');
  // Defer overlay update until after first auth check
  setTimeout(() => { try { updateLoginOverlay && updateLoginOverlay(); } catch {} }, 0);
  // Re-render compact gallery on resize for accurate column fit
  window.addEventListener('resize', () => {
    try { renderCompactGallery && renderCompactGallery(); } catch {}
  });
}

// Modal wiring
photoModalClose?.addEventListener('click', closePhotoModal);
photoModal?.addEventListener('click', (e) => { if (e.target === photoModal) closePhotoModal(); });

// Transcript detail page
function openLiveTranscriptDetailPage(segmentId) {
  if (!liveTranscriptDetailView) return;
  // Determine previous visible view
  try {
    const wasTranscripts = liveTranscriptsView && !liveTranscriptsView.classList.contains('hidden');
    state.prevLiveView = wasTranscripts ? 'transcripts' : 'main';
  } catch { state.prevLiveView = 'main'; }
  // Hide other Live views
  if (liveMainView) liveMainView.classList.add('hidden');
  if (liveTranscriptsView) liveTranscriptsView.classList.add('hidden');
  // ensure audio source
  if (transcriptDetailAudio) {
    transcriptDetailAudio.src = `/api/v1/audio/segments/${segmentId}`;
  }
  if (transcriptDetailBody) transcriptDetailBody.textContent = 'Loading transcript…';
  fetch(`/api/v1/audio/segments/${segmentId}/transcript`).then(async (res) => {
    if (!res.ok) throw new Error('Transcript not found');
    const data = await res.json();
    renderTranscriptDetail(data);
  }).catch(() => { if (transcriptDetailBody) transcriptDetailBody.textContent = 'Transcript unavailable'; });
  liveTranscriptDetailView.classList.remove('hidden');
  liveTranscriptDetailView.classList.add('slide-in');
  setTimeout(() => liveTranscriptDetailView.classList.remove('slide-in'), 300);
}

function closeLiveTranscriptDetailPage() {
  if (!liveTranscriptDetailView) return;
  pauseAllAudio();
  liveTranscriptDetailView.classList.add('hidden');
  // Restore previous view
  const prev = state.prevLiveView || 'main';
  if (prev === 'transcripts' && liveTranscriptsView) {
    liveTranscriptsView.classList.remove('hidden');
    liveTranscriptsView.classList.add('slide-in');
    setTimeout(() => liveTranscriptsView.classList.remove('slide-in'), 300);
  } else if (liveMainView) {
    liveMainView.classList.remove('hidden');
    liveMainView.classList.add('slide-in');
    setTimeout(() => liveMainView.classList.remove('slide-in'), 300);
  }
}
document.getElementById('liveTranscriptDetailBack')?.addEventListener('click', closeLiveTranscriptDetailPage);

// Login overlay wiring
function updateLoginOverlay() {
  if (!loginOverlay) return;
  const tab = (tabButtons.find(b => b.classList.contains('active'))?.dataset.tab) || 'live';
  const show = (tab === 'live') && !state.authed;
  loginOverlay.classList.toggle('hidden', !show);
  try { loginOverlay.setAttribute('aria-hidden', (!show).toString()); } catch {}
}

overlayToSettingsBtn?.addEventListener('click', () => setActiveTab('settings'));
overlayLoginBtn?.addEventListener('click', async () => {
  const email = (overlayEmail?.value || '').trim();
  const pwd = overlayPassword?.value || '';
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || !pwd) {
    setOverlayStatus('Enter valid email and password');
    return;
  }
  try {
    await apiPost('/api/v1/auth/login', { email, password: pwd });
    setOverlayStatus('Logged in ✔');
    try { localStorage.setItem('ig.lastEmail', email); } catch {}
    connectWs();
    refreshAccount();
  } catch {
    setOverlayStatus('Login failed');
  }
});

overlayRegisterBtn?.addEventListener('click', async () => {
  const email = (overlayEmail?.value || '').trim();
  const pwd = overlayPassword?.value || '';
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || pwd.length < 8) {
    setOverlayStatus('Enter valid email and 8+ char password');
    return;
  }
  try {
    await apiPost('/api/v1/auth/register', { email, password: pwd });
    setOverlayStatus('Registered ✔');
    try { localStorage.setItem('ig.lastEmail', email); } catch {}
    connectWs();
    refreshAccount();
  } catch {
    setOverlayStatus('Register failed');
  }
});

// Live photos page (push-style) handlers
function openLivePhotosPage() {
  if (!liveMainView || !livePhotosView) return;
  livePhotosView.classList.remove('hidden');
  livePhotosView.classList.add('slide-in');
  liveMainView.classList.add('hidden');
  setTimeout(() => livePhotosView.classList.remove('slide-in'), 300);
}
function closeLivePhotosPage() {
  if (!liveMainView || !livePhotosView) return;
  pauseAllAudio();
  liveMainView.classList.remove('hidden');
  liveMainView.classList.add('slide-in');
  setTimeout(() => liveMainView.classList.remove('slide-in'), 300);
  livePhotosView.classList.add('hidden');
}
document.getElementById('livePhotosBack')?.addEventListener('click', closeLivePhotosPage);
ideasBackBtn?.addEventListener('click', () => setActiveTab('live'));

// Swipe-to-go-back on Live Photos page (iOS-like)
(function enableLivePhotosSwipeBack() {
  if (!livePhotosView) return;
  let startX = 0, startY = 0, swiping = false;
  const THRESHOLD_X = 60; // px to trigger
  const MAX_Y = 40; // max vertical dev
  livePhotosView.addEventListener('touchstart', (e) => {
    if (!e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    startX = t.clientX; startY = t.clientY; swiping = true;
  }, { passive: true });
  livePhotosView.addEventListener('touchmove', (e) => {
    if (!swiping || !e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    const dx = t.clientX - startX; const dy = Math.abs(t.clientY - startY);
    // If vertical scroll dominates, cancel swipe detect
    if (dy > MAX_Y) swiping = false;
    // Don't prevent default; allow scroll
  }, { passive: true });
  livePhotosView.addEventListener('touchend', (e) => {
    if (!swiping) return;
    const changed = e.changedTouches && e.changedTouches[0];
    if (changed) {
      const dx = changed.clientX - startX; const dy = Math.abs(changed.clientY - startY);
      if (dx > THRESHOLD_X && dy <= MAX_Y) {
        closeLivePhotosPage();
      }
    }
    swiping = false;
  });
})();

// Swipe-to-go-back on Live Transcripts list page
(function enableLiveTranscriptsSwipeBack() {
  if (!liveTranscriptsView) return;
  let startX = 0, startY = 0, swiping = false;
  const THRESHOLD_X = 60;
  const MAX_Y = 40;
  liveTranscriptsView.addEventListener('touchstart', (e) => {
    if (!e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    startX = t.clientX; startY = t.clientY; swiping = true;
  }, { passive: true });
  liveTranscriptsView.addEventListener('touchmove', (e) => {
    if (!swiping || !e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    const dy = Math.abs(t.clientY - startY);
    if (dy > MAX_Y) swiping = false;
  }, { passive: true });
  liveTranscriptsView.addEventListener('touchend', (e) => {
    if (!swiping) return;
    const changed = e.changedTouches && e.changedTouches[0];
    if (changed) {
      const dx = changed.clientX - startX; const dy = Math.abs(changed.clientY - startY);
      if (dx > THRESHOLD_X && dy <= MAX_Y) closeLiveTranscriptsPage();
    }
    swiping = false;
  });
})();

// Swipe-to-go-back on Transcript detail page
(function enableLiveTranscriptDetailSwipeBack() {
  if (!liveTranscriptDetailView) return;
  let startX = 0, startY = 0, swiping = false;
  const THRESHOLD_X = 60;
  const MAX_Y = 40;
  liveTranscriptDetailView.addEventListener('touchstart', (e) => {
    if (!e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    startX = t.clientX; startY = t.clientY; swiping = true;
  }, { passive: true });
  liveTranscriptDetailView.addEventListener('touchmove', (e) => {
    if (!swiping || !e.touches || e.touches.length !== 1) return;
    const t = e.touches[0];
    const dy = Math.abs(t.clientY - startY);
    if (dy > MAX_Y) swiping = false;
  }, { passive: true });
  liveTranscriptDetailView.addEventListener('touchend', (e) => {
    if (!swiping) return;
    const changed = e.changedTouches && e.changedTouches[0];
    if (changed) {
      const dx = changed.clientX - startX; const dy = Math.abs(changed.clientY - startY);
      if (dx > THRESHOLD_X && dy <= MAX_Y) closeLiveTranscriptDetailPage();
    }
    swiping = false;
  });
})();

// VU variance animator: keep base level but add subtle bar-to-bar/time variance
function renderVuVariance() {
  if (!state.vuMode || !state.waveBars.length) return;
  const t = performance.now() * 0.001; // seconds
  const base = Math.min(1, Math.max(0.01, state.vuEmaLevel || state.vuBaseLevel || 0.08));
  const speak = state.vuSpeech;
  const amp = speak ? 0.08 : 0.03; // lower amplitude to avoid pegging
  const speed = speak ? 2.0 : 1.2; // oscillation speed
  const phaseStep = 0.35;
  const levels = new Array(state.waveformLimit);
  for (let i = 0; i < state.waveformLimit; i += 1) {
    const seed = state.waveJitterSeeds[i] || 1.0;
    const wobble = 1 + amp * Math.sin(t * speed + i * phaseStep);
    const raw = base * seed * wobble;
    // Clamp to avoid binary look and keep speech below full height
    const minL = speak ? 0.30 : 0.03;
    const maxL = speak ? 0.92 : 0.14;
    const clamped = Math.min(maxL, Math.max(minL, raw));
    levels[i] = clamped;
  }
  state.waveformLevels = levels;
  updateWaveformBars();
}

// Run animator at ~60–80 FPS budget friendly
setInterval(renderVuVariance, 80);
function openPhotoModal(entry) {
  if (!photoModal || !modalImage) return;
  modalImage.src = entry.photo_url;
  modalImage.alt = entry.message || "Photo";
  if (modalMetaPrimary) modalMetaPrimary.textContent = entry.message || "(no message)";
  if (modalMetaSecondary) modalMetaSecondary.textContent = `${entry.device_id} · ${new Date(entry.received_at).toLocaleString()}`;
  photoModal.classList.remove('hidden');
}
function closePhotoModal() { photoModal && photoModal.classList.add('hidden'); }
function pauseAllAudio() {
  try {
    // Pause DOM audio elements
    document.querySelectorAll('audio').forEach((a) => { try { a.pause(); } catch {} });
  } catch {}
  try {
    // Pause any programmatically created Audio()
    playingAudios.forEach((a) => { try { a.pause(); } catch {} });
  } catch {}
}
async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
    credentials: "include",
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${txt}`);
  }
  try { return await res.json(); } catch { return {}; }
}

async function apiGet(url) {
  const res = await fetch(url, { credentials: "include" });
  if (!res.ok) throw new Error(`${res.status}`);
  return await res.json();
}

// Render transcript detail view body (with language)
function renderTranscriptDetail(data) {
  if (!transcriptDetailBody) return;
  const frag = document.createDocumentFragment();
  // Language badge
  if (data && data.language) {
    const lang = document.createElement('div');
    lang.className = 'transcript-lang-badge';
    lang.textContent = String(data.language).toUpperCase();
    frag.appendChild(lang);
  }
  // Chunks
  const chunks = Array.isArray(data?.chunks) ? data.chunks : [];
  if (!chunks.length) {
    const p = document.createElement('p');
    p.textContent = '(no transcript)';
    frag.appendChild(p);
  } else {
    chunks.forEach((c) => {
      const row = document.createElement('div');
      row.className = 'segment-transcript-entry';
      const p = document.createElement('p');
      p.textContent = c.text || '';
      const small = document.createElement('small');
      const start = Number(c.start || 0).toFixed(1);
      const end = Number(c.end || 0).toFixed(1);
      small.textContent = `${start}s → ${end}s`;
      row.append(p, small);
      frag.appendChild(row);
    });
  }
  transcriptDetailBody.innerHTML = '';
  transcriptDetailBody.appendChild(frag);
}

function setAuthStatus(msg) {
  if (!authStatus) return;
  authStatus.textContent = msg || "";
}

function setOverlayStatus(msg) {
  if (!overlayAuthStatus) return;
  overlayAuthStatus.textContent = msg || '';
}

function setRecordLenStatus(msg) {
  if (!recordLenStatus) return;
  recordLenStatus.textContent = msg || '';
}

async function refreshAccount() {
  let me = null;
  try {
    me = await apiGet("/api/v1/auth/me");
  } catch {}
  const authed = Boolean(me && me.email);
  state.authed = authed;
  if (currentEmail) currentEmail.textContent = authed ? (me.email || '') : '';
  if (accountAvatar) {
    if (authed && me.email) {
      const letter = (me.email[0] || 'U').toUpperCase();
      accountAvatar.textContent = letter;
      accountAvatar.classList.remove('hidden');
    } else {
      accountAvatar.classList.add('hidden');
    }
  }
  if (currentDevices) {
    currentDevices.innerHTML = "";
    if (authed && Array.isArray(me.devices)) {
      const section = document.createElement('div');
      section.className = 'device-section';
      const title = document.createElement('div');
      title.className = 'device-title';
      title.textContent = 'Devices';
      const ul = document.createElement('ul');
      ul.className = 'device-list';
      if (me.devices.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'account-label';
        empty.textContent = 'No devices bound';
        section.append(title, empty);
      } else {
        me.devices.forEach((d) => {
          const li = document.createElement('li');
          li.className = 'device-item';
          li.textContent = d;
          ul.appendChild(li);
        });
        section.append(title, ul);
      }
      currentDevices.appendChild(section);
    }
  }
  if (authForm) authForm.classList.toggle('hidden', authed);
  const bindForm = bindBtn ? bindBtn.closest('form') : null;
  if (bindForm) bindForm.classList.toggle('hidden', !authed);
  if (authLogoutBtn) authLogoutBtn.classList.toggle('hidden', !authed);
  if (authed && deviceIdInput && Array.isArray(me.devices) && me.devices.length && !deviceIdInput.value) {
    deviceIdInput.value = me.devices[0];
  }
  // Prefill email fields with last used
  try {
    const last = localStorage.getItem('ig.lastEmail');
    if (!authed && last) {
      if (authEmail && !authEmail.value) authEmail.value = last;
      if (overlayEmail && !overlayEmail.value) overlayEmail.value = last;
    }
  } catch {}
  updateLoginOverlay();
  // Load preferences after auth state is known
  try { await refreshSettings(); } catch {}
}

authRegisterBtn?.addEventListener("click", async () => {
  try {
    const email = (authEmail?.value || "").trim();
    const pwd = authPassword?.value || "";
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || pwd.length < 8) {
      setAuthStatus("Enter valid email and 8+ char password");
      return;
    }
    await apiPost("/api/v1/auth/register", { email, password: pwd });
    setAuthStatus("Registered ✔");
    connectWs();
    refreshAccount();
  } catch (e) {
    setAuthStatus(`Register failed`);
  }
});

authLoginBtn?.addEventListener("click", async () => {
  try {
    const email = (authEmail?.value || "").trim();
    const pwd = authPassword?.value || "";
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || !pwd) {
      setAuthStatus("Enter valid email and password");
      return;
    }
    await apiPost("/api/v1/auth/login", { email, password: pwd });
    setAuthStatus("Logged in ✔");
    connectWs();
    refreshAccount();
    // Try to list devices
    try {
      const data = await apiGet("/api/v1/devices");
      if (data && Array.isArray(data.devices) && data.devices.length && !deviceIdInput.value) {
        deviceIdInput.value = data.devices[0];
        setAuthStatus(`Bound devices: ${data.devices.join(", ")}`);
      }
    } catch {}
  } catch (e) {
    setAuthStatus(`Login failed`);
  }
});

authLogoutBtn?.addEventListener("click", async () => {
  try {
    await apiPost("/api/v1/auth/logout", {});
    setAuthStatus("Logged out");
    refreshAccount();
  } catch {}
});

bindBtn?.addEventListener("click", async () => {
  const devId = (deviceIdInput?.value || "").trim();
  if (!devId) return;
  try {
    await apiPost("/api/v1/devices/bind", { device_id: devId });
    setAuthStatus(`Bound ${devId} ✔`);
    // Reconnect WS to ensure server-side filter includes this device
    try { socket && socket.close(); } catch {}
    connectWs();
    refreshAccount();
  } catch (e) {
    setAuthStatus("Bind failed");
  }
});

// Show current account on load
refreshAccount();
// Live transcripts page elements

async function refreshSettings() {
  try {
    const data = await apiGet('/api/v1/settings');
    if (data && typeof data.segment_target_ms === 'number') {
      const secs = Math.round(data.segment_target_ms / 1000);
      if (recordLenInput) recordLenInput.value = String(secs);
      state.segmentTargetMs = data.segment_target_ms;
    }
  } catch {}
}

recordLenSaveBtn?.addEventListener('click', async () => {
  const secs = parseInt((recordLenInput?.value || '').trim(), 10);
  if (!Number.isFinite(secs) || secs < 5 || secs > 60) {
    setRecordLenStatus('Enter 5–60 seconds');
    return;
  }
  try {
    const payload = { segment_target_ms: secs * 1000 };
    const out = await apiPost('/api/v1/settings', payload);
    if (out && typeof out.segment_target_ms === 'number') {
      state.segmentTargetMs = out.segment_target_ms;
      setRecordLenStatus('Saved ✔');
    } else {
      setRecordLenStatus('Saved');
    }
  } catch (e) {
    setRecordLenStatus('Save failed');
  }
});
