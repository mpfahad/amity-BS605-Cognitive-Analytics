/* CSIT654 v3 LMS — shared app logic (AmityProgress + curriculum) */
(function (global) {
  const SUBJECT = "csit654_v3";
  const DATA = "../data";

  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );
  }

  function qs(name) {
    return new URLSearchParams(location.search).get(name);
  }

  async function loadJson(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error("Failed to load " + path);
    return res.json();
  }

  async function loadBundles() {
    const [curriculum, conceptsWrap, mcqWrap, pdfPages, conceptMaps] = await Promise.all([
      loadJson(DATA + "/curriculum.json"),
      loadJson(DATA + "/concepts.json"),
      loadJson(DATA + "/mcq_bank.json"),
      loadJson(DATA + "/pdf_pages.json").catch(() => null),
      loadJson(DATA + "/concept_maps.json").catch(() => null),
    ]);
    return {
      curriculum,
      concepts: conceptsWrap.concepts || conceptsWrap,
      questions: mcqWrap.questions || [],
      pdfPages,
      conceptMaps,
    };
  }

  function pdfHref(pdfPages, page) {
    // Use in-LMS PDF.js viewer — python http.server often blanks Chrome's native
    // viewer on large PDFs because it ignores Range requests.
    const file = (pdfPages && pdfPages.viewerFile) || "../source/slm.pdf";
    let href = "pdf-viewer.html?file=" + encodeURIComponent(file);
    if (page != null && page !== "") href += "&page=" + Number(page);
    return href;
  }

  function pdfLinkHtml(pdfPages, page, label) {
    const href = pdfHref(pdfPages, page);
    if (!href) return "";
    const text = label || (page ? "Open SLM PDF · p." + page : "Open SLM PDF");
    return `<a class="pdf-link" href="${esc(href)}" target="_blank" rel="noopener">${esc(text)}</a>`;
  }

  function topicStatus(prog, id, currentId) {
    const done = (prog.conceptDone || {})[id];
    const visited = (prog.visited || {})[id];
    if (currentId && id === currentId) return "current";
    if (done) return "done";
    if (visited) return "seen";
    return "todo";
  }

  function statusMark(status) {
    if (status === "done") return "✓";
    if (status === "current") return "●";
    if (status === "seen") return "◐";
    return "○";
  }

  /** Build sidebar HTML for a module overview or concept page. */
  function renderSidebar(mod, prog, opts) {
    opts = opts || {};
    const currentId = opts.currentId || null;
    const maps = opts.conceptMaps;
    const map = maps && maps.modules && maps.modules[String(mod.id)];
    let body = "";
    if (map && map.branches) {
      body = map.branches.map((br) => {
        const items = (br.nodes || []).map((n) => {
          const st = topicStatus(prog, n.id, currentId);
          return `<a class="nav-item ${st}${n.id === currentId ? " current" : ""}" href="concept.html?id=${encodeURIComponent(n.id)}">
            <span class="mark" aria-hidden="true">${statusMark(st)}</span>
            <span>${esc(n.label || n.id)}</span>
          </a>`;
        }).join("");
        return `<div class="nav-group"><div class="nav-group-label">${esc(br.label)}</div>${items}</div>`;
      }).join("");
    } else {
      body = (mod.topics || []).map((t) => {
        const st = topicStatus(prog, t.id, currentId);
        return `<a class="nav-item ${st}${t.id === currentId ? " current" : ""}" href="concept.html?id=${encodeURIComponent(t.id)}">
          <span class="mark" aria-hidden="true">${statusMark(st)}</span>
          <span>${esc(t.title)}</span>
        </a>`;
      }).join("");
    }
    const overviewCurrent = !currentId ? " current" : "";
    return `<h2>Module ${mod.id}</h2>
      <div class="course-name">${esc(mod.short)}</div>
      <div class="nav-section">
        <a class="nav-item${overviewCurrent}" href="module.html?m=${mod.id}">
          <span class="mark">◎</span><span>Overview</span>
        </a>
        ${body}
      </div>`;
  }

  function whereAmIPath(conceptMaps, conceptId, concept) {
    const preset = conceptMaps?.youAreHere?.[conceptId];
    if (preset && preset.length) return preset;
    const mid = String(concept?.module || conceptId.split(".")[0]);
    const map = conceptMaps?.modules?.[mid];
    if (!map) return ["Module " + mid, concept?.title || conceptId];
    for (const br of map.branches || []) {
      const hit = (br.nodes || []).find((n) => n.id === conceptId);
      if (hit) return [map.story ? ("Module " + mid) : ("Module " + mid), br.label, hit.label];
    }
    return ["Module " + mid, concept?.title || conceptId];
  }

  function renderConceptMap(mod, map, prog, currentId) {
    if (!map) return `<p class="subtle">Concept map not authored yet for this module.</p>`;
    const branches = (map.branches || []).map((br) => {
      const nodes = (br.nodes || []).map((n) => {
        const st = topicStatus(prog, n.id, currentId);
        return `<a class="cmap-node ${st}" href="concept.html?id=${encodeURIComponent(n.id)}">
          <strong>${esc(n.label)}</strong>
          ${n.sub ? `<span>${esc(n.sub)}</span>` : ""}
        </a>`;
      }).join("");
      return `<div class="cmap-branch">
        <div class="cmap-branch-head">
          <strong>${esc(br.label)}</strong>
          ${br.hint ? `<span>${esc(br.hint)}</span>` : ""}
        </div>
        <div class="cmap-nodes">${nodes}</div>
      </div>`;
    }).join('<div class="cmap-flow" aria-hidden="true">↓</div>');
    return `<p class="cmap-story">${esc(map.story || "")}</p>
      <div class="cmap-root">Module ${mod.id} · ${esc(mod.short)}</div>
      <div class="cmap-flow" aria-hidden="true">↓</div>
      ${branches}`;
  }

  function P() {
    return global.AmityProgress || global.BS605Progress;
  }

  function readProgress() {
    const api = P();
    if (!api?.getSubjectPayload) return {};
    const full = api.readLocalCache()?.payload || { subjects: {} };
    return api.getSubjectPayload(full, SUBJECT) || {};
  }

  function saveSection(key, value) {
    const api = P();
    if (!api?.saveSection) return;
    api.saveSection(key, value, SUBJECT);
  }

  function markVisited(conceptId) {
    const prog = readProgress();
    const visited = Object.assign({}, prog.visited || {});
    visited[conceptId] = true;
    saveSection("visited", visited);
  }

  function markConceptDone(conceptId) {
    const prog = readProgress();
    const done = Object.assign({}, prog.conceptDone || {});
    done[conceptId] = true;
    saveSection("conceptDone", done);
  }

  function savePracticeAnswer(qid, chosen, correct) {
    const prog = readProgress();
    const answers = Object.assign({}, prog.practiceAnswers || {});
    answers[qid] = { chosen, correct: !!correct, at: new Date().toISOString() };
    saveSection("practiceAnswers", answers);
  }

  function progressStats(curriculum) {
    const prog = readProgress();
    const visited = prog.visited || {};
    const done = prog.conceptDone || {};
    const answers = prog.practiceAnswers || {};
    const allIds = [];
    (curriculum.modules || []).forEach((m) =>
      (m.topics || []).forEach((t) => allIds.push(t.id))
    );
    const total = allIds.length || 1;
    const visitedN = allIds.filter((id) => visited[id]).length;
    const doneN = allIds.filter((id) => done[id]).length;
    const practiceN = Object.keys(answers).length;
    const practiceOk = Object.values(answers).filter((a) => a && a.correct).length;
    const pct = Math.round(((visitedN * 0.4 + doneN * 0.6) / total) * 100);
    return { total, visitedN, doneN, practiceN, practiceOk, pct };
  }

  function moduleById(curriculum, mid) {
    return (curriculum.modules || []).find((m) => Number(m.id) === Number(mid));
  }

  function questionsForConcept(questions, conceptId) {
    return (questions || []).filter((q) => q.conceptId === conceptId);
  }

  function questionsForModule(questions, mid) {
    return (questions || []).filter((q) => Number(q.module) === Number(mid));
  }

  function continueTarget(curriculum) {
    const prog = readProgress();
    const visited = prog.visited || {};
    const done = prog.conceptDone || {};
    for (const m of curriculum.modules || []) {
      for (const t of m.topics || []) {
        if (!done[t.id]) {
          return { module: m, topic: t, reason: visited[t.id] ? "Resume" : "Start" };
        }
      }
    }
    const last = curriculum.modules?.[0]?.topics?.[0];
    return last
      ? { module: curriculum.modules[0], topic: last, reason: "Review" }
      : null;
  }

  function renderMdish(text) {
    const raw = String(text || "");
    const lines = raw.split("\n");
    let html = "";
    let inUl = false;
    const flush = () => {
      if (inUl) {
        html += "</ul>";
        inUl = false;
      }
    };
    lines.forEach((line) => {
      const bullet = line.match(/^\s*[-•]\s+(.*)$/);
      if (bullet) {
        if (!inUl) {
          html += "<ul>";
          inUl = true;
        }
        html += "<li>" + inlineFmt(bullet[1]) + "</li>";
        return;
      }
      flush();
      if (!line.trim()) {
        html += "";
        return;
      }
      html += "<p>" + inlineFmt(line) + "</p>";
    });
    flush();
    return html || "<p></p>";
  }

  function inlineFmt(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  function isFlowCell(s) {
    const t = String(s || "").trim();
    if (!t) return true;
    return /^[→←↓↑↔∨∧|/−–—·or]+$/i.test(t) || t === "or" || t === "↓" || t === "→";
  }

  /** Render a concept diagram object: { title, rows: string[][] } or legacy { steps }. */
  function renderDiagram(diagram) {
    if (!diagram) return "";
    const title = diagram.title
      ? `<p class="diagram-caption">${esc(diagram.title)}</p>`
      : "";
    if (diagram.rows && diagram.rows.length) {
      const rows = diagram.rows
        .map((row) => {
          const cells = (row || [])
            .map((cell) => {
              const raw = String(cell ?? "");
              const cls = isFlowCell(raw) ? "flow" : "";
              return `<td class="${cls}">${esc(raw)}</td>`;
            })
            .join("");
          return `<tr>${cells}</tr>`;
        })
        .join("");
      return `${title}<table class="diagram-table" role="presentation">${rows}</table>`;
    }
    if (diagram.steps && diagram.steps.length) {
      const parts = diagram.steps
        .map((step, i) => {
          const box = `<div class="box${i === 0 ? " key" : ""}">${esc(step)}</div>`;
          return i < diagram.steps.length - 1
            ? box + `<div class="arrow" aria-hidden="true">↓</div>`
            : box;
        })
        .join("");
      return `${title}<div class="diagram">${parts}</div>`;
    }
    return title;
  }

  /** Rich wrong-answer panel: correct option + explanation + concept link. */
  function wrongAnswerHtml(q, concepts, opts) {
    opts = opts || {};
    const correct = Number(q.correct);
    const letter = String.fromCharCode(65 + correct);
    const optText = (q.options && q.options[correct]) || "";
    const c = concepts && concepts[q.conceptId];
    const title = (c && c.title) || q.conceptId;
    const confusion = c && (c.commonConfusion || (c.learn && c.learn.commonConfusion));
    let html =
      `<div class="feedback-wrong-detail">` +
      `<p class="answer-line"><strong>Correct answer:</strong> ${letter}. ${esc(optText)}</p>`;
    if (q.explanation) html += `<p>${esc(q.explanation)}</p>`;
    if (confusion && (confusion.body || confusion.text) && opts.showConfusion !== false) {
      html += `<p><em>${esc(confusion.title || "Watch out")}:</em> ${esc(
        String(confusion.body || confusion.text).replace(/\*\*/g, "").slice(0, 220)
      )}</p>`;
    }
    html +=
      `<p style="margin:0.55rem 0 0"><a class="concept-link" href="concept.html?id=${encodeURIComponent(
        q.conceptId
      )}&mode=learn">Review · ${esc(title)}</a></p></div>`;
    return html;
  }

  global.CSIT654V3 = {
    SUBJECT,
    esc,
    qs,
    loadBundles,
    P,
    readProgress,
    saveSection,
    markVisited,
    markConceptDone,
    savePracticeAnswer,
    progressStats,
    moduleById,
    questionsForConcept,
    questionsForModule,
    continueTarget,
    renderMdish,
    renderDiagram,
    wrongAnswerHtml,
    pdfHref,
    pdfLinkHtml,
    topicStatus,
    statusMark,
    renderSidebar,
    whereAmIPath,
    renderConceptMap,
  };
})(window);
