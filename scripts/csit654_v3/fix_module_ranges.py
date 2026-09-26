"""Fix module_* .txt page ranges after TOC-confused extract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "subjects" / "csit654" / "v3" / "source"
RANGES = {1: (7, 43), 2: (44, 76), 3: (77, 95), 4: (96, 155), 5: (156, 189)}


def main() -> None:
    data = json.loads((SRC / "extracted_full.json").read_text(encoding="utf-8"))
    by = {p["page"]: p["text"] for p in data["pages"]}
    data["module_ranges"] = {str(k): list(v) for k, v in RANGES.items()}
    (SRC / "extracted_full.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )
    meta = json.loads((SRC / "outline.json").read_text(encoding="utf-8"))
    meta["module_ranges"] = data["module_ranges"]
    (SRC / "outline.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for mid, (lo, hi) in RANGES.items():
        chunks = [f"--- page {page} ---\n{by.get(page, '')}" for page in range(lo, hi + 1)]
        (SRC / f"module_{mid}.txt").write_text("\n\n".join(chunks), encoding="utf-8")
        print(mid, lo, hi, "chars", sum(len(by.get(p, "")) for p in range(lo, hi + 1)))


if __name__ == "__main__":
    main()
