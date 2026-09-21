"""Generate _study_facts.json + _module_maps.json + _lmr_notes.txt from PDF headings."""
from __future__ import annotations

import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "subjects"

META = {
    "cse601": {
        "course": "Data Structures and Algorithm Design (CSE601)",
        "title_short": "Data Structures & Algorithms",
        "pdf": "Data Structure and Algorithm F.pdf",
    },
    "csit654": {
        "course": "Network Security and Cryptography (CSIT654)",
        "title_short": "Network Security & Cryptography",
        "pdf": "Network Security and Cryptography  FINAL.pdf",
    },
    "csit745": {
        "course": "Research Methodology (CSIT745)",
        "title_short": "Research Methodology",
        "pdf": "Research Methodology  Final.pdf",
    },
}


def clean_title(s: str) -> str:
    s = s.replace("\t", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_id_title(raw: str) -> tuple[str | None, str]:
    raw = clean_title(raw)
    m = re.match(r"^(\d+(?:\.\d+)*)\s+(.+)$", raw)
    if not m:
        return None, raw
    return m.group(1), m.group(2).strip(" ·:-")


def module_of(tid: str) -> int:
    return int(tid.split(".")[0])


def find_snippet(pages: list[dict], title: str) -> str:
    key = title.lower()[:40]
    for p in pages:
        text = p.get("text") or ""
        low = text.lower()
        if key[:20] in low:
            # take a paragraph after the heading-ish line
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            for i, ln in enumerate(lines):
                if key[:18] in ln.lower() and i + 1 < len(lines):
                    chunk = " ".join(lines[i + 1 : i + 4])
                    chunk = re.sub(r"\s+", " ", chunk).strip()
                    if len(chunk) > 40:
                        return chunk[:420]
            # fallback: first long lines
            for ln in lines:
                if len(ln) > 60 and not re.match(r"^\d", ln):
                    return ln[:420]
    return ""


def build_subject(code: str) -> None:
    dest = ROOT / code
    outline = json.loads((dest / "_pdf_outline.json").read_text(encoding="utf-8"))
    extracted = json.loads((dest / "_extracted_pdf.json").read_text(encoding="utf-8"))
    pages = extracted.get("pages") or []
    meta = META[code]

    leaves: list[tuple[str, str]] = []
    parents: dict[str, str] = {}
    for h in outline.get("heading_guesses") or []:
        tid, title = parse_id_title(h["title"])
        if not tid:
            continue
        parts = tid.split(".")
        if len(parts) >= 3:
            leaves.append((tid, title))
        elif len(parts) == 2:
            parents[tid] = title

    # dedupe keep order
    seen = set()
    uniq = []
    for tid, title in leaves:
        if tid in seen:
            continue
        seen.add(tid)
        uniq.append((tid, title))
    leaves = uniq

    modules_map: dict[int, list] = defaultdict(list)
    for tid, title in leaves:
        modules_map[module_of(tid)].append((tid, title))

    modules_out = []
    maps_modules = []
    lmr_lines = []

    kinds = ["a", "b", "c"]
    for mid in sorted(modules_map.keys()):
        topics = []
        level_nodes = []
        for i, (tid, title) in enumerate(modules_map[mid]):
            snippet = find_snippet(pages, title) or f"Key SLM topic: {title}. Review definitions, steps, and one worked example from the study PDF."
            parent = ".".join(tid.split(".")[:2])
            parent_title = parents.get(parent, f"Unit {parent}")
            fc = [
                {
                    "front": f"What is the core idea of {title}?",
                    "back": snippet if len(snippet) > 30 else f"{title}: study the SLM section carefully — definition, purpose, and exam-ready example.",
                    "detail": f"From {meta['course']} · {tid} · {parent_title}",
                }
            ]
            # second card for longer topics
            if i % 2 == 0:
                fc.append(
                    {
                        "front": f"Name one exam point for {title}.",
                        "back": f"Be able to define {title}, state when it is used, and contrast it with a related concept in {parent_title}.",
                    }
                )
            ans = min(1, len(title) % 4)
            options = [
                f"A definition-only topic with no applications",
                f"A core idea in {meta['title_short']}: {title}",
                f"Unrelated to Module {mid}",
                f"Only a programming language keyword",
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
            topics.append({"id": tid, "title": title, "flashcards": fc, "mcqs": [mcq]})
            level_nodes.append(
                {
                    "id": tid,
                    "title": title[:42],
                    "sub": parent_title[:36],
                    "kind": kinds[i % 3],
                    "topicId": tid,
                    "lmr": i < 3,
                }
            )
            if i < 3:
                lmr_lines.append(f"{len(lmr_lines)+1}. {tid} {title} — Module {mid} priority.")

        # group nodes into up to 3 levels for map readability
        chunk = max(1, (len(level_nodes) + 2) // 3)
        levels = []
        for start in range(0, len(level_nodes), chunk):
            group = level_nodes[start : start + chunk]
            if not group:
                continue
            levels.append({"heading": f"Module {mid} · part {len(levels)+1}", "nodes": group})

        modules_out.append(
            {
                "id": mid,
                "title": f"Module {mid}",
                "topics": topics,
            }
        )
        maps_modules.append(
            {
                "id": mid,
                "title": f"Module {mid}",
                "weight": "high" if mid == 1 else "standard",
                "root": {
                    "id": f"m{mid}_root",
                    "title": f"Module {mid}",
                    "sub": meta["title_short"],
                    "kind": "root",
                    "path": f"{meta['course']} → Module {mid}",
                    "body": f"Study map for Module {mid} of {meta['course']}. Click a topic, then practise its MCQs.",
                    "points": ["Built from the SLM table of contents", "Orange LMR badges mark first-pass priorities"],
                },
                "levels": levels,
            }
        )

    facts = {"course": meta["course"], "modules": modules_out}
    maps = {"modules": maps_modules}
    (dest / "_study_facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    (dest / "_module_maps.json").write_text(json.dumps(maps, ensure_ascii=False, indent=2), encoding="utf-8")
    lmr = f"{meta['course']} — LMR priorities\n\n" + "\n".join(lmr_lines[:16]) + "\n"
    (dest / "_lmr_notes.txt").write_text(lmr, encoding="utf-8")
    n_fc = sum(len(t["flashcards"]) for m in modules_out for t in m["topics"])
    n_q = sum(len(t["mcqs"]) for m in modules_out for t in m["topics"])
    print(f"{code}: modules={len(modules_out)} topics={sum(len(m['topics']) for m in modules_out)} fc={n_fc} mcq={n_q}")


def main():
    for code in META:
        build_subject(code)


if __name__ == "__main__":
    main()
