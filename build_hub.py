#!/usr/bin/env python3
"""Build Amity multi-subject GitHub Pages hub (root + subjects/*/ tools)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from build_study_pages import (
    FLASH_CSS as _FLASH_CSS,
    MAP_CSS as _MAP_CSS,
    QUIZ_CSS,
    SHARED_CSS,
    html_escape,
)

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / "shared"
SUBJECTS_DIR = ROOT / "subjects"

SUBJECTS: dict[str, dict] = {
    "bs605": {
        "code": "BS605",
        "title_short": "Cognitive Analytics & Social Skills",
        "kicker": "Cognitive Analytics and Social Skills for Professional",
        "pdf": "Congnitive Analytics and Social skill for Profession W F 1.pdf",
        "flash_lede": (
            "Quick-reference cards drilled from the SLM and live-class transcripts across all modules. "
            "Flip a card, then move topic by topic — LMR priorities are marked for exam focus."
        ),
        "quiz_lede": (
            "MCQs drawn from the BS605 SLM and live-class emphasis. Filter by module, answer one by one, "
            "and use explanations to lock concepts — especially LMR priorities."
        ),
        "map_lede": (
            "Switch modules below. Click any card in the flow for definitions and exam tips — questions below "
            "filter to that topic. Orange LMR badges mark last-minute revision priorities."
        ),
        "links": [
            ("Live Class 2 transcript", "Live Class 2 Transcript.txt"),
            ("Live Class 3 transcript", "Live Class 3 Transcript.txt"),
            ("Study PDF (SLM)", "Congnitive Analytics and Social skill for Profession W F 1.pdf"),
        ],
        "extra_cards": [
            ("Live Class 2", "Transcript — Attitudes, Emotions & Inner Power.", "Live Class 2 Transcript.txt"),
            ("Live Class 3", "Transcript — faculty session notes.", "Live Class 3 Transcript.txt"),
        ],
    },
    "cse601": {
        "code": "CSE601",
        "title_short": "Data Structures & Algorithms",
        "kicker": "Data Structures and Algorithm Design",
        "pdf": "Data Structure and Algorithm F.pdf",
        "flash_lede": "Revision cards from the CSE601 SLM and Live Class 1–2 focus — filter by module and track what you know.",
        "quiz_lede": "MCQs weighted to Live Class exam focus (Modules 1–2 + NP). Modules 3–4 deferred until those live classes.",
        "map_lede": "Orange LMR badges follow teacher exam weightage from Live Class 1–2. Click cards for notes; practice MCQs below.",
        "links": [
            ("Live Class 1 transcript", "Live Class 1 Transcript.txt"),
            ("Live Class 2 transcript", "Live Class 2 Transcript.txt"),
            ("Study PDF (SLM)", "Data Structure and Algorithm F.pdf"),
        ],
        "extra_cards": [
            ("Live Class 1", "Transcript — opening sessions.", "Live Class 1 Transcript.txt"),
            ("Live Class 2", "Transcript — continued coverage.", "Live Class 2 Transcript.txt"),
        ],
    },
    "csit654": {
        "code": "CSIT654",
        "title_short": "Network Security & Cryptography",
        "kicker": "Network Security and Cryptography",
        "pdf": "Network Security and Cryptography  FINAL.pdf",
        "flash_lede": "Revision cards from the CSIT654 SLM — ciphers, protocols, and security mechanisms.",
        "quiz_lede": "MCQs by module with explanations for Network Security & Cryptography.",
        "map_lede": "Structure maps for each module. Click topics for summaries and practice questions.",
        "links": [
            ("Study PDF (SLM)", "Network Security and Cryptography  FINAL.pdf"),
        ],
        "extra_cards": [],
    },
    "csit745": {
        "code": "CSIT745",
        "title_short": "Research Methodology",
        "kicker": "Research Methodology",
        "pdf": "Research Methodology  Final.pdf",
        "flash_lede": "Flashcards for research design, methods, and analysis from the CSIT745 SLM.",
        "quiz_lede": "Objective questions covering research methodology concepts by module.",
        "map_lede": "Module structure maps with topic details and important questions.",
        "links": [
            ("Study PDF (SLM)", "Research Methodology  Final.pdf"),
        ],
        "extra_cards": [],
    },
}

# Green progress UX extensions
FLASH_CSS = _FLASH_CSS + r"""
.topic-list button {
  --prog: 0%;
  background: linear-gradient(90deg, #cfeee0 var(--prog), rgba(255,255,255,0.7) var(--prog));
  transition: background 0.2s ease, border-color 0.15s ease;
}
.topic-list button.active {
  border-color: rgba(15,107,76,0.4);
}
"""

MAP_CSS = _MAP_CSS + r"""
/* Visit depth: first click must be clearly darker than the pale unvisited base. */
.node.a.depth-1 { background: #a8dfc8; border-color: rgba(15,107,76,.4); }
.node.a.depth-2 { background: #7ecfad; border-color: rgba(15,107,76,.48); }
.node.a.depth-3 { background: #55b890; border-color: rgba(15,107,76,.55); color: #0d3d2e; }
.node.a.depth-4 { background: #3aaa7a; border-color: rgba(15,107,76,.65); color: #fff; }
.node.a.depth-4 .n-sub { color: rgba(255,255,255,.85); }
.node.a.depth-5 { background: #2f9a72; border-color: rgba(15,107,76,.75); color: #fff; }
.node.a.depth-5 .n-sub { color: rgba(255,255,255,.85); }

.node.b.depth-1 { background: #d4c8eb; border-color: rgba(90,70,140,.4); }
.node.b.depth-2 { background: #bba8de; border-color: rgba(90,70,140,.48); }
.node.b.depth-3 { background: #a088cf; border-color: rgba(90,70,140,.55); color: #2a1f45; }
.node.b.depth-4 { background: #8668b8; border-color: rgba(90,70,140,.65); color: #fff; }
.node.b.depth-4 .n-sub { color: rgba(255,255,255,.85); }
.node.b.depth-5 { background: #6f54a3; border-color: rgba(90,70,140,.75); color: #fff; }
.node.b.depth-5 .n-sub { color: rgba(255,255,255,.85); }

.node.c.depth-1 { background: #b4d2ec; border-color: rgba(31,79,120,.4); }
.node.c.depth-2 { background: #8fb8dc; border-color: rgba(31,79,120,.48); }
.node.c.depth-3 { background: #6a9cc8; border-color: rgba(31,79,120,.55); color: #16324a; }
.node.c.depth-4 { background: #4f88b8; border-color: rgba(31,79,120,.65); color: #fff; }
.node.c.depth-4 .n-sub { color: rgba(255,255,255,.85); }
.node.c.depth-5 { background: #3f7aad; border-color: rgba(31,79,120,.75); color: #fff; }
.node.c.depth-5 .n-sub { color: rgba(255,255,255,.85); }

/* LMR keeps coral; must win over group colours (A green / B violet / C blue). */
.node.a.lmr-node, .node.b.lmr-node, .node.c.lmr-node {
  background: #f3dfd0;
  border-color: rgba(196,92,38,.42);
  box-shadow: 0 0 0 2px rgba(196,92,38,.5);
}
.node.lmr-node.depth-1 { background: #ecc8b0; border-color: rgba(196,92,38,.5); }
.node.lmr-node.depth-2 { background: #e0a888; border-color: rgba(196,92,38,.58); }
.node.lmr-node.depth-3 { background: #d08860; border-color: rgba(196,92,38,.66); color: #4a2410; }
.node.lmr-node.depth-4 { background: #c96a3a; border-color: rgba(196,92,38,.74); color: #fff; }
.node.lmr-node.depth-4 .n-sub { color: rgba(255,255,255,.85); }
.node.lmr-node.depth-4 .n-badge { background: rgba(255,255,255,.22); color: #fff; }
.node.lmr-node.depth-5 { background: #c45c26; border-color: rgba(196,92,38,.82); color: #fff; }
.node.lmr-node.depth-5 .n-sub { color: rgba(255,255,255,.85); }
.node.lmr-node.depth-5 .n-badge { background: rgba(255,255,255,.22); color: #fff; }

.detail-tabs {
  display: flex; gap: .35rem; margin: 0 0 .85rem;
  border-bottom: 1px solid var(--line); padding-bottom: .45rem;
}
.detail-tabs .tab {
  appearance: none; border: 1px solid transparent; background: transparent;
  font: inherit; font-weight: 700; font-size: .88rem; color: var(--muted);
  padding: .4rem .75rem; border-radius: 999px; cursor: pointer;
}
.detail-tabs .tab:hover { color: var(--ink); background: rgba(255,255,255,.55); }
.detail-tabs .tab.active { color: #fff; background: var(--accent); border-color: transparent; }
.deep-block { margin: 0 0 1rem; }
.deep-block h3 {
  font-family: var(--font-display); font-size: 1.05rem;
  margin: 0 0 .4rem; color: var(--accent);
}
.deep-block.lmr-heavy h3 { color: var(--warn); }
.deep-block ul { margin: 0; padding-left: 1.1rem; color: var(--ink); }
.deep-block li { margin: .35rem 0; line-height: 1.45; }
.note-trap {
  background: #fff6e8; border-left: 3px solid rgba(196,92,38,.55);
  padding: .55rem .7rem; border-radius: 0 10px 10px 0; margin: .45rem 0;
  color: var(--muted); font-size: .92rem;
}
"""

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650'
    '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />'
)


def load_subject(subject_id: str) -> tuple[dict, dict, str, dict, dict]:
    base = SUBJECTS_DIR / subject_id
    data = json.loads((base / "_study_facts.json").read_text(encoding="utf-8"))
    maps = json.loads((base / "_module_maps.json").read_text(encoding="utf-8"))
    lmr = (base / "_lmr_notes.txt").read_text(encoding="utf-8")
    deep_path = base / "_deep_notes.json"
    deep_notes = json.loads(deep_path.read_text(encoding="utf-8")) if deep_path.exists() else {}
    meta = SUBJECTS[subject_id]
    return data, maps, lmr, meta, deep_notes


def _synth_deep_from_topic(topic: dict | None, lmr: bool = False) -> dict:
    """Fallback when _deep_notes.json lacks an entry — never emit TOC junk as 'terms'."""
    import re

    def toc(text: str) -> bool:
        return len(re.findall(r"\b\d+(?:\.\d+){1,3}\b", text or "")) >= 2

    terms: list[dict] = []
    concepts: list[str] = []
    notes: list[str] = []
    if not topic:
        return {"terms": [], "concepts": [], "notes": []}
    title = topic.get("title") or topic.get("id") or "Topic"
    definition = ""
    for c in topic.get("flashcards") or []:
        back = (c.get("back") or "").strip()
        if back and not toc(back) and len(back) > len(definition):
            definition = back
        if c.get("detail") and not toc(c["detail"]):
            notes.append(c["detail"])
    if definition:
        terms.append({"t": str(title), "d": definition})
    else:
        terms.append({"t": str(title), "d": f"Learn the definition, use-case, and one contrast for {title}."})
    for q in topic.get("mcqs") or []:
        explain = (q.get("explain") or "").strip()
        if explain and not toc(explain):
            notes.append(f"Exam cue: {explain}")
    concepts.append(f"{title}: Overview is short; use the term definition for exam recall.")
    if lmr:
        concepts.append("LMR: definition + use-case + contrast.")
    seen: set[str] = set()
    uniq = []
    for n in notes:
        if n and n not in seen and not toc(n):
            seen.add(n)
            uniq.append(n)
    return {
        "terms": terms[: 6 if lmr else 4],
        "concepts": concepts[: 4 if lmr else 3],
        "notes": uniq[: 7 if lmr else 4],
    }


def _deep_for(key: str, deep_notes: dict, topic: dict | None, lmr: bool = False) -> dict:
    raw = deep_notes.get(key) if deep_notes else None
    if raw and isinstance(raw, dict):
        return {
            "terms": raw.get("terms") or [],
            "concepts": raw.get("concepts") or [],
            "notes": raw.get("notes") or [],
        }
    return _synth_deep_from_topic(topic, lmr=lmr)


def enrich_maps_payload(data: dict, maps: dict, deep_notes: dict | None = None) -> dict:
    deep_notes = deep_notes or {}
    topics_by_id: dict[str, dict] = {}
    mcqs_by_module: dict[int, list] = {}
    for m in data["modules"]:
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
    for mod in maps["modules"]:
        mid = int(mod["id"])
        nodes: dict[str, dict] = {}
        root = dict(mod["root"])
        root_deep = _deep_for(root["id"], deep_notes, None)
        if not any(root_deep.values()):
            root_deep = {
                "terms": [{"t": root["title"], "d": root.get("body") or ""}],
                "concepts": list(root.get("points") or []),
                "notes": ["Open topic cards for Terms · Concepts · Short notes."],
            }
        nodes[root["id"]] = {
            "kind": root.get("kind", "root"),
            "title": root["title"],
            "path": root.get("path", ""),
            "body": root.get("body", ""),
            "points": root.get("points") or [],
            "deepNotes": root_deep,
            "lmr": False,
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
                topic_id = str(n.get("topicId") or nid)
                is_lmr = bool(n.get("lmr"))
                deep = _deep_for(topic_id, deep_notes, topic, lmr=is_lmr)
                if not any(deep.values()):
                    deep = _deep_for(nid, deep_notes, topic, lmr=is_lmr)
                nodes[nid] = {
                    "kind": n.get("kind", "a"),
                    "title": title,
                    "path": path,
                    "body": body or n.get("body") or "Open flashcards for this topic for full notes.",
                    "points": points,
                    "topicId": topic_id,
                    "lmr": is_lmr,
                    "note": n.get("note") or "",
                    "qCount": q_count,
                    "fcCount": fc_count,
                    "deepNotes": deep,
                }
                level_nodes.append(
                    {
                        "id": nid,
                        "title": n["title"],
                        "sub": n.get("sub") or "",
                        "kind": n.get("kind", "a"),
                        "topicId": topic_id,
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


def count_totals(data: dict, maps_payload: dict) -> dict:
    flash_total = 0
    quiz_total = 0
    quiz_answer_key = {}
    for m in data["modules"]:
        for t in m["topics"]:
            flash_total += len(t.get("flashcards") or [])
            for i, q in enumerate(t.get("mcqs") or []):
                qid = f'{m["id"]}-{t["id"]}-q{i}'
                quiz_answer_key[qid] = q["answer"]
                quiz_total += 1
    map_total = 0
    map_answer_key = {}
    for mod in maps_payload["modules"]:
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


def sync_head(shared_prefix: str, subject_id: str | None) -> str:
    sub_line = f'<script>window.AMITY_SUBJECT = "{subject_id}";</script>\n' if subject_id else ""
    return (
        sub_line
        + f'<script src="{shared_prefix}config.js"></script>\n'
        + f'<script src="{shared_prefix}progress.js"></script>\n'
        + f'<script src="{shared_prefix}sync-ui.js"></script>'
    )


def sync_boot(subject_id: str, subject_label: str) -> str:
    return f"""
function bootSync(restoreFn) {{
  const SUBJECT = "{subject_id}";
  function apply(subPayload) {{
    if (subPayload && restoreFn) restoreFn(subPayload);
    window.__AMITY_SYNC_READY = true;
    window.__BS605_SYNC_READY = true;
  }}
  const P = window.AmityProgress || window.BS605Progress;
  const UI = window.AmitySyncUI || window.BS605SyncUI;
  if (UI) {{
    UI.mount(document.getElementById("amity-sync-root"), {{
      subjectLabel: "{subject_label}",
      onLoaded: (sub) => apply(sub),
      onReady: (sub) => {{
        if (window.__AMITY_SYNC_READY) return;
        const local = P && P.readLocalCache && P.readLocalCache();
        const fallback = sub || (P && P.getSubjectPayload && P.getSubjectPayload(local?.payload, SUBJECT)) || null;
        apply(fallback);
      }}
    }});
  }} else {{
    const local = P && P.readLocalCache && P.readLocalCache();
    apply(P && P.getSubjectPayload ? P.getSubjectPayload(local?.payload, SUBJECT) : null);
  }}
}}
"""


def site_nav(active: str, all_subjects: bool = False) -> str:
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
    nav = '<nav class="site-nav" aria-label="Site">' + "".join(parts) + "</nav>"
    if all_subjects:
        nav += (
            '<p style="margin:0.5rem 0 0;font-size:0.88rem">'
            '<a href="../../index.html">← All subjects</a></p>'
        )
    return nav


def links_html(meta: dict) -> str:
    items = []
    for label, url in meta["links"]:
        cls = "lmr-link" if "PDF" in label or "LMR" in label else ""
        items.append(
            f'<a class="{cls}" href="{html_escape(url)}" target="_blank" rel="noopener">'
            f"{html_escape(label)}</a>"
        )
    return '<div class="links">' + "".join(items) + "</div>"


def lmr_items_html(lmr: str) -> str:
    items = []
    for line in lmr.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        text = line.split(". ", 1)[1] if ". " in line[:5] else line
        items.append(f"<li>{html_escape(text)}</li>")
    return "".join(items)


def build_flashcards(subject_id: str, data: dict, lmr: str, meta: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    code = meta["code"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{code} Flashcards — {html_escape(meta["title_short"])}</title>
{FONT_LINK}
<style>{FLASH_CSS}</style>
{sync_head("../../shared/", subject_id)}
</head>
<body>
<div class="wrap">
  {site_nav("flash")}
  <header class="hero">
    <div class="kicker">Amity · {code}</div>
    <h1>{html_escape(meta["title_short"])} flashcards</h1>
    <p class="lede">{html_escape(meta["flash_lede"])}</p>
    <div class="navrow">
      <a class="btn" href="#lmr">LMR priorities</a>
      <a class="btn ghost" href="{html_escape(meta["pdf"])}" target="_blank">Open PDF</a>
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
    {links_html(meta)}
    <div id="amity-sync-root"></div>
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
    <p class="lede" style="margin-bottom:0.4rem">Last-minute revision priorities from the SLM outline:</p>
    <ol>{lmr_items_html(lmr)}</ol>
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
let seen = {{}};
let known = {{}};
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
  if (restoring) return;
  const P = window.AmityProgress || window.BS605Progress;
  if (!P || !window.__AMITY_SYNC_READY) return;
  P.saveSection("flashcards", {{
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
    const pct = topicKeys.length ? Math.round((done / topicKeys.length) * 100) : 0;
    return `<button type="button" class="${{active}}" data-topic="${{t.topicId}}" style="--prog:${{pct}}%"><strong>${{t.topicId}} · ${{t.topicTitle}}</strong><span>Module ${{t.moduleId}} · ${{done}}/${{topicKeys.length}} known</span></button>`;
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
  seen[filtered[index].key] = true;
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
{sync_boot(subject_id, code)}
bootSync(restoreFlash);
</script>
</body>
</html>
"""


def build_quiz(subject_id: str, data: dict, meta: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    code = meta["code"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{code} Objective Questions — {html_escape(meta["title_short"])}</title>
{FONT_LINK}
<style>{QUIZ_CSS}</style>
{sync_head("../../shared/", subject_id)}
</head>
<body>
<div class="wrap">
  {site_nav("quiz")}
  <header class="hero">
    <div class="kicker">Amity · {code}</div>
    <h1>Objective questions by module</h1>
    <p class="lede">{html_escape(meta["quiz_lede"])}</p>
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
    {links_html(meta)}
    <div id="amity-sync-root"></div>
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
const state = {{}};
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

function currentList() {{ return filteredIds.map(i => bank[i]); }}

function persistQuiz() {{
  if (restoring) return;
  const P = window.AmityProgress || window.BS605Progress;
  if (!P || !window.__AMITY_SYNC_READY) return;
  P.saveSection("quiz", {{
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
  const quizMods = DATA.modules.filter(m => bank.some(q => q.moduleId === m.id));
  const mods = [{{id:"all", title:"All exam modules"}}, ...quizMods.map(m => ({{id:String(m.id), title:"Module "+m.id}}))];
  if (activeModule !== "all" && !quizMods.some(m => String(m.id) === String(activeModule))) {{
    activeModule = "all";
  }}
  box.innerHTML = mods.map(m => `<button type="button" class="chip ${{String(activeModule)===String(m.id)?"active":""}}" data-m="${{m.id}}">${{m.title}}</button>`).join("");
  box.querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {{
    activeModule = btn.dataset.m;
    applyFilter(false);
  }}));
}}

function renderStats() {{
  const box = el("moduleStats");
  const quizMods = DATA.modules.filter(m => bank.some(q => q.moduleId === m.id));
  box.innerHTML = quizMods.map(m => {{
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
{sync_boot(subject_id, meta["code"])}
bootSync(restoreQuiz);
</script>
</body>
</html>
"""


def build_module_map(subject_id: str, data: dict, maps: dict, meta: dict, deep_notes: dict | None = None) -> str:
    payload = enrich_maps_payload(data, maps, deep_notes)
    data_json = json.dumps(payload, ensure_ascii=False)
    code = meta["code"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{code} Module Map — {html_escape(meta["title_short"])}</title>
{FONT_LINK}
<style>{MAP_CSS}</style>
{sync_head("../../shared/", subject_id)}
</head>
<body>
<div class="wrap">
  {site_nav("map")}
  <header class="hero">
    <div class="kicker">Amity · {code} · Module Map</div>
    <h1>Structure maps &amp; important questions</h1>
    <p class="lede">{html_escape(meta["map_lede"])}</p>
    <div class="navrow">
      <a class="btn" href="#questions">Important questions</a>
    </div>
  </header>

  <section class="panel">
    <div class="meta" style="margin-bottom:0.6rem">
      <span>This module: <strong id="mapModAttempted">0</strong> / <strong id="mapModTotal">0</strong> answered</span>
      <span>Correct <strong id="mapModCorrect">0</strong></span>
      <span>Visited <strong id="mapVisitedCount">0</strong> topics</span>
      <span>All modules: <strong id="mapAllAttempted">0</strong> / <strong id="mapAllTotal">0</strong></span>
    </div>
    <div class="progress" style="margin-bottom:0.85rem"><span id="mapProgressBar"></span></div>
    <div class="summary-grid" id="mapStats"></div>
    <div class="filters" id="moduleFilters"></div>
    <div class="criteria-box">
      <strong>How this map is built:</strong>
      One card ≈ one study topic from the SLM outline.
      Overview = short blurb. Deep notes = terms, concepts, and short notes (denser on LMR).
      More taps darken a card’s own colour. Orange outline = LMR priority.
    </div>
    <div id="amity-sync-root"></div>
  </section>

  <div class="layout">
    <section class="flow-panel" aria-label="Structure flow diagram">
      <p class="section-label" id="flowLabel">Interactive flow</p>
      <p class="hint-bar">Tap a card → Overview / Deep notes on the right. More taps = darker shade of the same colour.</p>
      <div class="legend">
        <span><i class="swatch" style="background:#116b54"></i> Module root</span>
        <span><i class="swatch" style="background:#d8efe4"></i> Group A</span>
        <span><i class="swatch" style="background:#ebe4f5"></i> Group B</span>
        <span><i class="swatch" style="background:#dceaf7"></i> Group C</span>
        <span><i class="swatch" style="background:#7ecfad;outline:2px solid rgba(15,107,76,.35)"></i> Deeper = more visits</span>
        <span><i class="swatch" style="background:#f3dfd0;outline:2px solid rgba(196,92,38,.55)"></i> LMR badge + coral only</span>
      </div>
      <div class="tree" id="tree"></div>
    </section>
    <aside class="detail-panel" id="detailPanel">
      <p class="section-label">Selected term</p>
      <div class="detail-tabs" role="tablist">
        <button type="button" class="tab active" role="tab" id="tabOverview" aria-selected="true">Overview</button>
        <button type="button" class="tab" role="tab" id="tabDeep" aria-selected="false">Deep notes</button>
      </div>
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
let mapAnswers = {{}};
let mapVisited = {{}};
let restoring = false;
let topicFilter = null;
let selectedNodeId = null;
let detailTab = "overview";

const el = id => document.getElementById(id);
const mapProgressBar = el("mapProgressBar");
const mapAllTotal = MAPS.modules.reduce((n, m) => n + (m.questions || []).length, 0);
el("mapAllTotal").textContent = mapAllTotal;

function visitedKey(nodeId) {{
  return String(activeModuleId) + ":" + nodeId;
}}

function currentModule() {{
  return MAPS.modules.find(m => String(m.id) === String(activeModuleId)) || MAPS.modules[0];
}}

function weightLabel(w) {{
  if (w === "high") return " · exam focus";
  if (w === "foundation") return " · foundation";
  if (w === "deferred") return " · later class";
  return "";
}}

function visitCount(nodeId) {{
  const v = mapVisited[visitedKey(nodeId)];
  if (v === true) return 1;
  const n = Number(v);
  return Number.isFinite(n) && n > 0 ? Math.min(5, Math.floor(n)) : 0;
}}

function countVisited() {{
  return Object.keys(mapVisited).filter(k => {{
    const v = mapVisited[k];
    if (v === true) return true;
    const n = Number(v);
    return Number.isFinite(n) && n > 0;
  }}).length;
}}

function applyVisitDepth(node) {{
  for (let i = 1; i <= 5; i++) node.classList.remove("depth-" + i);
  const c = visitCount(node.dataset.id);
  if (c > 0) node.classList.add("depth-" + c);
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
  el("mapVisitedCount").textContent = countVisited();
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
  if (restoring) return;
  const P = window.AmityProgress || window.BS605Progress;
  if (!P || !window.__AMITY_SYNC_READY) return;
  P.saveSubjectProgress({{
    mapAnswers: mapAnswers,
    mapVisited: mapVisited,
    mapMeta: {{ activeModuleId: String(activeModuleId), topicFilter: topicFilter, selectedNodeId: selectedNodeId }}
  }});
}}

function restoreMap(payload) {{
  if (!payload) return;
  restoring = true;
  if (payload.mapAnswers && typeof payload.mapAnswers === "object") mapAnswers = payload.mapAnswers;
  if (payload.mapVisited && typeof payload.mapVisited === "object") {{
    mapVisited = {{}};
    Object.keys(payload.mapVisited).forEach(k => {{
      const v = payload.mapVisited[k];
      if (v === true) mapVisited[k] = 1;
      else {{
        const n = Number(v);
        if (Number.isFinite(n) && n > 0) mapVisited[k] = Math.min(5, Math.floor(n));
      }}
    }});
  }}
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
  const depth = visitCount(id);
  const depthCls = depth > 0 ? " depth-" + depth : "";
  return `<button type="button" class="node ${{cls}}${{lmrCls}}${{depthCls}}" data-id="${{id}}"><span class="n-title">${{title}}</span><span class="n-sub">${{sub || ""}}</span>${{badge}}</button>`;
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
    btn.addEventListener("click", () => showNode(btn.dataset.id, {{ mark: true }}));
  }});
  showNode(selectedNodeId && current.nodes[selectedNodeId] ? selectedNodeId : current.rootId, {{ mark: false }});
}}

function showNode(id, opts) {{
  const n = current.nodes[id];
  if (!n) return;
  selectedNodeId = id;
  const mark = !!(opts && opts.mark);
  if (mark && n.kind !== "root") {{
    const key = visitedKey(id);
    mapVisited[key] = Math.min(5, visitCount(id) + 1);
  }}
  document.querySelectorAll(".node").forEach(node => {{
    node.classList.toggle("active", node.dataset.id === id);
    applyVisitDepth(node);
  }});
  renderDetailPanel(n, id);
  if (n.kind !== "root") topicFilter = n.topicId || id;
  else topicFilter = null;
  renderQuestions();
  updateMapStats();
  if (window.matchMedia("(max-width: 920px)").matches) {{
    el("detailPanel").scrollIntoView({{ behavior: "smooth", block: "nearest" }});
  }}
  if (!restoring) persistMap();
}}

function renderDetailPanel(n, id) {{
  const tabOverview = el("tabOverview");
  const tabDeep = el("tabDeep");
  if (tabOverview && tabDeep) {{
    tabOverview.classList.toggle("active", detailTab === "overview");
    tabDeep.classList.toggle("active", detailTab === "deep");
    tabOverview.setAttribute("aria-selected", detailTab === "overview" ? "true" : "false");
    tabDeep.setAttribute("aria-selected", detailTab === "deep" ? "true" : "false");
  }}
  if (detailTab === "deep") {{
    el("detailContent").innerHTML = renderDeepNotes(n);
  }} else {{
    el("detailContent").innerHTML = renderOverview(n, id);
    const focusBtn = el("focusQsBtn");
    if (focusBtn) {{
      focusBtn.addEventListener("click", () => {{
        topicFilter = n.topicId || id;
        renderQuestions();
        persistMap();
        el("questions").scrollIntoView({{ behavior: "smooth", block: "start" }});
      }});
    }}
  }}
}}

function renderOverview(n, id) {{
  const points = (n.points || []).map(p => `<li>${{p}}</li>`).join("");
  const lmrLine = n.lmr ? `<span class="detail-kicker" style="background:#f8e5d8;color:var(--warn)">LMR priority</span>` : "";
  const counts = n.kind === "root" ? "" : `<p class="parent-path">${{n.fcCount || 0}} flashcards · ${{n.qCount || 0}} MCQs in bank</p>`;
  return `
    ${{lmrLine}}
    <div class="detail-kicker">${{n.kind === "root" ? "Module" : "Topic"}}</div>
    <h2 class="detail-title">${{n.title}}</h2>
    <p class="parent-path">${{n.path || ""}}</p>
    ${{counts}}
    <p class="detail-body">${{n.body || ""}}</p>
    ${{points ? `<ul class="detail-points">${{points}}</ul>` : ""}}
    ${{n.kind !== "root" ? `<div class="navrow" style="margin-top:0.8rem"><button type="button" class="btn primary" id="focusQsBtn">Practice this topic</button></div>` : ""}}
  `;
}}

function renderDeepNotes(n) {{
  const d = n.deepNotes || {{}};
  const terms = (d.terms || []).map(x => `<li><strong>${{x.t}}:</strong> ${{x.d}}</li>`).join("");
  const concepts = (d.concepts || []).map(c => `<li>${{c}}</li>`).join("");
  const notes = (d.notes || []).map(note => `<div class="note-trap">${{note}}</div>`).join("");
  const heavy = n.lmr ? " lmr-heavy" : "";
  const lmrLine = n.lmr ? `<span class="detail-kicker" style="background:#f8e5d8;color:var(--warn)">LMR · denser notes</span>` : "";
  const empty = !terms && !concepts && !notes;
  return `
    ${{lmrLine}}
    <div class="detail-kicker">Deep notes</div>
    <h2 class="detail-title">${{n.title}}</h2>
    <p class="parent-path">${{n.path || ""}}</p>
    ${{empty ? `<p class="detail-empty">Deep notes for this topic are still being added — use Overview and flashcards for now.</p>` : ""}}
    ${{terms ? `<div class="deep-block${{heavy}}"><h3>Terms</h3><ul>${{terms}}</ul></div>` : ""}}
    ${{concepts ? `<div class="deep-block${{heavy}}"><h3>Concepts</h3><ul>${{concepts}}</ul></div>` : ""}}
    ${{notes ? `<div class="deep-block${{heavy}}"><h3>Short notes</h3>${{notes}}</div>` : ""}}
  `;
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

el("tabOverview").addEventListener("click", () => {{
  detailTab = "overview";
  if (selectedNodeId && current.nodes[selectedNodeId]) renderDetailPanel(current.nodes[selectedNodeId], selectedNodeId);
}});
el("tabDeep").addEventListener("click", () => {{
  detailTab = "deep";
  if (selectedNodeId && current.nodes[selectedNodeId]) renderDetailPanel(current.nodes[selectedNodeId], selectedNodeId);
}});

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
{sync_boot(subject_id, code)}
bootSync(restoreMap);
</script>
</body>
</html>
"""


def build_subject_index(subject_id: str, data: dict, maps: dict, meta: dict, deep_notes: dict | None = None) -> str:
    maps_payload = enrich_maps_payload(data, maps, deep_notes)
    totals = count_totals(data, maps_payload)
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
    code = meta["code"]
    extra_cards = "".join(
        f'<a href="{html_escape(href)}" target="_blank"><h2>{html_escape(title)}</h2>'
        f"<p>{html_escape(desc)}</p></a>"
        for title, desc, href in meta.get("extra_cards", [])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{code} Study Pack — {html_escape(meta["title_short"])}</title>
{FONT_LINK}
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
{sync_head("../../shared/", subject_id)}
</head>
<body>
<div class="wrap">
  {site_nav("home", all_subjects=True)}
  <header class="hero">
    <div class="kicker">Amity University Online · {code}</div>
    <h1>{html_escape(meta["title_short"])} study pack</h1>
    <p class="lede">Home for every {code} study tool. Connect a sync code once — progress auto-saves across phone and PC.</p>
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
    <div id="amity-sync-root"></div>
  </section>

  <section class="panel">
    <strong>All pages</strong>
    <div class="cards" style="margin-top:0.9rem">
      <a href="module-map.html"><h2>Module Map</h2><p>Structure maps + important questions.</p><div class="tool-prog" id="cardMapProg">Not started</div></a>
      <a href="flashcards.html"><h2>Flashcards</h2><p>{totals["flashTotal"]} revision cards with LMR priority list.</p><div class="tool-prog" id="cardFlashProg">Not started</div></a>
      <a href="quiz.html"><h2>Objective quiz</h2><p>{totals["quizTotal"]} MCQs with explanations, filter by module.</p><div class="tool-prog" id="cardQuizProg">Not started</div></a>
      <a href="{html_escape(meta["pdf"])}" target="_blank"><h2>Study PDF</h2><p>Full SLM (opens in a new tab).</p></a>
      {extra_cards}
    </div>
  </section>
</div>
<script>
const TOTALS = {totals_json};
function paintHome(payload) {{
  const P = window.AmityProgress || window.BS605Progress;
  if (!P) return;
  const s = P.summarize(payload || {{}}, TOTALS);
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
    ? (m.attempted + " answered · " + m.correct + " correct" + (m.visited ? " · " + m.visited + " visited" : ""))
    : "Not started";
}}
{sync_boot(subject_id, code)}
bootSync(paintHome);
</script>
</body>
</html>
"""


def build_root_index(subject_totals: dict[str, dict]) -> str:
    cards = []
    for sid, meta in SUBJECTS.items():
        t = subject_totals[sid]
        cards.append(
            f'<a href="subjects/{sid}/index.html">'
            f'<h2>{meta["code"]}</h2>'
            f'<p>{html_escape(meta["title_short"])}</p>'
            f'<div class="tool-prog" id="prog-{sid}">'
            f'{t["flashTotal"]} cards · {t["quizTotal"]} MCQs · {t["mapTotal"]} map Qs</div></a>'
        )
    cards_html = "\n      ".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Amity Study Hub</title>
{FONT_LINK}
<style>{SHARED_CSS}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1rem; margin-top:1.2rem; }}
.cards a {{
  display:block; text-decoration:none; color:inherit; padding:1.3rem; border-radius:var(--radius);
  border:1px solid var(--line); background:var(--panel); box-shadow:var(--shadow);
  transition: transform .15s ease;
}}
.cards a:hover {{ transform: translateY(-3px); border-color: rgba(15,107,76,0.35); }}
.cards h2 {{ font-family:var(--font-display); margin:0 0 .4rem; font-size:1.55rem; color:var(--accent); }}
.cards p {{ margin:0; color:var(--muted); }}
.cards .tool-prog {{ margin-top:0.75rem; font-size:0.88rem; color:var(--ink); font-weight:600; }}
.hub-note {{ font-size:0.92rem; color:var(--muted); margin-top:0.5rem; }}
</style>
<script>window.AMITY_SUBJECT = "hub";</script>
{sync_head("shared/", None)}
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Amity University Online</div>
    <h1>Study hub — all subjects</h1>
    <p class="lede">Pick a subject to open flashcards, module maps, and quizzes. One sync code works everywhere — each subject keeps its own progress.</p>
  </header>

  <section class="panel" style="margin-bottom:1rem">
    <strong>Cloud sync</strong>
    <p class="hub-note">Connect once below. Existing BS605 progress is preserved automatically.</p>
    <div id="amity-sync-root"></div>
  </section>

  <section class="panel">
    <strong>Subjects</strong>
    <div class="cards" style="margin-top:0.9rem">
      {cards_html}
    </div>
  </section>
</div>
<script>
function bootHubSync() {{
  const UI = window.AmitySyncUI || window.BS605SyncUI;
  if (UI) {{
    UI.mount(document.getElementById("amity-sync-root"), {{
      subjectLabel: "all subjects",
      onLoaded: () => {{}},
      onReady: () => {{}}
    }});
  }}
}}
bootHubSync();
</script>
</body>
</html>
"""


def build_redirect(target: str, label: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta http-equiv="refresh" content="0;url={html_escape(target)}" />
<link rel="canonical" href="{html_escape(target)}" />
<title>Redirect — {html_escape(label)}</title>
<script>location.replace("{target}");</script>
</head>
<body>
<p>Redirecting to <a href="{html_escape(target)}">{html_escape(label)}</a>…</p>
</body>
</html>
"""


def copy_root_js() -> None:
    for name in ("config.js", "progress.js", "sync-ui.js"):
        src = SHARED / name
        dst = ROOT / name
        if src.exists():
            shutil.copy2(src, dst)


def build_subject(subject_id: str) -> dict:
    data, maps, lmr, meta, deep_notes = load_subject(subject_id)
    out = SUBJECTS_DIR / subject_id
    out.mkdir(parents=True, exist_ok=True)
    maps_payload = enrich_maps_payload(data, maps, deep_notes)
    totals = count_totals(data, maps_payload)

    pages = {
        "index.html": build_subject_index(subject_id, data, maps, meta, deep_notes),
        "flashcards.html": build_flashcards(subject_id, data, lmr, meta),
        "quiz.html": build_quiz(subject_id, data, meta),
        "module-map.html": build_module_map(subject_id, data, maps, meta, deep_notes),
    }
    for name, html in pages.items():
        (out / name).write_text(html, encoding="utf-8")
    return totals


def main() -> None:
    subject_totals: dict[str, dict] = {}
    for sid in SUBJECTS:
        subject_totals[sid] = build_subject(sid)
        t = subject_totals[sid]
        print(
            f"  {sid}: flash={t['flashTotal']} quiz={t['quizTotal']} map={t['mapTotal']} "
            f"-> subjects/{sid}/"
        )

    (ROOT / "index.html").write_text(build_root_index(subject_totals), encoding="utf-8")
    print("Wrote index.html (hub)")

    for page in ("flashcards.html", "quiz.html", "module-map.html"):
        target = f"subjects/bs605/{page}"
        (ROOT / page).write_text(build_redirect(target, f"BS605 {page.replace('.html','')}"), encoding="utf-8")
        print(f"Wrote redirect {page} -> {target}")

    copy_root_js()
    print("Copied shared/*.js -> root (backward compatible)")

    print("\nDone. Legacy BS605 progress migration: shared/progress.js (normalizePayload + LEGACY_* keys)")


if __name__ == "__main__":
    main()
