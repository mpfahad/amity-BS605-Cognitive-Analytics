# Module III Manual Review

Source: `subjects/csit745/v2/source/module_3.txt` (PDF pages 57–86)  
Pack: `scripts/csit745_v2/write_m3_pack.py` → merged into `v2/data/*`  
Date: 2026-09-25

## Summary

| Metric | Count |
|--------|------:|
| Concepts | 19 |
| MCQs | 54 |
| Tree branches | 3 (DOE / Data Collection / Basic Principles) |
| Leaves covered | 3.1.1–3.1.8, 3.2.1–3.2.8, 3.3.1–3.3.3 |

Other modules preserved on merge (M1/M2 still present in tree/bank).

## Section checklist

| Section | Definition | keyIdeas/detail | sourceQuote in extract | MCQs grounded | Result | Notes / fixes |
|---------|------------|-----------------|------------------------|---------------|--------|---------------|
| 3.1.1 Objectives & Strategies | pass | pass | pass | pass (3) | **pass** | Control/experimental groups, Type I/II, n=16·s²/D², glass-bottle strategy steps checked. |
| 3.1.2 Pre-Experimental | pass | pass | pass | pass (2) | **pass** | Basic/cost-effective; teacher-method example. |
| 3.1.3 Quasi-Experimental | pass | pass | pass | pass (3) | **pass** | Extract bullets say “control group is missing” yet example uses a comparison cohort — content notes both; CYU answer (quasi when randomisation not feasible) used for q3. |
| 3.1.4 True Experimental | pass | pass | pass | pass (2) | **pass** | Quote shortened to continuous line (“most precise…”) after hyphenated `cause-`/`effect` line-break failed exact match. Cause–effect claim still in keyIdeas/detail. |
| 3.1.5 Factorial | pass | pass | pass | pass (3) | **pass** | 2×3=6 store combinations; main + interaction effects. |
| 3.1.6 Engineering Experiments | pass | pass | pass | pass (3) | **pass** | Conjecture→experiment→analysis→conclusion; screening→refine→optimise. |
| 3.1.7 Causal Attributions | pass | pass | pass | pass (3) | **pass** | OECD-DAC quote fixed to curly quotes; sole/joint/alternative paths + three approaches. |
| 3.1.8 Statistical Control | pass | pass | pass | pass (3) | **pass** | Variable vs attribute charts; common vs special causes; prerequisites. |
| 3.2.1 Observation & Interview | pass | pass | pass | pass (3) | **pass** | Scientific observation criteria; structured vs other interview types. |
| 3.2.2 Cases | pass | pass | pass | pass (2) | **pass** | Five-step rigorous case sequence. |
| 3.2.3 Questionnaires | pass | pass | pass | pass (3) | **pass** | Mailing vs enumerator/schedule; suitability conditions. |
| 3.2.4 Questionnaire Guidelines | pass | pass | pass | pass (3) | **pass** | Aims→targets→items→types→layout→pilot. |
| 3.2.5 Data Editing | pass | pass | pass | pass (3) | **pass** | Visual / computer / double entry + importance. |
| 3.2.6 Data Coding | pass | pass | pass | pass (3) | **pass** | Reduction/organisation/patterns; Likert 5→1 example. |
| 3.2.7 Don’t Know | pass | pass | pass | pass (3) | **pass** | Quote punctuation fixed to extract curly quotes; “other” + familiarity caution. |
| 3.2.8 Missing Data | pass | pass | pass | pass (3) | **pass** | MCAR/MAR/MNAR; MNAR non-ignorable; prevention/storage. |
| 3.3.1 Validity & Reliability | pass | pass | pass | pass (3) | **pass** | Construct/content/criterion; discriminant/convergent; Cronbach bands; thermometer analogy. Note: extract’s “internal reliability” wording leans toward validity — reported as written. |
| 3.3.2 Replication / Randomisation / Blocking | pass | pass | pass | pass (3) | **pass** | Chance vs real difference; confound equalisation; homogeneous blocks / cage effect. |
| 3.3.3 Orthogonality & False Positives | pass | pass | pass | pass (3) | **pass** | Uncorrelated IVs; balanced ANOVA; false positive vs negative examples. |

## Fixes applied during review

1. **3.1.4 / 3.1.7 / 3.2.7 / 3.3.3 sourceQuotes** — matched extract punctuation (curly quotes; avoided hyphen line-break in 3.1.4).
2. **3.1.6 / 3.2.3 quotes** — trimmed to continuous extract phrases (no ellipsis mashups).
3. Re-ran `write_m3_pack.py` after fixes; quote scan: **0 fails**.

## Verdict

Module III pack **approved** for Explorer/Practice use.
