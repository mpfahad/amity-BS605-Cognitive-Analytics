/**
 * Amity multi-subject progress via sync code + Supabase.
 * One sync code covers all subjects. Same Supabase table as before.
 *
 * Payload: { subjects: { bs605: {quiz, flashcards, mapAnswers, mapVisited, mapMeta}, ... }, savedAt }
 * Legacy flat BS605 payloads + localStorage keys are migrated automatically
 * so existing progress stays available.
 */
(function (global) {
  const STORAGE_CODE = "amity_sync_code";
  const STORAGE_CACHE = "amity_progress_cache";
  const LEGACY_CODE = "bs605_sync_code";
  const LEGACY_CACHE = "bs605_progress_cache";
  const TABLE = "bs605_progress";

  function cfg() {
    return global.AMITY_SYNC || global.BS605_SYNC || {};
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

  function migrateLocalKeys() {
    try {
      if (!localStorage.getItem(STORAGE_CODE) && localStorage.getItem(LEGACY_CODE)) {
        localStorage.setItem(STORAGE_CODE, localStorage.getItem(LEGACY_CODE));
      }
      if (!localStorage.getItem(STORAGE_CACHE) && localStorage.getItem(LEGACY_CACHE)) {
        localStorage.setItem(STORAGE_CACHE, localStorage.getItem(LEGACY_CACHE));
      }
    } catch (_) {}
  }
  migrateLocalKeys();

  function getCode() {
    return (localStorage.getItem(STORAGE_CODE) || localStorage.getItem(LEGACY_CODE) || "").trim();
  }

  function setCode(code) {
    const v = String(code || "").trim();
    if (v) {
      localStorage.setItem(STORAGE_CODE, v);
      localStorage.setItem(LEGACY_CODE, v); // keep legacy in sync for old pages
    } else {
      localStorage.removeItem(STORAGE_CODE);
      localStorage.removeItem(LEGACY_CODE);
    }
  }

  function isLegacyFlat(payload) {
    if (!payload || typeof payload !== "object") return false;
    if (payload.subjects) return false;
    return Boolean(payload.quiz || payload.flashcards || payload.mapAnswers || payload.mapMeta);
  }

  /** Normalize any saved payload into { subjects: { ... } }. */
  function normalizePayload(raw) {
    if (!raw || typeof raw !== "object") return { subjects: {} };
    if (raw.subjects && typeof raw.subjects === "object") {
      return { subjects: Object.assign({}, raw.subjects), savedAt: raw.savedAt || null };
    }
    if (isLegacyFlat(raw)) {
      const bs605 = {};
      ["quiz", "flashcards", "mapAnswers", "mapMeta", "mapVisited"].forEach((k) => {
        if (raw[k] !== undefined) bs605[k] = raw[k];
      });
      return { subjects: { bs605 }, savedAt: raw.savedAt || null };
    }
    return { subjects: {}, savedAt: raw.savedAt || null };
  }

  function readLocalCache() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORAGE_CACHE) || localStorage.getItem(LEGACY_CACHE) || "null");
      if (!raw) return null;
      return {
        payload: normalizePayload(raw.payload || raw),
        updated_at: raw.updated_at || null,
      };
    } catch {
      return null;
    }
  }

  function writeLocalCache(payload, updatedAt) {
    const normalized = normalizePayload(payload);
    const blob = JSON.stringify({
      payload: normalized,
      updated_at: updatedAt || new Date().toISOString(),
    });
    localStorage.setItem(STORAGE_CACHE, blob);
    localStorage.setItem(LEGACY_CACHE, blob);
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
        out[k] = mergePayload(bv, pv);
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

  function currentSubject() {
    return String(global.AMITY_SUBJECT || "bs605").toLowerCase();
  }

  function getSubjectPayload(full, subjectId) {
    const n = normalizePayload(full);
    return (n.subjects && n.subjects[subjectId]) || {};
  }

  async function loadProgress() {
    const code = getCode();
    if (!code) {
      setStatus("idle", "Enter a sync code once — it stays on this device");
      return readLocalCache()?.payload || { subjects: {} };
    }
    if (!configured()) {
      setStatus("error", "Sync not configured (missing Supabase keys)");
      return readLocalCache()?.payload || { subjects: {} };
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
        const cloudNorm = normalizePayload(rows[0].payload);
        const localNorm = normalizePayload(local?.payload);
        let payload;
        let at;
        if (isNewer(local?.updated_at, rows[0].updated_at)) {
          payload = mergePayload(cloudNorm, localNorm);
          at = local.updated_at;
          writeLocalCache(payload, at);
          saveProgressNow(payload);
        } else {
          payload = mergePayload(localNorm, cloudNorm);
          at = rows[0].updated_at;
          writeLocalCache(payload, at);
          // If cloud was legacy flat, push normalized form once
          if (isLegacyFlat(rows[0].payload)) saveProgressNow(payload);
        }
        setStatus("connected", "Connected · auto-saves (" + maskedCode() + ")", at);
        return payload;
      }

      const payload = local?.payload || { subjects: {} };
      setStatus("connected", "Connected · auto-saves (" + maskedCode() + ")", local?.updated_at || null);
      if (payload && Object.keys(payload.subjects || {}).length) saveProgressNow(payload);
      return payload;
    } catch (err) {
      const local = readLocalCache();
      setStatus("offline", "Offline — will sync when online (" + maskedCode() + ")", local?.updated_at || null);
      return local?.payload || { subjects: {} };
    }
  }

  async function saveProgressNow(payload) {
    const code = getCode();
    const updatedAt = new Date().toISOString();
    const normalized = normalizePayload(payload);
    normalized.savedAt = updatedAt;
    writeLocalCache(normalized, updatedAt);

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
          payload: normalized,
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

  function saveProgress(patch) {
    const prev = readLocalCache()?.payload || { subjects: {} };
    const merged = mergePayload(prev, patch);
    merged.savedAt = new Date().toISOString();
    writeLocalCache(merged);
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => saveProgressNow(merged), 400);
  }

  /** Save one section for the active (or given) subject without wiping others. */
  function saveSection(sectionKey, sectionValue, subjectId) {
    const sid = subjectId || currentSubject();
    const patch = { subjects: {} };
    patch.subjects[sid] = {};
    patch.subjects[sid][sectionKey] = sectionValue;
    saveProgress(patch);
  }

  function saveSubjectProgress(subjectPatch, subjectId) {
    const sid = subjectId || currentSubject();
    const patch = { subjects: {} };
    patch.subjects[sid] = subjectPatch;
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

  async function clearProgress(subjectId) {
    const prev = readLocalCache()?.payload || { subjects: {} };
    const next = normalizePayload(prev);
    if (subjectId) {
      next.subjects[subjectId] = {};
    } else {
      next.subjects = {};
    }
    next.savedAt = new Date().toISOString();
    await saveProgressNow(next);
    return next;
  }

  function summarize(payload, totals, subjectId) {
    const sid = subjectId || currentSubject();
    const full = normalizePayload(payload);
    const p = getSubjectPayload(full, sid);
    const t = totals || {};
    const quizAnswers = (p.quiz && p.quiz.answers) || {};
    const quizAttempted = Object.keys(quizAnswers).length;
    let quizCorrect = 0;
    if (t.quizAnswerKey) {
      Object.entries(quizAnswers).forEach(([id, chosen]) => {
        if (t.quizAnswerKey[id] === chosen) quizCorrect += 1;
      });
    }
    const seen = (p.flashcards && p.flashcards.seen) || {};
    const known = (p.flashcards && p.flashcards.known) || {};
    const flashSeen = Object.keys(seen).filter((k) => seen[k]).length;
    const flashKnown = Object.keys(known).filter((k) => known[k]).length;
    const mapAnswers = p.mapAnswers || {};
    const mapVisited = p.mapVisited || {};
    let mapAttempted = 0;
    let mapCorrect = 0;
    if (t.mapAnswerKey) {
      Object.keys(t.mapAnswerKey).forEach((mid) => {
        const answers = mapAnswers[mid] || {};
        const key = t.mapAnswerKey[mid] || {};
        Object.keys(key).forEach((qi) => {
          if (answers[qi] !== undefined && answers[qi] !== null) {
            mapAttempted += 1;
            if (Number(answers[qi]) === Number(key[qi])) mapCorrect += 1;
          }
        });
      });
    } else {
      Object.values(mapAnswers).forEach((byQ) => {
        if (byQ && typeof byQ === "object") mapAttempted += Object.keys(byQ).length;
      });
    }
    return {
      quiz: { attempted: quizAttempted, correct: quizCorrect, total: t.quizTotal || 0 },
      flashcards: { seen: flashSeen, known: flashKnown, total: t.flashTotal || 0 },
      map: {
        attempted: mapAttempted,
        correct: mapCorrect,
        total: t.mapTotal || 0,
        visited: Object.keys(mapVisited).filter((k) => mapVisited[k]).length,
      },
      savedAt: full.savedAt || null,
    };
  }

  const api = {
    configured,
    getCode,
    setCode,
    maskedCode,
    connect,
    disconnect,
    loadProgress,
    saveProgress,
    saveSection,
    saveSubjectProgress,
    saveProgressNow,
    mergePayload,
    normalizePayload,
    getSubjectPayload,
    summarize,
    clearProgress,
    onStatus,
    getStatus: () => lastStatus,
    readLocalCache,
    currentSubject,
  };

  global.AmityProgress = api;
  global.BS605Progress = api; // backward compatible

  global.addEventListener("online", () => {
    const cache = readLocalCache();
    if (cache?.payload && getCode()) saveProgressNow(cache.payload);
  });
})(window);
