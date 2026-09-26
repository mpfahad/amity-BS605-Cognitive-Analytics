"""Extract CSIT654 Network Security PDF into subjects/csit654/v3/source/."""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # type: ignore

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "subjects" / "csit654" / "Network Security and Cryptography  FINAL.pdf"
OUT = ROOT / "subjects" / "csit654" / "v3" / "source"


def extract_all(pdf: Path) -> dict:
    doc = fitz.open(pdf)
    pages = []
    for i in range(len(doc)):
        pages.append({"page": i + 1, "text": doc[i].get_text("text")})
    toc = doc.get_toc() or []
    outline = [{"level": t[0], "title": t[1], "page": t[2]} for t in toc]
    heading_guesses = []
    for p in pages:
        for line in p["text"].splitlines():
            s = line.strip()
            if re.match(r"^(\d+\.)+\d*\s*[:.]?\s+\S+", s) or re.match(
                r"^Module\s*[-–]?\s*[IVX0-9]+", s, re.I
            ):
                if 6 < len(s) < 160:
                    heading_guesses.append({"page": p["page"], "title": s})
    page_count = len(doc)
    doc.close()
    return {
        "pdf": pdf.name,
        "page_count": page_count,
        "outline": outline,
        "heading_guesses": heading_guesses,
        "pages": pages,
    }


def guess_module_ranges(heading_guesses: list[dict], page_count: int) -> dict:
    """Best-effort Module I–V page starts from heading guesses."""
    starts: dict[int, int] = {}
    for h in heading_guesses:
        t = h["title"]
        m = re.search(r"Module\s*[-–]?\s*([IVX1-5])\b", t, re.I)
        if not m:
            continue
        raw = m.group(1).upper()
        roman = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
        mid = roman.get(raw)
        if mid and mid not in starts:
            starts[mid] = h["page"]
    ranges = {}
    for mid in range(1, 6):
        lo = starts.get(mid)
        if not lo:
            continue
        hi = page_count
        for nxt in range(mid + 1, 6):
            if nxt in starts:
                hi = starts[nxt] - 1
                break
        ranges[mid] = (lo, hi)
    return ranges


def write_module_slices(data: dict, ranges: dict) -> None:
    by_page = {p["page"]: p["text"] for p in data["pages"]}
    for mid, (lo, hi) in ranges.items():
        chunks = []
        for page in range(lo, hi + 1):
            chunks.append(f"--- page {page} ---\n{by_page.get(page, '')}")
        (OUT / f"module_{mid}.txt").write_text("\n\n".join(chunks), encoding="utf-8")


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"PDF not found: {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {PDF.name} …")
    data = extract_all(PDF)
    ranges = guess_module_ranges(data["heading_guesses"], data["page_count"])
    data["module_ranges"] = {str(k): list(v) for k, v in ranges.items()}
    (OUT / "extracted_full.json").write_text(
        json.dumps(
            {
                "pdf": data["pdf"],
                "page_count": data["page_count"],
                "outline": data["outline"],
                "heading_guesses": data["heading_guesses"],
                "module_ranges": data["module_ranges"],
                "pages": data["pages"],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    meta = {
        "pdf": data["pdf"],
        "page_count": data["page_count"],
        "outline": data["outline"],
        "heading_guesses": data["heading_guesses"][:200],
        "module_ranges": data["module_ranges"],
    }
    (OUT / "outline.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_module_slices(data, ranges)
    print(f"  pages={data['page_count']} ranges={ranges} -> {OUT}")


if __name__ == "__main__":
    main()
