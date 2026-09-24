#!/usr/bin/env python3
"""Build flashcards.html, quiz.html, module-map.html, and index.html from study JSON."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "_study_facts.json").read_text(encoding="utf-8"))
MAPS = json.loads((ROOT / "_module_maps.json").read_text(encoding="utf-8"))
LMR = (ROOT / "_lmr_notes.txt").read_text(encoding="utf-8")
PDF_NAME = "Congnitive Analytics and Social skill for Profession W F 1.pdf"
LINKS = [
    ("Live Class 2 transcript", "Live Class 2 Transcript.txt"),
    ("Live Class 3 transcript", "Live Class 3 Transcript.txt"),
    ("Study PDF (SLM)", PDF_NAME),
]

SHARED_CSS = r"""
:root {
  --ink: #15231c;
  --muted: #4a5c52;
  --paper: #f3f6f1;
  --panel: rgba(255,255,255,0.78);
  --line: rgba(21,35,28,0.12);
  --accent: #0f6b4c;
  --accent-2: #c45c26;
  --accent-soft: #d8efe4;
  --warn: #8a3b12;
  --ok: #1f7a4d;
  --bad: #a33b3b;
  --shadow: 0 18px 50px rgba(21,35,28,0.12);
  --radius: 18px;
  --font-display: "Fraunces", Georgia, serif;
  --font-body: "Source Sans 3", "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  font-family: var(--font-body);
  background:
    radial-gradient(1200px 600px at 10% -10%, #d7ebe0 0%, transparent 55%),
    radial-gradient(900px 500px at 100% 0%, #f3dfd0 0%, transparent 45%),
    linear-gradient(180deg, #eef4ef 0%, var(--paper) 40%, #e7eee8 100%);
  min-height: 100vh;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.35;
  background-image:
    linear-gradient(rgba(21,35,28,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(21,35,28,0.03) 1px, transparent 1px);
  background-size: 28px 28px;
  mask-image: linear-gradient(180deg, #000, transparent 85%);
}
a { color: var(--accent); }
.wrap { width: min(1120px, calc(100% - 2rem)); margin: 0 auto; padding: 1.5rem 0 3rem; position: relative; }
.hero {
  display: grid;
  gap: 1rem;
  padding: 1.6rem 0 1.2rem;
  animation: rise 0.6s ease both;
}
.kicker {
  display: inline-flex;
  gap: 0.5rem;
  align-items: center;
  color: var(--accent);
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-size: 0.78rem;
}
h1 {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.1;
  margin: 0.2rem 0;
  letter-spacing: -0.02em;
}
.lede { margin: 0; max-width: 46rem; color: var(--muted); font-size: 1.05rem; }
.navrow {
  display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.6rem;
}
.btn, button.btn {
  appearance: none;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  border-radius: 999px;
  padding: 0.55rem 1rem;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  backdrop-filter: blur(8px);
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.btn:hover, button.btn:hover { transform: translateY(-1px); border-color: rgba(15,107,76,0.35); }
.btn.primary { background: var(--accent); color: #fff; border-color: transparent; }
.btn.ghost { background: transparent; }
.panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
  padding: 1rem;
}
.filters {
  display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;
}
.chip {
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.65);
  border-radius: 999px;
  padding: 0.4rem 0.85rem;
  font-weight: 600;
  cursor: pointer;
  font: inherit;
}
.chip.active {
  background: var(--accent);
  color: #fff;
  border-color: transparent;
}
.chip.lmr {
  border-color: rgba(196,92,38,0.45);
  color: var(--warn);
}
.chip.lmr.active { background: var(--accent-2); color: #fff; }
.site-nav {
  display: flex; flex-wrap: wrap; gap: 0.45rem;
  align-items: center;
  margin: 0 0 0.4rem;
  padding: 0.55rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.82);
  backdrop-filter: blur(8px);
  width: fit-content;
  max-width: 100%;
}
.site-nav a {
  appearance: none;
  border: 1px solid transparent;
  background: transparent;
  color: var(--ink);
  border-radius: 999px;
  padding: 0.4rem 0.85rem;
  font: inherit;
  font-weight: 700;
  font-size: 0.92rem;
  text-decoration: none;
}
.site-nav a:hover { background: var(--accent-soft); color: var(--accent); }
.site-nav a.home {
  background: var(--accent);
  color: #fff;
}
.site-nav a.here {
  background: var(--accent-soft);
  color: var(--accent);
}
.meta {
  display: flex; flex-wrap: wrap; gap: 0.75rem 1.2rem;
  color: var(--muted); font-size: 0.95rem; margin-bottom: 1rem;
}
.meta strong { color: var(--ink); }
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.6rem;
  margin: 0.8rem 0;
}
.stat {
  background: rgba(255,255,255,0.75);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.8rem;
}
.stat b { display: block; font-size: 1.35rem; font-family: var(--font-display); color: var(--ink); }
.stat span { color: var(--muted); font-size: 0.88rem; }
.prog-line {
  margin-top: 0.55rem;
  height: 7px;
  border-radius: 999px;
  background: rgba(21,35,28,0.08);
  overflow: hidden;
}
.prog-line > i {
  display: block;
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--accent), #2f9e74);
  border-radius: inherit;
}
.links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.5rem;
  margin-top: 0.8rem;
}
.links a {
  display: block;
  text-decoration: none;
  padding: 0.7rem 0.85rem;
  border-radius: 12px;
  background: rgba(255,255,255,0.7);
  border: 1px solid var(--line);
  color: var(--ink);
  font-weight: 600;
  font-size: 0.92rem;
}
.links a.lmr-link {
  background: linear-gradient(135deg, #fff4ec, #ffe8d8);
  border-color: rgba(196,92,38,0.25);
}
@keyframes rise {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: none; }
}
@keyframes flipIn {
  from { opacity: 0; transform: rotateX(-8deg) translateY(8px); }
  to { opacity: 1; transform: none; }
}
@media (max-width: 720px) {
  .wrap { width: min(100% - 1.2rem, 1120px); }
}
"""

FLASH_CSS = SHARED_CSS + r"""
.stage {
  display: grid;
  gap: 1rem;
  margin-top: 0.5rem;
}
.flash-shell {
  min-height: 320px;
}
.flash-card {
  position: relative;
  width: 100%;
  min-height: 320px;
  cursor: pointer;
  animation: flipIn 0.35s ease both;
  border: none;
  padding: 0;
  background: transparent;
  text-align: left;
  font: inherit;
  color: inherit;
}
.face {
  min-height: 320px;
  border-radius: calc(var(--radius) + 4px);
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background:
    linear-gradient(160deg, rgba(255,255,255,0.95), rgba(232,244,238,0.92));
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.face.back {
  display: none;
  background:
    linear-gradient(160deg, rgba(255,248,242,0.97), rgba(255,255,255,0.94));
}
.flash-card.flipped .face.front { display: none; }
.flash-card.flipped .face.back { display: flex; }
.flash-card:focus-visible {
  outline: 3px solid rgba(15,107,76,0.45);
  outline-offset: 4px;
  border-radius: calc(var(--radius) + 4px);
}
.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  width: fit-content;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 0.28rem 0.65rem;
  border-radius: 999px;
}
.tag.warn { color: var(--warn); background: #f8e5d8; }
.prompt {
  font-family: var(--font-display);
  font-size: clamp(1.35rem, 2.6vw, 1.9rem);
  line-height: 1.25;
  margin: 1rem 0;
}
.answer {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--ink);
}
.detail {
  margin-top: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px dashed var(--line);
  color: var(--muted);
  font-size: 0.95rem;
}
.hint { color: var(--muted); font-size: 0.9rem; }
.controls {
  display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; justify-content: space-between;
}
.progress {
  height: 8px; border-radius: 999px; background: rgba(21,35,28,0.08); overflow: hidden; margin: 0.4rem 0 0.8rem;
}
.progress > span {
  display: block; height: 100%; width: 0%;
  background: linear-gradient(90deg, var(--accent), #2f9e74);
  transition: width 0.25s ease;
}
.topic-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.65rem;
  margin-top: 1.2rem;
}
.topic-list button {
  text-align: left;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.7);
  border-radius: 14px;
  padding: 0.8rem 0.9rem;
  cursor: pointer;
  font: inherit;
}
.topic-list button strong { display: block; margin-bottom: 0.15rem; }
.topic-list button span { color: var(--muted); font-size: 0.88rem; }
.topic-list button.active {
  border-color: rgba(15,107,76,0.4);
  background: #e8f5ee;
}
.lmr-box {
  margin-top: 1.4rem;
  padding: 1rem 1.1rem;
  border-radius: var(--radius);
  border: 1px solid rgba(196,92,38,0.25);
  background: linear-gradient(135deg, rgba(255,244,236,0.95), rgba(255,255,255,0.85));
}
.lmr-box h2 {
  font-family: var(--font-display);
  margin: 0 0 0.5rem;
  font-size: 1.35rem;
}
.lmr-box ol { margin: 0.4rem 0 0; padding-left: 1.2rem; color: var(--muted); }
.lmr-box li { margin: 0.35rem 0; }
"""

QUIZ_CSS = SHARED_CSS + r"""
.progress {
  height: 8px; border-radius: 999px; background: rgba(21,35,28,0.08); overflow: hidden;
}
.progress > span {
  display: block; height: 100%; width: 0%;
  background: linear-gradient(90deg, var(--accent), #2f9e74);
  transition: width 0.25s ease;
}
.quiz-layout { display: grid; gap: 1rem; }
.qcard {
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.82);
  border-radius: var(--radius);
  padding: 1.1rem 1.15rem;
  box-shadow: var(--shadow);
  animation: flipIn 0.35s ease both;
}
.qhead {
  display: flex; justify-content: space-between; gap: 0.8rem; flex-wrap: wrap;
  margin-bottom: 0.7rem;
}
.qnum {
  font-weight: 700; color: var(--accent); font-size: 0.85rem; letter-spacing: 0.03em;
}
.qtext {
  font-family: var(--font-display);
  font-size: clamp(1.15rem, 2vw, 1.4rem);
  line-height: 1.3;
  margin: 0 0 0.9rem;
}
.options { display: grid; gap: 0.55rem; }
.opt {
  display: flex; gap: 0.7rem; align-items: flex-start;
  width: 100%;
  text-align: left;
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 14px;
  padding: 0.75rem 0.85rem;
  cursor: pointer;
  font: inherit;
  transition: border-color 0.15s ease, background 0.15s ease, transform 0.15s ease;
}
.opt:hover:not(:disabled) { transform: translateY(-1px); border-color: rgba(15,107,76,0.35); }
.opt .letter {
  flex: 0 0 auto;
  width: 1.55rem; height: 1.55rem;
  border-radius: 50%;
  display: grid; place-items: center;
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 700;
  font-size: 0.82rem;
}
.opt.correct {
  border-color: rgba(31,122,77,0.55);
  background: #e8f7ef;
}
.opt.wrong {
  border-color: rgba(163,59,59,0.45);
  background: #fdeeee;
}
.opt:disabled { cursor: default; }
.explain {
  margin-top: 0.85rem;
  padding: 0.75rem 0.85rem;
  border-radius: 12px;
  background: #f2f7f4;
  color: var(--muted);
  display: none;
}
.explain.show { display: block; }
.scorebar {
  display: flex; flex-wrap: wrap; gap: 0.8rem; align-items: center; justify-content: space-between;
}
.score {
  font-family: var(--font-display);
  font-size: 1.4rem;
}
.footer-nav {
  display: flex; flex-wrap: wrap; gap: 0.6rem; justify-content: space-between; margin-top: 0.8rem;
}
"""


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def links_html() -> str:
    items = []
    for label, url in LINKS:
        cls = "lmr-link" if "PDF" in label or "LMR" in label else ""
        items.append(f'<a class="{cls}" href="{html_escape(url)}" target="_blank" rel="noopener">{html_escape(label)}</a>')
    return '<div class="links">' + "".join(items) + "</div>"


SYNC_HEAD = """
<script src="config.js"></script>
<script src="progress.js"></script>
<script src="sync-ui.js"></script>
"""

SYNC_PANEL = '<div id="bs605-sync-root"></div>'


def site_nav(active: str) -> str:
    """Top nav with Home always first and highlighted."""
    items = [
        ("home", "index.html", "Home"),
        ("map", "module-map.html", "Module Map"),
        ("flash", "flashcards.html", "Flashcards"),
        ("quiz", "quiz.html", "Quiz"),
    ]
    parts = []
    for key, href, label in items:
        cls = []
        if key == "home":
            cls.append("home")
        if key == active:
            cls.append("here")
        class_attr = f' class="{" ".join(cls)}"' if cls else ""
        parts.append(f'<a href="{href}"{class_attr}>{label}</a>')
    return '<nav class="site-nav" aria-label="Site">' + "".join(parts) + "</nav>"


SYNC_BOOT = """
function bootSync(restoreFn) {
  function apply(payload) {
    if (payload && restoreFn) restoreFn(payload);
    window.__BS605_SYNC_READY = true;
  }
  if (window.BS605SyncUI) {
    BS605SyncUI.mount(document.getElementById("bs605-sync-root"), {
      onLoaded: (payload) => apply(payload),
      onReady: (payload) => {
        if (window.__BS605_SYNC_READY) return;
        apply(payload || (window.BS605Progress && BS605Progress.readLocalCache() || {}).payload || null);
      }
    });
  } else {
    apply((window.BS605Progress && BS605Progress.readLocalCache() || {}).payload || null);
  }
}
"""


def count_totals() -> dict:
    flash_total = 0
    quiz_total = 0
    quiz_answer_key = {}
    for m in DATA["modules"]:
        for t in m["topics"]:
            flash_total += len(t.get("flashcards") or [])
            for i, q in enumerate(t.get("mcqs") or []):
                qid = f'{m["id"]}-{t["id"]}-q{i}'
                quiz_answer_key[qid] = q["answer"]
                quiz_total += 1
    maps = enrich_maps_payload()
    map_total = 0
    map_answer_key = {}
    for mod in maps["modules"]:
        mid = str(mod["id"])
        map_answer_key[mid] = {}
        for qi, q in enumerate(mod.get("questions") or []):
            map_answer_key[mid][str(qi)] = q["answer"]
            map_total += 1
    return {
        "flashTotal": flash_total,
        "quizTotal": quiz_total,
        "mapTotal": map_total,
        "quizAnswerKey": quiz_answer_key,
        "mapAnswerKey": map_answer_key,
    }


def build_flashcards() -> str:
    data_json = json.dumps(DATA, ensure_ascii=False)
    lmr_items = []
    for line in LMR.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        # Strip leading "12. " style numbering; <ol> provides numbers
        text = line.split(". ", 1)[1] if ". " in line[:4] else line
        lmr_items.append(f"<li>{html_escape(text)}</li>")
    lmr_items = "".join(lmr_items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>BS605 Flashcards — Cognitive Analytics & Social Skills</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
<style>{FLASH_CSS}</style>
{SYNC_HEAD}
</head>
<body>
<div class="wrap">
  {site_nav("flash")}
  <header class="hero">
    <div class="kicker">Amity · BS605</div>
    <h1>Cognitive Analytics &amp; Social Skills flashcards</h1>
    <p class="lede">Quick-reference cards drilled from the SLM and live-class transcripts across all five modules. Flip a card, then move topic by topic — LMR priorities are marked for exam focus.</p>
    <div class="navrow">
      <a class="btn" href="#lmr">LMR priorities</a>
      <a class="btn ghost" href="{PDF_NAME}" target="_blank">Open PDF</a>
    </div>
  </header>

  <section class="panel">
    <div class="meta">
      <span><strong id="countCards">0</strong> cards in view</span>
      <span>Seen <strong id="seenCount">0</strong> / <strong id="deckTotal">0</strong></span>
      <span>Known <strong id="knownCount">0</strong></span>
      <span>Still learning <strong id="learningCount">0</strong></span>
    </div>
    <div class="summary-grid" id="flashStats"></div>
    <div class="filters" id="moduleFilters"></div>
    {links_html()}
    {SYNC_PANEL}
  </section>

  <section class="stage">
    <div class="progress"><span id="progressBar"></span></div>
    <div class="controls">
      <div class="meta" style="margin:0">
        <span id="position">1 / 1</span>
        <span id="topicLabel"></span>
      </div>
      <div class="navrow" style="margin:0">
        <button class="btn" id="prevBtn" type="button">Previous</button>
        <button class="btn primary" id="flipBtn" type="button">Reveal answer</button>
        <button class="btn" id="nextBtn" type="button">Next</button>
      </div>
    </div>
    <div class="flash-shell">
      <button type="button" class="flash-card" id="card" aria-label="Reveal answer">
        <div class="face front">
          <span class="tag" id="frontTag">Module</span>
          <div>
            <div class="prompt" id="frontText"></div>
            <div class="hint">Click this card (or press Space) to reveal the answer</div>
          </div>
          <div></div>
        </div>
        <div class="face back">
          <span class="tag warn" id="backTag">Answer</span>
          <div>
            <div class="answer" id="backText"></div>
            <div class="detail" id="backDetail"></div>
          </div>
          <div class="hint">Mark how well you know it, then continue</div>
        </div>
      </button>
    </div>
    <div class="navrow" style="margin-top:0.8rem">
      <button class="btn primary" id="knownBtn" type="button">Got it</button>
      <button class="btn" id="learningBtn" type="button">Still learning</button>
      <button class="btn ghost" id="resetFlashBtn" type="button">Reset card progress</button>
    </div>
    <div class="topic-list" id="topicList"></div>
  </section>

  <section class="lmr-box" id="lmr">
    <h2>LMR — important topics</h2>
    <p class="lede" style="margin-bottom:0.4rem">From the last revision class focus and the densest exam-ready material in the SLM:</p>
    <ol>{lmr_items}</ol>
  </section>
</div>
<script>
const DATA = {data_json};
const deck = [];
DATA.modules.forEach(m => {{
  m.topics.forEach(t => {{
    (t.flashcards || []).forEach((c, i) => {{
      deck.push({{
        moduleId: m.id,
        moduleTitle: m.title,
        topicId: t.id,
        topicTitle: t.title,
        front: c.front,
        back: c.back,
        detail: c.detail || "",
        key: m.id + "-" + t.id + "-" + i
      }});
    }});
  }});
}});

let activeModule = "all";
let filtered = deck.slice();
let index = 0;
let flipped = false;
let seen = {{}};   // key -> true
let known = {{}};  // key -> true
let restoring = false;

const el = id => document.getElementById(id);
const card = el("card");
const progressBar = el("progressBar");
el("deckTotal").textContent = deck.length;

function renderFilters() {{
  const box = el("moduleFilters");
  const mods = [{{id:"all", title:"All modules"}}, ...DATA.modules.map(m => ({{id:String(m.id), title:"M"+m.id+": "+m.title}}))];
  box.innerHTML = mods.map(m => `<button type="button" class="chip ${{String(activeModule)===String(m.id)?"active":""}}" data-m="${{m.id}}">${{m.title}}</button>`).join("")
    + `<button type="button" class="chip lmr" data-jump="lmr">LMR list</button>`;
  box.querySelectorAll("[data-m]").forEach(btn => btn.addEventListener("click", () => {{
    activeModule = btn.dataset.m;
    applyFilter();
    renderFilters();
  }}));
  box.querySelectorAll("[data-jump]").forEach(btn => btn.addEventListener("click", () => {{
    document.getElementById("lmr").scrollIntoView({{behavior:"smooth"}});
  }}));
}}

function updateFlashStats() {{
  const seenN = Object.keys(seen).filter(k => seen[k]).length;
  const knownN = Object.keys(known).filter(k => known[k]).length;
  const learningN = Math.max(0, seenN - knownN);
  el("seenCount").textContent = seenN;
  el("knownCount").textContent = knownN;
  el("learningCount").textContent = learningN;
  const box = el("flashStats");
  box.innerHTML = DATA.modules.map(m => {{
    const keys = deck.filter(c => c.moduleId === m.id).map(c => c.key);
    const s = keys.filter(k => seen[k]).length;
    const kn = keys.filter(k => known[k]).length;
    const pct = keys.length ? Math.round((s / keys.length) * 100) : 0;
    return `<div class="stat"><b>${{s}}/${{keys.length}}</b><span>Module ${{m.id}} · ${{kn}} known</span><div class="prog-line"><i style="width:${{pct}}%"></i></div></div>`;
  }}).join("");
}}

function persistFlash() {{
  if (restoring || !window.BS605Progress || !window.__BS605_SYNC_READY) return;
  BS605Progress.saveSection("flashcards", {{
    activeModule: String(activeModule),
    index: index,
    flipped: flipped,
    seen: {{ ...seen }},
    known: {{ ...known }}
  }});
}}

function restoreFlash(payload) {{
  if (!payload || !payload.flashcards) return;
  restoring = true;
  const f = payload.flashcards;
  if (f.activeModule !== undefined) activeModule = String(f.activeModule);
  seen = (f.seen && typeof f.seen === "object") ? {{ ...f.seen }} : {{}};
  known = (f.known && typeof f.known === "object") ? {{ ...f.known }} : {{}};
  applyFilter();
  if (typeof f.index === "number" && filtered.length) {{
    index = Math.max(0, Math.min(filtered.length - 1, f.index));
  }}
  flipped = Boolean(f.flipped);
  renderFilters();
  renderTopics();
  renderCard();
  updateFlashStats();
  restoring = false;
}}

function applyFilter() {{
  filtered = activeModule === "all" ? deck.slice() : deck.filter(c => String(c.moduleId) === String(activeModule));
  index = 0;
  flipped = false;
  el("countCards").textContent = filtered.length;
  renderTopics();
  renderCard();
  updateFlashStats();
  persistFlash();
}}

function renderTopics() {{
  const topics = [];
  const seenT = new Set();
  filtered.forEach(c => {{
    const k = c.topicId;
    if (!seenT.has(k)) {{ seenT.add(k); topics.push(c); }}
  }});
  el("topicList").innerHTML = topics.map(t => {{
    const active = filtered[index] && filtered[index].topicId === t.topicId ? "active" : "";
    const topicKeys = filtered.filter(c => c.topicId === t.topicId).map(c => c.key);
    const done = topicKeys.filter(k => known[k]).length;
    return `<button type="button" class="${{active}}" data-topic="${{t.topicId}}"><strong>${{t.topicId}} · ${{t.topicTitle}}</strong><span>Module ${{t.moduleId}} · ${{done}}/${{topicKeys.length}} known</span></button>`;
  }}).join("");
  el("topicList").querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    const i = filtered.findIndex(c => c.topicId === btn.dataset.topic);
    if (i >= 0) {{ index = i; flipped = false; renderCard(); renderTopics(); persistFlash(); }}
  }}));
}}

function renderCard() {{
  if (!filtered.length) {{
    el("frontText").textContent = "No cards in this filter.";
    el("backText").textContent = "";
    el("backDetail").textContent = "";
    el("position").textContent = "0 / 0";
    progressBar.style.width = "0%";
    return;
  }}
  const c = filtered[index];
  el("frontTag").textContent = `Module ${{c.moduleId}} · ${{c.topicId}}`;
  el("backTag").textContent = c.topicTitle + (known[c.key] ? " · known" : seen[c.key] ? " · learning" : "");
  el("frontText").textContent = c.front;
  el("backText").textContent = c.back;
  el("backDetail").textContent = c.detail || "";
  el("backDetail").style.display = c.detail ? "block" : "none";
  el("topicLabel").textContent = c.topicTitle;
  el("position").textContent = `${{index+1}} / ${{filtered.length}}`;
  const seenInFilter = filtered.filter(x => seen[x.key]).length;
  progressBar.style.width = `${{(seenInFilter/filtered.length)*100}}%`;
  card.classList.toggle("flipped", flipped);
  card.setAttribute("aria-label", flipped ? "Hide answer" : "Reveal answer");
  el("flipBtn").textContent = flipped ? "Hide answer" : "Reveal answer";
}}

function markSeen() {{
  if (!filtered.length) return;
  const key = filtered[index].key;
  seen[key] = true;
  updateFlashStats();
  persistFlash();
}}

function flip() {{
  flipped = !flipped;
  if (flipped) markSeen();
  card.classList.toggle("flipped", flipped);
  card.setAttribute("aria-label", flipped ? "Hide answer" : "Reveal answer");
  el("flipBtn").textContent = flipped ? "Hide answer" : "Reveal answer";
  persistFlash();
}}
function next() {{ if (!filtered.length) return; index = (index + 1) % filtered.length; flipped = false; renderCard(); renderTopics(); persistFlash(); }}
function prev() {{ if (!filtered.length) return; index = (index - 1 + filtered.length) % filtered.length; flipped = false; renderCard(); renderTopics(); persistFlash(); }}

function markKnown(isKnown) {{
  if (!filtered.length) return;
  const key = filtered[index].key;
  seen[key] = true;
  if (isKnown) known[key] = true;
  else delete known[key];
  updateFlashStats();
  renderTopics();
  renderCard();
  persistFlash();
  next();
}}

card.addEventListener("click", (e) => {{ e.preventDefault(); flip(); }});
el("flipBtn").addEventListener("click", (e) => {{ e.preventDefault(); flip(); }});
el("nextBtn").addEventListener("click", next);
el("prevBtn").addEventListener("click", prev);
el("knownBtn").addEventListener("click", () => markKnown(true));
el("learningBtn").addEventListener("click", () => markKnown(false));
el("resetFlashBtn").addEventListener("click", () => {{
  if (!confirm("Clear seen/known progress for all flashcards?")) return;
  seen = {{}};
  known = {{}};
  updateFlashStats();
  renderTopics();
  renderCard();
  persistFlash();
}});
document.addEventListener("keydown", e => {{
  if (e.code === "Space" && !["INPUT","TEXTAREA","SELECT"].includes((e.target||{{}}).tagName)) {{
    e.preventDefault();
    flip();
  }}
  if (e.key === "ArrowRight") next();
  if (e.key === "ArrowLeft") prev();
}});

renderFilters();
applyFilter();
{SYNC_BOOT}
bootSync(restoreFlash);
</script>
</body>
</html>
"""


def build_quiz() -> str:
    data_json = json.dumps(DATA, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>BS605 Objective Questions — Cognitive Analytics & Social Skills</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
<style>{QUIZ_CSS}</style>
{SYNC_HEAD}
</head>
<body>
<div class="wrap">
  {site_nav("quiz")}
  <header class="hero">
    <div class="kicker">Amity · BS605</div>
    <h1>Objective questions by module</h1>
    <p class="lede">MCQs drawn from the BS605 SLM and live-class emphasis. Filter by module, answer one by one, and use explanations to lock concepts — especially LMR priorities.</p>
    <div class="navrow">
      <a class="btn" href="flashcards.html#lmr">LMR priorities</a>
    </div>
  </header>

  <section class="panel">
    <div class="scorebar">
      <div class="meta" style="margin:0">
        <span><strong id="totalQ">0</strong> questions</span>
        <span>Answered <strong id="attempted">0</strong></span>
        <span>Correct <strong id="scoreNow">0</strong></span>
        <span>Accuracy <strong id="accuracy">—</strong></span>
      </div>
      <div class="navrow" style="margin:0">
        <button class="btn" id="resetBtn" type="button">Reset answers</button>
        <button class="btn primary" id="shuffleBtn" type="button">Shuffle</button>
      </div>
    </div>
    <div class="progress" style="margin-top:0.75rem"><span id="quizProgressBar"></span></div>
    <div class="filters" id="moduleFilters" style="margin-top:0.9rem"></div>
    <div class="summary-grid" id="moduleStats"></div>
    {links_html()}
    {SYNC_PANEL}
  </section>

  <section class="quiz-layout" style="margin-top:1rem">
    <div class="qcard" id="qcard">
      <div class="qhead">
        <span class="qnum" id="qnum"></span>
        <span class="qnum" id="qtopic"></span>
      </div>
      <h2 class="qtext" id="qtext"></h2>
      <div class="options" id="options"></div>
      <div class="explain" id="explain"></div>
      <div class="footer-nav">
        <button class="btn" id="prevBtn" type="button">Previous</button>
        <button class="btn primary" id="nextBtn" type="button">Next</button>
      </div>
    </div>
  </section>
</div>
<script>
const DATA = {data_json};
const bank = [];
DATA.modules.forEach(m => {{
  m.topics.forEach(t => {{
    (t.mcqs || []).forEach((q, i) => {{
      bank.push({{
        moduleId: m.id,
        moduleTitle: m.title,
        topicId: t.id,
        topicTitle: t.title,
        q: q.q,
        options: q.options,
        answer: q.answer,
        explain: q.explain || "",
        id: m.id + "-" + t.id + "-q" + i
      }});
    }});
  }});
}});

let activeModule = "all";
let order = bank.map((_, i) => i);
let filteredIds = order.slice();
let index = 0;
const state = {{}}; // id -> selected option index
let restoring = false;

const el = id => document.getElementById(id);
const quizProgressBar = el("quizProgressBar");

function shuffle(arr) {{
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }}
  return a;
}}

