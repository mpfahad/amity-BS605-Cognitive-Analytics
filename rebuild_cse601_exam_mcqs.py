# -*- coding: utf-8 -*-
"""Rebuild CSE601 MCQs from deep notes + _exam_policy.json.

- Modules 1–2: denser MCQs on Live Class exam priorities (LMR)
- Modules 3–5: quizzes kept — hand-picked high-weight topics from SLM
- Skip only policy quiz_skip_topics (teacher avoid / downweight)
- deferred_modules (if any) cleared from quizzes

Run after deep notes + apply_handpicked_lmr.py:
  python rebuild_cse601_exam_mcqs.py
  python build_hub.py
"""
from __future__ import annotations

import json
from pathlib import Path

from rebuild_mcqs_from_deep import (
    collect_bank_defs,
    distractors_for,
    mcq,
    rng_for,
)

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "subjects" / "cse601"
POLICY_PATH = BASE / "_exam_policy.json"


def load_policy() -> dict:
    if not POLICY_PATH.exists():
        raise SystemExit(f"Missing {POLICY_PATH} — see EXAM-CURATION-GUIDE.md")
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


POLICY = load_policy()

# No live-class transcript weight yet — exclude from all quizzes.
SKIP_MODULES = {int(x) for x in (POLICY.get("deferred_modules") or [])}

# Skip from quizzes even inside covered modules (teacher downweight / not exam-focus).
SKIP_TOPICS = set(POLICY.get("quiz_skip_topics") or [])

# Live Class taught exam priorities — denser quiz weight.
HIGH_TOPICS = set(POLICY.get("high_quiz_topics") or POLICY.get("lmr_topic_ids") or [])

# Light coverage (know symbols / stack application / related syllabus).
LOW_TOPICS = set(POLICY.get("low_quiz_topics") or [])

MODULE_WEIGHTS = {
    int(k): v for k, v in (POLICY.get("module_weights") or {}).items()
}


def mcqs_weighted(topic_title: str, tid: str, deep: dict, bank_defs: list[str], cap: int) -> list[dict]:
    if not deep or cap <= 0:
        return []
    terms = [t for t in (deep.get("terms") or []) if (t.get("t") and t.get("d"))]
    concepts = [c.strip() for c in (deep.get("concepts") or []) if (c or "").strip()]
    notes = [n.strip() for n in (deep.get("notes") or []) if (n or "").strip()]
    # Prefer teacher/LMR tips for high-weight stems
    exam_notes = [
        n
        for n in notes
        if n.lower().startswith("lmr") or "class 1" in n.lower() or "class 2" in n.lower()
    ]
    out: list[dict] = []

    term_cap = min(len(terms), 5 if cap >= 5 else 3)
    for i, term in enumerate(terms[:term_cap]):
        if len(out) >= cap:
            break
        name, desc = term["t"].strip(), term["d"].strip()
        wrong_pool = [t["d"] for t in terms if t is not term] + bank_defs
        wrongs = distractors_for(desc, wrong_pool, 3, rng_for(tid, "def", name))
        out.append(
            mcq(
                q=f"Which statement best defines {name}?",
                correct=desc,
                wrongs=wrongs,
                explain=f"{name}: {desc}",
                key=f"{tid}-wdef-{i}",
            )
        )

    for i, concept in enumerate(concepts):
        if len(out) >= cap:
            break
        wrongs = distractors_for(concept, bank_defs + concepts, 3, rng_for(tid, "idea", str(i)))
        out.append(
            mcq(
                q=f"Which key idea belongs with {topic_title}?",
                correct=concept,
                wrongs=wrongs,
                explain=concept,
                key=f"{tid}-widea-{i}",
            )
        )

    for i, note in enumerate(exam_notes + notes):
        if len(out) >= cap:
            break
        # Prefer actionable exam tips; skip pure "no live-class" meta lines
        if note.lower().startswith("no live-class"):
            continue
        wrongs = distractors_for(note, bank_defs + notes, 3, rng_for(tid, "note", str(i)))
        out.append(
            mcq(
                q=f"Which exam tip fits {topic_title}?",
                correct=note,
                wrongs=wrongs,
                explain=note,
                key=f"{tid}-wnote-{i}",
            )
        )

    seen = set()
    uniq = []
    for q in out:
        if q["q"] in seen:
            continue
        seen.add(q["q"])
        uniq.append(q)
    return uniq[:cap]


def topic_cap(tid: str) -> int:
    if tid in SKIP_TOPICS:
        return 0
    if tid in HIGH_TOPICS:
        return 6
    if tid in LOW_TOPICS:
        return 1
    # Remaining M1/M2/M5 syllabus: standard weight
    return 3


def update_module_map_weights() -> None:
    path = BASE / "_module_maps.json"
    maps = json.loads(path.read_text(encoding="utf-8"))
    for mod in maps.get("modules") or []:
        mid = int(mod["id"])
        mod["weight"] = MODULE_WEIGHTS.get(mid, "standard")
        root = mod.get("root") or {}
        points = list(root.get("points") or [])
        points = [p for p in points if "Quiz deferred" not in p and "exam focus" not in p.lower() and "SLM hand-pick" not in p]
        if MODULE_WEIGHTS.get(mid) == "deferred":
            points.append("Quiz deferred until live class weights this module")
        elif MODULE_WEIGHTS.get(mid) == "high":
            points.append("Module map LMR badges + quiz weight follow Live Class exam focus")
        else:
            points.append("Quizzes are SLM hand-picks until a live class weights this module")
        root["points"] = points
        mod["root"] = root
    path.write_text(json.dumps(maps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    facts = json.loads((BASE / "_study_facts.json").read_text(encoding="utf-8"))
    deep = json.loads((BASE / "_deep_notes.json").read_text(encoding="utf-8"))
    bank = collect_bank_defs(deep)

    stats = {"high": 0, "std": 0, "low": 0, "skipped_topics": 0, "skipped_modules": 0, "mcq_total": 0}

    for mod in facts.get("modules") or []:
        mid = int(mod["id"])
        if mid in SKIP_MODULES:
            for topic in mod.get("topics") or []:
                topic["mcqs"] = []
                topic["quizSkip"] = True
                stats["skipped_modules"] += 1
            continue
        for topic in mod.get("topics") or []:
            tid = str(topic.get("id") or "")
            title = topic.get("title") or tid
            cap = topic_cap(tid)
            if cap == 0:
                topic["mcqs"] = []
                topic["quizSkip"] = True
                stats["skipped_topics"] += 1
                continue
            topic.pop("quizSkip", None)
            pack = deep.get(tid) or {}
            topic["mcqs"] = mcqs_weighted(title, tid, pack, bank, cap)
            n = len(topic["mcqs"])
            stats["mcq_total"] += n
            if tid in HIGH_TOPICS:
                stats["high"] += n
            elif tid in LOW_TOPICS:
                stats["low"] += n
            else:
                stats["std"] += n

    (BASE / "_study_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    update_module_map_weights()
    print(
        f"cse601 exam MCQs: total={stats['mcq_total']} "
        f"high={stats['high']} std={stats['std']} low={stats['low']} "
        f"skip_topics={stats['skipped_topics']} cleared_mod_topics={stats['skipped_modules']}"
    )


if __name__ == "__main__":
    main()
