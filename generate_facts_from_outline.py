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

# Fallback one-liners when PDF snippet is TOC junk (CSE601-heavy; safe generics otherwise)
FALLBACK_DEFS: dict[str, str] = {
    "stack": "A Last-In-First-Out (LIFO) structure: insert and remove from the same end (the top) via push/pop.",
    "queue": "A First-In-First-Out (FIFO) structure: enqueue at the rear, dequeue from the front.",
    "linked list": "A collection of nodes linked by pointers, supporting dynamic insertion and deletion.",
    "double linked list": "A linked list where each node has next and previous pointers, allowing bidirectional traversal.",
    "doubly linked list": "A linked list where each node has next and previous pointers, allowing bidirectional traversal.",
    "tower of hanoi problem": "Classic recursion problem: move n disks between pegs with the rule that a larger disk never sits on a smaller one.",
    "evaluation of postfix expression": "Evaluate an expression in postfix (RPN) form using a stack: operands push; operators pop operands and push the result.",
    "algorithm and characteristics": "An algorithm is a finite, unambiguous sequence of steps to solve a problem; characteristics include input, output, finiteness, definiteness, and effectiveness.",
    "asymtotic notations": "Asymptotic notations (Big-O, Ω, Θ) describe growth rates of time/space as input size grows.",
    "asymptotic notations": "Asymptotic notations (Big-O, Ω, Θ) describe growth rates of time/space as input size grows.",
    "algorithm time complexity": "Time complexity estimates how running time grows with input size, often expressed with Big-O.",
    "master theorem": "A cookbook method to solve divide-and-conquer recurrences of the form T(n)=aT(n/b)+f(n).",
    "binary search tree": "A binary tree where left subtree keys are less than the node and right subtree keys are greater.",
    "avl tree": "A self-balancing BST that keeps the height difference of subtrees at most 1 via rotations.",
    "hashing": "Map keys to indices with a hash function for average-case near-constant lookup, insert, and delete.",
    "graph": "A set of vertices connected by edges; may be directed/undirected, weighted/unweighted.",
    "bfs": "Breadth-First Search explores neighbours level by level, typically using a queue.",
    "dfs": "Depth-First Search explores as far as possible along each branch, typically using a stack/recursion.",
    "sorting": "Arrange elements in a defined order; compare algorithms by time, space, and stability.",
    "research": "Systematic inquiry to discover, interpret, or revise facts and theories.",
    "hypothesis": "A testable proposed explanation for a phenomenon, guiding data collection and analysis.",
    "sampling": "Selecting a subset of a population so findings can be generalised with known limitations.",
    "cryptography": "Techniques for securing communication and data via encryption, integrity, and authentication.",
    "encryption": "Transform plaintext into ciphertext so only authorised parties can recover the original message.",
    "firewall": "A network security control that filters traffic between trust zones according to rules.",
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


def looks_like_toc(text: str) -> bool:
    """True if the snippet is mostly neighbouring outline headings, not a definition."""
    if not text:
        return True
    ids = re.findall(r"\b\d+(?:\.\d+){1,3}\b", text)
    if len(ids) >= 2:
        return True
    # bare list of Title Case headings with numbers
    if re.search(r"\d+\.\d+.*\d+\.\d+", text) and len(text) < 220:
        return True
    return False


def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def find_snippet(pages: list[dict], title: str) -> str:
    """Pull a real definition-like paragraph for title from extracted PDF text."""
    full = "\n".join((p.get("text") or "") for p in pages)
    title_clean = clean_title(title)
    # drop leading numbering if present in title
    title_clean = re.sub(r"^\d+(?:\.\d+)*\s+", "", title_clean).strip()
    if not title_clean:
        return ""

    # 1) Prefer "Title: definition..." (common in Amity notes)
    esc = re.escape(title_clean)
    patterns = [
        rf"(?is){esc}\s*[:\-–—]\s*([^\n]{{20,280}}(?:\n(?![A-Z][a-z]{{0,20}}\s*[:\-])[^\n]{{10,200}})*)",
        rf"(?is)\b{esc}\b[^\n]{{0,40}}?\n\s*([A-Z][^\n]{{40,320}})",
    ]
    for pat in patterns:
        m = re.search(pat, full)
        if m:
            chunk = normalize_spaces(m.group(1))
            chunk = re.sub(r"^[•\-–—\s]+", "", chunk)
            if not looks_like_toc(chunk) and len(chunk) > 35:
                return chunk[:420]

    # 2) Line containing title followed by definition words
    key = title_clean.lower()
    lines = [normalize_spaces(ln) for ln in full.splitlines() if ln.strip()]
    for i, ln in enumerate(lines):
        low = ln.lower()
        if key[:18].lower() in low and len(ln) > 50 and not looks_like_toc(ln):
            # skip pure heading lines that are only the title
            if low.strip() in (key, key + ":"):
                continue
            if looks_like_toc(ln):
                continue
            return ln[:420]
        if key[:18].lower() in low and i + 1 < len(lines):
            nxt = lines[i + 1]
            if len(nxt) > 40 and not looks_like_toc(nxt) and not re.match(r"^\d+\.\d+", nxt):
                return nxt[:420]

    # 3) Fallback dictionary
    fb = FALLBACK_DEFS.get(key.lower())
    if fb:
        return fb
    # try shorter key (first 2 words)
    parts = key.lower().split()
    for n in (3, 2, 1):
        if len(parts) >= n:
            fb = FALLBACK_DEFS.get(" ".join(parts[:n]))
            if fb:
                return fb
    return ""


def definition_for(title: str, pages: list[dict]) -> str:
    snippet = find_snippet(pages, title)
    if snippet and not looks_like_toc(snippet):
        return snippet
    fb = FALLBACK_DEFS.get(clean_title(title).lower())
    if fb:
        return fb
    return (
        f"{title}: a syllabus topic in this module — learn the definition, "
        f"when it is used, key operations/steps, and one contrast with a related concept."
    )


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
    toc_hits = 0
    good = 0
    for mid in sorted(modules_map.keys()):
        topics = []
        level_nodes = []
        for i, (tid, title) in enumerate(modules_map[mid]):
            definition = definition_for(title, pages)
            if looks_like_toc(definition):
                toc_hits += 1
            else:
                good += 1
            parent = ".".join(tid.split(".")[:2])
            parent_title = parents.get(parent, f"Unit {parent}")
            fc = [
                {
                    "front": f"What is {title}?",
                    "back": definition,
                    "detail": f"{tid} · {parent_title}",
                },
                {
                    "front": f"Exam focus: {title}",
                    "back": (
                        f"Define {title} in one line, name when/why it is used, "
                        f"and contrast it with one related idea under {parent_title}."
                    ),
                },
            ]
            options = [
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

        chunk = max(1, (len(level_nodes) + 2) // 3)
        levels = []
        for start in range(0, len(level_nodes), chunk):
            group = level_nodes[start : start + chunk]
            if not group:
                continue
            levels.append({"heading": f"Module {mid} · part {len(levels)+1}", "nodes": group})

        modules_out.append({"id": mid, "title": f"Module {mid}", "topics": topics})
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
                    "body": f"Study map for Module {mid} of {meta['course']}. Click a topic for Overview and Deep notes, then practise MCQs.",
                    "points": [
                        "Built from the SLM outline + PDF definitions where available",
                        "Orange LMR badges mark first-pass priorities",
                    ],
                },
                "levels": levels,
            }
        )

    facts = {"course": meta["course"], "modules": modules_out}
    maps = {"modules": maps_modules}
    (dest / "_study_facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (dest / "_module_maps.json").write_text(json.dumps(maps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lmr = f"{meta['course']} — LMR priorities\n\n" + "\n".join(lmr_lines[:16]) + "\n"
    (dest / "_lmr_notes.txt").write_text(lmr, encoding="utf-8")
    n_fc = sum(len(t["flashcards"]) for m in modules_out for t in m["topics"])
    n_q = sum(len(t["mcqs"]) for m in modules_out for t in m["topics"])
    print(
        f"{code}: modules={len(modules_out)} topics={sum(len(m['topics']) for m in modules_out)} "
        f"fc={n_fc} mcq={n_q} defs_ok≈{good} toc_rejected≈{toc_hits}"
    )


def main():
    for code in META:
        build_subject(code)


if __name__ == "__main__":
    main()