function currentList() {{
  return filteredIds.map(i => bank[i]);
}}

function persistQuiz() {{
  if (restoring || !window.BS605Progress || !window.__BS605_SYNC_READY) return;
  BS605Progress.saveSection("quiz", {{
    activeModule: String(activeModule),
    index: index,
    answers: {{ ...state }},
    filteredIds: filteredIds.slice(),
    order: order.slice()
  }});
}}

function restoreQuiz(payload) {{
  if (!payload || !payload.quiz) return;
  restoring = true;
  const q = payload.quiz;
  if (q.activeModule !== undefined) activeModule = String(q.activeModule);
  Object.keys(state).forEach(k => delete state[k]);
  if (q.answers && typeof q.answers === "object") {{
    Object.entries(q.answers).forEach(([k, v]) => {{ state[k] = v; }});
  }}
  if (Array.isArray(q.order) && q.order.length === bank.length) order = q.order.slice();
  applyFilter(true);
  if (Array.isArray(q.filteredIds) && q.filteredIds.length) {{
    const allowed = new Set(bank.map((_, i) => i).filter(i => activeModule === "all" || String(bank[i].moduleId) === String(activeModule)));
    filteredIds = q.filteredIds.filter(i => allowed.has(i));
    if (!filteredIds.length) applyFilter(false);
  }}
  if (typeof q.index === "number" && filteredIds.length) {{
    index = Math.max(0, Math.min(filteredIds.length - 1, q.index));
  }}
  el("totalQ").textContent = filteredIds.length;
  renderFilters();
  renderStats();
  renderQuestion();
  updateScore();
  restoring = false;
}}

