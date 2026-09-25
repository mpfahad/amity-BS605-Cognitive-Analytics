"""Verify M4/M5 sourceQuotes appear in module extracts."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_pack(name: str):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def flatten_quotes(s: str) -> str:
    return (
        s.replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u25cf", "")
        .replace("\u2022", "")
    )


def check(module_txt: Path, concepts: dict) -> list[str]:
    src = norm(module_txt.read_text(encoding="utf-8"))
    src2 = flatten_quotes(src)
    fails = []
    for cid, c in sorted(concepts.items()):
        q = norm(c.get("sourceQuote", ""))
        if not q:
            fails.append(f"{cid} EMPTY")
            continue
        q2 = flatten_quotes(q)
        if q in src or q2 in src2:
            continue
        words = q.split()[:6]
        needle = " ".join(words[:4])
        i = src.lower().find(needle.lower())
        hint = src[i : i + 180] if i >= 0 else "(no needle)"
        fails.append(f"{cid} FAIL\n  QUOTE: {q}\n  HINT: {hint}")
    return fails


def main() -> None:
    m4 = load_pack("write_m4_pack.py")
    m5 = load_pack("write_m5_pack.py")
    draft = ROOT / "subjects/csit745/v2/data/draft"
    draft.mkdir(parents=True, exist_ok=True)
    f4 = check(ROOT / "subjects/csit745/v2/source/module_4.txt", m4.CONCEPTS)
    f5 = check(ROOT / "subjects/csit745/v2/source/module_5.txt", m5.CONCEPTS)
    (draft / "m4_quote_fails.txt").write_text("\n\n".join(f4) or "NONE", encoding="utf-8")
    (draft / "m5_quote_fails.txt").write_text("\n\n".join(f5) or "NONE", encoding="utf-8")
    print(f"M4 concepts {len(m4.CONCEPTS)} qs {len(m4.QUESTIONS)} fails {len(f4)}")
    print(f"M5 concepts {len(m5.CONCEPTS)} qs {len(m5.QUESTIONS)} fails {len(f5)}")


if __name__ == "__main__":
    main()
