# Replicate this study pack for another subject

This repo is the **template pattern** for one Amity Online subject:
static HTML study tools + optional sync code (phone ↔ PC) + GitHub Pages.

BS605-specific pieces are named `BS605` / `bs605`. For a new subject, copy the pattern and rename those.

---

## What you get

| Piece | Purpose |
| --- | --- |
| `index.html` | Home + progress dashboard + page list |
| `flashcards.html` | Flip cards, seen/known tracking |
| `quiz.html` | MCQs with score + per-module stats |
| `module-map.html` | Structure map + important questions |
| `progress.js` / `sync-ui.js` / `config.js` | Cross-device sync |
| `build_study_pages.py` | Regenerates HTML from JSON |
| `_study_facts.json` | Modules → topics → flashcards + MCQs |
| `_module_maps.json` | Map layout (nodes / levels) |
| `_lmr_notes.txt` | Last-minute revision list |
| Transcripts / PDF | Source materials (linked from pages) |

---

## One-time: copy for subject XYZ

Example subject code: `PFE701` (use your real code).

### 1. New GitHub repo + Pages

1. Create repo: `amity-PFE701-Professional-Ethics` (or similar).
2. Copy this folder’s files into it (or clone this repo and wipe BS605 content).
3. Settings → Pages → deploy from `main` / root.
4. Site URL becomes: `https://<you>.github.io/amity-PFE701-Professional-Ethics/`

Keep **one repo per subject** so Pages sites do not overwrite each other.

### 2. Rename sync identifiers

In the new repo, replace BS605 branding in code:

| File | Change |
| --- | --- |
| `config.js` | `window.BS605_SYNC` → `window.PFE701_SYNC` (or a shared `window.AMITY_SYNC` if you prefer) |
| `progress.js` | Storage keys `bs605_*`, table `bs605_progress`, global `BS605Progress` |
| `sync-ui.js` | Element ids / class prefix `bs605` (optional but cleaner) |
| `supabase/setup.sql` | Table name e.g. `pfe701_progress` |
| `build_study_pages.py` | Titles, course name, PDF filename, script globals |

Use a **separate Supabase table per subject** (same project is fine) so progress never mixes.

Then follow [SETUP-SYNC.md](SETUP-SYNC.md) with the new table name and `config.js` keys.

### 3. Replace study content

1. Put the new SLM PDF in the repo root.
2. Add live-class transcripts (`.txt`) and optional `.vtt` captions.
3. Rebuild content JSON:
   - `_study_facts.json` — modules, topics, flashcards, MCQs, explanations
   - `_module_maps.json` — interactive map structure
   - `_lmr_notes.txt` — numbered LMR priorities
4. Update `LINKS` / `PDF_NAME` / course title in `build_study_pages.py`.
5. Run:

```bash
python build_study_pages.py
```

6. Commit and push. Wait 1–2 minutes for GitHub Pages.

### 4. Content shape (minimum)

`_study_facts.json` sketch:

```json
{
  "course": "Subject title (CODE)",
  "modules": [
    {
      "id": 1,
      "title": "Module title",
      "topics": [
        {
          "id": "1.1",
          "title": "Topic title",
          "flashcards": [
            { "front": "Q?", "back": "A.", "detail": "optional tip" }
          ],
          "mcqs": [
            {
              "q": "Question?",
              "options": ["A", "B", "C", "D"],
              "answer": 1,
              "explain": "Why B is right."
            }
          ]
        }
      ]
    }
  ]
}
```

`_module_maps.json` must list each module’s `levels` / `nodes`; the builder merges flashcard text + MCQs onto those nodes.

---

## Workspace layout (multi-subject)

Recommended on your machine:

```text
Projects/
  AMITY/                          ← master workspace (all subjects’ source notes)
    PFE701-.../
    BS605-.../
  amity-BS605-Cognitive-Analytics/   ← public Pages site (this repo)
  amity-PFE701-.../                  ← next public Pages site
```

- **AMITY** = working notes, extracts, transcripts.
- **amity-CODE-…** = published study pack only.

---

## Ask Cursor to build the next one

In a new chat (with this repo or the new empty repo open), paste:

> Use this BS605 study pack as the template. Create the same pack for **[SUBJECT CODE + title]**.  
> Materials: [PDF / transcripts / notes].  
> New repo: `amity-[CODE]-[Short-Name]`.  
> Separate Supabase table and sync config.  
> Then rebuild pages and enable GitHub Pages.

Point the agent at `REPLICATE.md` and `SETUP-SYNC.md` so it follows the same steps.

---

## Checklist

- [ ] New `amity-CODE-…` repo + GitHub Pages
- [ ] Renamed sync keys + SQL table
- [ ] Fresh `_study_facts.json` / `_module_maps.json` / `_lmr_notes.txt`
- [ ] `python build_study_pages.py`
- [ ] Sync panel works on phone and PC with one code
- [ ] Home shows progress; every page has the top nav

---

## What is already documented here

| Doc | Covers |
| --- | --- |
| [README.md](README.md) | Open locally, Pages URL, rebuild, sync pointer |
| [SETUP-SYNC.md](SETUP-SYNC.md) | Supabase project + `config.js` |
| [REPLICATE.md](REPLICATE.md) | This file — clone for another subject |
| `supabase/setup.sql` | Table + RLS |

There is **no** separate Cursor skill installed for this yet; this repo’s docs are the playbook.
