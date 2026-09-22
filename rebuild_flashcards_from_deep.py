# -*- coding: utf-8 -*-
"""Rebuild flashcard backs from _deep_notes.json so cards show real answers.

Fixes CSE601 / CSIT654 / CSIT745 packs where many cards were:
- \"Exam focus: X\" with a Define-X prompt as the back (still a question)
- \"X: a syllabus topic in this module…\" placeholders

Run from repo root:
  python rebuild_flashcards_from_deep.py
  python build_hub.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"
CODES = ("cse601", "csit654", "csit745")


def is_weak_back(back: str) -> bool:
    b = (back or "").strip()
    if not b:
        return True
    if b.startswith("Define "):
        return True
    if "syllabus topic in this module" in b:
        return True
    if b.rstrip().endswith((" the", " a", " an", " with", " for", " and", " of", " to", " is", " are", ",")):
        return True
    if len(b) < 35:
        return True
    return False


def cards_from_deep(topic_title: str, tid: str, deep: dict | None) -> list[dict]:
    """Build answer-bearing flashcards from a deep-notes pack."""
    cards: list[dict] = []
    if not deep:
        return cards

    for term in deep.get("terms") or []:
        name = (term.get("t") or "").strip()
        desc = (term.get("d") or "").strip()
        if not name or not desc:
            continue
        back = desc
        if len(back) < 45:
            back = f"{name}: {desc}"
        if len(back) < 45:
            back = f"In {topic_title}, {name} means: {desc}"
        if len(back) < 25:
            continue
        cards.append(
            {
                "front": f"What is {name}?",
                "back": back,
                "detail": f"{tid} · {topic_title}" if tid else topic_title,
            }
        )

    for i, concept in enumerate(deep.get("concepts") or []):
        text = (concept or "").strip()
        if not text:
            continue
        if " — " in text:
            left, right = text.split(" — ", 1)
            left, right = left.strip(), right.strip()
            if len(right) >= 40:
                front = left.rstrip(".?") + "?"
                back = right
            else:
                # Keep full contrast as the answer; avoid tiny fragments like "LIFO vs FIFO."
                front = f"Key contrast in {topic_title}"
                back = text
        elif ": " in text and len(text) < 160:
            left, right = text.split(": ", 1)
            left, right = left.strip(), right.strip()
            if len(right) >= 40:
                front = f"What about {left}?"
                back = right
            else:
                front = f"Key idea ({topic_title})"
                back = text
        else:
            front = f"Key idea ({topic_title})" if i == 0 else f"Also remember ({topic_title})"
            back = text

        if len(back) < 25:
            continue
        cards.append(
            {
                "front": front,
                "back": back,
                "detail": f"{tid} · key idea",
            }
        )

    # Cap per topic so decks stay usable; keep richest first (terms already first)
    return cards[:6]


def rebuild_subject(code: str) -> dict:
    base = SUBJECTS / code
    facts_path = base / "_study_facts.json"
    deep_path = base / "_deep_notes.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    deep = json.loads(deep_path.read_text(encoding="utf-8")) if deep_path.exists() else {}

    replaced = 0
    kept_ok = 0
    still_weak = 0
    total_fc = 0

    for mod in facts.get("modules") or []:
        for topic in mod.get("topics") or []:
            tid = topic.get("id") or ""
            title = topic.get("title") or tid
            pack = deep.get(tid) or {}
            new_cards = cards_from_deep(title, tid, pack)

            if new_cards:
                topic["flashcards"] = new_cards
                replaced += 1
            else:
                # Filter out weak cards; keep any solid definition cards
                cleaned = []
                for c in topic.get("flashcards") or []:
                    if (c.get("front") or "").startswith("Exam focus:"):
                        continue
                    if is_weak_back(c.get("back") or ""):
                        continue
                    cleaned.append(c)
                if not cleaned:
                    # last resort: one honest card from title using first deep root note if any
                    root = deep.get(f"m{mod.get('id')}_root") or {}
                    terms = root.get("terms") or []
                    match = next(
                        (t for t in terms if title.lower() in (t.get("t") or "").lower()
                         or (t.get("t") or "").lower() in title.lower()),
                        None,
                    )
                    if match and match.get("d"):
                        cleaned = [
                            {
                                "front": f"What is {title}?",
                                "back": match["d"],
                                "detail": tid,
                            }
                        ]
                    else:
                        cleaned = [
                            {
                                "front": f"What is {title}?",
                                "back": (
                                    f"{title} is a core syllabus topic in this module. "
                                    f"Recall its definition, when it is used, and one contrast with a related concept."
                                ),
                                "detail": tid,
                            }
                        ]
                        still_weak += 1
                else:
                    kept_ok += 1
                topic["flashcards"] = cleaned

            total_fc += len(topic.get("flashcards") or [])

    facts_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "code": code,
        "topics_from_deep": replaced,
        "topics_kept_filtered": kept_ok,
        "topics_still_weak": still_weak,
        "flashcards": total_fc,
    }


def audit(code: str) -> dict:
    facts = json.loads((SUBJECTS / code / "_study_facts.json").read_text(encoding="utf-8"))
    cards = [
        c
        for m in facts["modules"]
        for t in m["topics"]
        for c in (t.get("flashcards") or [])
    ]
    return {
        "code": code,
        "n": len(cards),
        "exam_focus": sum(1 for c in cards if (c.get("front") or "").startswith("Exam focus")),
        "placeholder": sum(1 for c in cards if "syllabus topic in this module" in (c.get("back") or "")),
        "define_prompt": sum(1 for c in cards if (c.get("back") or "").startswith("Define ")),
    }


def main() -> None:
    results = []
    for code in CODES:
        results.append(rebuild_subject(code))
    print("REBUILT")
    for r in results:
        print(r)
    print("AUDIT")
    for code in CODES:
        print(audit(code))
    # also report bs605 for comparison
    print("bs605", audit("bs605") if (SUBJECTS / "bs605" / "_study_facts.json").exists() else "n/a")


if __name__ == "__main__":
    main()
