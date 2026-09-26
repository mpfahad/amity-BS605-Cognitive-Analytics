"""Merge handcrafted concept packs into concepts.json (prefer handcrafted)."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "subjects" / "csit654" / "v3" / "data"
BASE = DATA / "concepts.json"
PARTS = [
    DATA / "concepts_m1m2.json",
    DATA / "concepts_m3m5.json",
]


def main() -> None:
    base = {"concepts": {}}
    if BASE.exists():
        base = json.loads(BASE.read_text(encoding="utf-8"))
        if "concepts" not in base:
            base = {"concepts": base}
    concepts = dict(base.get("concepts") or {})
    for part in PARTS:
        if not part.exists():
            print(f"skip missing {part.name}")
            continue
        wrap = json.loads(part.read_text(encoding="utf-8"))
        chunk = wrap.get("concepts") or wrap
        concepts.update(chunk)
        print(f"merged {part.name}: {len(chunk)} concepts")
    BASE.write_text(
        json.dumps({"concepts": concepts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"total concepts={len(concepts)} -> {BASE}")


if __name__ == "__main__":
    main()