function applyFilter(preserveShuffle=false) {{
  const base = bank.map((q, i) => ({{q, i}})).filter(x => activeModule === "all" || String(x.q.moduleId) === String(activeModule)).map(x => x.i);
  filteredIds = preserveShuffle ? order.filter(i => base.includes(i)) : base;
  if (!preserveShuffle) order = bank.map((_, i) => i);
  index = 0;
  el("totalQ").textContent = filteredIds.length;
  renderFilters();
  renderStats();
  renderQuestion();
  updateScore();
  persistQuiz();
}}

function renderFilters() {{
  const box = el("moduleFilters");
  const mods = [{{id:"all", title:"All modules"}}, ...DATA.modules.map(m => ({{id:String(m.id), title:"Module "+m.id}}))];
  box.innerHTML = mods.map(m => `<button type="button" class="chip ${{String(activeModule)===String(m.id)?"active":""}}" data-m="${{m.id}}">${{m.title}}</button>`).join("");
  box.querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    activeModule = btn.dataset.m;
    applyFilter(false);
  }}));
}}

function renderStats() {{
  const box = el("moduleStats");
  box.innerHTML = DATA.modules.map(m => {{
    const qs = bank.filter(q => q.moduleId === m.id);
    const attempted = qs.filter(q => state[q.id] !== undefined).length;
    const correct = qs.filter(q => state[q.id] === q.answer).length;
    const pct = qs.length ? Math.round((attempted / qs.length) * 100) : 0;
    return `<div class="stat"><b>${{correct}}/${{qs.length}}</b><span>Module ${{m.id}} · ${{attempted}} answered</span><div class="prog-line"><i style="width:${{pct}}%"></i></div></div>`;
  }}).join("");
}}

