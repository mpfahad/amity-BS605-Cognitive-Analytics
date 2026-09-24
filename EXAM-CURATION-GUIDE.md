# Exam curation change guide

Criteria for hand-picking portal content (maps, LMR, flashcards, quizzes) so every subject follows the same rules. Use this when curating the **next module / next live class**, and when running `python audit_study_quality.py`.

## What we changed (so far)

### Portal-wide quality
| Change | Why |
| --- | --- |
| Flashcards show real answers (not “Exam focus…” prompts) | Flip/reveal must teach, not restate the question |
| MCQs rebuilt from deep notes (no “best matches / core idea” templates) | Exam practice must be real definitions and contrasts |
| Deep-note `pack(..., lmr=)` persists `"lmr": true` | LMR flags must survive JSON rewrite |
| Removed outline generator `lmr: i < 3` | First-three-topics was fake LMR |
| `apply_handpicked_lmr.py` syncs deep → maps → `_lmr_notes.txt` | One source of truth for badges and LMR list |
| Quality audit flags templates / empty / placeholders | `CRITICAL=0` required before publish |

### CSE601 (Class 1–2) — reference implementation
| Change | Why |
| --- | --- |
| LMR from **Live Class teacher weightage**, then SLM | Portal is exam prep, not TOC decoration |
| LMR only for topics **taught as exam-critical** in class | “Next class” foreshadow ≠ LMR badge yet |
| Deferred Modules 3–4 from quizzes (`quizSkip`, weight `deferred`) | No live-class weight yet |
| Quiz density: high on LMR, thin on low-weight, skip OOS / deferred | Match teacher advise |
| Out-of-syllabus called out (ADT, level-order) | Teacher said skip |
| Map Group B = violet; LMR = coral + badge | Peach Group B looked like fake LMR |
| Per-subject `_exam_policy.json` | Audit checklist is machine-checkable |

## Source priority (non-negotiable)

```text
1. Live class / LMR teacher advice (transcripts, captions, recordings)
2. Study materials (SLM / PDF) for definitions and syllabus coverage
3. Never invent weightage — if no teacher signal, leave unmarked / deferred
```

If only SLM exists: curate content from SLM, but **do not** stamp LMR badges from “first N outline topics.” Prefer unmarked or a short SLM-density list labelled honestly as *study-material priority (no live class yet)*.

## Criteria checklist (human + audit)

### A. Before touching a subject / module
- [ ] Live class transcript(s) for this module are in `subjects/<code>/` (or noted missing)
- [ ] Study PDF / SLM outline is available (`_pdf_outline.json` or PDF)
- [ ] Create or update `subjects/<code>/_exam_policy.json` (see schema below)

### B. LMR badges (module map + `_lmr_notes.txt`)
- [ ] Every `lmr: true` topic was named by the teacher as exam-important **in a class already held**
- [ ] Foreshadowed “we will cover next” topics are **not** LMR-badged yet
- [ ] Map node `lmr` ↔ deep-notes `lmr` ↔ policy `lmr_topic_ids` are identical sets
- [ ] No module uses auto first-N / first-three-per-level
- [ ] LMR note lines carry a real tip (not “Module N priority.”)

### C. Out of syllabus / downweighted
- [ ] Teacher “not in syllabus” items noted in deep notes (and not treated as LMR)
- [ ] Teacher “rarely asked” topics stay in SLM notes but low/zero quiz weight
- [ ] Map legend: Group B colour ≠ LMR coral

### D. Quizzes / MCQs
- [ ] Deferred modules have **zero** MCQs and `quizSkip: true` on those topics
- [ ] Policy `quiz_skip_topics` have `quizSkip: true` and empty `mcqs`
- [ ] LMR / high-weight topics have denser MCQs than standard topics
- [ ] No template stems (“best matches”, “core idea in…”)
- [ ] Quiz filter chips hide modules with no questions

### E. Module map weights
- [ ] `high` = live-class exam focus modules
- [ ] `deferred` = no live-class weight yet (quiz deferred)
- [ ] `standard` / `foundation` = covered lightly or foreshadow only

### F. Deep notes / flashcards
- [ ] Terms + concepts + traps are SLM-accurate; add teacher exam tips where said
- [ ] Flash backs are answers, not prompts
- [ ] After edits: `_write_handcrafted_deep_json.py` → `apply_handpicked_lmr.py` → subject quiz rebuild → `build_hub.py` → `audit_study_quality.py`

