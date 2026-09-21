"""Extract PDF text/outline for AMITY subjects using PyMuPDF."""
from __future__ import annotations
import json
import re
from pathlib import Path

import fitz

ROOT = Path(r"C:\Users\User\Projects\AMITY")
OUT = Path(r"C:\Users\User\Projects\amity-BS605-Cognitive-Analytics\subjects")

JOBS = [
    {
        "code": "cse601",
        "pdf": ROOT / "CSE601-Data-Structures-and-Algorithm-Design" / "materials" / "Data Structure and Algorithm F.pdf",
        "max_pages": 80,
    },
    {
        "code": "csit654",
        "pdf": ROOT / "CSIT654-Network-Security-and-Cryptography" / "materials" / "Network Security and Cryptography  FINAL.pdf",
        "max_pages": 80,
    },
    {
        "code": "csit745",
        "pdf": ROOT / "CSIT745-Research-Methodology" / "materials" / "Research Methodology  Final.pdf",
        "max_pages": 80,
    },
]


def extract(pdf: Path, max_pages: int) -> dict:
    doc = fitz.open(pdf)
    toc = doc.get_toc() or []
    pages = []
    n = min(len(doc), max_pages)
    for i in range(n):
        text = doc[i].get_text("text")
        pages.append({"page": i + 1, "text": text})
    # also grab last 5 pages for exam tips if long
    if len(doc) > max_pages:
        for i in range(max(max_pages, len(doc) - 5), len(doc)):
            pages.append({"page": i + 1, "text": doc[i].get_text("text")})
    outline = [{"level": t[0], "title": t[1], "page": t[2]} for t in toc]
    # fallback headings from first pages
    headings = []
    for p in pages[:30]:
        for line in p["text"].splitlines():
            s = line.strip()
            if re.match(r"^(\d+\.)+\d*\s+\S+", s) or re.match(r"^Module\s+\d+", s, re.I):
                if 8 < len(s) < 120:
                    headings.append({"page": p["page"], "title": s})
    doc.close()
    return {
        "pdf": pdf.name,
        "page_count": len(fitz.open(pdf)),
        "outline": outline[:200],
        "heading_guesses": headings[:120],
        "pages": pages,
    }


def main():
    for job in JOBS:
        dest = OUT / job["code"]
        dest.mkdir(parents=True, exist_ok=True)
        print(f"Extracting {job['code']} ...")
        data = extract(job["pdf"], job["max_pages"])
        # write slim meta without full pages for inspection
        meta = {
            "pdf": data["pdf"],
            "page_count": data["page_count"],
            "outline": data["outline"],
            "heading_guesses": data["heading_guesses"],
        }
        (dest / "_pdf_outline.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        # full extract for builder
        (dest / "_extracted_pdf.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        # also plain text sample
        sample = "\n\n".join(f"--- page {p['page']} ---\n{p['text']}" for p in data["pages"][:15])
        (dest / "_extract_sample.txt").write_text(sample, encoding="utf-8")
        print(f"  pages={data['page_count']} outline={len(data['outline'])} headings={len(data['heading_guesses'])}")


if __name__ == "__main__":
    main()
