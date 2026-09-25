"""Normalize all module packs to syllabus concept IDs and re-merge in order."""
from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
DATA = ROOT / "subjects" / "csit745" / "v2" / "data"


def normalize_file(path: Path) -> None:
    s = path.read_text(encoding="utf-8")
    out = []
    i = 0
    while i < len(s):
        m = re.match(r'"m([1-5])-([1-5](?:\.\d+){1,2})"', s[i:])
        if m:
            token_end = i + m.end()
            # keep question ids that contain -q
            # look at full quoted token
            end = s.find('"', i + 1)
            token = s[i + 1 : end]
            if "-q" in token or re.search(r"-q\d", token) or token.endswith("-a") or token.endswith("-b") or token.endswith("-c"):
                # question id like m4-4.1.1-q1 or m5-5.1.1-a — keep
                out.append(s[i : end + 1])
                i = end + 1
                continue
            # concept id m1-1.1.1 -> 1.1.1
            parts = token.split("-", 1)
            if len(parts) == 2 and re.match(r"[1-5](?:\.\d+){1,2}$", parts[1]):
                out.append('"' + parts[1] + '"')
                i = end + 1
                continue
        out.append(s[i])
        i += 1
    path.write_text("".join(out), encoding="utf-8")
    print("normalized", path.name)


def main() -> None:
    for name in [
        "write_m1_pack.py",
        "write_m2_pack.py",
        "write_m3_pack.py",
        "write_m4_pack.py",
        "write_m5_pack.py",
    ]:
        normalize_file(SCRIPTS / name)

    # reset data shells
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
    prefixed = [k for k in concepts if k.startswith("m")]
    missing = [q["id"] for q in questions if q["conceptId"] not in concepts]
    print("FINAL concepts", len(concepts), "questions", len(questions))
    print("prefixed concept leftovers", prefixed)
    print("missing concept refs", missing[:10], "count", len(missing))
    from collections import Counter

    print("by module concepts", Counter(v["module"] for v in concepts.values()))
    print("by module questions", Counter(q["module"] for q in questions))


if __name__ == "__main__":
    main()
