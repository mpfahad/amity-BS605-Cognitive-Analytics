# -*- coding: utf-8 -*-
"""Apply hand-picked LMR flags from deep notes onto maps + _lmr_notes.txt.

Source of truth: subjects/<code>/_deep_notes.json entry["lmr"] == True
(CSE601: Live Class teacher weightage where available; else deferred).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"

# Subjects that use handcrafted deep notes as LMR source.
HANDPICKED = ("cse601", "csit654", "csit745")

LMR_NOTE_RE = re.compile(r"^\s*LMR(?:\s*\([^)]*\))?\s*:", re.I)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lmr_tip(entry: dict) -> str:
    notes = entry.get("notes") or []
    for n in notes:
        if LMR_NOTE_RE.search(str(n)):
            tip = LMR_NOTE_RE.sub("", str(n)).strip().rstrip(".")
            return tip
    # Fall back to first concept or term definition
    concepts = entry.get("concepts") or []
    if concepts:
        return str(concepts[0]).strip().rstrip(".")
    terms = entry.get("terms") or []
    if terms:
        t0 = terms[0]
        if isinstance(t0, dict):
            return f"{t0.get('t', '')}: {t0.get('d', '')}".strip().rstrip(".")
    return "Exam priority — define clearly and contrast with one neighbour."


def topic_title(maps: dict, topic_id: str) -> str:
    for mod in maps.get("modules") or []:
        for level in mod.get("levels") or []:
            for n in level.get("nodes") or []:
                tid = str(n.get("topicId") or n.get("id") or "")
                if tid == topic_id:
                    return n.get("title") or topic_id
        root = mod.get("root") or {}
        if str(root.get("id")) == topic_id:
            return root.get("title") or topic_id
    return topic_id


def apply_subject(code: str) -> dict:
    dest = SUBJECTS / code
    deep_path = dest / "_deep_notes.json"
    maps_path = dest / "_module_maps.json"
    if not deep_path.exists() or not maps_path.exists():
        raise SystemExit(f"Missing deep notes or maps for {code}")

    deep = load_json(deep_path)
    maps = load_json(maps_path)

    flagged = {
        k: v
        for k, v in deep.items()
        if isinstance(v, dict) and v.get("lmr") and not str(k).endswith("_root") and not str(k).startswith("m")
    }
    # Also allow ids like "1.1.1" only — skip module roots explicitly
    flagged = {
        k: v
        for k, v in deep.items()
        if isinstance(v, dict) and bool(v.get("lmr")) and re.match(r"^\d+(\.\d+)+$", str(k))
    }

    flagged_ids = set(flagged.keys())
    updated_nodes = 0
    for mod in maps.get("modules") or []:
        root = mod.get("root") or {}
        points = list(root.get("points") or [])
        new_points = []
        for p in points:
            if "first-pass" in p.lower() or "first 3" in p.lower() or "first-three" in p.lower():
                new_points.append("Orange LMR badges mark hand-picked exam priorities from study materials")
            else:
                new_points.append(p)
        if root:
            root["points"] = new_points
            mod["root"] = root
        for level in mod.get("levels") or []:
            for n in level.get("nodes") or []:
                tid = str(n.get("topicId") or n.get("id") or "")
                want = tid in flagged_ids
                if bool(n.get("lmr")) != want:
                    updated_nodes += 1
                n["lmr"] = want

    save_json(maps_path, maps)

    # Ordered LMR list by module then topic id
    def sort_key(tid: str):
        parts = []
        for p in tid.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(p)
        return parts

    lines = [f"{code.upper()} — LMR priorities (live-class teacher weightage + study materials)", ""]
    for i, tid in enumerate(sorted(flagged_ids, key=sort_key), 1):
        title = topic_title(maps, tid)
        tip = lmr_tip(flagged[tid])
        lines.append(f"{i}. {tid} {title} — {tip}.")
    lmr_path = dest / "_lmr_notes.txt"
    lmr_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "code": code,
        "flagged": len(flagged_ids),
        "map_nodes_changed": updated_nodes,
        "ids": sorted(flagged_ids, key=sort_key),
    }


def main() -> None:
    for code in HANDPICKED:
        info = apply_subject(code)
        print(
            f"{info['code']}: LMR topics={info['flagged']} "
            f"map_flags_updated~={info['map_nodes_changed']}"
        )
        print("  " + ", ".join(info["ids"]))


if __name__ == "__main__":
    main()
