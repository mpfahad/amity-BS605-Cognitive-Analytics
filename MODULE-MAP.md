# How the Module Map is made

## Criteria

1. **Source** — SLM outline in the content brief (PDF section order) + live-class emphasis.
2. **One map card ≈ one study topic** in `_study_facts.json` (same IDs as flashcards/quiz).
3. **Merge when useful** — several SLM §§ share one exam idea → one node (e.g. stereotype + prejudice + criticism).
4. **Theme groups** — cards sit in levels (Self → thinking tools → social cognition, etc.).
5. **Colour kinds** — `a` / `b` / `c` = visual groups only, not marks.
6. **LMR** — orange badge = item on `_lmr_notes.txt` (last-minute revision).
7. **Weight** — Module 2 marked **exam focus** from faculty (EI/attitudes > Module 1 alone).
8. **Questions** — module MCQs from study facts; clicking a card filters to that topic.

## Gaps (known)

| Gap | Why | Status |
| --- | --- | --- |
| SLM has more §§ than map nodes | Merged for study usability | Documented on node notes |
| Locus of control (live class) | Not a dedicated SLM map node | Called out on Module 2 root tips |
| Cognition→emotion→behaviour pathway | Faculty thread, not a unit | Root tips only |
| Change vs Sociometry packed in 3.7 | One study topic ID | Note on node; sociometry is LMR |
| Brand / time / work–life / relationships in 3.8 | One study topic ID | Note on node |

## Edit the map

1. Change layout / LMR / notes in `_module_maps.json`.
2. Change definitions / MCQs in `_study_facts.json` (keep topic IDs stable).
3. Run `python build_study_pages.py`.