function updateScore() {{
  const list = currentList();
  const attempted = list.filter(q => state[q.id] !== undefined).length;
  const correct = list.filter(q => state[q.id] === q.answer).length;
  el("attempted").textContent = attempted;
  el("scoreNow").textContent = correct;
  el("accuracy").textContent = attempted ? Math.round((correct / attempted) * 100) + "%" : "—";
  quizProgressBar.style.width = list.length ? ((attempted / list.length) * 100) + "%" : "0%";
  renderStats();
}}

function renderQuestion() {{
  const list = currentList();
  if (!list.length) {{
    el("qtext").textContent = "No questions in this filter.";
    el("options").innerHTML = "";
    el("explain").classList.remove("show");
    el("qnum").textContent = "";
    return;
  }}
  const q = list[index];
  el("qnum").textContent = `Question ${{index+1}} of ${{list.length}}`;
  el("qtopic").textContent = `M${{q.moduleId}} · ${{q.topicId}} · ${{q.topicTitle}}`;
  el("qtext").textContent = q.q;
  const chosen = state[q.id];
  const letters = ["A","B","C","D"];
  el("options").innerHTML = q.options.map((opt, i) => {{
    let cls = "opt";
    if (chosen !== undefined) {{
      if (i === q.answer) cls += " correct";
      else if (i === chosen) cls += " wrong";
    }}
    return `<button type="button" class="${{cls}}" data-i="${{i}}" ${{chosen!==undefined?"disabled":""}}><span class="letter">${{letters[i]}}</span><span>${{opt.replace(/^[A-D]\\.\\s*/, "")}}</span></button>`;
  }}).join("");
  el("options").querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    state[q.id] = Number(btn.dataset.i);
    renderQuestion();
    updateScore();
    persistQuiz();
  }}));
  const explain = el("explain");
  if (chosen !== undefined) {{
    const ok = chosen === q.answer;
    explain.textContent = (ok ? "Correct. " : "Not quite. ") + (q.explain || "");
    explain.classList.add("show");
  }} else {{
    explain.classList.remove("show");
    explain.textContent = "";
  }}
}}

