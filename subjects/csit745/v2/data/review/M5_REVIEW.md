# Module 5 — Manual review log

Source: `subjects/csit745/v2/source/module_5.txt` (PDF pages 131–165).  
Pack: `scripts/csit745_v2/write_m5_pack.py` via `merge_util.merge_module` (does not wipe other modules).  
Practice: whole-subject shuffle. Coverage status: **approved**.

## Counts

| Item | Count |
|------|------:|
| Tree branches | 4 (Research Report / Presentation / Research Paper / Project Proposal) |
| Concept leaves | **22** (5.1.1–5.1.9, 5.2.1–5.2.5, 5.3.1–5.3.5, 5.4.1–5.4.3) |
| MCQs | **66** (3 per leaf; IDs `m5-5.x.y-a/b/c`) |
| Concept IDs | syllabus form `5.x.y` (not `m5-5.x.y`) |

## Manual verification

| Section | Status | Notes |
|---|---|---|
| 5.1.1 | pass | Three traits: structure / independent sections / unbiased conclusions |
| 5.1.2 | pass | Preliminaries / contents / reference materials |
| 5.1.3 | pass | Technical report components for peer academics |
| 5.1.4 | pass | Oral / written / informal / government report types |
| 5.1.5 | pass | Title → appendix steps |
| 5.1.6 | pass | Style rules (simplify / justify / quantify) |
| 5.1.7 | pass | Illustrations & tables guidance |
| 5.1.8 | pass | References (not Bibliography) for cited works |
| 5.1.9 | pass | Footnote purposes; `main part(body)` wording |
| 5.2.1 | pass | Oral harder than written; live audience interaction |
| 5.2.2 | pass | Making / planning a presentation |
| 5.2.3 | pass | Visual-aid rules (font ≥24pt, one point/slide, etc.) |
| 5.2.4 | pass | Effective communication benefits list |
| 5.2.5 | pass | Authentication conventions/strategies |
| 5.3.1 | pass | Journal paper preparation steps (authors → proof) |
| 5.3.2 | pass | Template / outline design of paper |
| 5.3.3 | pass | Impact factor A/B definition from extract |
| 5.3.4 | pass | Citation index; “simply establish” wording |
| 5.3.5 | pass | ISBN vs ISSN digit rules |
| 5.4.1 | pass | Identifying / defining the research problem |
| 5.4.2 | pass | Problem aspects and considerations |
| 5.4.3 | pass | Research plan blueprint / reporting for decision-makers |

## Fixes applied

- Concept IDs normalised from `m5-5.x.y` → `5.x.y`; question IDs keep `m5-…` suffix letters.
- Re-anchored source quotes that failed contiguous extract match (bullets, page footers, “simply” vs “easily”, References clause, footnotes body spacing).
- PDF self-check items 1–4 align with 5.1.1 / 5.1.2 / 5.1.4; item 5 (sampling) stays in Module 2.

## Re-run

```text
python scripts/csit745_v2/write_m5_pack.py
```
