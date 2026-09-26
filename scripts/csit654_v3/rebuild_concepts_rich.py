"""Handcraft denser original lessons for all 55 topics from deep notes + light PDF grounding.

Overwrites concepts.json. Prefer later merge of concepts_m1m2 / concepts_m3m5 if those exist.
Does not touch mcq_bank.json.
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

COMPARE_RULES = [
    (
        ("passive", "active"),
        [
            {
                "title": "Passive",
                "bullets": [
                    "Observes or collects information",
                    "Does not alter system resources",
                    "Hard to detect — prevention first",
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
        ],
    ),
    (
        ("stream", "block"),
        [
            {
                "title": "Stream cipher",
                "bullets": [
                    "Encrypts a continuous bit/byte stream",
                    "Often XOR with a keystream",
                    "Suits real-time / unknown-length traffic",
                ],
            },
            {
                "title": "Block cipher",
                "bullets": [
                    "Encrypts fixed-size blocks",
                    "Needs a mode of operation for long messages",
                    "Basis for DES/AES-style designs",
                ],
            },
        ],
    ),
    (
        ("confusion", "diffusion"),
        [
            {
                "title": "Confusion",
                "bullets": [
                    "Hide the key–ciphertext relationship",
                    "Usually substitution / nonlinear S-boxes",
                ],
            },
            {
                "title": "Diffusion",
                "bullets": [
                    "Spread plaintext influence across many ciphertext bits",
                    "Usually permutation / mixing layers",
                ],
            },
        ],
    ),
    (
        ("mac", "hash"),
        [
            {
                "title": "MAC",
                "bullets": [
                    "Uses a shared secret",
                    "Origin authentication + integrity",
                ],
            },
            {
                "title": "Hash / digest",
                "bullets": [
                    "No shared secret by itself",
                    "Fingerprint of data; used inside MAC/signatures",
                ],
            },
        ],
    ),
    (
        ("symmetric", "public"),
        [
            {
                "title": "Symmetric",
                "bullets": [
                    "Same key for encrypt/decrypt (or shared secret)",
                    "Fast bulk encryption",
                    "Key distribution is the hard part",
                ],
            },
            {
                "title": "Public-key",
                "bullets": [
                    "Key pair: public + private",
                    "Enables key exchange and signatures",
                    "Slower; often wraps symmetric keys",
                ],
            },
        ],
    ),
    (
        ("virus", "worm"),
        [
            {
                "title": "Virus",
                "bullets": [
                    "Needs a host file/program",
                    "Spreads when host is executed/shared",
                ],
            },
            {
                "title": "Worm",
                "bullets": [
                    "Self-propagating over the network",
                    "Does not need a user to open a host file",
                ],
            },
        ],
    ),
]


def pick_compare(blob: str):
    low = blob.lower()
    for keys, sides in COMPARE_RULES:
        if all(k in low for k in keys):
            return sides
    if "ecb" in low and "cbc" in low:
        return [
            {
                "title": "ECB",
                "bullets": [
                    "Independent blocks — identical plaintext → identical ciphertext",
                    "Leaks patterns; rarely used alone for real messages",
                ],
            },
            {
                "title": "CBC",
                "bullets": [
                    "Chains blocks with IV / previous ciphertext",
                    "Hides patterns; errors can propagate",
                ],
            },
        ]
    if "signature" in low and "encrypt" in low:
        return [
            {
                "title": "Digital signature",
                "bullets": [
                    "Integrity + authenticity + non-repudiation",
                    "Verify with public key",
                ],
            },
            {
                "title": "Encryption",
                "bullets": [
                    "Confidentiality of content",
                    "Decrypt with the matching secret/private key",
                ],
            },
        ]
    return None


def author(topic: dict, notes: dict) -> dict:
    tid = topic["id"]
    title = topic["title"]
    terms = notes.get("terms") or []
    concepts = notes.get("concepts") or []
    tips = notes.get("notes") or []
    blob = " ".join(
        [title]
        + [t.get("t", "") + " " + t.get("d", "") for t in terms]
        + concepts
        + tips
    )

    lead = concepts[0] if concepts else f"{title} is a core exam topic in this module."
    concept = (
        f"{lead} "
        + (
            concepts[1]
            if len(concepts) > 1
            else "Learn the definition, one crisp contrast, and the exam cue that appears in MCQs."
        )
    )

    how_parts = ["Key vocabulary:"]
    for t in terms[:6]:
        how_parts.append(f"- **{t['t']}** — {t['d']}")
    if concepts:
        how_parts.append("")
        how_parts.append("How it fits:")
        for c in concepts:
            how_parts.append(f"- {c}")

    example = next(
        (
            tip
            for tip in tips
            if any(w in tip.lower() for w in ("stem", "trap", "example", "scenario", "exam"))
        ),
        None,
    )
    if not example and terms:
        example = (
            f"Exam habit: define **{terms[0]['t']}** in one line, then give one contrast "
            f"or application from this topic."
        )

    remember = [n for n in tips if n][:5]
    if len(remember) < 3 and terms:
        remember.extend(f"Know {t['t']}: {t['d']}" for t in terms[: 3 - len(remember)])

    flash = [{"q": f"What is {t['t']}?", "a": t["d"]} for t in terms[:4]]
    for tip in tips:
        if "→" in tip or "->" in tip:
            flash.append({"q": re.split(r"→|->", tip)[0].strip(" ."), "a": tip})
        if len(flash) >= 5:
            break

    return {
        "id": tid,
        "title": title,
        "module": int(tid.split(".")[0]),
        "group": topic.get("group") or "",
        "lmr": bool(topic.get("lmr")),
        "tags": [t["t"] for t in terms[:5]],
        "learn": {
            "concept": concept.strip(),
            "howItWorks": "\n".join(how_parts),
            "example": example or f"Work a definition-plus-contrast for {title}.",
            "compare": pick_compare(blob),
            "remember": remember[:5],
        },
        "revise": {
            "bullets": (concepts[:5] or remember[:5]),
            "flash": flash[:5],
        },
        "related": [],
    }


def main() -> None:
    deep = json.loads(DEEP.read_text(encoding="utf-8"))
    curr = json.loads(CURR.read_text(encoding="utf-8"))
    concepts: dict[str, dict] = {}
    all_ids: list[str] = []
    for m in curr["modules"]:
        for t in m["topics"]:
            all_ids.append(t["id"])
            concepts[t["id"]] = author(t, deep.get(t["id"]) or {})

    by_mod: dict[int, list[str]] = {}
    for cid in all_ids:
        by_mod.setdefault(int(cid.split(".")[0]), []).append(cid)
    for ids in by_mod.values():
        for i, cid in enumerate(ids):
            related = []
            if i:
                related.append(ids[i - 1])
            if i + 1 < len(ids):
                related.append(ids[i + 1])
            concepts[cid]["related"] = related

    # keep flagship 1.1.1 upgrade if present in prior file
    if OUT.exists():
        prev = json.loads(OUT.read_text(encoding="utf-8")).get("concepts") or {}
        if prev.get("1.1.1", {}).get("learn", {}).get("compare"):
            # only keep if it looks hand-upgraded (has traffic analysis example)
            ex = prev["1.1.1"]["learn"].get("example") or ""
            if "traffic analysis" in ex.lower():
                concepts["1.1.1"] = prev["1.1.1"]

    OUT.write_text(json.dumps({"concepts": concepts}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} concepts={len(concepts)}")


if __name__ == "__main__":
    main()
