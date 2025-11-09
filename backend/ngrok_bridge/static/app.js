const wsStatus = document.getElementById("wsStatus");
const backendStatus = document.getElementById("backendStatus");
const list = document.getElementById("messageList");
const logPanelEl = document.getElementById("logPanel");
const installBtn = document.getElementById("installBtn");
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
};

let loadMoreObserver = null;

state.waveformLevels = Array(state.waveformLimit).fill(0);

const AUDIO_LOG_SUPPRESS = true;
function logWave(event, details = {}) {
  if (AUDIO_LOG_SUPPRESS) return;
  // eslint-disable-next-line no-console
  console.log(`[IdeasGlass][wave] ${event}`, details);
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
  for (let i = 0; i < state.waveformLimit; i += 1) {
    const bar = document.createElement("div");
    bar.className = "wave-bar";
    bar.style.setProperty("--level", "0");
    waveformBars.appendChild(bar);
    state.waveBars.push(bar);
  }
}

function computeLevel(chunk) {
  const rms = Math.max(0, chunk?.rms ?? 0);
  const boosted = Math.sqrt(rms * 1600);
  const speechBoost = chunk?.speech_detected ? 0.15 : 0;
  return Math.min(1, Math.max(0.02, boosted + speechBoost));
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
  const li = document.createElement("li");
  li.className = "entry";

  const heading = document.createElement("div");
  heading.className = "heading";
  heading.innerHTML = `<span>${entry.device_id}</span><span>${new Date(
    entry.received_at
  ).toLocaleString()}</span>`;

  const message = document.createElement("p");
  message.className = "message";
  message.textContent = entry.message;

  li.appendChild(heading);
  li.appendChild(message);
  if (entry.photo_url) {
    const photo = document.createElement("img");
    photo.src = entry.photo_url;
    photo.alt = "IdeasGlass photo";
    photo.loading = "lazy";
    photo.className = "entry-photo";
    li.appendChild(photo);
  }
  return li;
}

function renderEntry(entry, position = "top") {
  if (!entry || !list) return;
  const li = buildEntryElement(entry);
  if (position === "top") {
    list.prepend(li);
  } else {
    list.appendChild(li);
  }
}

function trimToRecentWindow() {
  if (state.hasManualMessageLoad || !list) return;
  while (list.children.length > state.messagePageSize) {
    list.removeChild(list.lastElementChild);
  }
  state.renderedMessages = Math.min(
    state.messagePageSize,
    state.messageBuffer.length
  );
}

function renderNextMessageBatch() {
  if (!list) return 0;
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
    fragment.appendChild(buildEntryElement(state.messageBuffer[i]));
  }
  list.appendChild(fragment);
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
  if (state.waveformLevels.length >= state.waveformLimit) {
    state.waveformLevels.shift();
  }
  state.waveformLevels.push(computeLevel(chunk));
  updateWaveformBars();
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
    timerEl.textContent = `Recording ${formatSeconds(clamped)}s / ${formatSeconds(targetMs)}s`;
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
  if (!list) return;
  list.innerHTML = "";
  const ordered = Array.isArray(entries) ? entries.slice() : [];
  state.messageBuffer = ordered;
  state.renderedMessages = 0;
  state.hasManualMessageLoad = false;
  state.reachedEnd = false;
  state.loadingOlder = false;
  if (ordered.length) {
    renderNextMessageBatch();
    state.messageOldestTs = ordered[ordered.length - 1].received_at;
  } else {
    state.messageOldestTs = null;
  }
  updateLoadMoreButton();
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
  }));
  state.transcriptRendered = 0;
  renderNextTranscriptBatch();
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
  }
}

function buildTranscriptItem(item) {
  const li = document.createElement("li");
  li.className = "transcript-item";
  const text = document.createElement("p");
  text.className = "transcript-text-inline";
  text.textContent = item.text || "";
  const meta = document.createElement("div");
  meta.className = "transcript-meta-inline";
  const dt = new Date(item.ended_at || item.started_at || Date.now());
  meta.textContent = `${item.device_id || "device"} · ${dt.toLocaleTimeString()}`;
  li.append(text, meta);
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
