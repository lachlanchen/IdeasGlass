const wsStatus = document.getElementById("wsStatus");
const backendStatus = document.getElementById("backendStatus");
const list = document.getElementById("messageList");
const installBtn = document.getElementById("installBtn");
const waveformBars = document.getElementById("waveformBars");
const waveformEl = document.getElementById("waveform");
const vadStatusEl = document.getElementById("vadStatus");
const audioStatusEl = document.getElementById("audioStatus");
const timerEl = document.getElementById("timer");
const segmentList = document.getElementById("segmentList");
const transcriptPanel = document.getElementById("transcriptPanel");

let deferredPrompt = null;
let socket;
const state = {
  messageOldestTs: null,
  loadingOlder: false,
  reachedEnd: false,
  audioHistory: [],
  waveformLimit: 72,
  waveformLevels: [],
  waveBars: [],
  audioSegments: [],
  segmentTargetMs: 15000,
  transcriptSegments: [],
  activeTranscriptSegmentId: null,
  transcriptFinal: false,
};

state.waveformLevels = Array(state.waveformLimit).fill(0);

function logWave(event, details = {}) {
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

function renderEntry(entry, position = "top") {
  if (!entry) return;
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

  if (position === "top") {
    list.prepend(li);
  } else {
    list.appendChild(li);
  }
}

function decorateStatus(connected) {
  wsStatus.textContent = connected ? "Connected" : "Disconnected";
  wsStatus.className = `status ${
    connected ? "status-online" : "status-offline"
  }`;
}

async function loadOlderMessages() {
  if (state.loadingOlder || state.reachedEnd || !state.messageOldestTs) return;
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
      data.forEach((entry) => renderEntry(entry, "bottom"));
      state.messageOldestTs =
        data[data.length - 1]?.received_at || state.messageOldestTs;
    }
  } catch (err) {
    console.error("Failed to load older messages", err);
  } finally {
    state.loadingOlder = false;
  }
}

function handleScroll() {
  if (
    window.innerHeight + window.scrollY >=
    document.body.offsetHeight - 200
  ) {
    loadOlderMessages();
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

function handleHistoryMessages(entries) {
  list.innerHTML = "";
  const ordered = entries.slice().reverse();
  ordered.forEach((entry) => renderEntry(entry, "bottom"));
  if (ordered.length) {
    state.messageOldestTs = ordered[0].received_at;
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
}

function handleAudioTranscript(entry) {
  applyTranscript(entry);
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
        renderEntry(data.payload, "top");
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
window.addEventListener("scroll", handleScroll);
