# -*- coding: utf-8 -*-
"""Rebuild MCQs (and re-check flashcards) from _deep_notes.json.

Replaces the outline-generator template:
  Q: Which statement best matches <Topic>?
  Options: core idea / unrelated / keyword / definition-only label

with real definition and contrast questions built from deep-notes terms/concepts.

  python rebuild_mcqs_from_deep.py
  python build_hub.py
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"
CODES = ("cse601", "csit654", "csit745")


def rng_for(*parts: str) -> random.Random:
    seed = int(hashlib.md5("|".join(parts).encode("utf-8")).hexdigest()[:8], 16)
    return random.Random(seed)


def distractors_for(correct: str, pool: list[str], n: int, rng: random.Random) -> list[str]:
    """Pick up to n wrong options from pool, never equal to correct."""
    cnorm = re.sub(r"\s+", " ", correct.strip().lower())
    cands = []
    for p in pool:
        p = (p or "").strip()
        if not p:
            continue
        if re.sub(r"\s+", " ", p.lower()) == cnorm:
            continue
        if p not in cands:
            cands.append(p)
    rng.shuffle(cands)
    out = cands[:n]
    # pad with generic but non-syllabus-meta distractors if needed
    fillers = [
        "It stores data only in secondary memory with no in-memory operations.",
        "It always runs in constant time regardless of input size.",
        "It is used only for UI layout and has no algorithmic role.",
        "It guarantees an optimal solution for every NP-hard problem.",
        "It removes the need for any data structure or analysis.",
    ]
    fi = 0
    while len(out) < n and fi < len(fillers):
        if fillers[fi] not in out and fillers[fi] != correct:
            out.append(fillers[fi])
        fi += 1
    return out[:n]


def mcq(q: str, correct: str, wrongs: list[str], explain: str, key: str) -> dict:
    opts = [correct] + wrongs
    rng = rng_for(key, q, correct)
    rng.shuffle(opts)
    return {
        "q": q,
        "options": opts,
        "answer": opts.index(correct),
        "explain": explain,
    }


def mcqs_from_deep(topic_title: str, tid: str, deep: dict | None, bank_defs: list[str]) -> list[dict]:
    if not deep:
        return []
    terms = [t for t in (deep.get("terms") or []) if (t.get("t") and t.get("d"))]
    concepts = [c.strip() for c in (deep.get("concepts") or []) if (c or "").strip()]
    notes = [n.strip() for n in (deep.get("notes") or []) if (n or "").strip()]
    out: list[dict] = []

    # 1) Definition MCQs from each term (cap 3)
    for i, term in enumerate(terms[:3]):
        name, desc = term["t"].strip(), term["d"].strip()
        wrong_pool = [t["d"] for t in terms if t is not term] + bank_defs
        wrongs = distractors_for(desc, wrong_pool, 3, rng_for(tid, "def", name))
        out.append(
            mcq(
                q=f"Which statement best defines {name}?",
                correct=desc,
                wrongs=wrongs,
                explain=f"{name}: {desc}",
                key=f"{tid}-def-{i}",
            )
        )

    # 2) Contrast / concept MCQs
    for i, concept in enumerate(concepts[:2]):
        if " — " in concept:
            left, right = concept.split(" — ", 1)
            left, right = left.strip(), right.strip()
            wrongs = distractors_for(right, bank_defs + [c.split(" — ", 1)[-1] for c in concepts if " — " in c], 3, rng_for(tid, "con", str(i)))
            out.append(
                mcq(
                    q=f"Regarding “{left}”, which is correct?",
                    correct=right,
                    wrongs=wrongs,
                    explain=concept,
                    key=f"{tid}-con-{i}",
                )
            )
        elif "→" in concept or " vs " in concept.lower():
            wrongs = distractors_for(concept, bank_defs + concepts, 3, rng_for(tid, "vs", str(i)))
            # ask which statement is true
            out.append(
                mcq(
                    q=f"Which statement about {topic_title} is correct?",
                    correct=concept,
                    wrongs=wrongs,
                    explain=concept,
                    key=f"{tid}-vs-{i}",
                )
            )
        else:
            wrongs = distractors_for(concept, bank_defs + concepts, 3, rng_for(tid, "idea", str(i)))
            out.append(
                mcq(
                    q=f"Which key idea belongs with {topic_title}?",
                    correct=concept,
                    wrongs=wrongs,
                    explain=concept,
                    key=f"{tid}-idea-{i}",
                )
            )

    # 3) One note-based recall if still thin
    if len(out) < 2 and notes:
        note = notes[0]
        wrongs = distractors_for(note, bank_defs + notes[1:], 3, rng_for(tid, "note"))
        out.append(
            mcq(
                q=f"Which exam tip fits {topic_title}?",
                correct=note,
                wrongs=wrongs,
                explain=note,
                key=f"{tid}-note",
            )
        )

    # De-dupe by question text
    seen = set()
    uniq = []
    for q in out:
        if q["q"] in seen:
            continue
        seen.add(q["q"])
        uniq.append(q)
    return uniq[:4]


def collect_bank_defs(deep: dict) -> list[str]:
    defs = []
    for pack in deep.values():
        for t in pack.get("terms") or []:
            if t.get("d"):
                defs.append(t["d"].strip())
    # unique preserve order
    out, seen = [], set()
    for d in defs:
        k = d.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(d)
    return out


def is_template_mcq(q: dict) -> bool:
    text = q.get("q") or ""
    opts = q.get("options") or []
    if "Which statement best matches" in text:
        return True
    if any("core idea in" in o for o in opts):
        return True
    if "is a syllabus topic under" in (q.get("explain") or ""):
        return True
    return False


def rebuild_subject(code: str) -> dict:
    base = SUBJECTS / code
    facts = json.loads((base / "_study_facts.json").read_text(encoding="utf-8"))
    deep = json.loads((base / "_deep_notes.json").read_text(encoding="utf-8"))
    bank = collect_bank_defs(deep)

    topics_fixed = 0
    mcq_total = 0
    still_template = 0

    for mod in facts.get("modules") or []:
        for topic in mod.get("topics") or []:
            tid = topic.get("id") or ""
            title = topic.get("title") or tid
            pack = deep.get(tid) or {}
            new_mcqs = mcqs_from_deep(title, tid, pack, bank)
            if new_mcqs:
                topic["mcqs"] = new_mcqs
                topics_fixed += 1
            else:
                # strip templates even if we have nothing better yet
                cleaned = [q for q in (topic.get("mcqs") or []) if not is_template_mcq(q)]
                topic["mcqs"] = cleaned
                if not cleaned:
                    still_template += 1
            mcq_total += len(topic.get("mcqs") or [])

    (base / "_study_facts.json").write_text(
        json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "code": code,
        "topics_fixed": topics_fixed,
        "mcq_total": mcq_total,
        "topics_empty_mcq": still_template,
    }


def audit(code: str) -> dict:
    facts = json.loads((SUBJECTS / code / "_study_facts.json").read_text(encoding="utf-8"))
    qs = [q for m in facts["modules"] for t in m["topics"] for q in (t.get("mcqs") or [])]
    fcs = [c for m in facts["modules"] for t in m["topics"] for c in (t.get("flashcards") or [])]
    return {
        "code": code,
        "mcq": len(qs),
        "template_mcq": sum(1 for q in qs if is_template_mcq(q)),
        "flash": len(fcs),
        "exam_focus_fc": sum(1 for c in fcs if (c.get("front") or "").startswith("Exam focus")),
        "placeholder_fc": sum(1 for c in fcs if "syllabus topic in this module" in (c.get("back") or "")),
        "sample_q": (qs[0]["q"] if qs else None),
        "sample_opts": (qs[0]["options"] if qs else None),
    }


def patch_generator() -> None:
    """Stop generate_facts_from_outline.py from recreating template MCQs."""
    path = ROOT / "generate_facts_from_outline.py"
    text = path.read_text(encoding="utf-8")
    if "TEMPLATE MCQ REMOVED" in text:
        return
    # Replace the mcq block construction with a comment + empty list default;
    # deep-notes rebuild is the source of truth for these subjects.
    old = '''            options = [
                f"A definition-only label with no role in {meta['title_short']}",
                f"A core idea in {meta['title_short']}: {title}",
                f"Unrelated to Module {mid}",
                f"Only a programming-language keyword with no syllabus meaning",
            ]
            seed = int(hashlib.md5(f"Which statement best matches {title}?".encode()).hexdigest()[:8], 16)
            rng = random.Random(seed)
            correct = options[1]
            rng.shuffle(options)
            mcq = {
                "q": f"Which statement best matches {title}?",
                "options": options,
                "answer": options.index(correct),
                "explain": f"{title} is a syllabus topic under {parent_title} in Module {mid}.",
            }
            # Prefer a second MCQ from the definition when it has a clear keyword
            topics.append({"id": tid, "title": title, "flashcards": fc, "mcqs": [mcq]})'''
    new = '''            # TEMPLATE MCQ REMOVED — do not emit "Which statement best matches".
            # Real MCQs come from rebuild_mcqs_from_deep.py / deep notes.
            mcqs = []
            if definition and not looks_like_toc(definition):
                wrongs = [
                    "It has no role in algorithmic problem-solving.",
                    "It only names a UI widget with no technical meaning.",
                    "It always guarantees O(1) time for every input size.",
                ]
                opts = [definition] + wrongs
                seed = int(hashlib.md5(f"define:{tid}:{title}".encode()).hexdigest()[:8], 16)
                rng = random.Random(seed)
                rng.shuffle(opts)
                mcqs.append({
                    "q": f"Which statement best defines {title}?",
                    "options": opts,
                    "answer": opts.index(definition),
                    "explain": f"{title}: {definition}",
                })
            topics.append({"id": tid, "title": title, "flashcards": fc, "mcqs": mcqs})'''
    if old not in text:
        print("WARN: generate_facts_from_outline.py pattern not found; skip patch")
        return
    path.write_text(text.replace(old, new), encoding="utf-8")
    print("Patched generate_facts_from_outline.py")


def main() -> None:
    print("BEFORE")
    for code in list(CODES) + ["bs605"]:
        print(audit(code))
    print("REBUILD")
    for code in CODES:
        print(rebuild_subject(code))
    patch_generator()
    print("AFTER")
    for code in list(CODES) + ["bs605"]:
        print(audit(code))


if __name__ == "__main__":
    main()
