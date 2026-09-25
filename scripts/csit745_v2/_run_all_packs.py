"""Reset data shells and run M1–M5 packs in order."""
from __future__ import annotations

import json
import runpy
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
DATA = SCRIPTS.parents[1] / "subjects" / "csit745" / "v2" / "data"


def reset() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "knowledge_tree.json").write_text(
        json.dumps(
            {"subject": "csit745", "title": "Research Methodology", "modules": []},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (DATA / "concepts.json").write_text(
        json.dumps({"concepts": {}}, indent=2) + "\n", encoding="utf-8"
    )
    (DATA / "mcq_bank.json").write_text(
        json.dumps({"questions": []}, indent=2) + "\n", encoding="utf-8"
    )
    (DATA / "coverage.json").write_text(
        json.dumps(
            {
                "subject": "csit745",
                "modules": {},
                "practiceMode": "whole_subject_shuffle",
                "notes": "Practice draws from the full bank across all modules; never module-locked.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    reset()
    for name in [
        "write_m1_pack.py",
        "write_m2_pack.py",
        "write_m3_pack.py",
        "write_m4_pack.py",
        "write_m5_pack.py",
    ]:
        print("RUN", name)
        runpy.run_path(str(SCRIPTS / name), run_name="__main__")

    concepts = json.loads((DATA / "concepts.json").read_text(encoding="utf-8"))["concepts"]
    questions = json.loads((DATA / "mcq_bank.json").read_text(encoding="utf-8"))["questions"]
    tree = json.loads((DATA / "knowledge_tree.json").read_text(encoding="utf-8"))
    prefixed = [k for k in concepts if k.startswith("m")]
    missing = [q["id"] for q in questions if q["conceptId"] not in concepts]
    print("FINAL concepts", len(concepts), "questions", len(questions))
    print("tree modules", [m["id"] for m in tree["modules"]])
    print("prefixed leftovers", prefixed)
    print("q missing concepts", len(missing), missing[:5])
    print("concepts by module", Counter(v["module"] for v in concepts.values()))
    print("questions by module", Counter(q["module"] for q in questions))


if __name__ == "__main__":
    main()
