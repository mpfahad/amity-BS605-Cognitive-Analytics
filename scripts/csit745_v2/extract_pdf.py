"""Extract full CSIT745 Research Methodology PDF into subjects/csit745/v2/source/."""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # type: ignore

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "subjects" / "csit745" / "Research Methodology  Final.pdf"
OUT = ROOT / "subjects" / "csit745" / "v2" / "source"

# PDF page (1-based) ranges for each module body (TOC is pages 4-7).
MODULE_RANGES = {
    1: (8, 31),
    2: (32, 56),
    3: (57, 86),
    4: (87, 130),
    5: (131, 165),
}


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
                if 6 < len(s) < 140:
                    heading_guesses.append({"page": p["page"], "title": s})
    page_count = len(doc)
    doc.close()
    return {
        "pdf": pdf.name,
        "page_count": page_count,
        "outline": outline,
        "heading_guesses": heading_guesses,
        "module_ranges": MODULE_RANGES,
        "pages": pages,
    }


def write_module_slices(data: dict) -> None:
    by_page = {p["page"]: p["text"] for p in data["pages"]}
    for mid, (lo, hi) in MODULE_RANGES.items():
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
    (OUT / "extracted_full.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )
    meta = {
        "pdf": data["pdf"],
        "page_count": data["page_count"],
        "outline": data["outline"],
        "heading_guesses": data["heading_guesses"],
        "module_ranges": data["module_ranges"],
    }
    (OUT / "outline.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_module_slices(data)
    sample = "\n\n".join(
        f"--- page {p['page']} ---\n{p['text']}" for p in data["pages"][:12]
    )
    (OUT / "extract_sample.txt").write_text(sample, encoding="utf-8")
    print(
        f"  pages={data['page_count']} headings={len(data['heading_guesses'])} -> {OUT}"
    )


if __name__ == "__main__":
    main()
