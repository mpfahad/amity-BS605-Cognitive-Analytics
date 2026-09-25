"""Shared merge helpers for CSIT745 v2 module packs."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "subjects" / "csit745" / "v2" / "data"


def load_json(name: str, default):
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(name: str, obj) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def merge_module(
    *,
    module_id: str,
    module_title: str,
    tree_children: list,
    concepts: dict,
    questions: list,
    status: str = "approved",
) -> None:
    tree = load_json("knowledge_tree.json", {"subject": "csit745", "title": "Research Methodology", "modules": []})
    concepts_doc = load_json("concepts.json", {"concepts": {}})
    bank = load_json("mcq_bank.json", {"questions": []})
    coverage = load_json(
        "coverage.json",
        {"subject": "csit745", "modules": {}, "practiceMode": "whole_subject_shuffle"},
    )

    modules = [m for m in tree.get("modules", []) if m.get("id") != module_id]
    modules.append({"id": module_id, "title": module_title, "children": tree_children})
    modules.sort(key=lambda m: m["id"])
    tree["modules"] = modules

    concepts_doc.setdefault("concepts", {})
    # replace this module's concepts only
    for cid in list(concepts_doc["concepts"]):
        if concepts_doc["concepts"][cid].get("module") == int(module_id.lstrip("m")):
            if cid not in concepts:
                del concepts_doc["concepts"][cid]
    concepts_doc["concepts"].update(concepts)

    mid = int(module_id.lstrip("m"))
    kept = [q for q in bank.get("questions", []) if q.get("module") != mid]
    # de-dupe by id within new questions
    seen = set()
    fresh = []
    for q in questions:
        if q["id"] in seen:
            continue
        seen.add(q["id"])
        fresh.append(q)
    bank["questions"] = kept + fresh

    coverage.setdefault("modules", {})
    coverage["practiceMode"] = "whole_subject_shuffle"
    coverage["modules"][str(mid)] = {
        "status": status,
        "conceptIds": sorted(concepts.keys()),
        "questionCount": len(fresh),
    }

    save_json("knowledge_tree.json", tree)
    save_json("concepts.json", concepts_doc)
    save_json("mcq_bank.json", bank)
    save_json("coverage.json", coverage)
    print(f"Merged {module_id}: {len(concepts)} concepts, {len(fresh)} questions")
