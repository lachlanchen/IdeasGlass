const wsStatus = document.getElementById("wsStatus");
const backendStatus = document.getElementById("backendStatus");
const list = document.getElementById("messageList");
const installBtn = document.getElementById("installBtn");
const waveformBars = document.getElementById("waveformBars");
const vadStatusEl = document.getElementById("vadStatus");
const audioStatusEl = document.getElementById("audioStatus");
const timerEl = document.getElementById("timer");

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
};

state.waveformLevels = Array(state.waveformLimit).fill(0);

function logWave(...args) {
  console.debug("[IdeasGlass][wave]", ...args);
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js");
}

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
  updateTimer(chunk.created_at);
  if (audioStatusEl) {
    audioStatusEl.textContent = `Last chunk ${new Date(
      chunk.created_at
    ).toLocaleTimeString()}`;
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
}

function updateTimer(timestamp) {
  if (!timerEl || !timestamp) return;
  const date = new Date(timestamp);
  timerEl.textContent = date.toLocaleTimeString();
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
}

function handleAudioSegment(entry) {
  if (!entry) return;
  state.audioSegments.unshift(entry);
  if (state.audioSegments.length > 50) {
    state.audioSegments.pop();
  }
  logWave("audio_segment", {
    id: entry.id,
    duration_ms: entry.duration_ms,
    rms: entry.rms,
    file_url: entry.file_url,
  });
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
      case "audio_chunk":
        addAudioSample(data.payload);
        break;
      case "audio_segment":
        handleAudioSegment(data.payload);
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
