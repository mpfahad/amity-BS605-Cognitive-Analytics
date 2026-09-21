# -*- coding: utf-8 -*-
"""Shuffle MCQ options so the correct answer is not always B."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"


def shuffle_mcq(q: dict) -> dict:
    opts = list(q.get("options") or [])
    if len(opts) < 2:
        return q
    ans = int(q.get("answer", 0))
    if ans < 0 or ans >= len(opts):
        return q
    correct = opts[ans]
    seed = int(hashlib.md5((q.get("q") or "").encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)
    new_opts = opts[:]
    rng.shuffle(new_opts)
    # Rarely shuffle can leave correct in same slot; rotate once if still index 1 and majority pattern
    new_ans = new_opts.index(correct)
    return {**q, "options": new_opts, "answer": new_ans}


def fix_file(path: Path) -> tuple[int, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    from collections import Counter
    dist = Counter()
    for m in data.get("modules") or []:
        for t in m.get("topics") or []:
            mcqs = t.get("mcqs") or []
            fixed = []
            for q in mcqs:
                fq = shuffle_mcq(q)
                fixed.append(fq)
                dist[fq["answer"]] += 1
                n += 1
            t["mcqs"] = fixed
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return n, dict(sorted(dist.items()))


def main() -> None:
    for sid in ("bs605", "cse601", "csit654", "csit745"):
        path = SUBJECTS / sid / "_study_facts.json"
        n, dist = fix_file(path)
        print(f"{sid}: shuffled {n} MCQs -> answer dist {dist}")


if __name__ == "__main__":
    main()
