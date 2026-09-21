# -*- coding: utf-8 -*-
"""Write handcrafted deep notes JSON for cse601, csit654, csit745 and rebuild check."""
from __future__ import annotations

import json
from pathlib import Path

from _handcraft_cse601_deep import CSE601
from _handcraft_csit654_deep import CSIT654
from _handcraft_csit745_deep import CSIT745

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"

PACKS = {
    "cse601": CSE601,
    "csit654": CSIT654,
    "csit745": CSIT745,
}


def main() -> None:
    for sid, data in PACKS.items():
        # sanity: every entry has terms/concepts/notes
        for k, v in data.items():
            assert "terms" in v and "concepts" in v and "notes" in v, k
            assert v["terms"], f"empty terms {sid} {k}"
        path = SUBJECTS / sid / "_deep_notes.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path} ({len(data)} entries)")


if __name__ == "__main__":
    main()
