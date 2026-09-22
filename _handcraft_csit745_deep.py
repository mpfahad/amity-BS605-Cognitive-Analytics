# -*- coding: utf-8 -*-
"""Handcrafted deep notes for CSIT745 Research Methodology (BS605 Module-3 quality).

Importable: from _handcraft_csit745_deep import CSIT745
Do not run build from this file.
"""
from __future__ import annotations


def T(name: str, d: str) -> dict:
    return {"t": name, "d": d}


def pack(terms, concepts, notes, lmr: bool = False) -> dict:
    """Handcrafted deep-note pack. Set lmr=True for exam-priority topics only."""
    return {"terms": terms, "concepts": concepts, "notes": notes, "lmr": bool(lmr)}


CSIT745: dict[str, dict] = {
    # =========================================================================
    # Module roots
    # =========================================================================
    "m1_root": pack(
        [
            T("Research", "Systematic, controlled inquiry to generate, verify, or extend knowledge."),
            T("Research design", "Blueprint: pure/applied, causal/correlational, experimental vs descriptive."),
            T("Research modeling", "Types of models, building stages, heuristics vs simulation."),
            T("Methods vs methodology", "Methods = tools/procedures; methodology = logic of how research is done."),
        ],
        [
            "Walk Module 1 as: what research is → process/approaches → design types → modeling.",
            "LMR cluster 1.1.1–1.1.3 sits first: definitions, characteristics, methods≠methodology.",
            "Design labels (causal, longitudinal, factorial later) reappear in Modules 3–4.",
        ],
        [
            "Prioritise LMR cards 1.1.1–1.1.3 before design catalogues.",
            "Trap: inductive ≠ qualitative automatically; deductive ≠ only quantitative.",
            "When asked for ‘process’, list problem→approach→design→data→analysis→report.",
        ],
    ),
    "m2_root": pack(
        [
            T("Data collection", "Primary vs secondary; observation, interview, questionnaire, records."),
            T("Questionnaire design", "Steps, question types, format — measurement instrument quality."),
            T("Sampling", "Plan, frame, probability vs non-probability, sampling vs non-sampling error."),
        ],
        [
            "Flow: decide what to measure → instrument → who to sample → validate/tabulate.",
            "LMR 2.1.1–2.1.3: collection intro, methods, tabulating/validating.",
            "Sampling error ≠ bias from a bad frame or non-response (non-sampling).",
        ],
        [
            "Exam contrast: probability (known chance) vs non-probability (unknown chance).",
            "Always name the sampling frame when discussing sample selection.",
            "Open/closed questions and Likert scales show up with reliability/validity in Module 3.",
        ],
    ),
    "m3_root": pack(
        [
            T("Experimental designs", "Pre-, quasi-, true, factorial — control and randomisation differ."),
            T("Field data handling", "Observation/interview/cases/questionnaires → edit, code, missing data."),
            T("Validity & reliability", "Accuracy vs consistency; plus replication, randomisation, blocking."),
        ],
        [
            "Design strength rises: pre-experimental < quasi < true experimental.",
            "LMR 3.1.1–3.1.3: DOE objectives, pre-experimental, quasi-experimental.",
            "Orthogonality and false positives link design to hypothesis testing (Module 4).",
        ],
        [
            "Causal attribution needs manipulation + control + (ideally) random assignment.",
            "Reliability without validity = consistent but wrong measure.",
            "Don’t Know / missing-data rules affect bias before any ANOVA.",
        ],
    ),
    "m4_root": pack(
        [
            T("Hypothesis testing", "H0 vs H1, Type I/II, one-/two-tailed, α, CI, rejection region."),
            T("Parametric tests", "z, t, proportions, variance/F, ANOVA fixed/random effects."),
            T("Model adequacy", "Residuals, assumptions — after fitting, check before interpreting."),
        ],
        [
            "LMR 4.1.1–4.1.3: what a hypothesis is, H0/H1, Type I vs Type II.",
            "Choose test by: parameter (mean/prop/var), samples (1/2/k), known σ, normality.",
            "ANOVA partitions SST into treatment + error; F = MST/MSE.",
        ],
        [
            "Reject H0 when test statistic falls in the rejection region (p < α).",
            "Type I = false positive (reject true H0); Type II = miss (fail to reject false H0).",
            "One-tailed vs two-tailed changes critical value and wording of H1.",
        ],
    ),
    "m5_root": pack(
        [
            T("Research report", "Meaning, structure, components, types, style, citations, footnotes."),
            T("Presentation", "Oral delivery, visuals, effective communication, authentication."),
            T("Publication metrics", "Impact factor, citation index, ISBN (books) vs ISSN (serials)."),
            T("Project proposal", "Problem definition, aspects/considerations, research plan."),
        ],
        [
            "LMR 5.1.1–5.1.3: report meaning, scientific structure, components.",
            "Writing → presenting → journal packaging → proposal planning.",
            "ISBN ≠ ISSN; impact factor ≠ citation count of one paper.",
        ],
        [
            "Standard report arc: title/abstract → intro → methods → results → discussion → refs.",
            "Cite to avoid plagiarism and to show scholarly trail.",
            "Proposal must define problem before methods and timeline.",
        ],
    ),

    # =========================================================================
    # Module 1 — Research foundations
    # =========================================================================
    "1.1.1": pack(  # LMR
        [
            T("Research (Redman & Mory)", "Systematised effort to gain new knowledge."),
            T("Research (Slesinger & Stephenson)", "Manipulation of things, concepts or symbols to generalise, extend, correct or verify knowledge."),
            T("Research (Clifford Woody)", "Define/redefine problems; form hypotheses; collect/organise/evaluate data; deduce; test conclusions against hypotheses."),
            T("General objectives", "Broad secondary aims — overall study goal (the ‘big picture’)."),
            T("Specific objectives", "Operational splits of the general aim — who/what/why/when/how."),
            T("R&D link", "Research underpins progress; tied to research and development."),
        ],
        [
            "Definitions cluster: new knowledge + systematic method + hypothesis–data–test loop.",
            "General objectives set scope; specific objectives make the plan executable.",
            "Research is not mere fact-gathering — it generalises or verifies knowledge.",
        ],
        [
            "LMR: ‘systematised effort / new knowledge’ → Redman & Mory.",
            "LMR: Woody’s list is the process mini-definition — good long-answer skeleton.",
            "Stem ‘secondary / detailed view of goal’ → general objectives; ‘who/what/how’ → specific.",
            "Don’t stop at ‘finding facts’ — mention hypothesis testing or generalisation.",
            "Breakthrough vs incremental improvement both count as research outcomes.",
            "Action-oriented wording in characteristics (1.1.2) complements objectives here.",
        ],
        lmr=True,
    ),
    "1.1.2": pack(  # LMR
        [
            T("Systematic", "Follow a structured, planned procedure — not ad hoc."),
            T("Logical", "Ideas manipulated coherently; scientific progress needs logical control."),
            T("Replicable / verifiable", "Earlier results checkable in new places, people, or times."),
            T("Condensed / transferable", "Findings shared so others need not repeat the same study blindly."),
            T("Action-oriented", "Aims at solutions usable by decision-makers or practice."),
            T("Multidisciplinary & participatory", "Uses multiple discipline approaches; involves stakeholders."),
        ],
        [
            "Characteristics answer ‘what makes inquiry scientific research?’ — process + quality + use.",
            "Replicable ≠ identical copy; means verifiable under comparable conditions.",
            "Cost/time constraints and clear design are practical characteristics, not afterthoughts.",
        ],
        [
            "LMR list cue: pressing problem, systematic, logical, condensed, repeatable, generative, action-oriented, multidisciplinary, participatory, timed, economical, usable format.",
            "Stem ‘results available so others needn’t redo’ → condensed/communicable findings.",
            "Stem ‘verifiable in new setting’ → replicable.",
            "Trap: creativity alone is not enough without systematic procedure.",
            "‘Successful’ often means generative — one question spawns further research.",
            "Delivery format for managers/community is an exam-listed characteristic.",
        ],
        lmr=True,
    ),
    "1.1.3": pack(  # LMR
        [
            T("Research methods", "Procedures, schemes, steps, algorithms used in a study (tools)."),
            T("Research methodology", "Science of how research should be done — the work plan / logic of inquiry."),
            T("Examples of methods", "Observation, experiments, numerical schemes, statistical approaches, sampling."),
            T("Value-agnostic methods", "Methods are planned and scientific; used to collect samples/data and solve problems."),
            T("Methodology goal", "Describe, explain, predict phenomena via a justified approach."),
        ],
        [
            "Methods = ‘what techniques’; methodology = ‘why this design and these techniques’. ",
            "You can list many methods inside one methodology framework.",
            "Business/scientific methods demand verification by facts/measurement, not pure reasoning alone.",
        ],
        [
            "LMR contrast table: methods (tools/procedures) vs methodology (study of methods / research plan).",
            "Stem ‘algorithms used during the study’ → methods; ‘how research ought to be conducted’ → methodology.",
            "Trap: using the words interchangeably loses marks.",
            "Methodology provides the research work plan; methods execute collection and analysis.",
            "Experiments and statistics are methods; choosing experimental vs survey design is methodological.",
            "One-liner: Methods are the tools; methodology is the logic of using them.",
        ],
        lmr=True,
    ),
    "1.2.1": pack(
        [
            T("Research criteria", "Clear goal, documented process, unbiased design, disclosed limits, suitable analysis, evidence-based conclusions, researcher integrity."),
            T("Research process (steps)", "Problem definition → approach → design → fieldwork/data → preparation/analysis → report/presentation."),
            T("Objectivity", "Scientific method component — minimise personal/political bias."),
            T("Integrity of prior work", "Describe process so others can continue or replicate development."),
        ],
        [
            "Criteria judge quality; process sequences the work — both appear in ‘research process’ stems.",
            "Impartiality is required even though researcher philosophy always influences framing.",
            "If scope is too wide or resources thin, refine the problem (feedback in the process).",
        ],
        [
            "Six-step marketing-style process is the usual list — memorise order.",
            "Stem ‘disclose shortcomings of design’ → criteria of good research.",
            "Trap: conclusions must be supported by findings — speculation fails criteria.",
            "Greater trust if researcher has reputation and integrity (exam criterion).",
        ],
    ),
    "1.2.2": pack(
        [
            T("Deductive approach", "Theory → hypothesis → test against observations (general to specific testing)."),
            T("Inductive approach", "Observations → pattern → theory/generalisation."),
            T("Quantitative research", "Numeric measurement, statistical analysis, often hypothesis testing."),
            T("Qualitative research", "Words, meanings, themes — depth over numeric generalisation."),
        ],
        [
            "Deductive fits theory-testing; inductive fits theory-building from data.",
            "Quantitative often pairs with deduction; qualitative often with induction — but not absolute rules.",
            "Deductive benefits: clarify variable links, measure concepts, limited generalisation.",
        ],
        [
            "Stem ‘test hypothesis from existing theory’ → deductive.",
            "Stem ‘find pattern in observations’ → inductive.",
            "Trap: SLM wording sometimes flips ‘specific/general’ — anchor on theory-first vs data-first.",
            "Mixed methods combine both — mention if stem asks for ‘approaches’ broadly.",
        ],
    ),
    "1.2.3": pack(
        [
            T("Research proposal", "Formal plan stating problem, objectives, design, methods, timeline, resources."),
            T("Problem statement", "Clear articulation of the gap or issue to be studied."),
            T("Aspects of a proposal", "Significance, feasibility, scope, ethics, expected contribution."),
            T("Work plan", "Schedule of activities from literature to reporting."),
        ],
        [
            "Proposal sells and guides the study before data collection starts.",
            "Objectives in the proposal must match design and analysis later.",
            "Feasibility (time, access, cost) is as important as intellectual novelty.",
        ],
        [
            "Stem ‘document submitted before starting research’ → proposal.",
            "Link to 5.4.x project-proposal topics for problem definition detail.",
            "Trap: proposal ≠ final report — plan vs results.",
            "Include how you will analyse data, not only how you will collect it.",
        ],
    ),
    "1.2.4": pack(
        [
            T("Literature survey", "Broad scan of existing work, sources, and themes in the field."),
            T("Literature review", "Critical synthesis — compare, critique, identify gaps."),
            T("Secondary sources", "Books, journals, reports, databases used to frame the problem."),
            T("Research gap", "Unanswered question or weakness in prior studies that justifies yours."),
        ],
        [
            "Survey gathers; review evaluates and positions your study.",
            "Good review avoids plagiarism by paraphrase + citation, and shows scholarly conversation.",
            "Gap analysis links Module 1 process to Module 5 reporting/citing.",
        ],
        [
            "Stem ‘critical evaluation of prior studies’ → review, not mere survey list.",
            "Use recent peer-reviewed sources for method and findings, not only textbooks.",
            "Trap: annotated bibliography ≠ analytical literature review.",
            "End review with how your objectives address the gap.",
        ],
    ),
    "1.2.5": pack(
        [
            T("Research error", "Deviation from true value due to design, measurement, sampling, or analysis flaws."),
            T("Bias", "Systematic distortion (selection, response, interviewer, confirmation)."),
            T("Random error", "Unpredictable fluctuation that averages out with larger n (in theory)."),
            T("Non-sampling error", "Frame, non-response, measurement, processing — not due to sample size alone."),
        ],
        [
            "Errors can enter at every process step — problem framing through reporting.",
            "Sampling error (Module 2) is only one class; design/measurement errors matter too.",
            "Disclosing limitations (1.2.1 criteria) is ethical handling of residual error.",
        ],
        [
            "Stem ‘systematic favouring of one outcome’ → bias.",
            "Larger sample reduces sampling error, not necessarily bias.",
            "Trap: Type I/II (Module 4) are decision errors, not the same as measurement error.",
            "Pilot tests catch instrument wording errors early.",
        ],
    ),
    "1.3.1": pack(
        [
            T("Pure (basic) research", "Aims at theory and knowledge for its own sake."),
            T("Applied research", "Aims at solving a practical problem or improving practice."),
            T("Theory–practice link", "Pure work can later enable applications; applied can feed theory."),
        ],
        [
            "Motive differs: curiosity/theory vs immediate use — methods may look similar.",
            "R&D organisations often fund applied work; universities emphasise both.",
            "Same topic can be framed as pure or applied depending on objectives.",
        ],
        [
            "Stem ‘no immediate practical aim / extend theory’ → pure.",
            "Stem ‘improve organisational practice / policy’ → applied.",
            "Trap: applied ≠ unscientific; it still needs systematic method.",
        ],
    ),
    "1.3.2": pack(
        [
            T("Causal research", "Establishes cause–effect (X → Y) via design that supports attribution."),
            T("Correlational research", "Measures association between variables without proving causation."),
            T("Spurious correlation", "Apparent link due to confounder, not true causal path."),
            T("Independent / dependent variable", "IV manipulated or presumed cause; DV measured effect."),
        ],
        [
            "Correlation is necessary but not sufficient for causation.",
            "Experiments strengthen causal claims; surveys often yield correlational evidence.",
            "Causal attribution returns in 3.1.7 with design language.",
        ],
        [
            "Stem ‘does A cause B’ → causal design needed.",
            "Stem ‘relationship / association between’ → correlational.",
            "Trap: ‘linked’ in a stem is not automatic causation.",
            "Control of confounders separates weak association studies from strong causal ones.",
        ],
    ),
    "1.3.3": pack(
        [
            T("Cross-sectional design", "Data at one point in time — snapshot comparison."),
            T("Longitudinal design", "Same variables (often same units) over multiple times — change/trends."),
            T("Panel study", "Longitudinal following the same sample repeatedly."),
            T("Trend / cohort studies", "Repeated samples from population or specific cohort over time."),
        ],
        [
            "Cross-sectional is cheaper/faster; longitudinal better for development and causality over time.",
            "Attrition is a classic longitudinal threat.",
            "One-time survey ≠ longitudinal even if questions ask about the past (recall bias).",
        ],
        [
            "Stem ‘single time point / prevalence’ → cross-sectional.",
            "Stem ‘over months/years / track change’ → longitudinal.",
            "Trap: SLM spelling ‘Crossectional’ still means cross-sectional.",
            "Causal claims are stronger with longitudinal or experimental evidence than one snapshot.",
        ],
    ),
    "1.3.4": pack(
        [
            T("Experimental design", "Manipulate IV, control conditions, measure DV — strong internal validity aim."),
            T("Semi- / quasi-experimental", "Intervention or comparison without full random assignment."),
            T("Non-experimental", "No manipulation — observe, survey, correlate as found."),
            T("Control", "Holding extraneous variables constant or accounting for them."),
        ],
        [
            "Random assignment distinguishes true experiments (Module 3) from quasi designs.",
            "Non-experimental can still be rigorous (e.g., well-sampled surveys) but causal claims weaken.",
            "Ethics/feasibility often force quasi or non-experimental choices.",
        ],
        [
            "Stem ‘researcher manipulates treatment’ → experimental family.",
            "Stem ‘pre-existing groups / no randomisation’ → quasi/semi.",
            "Map to 3.1.2–3.1.4 for design subtypes (one-shot, pretest–posttest, etc.).",
            "Trap: ‘experiment’ in casual speech ≠ true experimental design.",
        ],
    ),
    "1.3.5": pack(
        [
            T("Descriptive research", "Portray characteristics, frequencies, profiles — ‘what is’."),
            T("Exploratory research", "Clarify ambiguous problems, generate insights/hypotheses — early stage."),
            T("Hypothesis generation vs testing", "Exploratory often generates; later designs test."),
        ],
        [
            "Exploratory precedes precise descriptive or causal studies when little is known.",
            "Descriptive answers who/what/where/when; causal answers why/how (with design support).",
            "Both can use surveys; purpose and analysis depth differ.",
        ],
        [
            "Stem ‘map the situation / prevalence’ → descriptive.",
            "Stem ‘little prior knowledge / formulate hypotheses’ → exploratory.",
            "Trap: descriptive statistics ≠ automatically ‘descriptive research design’ label — check purpose.",
        ],
    ),
    "1.4.1": pack(
        [
            T("Model", "Simplified representation of a system or phenomenon for explanation/prediction."),
            T("Physical / iconic models", "Scaled tangible replicas."),
            T("Analogue models", "Use analogous properties (e.g., flow ↔ current) to represent behaviour."),
            T("Mathematical / symbolic models", "Equations and symbols relating variables."),
            T("Conceptual models", "Diagrammatic frameworks of constructs and links."),
        ],
        [
            "Model type chosen by purpose: insight, communication, optimisation, simulation.",
            "All models omit detail — usefulness > perfect realism.",
            "Statistical models in Module 4 are a mathematical subclass used for inference.",
        ],
        [
            "Stem ‘equations relating variables’ → mathematical/symbolic.",
            "Stem ‘scale model of a machine’ → physical/iconic.",
            "Trap: a flowchart conceptual model is still a model — not ‘only maths counts’.",
        ],
    ),
    "1.4.2": pack(
        [
            T("Model building", "Iterative construction of a usable representation from theory and data."),
            T("Stages (typical)", "Problem formulation → structure → parameterisation → evaluation → use/refine."),
            T("Validation", "Check model behaviour against real system or hold-out data."),
            T("Verification", "Check the model is built correctly (implementation/logic)."),
        ],
        [
            "Building stages parallel the research process: define, design, test, report.",
            "Verification ≠ validation — correct build vs correct representation of reality.",
            "Refinement loops when adequacy checks fail (see 4.2.11).",
        ],
        [
            "Exam: list stages in order; mention feedback/refinement.",
            "Stem ‘does the coded model match the intended logic’ → verification.",
            "Stem ‘does output match the real system’ → validation.",
            "Overfitting a statistical model fails adequacy even if R² looks high.",
        ],
    ),
    "1.4.3": pack(
        [
            T("Data consideration", "What data, quality, granularity, and availability the model needs."),
            T("Testing (model)", "Compare predictions/outputs to observations; sensitivity checks."),
            T("Data quality", "Accuracy, completeness, consistency, timeliness."),
            T("Assumptions check", "Confirm distributional/structural assumptions before trusting results."),
        ],
        [
            "Garbage-in → garbage-out: model testing cannot fix fatally flawed data.",
            "Split samples / cross-validation are common testing ideas for predictive models.",
            "Links forward to editing/coding (3.2) and adequacy checking (4.2.11).",
        ],
        [
            "Stem ‘suitability of input data for the model’ → data consideration.",
            "Always state units, period, and population the data represent.",
            "Trap: significant hypothesis test ≠ validated predictive model.",
        ],
    ),
    "1.4.4": pack(
        [
            T("Heuristic modeling", "Rule-of-thumb / approximate methods for hard problems — good-enough solutions."),
            T("Simulation modeling", "Imitate system behaviour over time under scenarios (often computational)."),
            T("What-if analysis", "Vary inputs in a simulation to study outcomes."),
            T("Optimality vs feasibility", "Heuristics may not guarantee global optimum."),
        ],
        [
            "Use heuristics when exact optimisation is intractable; use simulation when closed form is unavailable.",
            "Simulation needs a conceptual model plus data/parameters (1.4.2–1.4.3).",
            "Monte Carlo-style randomness is common in simulation but not required for all sims.",
        ],
        [
            "Stem ‘approximate practical rules’ → heuristic.",
            "Stem ‘computer imitation of system over time’ → simulation.",
            "Trap: simulation ≠ experiment on the real system — it is a model run.",
            "Report random seeds/replication count when simulation results are stochastic.",
        ],
    ),

    # =========================================================================
    # Module 2 — Data collection, questionnaire, sampling
    # =========================================================================
    "2.1.1": pack(  # LMR
        [
            T("Data collection", "Systematic gathering of information relevant to research objectives."),
            T("Primary data", "Collected firsthand by the researcher for the current study."),
            T("Secondary data", "Already existing — published stats, records, prior studies."),
            T("Qualitative vs quantitative data", "Text/observations vs numeric measurements."),
            T("Units of analysis", "Who/what is measured — individuals, firms, events, documents."),
        ],
        [
            "Collection decisions follow objectives and design — not the reverse.",
            "Primary is tailored but costly; secondary is fast but may mismatch concepts.",
            "Ethics: consent, privacy, and accurate recording start at collection.",
        ],
        [
            "LMR: define collection + primary/secondary contrast in one breath.",
            "Stem ‘already published company reports’ → secondary.",
            "Stem ‘new survey you administer’ → primary.",
            "Always state unit of analysis to avoid ecological fallacy later.",
            "Link to 2.1.2 methods and 2.1.3 validation/tabulation.",
            "Trap: big secondary datasets still need validation for your construct definitions.",
        ],
        lmr=True,
    ),
    "2.1.2": pack(  # LMR
        [
            T("Observation", "Record behaviour/events as they occur — structured or unstructured."),
            T("Interview", "Personal (or phone/online) Q&A — structured, semi-structured, unstructured."),
            T("Questionnaire / schedule", "Written instrument; schedule often filled by enumerator."),
            T("Documentary / archival methods", "Extract from records, logs, databases."),
            T("Experiment as collection context", "Measures taken under controlled treatment conditions."),
        ],
        [
            "Method choice trades depth, cost, bias risk, and scalability.",
            "Observation reduces some response bias but may add observer effects.",
            "Interviews allow probes; questionnaires standardise and scale.",
        ],
        [
            "LMR: list major methods and one strength/weakness each.",
            "Stem ‘watch without asking’ → observation; ‘face-to-face probing’ → interview.",
            "Schedule vs questionnaire: who fills it (enumerator vs respondent) is the classic distinction.",
            "Multi-method (triangulation) strengthens credibility.",
            "Trap: ‘survey’ is not one technique — it usually means questionnaire-based collection.",
            "Module 3.2 revisits observation/interview/cases/questionnaires in design context.",
        ],
        lmr=True,
    ),
    "2.1.3": pack(  # LMR
        [
            T("Tabulation", "Organising data into tables/counts for summary and analysis."),
            T("Validation of data", "Checks that entries are complete, consistent, within range, and logical."),
            T("Data cleaning", "Correct or flag errors before statistical analysis."),
            T("Frequency / cross-tabulation", "Univariate counts vs joint distributions of two+ variables."),
            T("Consistency checks", "Skip patterns, impossible combinations, duplicate IDs."),
        ],
        [
            "Validate before analyse — bad tables amplify instrument and field errors.",
            "Tabulation is preparation, not the final inferential test.",
            "Editing/coding detail continues in 3.2.5–3.2.8.",
        ],
        [
            "LMR: tabulating = organise; validating = verify quality/legitimacy.",
            "Stem ‘arrange responses in rows/columns’ → tabulation.",
            "Stem ‘check legitimacy and dependability of data’ → validation (echoes 1.2.1 criteria).",
            "Out-of-range ages or contradictory yes/no paths fail validation.",
            "Document cleaning rules for reproducibility.",
            "Trap: pretty charts ≠ validated data.",
        ],
        lmr=True,
    ),
    "2.2.1": pack(
        [
            T("Questionnaire construction steps", "Objectives → information needs → method → content → wording → sequence → format → pilot → revise."),
            T("Pilot testing", "Small trial to catch ambiguity, length, and skip errors."),
            T("Information needs", "Map each question to an objective or variable."),
        ],
        [
            "Every item should earn its place against objectives — drop orphans.",
            "Pilot before full field work saves non-sampling error.",
            "Mode (online/paper/interview) constrains wording and length.",
        ],
        [
            "Exam: recite sequential steps; emphasise pilot/revise.",
            "Stem ‘pre-test the instrument’ → pilot.",
            "Trap: writing questions before clarifying objectives produces irrelevant items.",
        ],
    ),
    "2.2.2": pack(
        [
            T("Open-ended questions", "Free response — rich detail, harder to code."),
            T("Closed-ended questions", "Fixed options — easy to tabulate, risk forcing choices."),
            T("Dichotomous / multiple choice", "Yes–no or several alternatives."),
            T("Rating / Likert-type items", "Ordered agreement or intensity scales."),
            T("Ranking questions", "Order preferences among options."),
        ],
        [
            "Open for exploration; closed for quantification and comparison.",
            "Poor options create measurement bias (missing ‘other’, double-barrelled stems).",
            "Scale level (nominal/ordinal/interval) later constrains parametric tests.",
        ],
        [
            "Stem ‘respondent writes own words’ → open-ended.",
            "Stem ‘select from listed options’ → closed.",
            "Avoid double-barrelled and leading questions in any type.",
            "Trap: Likert is ordinal by strict view — still often treated as interval in exams if stated.",
        ],
    ),
    "2.2.3": pack(
        [
            T("Questionnaire format", "Layout, sections, instructions, skip patterns, visual design."),
            T("Question sequence", "Easy/warm-up → main → sensitive last; funnel from general to specific."),
            T("Skip logic", "Route respondents past irrelevant blocks."),
            T("Cover / intro", "Purpose, confidentiality, estimated time — raises response quality."),
        ],
        [
            "Format affects response rate and error as much as wording.",
            "Crowded pages and unclear instructions inflate Don’t Know / missing (3.2.7–3.2.8).",
            "Consistent scale direction reduces careless answering.",
        ],
        [
            "Stem ‘order and layout of items’ → format/sequence.",
            "Put demographics usually at end unless needed for screening.",
            "Trap: pretty design cannot fix invalid constructs — still need validity (3.3.1).",
        ],
    ),
    "2.3.1": pack(
        [
            T("Sampling plan", "Framework specifying population, frame, method, size, and execution procedures."),
            T("Target population", "Universe to which you want to generalise."),
            T("Sample size", "n chosen for precision, power, cost, and design effect."),
        ],
        [
            "Plan before fieldwork — ad hoc convenience sampling weakens inference.",
            "Size without a method still leaves selection bias risk.",
            "Plan documents inclusion/exclusion and replacement rules.",
        ],
        [
            "Stem ‘framework research projects rely on for sampling’ → sampling plan.",
            "Always name population + method + n in exam answers.",
            "Trap: large n does not fix a biased selection method.",
        ],
    ),
    "2.3.2": pack(
        [
            T("Sampling frame", "List or database of population members from which the sample is drawn."),
            T("Frame coverage", "Undercoverage / overcoverage relative to the target population."),
            T("Frame error", "Mismatch between frame and true population — a non-sampling error."),
        ],
        [
            "No probability sample without a workable frame (or equivalent listing mechanism).",
            "Updating frames (students enrolled this term) matters for currency.",
            "Web panels and incomplete registries are classic imperfect frames.",
        ],
        [
            "Stem ‘list/database of members’ → sampling frame.",
            "Population ≠ frame when some units are missing or ineligible units appear.",
            "Trap: using an employee email list to study ‘all citizens’ is frame bias.",
            "State the frame explicitly in methods sections.",
        ],
    ),
    "2.3.3": pack(
        [
            T("Sample selection methods", "Broadly: probability vs non-probability procedures."),
            T("Random selection", "Each eligible unit has a known (often equal) chance."),
            T("Purposive selection", "Units chosen by judgment for relevance — non-probability."),
        ],
        [
            "Selection method drives whether sampling error theory and CIs apply cleanly.",
            "2.3.4 and 2.3.5 unpack the two families.",
            "Multi-stage designs combine techniques (e.g., cluster then SRS).",
        ],
        [
            "First branch exam answer: probability vs non-probability.",
            "Stem ‘known nonzero probability’ → probability family.",
            "Trap: ‘random’ in casual speech ≠ statistical random sample.",
        ],
    ),
    "2.3.4": pack(
        [
            T("Simple random sampling (SRS)", "Every sample of size n equally likely; known inclusion probabilities."),
            T("Systematic sampling", "Every k-th unit after a random start."),
            T("Stratified sampling", "Independent samples from homogeneous strata — precision gain."),
            T("Cluster sampling", "Sample clusters then units — cost efficient, design effect usually ↑."),
            T("Multistage sampling", "Hierarchical selection (e.g., districts → schools → students)."),
        ],
        [
            "Probability ⇒ can estimate sampling error and use inferential machinery more defensibly.",
            "Stratify on variables related to the DV; cluster when lists of individuals are costly.",
            "Systematic fails if frame has hidden periodicity matching k.",
        ],
        [
            "Stem ‘divide into groups then random within’ → stratified.",
            "Stem ‘select whole groups first’ → cluster.",
            "Trap: stratified ≠ quota (quota is non-probability unless randomised within).",
            "Name at least three techniques in long answers.",
        ],
    ),
    "2.3.5": pack(
        [
            T("Convenience sampling", "Easily available units — fast, high bias risk."),
            T("Judgment / purposive sampling", "Expert picks ‘typical’ or information-rich cases."),
            T("Quota sampling", "Fill demographic quotas without random selection within cells."),
            T("Snowball sampling", "Respondents recruit peers — hidden populations."),
        ],
        [
            "Unknown selection probabilities limit generalisation and classic sampling-error formulas.",
            "Useful for exploratory/qualitative work; weak for population parameter estimates.",
            "Quota looks like stratified but lacks random draws inside quotas.",
        ],
        [
            "Stem ‘first 50 shoppers who agree’ → convenience.",
            "Stem ‘ask respondents to refer others’ → snowball.",
            "Trap: non-probability ≠ always ‘wrong’ — wrong when claiming representative population estimates.",
            "Disclose method limitations in the report.",
        ],
    ),
    "2.3.6": pack(
        [
            T("Sampling error", "Error because only a sample is observed — decreases as n increases (given good design)."),
            T("Non-sampling error", "Frame, non-response, measurement, processing, interviewer bias — not fixed by larger n alone."),
            T("Non-response error", "Difference because non-respondents differ systematically from respondents."),
            T("Total survey error", "Combined sampling + non-sampling components."),
        ],
        [
            "Trade-off: huge n with poor instrument can worsen non-sampling error more than it helps.",
            "Probability samples quantify sampling error; non-sampling needs process quality control.",
            "Links to validation (2.1.3) and Type I/II are different concepts (decision vs measurement).",
        ],
        [
            "Stem ‘error due to using sample not census’ → sampling error.",
            "Stem ‘wrong question wording / bad frame’ → non-sampling.",
            "Trap: ‘reduce error by bigger sample’ is incomplete — say which error.",
            "Report response rate as a non-response quality indicator.",
        ],
    ),

    # =========================================================================
    # Module 3 — Experiments, field data, principles
    # =========================================================================
    "3.1.1": pack(  # LMR
        [
            T("Design of experiments (DOE)", "Plan to study factor effects on responses with controlled variation."),
            T("Objectives of DOE", "Compare treatments, estimate effects/interactions, minimise error variance, support causal claims."),
            T("Strategies", "Replication, randomisation, blocking; choose factors/levels; define response metrics."),
            T("Treatment", "A controlled condition or factor-level combination applied to experimental units."),
            T("Experimental unit", "Smallest entity independently randomised to a treatment."),
        ],
        [
            "DOE is methodology for causal/engineering experiments — not just ‘running a test once’.",
            "Strategy balances precision (replication/blocking) and validity (randomisation).",
            "Factorial thinking (3.1.5) starts from objectives: which factors and interactions matter.",
        ],
        [
            "LMR: objectives + three principles (replication, randomisation, blocking) often co-tested.",
            "Stem ‘minimise noise / isolate factor effects’ → DOE objectives.",
            "Define response variable and factors before picking a design label.",
            "Trap: observing a natural event ≠ designed experiment.",
            "Engineering experiments (3.1.6) apply the same principles to processes/products.",
            "Link forward to ANOVA (4.2.7+) for analysing designed data.",
        ],
        lmr=True,
    ),
    "3.1.2": pack(  # LMR
        [
            T("Pre-experimental designs", "Weak control — limited basis for causal inference."),
            T("One-shot case study", "X then O — no pretest, no control group."),
            T("One-group pretest–posttest", "O1 X O2 — history/maturation threaten validity."),
            T("Static-group comparison", "X O vs O — groups not randomly assigned."),
        ],
        [
            "Pre-experimental lacks random assignment and often lacks adequate controls.",
            "Useful for pilots/ideas, weak for strong causal claims.",
            "Threats: history, maturation, testing, selection, mortality.",
        ],
        [
            "LMR: name the three classic Campbell–Stanley-style pre-experimental forms.",
            "Stem ‘treat then observe only’ → one-shot.",
            "Stem ‘same group before/after, no control’ → one-group pretest–posttest.",
            "Trap: pretest–posttest alone ≠ true experiment.",
            "Compare to quasi (3.1.3) and true (3.1.4) on control features.",
            "Exam phrase: ‘inadequate for rigorous causal attribution’.",
        ],
        lmr=True,
    ),
    "3.1.3": pack(  # LMR
        [
            T("Quasi-experimental design", "Intervention/comparison without full random assignment."),
            T("Nonequivalent control group", "Pretest–posttest with comparison group not randomised."),
            T("Interrupted time series", "Many observations before/after intervention on a series."),
            T("Selection threat", "Groups differ at baseline — confounds treatment effect."),
        ],
        [
            "Stronger than pre-experimental when trends/controls are used carefully.",
            "Weaker internal validity than true experiments due to selection confounds.",
            "Common in field/policy/education where randomisation is blocked.",
        ],
        [
            "LMR: ‘no random assignment but has comparison/structure’ → quasi.",
            "Stem ‘intact classrooms compared’ → nonequivalent groups / quasi.",
            "Time series helps against maturation but not all confounds.",
            "Trap: quasi ≠ ‘almost any non-survey design’.",
            "Report baseline differences and adjustment strategies.",
            "Causal language must be hedged relative to randomised trials.",
        ],
        lmr=True,
    ),
    "3.1.4": pack(
        [
            T("True experimental design", "Random assignment to treatments — gold standard internal validity."),
            T("Pretest–posttest control group", "R: O1 X O2 vs O1  O2."),
            T("Posttest-only control group", "R: X O vs O — avoids pretest sensitisation."),
            T("Solomon four-group", "Combines pretest and posttest-only arms to detect testing effects."),
        ],
        [
            "Randomisation equates groups in expectation on known and unknown confounders.",
            "Control group estimates the counterfactual without treatment.",
            "True experiments still need proper measurement and ethics.",
        ],
        [
            "Stem ‘randomly assigned treatment and control’ → true experimental.",
            "Solomon four-group is the classic ‘detect pretest interaction’ design.",
            "Trap: random sampling ≠ random assignment (population vs causal internal validity).",
        ],
    ),
    "3.1.5": pack(
        [
            T("Factorial design", "Two+ factors studied so main effects and interactions are estimable."),
            T("Main effect", "Effect of one factor averaged over levels of others."),
            T("Interaction", "Effect of one factor depends on the level of another."),
            T("2×2 factorial", "Simplest two-factor, two-level layout — four treatment cells."),
        ],
        [
            "Factorials are efficient versus one-factor-at-a-time for discovering interactions.",
            "ANOVA for factorial partitions variance into main effects, interaction, error.",
            "Orthogonality (3.3.3) keeps effect estimates independent in balanced designs.",
        ],
        [
            "Stem ‘study A and B together / interaction’ → factorial.",
            "Significant interaction ⇒ interpret simple effects, not only main effects.",
            "Trap: more factors explode cell counts — need replication planning.",
        ],
    ),
    "3.1.6": pack(
        [
            T("Engineering experiments", "DOE applied to products/processes — quality, yield, robustness."),
            T("Factors & levels", "Controllable process inputs set by the engineer."),
            T("Response metrics", "Output quality characteristics (strength, defect rate, latency)."),
            T("Robust design idea", "Reduce sensitivity to noise factors."),
        ],
        [
            "Same statistical principles as behavioural experiments; domain responses differ.",
            "Often uses factorial/fractional factorial and ANOVA/regression.",
            "Safety and operating constraints limit the experimental region.",
        ],
        [
            "Stem ‘plant process factors / product quality’ → engineering DOE framing.",
            "State controllable vs noise factors in answers.",
            "Trap: one successful run ≠ designed experiment with replication.",
        ],
    ),
    "3.1.7": pack(
        [
            T("Causal attribution", "Concluding that the treatment caused the observed change in the DV."),
            T("Covariation", "Cause and effect must associate."),
            T("Temporal precedence", "Cause occurs before effect."),
            T("Nonspuriousness", "No plausible confounder explains the link."),
        ],
        [
            "Design (randomisation/control) is the main tool for nonspuriousness.",
            "Correlational designs struggle on temporal order and confounds.",
            "Statistical control (3.1.8) helps but is not a full substitute for randomisation.",
        ],
        [
            "Exam triad: covariation + time order + rule out alternatives.",
            "Stem ‘can we say X caused Y’ → discuss design threats, not only p-values.",
            "Trap: significant correlation ≠ causal attribution.",
        ],
    ),
    "3.1.8": pack(
        [
            T("Statistical control", "Adjust for covariates (ANCOVA, regression) to reduce confounding."),
            T("Covariate", "Variable correlated with DV that you measure and partial out."),
            T("Blocking (related)", "Design-time control by grouping similar units — see 3.3.2."),
            T("Residual confounding", "Bias left when important confounders are unmeasured/mismeasured."),
        ],
        [
            "Control by design (randomise/block) beats control only by statistics when possible.",
            "ANCOVA assumes covariate measured before treatment and linear relationships, etc.",
            "Over-controlling mediators can wrongly remove part of the causal path.",
        ],
        [
            "Stem ‘hold Z constant statistically’ → statistical control.",
            "Mention assumption risks in long answers.",
            "Trap: ‘controlled for everything’ is never literally true.",
        ],
    ),
    "3.2.1": pack(
        [
            T("Observation (field)", "Passive or participatory recording of behaviour in context."),
            T("Interview (field)", "Structured to unstructured verbal data collection."),
            T("Structured observation", "Preset categories/checklists — higher reliability potential."),
            T("Unstructured interview", "Flexible probes — rich qualitative data."),
        ],
        [
            "Complements questionnaires when behaviour ≠ self-report.",
            "Observer drift and reactivity are threats — train and calibrate observers.",
            "Ethics: covert observation is restricted; consent norms apply.",
        ],
        [
            "Contrast observation (see) vs interview (ask).",
            "Stem ‘checklist of behaviours every 5 minutes’ → structured observation.",
            "Trap: interview transcripts still need coding rules (3.2.6).",
        ],
    ),
    "3.2.2": pack(
        [
            T("Case study method", "In-depth study of a bounded case (person, firm, event, system)."),
            T("Case data sources", "Interviews, documents, observation — triangulation."),
            T("Analytic generalisation", "To theory, not always to a statistical population."),
        ],
        [
            "Cases excel at context and process; weak for prevalence estimates alone.",
            "Multiple cases strengthen pattern matching versus single anecdote.",
            "Not the same as a legal ‘case’ or a single questionnaire respondent.",
        ],
        [
            "Stem ‘detailed investigation of one organisation’ → case study.",
            "State bounding of the case and data sources.",
            "Trap: n=1 case ≠ census; mind generalisation claims.",
        ],
    ),
    "3.2.3": pack(
        [
            T("Questionnaire data collection", "Standardised items administered to a sample."),
            T("Self-administered vs interviewer-administered", "Mode affects bias, cost, literacy needs."),
            T("Response rate", "Share of sample that completes — quality indicator."),
        ],
        [
            "Builds on Module 2.2 design; here emphasis is collection execution.",
            "Mode effects: social desirability higher in interviewer modes for sensitive topics.",
            "Follow-ups and incentives are practical response-rate tools.",
        ],
        [
            "Link each batch to the sampling plan (2.3.1).",
            "Stem ‘mail/online form completed by respondent’ → self-administered questionnaire.",
            "Trap: collecting without a codebook makes 3.2.6 painful later.",
        ],
    ),
    "3.2.4": pack(
        [
            T("Questionnaire guidelines", "Clear wording, one idea per item, balanced options, neutral tone."),
            T("Avoid leading / loaded items", "Do not push toward a socially desired answer."),
            T("Avoid double-barrelled items", "Split ‘and/or’ compounds into separate questions."),
            T("Appropriate length & language", "Match respondent literacy and attention."),
        ],
        [
            "Guidelines operationalise validity/reliability before statistics.",
            "Translate/back-translate for multilingual studies.",
            "Sensitive items need privacy assurances and careful placement.",
        ],
        [
            "Exam: list 4–5 concrete guidelines with a bad vs good example.",
            "Stem ‘two questions in one’ → double-barrelled flaw.",
            "Trap: jargon and negations (‘not infrequently’) inflate error.",
        ],
    ),
    "3.2.5": pack(
        [
            T("Data editing", "Review raw data for completeness, consistency, legibility, and accuracy."),
            T("Field editing", "Quick checks by supervisors during collection."),
            T("Central editing", "Office/system review after data arrive."),
            T("Treatment of unsatisfactory responses", "Call-backs, discard rules, or imputation policy."),
        ],
        [
            "Editing precedes coding and analysis — catches non-sampling errors early.",
            "Rules must be documented for auditability.",
            "Over-editing that ‘forces’ consistency can invent data — unethical.",
        ],
        [
            "Stem ‘scrutinise questionnaires for errors before coding’ → editing.",
            "Distinguish field vs central editing in long answers.",
            "Trap: editing ≠ analysing hypotheses.",
        ],
    ),
    "3.2.6": pack(
        [
            T("Data coding", "Assigning numeric/symbolic codes to responses for analysis."),
            T("Codebook", "Defines codes, labels, missing values, skip patterns."),
            T("Coding rules", "Mutual exclusivity, exhaustiveness, consistency across coders."),
            T("Intercoder reliability", "Agreement when multiple coders label open responses."),
        ],
        [
            "Closed items are pre-coded; open items need coding frames.",
            "Bad coding creates measurement error indistinguishable from ‘findings’.",
            "Keep raw text when possible for audit of open-ended codes.",
        ],
        [
            "Stem ‘convert answers to numbers for computer analysis’ → coding.",
            "Exhaustive + mutually exclusive categories is a classic rule pair.",
            "Trap: reusing code ‘9’ for both ‘age 9’ and ‘missing’ without scheme — disaster.",
        ],
    ),
    "3.2.7": pack(
        [
            T("Don’t Know (DK) responses", "Explicit option or spontaneous DK — signals uncertainty or item failure."),
            T("DK as data", "May be substantive (no opinion) or instrument defect."),
            T("Handling DK", "Separate code, probe, or exclude per analysis plan — don’t silently coerce."),
        ],
        [
            "High DK rates flag wording, knowledge mismatch, or sensitive topics.",
            "Forcing a choice when knowledge is absent adds measurement error.",
            "Report DK rates as a quality diagnostic.",
        ],
        [
            "Stem ‘respondent selects Don’t Know’ → code distinctly; analyse carefully.",
            "Trap: treating DK as neutral midpoint on Likert without justification.",
            "Link to missing-data topic 3.2.8 when DK is later blanked.",
        ],
    ),
    "3.2.8": pack(
        [
            T("Missing data", "Absent values due to skip, refusal, dropout, or sensor failure."),
            T("MCAR / MAR / MNAR (exam awareness)", "Missing completely at random / at random / not at random — bias implications."),
            T("Listwise deletion", "Drop cases with any missing — simple, can bias and lose power."),
            T("Imputation", "Fill values by mean/regression/multiple imputation — assumptions required."),
        ],
        [
            "Mechanism of missingness matters more than the mere count of holes.",
            "Prevent missingness via design; handle residual missingness transparently.",
            "Multiple imputation is preferred in modern practice when MAR is plausible.",
        ],
        [
            "Stem ‘blank fields after editing’ → missing data problem.",
            "Always report % missing and the handling rule.",
            "Trap: mean imputation shrinks variance and distorts correlations.",
        ],
    ),
    "3.3.1": pack(
        [
            T("Validity", "Instrument/design measures what it claims — accuracy of inference."),
            T("Reliability", "Consistency / repeatability of measurement."),
            T("Internal validity", "Causal conclusion correctness inside the study."),
            T("External validity", "Generalisation to other people, settings, times."),
            T("Types (measurement)", "Content, criterion, construct validity; test–retest, parallel, internal consistency reliability."),
        ],
        [
            "Reliability is necessary but not sufficient for validity.",
            "True experiments boost internal validity; sampling design boosts external validity.",
            "Cronbach’s α is a common internal-consistency reliability index (exam name-drop).",
        ],
        [
            "Stem ‘consistent scores across occasions’ → reliability.",
            "Stem ‘measures the intended construct’ → validity.",
            "Trap: high α ≠ proof of unidimensional valid construct.",
            "Threats to internal validity: history, maturation, selection, mortality, testing, instrumentation.",
        ],
    ),
    "3.3.2": pack(
        [
            T("Replication", "Repeat treatments to estimate pure error and improve precision."),
            T("Randomisation", "Allocate units to treatments by chance — unbiased comparison."),
            T("Blocking", "Group similar units; randomise within blocks to remove known noise."),
            T("Fisher’s principles", "Classical DOE triad: replicate, randomise, block."),
        ],
        [
            "Replication ≠ pseudoreplication (repeated measures on one unit miscounted as independent).",
            "Blocking is design analogue of statistical control for known nuisance factors.",
            "Without randomisation, blocks/controls still leave selection threats.",
        ],
        [
            "LMR-adjacent: name all three principles in DOE answers (also 3.1.1).",
            "Stem ‘group by machine/shift then randomise’ → blocking.",
            "Trap: one observation per treatment with no replication — cannot estimate error well.",
        ],
    ),
    "3.3.3": pack(
        [
            T("Orthogonality (design)", "Factor columns uncorrelated — main-effect estimates independent in balanced factorials."),
            T("False positive", "Declaring an effect real when it is not — Type I error analogue."),
            T("Multiple testing problem", "Many comparisons inflate family-wise false positive rate."),
            T("α control", "Use planned contrasts, Bonferroni/FDR, or pre-registered primary outcomes."),
        ],
        [
            "Orthogonal designs simplify interpretation and variance allocation.",
            "False positives link design multiplicity to hypothesis testing (Module 4 Type I).",
            "Fishing through many endpoints without correction is an exam critique target.",
        ],
        [
            "Stem ‘independent estimation of factor effects’ → orthogonality.",
            "Stem ‘significant by chance among many tests’ → false positive / multiplicity.",
            "Trap: p < 0.05 on one of 40 unplanned tests is weak evidence.",
        ],
    ),

    # =========================================================================
    # Module 4 — Hypothesis testing & parametric tests
    # =========================================================================
    "4.1.1": pack(  # LMR
        [
            T("Hypothesis", "Testable statement about a population parameter or relationship."),
            T("Research hypothesis", "Substantive claim the study investigates (often mirrors H1)."),
            T("Statistical hypothesis", "Formal H0/H1 about parameters used in testing."),
            T("Testable", "Must be falsifiable with data — not vague value judgments."),
        ],
        [
            "Hypothesis bridges theory and data — Module 1 objectives become testable claims here.",
            "Not all studies test hypotheses (purely descriptive), but this module assumes they do.",
            "Good hypotheses specify variables, direction (if any), and population.",
        ],
        [
            "LMR: define hypothesis + ‘testable/falsifiable’ + link to data.",
            "Stem ‘tentative proposition awaiting empirical test’ → hypothesis.",
            "Trap: prediction without variables/population is a weak hypothesis statement.",
            "Distinguish research question (ask) from hypothesis (claim).",
            "Next cards formalise H0/H1 and error types.",
            "Directional vs non-directional wording sets up one- vs two-tailed tests.",
        ],
        lmr=True,
    ),
    "4.1.2": pack(  # LMR
        [
            T("Null hypothesis (H0)", "Statement of no effect / no difference / status quo — tested for possible rejection."),
            T("Alternative hypothesis (H1 / Ha)", "Statement of effect/difference the researcher entertains."),
            T("Two-sided H1", "Parameter ≠ value (difference in either direction)."),
            T("One-sided H1", "Parameter > or < value (direction specified)."),
            T("Fail to reject H0", "Data insufficient to discard H0 — not proof H0 is true."),
        ],
        [
            "Tests put H0 at risk; science progresses by rejecting untenable nulls.",
            "H1 direction must be justified a priori for one-tailed testing.",
            "Equality usually lives in H0 for classical Neyman–Pearson setups.",
        ],
        [
            "LMR: write H0: μ = μ0 vs H1: μ ≠ μ0 (or > / <) as templates.",
            "Stem ‘no significant difference’ → H0 wording.",
            "Trap: ‘accept H0’ is sloppy — prefer ‘fail to reject’.",
            "Never put the research claim only in H0 if you hope to ‘prove’ it by rejection logic.",
            "p-value is computed under H0 assumed true.",
            "Match H1 to one-/two-tailed critical regions (4.1.4, 4.1.8).",
        ],
        lmr=True,
    ),
    "4.1.3": pack(  # LMR
        [
            T("Type I error (α)", "Reject H0 when H0 is true — false positive."),
            T("Type II error (β)", "Fail to reject H0 when H1 is true — false negative / miss."),
            T("Significance level α", "Pre-set maximum P(Type I) — commonly 0.05 or 0.01."),
            T("Power (1 − β)", "Probability of correctly rejecting false H0."),
            T("Trade-off", "Lowering α typically raises β unless n increases."),
        ],
        [
            "Error types are about decisions, not sampling error (2.3.6).",
            "Power rises with n, effect size, and α; falls with noise.",
            "False positives (3.3.3) in multiplicity are Type I phenomena across tests.",
        ],
        [
            "LMR mnemonic: Type I — Innocent rejected (false alarm); Type II — Miss the effect.",
            "Stem ‘conclude drug works when it doesn’t’ → Type I.",
            "Stem ‘miss a real difference’ → Type II.",
            "State α before seeing data in proper procedure.",
            "Trap: non-significant result ≠ proof of no effect (β may be large).",
            "Report power or justify n when claiming ‘no difference’.",
        ],
        lmr=True,
    ),
    "4.1.4": pack(
        [
            T("One-tailed test", "Rejection region in one tail — directional H1."),
            T("Two-tailed test", "Rejection region split across both tails — non-directional H1."),
            T("Critical value", "Cutoff on the test-statistic scale for rejection at α."),
        ],
        [
            "Same α: one-tailed critical value is closer to the centre than each two-tailed tail’s share.",
            "Choosing one-tailed after seeing data is p-hacking — unjustified.",
            "CI duality: two-tailed tests align with two-sided confidence intervals.",
        ],
        [
            "Stem ‘H1: μ > 100’ → one-tailed right.",
            "Stem ‘H1: μ ≠ 100’ → two-tailed.",
            "Trap: reporting only one tail to ‘get significance’ without prior justification.",
        ],
    ),
    "4.1.5": pack(
        [
            T("Degrees of freedom (df)", "Number of independent pieces of information for an estimate/test."),
            T("t df example", "One-sample t: df = n − 1 (mean estimated)."),
            T("χ² / F df", "Depend on categories or numerator/denominator sample structure."),
            T("Why df matters", "Critical values from t/χ²/F tables depend on df."),
        ],
        [
            "Each parameter estimated from data typically costs one df.",
            "ANOVA df split across treatments and error (4.2.8).",
            "Large df → t approaches z.",
        ],
        [
            "Stem ‘n−1 for sample variance/t’ → classic one-sample df.",
            "Always state df with t/F reporting.",
            "Trap: using z critical values for small n with unknown σ — wrong distribution.",
        ],
    ),
    "4.1.6": pack(
        [
            T("Confidence interval (CI)", "Range of plausible parameter values at a stated confidence level."),
            T("Confidence level", "Long-run proportion of intervals that cover the true parameter (e.g., 95%)."),
            T("Margin of error", "Half-width of a symmetric CI — depends on SE and critical value."),
            T("CI ↔ test link", "If H0 value lies outside (1−α) CI, two-sided test rejects at α."),
        ],
        [
            "CI estimates magnitude; hypothesis test gives reject/not decision — complementary.",
            "Narrower CI from larger n or smaller variance.",
            "Misread: 95% CI does not mean P(parameter in this interval)=0.95 after seeing data (frequentist subtlety) — exams often want coverage idea.",
        ],
        [
            "Stem ‘range with 95% confidence’ → CI.",
            "Report estimate ± margin or (lower, upper).",
            "Trap: CI for mean ≠ prediction interval for a new observation.",
        ],
    ),
    "4.1.7": pack(
        [
            T("Level of significance (α)", "Probability threshold for Type I error set by the researcher."),
            T("Confidence coefficient (1 − α)", "Complement of significance level — basis for CI confidence level."),
            T("Conventional α", "0.05 common; 0.01 stricter; domain-driven choices exist."),
        ],
        [
            "α is chosen before testing; it is not the p-value.",
            "Smaller α means stronger evidence required to reject H0.",
            "Confidence coefficient naming emphasises the CI duality.",
        ],
        [
            "Stem ‘probability of rejecting true H0’ → α / significance level.",
            "Stem ‘0.95 when α=0.05’ → confidence coefficient.",
            "Trap: ‘result is 95% significant’ — wrong phrasing; say significant at 5% level.",
        ],
    ),
    "4.1.8": pack(
        [
            T("Rejection region", "Set of test-statistic values leading to reject H0."),
            T("Non-rejection (acceptance) region", "Values where you fail to reject H0."),
            T("Critical region placement", "One or both tails depending on H1."),
            T("Observed statistic", "Computed from sample — compare to critical value or via p-value."),
        ],
        [
            "Regions partition the statistic’s support under the null distribution.",
            "p-value approach: reject if p ≤ α — equivalent decision rule when set up correctly.",
            "Borderline values need pre-stated equality conventions.",
        ],
        [
            "Stem ‘values of z that cause rejection’ → rejection region.",
            "Sketch tails in long answers for one- vs two-tailed.",
            "Trap: non-rejection ≠ proving H0; it is insufficient evidence against it.",
        ],
    ),
    "4.1.9": pack(
        [
            T("Hypothesis testing procedure", "State H0/H1 → choose α → select test → assumptions check → compute statistic/p → decide → interpret in context."),
            T("Assumptions", "Independence, distributional form, variance equality as required."),
            T("Decision rule", "Compare statistic to critical value or p to α."),
            T("Substantive conclusion", "Translate reject/fail into research language — not only ‘significant’."),
        ],
        [
            "Procedure is standardised — marks for order and interpretation.",
            "Skipping assumption checks risks invalid Type I/II rates.",
            "Effect size and CI enrich bare significance calls.",
        ],
        [
            "Memorise the step list for 6–8 mark answers.",
            "Always end with meaning for the original research question.",
            "Trap: computing a t without stating H0/H1 first.",
        ],
    ),
    "4.1.10": pack(
        [
            T("Parametric tests", "Assume distributional form (often normality) about parameters — z, t, F, ANOVA."),
            T("Non-parametric tests", "Fewer distribution assumptions — rank/sign based (χ², Mann–Whitney, etc.)."),
            T("One-sample / two-sample / k-sample", "Classifies tests by how many groups/populations."),
        ],
        [
            "Module 4.2 focuses parametric; know non-parametric exist when assumptions fail.",
            "χ² goodness-of-fit/independence often taught alongside even if ‘non-parametric’.",
            "Test type ≠ research type (exploratory etc.) — different axes.",
        ],
        [
            "Stem ‘assume normal population’ → parametric family.",
            "Stem ‘ranks / distribution-free’ → non-parametric.",
            "Trap: using ANOVA on wildly non-normal tiny samples without comment.",
        ],
    ),
    "4.1.11": pack(
        [
            T("Selecting a test", "Match: hypothesis, data level, #groups, paired vs independent, σ known?, n."),
            T("z vs t for means", "z if σ known (or large-n approx); t if σ unknown and normal-ish."),
            T("Paired vs independent", "Same units twice → paired t; separate samples → two-sample t."),
            T("ANOVA when", "Compare means across 3+ groups (avoid uncorrected pairwise t’s)."),
        ],
        [
            "Wrong test = wrong assumptions = wrong error rates.",
            "Measurement scale gates means vs medians vs proportions.",
            "Flowchart thinking scores well in exams.",
        ],
        [
            "Decision tree: parameter (mean/prop/var) → samples → known σ → choose statistic.",
            "Stem ‘three teaching methods, compare means’ → ANOVA.",
            "Trap: multiple t-tests without α correction instead of ANOVA.",
        ],
    ),
    "4.2.1": pack(
        [
            T("Important parametric tests", "z-test, t-test, F-test, ANOVA — on means/variances under assumptions."),
            T("Normality assumption", "Population or sampling distribution approximately normal."),
            T("Homogeneity of variance", "Equal σ² across groups for classic two-sample t / ANOVA."),
        ],
        [
            "Parametric power is higher when assumptions hold versus many non-parametric alternatives.",
            "Central Limit Theorem justifies z approx for large n even if population is non-normal.",
            "4.2.2–4.2.11 specialise these tests.",
        ],
        [
            "List major parametric tests and the parameter each targets.",
            "State assumptions explicitly in answers.",
            "Trap: ‘parametric’ does not mean ‘uses parameters in H0 only’ — all tests have parameters; it means distributional model.",
        ],
    ),
    "4.2.2": pack(
        [
            T("z-test for mean", "H0 about μ when σ known (or large-sample): z = (x̄ − μ0) / (σ/√n)."),
            T("Standard error of mean", "σ/√n — variability of x̄."),
            T("Large-sample practice", "Sometimes replace σ by s when n is large."),
        ],
        [
            "Use when population SD known — rare in practice, common in exams.",
            "Compare |z| to zα or zα/2 critical values.",
            "Equivalent CI: x̄ ± zα/2 · σ/√n.",
        ],
        [
            "Write formula + decision rule in numerical questions.",
            "Stem ‘σ known’ → z over t.",
            "Trap: using σ/√n with sample σ claimed ‘known’ incorrectly.",
        ],
    ),
    "4.2.3": pack(
        [
            T("One-sample t-test", "σ unknown: t = (x̄ − μ0) / (s/√n), df = n − 1."),
            T("Student’s t distribution", "Heavier tails than z; depends on df."),
            T("Assumptions", "Independent observations; approximately normal population (esp. small n)."),
        ],
        [
            "Default mean test when σ unknown.",
            "As df↑, t critical values → z critical values.",
            "Report t, df, p, and CI for μ.",
        ],
        [
            "Stem ‘s instead of σ’ → t-statistic.",
            "Show df = n−1 in working.",
            "Trap: paired data need paired t, not one-sample on raw unpaired list without differencing.",
        ],
    ),
    "4.2.4": pack(
        [
            T("Test for proportion", "H0: p = p0; z ≈ (p̂ − p0) / √(p0(1−p0)/n) under conditions."),
            T("Sample proportion p̂", "x/n successes in Bernoulli/binomial setup."),
            T("Success–failure condition", "np0 and n(1−p0) large enough for normal approx."),
        ],
        [
            "Binary outcomes → proportions, not means of continuous Y.",
            "Two-proportion z-tests compare independent groups.",
            "Exact binomial tests used when n small.",
        ],
        [
            "Stem ‘percentage of defectives / voters’ → proportion test.",
            "Use p0 in SE under H0 for classic score-style z.",
            "Trap: applying t-for-means formulas to 0/1 data without thinking proportion model.",
        ],
    ),
    "4.2.5": pack(
        [
            T("Variance test (χ²)", "H0: σ² = σ0²; χ² = (n−1)s² / σ0² with df = n−1 (normal data)."),
            T("One-sided variance alternatives", "σ² > or < σ0² — process control contexts."),
            T("Normality sensitivity", "χ² variance tests are sensitive to non-normality."),
        ],
        [
            "Used in quality control when variability itself is the claim.",
            "Distinct from tests about means — different parameter.",
            "CI for variance uses χ² quantiles inverted.",
        ],
        [
            "Stem ‘population variance equals hypothesised value’ → χ² variance test.",
            "State normality assumption.",
            "Trap: confusing this with two-variance F-test (4.2.6).",
        ],
    ),
    "4.2.6": pack(
        [
            T("F-test for two variances", "H0: σ1² = σ2²; F = s1²/s2² with df1=n1−1, df2=n2−1."),
            T("Normal populations", "Classic F variance test assumes normality in both groups."),
            T("Equal-variance check", "Often preliminary to Student’s two-sample t (vs Welch)."),
        ],
        [
            "Place larger s² on top if using upper-tail tables carefully — follow your SLM convention.",
            "Levene/Brown–Forsythe are more robust alternatives in modern practice.",
            "ANOVA’s F is related but tests mean equality via variance ratios of mean squares.",
        ],
        [
            "Stem ‘equality of variances of two normal populations’ → F-test.",
            "Report both dfs.",
            "Trap: significant F for variances ≠ significant difference in means.",
        ],
    ),
    "4.2.7": pack(
        [
            T("ANOVA (fixed effects)", "Test equality of k treatment means; factors levels fixed/of interest."),
            T("F = MST / MSE", "Between-treatment mean square over error mean square."),
            T("H0 in one-way ANOVA", "μ1 = μ2 = … = μk."),
            T("Fixed effect model", "Inferences about the specific treatments studied."),
        ],
        [
            "Rejecting H0 means at least one mean differs — not which one (need post hoc).",
            "Assumptions: independence, normality, equal variances (classic).",
            "Contrasts with random effects (4.2.9) where levels are a sample from a population of levels.",
        ],
        [
            "Stem ‘compare means of 3+ fixed treatments’ → fixed-effect ANOVA.",
            "Write ANOVA table sketch: Source | SS | df | MS | F.",
            "Trap: interpreting a significant F as every pair differs.",
        ],
    ),
    "4.2.8": pack(
        [
            T("Total sum of squares (SST / SSTotal)", "Total variability of observations about grand mean."),
            T("Treatment SS (SSTr)", "Variability explained by treatment means."),
            T("Error SS (SSE)", "Within-treatment residual variability."),
            T("Identity", "SST = SSTr + SSE (one-way)."),
        ],
        [
            "Mean squares = SS/df; F uses MSTr/MSE.",
            "Large SSTr relative to SSE → evidence of treatment effects.",
            "Partition idea generalises to factorial ANOVA (more SS terms).",
        ],
        [
            "Memorise SST = treatment + error for one-factor.",
            "Stem ‘within-group sum of squares’ → error SS.",
            "Trap: mixing up SST total with treatment SS naming across textbooks.",
        ],
    ),
    "4.2.9": pack(
        [
            T("ANOVA random effects", "Treatment levels are a random sample from a wider population of levels."),
            T("Inference target", "Variance component σ²_τ rather than specific fixed means only."),
            T("Model", "Response = overall mean + random treatment effect + error."),
        ],
        [
            "Use when interest is variability among a universe of treatments (batches, operators, labs).",
            "Expected mean squares differ from fixed model — F tests may change form.",
            "Mixed models combine fixed and random factors.",
        ],
        [
            "Stem ‘levels randomly sampled from many possible’ → random effects.",
            "Contrast explicitly with fixed-effect interpretation (4.2.7).",
            "Trap: calling every ANOVA ‘random effects’ — wrong.",
        ],
    ),
    "4.2.10": pack(
        [
            T("Single-factor experiment", "One experimental factor at several levels — one-way ANOVA setup."),
            T("Completely randomised design (CRD)", "Units randomly assigned to factor levels."),
            T("Response model", "y_ij = μ + τ_i + ε_ij."),
        ],
        [
            "Simplest designed experiment analysed by one-way ANOVA.",
            "Add blocking → RCBD; add factors → factorial (3.1.5).",
            "Replication per level estimates MSE.",
        ],
        [
            "Stem ‘only one factor varied’ → single-factor experiment.",
            "State randomisation and replication in design description.",
            "Trap: multiple factors analysed as if single-factor — misses interactions.",
        ],
    ),
    "4.2.11": pack(
        [
            T("Model adequacy checking", "Diagnostics that fitted model assumptions hold."),
            T("Residual plots", "vs fitted values — look for funnel shapes (variance), curvature."),
            T("Normality of residuals", "QQ plot / tests — ANOVA/t validity support."),
            T("Outliers / influence", "Unusual points that distort estimates and F tests."),
        ],
        [
            "Significant ANOVA with bad residuals → unreliable inference.",
            "Transforms or nonparametric alternatives if assumptions fail badly.",
            "Adequacy closes the loop with model building (1.4.2–1.4.3).",
        ],
        [
            "Stem ‘check residuals after ANOVA’ → adequacy checking.",
            "List at least two diagnostics in exam answers.",
            "Trap: only looking at p-value and ignoring residual patterns.",
        ],
    ),

    # =========================================================================
    # Module 5 — Reporting, presentation, publication, proposals
    # =========================================================================
    "5.1.1": pack(  # LMR
        [
            T("Research report", "Written document communicating purpose, methods, findings, and conclusions."),
            T("Purpose of reporting", "Inform decisions, enable scrutiny/replication, archive knowledge."),
            T("Audience", "Academics, managers, policymakers — tone and detail adapt."),
            T("Objectivity in reporting", "Separate findings from speculation; disclose limits."),
        ],
        [
            "Report is the final process step (1.2.1) — quality of science includes communication.",
            "Meaning ≠ template alone; it is accountable public knowledge claim.",
            "Ethical reporting includes negative results and limitations.",
        ],
        [
            "LMR: define report + purposes (inform, scrutinise, archive).",
            "Stem ‘formal presentation of research findings in writing’ → research report.",
            "Trap: report ≠ raw SPSS output dump — needs interpretation structure.",
            "Match length/detail to audience (thesis vs executive brief).",
            "Links to structure (5.1.2) and components (5.1.3).",
            "Citation integrity (5.1.8) is part of report meaning, not optional polish.",
        ],
        lmr=True,
    ),
    "5.1.2": pack(  # LMR
        [
            T("Structure of scientific report", "Logical IMRaD-like flow: front matter → intro → methods → results → discussion → refs."),
            T("Front matter", "Title, authors, abstract/summary, sometimes TOC/lists."),
            T("Back matter", "References, appendices, acknowledgements."),
            T("Coherence", "Objectives ↔ methods ↔ results ↔ conclusions must align."),
        ],
        [
            "Structure aids peer review and replication — readers know where to look.",
            "Results state findings; discussion interprets — keep separate.",
            "Different venues tweak order (journal vs thesis vs technical report).",
        ],
        [
            "LMR: recite standard scientific report skeleton in order.",
            "Stem ‘organisation of a scientific write-up’ → structure.",
            "Trap: mixing methods into results or new results into conclusions.",
            "Abstract is structured summary — not a teaser omitting methods/findings.",
            "Number sections consistently for cross-reference.",
            "Pair with components list in 5.1.3 for full marks.",
        ],
        lmr=True,
    ),
    "5.1.3": pack(  # LMR
        [
            T("Title", "Concise, informative statement of the study topic."),
            T("Abstract", "Brief summary of aims, methods, key results, conclusion."),
            T("Introduction", "Context, problem, objectives/hypotheses, rationale."),
            T("Methods", "Design, sample, instruments, procedure, analysis plan."),
            T("Results", "Findings with tables/figures — without extended interpretation."),
            T("Discussion / conclusion", "Interpretation, limits, implications, future work; then references."),
        ],
        [
            "Components flesh out the structure — each has a job.",
            "Methods must be detailed enough for replication (1.2.1 criteria).",
            "Conclusions must be warranted by results (no overclaim).",
        ],
        [
            "LMR: list core components in order with one-line roles.",
            "Stem ‘where do you put sampling procedure’ → methods.",
            "Stem ‘summary for quick screening’ → abstract.",
            "Trap: putting citations only in intro and skipping a reference list.",
            "Tables/figures are components of results communication (5.1.7).",
            "Footnotes (5.1.9) support, not replace, main components.",
        ],
        lmr=True,
    ),
    "5.1.4": pack(
        [
            T("Technical report", "Detailed methods/results for specialists or sponsors."),
            T("Popular / popularised report", "Accessible language for general audiences."),
            T("Interim vs final reports", "Progress updates versus complete findings."),
            T("Thesis / dissertation / journal article", "Academic genres with venue-specific norms."),
        ],
        [
            "Type follows audience and purpose — same study can yield multiple report types.",
            "Executive summaries front business reports; abstracts front journal articles.",
            "Confidential client reports may omit publishable detail.",
        ],
        [
            "Stem ‘report for lay readers’ → popular style.",
            "Name 3–4 types in exam lists.",
            "Trap: jargon-heavy ‘academic’ tone in a managerial brief.",
        ],
    ),
    "5.1.5": pack(
        [
            T("Steps in report writing", "Outline → draft sections → insert tables/figures → cite → revise → proof → finalise."),
            T("Outline first", "Maps objectives to section content before prose."),
            T("Revision", "Clarity, logic, grammar, consistency of terms and numbers."),
            T("Peer feedback", "Catches gaps in methods detail and overclaims."),
        ],
        [
            "Writing is iterative — parallel to model refinement.",
            "Freeze analysis decisions before rewriting results ad hoc to chase significance.",
            "Version control of drafts helps audit changes.",
        ],
        [
            "Give ordered steps in long answers.",
            "Stem ‘prepare outline before full draft’ → report-writing step.",
            "Trap: writing conclusions before results are finalised.",
        ],
    ),
    "5.1.6": pack(
        [
            T("Format", "Margins, headings, numbering, required institutional/journal template."),
            T("Writing style", "Precise, impersonal (often), past tense for methods/results, defined terms."),
            T("Tone", "Objective — avoid promotional adjectives."),
            T("Consistency", "Notation, decimal places, spelling (UK/US), abbreviations."),
        ],
        [
            "Format compliance is often gated before content review.",
            "Style serves clarity and credibility — not ornament.",
            "Templates (5.3.2) enforce format for camera-ready papers.",
        ],
        [
            "Stem ‘follow university thesis layout’ → format.",
            "Prefer active clarity over vague passive stacks when SLM allows.",
            "Trap: switching tenses randomly between methods and results.",
        ],
    ),
    "5.1.7": pack(
        [
            T("Tables", "Exact values in rows/columns — titled, numbered, self-contained."),
            T("Figures / illustrations", "Graphs, diagrams, images — visual patterns."),
            T("Captioning", "Every table/figure numbered with descriptive caption."),
            T("In-text reference", "Refer to Table x / Figure y; don’t orphan graphics."),
        ],
        [
            "Choose table for precision, figure for trends/comparisons.",
            "Don’t duplicate the same numbers in both without purpose.",
            "Axis labels, units, and legends are mandatory exam checklist items.",
        ],
        [
            "Stem ‘present exact cell frequencies’ → table.",
            "Stem ‘show trend over time visually’ → figure.",
            "Trap: 3D chart junk that obscures values.",
        ],
    ),
    "5.1.8": pack(
        [
            T("Citing", "In-text acknowledgement of others’ ideas/data at the point of use."),
            T("Referencing", "Full bibliographic list enabling retrieval (APA/IEEE/Chicago etc.)."),
            T("Plagiarism avoidance", "Quote/paraphrase + cite; never present others’ work as yours."),
            T("Primary vs secondary citation", "Prefer original sources; use ‘as cited in’ sparingly."),
        ],
        [
            "Citation styles differ in order and punctuation — follow the mandated style sheet.",
            "Software (Zotero/EndNote) helps but must be checked.",
            "Self-plagiarism and duplicate publication are also integrity issues.",
        ],
        [
            "Stem ‘list of sources at end’ → references.",
            "Every in-text cite needs a reference entry and vice versa (usually).",
            "Trap: URL-only ‘references’ without author/year/title when style requires them.",
        ],
    ),
    "5.1.9": pack(
        [
            T("Footnotes", "Supplementary notes at page bottom — clarification, extra sources, asides."),
            T("Endnotes", "Notes collected at chapter/document end — same role, different placement."),
            T("Not a substitute for references", "Bibliographic credits still need a reference list/style."),
        ],
        [
            "Use footnotes sparingly — important arguments belong in main text.",
            "Some styles discourage footnotes for citations (author–date) but allow content notes.",
            "Numbering must stay consistent after revisions.",
        ],
        [
            "Stem ‘note at bottom of page’ → footnote.",
            "Distinguish footnote (content) from citation system required by venue.",
            "Trap: hiding key methods only in footnotes.",
        ],
    ),
    "5.2.1": pack(
        [
            T("Oral presentation", "Spoken delivery of research to an audience with limited time."),
            T("Talk structure", "Hook/problem → methods snapshot → key results → implications → Q&A."),
            T("Time discipline", "Design for the slot; rehearsed pacing."),
        ],
        [
            "Oral ≠ reading the full paper aloud — curate a narrative.",
            "Anticipate questions on validity, sample, and limitations.",
            "Authentication/credibility cues continue in 5.2.5.",
        ],
        [
            "Stem ‘present findings verbally at a seminar’ → oral presentation.",
            "State 3–4 structural parts of a research talk.",
            "Trap: drowning audience in every table from the thesis.",
        ],
    ),
    "5.2.2": pack(
        [
            T("Making a presentation", "Prepare slides/notes, rehearse, manage stage presence, handle Q&A."),
            T("Audience analysis", "Adjust jargon and depth to listeners."),
            T("Signposting", "Tell them what you’ll say, say it, summarise."),
        ],
        [
            "Delivery skills amplify content clarity — eye contact, voice, posture.",
            "Backup plans for tech failure are professional practice.",
            "One idea per slide pairs with 5.2.3 visual aids.",
        ],
        [
            "Exam: preparation → delivery → discussion steps.",
            "Stem ‘rehearse and adapt to audience’ → making presentation.",
            "Trap: apologetic filler and unread dense paragraphs on slides.",
        ],
    ),
    "5.2.3": pack(
        [
            T("Visual aids", "Slides, charts, posters, demos supporting the spoken message."),
            T("Design principles", "High contrast, large fonts, minimal text, highlighted takeaway."),
            T("Data visuals", "Simple charts > decorative clutter; same integrity as report figures."),
        ],
        [
            "Aids support, not replace, the speaker.",
            "Accessibility: read keys aloud; don’t rely on colour alone.",
            "Handouts optionally leave precise tables for later.",
        ],
        [
            "Stem ‘PowerPoint/charts during talk’ → visual aids.",
            "Rule of thumb: fewer words, larger graphics.",
            "Trap: reading every bullet verbatim.",
        ],
    ),
    "5.2.4": pack(
        [
            T("Effective communication", "Message received as intended — clarity, structure, feedback."),
            T("Barriers", "Jargon, noise, cultural mismatch, information overload."),
            T("Feedback loop", "Questions and paraphrases confirm understanding."),
        ],
        [
            "Research value is lost if stakeholders cannot understand claims and limits.",
            "Matches report style goals (5.1.6) in spoken form.",
            "Ethical communication avoids hype of uncertain findings.",
        ],
        [
            "Stem ‘importance of clear transfer of research meaning’ → effective communication.",
            "List barriers + one mitigation each.",
            "Trap: equating persuasion with exaggeration of p-values.",
        ],
    ),
    "5.2.5": pack(
        [
            T("Authentication strategies", "Signals that the work is genuine, accurate, and attributable."),
            T("Conventions", "Disclose affiliations, funding, conflicts; accurate author credit."),
            T("Evidence trail", "Cite data sources, show methods, provide reproducible materials when required."),
        ],
        [
            "Authentication underpins trust in both talks and papers.",
            "Related to academic integrity and anti-plagiarism (5.1.8).",
            "Digital contexts may add DOIs, ORCID, timestamps.",
        ],
        [
            "Stem ‘conventions to show work is authentic’ → authentication strategies.",
            "Mention funding/conflict disclosure as exam-ready examples.",
            "Trap: fancy slides without source attribution for borrowed figures.",
        ],
    ),
    "5.3.1": pack(
        [
            T("Journal research paper", "Scholarly article reporting original research to peer review standards."),
            T("Author guidelines", "Scope, length, structure, reference style, ethics statements."),
            T("Peer review", "Independent evaluation before publication."),
            T("Cover letter / submission", "Match paper to journal aims; declare originality."),
        ],
        [
            "Preparing for journals is stricter than coursework reports.",
            "Select journal by scope, audience, and metrics (5.3.3–5.3.4) — not prestige alone.",
            "Predatory journals: check indexing and review practices.",
        ],
        [
            "Stem ‘format study for periodical publication’ → journal paper prep.",
            "Follow IMRaD unless journal specifies otherwise.",
            "Trap: submitting one manuscript simultaneously to multiple journals (unethical).",
        ],
    ),
    "5.3.2": pack(
        [
            T("Paper template", "Publisher/society layout file (Word/LaTeX) controlling format."),
            T("Camera-ready copy", "Final formatted manuscript meeting template constraints."),
            T("Styles & metadata", "Title styles, keywords, author blocks, headers."),
        ],
        [
            "Templates enforce 5.1.6 format at publication scale.",
            "Ignoring template causes desk rejection even if science is sound.",
            "Figures must meet resolution/column-width rules in the template.",
        ],
        [
            "Stem ‘design paper using publisher template’ → template-based formatting.",
            "Use styles, not manual spacing hacks.",
            "Trap: altering margins to squeeze extra pages against rules.",
        ],
    ),
    "5.3.3": pack(
        [
            T("Impact factor (IF)", "Journal-level metric: roughly citations in a year to recent items divided by citable items (classic JCR definition)."),
            T("Calculation idea", "IF_year = citations to recent years’ articles / number of citable articles in those years."),
            T("Use & misuse", "Proxy for journal visibility — not a quality score for a single paper."),
        ],
        [
            "IF compares journals within fields cautiously — fields differ in citation practices.",
            "New journals may lack IF; other indices exist.",
            "Researchers should not be judged solely by IF of venue.",
        ],
        [
            "Stem ‘calculate / meaning of journal impact factor’ → citations/citable articles ratio.",
            "Emphasise journal-level, not article-level, nature.",
            "Trap: saying IF = how many times your paper was cited.",
        ],
    ),
    "5.3.4": pack(
        [
            T("Citation index", "Database tracking citing ↔ cited relationships among publications."),
            T("Citation count", "How often a paper/author is cited — article/author level signal."),
            T("h-index (awareness)", "Author metric combining productivity and citation impact."),
        ],
        [
            "Citation indices (Web of Science, Scopus, Google Scholar) enable IF and literature search.",
            "Citations ≠ automatic endorsement (critical cites count too).",
            "Field-normalised metrics address raw-count bias.",
        ],
        [
            "Stem ‘database of who cited whom’ → citation index.",
            "Distinguish citation index (system) from impact factor (journal metric).",
            "Trap: equating zero citations yet with worthless research — time lag exists.",
        ],
    ),
    "5.3.5": pack(
        [
            T("ISBN", "International Standard Book Number — identifies book-length monographs."),
            T("ISSN", "International Standard Serial Number — identifies serials/journals/magazines."),
            T("Purpose", "Unique identification for publishing, libraries, commerce."),
        ],
        [
            "ISBN ≠ ISSN: book vs serial is the exam contrast.",
            "A journal has ISSN; a special issue book might also carry ISBN.",
            "Identifiers support correct referencing and retrieval.",
        ],
        [
            "Stem ‘code for books’ → ISBN; ‘code for journals/serials’ → ISSN.",
            "One-liner contrast scores easy marks.",
            "Trap: claiming ISBN measures quality like IF — it does not.",
        ],
    ),
    "5.4.1": pack(
        [
            T("Research problem", "Issue/gap stated clearly enough to guide investigation."),
            T("Problem identification", "From practice pain points, theory gaps, lit review anomalies."),
            T("Problem definition", "Bound scope, variables, context, and success criteria."),
        ],
        [
            "Fuzzy problems yield fuzzy designs — definition is the proposal’s cornerstone.",
            "Links back to 1.2.3 proposal aspects and 1.2.4 gap from literature.",
            "Good problems are important, researchable, and ethical.",
        ],
        [
            "Stem ‘identify and define the problem’ → first proposal step.",
            "Write problem as a precise statement, not a thesis title only.",
            "Trap: choosing methods before the problem is clear.",
        ],
    ),
    "5.4.2": pack(
        [
            T("Problem aspects", "Technical, economic, ethical, social, feasibility dimensions."),
            T("Considerations", "Data access, skills, time, funding, stakeholder risk."),
            T("Scope & delimitations", "What is in/out of the study by choice."),
            T("Limitations", "Constraints that weaken inference (acknowledge early)."),
        ],
        [
            "Aspects/considerations turn a topic into a doable project.",
            "Ethics (consent, privacy, harm) can veto otherwise interesting problems.",
            "Feasibility filters prevent proposal failure mid-stream.",
        ],
        [
            "List multiple considerations in 6–8 mark answers.",
            "Stem ‘factors while selecting a research problem’ → aspects/considerations.",
            "Trap: ignoring ethics until after data collection design.",
        ],
    ),
    "5.4.3": pack(
        [
            T("Research plan", "Operational roadmap: objectives, design, methods, schedule, budget, deliverables."),
            T("Gantt / timeline", "When each phase occurs — lit review to report."),
            T("Milestones", "Proposal approval, data collected, analysis done, report submitted."),
            T("Resource plan", "People, tools, access, contingency."),
        ],
        [
            "Plan implements methodology as a managed project.",
            "Aligns with process steps (1.2.1) and proposal content (1.2.3).",
            "Update the plan when pilot results force redesign — document changes.",
        ],
        [
            "Stem ‘schedule and resources for the study’ → research plan.",
            "Include risk/contingency briefly for realism marks.",
            "Trap: plan with methods but no timeline or population definition.",
        ],
    ),
}
