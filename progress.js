/**
 * BS605 cross-device progress via sync code + Supabase.
 * Config: window.BS605_SYNC = { url, anonKey } from config.js
 *
 * Once a sync code is saved on a device, it stays connected automatically.
 * Saves merge quiz / flashcards / mapAnswers so pages do not wipe each other.
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

  function isNewer(a, b) {
    if (!a) return false;
    if (!b) return true;
    return new Date(a).getTime() > new Date(b).getTime();
  }

  /** Shallow-merge top-level sections; nested objects merge one level deep. */
  function mergePayload(base, patch) {
    const out = Object.assign({}, base || {});
    if (!patch) return out;
    Object.keys(patch).forEach((k) => {
      const pv = patch[k];
      const bv = out[k];
      if (
        pv &&
        typeof pv === "object" &&
        !Array.isArray(pv) &&
        bv &&
        typeof bv === "object" &&
        !Array.isArray(bv)
      ) {
        out[k] = Object.assign({}, bv, pv);
      } else if (pv !== undefined) {
        out[k] = pv;
      }
    });
    return out;
  }

  let saveTimer = null;
  let lastStatus = { state: "idle", message: "Not connected", at: null };
  const listeners = new Set();

  function setStatus(state, message, at) {
    lastStatus = { state, message, at: at || null };
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

  function maskedCode() {
    const c = getCode();
    if (!c) return "";
    if (c.length <= 4) return "••••";
    return c.slice(0, 2) + "•••" + c.slice(-2);
  }

  async function loadProgress() {
    const code = getCode();
    if (!code) {
      setStatus("idle", "Enter a sync code once — it stays on this device");
      return readLocalCache()?.payload || null;
    }
    if (!configured()) {
      setStatus("error", "Sync not configured (missing Supabase keys)");
      return readLocalCache()?.payload || null;
    }

    const hash = await sha256Hex(code);
    setStatus("syncing", "Loading cloud…");
    try {
      const res = await fetch(
        restUrl(TABLE + "?code_hash=eq." + encodeURIComponent(hash) + "&select=payload,updated_at"),
        { headers: restHeaders() }
      );
      if (!res.ok) throw new Error("HTTP " + res.status);
      const rows = await res.json();
      const local = readLocalCache();

      if (rows && rows[0]) {
        const cloud = rows[0];
        // Prefer newer side, then merge so quiz/map/flashcards are not lost
        let payload;
        let at;
        if (isNewer(local?.updated_at, cloud.updated_at)) {
          payload = mergePayload(cloud.payload, local.payload);
          at = local.updated_at;
          writeLocalCache(payload, at);
          // Push merged newer local up so phone gets it
          saveProgressNow(payload);
        } else {
          payload = mergePayload(local?.payload, cloud.payload);
          at = cloud.updated_at;
          writeLocalCache(payload, at);
        }
        setStatus("connected", "Connected · auto-saves (" + maskedCode() + ")", at);
        return payload;
      }

      const payload = local?.payload || null;
      setStatus("connected", "Connected · auto-saves (" + maskedCode() + ")", local?.updated_at || null);
      if (payload) saveProgressNow(payload);
      return payload;
    } catch (err) {
      const local = readLocalCache();
      setStatus("offline", "Offline — will sync when online (" + maskedCode() + ")", local?.updated_at || null);
      return local?.payload || null;
    }
  }

  async function saveProgressNow(payload) {
    const code = getCode();
    const updatedAt = new Date().toISOString();
    writeLocalCache(payload, updatedAt);

    if (!code) {
      setStatus("idle", "Saved on this device only (no sync code yet)");
      return false;
    }
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
      setStatus("connected", "Connected · auto-saves (" + maskedCode() + ")", updatedAt);
      return true;
    } catch (err) {
      setStatus("offline", "Saved locally — will retry when online", updatedAt);
      return false;
    }
  }

  function saveProgress(payload) {
    const prev = readLocalCache()?.payload || {};
    const merged = mergePayload(prev, payload);
    merged.savedAt = new Date().toISOString();
    writeLocalCache(merged);
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      saveProgressNow(merged);
    }, 400);
  }

  /** Update one section (quiz / flashcards / mapAnswers) without wiping others. */
  function saveSection(sectionKey, sectionValue) {
    const patch = {};
    patch[sectionKey] = sectionValue;
    saveProgress(patch);
  }

  async function connect(code) {
    setCode(code);
    return loadProgress();
  }

  function disconnect() {
    setCode("");
    setStatus("idle", "Disconnected — enter a sync code to reconnect");
  }

  global.BS605Progress = {
    configured,
    getCode,
    setCode,
    maskedCode,
    connect,
    disconnect,
    loadProgress,
    saveProgress,
    saveSection,
    saveProgressNow,
    mergePayload,
    onStatus,
    getStatus: () => lastStatus,
    readLocalCache,
  };

  global.addEventListener("online", () => {
    const cache = readLocalCache();
    if (cache?.payload && getCode()) saveProgressNow(cache.payload);
  });
})(window);
