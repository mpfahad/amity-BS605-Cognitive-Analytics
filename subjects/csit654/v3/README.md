# CSIT654 v3 — Network Security and Cryptography

Isolated from the existing v1 hub tools under `subjects/csit654/`.

## What this is

A full LMS (not the old quiz/map hub):

- Subject → Module → Topic/Concept → Learn / Revise / Practice
- Lessons rewritten in original language (grounded in SLM + deep notes)
- Practice from Amigo + handcrafted bank (`data/mcq_bank.json`, 220 questions)
- Compare contrasts (`lms/compare.html`)
- Progress via shared AmityProgress / Supabase under subject key **`csit654_v3`** (fresh namespace; does not wipe CSIT745 / other subjects)

## Open locally

Serve the repo (or at least `subjects/csit654/v3`) over HTTP, then:

- [`lms/index.html`](lms/index.html) — course home + sync panel
- [`lms/module.html?m=1`](lms/module.html?m=1) — module overview + concept map
- [`lms/concept.html?id=1.1.1`](lms/concept.html?id=1.1.1) — Learn / Revise / Practice
- [`lms/practice.html`](lms/practice.html) — 20-question sessions + browse bank
- [`lms/compare.html`](lms/compare.html) — exam contrast pairs

Example:

```bash
python -m http.server 8767
# open http://127.0.0.1:8767/subjects/csit654/v3/lms/index.html
```

## Data

| File | Role |
|------|------|
| `data/mcq_bank.json` | Amigo topic MCQs (do not overwrite lightly) |
| `data/curriculum.json` | 5 modules × 55 topics |
| `data/concepts.json` | Learn/Revise lesson bodies |
| `source/amigo/` | Raw scrapes |
| `source/module_*.txt` | PDF extracts for authoring |

## LMR

No live-class teacher weightage yet. **No LMR badges** are shown (policy: do not invent from outline order). When a class names priorities, set them via deep notes + `apply_handpicked_lmr.py` / `_exam_policy.json`.

## Progress / Supabase

Same project and table (`bs605_progress`) as other subjects. Payload is namespaced:

```text
subjects.csit654_v3.{visited, conceptDone, practiceAnswers, …}
```

Use **Clear this subject progress** in the sync panel for a fresh start. Do **not** `DROP` the shared table — that would erase every subject.

## Rebuild pipeline

```text
extract_pdf.py → fix_module_ranges.py → build_curriculum.py
→ build_concepts_from_notes.py (+ handcrafted concepts_m1m2 / m3m5)
→ merge_concepts.py → upgrade_flagship_concepts.py
```

MCQ bank stays unless you intentionally reassemble from `source/amigo/`.