el("nextBtn").addEventListener("click", () => {{
  const list = currentList();
  if (!list.length) return;
  index = (index + 1) % list.length;
  renderQuestion();
  persistQuiz();
}});
el("prevBtn").addEventListener("click", () => {{
  const list = currentList();
  if (!list.length) return;
  index = (index - 1 + list.length) % list.length;
  renderQuestion();
  persistQuiz();
}});
el("resetBtn").addEventListener("click", () => {{
  Object.keys(state).forEach(k => delete state[k]);
  updateScore();
  renderQuestion();
  persistQuiz();
}});
el("shuffleBtn").addEventListener("click", () => {{
  const base = bank.map((q, i) => i).filter(i => activeModule === "all" || String(bank[i].moduleId) === String(activeModule));
  filteredIds = shuffle(base);
  order = shuffle(bank.map((_, i) => i));
  index = 0;
  renderQuestion();
  persistQuiz();
}});

document.addEventListener("keydown", e => {{
  if (e.key === "ArrowRight") el("nextBtn").click();
  if (e.key === "ArrowLeft") el("prevBtn").click();
  const map = {{"1":0,"2":1,"3":2,"4":3,"a":0,"b":1,"c":2,"d":3}};
  if (map[e.key.toLowerCase()] !== undefined) {{
    const btn = el("options").querySelector(`[data-i="${{map[e.key.toLowerCase()]}}"]`);
    if (btn && !btn.disabled) btn.click();
  }}
}});

