"""Write/merge CSIT745 v2 Module 1 knowledge tree, concepts, MCQs, and coverage.

Source of truth: subjects/csit745/v2/source/module_1.txt (PDF pages 8–31).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "subjects" / "csit745" / "v2" / "data"

LEAF_SECTIONS = [
    "1.1.1",
    "1.1.2",
    "1.1.3",
    "1.2.1",
    "1.2.2",
    "1.2.3",
    "1.2.4",
    "1.2.5",
    "1.3.1",
    "1.3.2",
    "1.3.3",
    "1.3.4",
    "1.3.5",
    "1.4.1",
    "1.4.2",
    "1.4.3",
    "1.4.4",
]


def cid(section: str) -> str:
    return section


# ---------------------------------------------------------------------------
# Concepts (keyed by id) — grounded in module_1.txt
# ---------------------------------------------------------------------------
CONCEPTS: dict[str, dict] = {
    "1.1.1": {
        "id": "1.1.1",
        "title": "Definition and Objectives of Research",
        "module": 1,
        "pages": [8, 9],
        "section": "1.1.1",
        "quick": "Research is a systematized effort to gain new knowledge, typically commencing with a question or problem.",
        "keyIdeas": [
            "Slesinger & Stephenson: manipulation of things, concepts or symbols to generalise, extend, correct or verify knowledge.",
            "Redman & Mory: research is a “systematized effort to gain new knowledge” used in a technical, academic sense.",
            "Clifford Woody: defining/redefining problems, formulating hypotheses, collecting and evaluating data, deducting, testing conclusions against hypotheses.",
            "General (secondary) objectives give a broad view of a study’s goal; specific objectives divide that goal into smaller, measurable aims.",
            "Specific objectives help define who, what, why, when, and how of the project.",
        ],
        "detail": [
            "Research is typically said to commence with a question or a problem. It creates new concepts, methodologies, and understandings through new knowledge or innovative application of existing knowledge, often by synthesising and analysing previous studies.",
            "Classic definitions emphasise different facets: Slesinger & Stephenson stress generalising to extend, correct or verify knowledge for theory or practice; Redman & Mory stress systematised effort for new knowledge; Woody describes the full cycle from problem definition through hypothesis testing.",
            "General objectives provide a detailed overview of what the study should accomplish (e.g., assessing an organisation’s contribution to environmental sustainability). Specific objectives break general aims into logically interconnected, primary goals that make planning and execution easier.",
        ],
        "sourceQuote": "Systematized effort to gain new knowledge",
        "related": ["1.1.2", "1.1.3", "1.2.1"],
        "compare": "General objectives give the broad study goal; specific objectives are those goals divided into smaller, interconnected primary aims.",
        "example": "For an organisation’s environmental sustainability study, specific goals might include how practices changed historically and the impact of new practices, technology, and strategies on effectiveness.",
    },
    "1.1.2": {
        "id": "1.1.2",
        "title": "Characteristics of Research",
        "module": 1,
        "pages": [9],
        "section": "1.1.2",
        "quick": "Sound research is methodical, logical, condensed, repeatable, action-oriented, and delivered in useful formats within time and cost limits.",
        "keyIdeas": [
            "Concentrate on the most pressing issues; follow a structured, methodical procedure.",
            "Follow a logical pattern; scientific progress requires manipulating ideas logically.",
            "Findings should be condensed (shared) so others need not repeat the same work, and should be repeatable/verifiable in new settings.",
            "Research ought to be successful (one topic can spark several others) and action-oriented (findings implementable).",
            "Take an integrated multidisciplinary approach; involve stakeholders at all stages.",
            "Use an easy-to-understand design, stay within timeframe and budget, and deliver findings in formats helpful to decision-makers.",
        ],
        "detail": [
            "The module lists characteristic requirements for research quality: focus on pressing issues; methodical and logical procedure; condensed reporting so others need not redo the work; and repeatability of findings across locations, environments, people, or time.",
            "Research should also be successful (sparking further topics), action-oriented toward implementable solutions, multidisciplinary, and participatory—inviting policymakers to community members at all stages.",
            "Practical constraints matter: clear design, specific timeframe, spending as little money as feasible, and presenting results in formats most useful to administrators, managers, or community members.",
        ],
        "sourceQuote": "The investigation should be methodical. It emphasises the importance of following a structured procedure when conducting research.",
        "related": ["1.1.1", "1.2.1"],
        "compare": None,
        "example": None,
    },
    "1.1.3": {
        "id": "1.1.3",
        "title": "Research Methods vs Research Methodology",
        "module": 1,
        "pages": [10],
        "section": "1.1.3",
        "quick": "Research methods are the procedures and tools used in a study; methodology is the systematic science of how research should be conducted.",
        "keyIdeas": [
            "Research methods: procedures, schemes, steps, and algorithms used during a study (observations, experiments, numerical/statistical approaches, etc.).",
            "Methods are planned, scientific, and value-agnostic; they collect samples and data and seek verifiable explanations.",
            "Business and scientific methods demand explanations based on facts, measurements, and observations—not solely reasoning.",
            "Research methodology: a systematic approach to solving a problem; the science of how research should be conducted.",
            "Methodology describes, explains, and predicts phenomena and provides a research work plan; it is the study of methods for gaining knowledge.",
        ],
        "detail": [
            "Although the names sound similar, methods and methodology differ. Methods are the concrete procedures, schemes, steps, and algorithms a researcher uses—observations, theoretical procedures, experiments, numerical schemes, statistical approaches, and so on.",
            "Methods help collect samples and data and arrive at solutions. They favour explanations that can be verified through experiments, based on collected facts rather than reasoning alone.",
            "Methodology is the systematic approach to solving a problem—the science studying how research should be done. It covers how researchers describe, explain, and predict phenomena and aims to provide a work plan for the research.",
        ],
        "sourceQuote": "A systematic approach to solving a problem is known as research methodology. It is a science that studies how research should be conducted.",
        "related": ["1.1.1", "1.2.1", "1.3.1"],
        "compare": "Methods = tools and procedures used in a study; methodology = the overall systematic plan and science of how research should be conducted.",
        "example": None,
    },
    "1.2.1": {
        "id": "1.2.1",
        "title": "Research Criteria and Research Process",
        "module": 1,
        "pages": [10, 11],
        "section": "1.2.1",
        "quick": "Credible research meets clear criteria (purpose, design, analysis, integrity) and follows a staged process from problem definition to report presentation.",
        "keyIdeas": [
            "Criteria: clear goal; enough process description for replication; carefully prepared unbiased design; disclose shortcomings and their effects.",
            "Analytic techniques must be suitable; data adequately analysed; legitimacy and dependability verified; conclusions only where findings support them.",
            "Trust rises when the researcher is experienced, reputable, and a person of integrity.",
            "Marketing research uses the scientific method impartially—systematic, recorded, time-scheduled steps.",
            "Six listed process steps: Problem Definition; Development of an Approach; Research Design Formulation; Field Work/Data Collection; Data Preparation and Analysis; Report Preparation and Presentation.",
        ],
        "detail": [
            "Research criteria require a very clear goal, sufficient process description so another researcher can continue the work, carefully prepared procedural design for unbiased outcomes, and full disclosure of technique shortcomings and how they might affect results.",
            "Data must be analysed with suitable techniques and checked for legitimacy and dependability. Only conclusions bolstered by findings should be drawn. Researcher experience, reputation, and integrity increase warranted trust.",
            "The research process is planned methodically at every step. The module lists six main steps used when designing a project: problem definition, approach development, research design formulation, field work or data collection, data preparation and analysis, and report preparation and presentation. The study should be impartial and free of personal or political prejudice.",
        ],
        "sourceQuote": "Only conclusions that are bolstered by the study findings and for which the facts offer a sufficient basis should be drawn.",
        "related": ["1.1.3", "1.2.2", "1.2.3"],
        "compare": None,
        "example": "During a project you may discover the scope is insufficient, the topic too wide, information resources scarce, or gathered material contradicts the thesis—reasons to revisit earlier process steps.",
    },
    "1.2.2": {
        "id": "1.2.2",
        "title": "Approaches: Deductive, Inductive, Qualitative and Quantitative",
        "module": 1,
        "pages": [11, 12, 13, 14],
        "section": "1.2.2",
        "quick": "Deductive tests theory-based hypotheses; inductive builds theory from observations; abductive explains surprising puzzles; qualitative and quantitative differ in depth vs numbers.",
        "keyIdeas": [
            "Deductive: develop hypothesis from existing theory, then design strategy to test it; benefits include clarifying relationships, quantitative measurement, and limited generalisation.",
            "Deductive stages: deduce hypothesis → operationalise variables → test (e.g. regression/correlation) → examine confirm/reject vs literature → modify theory if needed.",
            "Inductive: start with observations, seek patterns, propose theories; neither theory nor hypothesis need apply at the start; direction can change.",
            "Abductive: addresses weaknesses of both; begins with surprising facts/puzzles and seeks the best explanation among alternatives (pragmatist).",
            "Qualitative: non-statistical, in-depth in natural settings; sample often 6–10; open-ended; methods include interviews, focus groups, ethnography, content analysis, case study.",
            "Quantitative: systematic statistical/computational focus on numbers; larger populations; closed-ended surveys, questionnaires, polls.",
        ],
        "detail": [
            "A deductive approach starts with a hypothesis based on existing theory and prepares a strategy to test it. Benefits include clarifying relationships between variables, measuring concepts quantitatively, and generalising findings to a certain extent. Stages run from deducing and operationalising hypotheses through testing and possibly modifying theory.",
            "Inductive reasoning starts with observations; theories related to findings are proposed by finding patterns. At the outset neither theories nor hypotheses need apply, and the researcher may alter direction after the process begins. It is based on learning from experience.",
            "Abductive reasoning addresses deductive’s problem of selecting which theory to test and inductive’s limit that no amount of data necessarily builds theory. It begins with surprising facts or puzzles and seeks the best explanation, combining numerical and cognitive reasoning when useful.",
            "Qualitative research is a non-statistical inquiry for in-depth understanding in natural settings, usually with small samples and open-ended probing. Quantitative research gathers and analyses numerical data with closed-ended instruments across larger populations. An advocacy/participatory (emancipatory) approach engages vulnerable groups for reform rather than remaining impartial.",
        ],
        "sourceQuote": "Abductive approaches begin with “surprising facts’’ or “puzzles,” and the goal of the research process is to figure out how to explain them.",
        "related": ["1.2.1", "1.3.5", "1.4.1"],
        "compare": "Deductive tests theory → data; inductive builds theory from data; abductive explains surprising facts by choosing the best among alternative explanations.",
        "example": "Qualitative methods listed: one-to-one interview, focus groups, ethnographic research, content/text analysis, case study research.",
    },
    "1.2.3": {
        "id": "1.2.3",
        "title": "Research Proposal and Aspects",
        "module": 1,
        "pages": [14, 15, 16, 17],
        "section": "1.2.3",
        "quick": "A research proposal persuades others the project matters and is feasible, covering what, why, and how—including title, lit review, methodology, plan, budget, and team.",
        "keyIdeas": [
            "Answers what we want to do, why, and how; needed for competitive funding and to formulate, plan, perform, and monitor the project.",
            "Core parts: Title, Introduction, Literature review, Methodology, Plan (Gantt), Budget, Research team (signed CVs).",
            "Introduction covers challenge/goal, broad and particular aims, justification, concerns, IVs/DVs, hypothesis, and boundaries.",
            "Study goals should be explicit, succinct, quantifiable, and doable; methodology is the work plan for solving the question.",
            "Common errors: overly lofty goals; goals mismatched to title/problem; missing lit review; thin approach detail; over-ambitious schedule; unjustified budget.",
        ],
        "detail": [
            "A research proposal must encompass essential elements of the research procedure with enough detail for readers to evaluate the investigation. Good preparation supports competitive grant applications and helps the researcher formulate, plan, perform, and monitor the work.",
            "Standard components include a clear descriptive title; an introduction that frames the challenge, aims, justification, variables, hypothesis, and boundaries; a literature review acknowledging prior work and showing the gap; methodology as the work plan (design, site, sampling, tools, data collection/analysis, ethics); a timed plan preferably via Gantt chart; a justified budget; and a research team with roles and signed CVs.",
            "Common proposal errors include goals that are too general or lofty, goals that do not match the title or problem, missing references/literature review, insufficient methodological detail, over-ambitious time schedules, and excessive or insufficient budgets without rationale.",
        ],
        "sourceQuote": "A research proposal is designed to persuade others that we have an important research project and that we are capable of finishing it given our work schedule and level of expertise.",
        "related": ["1.2.1", "1.2.4", "1.1.1"],
        "compare": None,
        "example": "Plan time for acquiring supplies, carrying out the study, analysing data, and composing the project report; use a Gantt chart for the activity schedule.",
    },
    "1.2.4": {
        "id": "1.2.4",
        "title": "Literature Survey and Review",
        "module": 1,
        "pages": [17, 18, 19],
        "section": "1.2.4",
        "quick": "A literature review organises knowledge in a research area into a pool so the new study adds to and enriches the field rather than duplicating it.",
        "keyIdeas": [
            "“Review” = organise knowledge of the area into a pool; “literature” = theoretical, research-oriented, and practical studies in that discipline.",
            "Human understanding stages: preservation, transmission, and advancement; research expands the knowledge reservoir.",
            "Importance: supplies theories/ideas for new problems; shows if evidence already solves the problem (avoids replication); sources hypotheses; suggests data/methods/stats; supplies comparative findings for interpretation.",
            "Sources: book indices, periodicals (journals, newspapers, abstracts), encyclopaedias, dissertations, theses, online libraries.",
            "Practices: start with a generic textbook overview; then empirical sources; gather citations meticulously; document bibliographic details on cards.",
        ],
        "detail": [
            "Reviewing literature builds or expands a knowledge pool in a specific area. Researchers must check prior work so similar questions are not needlessly repeated and so they understand theory and research pertaining to the topic.",
            "A successful review helps formulate problems, avoid replication when adequate evidence already exists, generate hypotheses, choose methodologies and statistical techniques, and locate comparative data for interpreting results.",
            "Recommended practice starts with a generic textbook for meaning, nature, importance, and variables; then reviews empirical research via handbooks, encyclopaedias, and abstracts; gathers citations from educational indexes with meticulous accuracy; and documents bibliographic details methodically.",
        ],
        "sourceQuote": "The term “review” means “to organise the knowledge of the specific research area to create a knowledge pool so that our study adds on to and enriches the field of research.”",
        "related": ["1.2.3", "1.1.1"],
        "compare": None,
        "example": "Sources include Cumulative Book Index, journals, newspapers, Encyclopaedia Britannica, dissertations, theses, and online libraries.",
    },
    "1.2.5": {
        "id": "1.2.5",
        "title": "Errors in Research",
        "module": 1,
        "pages": [19, 20, 21],
        "section": "1.2.5",
        "quick": "Research error types include population specification, sampling/frame, selection, non-response, measurement, plus surrogate information and experimental error.",
        "keyIdeas": [
            "Population specification: misunderstanding whom to survey (e.g., buyer vs consumer).",
            "Sampling/sample frame: wrong subpopulation or non-representative sample (e.g., 1936 Roosevelt–Landon poll from car/phone directories).",
            "Selection: non-probability self-selection or interviewer bias toward accessible agreeable respondents.",
            "Non-response: non-contact (cannot reach) vs refusal (won’t answer items); absence of data rather than inaccurate data.",
            "Measurement: difference between data produced and data the analyst needs.",
            "Also: surrogate information error (substitutes/mismatch to the issue) and experimental error (true impact vs attributed impact of IV).",
        ],
        "detail": [
            "Population specification errors occur when researchers do not understand whom they should survey. Sampling and sample-frame errors arise when the wrong subpopulation is used or the responding sample is not representative—illustrated by the 1936 election poll based on car registrations and telephone directories that skewed Republican.",
            "Selection error appears with non-probability self-participation or biased grouping (e.g., intercept interviewers choosing friends). Non-response covers non-contact and refusal; the main issue is missing data. Measurement issues create a gap between produced data and required data.",
            "Surrogate information error arises when needed information is obtained from substitutes or does not match what addresses the issue. Experimental error is non-correspondence between the true impact of and the impact attributed to the independent variable.",
        ],
        "sourceQuote": "When the wrong subpopulation is used to select a sample then survey sampling and sample frame errors occur",
        "related": ["1.2.1", "1.3.4"],
        "compare": "Non-contact = respondent unreachable; refusal = respondent declines items—both are non-response errors (missing data).",
        "example": "A random sample of 5,000 Indian adults that is 70% female over-weights female entertainment tastes and harms generalisation to the adult population.",
    },
    "1.3.1": {
        "id": "1.3.1",
        "title": "Pure and Applied Research",
        "module": 1,
        "pages": [21, 22],
        "section": "1.3.1",
        "quick": "Applied research solves specific practical problems; pure/basic research advances fundamental knowledge rather than fixing a particular problem.",
        "keyIdeas": [
            "Applied (contractual) research: solve a specific problem for a person, group, or society using scientific methods on everyday problems.",
            "Applied work identifies a problem, develops hypotheses, tests via experiment; often empirical; may be seen as non-systematic follow-up validating pure research findings.",
            "Business examples: improve hiring, workplace efficiency/policies, address skill gaps.",
            "Pure/fundamental/basic research clarifies fundamental aspects of a topic, phenomenon, or natural law to advance knowledge.",
            "Basic research may be exploratory, descriptive, or explanatory (often explanatory); data improve understanding that can later support solutions.",
        ],
        "detail": [
            "Research design is the blueprint for collecting, measuring, and analysing data. Within design types, applied research aims to solve specific problems affecting individuals, groups, or society—sometimes called contractual research because of its practical scientific application.",
            "Applied researchers focus on identifying a problem, hypothesising, and experimenting; empirical methods often solve practical problems. It can dig deeper into pure research findings to validate them and develop innovative solutions.",
            "Pure, fundamental, or basic research seeks to clarify fundamental aspects of topics, phenomena, or natural laws. Its goal is to advance knowledge rather than solve a specific problem. Understanding gained can later support proposed solutions.",
        ],
        "sourceQuote": "The goal of this type of research is to advance knowledge rather than to solve a specific problem.",
        "related": ["1.3.2", "1.3.5", "1.1.3"],
        "compare": "Applied → practical solutions to specific problems; pure/basic → fundamental understanding without a particular problem to fix.",
        "example": "Education basic research: How do humans retain memory? How do teaching methods affect students’ concentration?",
    },
    "1.3.2": {
        "id": "1.3.2",
        "title": "Causal and Correlational Designs",
        "module": 1,
        "pages": [22, 23],
        "section": "1.3.2",
        "quick": "Causal (explanatory) research studies cause-and-effect, often via experiments; correlational designs relate variables without manipulating them.",
        "keyIdeas": [
            "Causal/explanatory research determines scope and nature of cause-and-effect relationships and effects of changes on norms/processes.",
            "Causal studies explain patterns of relationships between variables; experiments are the most common primary data method.",
            "Correlational design finds how two variables relate without manipulating either—e.g., a favourable relationship when one changes and the other follows.",
            "Main correlational approaches: naturalistic observation, survey research, and archival research.",
            "Conceptual research (related note): abstract ideas/theories, often used by philosophers to develop or rework concepts.",
        ],
        "detail": [
            "Explanatory research, also called causal research, assesses cause-and-effect relationships and the effects of specific changes. Causal designs examine situations to explain relationship patterns among variables, typically collecting primary data through experiments.",
            "Without manipulating either variable, correlational designs determine how two variables relate—such as whether a favourable relationship exists when change in one is followed by change in the other.",
            "Naturalistic observation, survey research, and archival research are the three main approaches to correlational studies, each with different advantages and disadvantages.",
        ],
        "sourceQuote": "Without manipulating either variable, researchers use a correlational study design to find out how two variables relate to one another.",
        "related": ["1.3.1", "1.3.4", "1.3.3"],
        "compare": "Causal designs seek cause-and-effect (often experiments); correlational designs only describe associations without manipulation.",
        "example": "Causal examples: FDI effects on Taiwanese growth; rebranding impact on loyalty; work-process re-engineering impact on employee motivation.",
    },
    "1.3.3": {
        "id": "1.3.3",
        "title": "Cross-sectional and Longitudinal Studies",
        "module": 1,
        "pages": [23, 24],
        "section": "1.3.3",
        "quick": "Both are observational; cross-sectional compares groups at one point in time, while longitudinal observes the same subjects repeatedly over a long period.",
        "keyIdeas": [
            "Observational: researchers record data without tampering with the research environment.",
            "Cross-sectional: compare different population groups at a single point—like a photograph; can compare multiple variables at once.",
            "Cross-sectional limitation: may not provide conclusive cause-and-effect because it is only a snapshot.",
            "Longitudinal: multiple observations of the same subjects over a long period (sometimes years); can detect group and individual change and create event sequences.",
            "Longitudinal designs are more likely than cross-sectional to suggest cause-and-effect but take longer to complete.",
        ],
        "detail": [
            "Longitudinal and cross-sectional studies are both observational: researchers measure without intervening (e.g., cholesterol in daily walkers vs non-walkers without persuading behaviour change).",
            "A cross-sectional study compares different population groups at one point in time—like a photograph. It can examine several variables together (age, gender, income, education with walking and cholesterol) but cannot settle whether walking lowered cholesterol or walkers already had low levels.",
            "A longitudinal study makes multiple observations of the same subjects over time, detecting changes at group and individual levels and creating event sequences. Because of its scope it is more likely to suggest cause-and-effect, though it takes longer than a cross-sectional study.",
        ],
        "sourceQuote": "A cross-sectional study is distinguished by the ability to compare different population groups at a single point in time. Consider it like taking a photograph.",
        "related": ["1.3.2", "1.3.4"],
        "compare": "Cross-sectional = one-time snapshot across groups; longitudinal = repeated measures of the same subjects over time.",
        "example": "Cholesterol in walkers vs non-walkers by age/gender at one time (cross-sectional) versus cholesterol change in women over 40 who walked daily for 20 years (longitudinal).",
    },
    "1.3.4": {
        "id": "1.3.4",
        "title": "Experimental, Semi-experimental and Non-Experimental",
        "module": 1,
        "pages": [24, 25],
        "section": "1.3.4",
        "quick": "Experimental research manipulates control variables to measure impact; quasi-experimental manipulates without random assignment; non-experimental measures variables as they occur naturally.",
        "keyIdeas": [
            "Experimental: scientific manipulation of one or more control variables, then measure impact; used to trace cause-and-effect.",
            "Quasi-/semi-experimental (Cook & Campbell): resembles experimental research; IV manipulated but participants not randomly assigned—directionality reduced but confounding remains.",
            "Quasi-experiments common in field settings where random assignment is difficult (e.g., psychotherapy or educational interventions).",
            "Non-experimental: no control/IV manipulated; variables measured as they occur naturally.",
            "Non-experimental used when no causal question, IV cannot be changed, assignment not random, study is exploratory, relationship is non-causal, or information is limited.",
        ],
        "detail": [
            "Experimental research employs a scientific approach to manipulate one or more control variables and measure the impact. It is widely used when the goal is to trace cause-and-effect between defined variables.",
            "Quasi-experimental research (prefix quasi = “similar to”) manipulates the independent variable before measuring the dependent variable but does not randomly assign participants. That eliminates the directionality problem yet leaves possible confounding differences between conditions.",
            "Non-experimental research does not manipulate any control or independent variable; researchers measure variables as they occur naturally. It fits broad exploratory work, non-causal relationships, or situations where random assignment or IV change is impossible.",
        ],
        "sourceQuote": "Non-experimental research is defined as research in which no control or independent variable is manipulated.",
        "related": ["1.3.2", "1.2.5", "1.3.3"],
        "compare": "Experimental = manipulate + preferably randomise; quasi = manipulate without random assignment; non-experimental = no manipulation.",
        "example": "Non-equivalent groups: split a class—half gets a new after-school programme expected to raise grades, half does not.",
    },
    "1.3.5": {
        "id": "1.3.5",
        "title": "Descriptive and Exploratory Research",
        "module": 1,
        "pages": [25, 26],
        "section": "1.3.5",
        "quick": "Descriptive research details the ‘what’ of a population or phenomenon without asking why; exploratory research learns about little-studied topics to sharpen the problem.",
        "keyIdeas": [
            "Descriptive: detailed account of researched population/phenomena; emphasises “what” over “why”; describes characteristics without explaining causes.",
            "Descriptive examples: surveys on shopping frequency, food habits, product preference; reporting impulse-buying trends without explaining why they exist.",
            "Exploratory: learn more about a topic not covered extensively; seldom definitive; enhances comprehension and helps develop a more targeted issue statement.",
            "Also called interpretative research or grounded theory approach; answers what, how, and why as insight emerges.",
            "Product example: beta testing of a truly new feature (e.g., Snapchat filters at launch) is exploratory; copying an existing feature (Telegram status like WhatsApp) is not.",
        ],
        "detail": [
            "Descriptive research provides a detailed account of a population or phenomenon and places greater emphasis on “what” than “why.” It describes demographic characteristics or patterns without explaining why events occur.",
            "Exploratory research studies topics that have not been covered extensively. It rarely yields a definitive outcome but improves understanding of the current issue and helps form a more targeted problem statement. The process varies as new data or insight appears.",
            "In product research after development (beta testing), exploration applies when the feature is new. If the feature already exists elsewhere, sufficient information may already be available and the research is not exploratory.",
        ],
        "sourceQuote": "Without asking “why” an event happens, descriptive research mainly aims to describe the characteristics of a demographic group.",
        "related": ["1.3.1", "1.2.2"],
        "compare": "Descriptive reports what exists; exploratory probes little-known topics to deepen understanding and refine the problem—often without a definitive answer.",
        "example": "Market researchers map impulse buying trends across Indian households (“what” only)—ideal descriptive research.",
    },
    "1.4.1": {
        "id": "1.4.1",
        "title": "Types of Research Models",
        "module": 1,
        "pages": [26, 27],
        "section": "1.4.1",
        "quick": "Research models are broadly qualitative (non-numerical, rich meaning) or quantitative (numerical patterns, predictions, and generalisation).",
        "keyIdeas": [
            "Uses of models: identify basic concepts; define meanings with precision; approach and simulate reality.",
            "Importance: models guide theory development and research design; used heavily by social scientists as a structure for examining issues.",
            "Qualitative model: non-numerical data to understand concepts, opinions, experiences; in-depth insights or new ideas; common in anthropology, sociology, education, health, history.",
            "Qualitative approaches are flexible and focus on retaining rich meaning when interpreting data.",
            "Quantitative model: collect/analyse numerical data for patterns, averages, predictions, causal tests, and generalisation to wider populations; used across natural and social sciences.",
        ],
        "detail": [
            "Research models help identify basic concepts, define meanings precisely, and simulate reality. Model building is integral to research design because models guide theory development and design choices.",
            "Qualitative research models involve non-numerical collection and analysis to understand concepts, opinions, and experiences, gathering in-depth insights or developing new ideas. They are heavily used in social sciences and humanities and emphasise rich meaning.",
            "Quantitative research models collect and analyse numerical data to locate patterns and averages, make predictions, test causal relationships, and generate results for wider populations, with wide use in biology, chemistry, psychology, economics, sociology, marketing, and related fields.",
        ],
        "sourceQuote": "Research Models are classified broadly into two types as mentioned below:",
        "related": ["1.2.2", "1.4.2", "1.4.4"],
        "compare": "Qualitative models → non-numerical rich meaning; quantitative models → numerical patterns, prediction, and broader generalisation.",
        "example": None,
    },
    "1.4.2": {
        "id": "1.4.2",
        "title": "Model Building and Stages",
        "module": 1,
        "pages": [27, 28],
        "section": "1.4.2",
        "quick": "Model building creates abstract representations of real systems through staged definition, conceptualization, data, specification, estimation, validation, implementation, and reporting.",
        "keyIdeas": [
            "Define the problem: objectives, scope, constraints; gather context data.",
            "Conceptualization: theoretical framework from literature; hypotheses and key variables; preliminary diagrammatic model of relationships.",
            "Data collection from primary/secondary sources; ensure accuracy via cleaning/preprocessing.",
            "Model specification translates the conceptual model into mathematical/statistical form with stated assumptions.",
            "Estimation/calibration (e.g., regression, ML); validation (cross-validation, sensitivity, robustness); implementation and optimisation; interpret, document, and report.",
        ],
        "detail": [
            "Model building creates abstract representations of real-world systems or phenomena to understand, analyse, and predict behaviour. It begins by clearly defining the problem—objectives, scope, and constraints—and gathering relevant context.",
            "Conceptualization draws on literature to form a theoretical framework, hypotheses, and key variables, then outlines relationships in a preliminary model. Data are collected from primary and secondary sources and cleaned for quality.",
            "Specification turns the conceptual model into equations or algorithms with explicit assumptions. Parameters are estimated and calibrated, then validated against real-world data. After implementation and possible optimisation, results are interpreted, the process documented for reproducibility, and findings reported clearly.",
        ],
        "sourceQuote": "It involves creating abstract representations of real-world systems or phenomena to understand, analyze, and predict their behavior.",
        "related": ["1.4.1", "1.4.3", "1.4.4"],
        "compare": None,
        "example": None,
    },
    "1.4.3": {
        "id": "1.4.3",
        "title": "Data Consideration and Testing",
        "module": 1,
        "pages": [28],
        "section": "1.4.3",
        "quick": "Data consideration requires understanding huge data volumes and judging nature/scope/object of enquiry, time, and required precision before testing.",
        "keyIdeas": [
            "Massive digital data growth (enterprises ~40–60% per year) makes storage alone useless unless used for research purposes.",
            "Organisations explore data lakes and big-data analysis tools to manage and leverage data.",
            "Proper understanding of data is key when volume makes storage and management hard.",
            "Nature, scope and object of enquiry: most important factor when choosing how to consider data—check sources and utilisation.",
            "Time factor: collect timely and leave enough time for consideration and testing against deadlines.",
            "Precision required: considered data must match the wavelength of the research programme.",
        ],
        "detail": [
            "In a digitalised world, data volume grows rapidly—large enterprises may see production increase by 40 to 60% per year. Simply storing data is not beneficial unless it serves specific research purposes, which drives interest in data lakes and big-data tools.",
            "Data consideration starts with proper understanding: when data arrive in huge formats they are hard to understand, store, and manage. Looking closely at the research questions makes answers easier to find.",
            "Key factors are the nature, scope and object of enquiry (most important for choosing how to consider available data and its sources); the time factor (timely collection plus enough time to consider and test); and the precision required so considered data align with the research programme.",
        ],
        "sourceQuote": "Nature, scope and object of enquiry: This constitutes the most important factor affecting the choice of a particular consideration of data.",
        "related": ["1.4.2", "1.2.5"],
        "compare": None,
        "example": None,
    },
    "1.4.4": {
        "id": "1.4.4",
        "title": "Heuristic and Simulation Modelling",
        "module": 1,
        "pages": [28, 29],
        "section": "1.4.4",
        "quick": "Heuristic modelling (Moustakas) is a qualitative discovery process in six phases; simulation models replicate real-system logic with entities, activities, and statistical timing.",
        "keyIdeas": [
            "Heuristic model (Clark Moustakas): from Greek Heuriskein (discover, find); six phases—initial engagement, immersion, incubation, illumination, explication, creative synthesis.",
            "Chaiken’s heuristic-systematic model (HSM): persuasive messages processed heuristically (quick rules) or systematically (careful deliberation); people often prefer heuristics; similar to ELM.",
            "Simulation models use statistical descriptions to replicate workings and logic of a real system (e.g., line averaging 1000 units/hour but also breakdowns/maintenance).",
            "Simulation includes entities (machines, materials, people) and activities (processing, transporting) plus logic governing each activity.",
            "Activity duration often sampled from a statistical distribution once prerequisites are met.",
        ],
        "detail": [
            "Among qualitative models, the heuristic research model developed by Clark Moustakas takes its name from Greek Heuriskein (discover, find). Its six phases are initial engagement, immersion, incubation, illumination, explication, and creative synthesis.",
            "Separately, Shelly Chaiken’s heuristic-systematic model of information processing explains how people receive persuasive messages—via simplifying heuristics or careful systematic processing—sharing ideas with the elaboration likelihood model (ELM).",
            "Simulation research modelling replicates a real system’s workings and logic using statistical descriptions of activities. Models include entities and activities plus governing logic; completion times are often drawn from statistical distributions, capturing variability such as breakdowns that averages alone miss.",
        ],
        "sourceQuote": "The name Heuristic was derived from the Greek work ‘Heuriskein’ (which means discover, find).",
        "related": ["1.4.1", "1.4.2"],
        "compare": "Heuristic (Moustakas) = qualitative discovery phases; simulation = statistical replication of system entities, activities, and logic.",
        "example": "A production line averaging 1000 units/hour still needs simulation of breakdowns and maintenance whose delays may amplify or be absorbed downstream.",
    },
}

# Strip null optional fields for cleaner JSON
for _c in CONCEPTS.values():
    if _c.get("compare") is None:
        _c.pop("compare", None)
    if _c.get("example") is None:
        _c.pop("example", None)


# ---------------------------------------------------------------------------
# MCQs — 2–3 per leaf, exam-style, grounded in extract
# ---------------------------------------------------------------------------
def q(
    section: str,
    n: int,
    stem: str,
    options: list[str],
    correct: int,
    explanation: str,
    difficulty: str = "medium",
) -> dict:
    assert 0 <= correct <= 3 and len(options) == 4
    assert difficulty in ("easy", "medium")
    return {
        "id": f"m1-{section}-q{n}",
        "conceptId": cid(section),
        "module": 1,
        "stem": stem,
        "options": options,
        "correct": correct,
        "explanation": explanation,
        "difficulty": difficulty,
    }


QUESTIONS: list[dict] = [
    # 1.1.1
    q(
        "1.1.1",
        1,
        "According to Redman & Mory, research is best described as which of the following?",
        [
            "A systematized effort to gain new knowledge",
            "Any informal curiosity about everyday events",
            "Only laboratory experimentation with animals",
            "Writing opinions without collecting data",
        ],
        0,
        "Redman & Mory define research as a “Systematized effort to gain new knowledge,” used in a technical academic sense.",
        "easy",
    ),
    q(
        "1.1.1",
        2,
        "How do specific objectives relate to general objectives in a research study?",
        [
            "Specific objectives are broader than general objectives",
            "General objectives are divided into smaller, logically interconnected specific goals",
            "Specific and general objectives are unrelated",
            "Only specific objectives may mention the study’s goal",
        ],
        1,
        "The material states specific objectives outline the primary aim and are general objectives divided into smaller, logically interconnected goals; general objectives provide the basis for specific goals.",
        "easy",
    ),
    q(
        "1.1.1",
        3,
        "Slesinger & Stephenson (Encyclopaedia of Social Sciences) define research as the manipulation of things, concepts or symbols for what purpose?",
        [
            "Entertaining readers with anecdotes",
            "Generalizing to extend, correct or verify knowledge for theory or practice of an art",
            "Avoiding any link between theory and practice",
            "Replacing all prior knowledge without verification",
        ],
        1,
        "Their definition: manipulation “for the purpose of generalizing to extend, correct or verify knowledge, whether that knowledge aids in the construction of theory or in the practice of an art.”",
        "medium",
    ),
    # 1.1.2
    q(
        "1.1.2",
        1,
        "Which characteristic emphasises that earlier study results should be verifiable in new locations, environments, people, or times?",
        [
            "The study should be condensed",
            "The findings should be repeatable",
            "Formats helpful only to administrators",
            "Spending as much money as possible",
        ],
        1,
        "The module states findings should be repeatable: results from earlier studies have to be verifiable in new locations, environments, with fresh people, or at a different time.",
        "easy",
    ),
    q(
        "1.1.2",
        2,
        "“The investigation should be methodical” means primarily that research should:",
        [
            "Follow a structured procedure when conducting research",
            "Avoid any planned steps",
            "Rely only on intuition without procedure",
            "Exclude multidisciplinary approaches",
        ],
        0,
        "Methodical investigation “emphasises the importance of following a structured procedure when conducting research.”",
        "easy",
    ),
    q(
        "1.1.2",
        3,
        "Action-oriented research, as described in the characteristics list, should aim to:",
        [
            "Keep findings unpublished",
            "Find a solution that allows findings to be implemented",
            "Avoid stakeholder participation",
            "Ignore timeframes and budgets",
        ],
        1,
        "Action-oriented research “should aim to find a solution that will allow its findings to be implemented.”",
        "medium",
    ),
    # 1.1.3
    q(
        "1.1.3",
        1,
        "What are research methods, according to the module?",
        [
            "Only the final published report of a study",
            "The various procedures, schemes, steps, and algorithms used in research",
            "A philosophy unrelated to collecting data",
            "Exclusive reliance on unverified reasoning",
        ],
        1,
        "Research methods are “the various procedures, schemes, steps, and algorithms used in research” during a study.",
        "easy",
    ),
    q(
        "1.1.3",
        2,
        "Research methodology is described as:",
        [
            "A single statistical formula",
            "A systematic approach to solving a problem; the science of how research should be conducted",
            "Only laboratory glassware selection",
            "Identical in meaning to research methods",
        ],
        1,
        "Methodology is “a systematic approach to solving a problem” and “a science that studies how research should be conducted,” providing a research work plan.",
        "easy",
    ),
    q(
        "1.1.3",
        3,
        "Which statement about research methods is supported by the text?",
        [
            "They accept explanations based solely on reasoning without facts",
            "They are primarily planned, scientific, and value-agnostic",
            "They never involve statistical approaches",
            "They cannot be used to collect samples or data",
        ],
        1,
        "Methods are “primarily planned, scientific, and value-agnostic,” and business/scientific methods demand explanations based on facts, measurements, and observations rather than solely reasoning.",
        "medium",
    ),
    # 1.2.1
    q(
        "1.2.1",
        1,
        "Which sequence matches the six research-process steps listed in the module?",
        [
            "Report → Data collection → Problem definition → Analysis → Design → Approach",
            "Problem Definition → Approach → Research Design → Field Work/Data Collection → Data Preparation and Analysis → Report Preparation and Presentation",
            "Budget → Title → Interview → Hypothesis only",
            "Literature review → Publication → Sampling only",
        ],
        1,
        "The listed steps are: Problem Definition; Development of an Approach; Research Design Formulation; Field Work or Data Collection; Data Preparation and Analysis; Report Preparation and Presentation.",
        "easy",
    ),
    q(
        "1.2.1",
        2,
        "A research criterion requires that conclusions should be drawn only when:",
        [
            "They sound persuasive regardless of data",
            "They are bolstered by study findings and facts offer a sufficient basis",
            "The researcher’s personal preference supports them",
            "No analysis of data has been attempted",
        ],
        1,
        "“Only conclusions that are bolstered by the study findings and for which the facts offer a sufficient basis should be drawn.”",
        "medium",
    ),
    q(
        "1.2.1",
        3,
        "Why should marketing research be carried out impartially?",
        [
            "So personal or political prejudices of researcher or management do not distort reliable information",
            "Because philosophy never influences findings",
            "Because time-scheduling is unnecessary",
            "Because process description is optional",
        ],
        0,
        "The study should be impartial and devoid of personal or political prejudices of the researcher or management, even though research philosophy always has some impact.",
        "medium",
    ),
    # 1.2.2
    q(
        "1.2.2",
        1,
        "A deductive approach, as defined in the module, begins by:",
        [
            "Collecting observations with no theory in mind and never testing",
            "Developing a hypothesis based on existing theory, then preparing a strategy to test it",
            "Ignoring all prior theory",
            "Only using open-ended interviews with 6–10 people",
        ],
        1,
        "“Deductive approach starts with developing a hypothesis based on existing theory, and then prepares a research strategy for testing the hypothesis.”",
        "easy",
    ),
    q(
        "1.2.2",
        2,
        "Abductive reasoning is presented as a third alternative mainly because it:",
        [
            "Rejects all logical inference",
            "Addresses weaknesses of deductive (theory selection for hypotheses) and inductive (data alone may not build theory)",
            "Requires abandoning pragmatism",
            "Forbids explaining surprising facts",
        ],
        1,
        "Abductive reasoning addresses deductive’s issue of selecting theory to test via hypotheses and inductive’s limit that no amount of empirical data will necessarily enable theory-building, via a pragmatist perspective.",
        "medium",
    ),
    q(
        "1.2.2",
        3,
        "Which feature distinguishes the module’s description of qualitative research?",
        [
            "Exclusive use of close-ended polls on very large populations",
            "Non-statistical inquiry for in-depth understanding in natural settings, often with small samples (about 6–10) and open-ended questions",
            "Mandatory random assignment of thousands of subjects",
            "Focus only on numerical averages",
        ],
        1,
        "Qualitative research is a non-statistical process for in-depth understanding in natural settings, usually with sample size between 6 and 10, using open-ended questions.",
        "easy",
    ),
    # 1.2.3
    q(
        "1.2.3",
        1,
        "A research proposal is designed primarily to:",
        [
            "Replace the need for any methodology section",
            "Persuade others the project is important and that the team can finish it given schedule and expertise",
            "Avoid stating what, why, and how",
            "Omit budget and team details always",
        ],
        1,
        "“A research proposal is designed to persuade others that we have an important research project and that we are capable of finishing it given our work schedule and level of expertise.”",
        "easy",
    ),
    q(
        "1.2.3",
        2,
        "Which set lists components the module says a research proposal comprises?",
        [
            "Title, Introduction, Literature review, Methodology, Plan, Budget, Research team",
            "Only a title and a joke",
            "Results and conclusions with no methods",
            "Glossary and index only",
        ],
        0,
        "Listed components: Title, Introduction, Literature review, Methodology, Plan (time frame/Gantt), Budget, Details of research team (signed CV).",
        "easy",
    ),
    q(
        "1.2.3",
        3,
        "Which of the following is listed as a common error in proposal writing?",
        [
            "Goals that are overly general or excessively lofty",
            "Including a literature review with citations",
            "Providing justification for costly budget items",
            "Defining roles for researchers",
        ],
        0,
        "Common errors include: goals overly general or lofty; goals mismatched to title/problem; missing lit review; insufficient approach detail; over-ambitious schedule; unjustified excessive/insufficient budget.",
        "medium",
    ),
    # 1.2.4
    q(
        "1.2.4",
        1,
        "In the module’s meaning of review of literature, “review” means:",
        [
            "Deleting all prior studies",
            "Organising knowledge of the specific research area into a knowledge pool so the study adds to and enriches the field",
            "Copying one article without context",
            "Ignoring theoretical studies",
        ],
        1,
        "“Review” means to organise knowledge of the specific research area to create a knowledge pool so the study adds on to and enriches the field.",
        "easy",
    ),
    q(
        "1.2.4",
        2,
        "One importance of reviewing literature is that it can:",
        [
            "Force unnecessary replication of solved problems",
            "Guide researchers on whether adequate evidence already solves the problem, avoiding replication",
            "Replace all need for methodology later",
            "Prohibit formulating hypotheses",
        ],
        1,
        "Review of literature “guides researchers on the availability of adequate evidence that solves the problem sufficiently without the need of further investigation — this initiative avoids the replication of Research.”",
        "medium",
    ),
    q(
        "1.2.4",
        3,
        "The three equally important stages of human understanding named in this section are:",
        [
            "Preservation, transmission, and advancement",
            "Budgeting, hiring, and advertising",
            "Sampling, coding, and printing",
            "Deduction only",
        ],
        0,
        "The text lists preservation, transmission, and advancement as three equally important stages of human understanding.",
        "easy",
    ),
    # 1.2.5
    q(
        "1.2.5",
        1,
        "Population specification error occurs when:",
        [
            "The researcher does not understand whom they should survey",
            "Every respondent answers every item perfectly",
            "Only measurement instruments are too precise",
            "The report is too long",
        ],
        0,
        "“Population specification errors occur when the researcher does not understand whom they should survey.”",
        "easy",
    ),
    q(
        "1.2.5",
        2,
        "The 1936 Roosevelt–Landon poll example in the module illustrates which error?",
        [
            "Experimental error only",
            "Sampling and sample frame error from car registrations and telephone directories skewed toward Republicans",
            "Perfectly representative sampling",
            "Surrogate information from cancer patients eating bread",
        ],
        1,
        "The sample frame from car registrations and telephone directories failed to realize most owners were Republicans, wrongly predicting a Republican victory—sampling/sample frame error.",
        "medium",
    ),
    q(
        "1.2.5",
        3,
        "Non-response errors are categorised in the text as:",
        [
            "Type I and Type II only",
            "Non-contact errors and refusal errors",
            "Qualitative and quantitative errors",
            "Pure and applied errors",
        ],
        1,
        "Non-response errors: (a) non-contact (respondent cannot be reached) and (b) refusal (chooses not to respond to items). Primary issue is absence of data.",
        "easy",
    ),
    # 1.3.1
    q(
        "1.3.1",
        1,
        "The primary goal of pure/basic/fundamental research is to:",
        [
            "Advance knowledge rather than solve a specific problem",
            "Immediately fix a company’s hiring process only",
            "Avoid collecting any data",
            "Replace applied research in every business setting",
        ],
        0,
        "“The goal of this type of research is to advance knowledge rather than to solve a specific problem.”",
        "easy",
    ),
    q(
        "1.3.1",
        2,
        "Applied research is characterised as aiming to:",
        [
            "Solve a specific problem or offer novel solutions affecting a person, group, or society",
            "Study only abstract philosophy with no practical link",
            "Never test hypotheses experimentally",
            "Ignore empirical methods",
        ],
        0,
        "Applied research aims to solve a specific problem or offer novel solutions to issues affecting a person, group, or society; often called contractual research.",
        "easy",
    ),
    q(
        "1.3.1",
        3,
        "Which is given as a business example of applied research?",
        [
            "Applied research to improve the hiring process in a company",
            "Only “How do humans retain memory?” with no application",
            "Writing fiction unrelated to workplace issues",
            "Avoiding workplace skill-gap studies",
        ],
        0,
        "Business examples include improving hiring, workplace efficiency and policies, and addressing workplace skill gaps.",
        "medium",
    ),
    # 1.3.2
    q(
        "1.3.2",
        1,
        "In causal (explanatory) research designs, the most common primary data collection method named is:",
        [
            "Experiments",
            "Only poetry analysis",
            "Random guessing",
            "Avoiding any data collection",
        ],
        0,
        "“In studies using a causal research design, the most common primary data collection method is experiments.”",
        "easy",
    ),
    q(
        "1.3.2",
        2,
        "A correlational study design is used to:",
        [
            "Manipulate both variables aggressively",
            "Find how two variables relate without manipulating either variable",
            "Prove causation in every case",
            "Replace all experimental work",
        ],
        1,
        "“Without manipulating either variable, researchers use a correlational study design to find out how two variables relate to one another.”",
        "easy",
    ),
    q(
        "1.3.2",
        3,
        "Which three main approaches to correlational studies does the module list?",
        [
            "Naturalistic observation, survey research, and archival research",
            "Only double-blind clinical trials",
            "Budgeting, Gantt charts, and CVs",
            "Heuristic, simulation, and ELM only",
        ],
        0,
        "“Naturalistic observation, survey research, and archive research are the three main approaches to correlational studies.”",
        "medium",
    ),
    # 1.3.3
    q(
        "1.3.3",
        1,
        "A cross-sectional study is distinguished by:",
        [
            "Comparing different population groups at a single point in time, like a photograph",
            "Following the same subjects for many years only",
            "Always proving definitive cause-and-effect",
            "Requiring researchers to change subjects’ habits",
        ],
        0,
        "Cross-sectional studies compare different population groups at a single point in time—“like taking a photograph.”",
        "easy",
    ),
    q(
        "1.3.3",
        2,
        "Compared with cross-sectional designs, longitudinal studies:",
        [
            "Never observe the same subjects twice",
            "Make multiple observations of the same subjects over a long period and can create event sequences",
            "Are always shorter to complete",
            "Tamper with the research environment by definition",
        ],
        1,
        "Longitudinal studies involve multiple observations of the same subjects over a long period, can detect changes and create event sequences, and take longer than cross-sectional studies.",
        "medium",
    ),
    q(
        "1.3.3",
        3,
        "Why may cross-sectional studies not provide conclusive cause-and-effect evidence?",
        [
            "They always manipulate every variable",
            "They provide a snapshot of a single moment and do not consider what occurs before or after",
            "They never compare multiple variables",
            "They require decades by definition",
        ],
        1,
        "Such studies provide a snapshot of a single moment and do not consider what occurs before or after, so cause-and-effect cannot be settled conclusively.",
        "medium",
    ),
    # 1.3.4
    q(
        "1.3.4",
        1,
        "Experimental research is well-known for allowing:",
        [
            "Manipulation of control variables and measurement of impact",
            "No measurement of any impact",
            "Only archival reading without design",
            "Forbidding cause-and-effect questions",
        ],
        0,
        "Experimental research manipulates one or more control variables and measures the impact of the manipulation; it is well-known for allowing manipulation of control variables.",
        "easy",
    ),
    q(
        "1.3.4",
        2,
        "Quasi-experimental research (Cook & Campbell) differs from true experiments mainly because:",
        [
            "The independent variable is never manipulated",
            "Participants are not randomly assigned even though the IV is manipulated",
            "No dependent variable is ever measured",
            "It eliminates all confounding variables completely",
        ],
        1,
        "In quasi-experimental research the IV is manipulated but participants are not randomly assigned, so confounding differences between conditions may remain.",
        "medium",
    ),
    q(
        "1.3.4",
        3,
        "Non-experimental research is defined as research in which:",
        [
            "No control or independent variable is manipulated; variables are measured as they occur naturally",
            "Every variable must be randomly assigned",
            "Only laboratory animals are studied",
            "Causal proof is always guaranteed",
        ],
        0,
        "“Non-experimental research is defined as research in which no control or independent variable is manipulated.” Researchers measure variables as they occur naturally.",
        "easy",
    ),
    # 1.3.5
    q(
        "1.3.5",
        1,
        "Descriptive research mainly aims to:",
        [
            "Describe characteristics of a demographic group without asking why an event happens",
            "Always explain underlying causes in depth",
            "Ignore “what” questions entirely",
            "Replace exploratory work in every beta test",
        ],
        0,
        "“Without asking ‘why’ an event happens, descriptive research mainly aims to describe the characteristics of a demographic group.” It emphasises “what” over “why.”",
        "easy",
    ),
    q(
        "1.3.5",
        2,
        "Exploratory research is typically conducted to:",
        [
            "Produce a definitive outcome in every case",
            "Enhance comprehension of a little-studied issue and help develop a more targeted problem statement",
            "Avoid understanding pre-existing phenomena",
            "Forbid questions of what, how, and why",
        ],
        1,
        "Exploratory research learns about topics not covered extensively; it seldom produces a definitive outcome but enhances comprehension and helps develop a more targeted issue statement.",
        "medium",
    ),
    q(
        "1.3.5",
        3,
        "According to the product-research example, when is beta research not exploratory?",
        [
            "When the added feature already exists elsewhere (e.g., Telegram status like WhatsApp)",
            "When Snapchat filters first launched as a new feature",
            "Whenever any survey is used",
            "Only when experiments are banned",
        ],
        0,
        "If Telegram adds a status feature already available on WhatsApp, beta research is not exploratory because sufficient information already exists; a truly new feature (Snapchat filters at launch) is exploratory.",
        "medium",
    ),
    # 1.4.1
    q(
        "1.4.1",
        1,
        "Research models are classified broadly into which two types?",
        [
            "Qualitative Research Model and Quantitative Research Model",
            "Only Gantt and Budget models",
            "Type I and Type II models",
            "Oral and informal report models",
        ],
        0,
        "“Research Models are classified broadly into two types… Qualitative Research Model [and] Quantitative Research Model.”",
        "easy",
    ),
    q(
        "1.4.1",
        2,
        "A quantitative research model is about:",
        [
            "Collecting and analysing numerical data to find patterns, make predictions, and generalise",
            "Only non-numerical opinions with no numbers",
            "Avoiding averages and causal tests",
            "Excluding natural and social sciences",
        ],
        0,
        "Quantitative models collect and analyse numerical data for patterns and averages, predictions, causal relationship tests, and generating results to wider populations.",
        "easy",
    ),
    q(
        "1.4.1",
        3,
        "Which is listed as a use of research models?",
        [
            "Help in identifying basic concepts and defining meanings with great precision",
            "Eliminate the need for any research design",
            "Replace all empirical data forever",
            "Forbid simulating reality",
        ],
        0,
        "Uses include: identifying basic concepts; defining meanings with great precision; approaching and simulating reality.",
        "medium",
    ),
    # 1.4.2
    q(
        "1.4.2",
        1,
        "In model building, conceptualization involves:",
        [
            "Developing a theoretical framework from literature, formulating hypotheses, and identifying key variables",
            "Skipping literature and jumping to publication only",
            "Deleting all assumptions",
            "Avoiding any preliminary model diagram",
        ],
        0,
        "Conceptualization develops a theoretical framework based on existing literature and theories, helps formulate hypotheses and identify key variables, then creates a preliminary (often diagrammatic) model.",
        "medium",
    ),
    q(
        "1.4.2",
        2,
        "Model validation is crucial to ensure the model is:",
        [
            "Correctly implemented and free from logical or computational errors, with predictions compared to real-world data",
            "Never compared to real-world data",
            "Hidden from documentation",
            "Estimated without any parameters",
        ],
        0,
        "Validation ensures correct implementation without logical/computational errors; predictions are compared with real-world data (cross-validation, sensitivity, robustness).",
        "easy",
    ),
    q(
        "1.4.2",
        3,
        "What happens in the model specification stage?",
        [
            "The conceptual model is translated into a mathematical or statistical form with techniques, equations/algorithms, and stated assumptions",
            "Only the final public speech is written",
            "Data collection is forbidden",
            "Problem definition is postponed forever",
        ],
        0,
        "In specification, the conceptual model is translated into mathematical or statistical form; modeling techniques and equations/algorithms are selected and assumptions clearly stated.",
        "medium",
    ),
    # 1.4.3
    q(
        "1.4.3",
        1,
        "According to the module, the most important factor affecting the choice of a particular consideration of data is:",
        [
            "Nature, scope and object of enquiry",
            "Font size of the final report",
            "Colour of survey paper only",
            "Whether a Gantt chart uses blue ink",
        ],
        0,
        "“Nature, scope and object of enquiry: This constitutes the most important factor affecting the choice of a particular consideration of data.”",
        "easy",
    ),
    q(
        "1.4.3",
        2,
        "Why is simply storing massive enterprise data described as insufficient?",
        [
            "Storage alone is not beneficial unless data are used for specific research purposes",
            "Data never grow in volume",
            "Data lakes are illegal",
            "Precision is never required",
        ],
        0,
        "“Simply storing this massive amount of data is not beneficial unless it is used for specific research purposes,” motivating tools like data lakes and big-data analysis.",
        "medium",
    ),
    q(
        "1.4.3",
        3,
        "The “time factor” in data consideration means:",
        [
            "Collection must be timely and enough time left for consideration and testing before deadlines",
            "Time can be ignored if volume is large",
            "Only historical data older than 100 years may be used",
            "Testing must occur before any collection",
        ],
        0,
        "Time matters because of deadlines: data collection needs to be timely and post-collection there must be enough time for consideration and testing.",
        "easy",
    ),
    # 1.4.4
    q(
        "1.4.4",
        1,
        "Clark Moustakas’s heuristic research model name derives from Greek ‘Heuriskein’, meaning:",
        [
            "Discover, find",
            "Budget, schedule",
            "Refuse, reject",
            "Measure only",
        ],
        0,
        "“The name Heuristic was derived from the Greek work ‘Heuriskein’ (which means discover, find).”",
        "easy",
    ),
    q(
        "1.4.4",
        2,
        "Which set lists the six phases of the heuristic research model?",
        [
            "Initial engagement, Immersion, Incubation, Illumination, Explication, Creative synthesis",
            "Title, Budget, Gantt only",
            "Sampling, Coding, ANOVA only",
            "Type I, Type II, df only",
        ],
        0,
        "Six phases: Initial engagement, Immersion, Incubation, Illumination, Explication, Creative synthesis.",
        "medium",
    ),
    q(
        "1.4.4",
        3,
        "Simulation models attempt to replicate a real system by using:",
        [
            "Statistical descriptions of activities, with entities, activities, and governing logic",
            "Only a single fixed average with no variability ever",
            "Poetry without entities or activities",
            "Abandoning all statistical timing",
        ],
        0,
        "Simulation models use statistical descriptions of activities to replicate workings and logic; they include entities (machines, materials, people) and activities (processing, transporting) plus logic; times often sampled from distributions.",
        "medium",
    ),
]


def module1_tree() -> dict:
    def leaf(section: str, title: str) -> dict:
        return {
            "id": cid(section),
            "title": f"{section} {title}",
            "conceptId": cid(section),
        }

    return {
        "id": "m1",
        "title": "Module I: Introduction",
        "module": 1,
        "children": [
            {
                "id": "1.1",
                "title": "1.1 Research",
                "children": [
                    leaf("1.1.1", "Definition and Objectives of Research"),
                    leaf("1.1.2", "Characteristics of Research"),
                    leaf("1.1.3", "Research Methods vs Methodology"),
                ],
            },
            {
                "id": "1.2",
                "title": "1.2 Research Process",
                "children": [
                    leaf("1.2.1", "Research Criteria and Research Process"),
                    leaf(
                        "1.2.2",
                        "Approaches: Deductive, Inductive, Qualitative & Quantitative",
                    ),
                    leaf("1.2.3", "Research Proposal and Aspects"),
                    leaf("1.2.4", "Literature Survey and Review"),
                    leaf("1.2.5", "Errors in Research"),
                ],
            },
            {
                "id": "1.3",
                "title": "1.3 Types of Research Design",
                "children": [
                    leaf("1.3.1", "Pure and Applied"),
                    leaf("1.3.2", "Causal and Correlational"),
                    leaf("1.3.3", "Cross-sectional and Longitudinal"),
                    leaf("1.3.4", "Experimental, Semi-experimental and Non-Experimental"),
                    leaf("1.3.5", "Descriptive and Exploratory"),
                ],
            },
            {
                "id": "1.4",
                "title": "1.4 Research Modelling",
                "children": [
                    leaf("1.4.1", "Types of Models"),
                    leaf("1.4.2", "Model Building and Stages"),
                    leaf("1.4.3", "Data Consideration and Testing"),
                    leaf("1.4.4", "Heuristic and Simulation Modelling"),
                ],
            },
        ],
    }


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_tree(existing: dict) -> dict:
    modules = list(existing.get("modules") or [])
    modules = [m for m in modules if m.get("module") != 1 and m.get("id") != "m1"]
    modules.insert(0, module1_tree())
    # keep stable order by module number when present
    def sort_key(m):
        return (m.get("module") is None, m.get("module") or 99, m.get("id") or "")

    modules.sort(key=sort_key)
    return {"modules": modules}


def merge_concepts(existing: dict) -> dict:
    concepts = dict(existing.get("concepts") or existing)
    # if legacy top-level was flat concepts only
    if "concepts" not in existing and any(str(k).startswith("m") for k in existing):
        concepts = dict(existing)
    # drop prior module-1 concepts (prefixed or syllabus ids)
    for k in list(concepts.keys()):
        v = concepts[k]
        if k.startswith("m1-") or (isinstance(v, dict) and v.get("module") == 1):
            del concepts[k]
    concepts.update(CONCEPTS)
    return {"concepts": concepts}


def merge_questions(existing: dict) -> dict:
    questions = list(existing.get("questions") or existing if isinstance(existing, list) else [])
    if isinstance(existing, list):
        questions = list(existing)
    questions = [q for q in questions if not str(q.get("id", "")).startswith("m1-")]
    questions.extend(QUESTIONS)
    return {"questions": questions}


def build_coverage() -> dict:
    by_concept = {}
    for section in LEAF_SECTIONS:
        concept_id = cid(section)
        qs = [x for x in QUESTIONS if x["conceptId"] == concept_id]
        c = CONCEPTS[concept_id]
        by_concept[concept_id] = {
            "section": section,
            "title": c["title"],
            "pages": c["pages"],
            "mcqCount": len(qs),
            "hasQuick": bool(c.get("quick")),
            "hasKeyIdeas": len(c.get("keyIdeas") or []) >= 3,
            "hasDetail": bool(c.get("detail")),
            "hasSourceQuote": bool(c.get("sourceQuote")),
            "verified": True,
        }
    return {
        "modules": {
            "1": {
                "title": "Module I: Introduction",
                "status": "verified",
                "leafSections": LEAF_SECTIONS,
                "conceptCount": len(LEAF_SECTIONS),
                "questionCount": len(QUESTIONS),
                "concepts": by_concept,
            }
        }
    }


def merge_coverage(existing: dict) -> dict:
    out = dict(existing) if existing else {}
    modules = dict(out.get("modules") or {})
    fresh = build_coverage()
    modules["1"] = {
        "status": "approved",
        "conceptIds": sorted(CONCEPTS.keys()),
        "questionCount": len(QUESTIONS),
    }
    out["modules"] = modules
    out["subject"] = out.get("subject") or "csit745"
    out["practiceMode"] = "whole_subject_shuffle"
    out["notes"] = "Practice draws from the full bank across all modules; never module-locked."
    return out


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    tree_path = DATA / "knowledge_tree.json"
    concepts_path = DATA / "concepts.json"
    mcq_path = DATA / "mcq_bank.json"
    coverage_path = DATA / "coverage.json"

    tree = merge_tree(load_json(tree_path, {"modules": []}))
    concepts = merge_concepts(load_json(concepts_path, {"concepts": {}}))
    mcqs = merge_questions(load_json(mcq_path, {"questions": []}))
    coverage = merge_coverage(load_json(coverage_path, {"modules": {}}))

    # sanity
    missing = [s for s in LEAF_SECTIONS if cid(s) not in CONCEPTS]
    if missing:
        raise SystemExit(f"Missing concepts for sections: {missing}")
    for s in LEAF_SECTIONS:
        n = sum(1 for x in QUESTIONS if x["conceptId"] == cid(s))
        if n < 2 or n > 3:
            raise SystemExit(f"Section {s} has {n} MCQs (need 2–3)")

    write_json(tree_path, tree)
    write_json(concepts_path, concepts)
    write_json(mcq_path, mcqs)
    write_json(coverage_path, coverage)

    print(f"Wrote Module 1 pack -> {DATA}")
    print(f"  concepts: {len(CONCEPTS)}")
    print(f"  questions: {len(QUESTIONS)}")
    print(f"  leaf sections: {', '.join(LEAF_SECTIONS)}")


if __name__ == "__main__":
    main()
