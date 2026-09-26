"""Merge handcrafted extra MCQs into mcq_bank.json without touching Amigo rows."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "subjects" / "csit654" / "v3" / "data"
BANK = DATA / "mcq_bank.json"
PARTS = [DATA / "extra_mcq_m1m2.json", DATA / "extra_mcq_m3m5.json"]
COV = DATA / "coverage.json"


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    questions = list(bank.get("questions") or [])
    # Drop prior handcrafted extras so re-merge is idempotent
    questions = [q for q in questions if q.get("source") != "handcrafted"]
    existing_ids = {q["id"] for q in questions}

    added = 0
    for part in PARTS:
        if not part.exists():
            print(f"skip missing {part.name}")
            continue
        wrap = json.loads(part.read_text(encoding="utf-8"))
        chunk = wrap.get("questions") or []
        for q in chunk:
            assert q.get("source") == "handcrafted", q.get("id")
            assert len(q.get("options") or []) == 4, q.get("id")
            assert q.get("correct") in (0, 1, 2, 3), q.get("id")
            if q["id"] in existing_ids:
                continue
            questions.append(q)
            existing_ids.add(q["id"])
            added += 1
        print(f"from {part.name}: {len(chunk)} rows")

    bank["questions"] = questions
    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")

    by_src = Counter(q.get("source") for q in questions)
    by_mod = Counter(q.get("module") for q in questions)
    by_concept = Counter(q.get("conceptId") for q in questions)
    thin = [cid for cid, n in sorted(by_concept.items()) if n < 4]
    cov = {
        "total": len(questions),
        "bySource": dict(by_src),
        "byModule": {str(k): v for k, v in sorted(by_mod.items())},
        "handcraftedAdded": added,
        "conceptsBelow4": thin,
        "note": "Amigo topic rows preserved; handcrafted extras tagged source=handcrafted",
    }
    if COV.exists():
        prev = json.loads(COV.read_text(encoding="utf-8"))
        prev.update(cov)
        COV.write_text(json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        COV.write_text(json.dumps(cov, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"bank total={len(questions)} added={added} thin_concepts={thin}")


if __name__ == "__main__":
    main()
