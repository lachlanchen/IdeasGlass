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
  waveformLimit: 60,
};

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
  state.audioHistory.push(chunk);
  if (state.audioHistory.length > state.waveformLimit) {
    state.audioHistory.shift();
  }
  renderWaveform();
  updateVadStatus(chunk.rms);
  updateTimer(chunk.created_at);
  if (audioStatusEl) {
    audioStatusEl.textContent = `Last chunk ${new Date(
      chunk.created_at
    ).toLocaleTimeString()}`;
  }
}

function renderWaveform() {
  if (!waveformBars) return;
  waveformBars.innerHTML = "";
  if (state.audioHistory.length === 0) {
    const placeholder = document.createElement("div");
    placeholder.className = "wave-placeholder";
    placeholder.textContent = "Waiting for audio…";
    waveformBars.appendChild(placeholder);
    return;
  }
  state.audioHistory.forEach((chunk) => {
    const bar = document.createElement("div");
    bar.className = "wave-bar";
    const height = Math.max(6, Math.min(100, chunk.rms * 4000));
    bar.style.height = `${height}%`;
    waveformBars.appendChild(bar);
  });
}

function updateVadStatus(rms) {
  if (!vadStatusEl) return;
  const threshold = 0.02;
  if (rms > threshold) {
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
  const ordered = entries.slice().reverse();
  ordered.forEach(addAudioSample);
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
      case "audio_chunk":
        addAudioSample(data.payload);
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

checkBackend();
setInterval(checkBackend, 10000);
connectWs();
window.addEventListener("scroll", handleScroll);
