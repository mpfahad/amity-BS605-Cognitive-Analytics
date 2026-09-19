#!/usr/bin/env python3
"""Build flashcards.html and quiz.html from _study_facts.json"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "_study_facts.json").read_text(encoding="utf-8"))
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
.meta {
  display: flex; flex-wrap: wrap; gap: 0.75rem 1.2rem;
  color: var(--muted); font-size: 0.95rem; margin-bottom: 1rem;
}
.meta strong { color: var(--ink); }
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
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.6rem;
  margin-top: 0.8rem;
}
.stat {
  background: rgba(255,255,255,0.75);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.8rem;
}
.stat b { display: block; font-size: 1.4rem; font-family: var(--font-display); }
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
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Amity · BS605</div>
    <h1>Cognitive Analytics &amp; Social Skills flashcards</h1>
    <p class="lede">Quick-reference cards drilled from the SLM and live-class transcripts across all five modules. Flip a card, then move topic by topic — LMR priorities are marked for exam focus.</p>
    <div class="navrow">
      <a class="btn primary" href="quiz.html">Open objective quiz</a>
      <a class="btn" href="#lmr">LMR priorities</a>
      <a class="btn ghost" href="{PDF_NAME}" target="_blank">Open PDF</a>
    </div>
  </header>

  <section class="panel">
    <div class="meta">
      <span><strong id="countCards">0</strong> cards</span>
      <span><strong>5</strong> modules</span>
      <span>Source: SLM + live class links</span>
    </div>
    <div class="filters" id="moduleFilters"></div>
    {links_html()}
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
          <div class="hint">Click again to hide the answer</div>
        </div>
      </button>
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

const el = id => document.getElementById(id);
const card = el("card");
const progressBar = el("progressBar");

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

function applyFilter() {{
  filtered = activeModule === "all" ? deck.slice() : deck.filter(c => String(c.moduleId) === String(activeModule));
  index = 0;
  flipped = false;
  el("countCards").textContent = filtered.length;
  renderTopics();
  renderCard();
}}

function renderTopics() {{
  const topics = [];
  const seen = new Set();
  filtered.forEach(c => {{
    const k = c.topicId;
    if (!seen.has(k)) {{ seen.add(k); topics.push(c); }}
  }});
  el("topicList").innerHTML = topics.map(t => {{
    const active = filtered[index] && filtered[index].topicId === t.topicId ? "active" : "";
    return `<button type="button" class="${{active}}" data-topic="${{t.topicId}}"><strong>${{t.topicId}} · ${{t.topicTitle}}</strong><span>Module ${{t.moduleId}}</span></button>`;
  }}).join("");
  el("topicList").querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    const i = filtered.findIndex(c => c.topicId === btn.dataset.topic);
    if (i >= 0) {{ index = i; flipped = false; renderCard(); renderTopics(); }}
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
  el("backTag").textContent = c.topicTitle;
  el("frontText").textContent = c.front;
  el("backText").textContent = c.back;
  el("backDetail").textContent = c.detail || "";
  el("backDetail").style.display = c.detail ? "block" : "none";
  el("topicLabel").textContent = c.topicTitle;
  el("position").textContent = `${{index+1}} / ${{filtered.length}}`;
  progressBar.style.width = `${{((index+1)/filtered.length)*100}}%`;
  card.classList.toggle("flipped", flipped);
  card.setAttribute("aria-label", flipped ? "Hide answer" : "Reveal answer");
  el("flipBtn").textContent = flipped ? "Hide answer" : "Reveal answer";
}}

function flip() {{
  flipped = !flipped;
  card.classList.toggle("flipped", flipped);
  card.setAttribute("aria-label", flipped ? "Hide answer" : "Reveal answer");
  el("flipBtn").textContent = flipped ? "Hide answer" : "Reveal answer";
}}
function next() {{ if (!filtered.length) return; index = (index + 1) % filtered.length; flipped = false; renderCard(); renderTopics(); }}
function prev() {{ if (!filtered.length) return; index = (index - 1 + filtered.length) % filtered.length; flipped = false; renderCard(); renderTopics(); }}

card.addEventListener("click", (e) => {{ e.preventDefault(); flip(); }});
el("flipBtn").addEventListener("click", (e) => {{ e.preventDefault(); flip(); }});
el("nextBtn").addEventListener("click", next);
el("prevBtn").addEventListener("click", prev);
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
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Amity · BS605</div>
    <h1>Objective questions by module</h1>
    <p class="lede">MCQs drawn from the BS605 SLM and live-class emphasis. Filter by module, answer one by one, and use explanations to lock concepts — especially LMR priorities.</p>
    <div class="navrow">
      <a class="btn primary" href="flashcards.html">Open flashcards</a>
      <a class="btn" href="flashcards.html#lmr">LMR priorities</a>
    </div>
  </header>

  <section class="panel">
    <div class="scorebar">
      <div class="meta" style="margin:0">
        <span><strong id="totalQ">0</strong> questions</span>
        <span>Score <strong id="scoreNow">0</strong> / <strong id="attempted">0</strong></span>
      </div>
      <div class="navrow" style="margin:0">
        <button class="btn" id="resetBtn" type="button">Reset answers</button>
        <button class="btn primary" id="shuffleBtn" type="button">Shuffle</button>
      </div>
    </div>
    <div class="filters" id="moduleFilters" style="margin-top:0.9rem"></div>
    <div class="summary-grid" id="moduleStats"></div>
    {links_html()}
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

const el = id => document.getElementById(id);

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
    return `<div class="stat"><b>${{correct}}/${{qs.length}}</b>Module ${{m.id}} · attempted ${{attempted}}</div>`;
  }}).join("");
}}

function updateScore() {{
  const list = currentList();
  const attempted = list.filter(q => state[q.id] !== undefined).length;
  const correct = list.filter(q => state[q.id] === q.answer).length;
  el("attempted").textContent = attempted;
  el("scoreNow").textContent = correct;
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
}});
el("prevBtn").addEventListener("click", () => {{
  const list = currentList();
  if (!list.length) return;
  index = (index - 1 + list.length) % list.length;
  renderQuestion();
}});
el("resetBtn").addEventListener("click", () => {{
  Object.keys(state).forEach(k => delete state[k]);
  updateScore();
  renderQuestion();
}});
el("shuffleBtn").addEventListener("click", () => {{
  const base = bank.map((q, i) => i).filter(i => activeModule === "all" || String(bank[i].moduleId) === String(activeModule));
  filteredIds = shuffle(base);
  order = shuffle(bank.map((_, i) => i));
  index = 0;
  renderQuestion();
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
</script>
</body>
</html>
"""


def main() -> None:
    flash = ROOT / "flashcards.html"
    quiz = ROOT / "quiz.html"
    flash.write_text(build_flashcards(), encoding="utf-8")
    quiz.write_text(build_quiz(), encoding="utf-8")
    # also a tiny index
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
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Amity University Online · BS605</div>
    <h1>Cognitive Analytics &amp; Social Skills study pack</h1>
    <p class="lede">Built from your SLM PDF and Live Class 2–3 transcripts — flashcards for quick revision and module-wise objective questions for practice.</p>
  </header>
  <div class="cards">
    <a href="flashcards.html"><h2>Flashcards</h2><p>63 topic cards across 5 modules with LMR priority list.</p></a>
    <a href="quiz.html"><h2>Objective quiz</h2><p>60 MCQs with explanations, filterable by module.</p></a>
    <a href="{PDF_NAME}" target="_blank"><h2>Study PDF</h2><p>Original BS605 SLM.</p></a>
  </div>
  <section class="panel" style="margin-top:1.2rem">
    <strong>Materials &amp; transcripts</strong>
    {links_html()}
  </section>
</div>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Wrote {flash.name}, {quiz.name}, {index.name}")


if __name__ == "__main__":
    main()
