"""CSIT654 v3 — assemble keyed mcq_bank from Amigo scrapes + SLM keys.

Usage:
  python scripts/csit654_v3/assemble_bank.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "subjects" / "csit654" / "v3"
AMIGO = V3 / "source" / "amigo"
OUT = V3 / "data"


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_option(text: str) -> str:
    t = " ".join((text or "").split())
    # strip leading a. / b) labels
    if len(t) >= 2 and t[0].lower() in "abcd" and t[1] in ".)":
        t = t[2:].strip()
    return t


def questions_from_scrape(scrape: dict, meta: dict) -> list[dict]:
    out = []
    cmid = str(meta["cmid"])
    source = meta["type"]
    prefix = "t" if source == "topic" else "r"
    for q in scrape.get("questions") or []:
        opts = [normalize_option(o) for o in q.get("options") or []]
        opts = [o for o in opts if o and o.lower() not in {"clear my choice", "clear"}]
        stem = " ".join((q.get("stem") or "").split())
        if not stem or not opts:
            continue
        correct = q.get("correct")
        answer_source = q.get("answerSource")
        if correct is None and q.get("correctOptionText"):
            cot = normalize_option(q["correctOptionText"])
            for i, o in enumerate(opts):
                if o.lower() == cot.lower() or cot.lower() in o.lower() or o.lower() in cot.lower():
                    correct = i
                    answer_source = answer_source or "amigo_review"
                    break
        item = {
            "id": f"amigo-{prefix}-{cmid}-{q.get('no') or len(out)+1}",
            "module": meta.get("module"),
            "conceptId": meta.get("conceptId") or (f"re50-m{meta.get('module')}" if source == "re50" else None),
            "source": source,
            "cmid": cmid,
            "quizTitle": meta.get("title"),
            "stem": stem,
            "options": opts,
            "correct": correct,
            "explanation": q.get("explanation") or "",
            "answerSource": answer_source,
            "difficulty": "easy" if source == "topic" else "medium",
        }
        out.append(item)
    return out


def main():
    inv = load_json(AMIGO / "_inventory.json")
    keys = load_json(AMIGO / "_slm_keys.json") or {}
    key_by_id = {k["id"]: k for k in keys.get("questions", [])} if isinstance(keys, dict) else {}

    bank = []
    log = {"ok": [], "missing_file": [], "empty": [], "unkeyed": []}

    for meta in inv["quizzes"]:
        sub = "topic" if meta["type"] == "topic" else "re50"
        path = AMIGO / sub / f"{meta['cmid']}.json"
        scrape = load_json(path)
        if scrape is None:
            log["missing_file"].append(meta["cmid"])
            continue
        if scrape.get("status") in {"blocked", "no_attempt", "stub"}:
            log["empty"].append({"cmid": meta["cmid"], "status": scrape.get("status"), "note": scrape.get("note")})
            continue
        qs = questions_from_scrape(scrape, meta)
        if not qs:
            log["empty"].append(meta["cmid"])
            continue
        for q in qs:
            # apply SLM key override / fill
            k = key_by_id.get(q["id"])
            if k:
                if q.get("correct") is None and k.get("correct") is not None:
                    q["correct"] = k["correct"]
                    q["answerSource"] = "slm"
                if k.get("explanation"):
                    q["explanation"] = k["explanation"]
                    if q.get("answerSource") is None:
                        q["answerSource"] = "slm"
            if q.get("correct") is None:
                log["unkeyed"].append(q["id"])
            else:
                if not q.get("answerSource"):
                    q["answerSource"] = "amigo_review"
            bank.append(q)
        log["ok"].append(meta["cmid"])

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mcq_bank.json").write_text(
        json.dumps({"questions": bank}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    coverage = {
        "total": len(bank),
        "keyed": sum(1 for q in bank if q.get("correct") is not None),
        "unkeyed": [q["id"] for q in bank if q.get("correct") is None],
        "byModule": dict(Counter(str(q.get("module")) for q in bank)),
        "bySource": dict(Counter(q.get("source") for q in bank)),
        "byAnswerSource": dict(Counter(q.get("answerSource") or "none" for q in bank)),
        "scrapeLog": log,
    }
    (OUT / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (AMIGO / "_scrape_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"bank={len(bank)} keyed={coverage['keyed']} unkeyed={len(coverage['unkeyed'])}")
    print(f"missing_files={len(log['missing_file'])} empty={len(log['empty'])}")


if __name__ == "__main__":
    main()
