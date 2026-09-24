# -*- coding: utf-8 -*-
"""Full quality audit for Amity multi-subject study packs.

Flags template / placeholder / truncated content in:
  - flashcards
  - MCQs
  - module maps (node bodies / deep notes surfaces)
  - LMR / important-topics lists
  - exam curation checklist (subjects with _exam_policy.json)

Run: python audit_study_quality.py
Exit code 1 if any critical issues remain.

See EXAM-CURATION-GUIDE.md for the human checklist.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"
CODES = ("bs605", "cse601", "csit654", "csit745")

TEMPLATE_Q = re.compile(r"Which statement best matches\b", re.I)
CORE_IDEA = re.compile(r"core idea in\b", re.I)
SYLLABUS_TOPIC = re.compile(r"syllabus topic in this module", re.I)
DEFINE_PROMPT = re.compile(r"^Define .+ in one line", re.I)
EXAM_FOCUS = re.compile(r"^Exam focus:", re.I)
PLACEHOLDER_BODY = re.compile(
    r"Open flashcards for this topic|Deep notes for this topic are still|TODO|TBD|lorem ipsum",
    re.I,
)
TRUNC_END = re.compile(r"(?:\b(?:the|a|an|with|for|and|of|to|is|are|in|on|by)\b|[,;:])\s*$", re.I)
TOPIC_ID_RE = re.compile(r"^\d+(\.\d+)+$")


def weak_flash_back(back: str) -> str | None:
    b = (back or "").strip()
    if not b:
        return "empty_back"
    if DEFINE_PROMPT.search(b):
        return "define_prompt_back"
    if SYLLABUS_TOPIC.search(b):
        return "syllabus_placeholder_back"
    if len(b) < 25:
        return "too_short_back"
    if TRUNC_END.search(b) and len(b) < 90:
        return "truncated_back"
    if b.endswith("?") and not b.lower().startswith(("what", "which", "how", "why", "when", "where")):
        # answer that is still a question
        return "question_as_back"
    return None


def weak_flash_front(front: str) -> str | None:
    f = (front or "").strip()
    if EXAM_FOCUS.search(f):
        return "exam_focus_front"
    if not f:
        return "empty_front"
    return None


def weak_mcq(q: dict) -> list[str]:
    issues = []
    text = q.get("q") or ""
    opts = q.get("options") or []
    explain = q.get("explain") or ""
    if TEMPLATE_Q.search(text):
        issues.append("template_best_matches_q")
    if any(CORE_IDEA.search(o or "") for o in opts):
        issues.append("core_idea_option")
    if "is a syllabus topic under" in explain:
        issues.append("syllabus_explain")
    if len(opts) != 4:
        issues.append(f"option_count_{len(opts)}")
    if not text.strip():
        issues.append("empty_q")
    # identical options
    norms = [re.sub(r"\s+", " ", (o or "").strip().lower()) for o in opts]
    if len(set(norms)) < len(norms):
        issues.append("duplicate_options")
    ans = q.get("answer")
    if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
        issues.append("bad_answer_index")
    # correct option empty
    if isinstance(ans, int) and 0 <= ans < len(opts) and not (opts[ans] or "").strip():
        issues.append("empty_correct_option")
    # all options look like meta labels
    meta = sum(1 for o in opts if CORE_IDEA.search(o or "") or "Unrelated to Module" in (o or "") or "programming-language keyword" in (o or "") or "definition-only label" in (o or ""))
    if meta >= 3:
        issues.append("meta_options_cluster")
    return issues


def audit_facts(code: str) -> dict:
    path = SUBJECTS / code / "_study_facts.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    fc_issues = []
    mcq_issues = []
    fc_n = mcq_n = 0
    for mod in data.get("modules") or []:
        mid = mod.get("id")
        for topic in mod.get("topics") or []:
            tid = topic.get("id")
            title = topic.get("title")
            cards = topic.get("flashcards") or []
            if not cards:
                fc_issues.append({"id": tid, "issue": "no_flashcards", "title": title})
            for i, c in enumerate(cards):
                fc_n += 1
                fi = weak_flash_front(c.get("front") or "")
                bi = weak_flash_back(c.get("back") or "")
                if fi or bi:
                    fc_issues.append(
                        {
                            "id": tid,
                            "card": i,
                            "issue": ",".join(x for x in [fi, bi] if x),
                            "front": (c.get("front") or "")[:80],
                            "back": (c.get("back") or "")[:100],
                        }
                    )
            qs = topic.get("mcqs") or []
            if not qs:
                if topic.get("quizSkip"):
                    continue  # intentional exam-weight skip
                mcq_issues.append({"id": tid, "issue": "no_mcqs", "title": title, "module": mid})
            for i, q in enumerate(qs):
                mcq_n += 1
                bad = weak_mcq(q)
                if bad:
                    mcq_issues.append(
                        {
                            "id": tid,
                            "q_i": i,
                            "issue": ",".join(bad),
                            "q": (q.get("q") or "")[:100],
                        }
                    )
    return {
        "flash_total": fc_n,
        "flash_issues": fc_issues,
        "mcq_total": mcq_n,
        "mcq_issues": mcq_issues,
    }


def audit_maps(code: str) -> dict:
    path = SUBJECTS / code / "_module_maps.json"
    deep_path = SUBJECTS / code / "_deep_notes.json"
    issues = []
    node_n = 0
    if not path.exists():
        return {"nodes": 0, "issues": [{"issue": "missing_module_maps"}]}
    maps = json.loads(path.read_text(encoding="utf-8"))
    deep = json.loads(deep_path.read_text(encoding="utf-8")) if deep_path.exists() else {}

    for mod in maps.get("modules") or []:
        root = mod.get("root") or {}
        node_n += 1
        body = root.get("body") or ""
        if PLACEHOLDER_BODY.search(body):
            issues.append({"id": root.get("id"), "issue": "placeholder_root_body", "body": body[:100]})
        for level in mod.get("levels") or []:
            for n in level.get("nodes") or []:
                node_n += 1
                nid = n.get("id") or n.get("topicId")
                title = n.get("title") or ""
                # deep notes coverage for topic nodes
                tid = n.get("topicId") or nid
                if tid and not str(tid).endswith("_root"):
                    pack = deep.get(tid)
                    if not pack:
                        issues.append({"id": tid, "issue": "map_node_missing_deep_notes", "title": title})
                    else:
                        terms = pack.get("terms") or []
                        if not terms:
                            issues.append({"id": tid, "issue": "deep_notes_no_terms", "title": title})
                        else:
                            # weak term defs
                            for t in terms:
                                d = (t.get("d") or "").strip()
                                if not d or SYLLABUS_TOPIC.search(d) or len(d) < 15:
                                    issues.append(
                                        {
                                            "id": tid,
                                            "issue": "weak_deep_term",
                                            "term": t.get("t"),
                                            "d": d[:80],
                                        }
                                    )
                body = n.get("body") or ""
                if body and PLACEHOLDER_BODY.search(body):
                    issues.append({"id": nid, "issue": "placeholder_node_body", "body": body[:100]})
    return {"nodes": node_n, "issues": issues}


def audit_lmr(code: str) -> dict:
    path = SUBJECTS / code / "_lmr_notes.txt"
    issues = []
    lines = []
    if not path.exists():
        return {"lines": 0, "issues": [{"issue": "missing_lmr_notes"}]}
    text = path.read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.lower().startswith(code) or "—" in line[:40] and "LMR" in line:
            continue
        if re.match(r"^\d+[\).]", line) or line[0].isdigit() or line.startswith("-"):
            lines.append(line)
            if SYLLABUS_TOPIC.search(line) or "priority." == line[-9:]:
                # "1.1.1 Stack — Module 1 priority." is thin but acceptable as LMR pointer
                pass
            if TEMPLATE_Q.search(line) or CORE_IDEA.search(line):
                issues.append({"issue": "template_in_lmr", "line": line[:120]})
            if len(line) < 8:
                issues.append({"issue": "too_short_lmr", "line": line})
    if len(lines) < 3:
        issues.append({"issue": "too_few_lmr_items", "count": len(lines)})
    return {"lines": len(lines), "issues": issues}


def audit_html_embed(code: str) -> dict:
    """Ensure generated HTML no longer embeds known template strings."""
    issues = []
    base = SUBJECTS / code
    checks = {
        "flashcards.html": ["Exam focus:", "syllabus topic in this module", "Define "],
        "quiz.html": ["Which statement best matches", "core idea in", "is a syllabus topic under"],
    }
    for fname, needles in checks.items():
        path = base / fname
        if not path.exists():
            issues.append({"file": fname, "issue": "missing_html"})
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            # Allow "Define" only as part of legitimate questions like "Which statement best defines"
            if needle == "Define ":
                # count Define-prompt backs specifically
                if "Define " in text and " in one line" in text:
                    issues.append({"file": fname, "issue": "html_contains", "needle": "Define ... in one line"})
                continue
            if needle in text:
                issues.append({"file": fname, "issue": "html_contains", "needle": needle})
    return {"issues": issues}


def _topic_sort_key(tid: str):
    parts = []
    for p in str(tid).split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(p)
    return parts


def audit_curation(code: str) -> dict:
    """Checklist from subjects/<code>/_exam_policy.json (EXAM-CURATION-GUIDE.md)."""
    base = SUBJECTS / code
    policy_path = base / "_exam_policy.json"
    if not policy_path.exists():
        return {"enabled": False, "issues": [], "checks": []}

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    issues: list[dict] = []
    checks: list[str] = []

    deep = {}
    deep_path = base / "_deep_notes.json"
    if deep_path.exists():
        deep = json.loads(deep_path.read_text(encoding="utf-8"))
    maps = {}
    maps_path = base / "_module_maps.json"
    if maps_path.exists():
        maps = json.loads(maps_path.read_text(encoding="utf-8"))
    facts = {}
    facts_path = base / "_study_facts.json"
    if facts_path.exists():
        facts = json.loads(facts_path.read_text(encoding="utf-8"))

    want_lmr = sorted(policy.get("lmr_topic_ids") or [], key=_topic_sort_key)
    deep_lmr = sorted(
        (
            k
            for k, v in deep.items()
            if isinstance(v, dict) and v.get("lmr") and TOPIC_ID_RE.match(str(k))
        ),
        key=_topic_sort_key,
    )
    map_lmr = []
    for mod in maps.get("modules") or []:
        for level in mod.get("levels") or []:
            for n in level.get("nodes") or []:
                if n.get("lmr"):
                    map_lmr.append(str(n.get("topicId") or n.get("id")))
    map_lmr = sorted(set(map_lmr), key=_topic_sort_key)

    checks.append("lmr_sets_aligned")
    if deep_lmr != want_lmr:
        issues.append(
            {
                "issue": "curation_lmr_deep_mismatch",
                "expected": want_lmr,
                "actual": deep_lmr,
            }
        )
    if map_lmr != want_lmr:
        issues.append(
            {
                "issue": "curation_lmr_map_mismatch",
                "expected": want_lmr,
                "actual": map_lmr,
            }
        )

    # Live-class files present when claimed
    for fname in policy.get("live_classes") or []:
        checks.append(f"live_class_present:{fname}")
        if not (base / fname).exists():
            issues.append({"issue": "curation_missing_live_class", "file": fname})

    # Module weights
    want_weights = {str(k): v for k, v in (policy.get("module_weights") or {}).items()}
    if want_weights:
        checks.append("module_weights")
        for mod in maps.get("modules") or []:
            mid = str(mod.get("id"))
            if mid in want_weights and (mod.get("weight") or "standard") != want_weights[mid]:
                issues.append(
                    {
                        "issue": "curation_module_weight_mismatch",
                        "module": mid,
                        "expected": want_weights[mid],
                        "actual": mod.get("weight"),
                    }
                )

    deferred = {int(x) for x in (policy.get("deferred_modules") or [])}
    skip_topics = set(policy.get("quiz_skip_topics") or [])
    if deferred or skip_topics:
        checks.append("quiz_skip_and_deferred")
        for mod in facts.get("modules") or []:
            mid = int(mod.get("id"))
            for topic in mod.get("topics") or []:
                tid = str(topic.get("id") or "")
                n_mcq = len(topic.get("mcqs") or [])
                skipped = bool(topic.get("quizSkip"))
                if mid in deferred:
                    if n_mcq:
                        issues.append(
                            {
                                "issue": "curation_deferred_module_has_mcqs",
                                "module": mid,
                                "id": tid,
                                "mcq_count": n_mcq,
                            }
                        )
                    if not skipped:
                        issues.append(
                            {
                                "issue": "curation_deferred_missing_quizSkip",
                                "module": mid,
                                "id": tid,
                            }
                        )
                if tid in skip_topics:
                    if n_mcq:
                        issues.append(
                            {
                                "issue": "curation_skip_topic_has_mcqs",
                                "id": tid,
                                "mcq_count": n_mcq,
                            }
                        )
                    if not skipped:
                        issues.append(
                            {
                                "issue": "curation_skip_topic_missing_quizSkip",
                                "id": tid,
                            }
                        )

    # Foreshadowed topics must not be LMR-badged
    foreshadow = policy.get("foreshadowed_not_lmr_yet") or []
    if foreshadow:
        checks.append("foreshadow_not_lmr")
        for line in foreshadow:
            m = re.match(r"^(\d+(?:\.\d+)+)\b", str(line).strip())
            if not m:
                continue
            tid = m.group(1)
            if tid in want_lmr or tid in deep_lmr or tid in map_lmr:
                issues.append({"issue": "curation_foreshadow_still_lmr", "id": tid, "note": line})

    # Map UI: Group B must not reuse old coral peach
    map_ui = policy.get("map_ui") or {}
    if map_ui.get("group_b_must_not_be_coral"):
        checks.append("group_b_not_coral")
        forbidden = (map_ui.get("forbidden_group_b_bg") or "#f7e4d5").lower()
        html_path = base / "module-map.html"
        if html_path.exists():
            html = html_path.read_text(encoding="utf-8")
            # Old pattern: .node.b { background: #f7e4d5
            if re.search(rf"\.node\.b\s*\{{[^}}]*background:\s*{re.escape(forbidden)}", html, re.I):
                issues.append(
                    {
                        "issue": "curation_group_b_coral_collision",
                        "detail": f".node.b still uses {forbidden} (collides with LMR)",
                    }
                )

    return {"enabled": True, "issues": issues, "checks": checks, "lmr_expected": want_lmr}


def main() -> int:
    report = {"subjects": {}, "critical": 0, "warn": 0}
    critical_keys = {
        "template_best_matches_q",
        "core_idea_option",
        "syllabus_explain",
        "meta_options_cluster",
        "exam_focus_front",
        "define_prompt_back",
        "syllabus_placeholder_back",
        "html_contains",
        "no_flashcards",
        "no_mcqs",
        # curation checklist (EXAM-CURATION-GUIDE.md)
        "curation_lmr_deep_mismatch",
        "curation_lmr_map_mismatch",
        "curation_missing_live_class",
        "curation_module_weight_mismatch",
        "curation_deferred_module_has_mcqs",
        "curation_deferred_missing_quizSkip",
        "curation_skip_topic_has_mcqs",
        "curation_skip_topic_missing_quizSkip",
        "curation_foreshadow_still_lmr",
        "curation_group_b_coral_collision",
    }

    for code in CODES:
        facts = audit_facts(code)
        maps = audit_maps(code)
        lmr = audit_lmr(code)
        html = audit_html_embed(code)
        curation = audit_curation(code)
        sub = {
            "facts": {
                "flash_total": facts["flash_total"],
                "flash_issue_count": len(facts["flash_issues"]),
                "mcq_total": facts["mcq_total"],
                "mcq_issue_count": len(facts["mcq_issues"]),
                "flash_issues_sample": facts["flash_issues"][:8],
                "mcq_issues_sample": facts["mcq_issues"][:8],
            },
            "maps": {
                "nodes": maps["nodes"],
                "issue_count": len(maps["issues"]),
                "issues_sample": maps["issues"][:8],
            },
            "lmr": {
                "lines": lmr["lines"],
                "issue_count": len(lmr["issues"]),
                "issues": lmr["issues"][:8],
            },
            "html": html,
            "curation": {
                "enabled": curation["enabled"],
                "check_count": len(curation.get("checks") or []),
                "issue_count": len(curation["issues"]),
                "issues": curation["issues"][:12],
                "lmr_expected": curation.get("lmr_expected") or [],
            },
        }
        report["subjects"][code] = sub

        def count_crit(items, key="issue"):
            n = 0
            for it in items:
                iss = it.get(key) or ""
                for part in iss.split(","):
                    if part in critical_keys or part.startswith("html_contains") or part.startswith("curation_"):
                        n += 1
            return n

        crit = 0
        crit += count_crit(facts["flash_issues"])
        crit += count_crit(facts["mcq_issues"])
        crit += count_crit(html["issues"])
        crit += count_crit(curation["issues"])
        # missing deep notes for maps = warn not critical if overview still works
        warn = (
            len(facts["flash_issues"])
            + len(facts["mcq_issues"])
            + len(maps["issues"])
            + len(lmr["issues"])
            + len(curation["issues"])
            - crit
        )
        report["critical"] += crit
        report["warn"] += max(0, warn)

    out = ROOT / "_quality_audit_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # human summary
    print(f"CRITICAL={report['critical']} WARN~={report['warn']}")
    for code, sub in report["subjects"].items():
        f, m = sub["facts"], sub["maps"]
        cur = sub["curation"]
        cur_bit = (
            f"curation {cur['check_count']} checks (issues {cur['issue_count']})"
            if cur["enabled"]
            else "curation off"
        )
        print(
            f"{code}: flash {f['flash_total']} (issues {f['flash_issue_count']}) | "
            f"mcq {f['mcq_total']} (issues {f['mcq_issue_count']}) | "
            f"map nodes {m['nodes']} (issues {m['issue_count']}) | "
            f"lmr {sub['lmr']['lines']} (issues {sub['lmr']['issue_count']}) | "
            f"html_issues {len(sub['html']['issues'])} | {cur_bit}"
        )
        for sample in f["mcq_issues_sample"][:3]:
            print(f"  MCQ {sample.get('id')}: {sample.get('issue')} | {sample.get('q')}")
        for sample in f["flash_issues_sample"][:3]:
            print(f"  FC  {sample.get('id')}: {sample.get('issue')} | {sample.get('front')}")
        for sample in m["issues_sample"][:3]:
            print(f"  MAP {sample.get('id')}: {sample.get('issue')}")
        for sample in sub["html"]["issues"][:3]:
            print(f"  HTML {sample.get('file')}: {sample.get('needle') or sample.get('issue')}")
        for sample in cur["issues"][:5]:
            print(f"  CURATION {sample.get('issue')}: {sample.get('id') or sample.get('module') or sample.get('detail') or sample.get('file') or sample.get('expected')}")
    print(f"Wrote {out}")
    return 1 if report["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
