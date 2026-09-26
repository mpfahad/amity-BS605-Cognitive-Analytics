"""Map each CSIT654 concept to its first PDF body page; write data/pdf_pages.json."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
SUB = ROOT / "subjects" / "csit654"
DATA = SUB / "v3" / "data"
SRC = SUB / "v3" / "source"
PDF_NAME = "Network Security and Cryptography  FINAL.pdf"
PDF_SRC = SUB / PDF_NAME
SLM_COPY = SRC / "slm.pdf"
VIEWER_FILE = "../source/slm.pdf"
PDF_HREF = "../../" + quote(PDF_NAME)


def main() -> None:
    if PDF_SRC.exists():
        SRC.mkdir(parents=True, exist_ok=True)
        if not SLM_COPY.exists() or SLM_COPY.stat().st_size != PDF_SRC.stat().st_size:
            shutil.copy2(PDF_SRC, SLM_COPY)
            print(f"copied SLM -> {SLM_COPY}")

    pages = json.loads((SRC / "extracted_full.json").read_text(encoding="utf-8"))["pages"]
    curr = json.loads((DATA / "curriculum.json").read_text(encoding="utf-8"))
    ids = [t["id"] for m in curr["modules"] for t in m["topics"]]

    by_concept: dict[str, int] = {}
    for cid in ids:
        pat = re.compile(rf"(?m)^\s*{re.escape(cid)}\b")
        for p in pages:
            if p["page"] <= 5:
                continue
            if pat.search(p["text"]):
                by_concept[cid] = p["page"]
                break
        if cid not in by_concept:
            raise SystemExit(f"No page for {cid}")

    by_module = {
        str(m["id"]): by_concept[m["topics"][0]["id"]] for m in curr["modules"]
    }

    payload = {
        "pdfFile": PDF_NAME,
        "viewerFile": VIEWER_FILE,
        "pdfHrefFromLms": PDF_HREF,
        "note": "Open via lms/pdf-viewer.html (PDF.js). Direct #page= blanks under python http.server (no Range).",
        "byConcept": by_concept,
        "byModule": by_module,
    }
    (DATA / "pdf_pages.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    concepts_path = DATA / "concepts.json"
    wrap = json.loads(concepts_path.read_text(encoding="utf-8"))
    for cid, c in wrap["concepts"].items():
        if cid in by_concept:
            c["pdfPage"] = by_concept[cid]
    concepts_path.write_text(json.dumps(wrap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"concepts={len(by_concept)} viewer={VIEWER_FILE}")


if __name__ == "__main__":
    main()
