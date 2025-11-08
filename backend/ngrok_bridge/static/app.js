const wsStatus = document.getElementById("wsStatus");
const backendStatus = document.getElementById("backendStatus");
const list = document.getElementById("messageList");
const installBtn = document.getElementById("installBtn");

let deferredPrompt = null;

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
  } catch (err) {
    backendStatus.textContent = "Offline";
    backendStatus.className = "status status-offline";
  }
}

function renderEntry(entry) {
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
  list.prepend(li);
}

function decorateStatus(connected) {
  wsStatus.textContent = connected ? "Connected" : "Disconnected";
  wsStatus.className = `status ${
    connected ? "status-online" : "status-offline"
  }`;
}

let socket;
function connectWs() {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${scheme}://${window.location.host}/ws/stream`);
  socket.addEventListener("open", () => decorateStatus(true));
  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "history" && Array.isArray(data.data)) {
      list.innerHTML = "";
      data.data.forEach(renderEntry);
      return;
    }
    renderEntry(data);
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