### G. Publish gate
- [ ] `python audit_study_quality.py` → **CRITICAL=0** (includes curation checklist)
- [ ] Spot-check map: only LMR badges on policy list; Group B not coral
- [ ] Push only after audit clean

## Pipeline (CSE601 pattern)

```bash
# 1) Edit handcraft deep notes (lmr=True only for taught exam priorities)
# 2) Rewrite JSON + sync maps/LMR list
python _write_handcrafted_deep_json.py
python apply_handpicked_lmr.py

# 3) Weight quizzes from policy / live-class rules (CSE601)
python rebuild_cse601_exam_mcqs.py

# 4) Build + audit
python build_hub.py
python audit_study_quality.py
```

For a **new subject**, copy the CSE601 pattern: handcraft deep notes → policy JSON → apply LMR → weighted MCQ rebuild → hub → audit.

## `_exam_policy.json` schema

Path: `subjects/<code>/_exam_policy.json`

```json
{
  "code": "cse601",
  "title": "Data Structures & Algorithms",
  "live_classes": [
    "Live Class 1 Transcript.txt",
    "Live Class 2 Transcript.txt"
  ],
  "lmr_source": "live_class",
  "lmr_topic_ids": ["1.1.1", "1.1.2", "1.2.1", "2.1.1", "2.1.2", "2.2.1"],
  "deferred_modules": [3, 4],
  "quiz_skip_topics": ["1.2.4", "1.2.5", "5.1.1"],
  "high_quiz_topics": ["1.1.1", "1.1.2", "1.2.1", "2.1.1", "2.1.2", "2.2.1"],
  "low_quiz_topics": ["1.1.3", "1.2.2", "1.2.3"],
  "module_weights": {
    "1": "high",
    "2": "high",
    "3": "deferred",
    "4": "deferred",
    "5": "standard"
  },
  "out_of_syllabus_notes": [
    "ADT not in syllabus (Class 1–2)",
    "Level-order traversal not in syllabus (Class 2)"
  ],
  "foreshadowed_not_lmr_yet": [
    "2.1.8 Spanning trees — next class",
    "2.2.4 Shortest path — next class",
    "NP-hard / NP-complete — later class"
  ],
  "map_ui": {
    "group_b_must_not_be_coral": true,
    "lmr_requires_badge_and_coral": true
  }
}
```

When the next live class lands: move topics from `foreshadowed_not_lmr_yet` into `lmr_topic_ids`, clear deferred modules if covered, rebuild quizzes, re-audit.

## CSE601 current LMR (Class 1–2)

1. **1.1.1** Stack — overflow/underflow + pseudocode  
2. **1.1.2** Postfix / infix↔prefix conversions  
3. **1.2.1** Algorithm + five characteristics  
4. **2.1.1** Tree height / terminology  
5. **2.1.2** Binary tree properties + pre/in/postorder  
6. **2.2.1** Graph types + matrix/list representations  

## Audit integration

`audit_study_quality.py` loads each subject’s `_exam_policy.json` (if present) and fails **CRITICAL** when:

1. Map LMR set ≠ policy `lmr_topic_ids`
2. Deep-notes LMR set ≠ policy `lmr_topic_ids`
3. Deferred module still has MCQs
4. `quiz_skip_topics` missing `quizSkip` or still have MCQs
5. Module `weight` ≠ policy `module_weights`
6. Built map CSS still paints Group B as coral peach (`#f7e4d5`) when policy requires separation

Subjects **without** `_exam_policy.json` skip the curation block (legacy / not yet curated) but still get the template/quality audit.

## Related files

| File | Role |
| --- | --- |
| `subjects/<code>/_exam_policy.json` | Machine checklist for that subject |
| `apply_handpicked_lmr.py` | deep `lmr` → maps + `_lmr_notes.txt` |
| `rebuild_cse601_exam_mcqs.py` | Weighted / deferred quizzes (CSE601) |
| `_handcraft_*_deep.py` | Handcrafted terms/concepts/notes + `lmr` |
| `audit_study_quality.py` | Quality + curation checklist |
| `.cursor/rules/exam-curation.mdc` | Agent must follow this guide |

## Next module playbook (short)

1. Drop new transcript into `subjects/<code>/`.
2. Mine teacher lines: exam / important / not in syllabus / next class.
3. Update handcraft `lmr=True` only for newly taught priorities; demote stale foreshadow badges.
4. Update `_exam_policy.json` lists + weights.
5. Run pipeline + audit until CRITICAL=0.
6. Push; hard-refresh Pages.
