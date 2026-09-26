import json
from pathlib import Path

inv = json.loads(Path("subjects/csit654/v3/source/amigo/_inventory.json").read_text(encoding="utf-8"))
outdir = Path("subjects/csit654/v3/source/amigo/re50")
outdir.mkdir(parents=True, exist_ok=True)
for q in inv["quizzes"]:
    if q["type"] != "re50":
        continue
    stub = {
        "cmid": q["cmid"],
        "title": q["title"],
        "module": q["module"],
        "status": "blocked",
        "note": "No Attempt/Continue/Re-attempt button; finished attempts show Review not permitted. Stems not scraped.",
        "expectedQuestions": 17,
        "questions": [],
    }
    (outdir / f"{q['cmid']}.json").write_text(json.dumps(stub, indent=2), encoding="utf-8")
    print("stub", q["cmid"])
