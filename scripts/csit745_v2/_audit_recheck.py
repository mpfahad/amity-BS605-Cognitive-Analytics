"""Manual QA audit: concepts + MCQs vs module extracts for CSIT745 v2."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "subjects" / "csit745" / "v2" / "data"
SRC = ROOT / "subjects" / "csit745" / "v2" / "source"

concepts = json.loads((DATA / "concepts.json").read_text(encoding="utf-8"))["concepts"]
questions = json.loads((DATA / "mcq_bank.json").read_text(encoding="utf-8"))["questions"]
tree = json.loads((DATA / "knowledge_tree.json").read_text(encoding="utf-8"))
coverage = json.loads((DATA / "coverage.json").read_text(encoding="utf-8"))

extracts = {
    m: " ".join((SRC / f"module_{m}.txt").read_text(encoding="utf-8").split()).lower()
    for m in range(1, 6)
}

issues = []

# --- structure ---
print("=== STRUCTURE ===")
print("concepts by module:", Counter(c["module"] for c in concepts.values()))
print("questions by module:", Counter(q["module"] for q in questions))
print("coverage:", {k: v.get("status") for k, v in coverage.get("modules", {}).items()})
print("practiceMode:", coverage.get("practiceMode"))

leaf_ids = []

def walk(n):
    if n.get("conceptId"):
        leaf_ids.append(n["conceptId"])
    for ch in n.get("children") or []:
        walk(ch)

for m in tree["modules"]:
    for ch in m.get("children") or []:
        walk(ch)

missing_tree = [i for i in leaf_ids if i not in concepts]
orphan_q = [q["id"] for q in questions if q["conceptId"] not in concepts]
print("tree leaves", len(leaf_ids), "missing concepts", missing_tree)
print("orphan questions", len(orphan_q))

# expected leaf sets from syllabus
expected = {
    1: [f"1.1.{i}" for i in range(1, 4)]
    + [f"1.2.{i}" for i in range(1, 6)]
    + [f"1.3.{i}" for i in range(1, 6)]
    + [f"1.4.{i}" for i in range(1, 5)],
    2: [f"2.1.{i}" for i in range(1, 4)]
    + [f"2.2.{i}" for i in range(1, 4)]
    + [f"2.3.{i}" for i in range(1, 7)],
    3: [f"3.1.{i}" for i in range(1, 9)]
    + [f"3.2.{i}" for i in range(1, 9)]
    + [f"3.3.{i}" for i in range(1, 4)],
    4: [f"4.1.{i}" for i in range(1, 12)] + [f"4.2.{i}" for i in range(1, 12)],
    5: [f"5.1.{i}" for i in range(1, 10)]
    + [f"5.2.{i}" for i in range(1, 6)]
    + [f"5.3.{i}" for i in range(1, 6)]
    + [f"5.4.{i}" for i in range(1, 4)],
}

print("\n=== LEAF COVERAGE ===")
for mid, exp in expected.items():
    have = sorted(k for k, v in concepts.items() if v["module"] == mid)
    missing = [x for x in exp if x not in have]
    extra = [x for x in have if x not in exp]
    print(f"M{mid}: have {len(have)} expected {len(exp)} missing={missing} extra={extra}")
    if missing:
        issues.append(f"M{mid} missing leaves {missing}")

# --- concept quality ---
print("\n=== CONCEPT CHECKS ===")
junk_patterns = [
    r"neighbouring topic",
    r"a syllabus topic",
    r"core idea in research methodology",
    r"learn the definition, when it is used",
]
for cid, c in sorted(concepts.items()):
    mid = c["module"]
    src = extracts[mid]
    quick = (c.get("quick") or "").strip()
    if len(quick) < 40:
        issues.append(f"{cid}: weak quick ({len(quick)} chars)")
    if re.match(r"^\d+\.\d+", quick):
        issues.append(f"{cid}: quick looks like a heading id")
    for pat in junk_patterns:
        if re.search(pat, quick, re.I) or re.search(pat, " ".join(c.get("keyIdeas") or []), re.I):
            issues.append(f"{cid}: junk pattern {pat}")
    ideas = c.get("keyIdeas") or []
    if len(ideas) < 2:
        issues.append(f"{cid}: fewer than 2 keyIdeas")
    quote = " ".join((c.get("sourceQuote") or "").split()).lower()
    if quote:
        # allow first 40 chars match (encoding noise)
        head = quote[:50]
        if head not in src and quote[:30] not in src:
            # try without fancy punctuation
            head2 = re.sub(r"[^\w\s]", "", head)
            src2 = re.sub(r"[^\w\s]", "", src)
            if head2[:40] not in src2:
                issues.append(f"{cid}: sourceQuote not found in extract: {c.get('sourceQuote')[:70]!r}")
    else:
        issues.append(f"{cid}: missing sourceQuote")
    pages = c.get("pages") or []
    if not pages:
        issues.append(f"{cid}: missing pages")

# --- MCQ quality ---
print("\n=== MCQ CHECKS ===")
by_concept = defaultdict(list)
for q in questions:
    by_concept[q["conceptId"]].append(q)

for cid in concepts:
    qs = by_concept.get(cid, [])
    if len(qs) < 2:
        issues.append(f"{cid}: only {len(qs)} MCQs")

correct_hist = Counter()
for q in questions:
    opts = q.get("options") or []
    if len(opts) != 4:
        issues.append(f"{q['id']}: {len(opts)} options")
    corr = q.get("correct")
    if corr not in (0, 1, 2, 3):
        issues.append(f"{q['id']}: bad correct {corr}")
    else:
        correct_hist[corr] += 1
    stem = (q.get("stem") or "").strip()
    if len(stem) < 20:
        issues.append(f"{q['id']}: short stem {stem!r}")
    for pat in junk_patterns:
        if re.search(pat, stem, re.I) or re.search(pat, q.get("explanation") or "", re.I):
            issues.append(f"{q['id']}: junk pattern")
    # duplicate options
    norm = [re.sub(r"\s+", " ", o.strip().lower()) for o in opts]
    if len(set(norm)) < 4:
        issues.append(f"{q['id']}: duplicate options")
    if q["conceptId"] not in concepts:
        issues.append(f"{q['id']}: concept missing")
    # explanation should mention something substantive
    if len((q.get("explanation") or "").strip()) < 20:
        issues.append(f"{q['id']}: thin explanation")

print("correct-index distribution:", dict(sorted(correct_hist.items())))
# warn if one index dominates >45%
total = sum(correct_hist.values())
for k, v in correct_hist.items():
    pct = 100 * v / total
    if pct > 50:
        issues.append(f"correct index {k} is {pct:.0f}% of bank (possible bias)")

# review files
print("\n=== REVIEW FILES ===")
for n in range(1, 6):
    p = DATA / "review" / f"M{n}_REVIEW.md"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    fails = len(re.findall(r"\bfail\b", text, re.I))
    passes = len(re.findall(r"\bpass\b", text, re.I))
    print(f"M{n}_REVIEW.md: {len(text)} chars, pass~{passes}, fail~{fails}")
    if not p.exists():
        issues.append(f"missing review M{n}")
    elif "pass" not in text.lower():
        issues.append(f"M{n}_REVIEW has no pass markers")

# sample deep check: pick 2 random concepts per module and print for human review section
print("\n=== SAMPLE SPOT CHECK (2 per module) ===")
import random

random.seed(42)
for mid in range(1, 6):
    ids = [k for k, v in concepts.items() if v["module"] == mid]
    sample = sorted(random.sample(ids, min(2, len(ids))))
    for cid in sample:
        c = concepts[cid]
        qs = by_concept[cid]
        print(f"\n[{cid}] {c['title']}")
        print(f"  quick: {c['quick'][:140]}...")
        print(f"  pages: {c.get('pages')} quoteOK={( ' '.join((c.get('sourceQuote') or '').split()).lower()[:40] in extracts[mid])}")
        print(f"  MCQs: {len(qs)}")
        for q in qs[:2]:
            print(f"    - {q['stem'][:100]}")
            print(f"      correct[{q['correct']}]= {q['options'][q['correct']][:80]}")

print("\n=== ISSUES SUMMARY ===")
print(f"Total issues: {len(issues)}")
for i in issues[:40]:
    print(" -", i)
if len(issues) > 40:
    print(f" ... and {len(issues)-40} more")

(DATA / "review" / "AUDIT_RECHECK.md").write_text(
    "\n".join(
        [
            "# Recheck audit",
            "",
            f"Concepts: {len(concepts)} | Questions: {len(questions)}",
            f"Issues found: {len(issues)}",
            "",
            "## Issues",
            *( [f"- {x}" for x in issues] if issues else ["- none"] ),
            "",
        ]
    ),
    encoding="utf-8",
)
print("\nWrote data/review/AUDIT_RECHECK.md")
