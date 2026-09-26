"""Convert deep_notes + PDF/module grounding into LMS lesson concepts (original wording).

Does NOT touch mcq_bank.json. Prefer Amigo bank for practice; lessons are rewritten study prose.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEEP = ROOT / "subjects" / "csit654" / "_deep_notes.json"
CURR = ROOT / "subjects" / "csit654" / "v3" / "data" / "curriculum.json"
OUT = ROOT / "subjects" / "csit654" / "v3" / "data" / "concepts.json"
SRC = ROOT / "subjects" / "csit654" / "v3" / "source"


def load_module_text(mid: int) -> str:
    p = SRC / f"module_{mid}.txt"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def section_snippet(text: str, section: str, maxlen: int = 900) -> str:
    """Pull a short grounded snippet after a section heading (for authoring aid only)."""
    pat = re.compile(rf"{re.escape(section)}\s*[^\n]{{0,80}}\n(.{{0,{maxlen}}})", re.S)
    m = pat.search(text)
    if not m:
        # looser: first line containing section id
        for m2 in re.finditer(rf"(?m)^.*{re.escape(section)}.*$", text):
            start = m2.start()
            return text[start : start + maxlen]
        return ""
    return (m.group(0) or "")[:maxlen]


def rewrite_from_notes(topic: dict, notes: dict, snippet: str) -> dict:
    """Author original Learn/Revise blocks from deep notes (+ optional SLM grounding)."""
    tid = topic["id"]
    title = topic["title"]
    terms = notes.get("terms") or []
    concepts = notes.get("concepts") or []
    tips = notes.get("notes") or []

    term_lines = [f"**{t['t']}** — {t['d']}" for t in terms[:6] if t.get("t") and t.get("d")]
    concept_para = " ".join(concepts[:3]) if concepts else f"{title} is a core topic in this module."
    remember = [n for n in tips if n][:5]
    if not remember and terms:
        remember = [f"Know: {t['t']} — {t['d']}" for t in terms[:3]]

    # Build a compare block when notes suggest a contrast
    compare = None
    joined = " ".join(concepts + tips).lower()
    if "passive" in joined and "active" in joined:
        compare = [
            {
                "title": "Passive",
                "bullets": [
                    "Observes or collects information",
                    "Does not alter system resources",
                    "Hard to detect; focus on prevention",
                ],
            },
            {
                "title": "Active",
                "bullets": [
                    "Modifies, fabricates, replays, or interrupts",
                    "Changes behaviour or availability",
                    "Detection and recovery matter",
                ],
            },
        ]
    elif "stream" in joined and "block" in joined:
        compare = [
            {
                "title": "Stream cipher",
                "bullets": [
                    "Encrypts bit/byte stream continuously",
                    "Often XOR with keystream",
                    "Good for real-time / unknown length",
                ],
            },
            {
                "title": "Block cipher",
                "bullets": [
                    "Encrypts fixed-size blocks",
                    "Needs a mode of operation for longer messages",
                    "Foundation for DES/AES-style designs",
                ],
            },
        ]
    elif "confusion" in joined and "diffusion" in joined:
        compare = [
            {
                "title": "Confusion",
                "bullets": [
                    "Hide the relationship between key and ciphertext",
                    "Typically via substitution / nonlinear S-boxes",
                ],
            },
            {
                "title": "Diffusion",
                "bullets": [
                    "Spread plaintext influence across many ciphertext bits",
                    "Typically via permutation / mixing layers",
                ],
            },
        ]
    elif "mac" in joined and ("hash" in joined or "digest" in joined):
        compare = [
            {
                "title": "MAC",
                "bullets": [
                    "Uses a shared secret key",
                    "Provides origin authentication + integrity",
                ],
            },
            {
                "title": "Hash / digest",
                "bullets": [
                    "No shared secret by itself",
                    "Fingerprint of data; often used inside MAC/signatures",
                ],
            },
        ]

    how_bits = []
    if term_lines:
        how_bits.append("Key vocabulary:")
        how_bits.extend(f"- {line}" for line in term_lines)
    if concepts[1:]:
        how_bits.append("")
        how_bits.append("How the pieces fit:")
        how_bits.extend(f"- {c}" for c in concepts)

    example = None
    for tip in tips:
        if any(w in tip.lower() for w in ("stem", "example", "scenario", "trap")):
            example = tip
            break
    if not example and terms:
        example = f"Exam habit: define {terms[0]['t']} in one line, then give one contrast or application."

    flash = []
    for t in terms[:4]:
        flash.append({"q": f"What is {t['t']}?", "a": t["d"]})
    for tip in tips[:2]:
        if "→" in tip or "->" in tip:
            flash.append({"q": tip.split("→")[0].split("->")[0].strip(), "a": tip})

    # Original prose — never paste long SLM verbatim
    concept_text = concept_para
    if snippet and len(snippet) > 80:
        # lightly ground without copying: mention topics present, keep our wording
        concept_text = (
            f"{concept_para} In the study material this section sits under the module’s "
            f"ordered topics and builds the definitions you need for later algorithms and protocols."
        )

    return {
        "id": tid,
        "title": title,
        "module": int(tid.split(".")[0]),
        "group": topic.get("group") or "",
        "lmr": bool(topic.get("lmr")),
        "tags": [t["t"] for t in terms[:5]],
        "learn": {
            "concept": concept_text,
            "howItWorks": "\n".join(how_bits) if how_bits else concept_text,
            "example": example or f"Work a short definition-plus-contrast for {title}.",
            "compare": compare,
            "remember": remember,
        },
        "revise": {
            "bullets": concepts[:5] or remember[:4],
            "flash": flash[:6],
        },
        "related": [],
    }


def main() -> None:
    deep = json.loads(DEEP.read_text(encoding="utf-8"))
    curr = json.loads(CURR.read_text(encoding="utf-8"))
    module_text = {m["id"]: load_module_text(m["id"]) for m in curr["modules"]}

    concepts: dict[str, dict] = {}
    all_ids: list[str] = []
    for m in curr["modules"]:
        for t in m["topics"]:
            all_ids.append(t["id"])
            notes = deep.get(t["id"]) or {}
            snip = section_snippet(module_text[m["id"]], t["id"])
            concepts[t["id"]] = rewrite_from_notes(t, notes, snip)

    # related: neighbours within module
    by_mod: dict[int, list[str]] = {}
    for cid in all_ids:
        by_mod.setdefault(int(cid.split(".")[0]), []).append(cid)
    for mid, ids in by_mod.items():
        for i, cid in enumerate(ids):
            related = []
            if i:
                related.append(ids[i - 1])
            if i + 1 < len(ids):
                related.append(ids[i + 1])
            concepts[cid]["related"] = related

    OUT.write_text(
        json.dumps({"concepts": concepts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} concepts={len(concepts)}")


if __name__ == "__main__":
    main()
