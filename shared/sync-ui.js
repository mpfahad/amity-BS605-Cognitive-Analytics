/**
 * Sync-code panel UI for Amity multi-subject hub.
 * Same sync code for all subjects; progress is namespaced per subject.
 */
(function (global) {
  const CSS = `
.bs605-sync, .amity-sync {
  margin-top: 1rem;
  padding: 0.95rem 1rem;
  border-radius: var(--radius, 18px);
  border: 1px solid var(--line, rgba(21,35,28,0.12));
  background: rgba(255,255,255,0.72);
}
.amity-sync h3 {
  margin: 0 0 0.35rem;
  font-family: var(--font-display, Georgia, serif);
  font-size: 1.15rem;
}
.amity-sync p {
  margin: 0 0 0.7rem;
  color: var(--muted, #4a5c52);
  font-size: 0.92rem;
}
.amity-sync-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
.amity-sync input[type="text"],
.amity-sync input[type="password"] {
  flex: 1 1 180px;
  min-width: 160px;
  border: 1px solid var(--line, rgba(21,35,28,0.12));
  border-radius: 999px;
  padding: 0.55rem 0.9rem;
  font: inherit;
  background: #fff;
}
.amity-sync .status {
  margin-top: 0.55rem;
  font-size: 0.88rem;
  color: var(--muted, #4a5c52);
}
.amity-sync .status.ok { color: var(--ok, #1f7a4d); }
.amity-sync .status.warn { color: var(--warn, #8a3b12); }
.amity-sync .status.err { color: var(--bad, #a33b3b); }
.amity-sync.connected-mode .amity-enter { display: none; }
.amity-sync:not(.connected-mode) .amity-connected { display: none; }
.amity-sync .code-pill {
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
    if (document.getElementById("amity-sync-style")) return;
    const s = document.createElement("style");
    s.id = "amity-sync-style";
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
    const P = global.AmityProgress || global.BS605Progress;
    if (!root || !P) return;
    const subjectLabel = (opts && opts.subjectLabel) || (global.AMITY_SUBJECT || "this subject");

    root.innerHTML = `
      <div class="amity-sync" id="amitySyncBox">
        <h3>Sync progress</h3>
        <p>One private sync code works across <strong>all subjects</strong> on phone and PC. Progress for <strong>${subjectLabel}</strong> is saved separately so subjects never wipe each other. Existing BS605 progress is kept.</p>
        <div class="amity-enter amity-sync-row">
          <input id="amitySyncCode" type="password" autocomplete="off" placeholder="Create or enter sync code" />
          <button type="button" class="btn primary" id="amitySyncConnect">Connect</button>
        </div>
        <div class="amity-connected amity-sync-row">
          <span class="code-pill" id="amityCodePill">Connected</span>
          <button type="button" class="btn" id="amitySyncChange">Change code</button>
          <button type="button" class="btn" id="amitySyncClear">Disconnect</button>
        </div>
        <div class="amity-sync-row" style="margin-top:0.55rem">
          <button type="button" class="btn" id="amityClearProgress">Clear this subject progress</button>
        </div>
        <div class="status" id="amitySyncStatus">…</div>
      </div>
    `;

    const box = root.querySelector("#amitySyncBox");
    const input = root.querySelector("#amitySyncCode");
    const statusEl = root.querySelector("#amitySyncStatus");
    const pill = root.querySelector("#amityCodePill");

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

    function subjectPayload(full) {
      if (!full) return null;
      if (P.getSubjectPayload) return P.getSubjectPayload(full, P.currentSubject());
      return full;
    }

    async function doConnect() {
      const code = input.value.trim() || P.getCode();
      if (!code) {
        paint({ state: "error", message: "Enter a sync code first", at: null });
        return;
      }
      const payload = await P.connect(code);
      setConnectedMode(true);
      const sub = subjectPayload(payload);
      if (opts && typeof opts.onLoaded === "function") opts.onLoaded(sub, payload);
      if (opts && typeof opts.onReady === "function") opts.onReady(sub, payload);
    }

    root.querySelector("#amitySyncConnect").addEventListener("click", doConnect);
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doConnect();
    });
    root.querySelector("#amitySyncChange").addEventListener("click", () => {
      setConnectedMode(false);
      input.value = P.getCode() || "";
      input.focus();
    });
    root.querySelector("#amitySyncClear").addEventListener("click", () => {
      P.disconnect();
      input.value = "";
      setConnectedMode(false);
      if (opts && typeof opts.onCleared === "function") opts.onCleared();
    });
    root.querySelector("#amityClearProgress").addEventListener("click", async () => {
      if (!confirm("Clear progress for " + subjectLabel + " only? Other subjects stay intact.")) return;
      await P.clearProgress(P.currentSubject());
      window.location.reload();
    });

    if (P.getCode()) {
      setConnectedMode(true);
      input.value = P.getCode();
      P.loadProgress().then((payload) => {
        const sub = subjectPayload(payload);
        if (opts && typeof opts.onLoaded === "function") opts.onLoaded(sub, payload);
        if (opts && typeof opts.onReady === "function") opts.onReady(sub, payload);
      });
    } else if (opts && typeof opts.onReady === "function") {
      const local = P.readLocalCache()?.payload || null;
      opts.onReady(subjectPayload(local), local);
    }
  }

  global.AmitySyncUI = { mount };
  global.BS605SyncUI = { mount }; // alias
})(window);
