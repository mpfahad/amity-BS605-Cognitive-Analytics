/**
 * Sync-code panel UI for BS605 pages.
 * Code is remembered on the device — you stay connected until Clear.
 */
(function (global) {
  const CSS = `
.bs605-sync {
  margin-top: 1rem;
  padding: 0.95rem 1rem;
  border-radius: var(--radius, 18px);
  border: 1px solid var(--line, rgba(21,35,28,0.12));
  background: rgba(255,255,255,0.72);
}
.bs605-sync h3 {
  margin: 0 0 0.35rem;
  font-family: var(--font-display, Georgia, serif);
  font-size: 1.15rem;
}
.bs605-sync p {
  margin: 0 0 0.7rem;
  color: var(--muted, #4a5c52);
  font-size: 0.92rem;
}
.bs605-sync-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
.bs605-sync input[type="text"],
.bs605-sync input[type="password"] {
  flex: 1 1 180px;
  min-width: 160px;
  border: 1px solid var(--line, rgba(21,35,28,0.12));
  border-radius: 999px;
  padding: 0.55rem 0.9rem;
  font: inherit;
  background: #fff;
}
.bs605-sync .status {
  margin-top: 0.55rem;
  font-size: 0.88rem;
  color: var(--muted, #4a5c52);
}
.bs605-sync .status.ok { color: var(--ok, #1f7a4d); }
.bs605-sync .status.warn { color: var(--warn, #8a3b12); }
.bs605-sync .status.err { color: var(--bad, #a33b3b); }
.bs605-sync.connected-mode .bs605-enter { display: none; }
.bs605-sync:not(.connected-mode) .bs605-connected { display: none; }
.bs605-sync .code-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.85rem;
  border-radius: 999px;
  background: var(--accent-soft, #d8efe4);
  color: var(--accent, #0f6b4c);
  font-weight: 700;
  font-size: 0.9rem;
}
`;

  function ensureStyle() {
    if (document.getElementById("bs605-sync-style")) return;
    const s = document.createElement("style");
    s.id = "bs605-sync-style";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function formatAt(iso) {
    if (!iso) return "";
    try {
      return new Date(iso).toLocaleString();
    } catch {
      return iso;
    }
  }

  function mount(root, opts) {
    ensureStyle();
    const P = global.BS605Progress;
    if (!root || !P) return;

    root.innerHTML = `
      <div class="bs605-sync" id="bs605SyncBox">
        <h3>Sync progress</h3>
        <p>Enter a private sync code <strong>once</strong> on each device. It stays connected and auto-saves quiz, flashcards, and module-map answers.</p>
        <div class="bs605-enter bs605-sync-row">
          <input id="bs605SyncCode" type="password" autocomplete="off" placeholder="Create or enter sync code" />
          <button type="button" class="btn primary" id="bs605SyncConnect">Connect</button>
        </div>
        <div class="bs605-connected bs605-sync-row">
          <span class="code-pill" id="bs605CodePill">Connected</span>
          <button type="button" class="btn" id="bs605SyncChange">Change code</button>
          <button type="button" class="btn" id="bs605SyncClear">Disconnect</button>
        </div>
        <div class="status" id="bs605SyncStatus">…</div>
      </div>
    `;

    const box = root.querySelector("#bs605SyncBox");
    const input = root.querySelector("#bs605SyncCode");
    const statusEl = root.querySelector("#bs605SyncStatus");
    const pill = root.querySelector("#bs605CodePill");

    function setConnectedMode(on) {
      box.classList.toggle("connected-mode", Boolean(on));
      if (on) pill.textContent = "Code " + (P.maskedCode() || "••••");
    }

    function paint(st) {
      statusEl.className = "status";
      if (st.state === "connected") statusEl.classList.add("ok");
      else if (st.state === "offline" || st.state === "syncing") statusEl.classList.add("warn");
      else if (st.state === "error") statusEl.classList.add("err");
      const when = st.at ? " · last sync " + formatAt(st.at) : "";
      statusEl.textContent = st.message + when;
      setConnectedMode(Boolean(P.getCode()) && (st.state === "connected" || st.state === "offline" || st.state === "syncing"));
    }

    P.onStatus(paint);

    async function doConnect() {
      const code = input.value.trim() || P.getCode();
      if (!code) {
        paint({ state: "error", message: "Enter a sync code first", at: null });
        return;
      }
      const payload = await P.connect(code);
      setConnectedMode(true);
      if (opts && typeof opts.onLoaded === "function") opts.onLoaded(payload);
      if (opts && typeof opts.onReady === "function") opts.onReady();
    }

    root.querySelector("#bs605SyncConnect").addEventListener("click", doConnect);
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doConnect();
    });
    root.querySelector("#bs605SyncChange").addEventListener("click", () => {
      setConnectedMode(false);
      input.value = P.getCode() || "";
      input.focus();
    });
    root.querySelector("#bs605SyncClear").addEventListener("click", () => {
      P.disconnect();
      input.value = "";
      setConnectedMode(false);
      if (opts && typeof opts.onCleared === "function") opts.onCleared();
    });

    // Auto-connect if this device already has a code — no need to click Connect again
    if (P.getCode()) {
      setConnectedMode(true);
      input.value = P.getCode();
      P.loadProgress().then((payload) => {
        if (opts && typeof opts.onLoaded === "function") opts.onLoaded(payload);
        if (opts && typeof opts.onReady === "function") opts.onReady();
      });
    } else if (opts && typeof opts.onReady === "function") {
      opts.onReady();
    }
  }

  global.BS605SyncUI = { mount };
})(window);
