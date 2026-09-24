# Amity study hub (multi-subject)

One GitHub Pages site for Semester II subjects. Same sync code across all subjects; progress is stored **per subject** so they never wipe each other.

## Live
https://mpfahad.github.io/amity-BS605-Cognitive-Analytics/

## Subjects
| Code | Path |
| --- | --- |
| BS605 | [subjects/bs605/](subjects/bs605/) Cognitive Analytics & Social Skills |
| CSE601 | [subjects/cse601/](subjects/cse601/) Data Structures & Algorithm Design |
| CSIT654 | [subjects/csit654/](subjects/csit654/) Network Security & Cryptography |
| CSIT745 | [subjects/csit745/](subjects/csit745/) Research Methodology |

## Progress (important)
Your **existing BS605 sync code and cloud/local progress are kept**.
On first load the hub migrates legacy flat payloads into `subjects.bs605` automatically (same Supabase table).

## Rebuild
```bash
python generate_facts_from_outline.py   # only if regenerating CSE601/CSIT packs from PDF outlines
python _write_handcrafted_deep_json.py
python apply_handpicked_lmr.py
python rebuild_cse601_exam_mcqs.py      # CSE601 live-class weighted quizzes
python build_hub.py
python audit_study_quality.py           # must be CRITICAL=0 (includes curation checklist)
```

## Docs
- [EXAM-CURATION-GUIDE.md](EXAM-CURATION-GUIDE.md) — **change guide + checklist** for LMR, quizzes, maps, next modules
- [SETUP-SYNC.md](SETUP-SYNC.md) — Supabase (already configured)
- [MODULE-MAP.md](MODULE-MAP.md) — map criteria (BS605)
- Per curated subject: `subjects/<code>/_exam_policy.json` (machine checklist for audit)
