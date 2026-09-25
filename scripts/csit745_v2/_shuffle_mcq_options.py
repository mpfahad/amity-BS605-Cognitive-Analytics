"""Shuffle MCQ option order so correct answers are not stuck on index 1 (B)."""
from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "subjects" / "csit745" / "v2" / "data"
BANK = DATA / "mcq_bank.json"


def shuffle_question(q: dict) -> dict:
    opts = list(q["options"])
    correct = int(q["correct"])
    pairs = list(enumerate(opts))
    # deterministic per question id
    seed = int(hashlib.sha256(q["id"].encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    rng.shuffle(pairs)
    new_opts = [p[1] for p in pairs]
    new_correct = next(i for i, (old_i, _) in enumerate(pairs) if old_i == correct)
    out = dict(q)
    out["options"] = new_opts
    out["correct"] = new_correct
    return out


def main() -> None:
    doc = json.loads(BANK.read_text(encoding="utf-8"))
    qs = [shuffle_question(q) for q in doc["questions"]]
    # verify answers still match original text
    old = {q["id"]: q for q in doc["questions"]}
    for q in qs:
        o = old[q["id"]]
        assert q["options"][q["correct"]] == o["options"][o["correct"]]
    doc["questions"] = qs
    BANK.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hist = Counter(q["correct"] for q in qs)
    print("shuffled", len(qs), "correct dist", dict(sorted(hist.items())))


if __name__ == "__main__":
    main()
