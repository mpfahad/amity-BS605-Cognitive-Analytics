# Module II Manual Review — CSIT745 v2

**Source:** `subjects/csit745/v2/source/module_2.txt` (PDF pages 32–56)  
**Pack script:** `scripts/csit745_v2/write_m2_pack.py`  
**Reviewed:** 2026-09-25  
**Result:** All 12 leaves **PASS** after fixes below.

## Coverage checklist

| Section | Concept id | Pages cited | Quick def | Quote in extract | MCQs (3) | Verdict |
|---------|------------|-------------|-----------|------------------|----------|---------|
| 2.1.1 | m2-2.1.1 | 33 | Pass | Pass | 3 | **PASS** |
| 2.1.2 | m2-2.1.2 | 33–40 | Pass | Pass (Bowley) | 3 | **PASS** |
| 2.1.3 | m2-2.1.3 | 40–42 | Pass | Pass (UNECE) | 3 | **PASS** |
| 2.2.1 | m2-2.2.1 | 42–44 | Pass | Pass (double-barrelled) | 3 | **PASS** |
| 2.2.2 | m2-2.2.2 | 44 | Pass | Pass | 3 | **PASS** |
| 2.2.3 | m2-2.2.3 | 44–45 | Pass | Pass (page limit) | 3 | **PASS** |
| 2.3.1 | m2-2.3.1 | 45–46 | Pass | Pass (sampling plan) | 3 | **PASS** |
| 2.3.2 | m2-2.3.2 | 46–47 | Pass | Pass | 3 | **PASS** |
| 2.3.3 | m2-2.3.3 | 47–49 | Pass | Pass (classification line) | 3 | **PASS** |
| 2.3.4 | m2-2.3.4 | 49–51 | Pass | Pass | 3 | **PASS** |
| 2.3.5 | m2-2.3.5 | 52 | Pass | Pass | 3 | **PASS** |
| 2.3.6 | m2-2.3.6 | 53 | Pass | Pass | 3 | **PASS** |

**Tree:** Module II → 2.1 Data Collection / 2.2 Questionnaire Designing / 2.3 Sampling → all leaves above.  
**Merge:** Module I (and other modules present) preserved; M2 concepts/questions replaced idempotently via `merge_util.merge_module`.

## Section notes

### 2.1.1 Introduction to Data Collection
- Primary/secondary definitions and women’s apparel example match pp. 33 (and summary pp. 53–54).
- CYU answers (surveys; purpose-specific primary) mirrored in q1–q2.
- **Fix applied:** pages set to `[33]` only (earlier draft incorrectly included p. 32 module intro).

### 2.1.2 Data Collection Methods
- Observation/interview/questionnaire/schedule distinctions and secondary published/unpublished sources grounded in pp. 33–40.
- Compare questionnaire vs schedule is explicit in extract.
- Multistage quantitative/qualitative method lists included without inventing extra techniques.

### 2.1.3 Tabulating and Validating Data
- Tabulation objectives and UNECE validation wording verified.
- Validity typology (construct through statistical conclusion) matches pp. 41–42; no extra types invented.
- Email/phone validation examples are from the material.

### 2.2.1 Steps in Constructing a Questionnaire
- Eight steps and questionnaire≠survey misconception match pp. 42–44.
- CYU items (scope step; double-barrelled; personal questions last) used for q1–q3.

### 2.2.2 Types of Questions
- Open-ended, dichotomous, MCQ, scaling subtypes, pictorial — all named in extract; no extra types.

### 2.2.3 Format of Questionnaire
- Size/appearance/clarity/sequence/communicability/span verified; compact-vs-schedule compare present.

### 2.3.1 Sampling Plan
- Plan triad (population, size, procedure) and fuse destructiveness example verified.
- Sample definitions (Bryman & Bell; Cooper & Schindler) from §2.3 intro retained as adjacent grounding for the plan section.

### 2.3.2 Sampling Frame
- Definition + process steps (classify / interval / strategy / size / complete) verified.
- Third MCQ added for market-research “potential respondents database” wording.

### 2.3.3 Sample Selection Methods
- Probability vs non-probability families and mechanisms verified.
- **Fix applied:** `sourceQuote` shortened to exact extract sentence start (`The sample selection methods can be broadly classified into:`) instead of a paraphrased continuation.

### 2.3.4 Probability Sampling Techniques
- P = 25/591 ≈ 4.2% and k ≈ 23 checked against worked examples.
- Multistage listed only (named in material; no invented procedure).

### 2.3.5 Non-Probability Sampling Techniques
- Deliberate/purposeful/judgement alias, convenience/quota/purposive/snowball, and quota table idea verified.

### 2.3.6 Sampling and Non-Sampling Errors
- Sampling vs non-sampling definitions; non-response vs response; response-error sources verified.

## MCQ QA spot-checks
- Stems are exam-style (which/what/why/how), not raw PDF fragments.
- Four options each; `correct` index matches intended answer; explanations cite material facts.
- CYU keys from pp. 54–55 used where they map to sections (2.1.1, 2.2.1).

## Counts (after final merge)
- **Concepts (Module 2):** 12  
- **Questions (Module 2):** 36  
- **IDs:** concepts `m2-2.x.x`; questions `m2-2.x.x-qN`
