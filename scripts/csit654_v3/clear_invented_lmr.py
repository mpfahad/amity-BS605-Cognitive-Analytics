"""Clear invented LMR badges for CSIT654 — no live-class LMR signal.

Per EXAM-CURATION-GUIDE: never invent weightage. If no teacher signal, leave unmarked.
The previous 15 flags matched first-3-per-module pattern (fake LMR).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUB = ROOT / "subjects" / "csit654"
TIP_PREFIX = re.compile(r"^LMR:\s*", re.I)


def scrub_tip(s: str) -> str:
    return TIP_PREFIX.sub("", s.strip()) if isinstance(s, str) else s


def scrub_concept(c: dict) -> None:
    c["lmr"] = False
    learn = c.get("learn") or {}
    if isinstance(learn.get("remember"), list):
        learn["remember"] = [scrub_tip(x) for x in learn["remember"]]
    revise = c.get("revise") or {}
    if isinstance(revise.get("bullets"), list):
        revise["bullets"] = [scrub_tip(x) for x in revise["bullets"]]


def main() -> None:
    cleared: dict[str, int] = {}

    for name in ("concepts.json", "concepts_m1m2.json", "concepts_m3m5.json"):
        path = SUB / "v3" / "data" / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        concepts = data["concepts"]
        n = sum(1 for c in concepts.values() if c.get("lmr"))
        for c in concepts.values():
            scrub_concept(c)
        path.write_text(
            json.dumps({"concepts": concepts}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        cleared[name] = n

    cur_path = SUB / "v3" / "data" / "curriculum.json"
    cur = json.loads(cur_path.read_text(encoding="utf-8"))
    n = 0
    for m in cur["modules"]:
        for t in m.get("topics", []):
            if t.get("lmr"):
                n += 1
            t["lmr"] = False
    cur_path.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
    cleared["curriculum.json"] = n

    maps_path = SUB / "_module_maps.json"
    maps = json.loads(maps_path.read_text(encoding="utf-8"))
    n = 0
    for m in maps["modules"]:
        # drop LMR wording from map root points
        root = m.get("root") or {}
        if isinstance(root.get("points"), list):
            root["points"] = [
                p
                for p in root["points"]
                if "LMR" not in p and "Orange" not in p
            ]
        for level in m.get("levels", []):
            for node in level.get("nodes", []):
                if node.get("lmr"):
                    n += 1
                node["lmr"] = False
    maps_path.write_text(json.dumps(maps, ensure_ascii=False, indent=2), encoding="utf-8")
    cleared["_module_maps.json"] = n

    deep_path = SUB / "_deep_notes.json"
    deep = json.loads(deep_path.read_text(encoding="utf-8"))
    n = 0
    for _k, v in deep.items():
        if not isinstance(v, dict) or "lmr" not in v:
            continue
        if v.get("lmr"):
            n += 1
        v["lmr"] = False
        if isinstance(v.get("notes"), list):
            v["notes"] = [scrub_tip(x) if isinstance(x, str) else x for x in v["notes"]]
    deep_path.write_text(json.dumps(deep, ensure_ascii=False, indent=2), encoding="utf-8")
    cleared["_deep_notes.json"] = n

    (SUB / "_lmr_notes.txt").write_text(
        "CSIT654 — LMR status\n"
        "\n"
        "No live-class teacher weightage is available for this subject yet.\n"
        "Per exam curation policy: do not invent LMR badges from outline order\n"
        "(e.g. first-three topics per module).\n"
        "\n"
        "LMR topic list: (empty — unmarked until a live class names exam priorities)\n",
        encoding="utf-8",
    )

    policy_path = SUB / "_exam_policy.json"
    policy = {
        "subject": "csit654",
        "lmr_source": "none",
        "lmr_topic_ids": [],
        "note": "No live-class LMR signal. Badges left unmarked intentionally.",
        "quiz_skip_topics": [],
    }
    if policy_path.exists():
        try:
            prev = json.loads(policy_path.read_text(encoding="utf-8"))
            if isinstance(prev, dict):
                prev.update(
                    {
                        "lmr_source": "none",
                        "lmr_topic_ids": [],
                        "note": policy["note"],
                    }
                )
                policy = prev
        except json.JSONDecodeError:
            pass
    policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Cleared LMR flags (were invented first-3-per-module):")
    for k, v in cleared.items():
        print(f"  {k}: {v} -> 0")


if __name__ == "__main__":
    main()