applyFilter(false);
{SYNC_BOOT}
bootSync(restoreQuiz);
</script>
</body>
</html>
"""


def enrich_maps_payload() -> dict:
    """Merge map layout with flashcard text + MCQs from study facts."""
    topics_by_id: dict[str, dict] = {}
    mcqs_by_module: dict[int, list] = {}
    for m in DATA["modules"]:
        mid = int(m["id"])
        mcqs_by_module[mid] = []
        for t in m["topics"]:
            topics_by_id[str(t["id"])] = t
            for q in t.get("mcqs") or []:
                mcqs_by_module[mid].append(
                    {
                        "q": q["q"],
                        "options": q["options"],
                        "answer": q["answer"],
                        "explain": q.get("explain") or "",
                        "topicId": t["id"],
                        "topicTitle": t["title"],
                    }
                )

    modules_out = []
    for mod in MAPS["modules"]:
        mid = int(mod["id"])
        nodes: dict[str, dict] = {}
        root = dict(mod["root"])
        nodes[root["id"]] = {
            "kind": root.get("kind", "root"),
            "title": root["title"],
            "path": root.get("path", ""),
            "body": root.get("body", ""),
            "points": root.get("points") or [],
        }
        levels_out = []
        for level in mod["levels"]:
            level_nodes = []
            for n in level["nodes"]:
                nid = n["id"]
                topic = topics_by_id.get(str(n.get("topicId") or nid))
                body = ""
                points: list[str] = []
                if topic:
                    cards = topic.get("flashcards") or []
                    if cards:
                        body = cards[0].get("back") or ""
                        if cards[0].get("detail"):
                            points.append(cards[0]["detail"])
                        for extra in cards[1:]:
                            points.append(f"{extra.get('front', '')}: {extra.get('back', '')}")
                    path = f"Module {mid} · {topic.get('id')} · {topic.get('title')}"
                    title = n.get("title") or topic.get("title")
                    q_count = len(topic.get("mcqs") or [])
                    fc_count = len(cards)
                else:
                    path = n.get("path") or f"Module {mid}"
                    title = n["title"]
                    q_count = 0
                    fc_count = 0
                if n.get("note"):
                    points.insert(0, "Map note: " + n["note"])
                nodes[nid] = {
                    "kind": n.get("kind", "a"),
                    "title": title,
                    "path": path,
                    "body": body or n.get("body") or "Open flashcards for this topic for full notes.",
                    "points": points,
                    "topicId": str(n.get("topicId") or nid),
                    "lmr": bool(n.get("lmr")),
                    "note": n.get("note") or "",
                    "qCount": q_count,
                    "fcCount": fc_count,
                }
                level_nodes.append(
                    {
                        "id": nid,
                        "title": n["title"],
                        "sub": n.get("sub") or "",
                        "kind": n.get("kind", "a"),
                        "topicId": str(n.get("topicId") or nid),
                        "lmr": bool(n.get("lmr")),
                    }
                )
            levels_out.append({"heading": level["heading"], "nodes": level_nodes})
        modules_out.append(
            {
                "id": mid,
                "title": mod["title"],
                "weight": mod.get("weight") or "standard",
                "rootId": root["id"],
                "levels": levels_out,
                "nodes": nodes,
                "questions": mcqs_by_module.get(mid, []),
            }
        )
    return {"modules": modules_out}


MAP_CSS = SHARED_CSS + r"""
.progress {
  height: 8px; border-radius: 999px; background: rgba(21,35,28,0.08); overflow: hidden;
}
.progress > span {
  display: block; height: 100%; width: 0%;
  background: linear-gradient(90deg, var(--accent), #2f9e74);
  transition: width 0.25s ease;
}
.layout {
  display: grid;
  grid-template-columns: 1.35fr .9fr;
  gap: 1rem;
  align-items: start;
  margin-top: 1rem;
}
@media (max-width: 920px) {
  .layout { grid-template-columns: 1fr; }
  .detail-panel { position: static !important; }
}
.flow-panel, .detail-panel, .quiz-panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: calc(var(--radius) + 4px);
  box-shadow: var(--shadow);
  padding: 1rem;
}
.detail-panel { position: sticky; top: 1rem; min-height: 280px; }
.section-label {
  font-size: .78rem; font-weight: 700; letter-spacing: .05em;
  text-transform: uppercase; color: var(--muted); margin: 0 0 .7rem;
}
.tree { display: grid; gap: .85rem; }
.level { display: grid; gap: .55rem; justify-items: center; }
.connectors {
  display: flex; justify-content: center; height: 18px; position: relative;
}
.connectors::before {
  content: "";
  position: absolute; top: 0; bottom: 50%;
  width: 2px; background: rgba(15,107,76,.35);
}
.row {
  display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; width: 100%;
}
.node {
  appearance: none; border: 1px solid var(--line); background: #fff;
  border-radius: 14px; padding: .7rem .85rem; min-width: 118px; max-width: 190px;
  text-align: left; cursor: pointer; font: inherit; color: inherit;
  box-shadow: 0 6px 16px rgba(21,35,28,.06);
  transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
}
.node:hover { transform: translateY(-2px); border-color: rgba(15,107,76,.35); }
.node.active {
  border-color: transparent;
  box-shadow: 0 10px 24px rgba(15,107,76,.22);
  outline: 2px solid rgba(15,107,76,.55);
}
.node .n-title {
  display: block; font-family: var(--font-display);
  font-size: .98rem; line-height: 1.2; margin-bottom: .15rem;
}
.node .n-sub { display: block; color: var(--muted); font-size: .78rem; line-height: 1.3; }
.node .n-badge {
  display: inline-block; margin-top: .35rem; font-size: .68rem; font-weight: 800;
  letter-spacing: .04em; text-transform: uppercase; padding: .15rem .4rem;
  border-radius: 999px; background: #f3dfd0; color: var(--warn);
}
.node.root {
  background: linear-gradient(145deg, #116b54, #0d4f3e);
  color: #fff; min-width: 220px; max-width: 300px; text-align: center;
}
.node.root .n-sub { color: rgba(255,255,255,.82); }
.node.root .n-badge { background: rgba(255,255,255,.2); color: #fff; }
.node.a { background: #d8efe4; border-color: rgba(15,107,76,.2); }
.node.b { background: #ebe4f5; border-color: rgba(90,70,140,.22); }
.node.c { background: #dceaf7; border-color: rgba(31,79,120,.2); }
.node.lmr-node {
  box-shadow: 0 0 0 2px rgba(196,92,38,.5);
  background: #f3dfd0;
  border-color: rgba(196,92,38,.42);
}
.chip.weight-high { border-color: rgba(196,92,38,.55); }
.chip.weight-high.active { background: var(--accent-2); }
.criteria-box {
  margin: 0.7rem 0 0;
  padding: 0.75rem 0.9rem;
  border-radius: 12px;
  background: rgba(255,255,255,0.7);
  border: 1px dashed var(--line);
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.45;
}
.criteria-box strong { color: var(--ink); }
.filter-row { display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center; margin-top:0.65rem; }
.qcard.dimmed { opacity: 0.38; }
.branch-block {
  width: 100%; border: 1px dashed rgba(21,35,28,.16);
  border-radius: 16px; padding: .75rem; background: rgba(255,255,255,.45);
}
.branch-block h3 {
  margin: 0 0 .55rem; font-family: var(--font-display);
  font-size: 1.05rem; text-align: center;
}
.legend {
  display: flex; flex-wrap: wrap; gap: .55rem; margin: .2rem 0 .8rem; justify-content: center;
}
.legend span {
  display: inline-flex; align-items: center; gap: .35rem;
  font-size: .82rem; color: var(--muted); font-weight: 600;
}
.swatch { width: .75rem; height: .75rem; border-radius: 3px; display: inline-block; }
.detail-empty { color: var(--muted); margin: 1.2rem 0 0; }
.detail-kicker {
  display: inline-flex; font-size: .75rem; font-weight: 700; letter-spacing: .04em;
  text-transform: uppercase; padding: .25rem .55rem; border-radius: 999px;
  margin-bottom: .55rem; background: var(--accent-soft); color: var(--accent);
}
.detail-title {
  font-family: var(--font-display);
  font-size: clamp(1.35rem, 2.4vw, 1.7rem);
  margin: 0 0 .55rem; line-height: 1.2;
}
.detail-body { color: var(--ink); line-height: 1.55; margin: 0 0 .7rem; }
.detail-points { margin: 0; padding-left: 1.1rem; color: var(--muted); }
.detail-points li { margin: .35rem 0; }
.parent-path { font-size: .88rem; color: var(--muted); margin: 0 0 .7rem; }
.quiz-panel { margin-top: 1rem; }
.quiz-panel h2 { font-family: var(--font-display); margin: 0 0 .35rem; font-size: 1.45rem; }
.qlist { display: grid; gap: .7rem; margin-top: .8rem; }
.qcard {
  border: 1px solid var(--line); border-radius: 14px; padding: .85rem .9rem; background: #fff;
}
.qcard h3 {
  font-family: var(--font-display); font-size: 1.05rem; margin: 0 0 .55rem; line-height: 1.3;
}
.qmeta { color: var(--muted); font-size: .82rem; font-weight: 600; margin: 0 0 .45rem; }
.opts { display: grid; gap: .4rem; }
.opt {
  appearance: none; width: 100%; text-align: left; font: inherit;
  border: 1px solid var(--line); background: #fbfcfb; border-radius: 10px;
  padding: .55rem .7rem; cursor: pointer;
}
.opt:hover:not(:disabled) { border-color: rgba(15,107,76,.35); }
.opt.correct { background: #e7f6ee; border-color: rgba(15,107,76,.45); }
.opt.wrong { background: #fdeeee; border-color: rgba(163,59,59,.4); }
.explain {
  display: none; margin-top: .55rem; color: var(--muted);
  font-size: .92rem; background: #f3f7f4; border-radius: 10px; padding: .55rem .7rem;
}
.explain.show { display: block; }
.hint-bar { text-align: center; color: var(--muted); font-size: .9rem; margin: 0 0 .7rem; }
"""


def build_module_map() -> str:
    payload = enrich_maps_payload()
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>BS605 Module Map — Structure &amp; Important Questions</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
<style>{MAP_CSS}</style>
{SYNC_HEAD}
</head>
<body>
<div class="wrap">
  {site_nav("map")}
  <header class="hero">
    <div class="kicker">Amity · BS605 · Module Map</div>
    <h1>Structure maps &amp; important questions</h1>
    <p class="lede">Switch modules below. Click any card in the flow for definitions and exam tips — questions below filter to that topic. Orange <strong>LMR</strong> badges mark last-minute revision priorities.</p>
    <div class="navrow">
      <a class="btn" href="#questions">Important questions</a>
    </div>
  </header>

  <section class="panel">
    <div class="meta" style="margin-bottom:0.6rem">
      <span>This module: <strong id="mapModAttempted">0</strong> / <strong id="mapModTotal">0</strong> answered</span>
      <span>Correct <strong id="mapModCorrect">0</strong></span>
      <span>All modules: <strong id="mapAllAttempted">0</strong> / <strong id="mapAllTotal">0</strong></span>
    </div>
    <div class="progress" style="margin-bottom:0.85rem"><span id="mapProgressBar"></span></div>
    <div class="summary-grid" id="mapStats"></div>
    <div class="filters" id="moduleFilters"></div>
    <div class="criteria-box">
      <strong>How this map is built:</strong>
      One card ≈ one study topic from the SLM outline (some SLM sections are merged when they share one exam idea).
      Grouped left→right / top→bottom by theme. Colours = topic groups.
      <strong>Exam weight:</strong> Module 2 is marked high (faculty). Orange outline = LMR priority.
    </div>
    {SYNC_PANEL}
  </section>

  <div class="layout">
    <section class="flow-panel" aria-label="Structure flow diagram">
      <p class="section-label" id="flowLabel">Interactive flow</p>
      <p class="hint-bar">Tap a card → details open on the right (below on mobile)</p>
      <div class="legend">
        <span><i class="swatch" style="background:#116b54"></i> Module root</span>
        <span><i class="swatch" style="background:#d8efe4"></i> Group A</span>
        <span><i class="swatch" style="background:#f7e4d5"></i> Group B</span>
        <span><i class="swatch" style="background:#dceaf7"></i> Group C</span>
        <span><i class="swatch" style="background:#f3dfd0;outline:2px solid rgba(196,92,38,.45)"></i> LMR priority</span>
      </div>
      <div class="tree" id="tree"></div>
    </section>
    <aside class="detail-panel" id="detailPanel">
      <p class="section-label">Selected term</p>
      <div id="detailContent">
        <p class="detail-empty">Click any card in the flow to see definition, place in the structure, and exam tips.</p>
      </div>
    </aside>
  </div>

  <section class="quiz-panel" id="questions">
    <h2 id="questionsTitle">Important questions</h2>
    <p class="lede" style="margin:0">Practice after you walk the map. Tap a map card to focus questions on that topic.</p>
    <div class="filter-row">
      <button type="button" class="btn primary" id="showAllQs">Show all module questions</button>
      <span class="meta" style="margin:0" id="qFilterLabel">Showing all</span>
    </div>
    <div class="qlist" id="qlist"></div>
  </section>
</div>
<script>
const MAPS = {data_json};
let activeModuleId = String(MAPS.modules[0].id);
let current = MAPS.modules[0];
/** mapAnswers: {{ [moduleId]: {{ [questionIndex]: selectedOption }} }} */
let mapAnswers = {{}};
let restoring = false;
let topicFilter = null; // topicId string or null
let selectedNodeId = null;

const el = id => document.getElementById(id);
const mapProgressBar = el("mapProgressBar");
const mapAllTotal = MAPS.modules.reduce((n, m) => n + (m.questions || []).length, 0);
el("mapAllTotal").textContent = mapAllTotal;

function currentModule() {{
  return MAPS.modules.find(m => String(m.id) === String(activeModuleId)) || MAPS.modules[0];
}}

function weightLabel(w) {{
  if (w === "high") return " · exam focus";
  if (w === "foundation") return " · foundation";
  return "";
}}

function updateMapStats() {{
  current = currentModule();
  const list = current.questions || [];
  const mid = String(current.id);
  const answers = mapAnswers[mid] || {{}};
  let attempted = 0, correct = 0;
  list.forEach((item, qi) => {{
    if (answers[qi] === undefined || answers[qi] === null) return;
    attempted += 1;
    if (Number(answers[qi]) === item.answer) correct += 1;
  }});
  el("mapModAttempted").textContent = attempted;
  el("mapModTotal").textContent = list.length;
  el("mapModCorrect").textContent = correct;
  mapProgressBar.style.width = list.length ? ((attempted / list.length) * 100) + "%" : "0%";

  let allA = 0;
  MAPS.modules.forEach(m => {{
    const ans = mapAnswers[String(m.id)] || {{}};
    (m.questions || []).forEach((item, qi) => {{
      if (ans[qi] === undefined || ans[qi] === null) return;
      allA += 1;
    }});
  }});
  el("mapAllAttempted").textContent = allA;

  el("mapStats").innerHTML = MAPS.modules.map(m => {{
    const qs = m.questions || [];
    const ans = mapAnswers[String(m.id)] || {{}};
    let a = 0, c = 0;
    qs.forEach((item, qi) => {{
      if (ans[qi] === undefined || ans[qi] === null) return;
      a += 1;
      if (Number(ans[qi]) === item.answer) c += 1;
    }});
    const pct = qs.length ? Math.round((a / qs.length) * 100) : 0;
    const w = m.weight === "high" ? " · high weight" : "";
    return `<div class="stat"><b>${{c}}/${{qs.length}}</b><span>Module ${{m.id}}${{w}} · ${{a}} answered</span><div class="prog-line"><i style="width:${{pct}}%"></i></div></div>`;
  }}).join("");
}}

function persistMap() {{
  if (restoring || !window.BS605Progress || !window.__BS605_SYNC_READY) return;
  BS605Progress.saveProgress({{
    mapAnswers: mapAnswers,
    mapMeta: {{ activeModuleId: String(activeModuleId), topicFilter: topicFilter, selectedNodeId: selectedNodeId }}
  }});
}}

function restoreMap(payload) {{
  if (!payload) return;
  restoring = true;
  if (payload.mapAnswers && typeof payload.mapAnswers === "object") mapAnswers = payload.mapAnswers;
  if (payload.mapMeta && payload.mapMeta.activeModuleId) activeModuleId = String(payload.mapMeta.activeModuleId);
  if (payload.mapMeta) {{
    topicFilter = payload.mapMeta.topicFilter || null;
    selectedNodeId = payload.mapMeta.selectedNodeId || null;
  }}
  renderAll();
  restoring = false;
}}

function renderFilters() {{
  const box = el("moduleFilters");
  box.innerHTML = MAPS.modules.map(m => {{
    const wClass = m.weight === "high" ? " weight-high" : "";
    return `<button type="button" class="chip${{wClass}} ${{String(activeModuleId)===String(m.id)?"active":""}}" data-m="${{m.id}}">M${{m.id}}: ${{m.title}}${{weightLabel(m.weight)}}</button>`;
  }}).join("");
  box.querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    activeModuleId = btn.dataset.m;
    topicFilter = null;
    selectedNodeId = null;
    renderAll();
    persistMap();
  }}));
}}

function makeNode(id, title, sub, cls, lmr) {{
  const badge = lmr ? `<span class="n-badge">LMR</span>` : "";
  const lmrCls = lmr ? " lmr-node" : "";
  return `<button type="button" class="node ${{cls}}${{lmrCls}}" data-id="${{id}}"><span class="n-title">${{title}}</span><span class="n-sub">${{sub || ""}}</span>${{badge}}</button>`;
}}

function renderTree() {{
  current = currentModule();
  el("flowLabel").textContent = `Module ${{current.id}} · Interactive flow`;
  const parts = [];
  parts.push(`<div class="level">${{makeNode(current.rootId, current.nodes[current.rootId].title, current.nodes[current.rootId].path, "root", false)}}</div>`);
  current.levels.forEach(level => {{
    parts.push(`<div class="connectors"></div>`);
    const row = level.nodes.map(n => makeNode(n.id, n.title, n.sub, n.kind || "a", n.lmr)).join("");
    parts.push(`<div class="branch-block"><h3>${{level.heading}}</h3><div class="row">${{row}}</div></div>`);
  }});
  el("tree").innerHTML = parts.join("");
  el("tree").querySelectorAll(".node").forEach(btn => {{
    btn.addEventListener("click", () => showNode(btn.dataset.id));
  }});
  showNode(selectedNodeId && current.nodes[selectedNodeId] ? selectedNodeId : current.rootId);
}}

function showNode(id) {{
  const n = current.nodes[id];
  if (!n) return;
  selectedNodeId = id;
  document.querySelectorAll(".node").forEach(node => node.classList.toggle("active", node.dataset.id === id));
  const points = (n.points || []).map(p => `<li>${{p}}</li>`).join("");
  const lmrLine = n.lmr ? `<span class="detail-kicker" style="background:#f8e5d8;color:var(--warn)">LMR priority</span>` : "";
  const counts = n.kind === "root" ? "" : `<p class="parent-path">${{n.fcCount || 0}} flashcards · ${{n.qCount || 0}} MCQs in bank</p>`;
  el("detailContent").innerHTML = `
    ${{lmrLine}}
    <div class="detail-kicker">${{n.kind === "root" ? "Module" : "Topic"}}</div>
    <h2 class="detail-title">${{n.title}}</h2>
    <p class="parent-path">${{n.path || ""}}</p>
    ${{counts}}
    <p class="detail-body">${{n.body || ""}}</p>
    ${{points ? `<ul class="detail-points">${{points}}</ul>` : ""}}
    ${{n.kind !== "root" ? `<div class="navrow" style="margin-top:0.8rem"><button type="button" class="btn primary" id="focusQsBtn">Practice this topic</button></div>` : ""}}
  `;
  const focusBtn = el("focusQsBtn");
  if (focusBtn) {{
    focusBtn.addEventListener("click", () => {{
      topicFilter = n.topicId || id;
      renderQuestions();
      persistMap();
      el("questions").scrollIntoView({{ behavior: "smooth", block: "start" }});
    }});
  }}
  if (n.kind !== "root") {{
    topicFilter = n.topicId || id;
    renderQuestions();
  }} else {{
    topicFilter = null;
    renderQuestions();
  }}
  if (window.matchMedia("(max-width: 920px)").matches) {{
    el("detailPanel").scrollIntoView({{ behavior: "smooth", block: "nearest" }});
  }}
  if (!restoring) persistMap();
}}

function applySavedAnswer(qi) {{
  const mid = String(current.id);
  const saved = mapAnswers[mid] && mapAnswers[mid][qi];
  if (saved === undefined || saved === null) return;
  const item = current.questions[qi];
  const card = document.getElementById("q" + qi);
  if (!item || !card) return;
  const i = Number(saved);
  card.querySelectorAll(".opt").forEach((o, idx) => {{
    o.disabled = true;
    if (idx === item.answer) o.classList.add("correct");
    if (idx === i && i !== item.answer) o.classList.add("wrong");
  }});
  const ex = document.getElementById("ex" + qi);
  ex.textContent = (i === item.answer ? "Correct. " : "Not quite. ") + (item.explain || "");
  ex.classList.add("show");
}}

function renderQuestions() {{
  el("questionsTitle").textContent = `Important questions — Module ${{current.id}}`;
  const letters = ["A","B","C","D"];
  const list = current.questions || [];
  const filtered = topicFilter
    ? list.map((item, qi) => ({{item, qi}})).filter(x => String(x.item.topicId) === String(topicFilter))
    : list.map((item, qi) => ({{item, qi}}));
  el("qFilterLabel").textContent = topicFilter
    ? `Focused on topic ${{topicFilter}} (${{filtered.length}} of ${{list.length}})`
    : `Showing all ${{list.length}} questions`;
  el("qlist").innerHTML = filtered.map(({{item, qi}}) => {{
    const opts = item.options.map((o, i) =>
      `<button type="button" class="opt" data-q="${{qi}}" data-i="${{i}}"><strong>${{letters[i]}}.</strong> ${{o}}</button>`
    ).join("");
    return `<article class="qcard" id="q${{qi}}"><p class="qmeta">${{item.topicId}} · ${{item.topicTitle}}</p><h3>${{qi+1}}. ${{item.q}}</h3><div class="opts">${{opts}}</div><div class="explain" id="ex${{qi}}"></div></article>`;
  }}).join("") || `<p class="detail-empty">No MCQs for this filter.</p>`;
  filtered.forEach(({{qi}}) => applySavedAnswer(qi));
  updateMapStats();
}}

el("showAllQs").addEventListener("click", () => {{
  topicFilter = null;
  selectedNodeId = current.rootId;
  renderTree();
  persistMap();
}});

el("qlist").addEventListener("click", e => {{
  const btn = e.target.closest(".opt");
  if (!btn || btn.disabled) return;
  const qi = Number(btn.dataset.q);
  const i = Number(btn.dataset.i);
  const item = current.questions[qi];
  const card = document.getElementById("q" + qi);
  card.querySelectorAll(".opt").forEach((o, idx) => {{
    o.disabled = true;
    if (idx === item.answer) o.classList.add("correct");
    if (idx === i && i !== item.answer) o.classList.add("wrong");
  }});
  const ex = document.getElementById("ex" + qi);
  ex.textContent = (i === item.answer ? "Correct. " : "Not quite. ") + (item.explain || "");
  ex.classList.add("show");
  const mid = String(current.id);
  if (!mapAnswers[mid]) mapAnswers[mid] = {{}};
  mapAnswers[mid][qi] = i;
  updateMapStats();
  persistMap();
}});

function renderAll() {{
  renderFilters();
  renderTree();
}}

renderAll();
{SYNC_BOOT}
bootSync(restoreMap);
</script>
</body>
</html>
"""


def main() -> None:
    totals = count_totals()
    totals_json = json.dumps(
        {
            "flashTotal": totals["flashTotal"],
            "quizTotal": totals["quizTotal"],
            "mapTotal": totals["mapTotal"],
            "quizAnswerKey": totals["quizAnswerKey"],
            "mapAnswerKey": totals["mapAnswerKey"],
        },
        ensure_ascii=False,
    )
    flash = ROOT / "flashcards.html"
    quiz = ROOT / "quiz.html"
    mmap = ROOT / "module-map.html"
    flash.write_text(build_flashcards(), encoding="utf-8")
    quiz.write_text(build_quiz(), encoding="utf-8")
    mmap.write_text(build_module_map(), encoding="utf-8")
    index = ROOT / "index.html"
    index.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>BS605 Study Pack</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,650&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
<style>{SHARED_CSS}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; margin-top:1.2rem; }}
.cards a {{
  display:block; text-decoration:none; color:inherit; padding:1.3rem; border-radius:var(--radius);
  border:1px solid var(--line); background:var(--panel); box-shadow:var(--shadow);
  transition: transform .15s ease;
}}
.cards a:hover {{ transform: translateY(-3px); }}
.cards h2 {{ font-family:var(--font-display); margin:0 0 .4rem; font-size:1.45rem; }}
.cards p {{ margin:0; color:var(--muted); }}
.cards .tool-prog {{ margin-top:0.75rem; font-size:0.92rem; color:var(--ink); font-weight:600; }}
</style>
{SYNC_HEAD}
</head>
<body>
<div class="wrap">
  {site_nav("home")}
  <header class="hero">
    <div class="kicker">Amity University Online · BS605</div>
    <h1>Cognitive Analytics &amp; Social Skills study pack</h1>
    <p class="lede">Home for every study tool. Connect a sync code once — progress auto-saves across phone and PC.</p>
  </header>

  <section class="panel" style="margin-bottom:1rem">
    <strong>Your progress</strong>
    <p class="lede" style="margin:0.35rem 0 0.7rem;font-size:0.95rem">Live totals from this device (and cloud when connected).</p>
    <div class="summary-grid" id="homeStats">
      <div class="stat"><b id="homeFlash">0/{totals["flashTotal"]}</b><span>Flashcards seen</span><div class="prog-line"><i id="homeFlashBar"></i></div></div>
      <div class="stat"><b id="homeKnown">0</b><span>Flashcards marked known</span></div>
      <div class="stat"><b id="homeQuiz">0/{totals["quizTotal"]}</b><span>Quiz answered · <span id="homeQuizCorrect">0</span> correct</span><div class="prog-line"><i id="homeQuizBar"></i></div></div>
      <div class="stat"><b id="homeMap">0/{totals["mapTotal"]}</b><span>Module-map answered · <span id="homeMapCorrect">0</span> correct</span><div class="prog-line"><i id="homeMapBar"></i></div></div>
    </div>
    {SYNC_PANEL}
  </section>

  <section class="panel">
    <strong>All pages</strong>
    <div class="cards" style="margin-top:0.9rem">
      <a href="module-map.html"><h2>Module Map</h2><p>Structure maps + important questions for Modules 1–5.</p><div class="tool-prog" id="cardMapProg">Not started</div></a>
      <a href="flashcards.html"><h2>Flashcards</h2><p>{totals["flashTotal"]} revision cards with LMR priority list.</p><div class="tool-prog" id="cardFlashProg">Not started</div></a>
      <a href="quiz.html"><h2>Objective quiz</h2><p>{totals["quizTotal"]} MCQs with explanations, filter by module.</p><div class="tool-prog" id="cardQuizProg">Not started</div></a>
      <a href="{PDF_NAME}" target="_blank"><h2>Study PDF</h2><p>Full SLM (opens in a new tab).</p></a>
      <a href="Live Class 2 Transcript.txt" target="_blank"><h2>Live Class 2</h2><p>Transcript — Attitudes, Emotions &amp; Inner Power.</p></a>
      <a href="Live Class 3 Transcript.txt" target="_blank"><h2>Live Class 3</h2><p>Transcript — faculty session notes.</p></a>
    </div>
  </section>
</div>
<script>
const TOTALS = {totals_json};
function paintHome(payload) {{
  if (!window.BS605Progress) return;
  const s = BS605Progress.summarize(payload || {{}}, TOTALS);
  const f = s.flashcards, q = s.quiz, m = s.map;
  document.getElementById("homeFlash").textContent = f.seen + "/" + f.total;
  document.getElementById("homeKnown").textContent = String(f.known);
  document.getElementById("homeQuiz").textContent = q.attempted + "/" + q.total;
  document.getElementById("homeQuizCorrect").textContent = String(q.correct);
  document.getElementById("homeMap").textContent = m.attempted + "/" + m.total;
  document.getElementById("homeMapCorrect").textContent = String(m.correct);
  document.getElementById("homeFlashBar").style.width = (f.total ? (f.seen/f.total)*100 : 0) + "%";
  document.getElementById("homeQuizBar").style.width = (q.total ? (q.attempted/q.total)*100 : 0) + "%";
  document.getElementById("homeMapBar").style.width = (m.total ? (m.attempted/m.total)*100 : 0) + "%";
  document.getElementById("cardFlashProg").textContent = f.seen
    ? (f.seen + " seen · " + f.known + " known")
    : "Not started";
  document.getElementById("cardQuizProg").textContent = q.attempted
    ? (q.attempted + " answered · " + q.correct + " correct")
    : "Not started";
  document.getElementById("cardMapProg").textContent = m.attempted
    ? (m.attempted + " answered · " + m.correct + " correct")
    : "Not started";
}}
{SYNC_BOOT}
bootSync(paintHome);
</script>
</body>
</html>
"""
,
        encoding="utf-8",
    )
    print(f"Wrote {flash.name}, {mmap.name}, {quiz.name}, {index.name}")
    print(f"Totals: flash={totals['flashTotal']} quiz={totals['quizTotal']} map={totals['mapTotal']}")


if __name__ == "__main__":
    main()
