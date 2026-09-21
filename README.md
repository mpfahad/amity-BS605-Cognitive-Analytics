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
python build_hub.py
```

## Docs
- [SETUP-SYNC.md](SETUP-SYNC.md) — Supabase (already configured)
- [MODULE-MAP.md](MODULE-MAP.md) — map criteria (BS605)
- Working notes live under `C:\Users\User\Projects\AMITY\`
