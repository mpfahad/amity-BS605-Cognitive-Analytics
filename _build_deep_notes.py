"""One-shot: build subjects/bs605/_deep_notes.json from sample + study facts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BS = ROOT / "subjects" / "bs605"


def extract_m3_from_sample() -> dict:
    html = (BS / "module3-deep-notes-sample.html").read_text(encoding="utf-8")
    m = re.search(r"const NODES = (\{.*?\});\s*\n\s*const LEVELS", html, re.S)
    if not m:
        raise SystemExit("Could not find NODES in sample")
    js = m.group(1)
    tmp = ROOT / "_tmp_nodes.mjs"
    out_path = ROOT / "_tmp_m3_deep.json"
    tmp.write_text("export default " + js + ";\n", encoding="utf-8")
    import subprocess

    code = (
        "import n from './_tmp_nodes.mjs';"
        "import { writeFileSync } from 'fs';"
        "const out={};"
        "for (const [k,v] of Object.entries(n)) { if (v.deep) out[k]=v.deep; }"
        "writeFileSync('./_tmp_m3_deep.json', JSON.stringify(out), 'utf8');"
    )
    r = subprocess.run(
        ["node", "--input-type=module", "-e", code],
        cwd=ROOT,
        capture_output=True,
    )
    if r.returncode != 0:
        err = (r.stderr or r.stdout or b"").decode("utf-8", errors="replace")
        raise SystemExit(err)
    data = json.loads(out_path.read_text(encoding="utf-8"))
    tmp.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)
    return data


def clean_term_label(front: str) -> str:
    s = (front or "").strip()
    for prefix in (
        "What is ",
        "What are ",
        "What distinguishes ",
        "Define ",
        "Explain ",
        "List ",
        "Name ",
        "How do ",
        "How does ",
        "How should ",
        "Describe ",
        "Distinguish ",
        "Match ",
    ):
        if s.lower().startswith(prefix.lower()):
            s = s[len(prefix) :]
            break
    s = s.rstrip("?")
    if len(s) > 72:
        s = s[:69] + "…"
    return s[0].upper() + s[1:] if s else "Key point"


def synth_from_topic(topic: dict, denser: bool) -> dict:
    terms = []
    concepts = []
    notes = []
    cards = topic.get("flashcards") or []
    for c in cards:
        terms.append({"t": clean_term_label(c.get("front") or ""), "d": c.get("back") or ""})
        if c.get("detail"):
            notes.append(c["detail"])
    title = topic.get("title") or topic.get("id")
    concepts.append(f"Core topic: {title}.")
    if denser and cards:
        concepts.append("LMR focus: be able to define each term in one line and spot exam traps below.")
        for c in cards:
            front = (c.get("front") or "").rstrip("?")
            notes.append(f"Recall cue — {front}.")
        notes.append("Don’t confuse neighbouring topics that share similar vocabulary.")
    elif cards:
        notes.append("Skim Overview first, then flashcards for drill.")
    # de-dupe notes
    seen = set()
    uniq = []
    for n in notes:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return {"terms": terms, "concepts": concepts, "notes": uniq}


def main() -> None:
    facts = json.loads((BS / "_study_facts.json").read_text(encoding="utf-8"))
    maps = json.loads((BS / "_module_maps.json").read_text(encoding="utf-8"))
    lmr_ids = set()
    for mod in maps["modules"]:
        for level in mod["levels"]:
            for n in level["nodes"]:
                if n.get("lmr"):
                    lmr_ids.add(str(n.get("topicId") or n["id"]))

    m3 = extract_m3_from_sample()
    out: dict = {}

    # roots
    for mod in maps["modules"]:
        root = mod["root"]
        rid = root["id"]
        points = root.get("points") or []
        out[rid] = {
            "terms": [
                {"t": root["title"], "d": root.get("body") or ""},
            ],
            "concepts": points[:],
            "notes": ["Open topic cards for Terms · Concepts · Short notes."],
        }

    for mod in facts["modules"]:
        for topic in mod["topics"]:
            tid = str(topic["id"])
            if tid in m3:
                out[tid] = m3[tid]
            else:
                out[tid] = synth_from_topic(topic, denser=tid in lmr_ids)

    # keep m3 root from sample if present
    if "m3_root" in m3:
        out["m3_root"] = m3["m3_root"]

    path = BS / "_deep_notes.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path} with {len(out)} entries")
    print("LMR denser:", sorted(lmr_ids))


if __name__ == "__main__":
    main()
