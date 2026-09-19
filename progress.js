/**
 * BS605 cross-device progress via sync code + Supabase.
 * Config: window.BS605_SYNC = { url, anonKey } from config.js
 */
(function (global) {
  const STORAGE_CODE = "bs605_sync_code";
  const STORAGE_CACHE = "bs605_progress_cache";
  const TABLE = "bs605_progress";

  function cfg() {
    return global.BS605_SYNC || {};
  }

  function configured() {
    const c = cfg();
    return Boolean(c.url && c.anonKey && !String(c.url).includes("YOUR_"));
  }

  async function sha256Hex(text) {
    const data = new TextEncoder().encode(String(text).trim());
    const digest = await crypto.subtle.digest("SHA-256", data);
    return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  function getCode() {
    return (localStorage.getItem(STORAGE_CODE) || "").trim();
  }

  function setCode(code) {
    const v = String(code || "").trim();
    if (v) localStorage.setItem(STORAGE_CODE, v);
    else localStorage.removeItem(STORAGE_CODE);
  }

  function readLocalCache() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_CACHE) || "null");
    } catch {
      return null;
    }
  }

  function writeLocalCache(payload, updatedAt) {
    localStorage.setItem(
      STORAGE_CACHE,
      JSON.stringify({ payload, updated_at: updatedAt || new Date().toISOString() })
    );
  }

  function restHeaders() {
    const c = cfg();
    return {
      apikey: c.anonKey,
      Authorization: "Bearer " + c.anonKey,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    };
  }

  function restUrl(pathQuery) {
    return String(cfg().url).replace(/\/$/, "") + "/rest/v1/" + pathQuery;
  }

  let saveTimer = null;
  let lastStatus = { state: "idle", message: "Not connected", at: null };
  const listeners = new Set();

  function setStatus(state, message, at) {
    lastStatus = { state, message, at: at || lastStatus.at };
    listeners.forEach((fn) => {
      try {
        fn(lastStatus);
      } catch (_) {}
    });
  }

  function onStatus(fn) {
    listeners.add(fn);
    fn(lastStatus);
    return () => listeners.delete(fn);
  }

  async function loadProgress() {
    const code = getCode();
    if (!code) {
      setStatus("idle", "Enter a sync code to connect");
      return readLocalCache()?.payload || null;
    }
    if (!configured()) {
      setStatus("error", "Sync not configured (missing Supabase keys)");
      return readLocalCache()?.payload || null;
    }

    const hash = await sha256Hex(code);
    setStatus("syncing", "Loading…");
    try {
      const res = await fetch(
        restUrl(TABLE + "?code_hash=eq." + encodeURIComponent(hash) + "&select=payload,updated_at"),
        { headers: restHeaders() }
      );
      if (!res.ok) throw new Error("HTTP " + res.status);
      const rows = await res.json();
      if (rows && rows[0]) {
        writeLocalCache(rows[0].payload, rows[0].updated_at);
        setStatus("connected", "Synced", rows[0].updated_at);
        return rows[0].payload;
      }
      const local = readLocalCache();
      setStatus("connected", "Connected (empty cloud)", local?.updated_at || null);
      return local?.payload || null;
    } catch (err) {
      const local = readLocalCache();
      setStatus("offline", "Offline — using local cache", local?.updated_at || null);
      return local?.payload || null;
    }
  }

  async function saveProgressNow(payload) {
    const code = getCode();
    if (!code) {
      writeLocalCache(payload);
      setStatus("idle", "Saved locally only (no sync code)");
      return false;
    }
    const updatedAt = new Date().toISOString();
    writeLocalCache(payload, updatedAt);

    if (!configured()) {
      setStatus("error", "Local save only — configure Supabase");
      return false;
    }

    const hash = await sha256Hex(code);
    setStatus("syncing", "Saving…");
    try {
      const res = await fetch(restUrl(TABLE), {
        method: "POST",
        headers: {
          ...restHeaders(),
          Prefer: "resolution=merge-duplicates,return=representation",
        },
        body: JSON.stringify({
          code_hash: hash,
          payload,
          updated_at: updatedAt,
        }),
      });
      if (!res.ok) throw new Error("HTTP " + res.status);
      setStatus("connected", "Synced", updatedAt);
      return true;
    } catch (err) {
      setStatus("offline", "Saved locally — will retry when online", updatedAt);
      return false;
    }
  }

  function saveProgress(payload) {
    writeLocalCache(payload);
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      saveProgressNow(payload);
    }, 500);
  }

  async function connect(code) {
    setCode(code);
    return loadProgress();
  }

  function disconnect() {
    setCode("");
    setStatus("idle", "Disconnected");
  }

  global.BS605Progress = {
    configured,
    getCode,
    setCode,
    connect,
    disconnect,
    loadProgress,
    saveProgress,
    saveProgressNow,
    onStatus,
    getStatus: () => lastStatus,
    readLocalCache,
  };

  global.addEventListener("online", () => {
    const cache = readLocalCache();
    if (cache?.payload && getCode()) saveProgressNow(cache.payload);
  });
})(window);
