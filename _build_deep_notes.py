# -*- coding: utf-8 -*-
"""Author BS605 deep notes (Module 3 quality) + improved packs for other subjects."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBJECTS = ROOT / "subjects"

# ---------------------------------------------------------------------------
# BS605 — handcrafted. Same shape as Module 3 sample:
#   terms = exam-ready one-liners
#   concepts = how pieces relate / compare-contrast
#   notes = stem cues, traps, "don't confuse X with Y" (specific, never generic)
# LMR topics are denser.
# ---------------------------------------------------------------------------

def t(name: str, definition: str) -> dict:
    return {"t": name, "d": definition}


BS605: dict[str, dict] = {
    # ----- roots -----
    "m1_root": {
        "terms": [
            t("Self tools", "TEA, Johari, PE Scale, esteem/efficacy/respect, assertiveness."),
            t("Thinking tools", "ICEDIP, Six Hats, cognitive flexibility and errors."),
            t("Social cognition", "Schemas, attribution, stereotype vs prejudice."),
        ],
        "concepts": [
            "Walk the map: Self → thinking tools → social cognition.",
            "Faculty often weight Module 2 (EI/attitudes) higher than Module 1 foundations.",
            "Many Module 1 LMR items are definition + contrast pairs.",
        ],
        "notes": [
            "Open each card’s Deep notes for term lists and exam traps.",
            "LMR cards (orange outline) are denser — prioritise those for revision.",
        ],
    },
    "m2_root": {
        "terms": [
            t("Attitude", "Evaluation of a person, idea, or object as favourable or unfavourable."),
            t("Emotional intelligence (Goleman)", "Interpret, understand, and manage own and others’ emotions at work."),
            t("Attitude ABC", "Affective · Behavioural · Cognitive — not Ellis ABC."),
        ],
        "concepts": [
            "Exam-heavy module: attitude structure + Goleman EI usually outweigh Module 1 alone.",
            "Attitude ABC ≠ Ellis ABC (Module 5: Adversity–Beliefs–Consequences).",
            "EI (self + others) ≠ Gardner intrapersonal (self only).",
        ],
        "notes": [
            "If a stem mixes ABC flavours, check which module frame it is asking for.",
            "Locus of control (internal/external) is a live-class extra — useful in case answers.",
        ],
    },
    "m4_root": {
        "terms": [
            t("Conflict", "Incompatible goals, cognitions, or emotions leading to opposition."),
            t("Mediation", "Neutral facilitation — not taking sides or judging."),
            t("Negotiation", "Distributive (claim value) vs integrative (create value)."),
        ],
        "concepts": [
            "Flow: diagnose conflict → choose style → mediate if needed → negotiate.",
            "Disagreement ≠ full conflict; conflict is not always negative.",
            "Four pillars sit on top of negotiation technique.",
        ],
        "notes": [
            "Match resolution style to stakes and time (compete vs collaborate vs avoid).",
            "Mediator ≠ arbitrator who decides for the parties.",
        ],
    },
    "m5_root": {
        "terms": [
            t("Values (Rokeach)", "Terminal = desired ends; instrumental = preferred means/modes of behaviour."),
            t("Resilience", "Positive adaptation in the face of serious adversity — both parts required."),
            t("VUCA", "Volatility, Uncertainty, Complexity, Ambiguity."),
        ],
        "concepts": [
            "Ethics applies standards to conduct; values shape what is desirable.",
            "Ellis ABC (beliefs mediate feelings) ≠ Attitude ABC.",
            "Agility adapts behaviour under VUCA; resilience adapts under adversity.",
        ],
        "notes": [
            "Resilience stems need both adversity and positive adaptation.",
            "Rokeach: responsibility as means to friendship = instrumental serving terminal.",
        ],
    },

    # ----- Module 1 -----
    "1.1": {
        "terms": [
            t("Self", "Sense of personal identity; studied via person–situation interaction."),
            t("ABCs of the self", "Affective, Behavioural, Cognitive domains of the self."),
            t("Self-concept", "Knowledge representation about oneself — traits, roles, values — organised into self-schemas."),
            t("Self-schema", "Mental structure that guides processing of self-relevant information."),
        ],
        "concepts": [
            "Self-concept is cognitive self-knowledge; it is not the same as self-esteem (global worth).",
            "ABCs here describe domains of the self — different from Attitude ABC and Ellis ABC.",
            "Schemas about the self filter what you notice and remember about yourself.",
        ],
        "notes": [
            "Stem “knowledge about oneself / self-schemas” → self-concept.",
            "Stem “global worth / liking yourself” → self-esteem (1.5), not self-concept.",
            "Don’t answer Attitude ABC when the stem is about the self’s ABCs.",
        ],
    },
    "1.2": {  # LMR
        "terms": [
            t("T-E-A model", "Thoughts, Emotions, and Actions constantly influence each other."),
            t("Thoughts", "Internal processing and beliefs."),
            t("Emotions", "Internal states and felt values."),
            t("Actions", "External behaviours and words."),
        ],
        "concepts": [
            "Changing one TEA component tends to shift the others — reciprocal, not one-way.",
            "Useful for coaching/case answers: intervene at thought, feeling, or behaviour level.",
            "Related to but not identical with Attitude ABC (evaluation components) or Ellis ABC (adversity→beliefs→consequences).",
        ],
        "notes": [
            "LMR: “mutual influence / change one shifts others” → TEA.",
            "If stem lists Affective–Behavioural–Cognitive as attitude parts → Module 2, not TEA.",
            "If stem is Adversity–Beliefs–Consequences → Ellis (5.4), not TEA.",
            "One-line exam answer: Thoughts, emotions, and actions continually influence each other.",
        ],
    },
    "1.3": {  # LMR
        "terms": [
            t("Johari Window", "Four panes of known/unknown information to self and others (Luft & Ingham)."),
            t("Open / Arena", "Known to self and known to others."),
            t("Blind spot", "Known to others, unknown to self."),
            t("Hidden / Façade", "Known to self, unknown to others."),
            t("Unknown", "Unknown to self and unknown to others."),
        ],
        "concepts": [
            "Enlarge Open by feedback (shrink Blind) + disclosure (shrink Hidden).",
            "Trust grows when disclosure and learning from feedback work together.",
            "PE Scale (1.4) are skills that operate on Johari panes — they are not the four panes themselves.",
        ],
        "notes": [
            "LMR: “others know / you don’t” → Blind; “you know / others don’t” → Hidden.",
            "Listing panes without Unknown is a common miss.",
            "Don’t confuse Johari panes with PE Scale dimensions (SD, OTF, Perceptiveness).",
            "Stem “enlarge the Arena” → feedback + disclosure.",
        ],
    },
    "1.4": {
        "terms": [
            t("PE Scale", "Personal Effectiveness: Self-disclosure (SD), Openness to feedback (OTF), Perceptiveness."),
            t("Self-disclosure (SD)", "Willingness to share relevant self-information."),
            t("Openness to feedback (OTF)", "Willingness to receive and use others’ observations."),
            t("Perceptiveness", "Ability to notice cues about self, others, and situations."),
        ],
        "concepts": [
            "Effective people use SD + OTF + perceptiveness to shrink secret/blind areas and enlarge the Arena.",
            "PE dimensions act on Johari — they are tools, not the pane names.",
            "Low SD + low OTF keeps people stuck with large Hidden/Blind areas.",
        ],
        "notes": [
            "Stem asks for three PE dimensions → SD, OTF, Perceptiveness.",
            "If options are Open/Blind/Hidden/Unknown → Johari, not PE Scale.",
            "Link answer to Johari when asked how PE improves the Open area.",
        ],
    },
    "1.5": {  # LMR
        "terms": [
            t("Self-esteem", "Overall subjective sense of personal worth / liking of self."),
            t("Self-efficacy (Bandura)", "Belief you can succeed at a specific task or goal — not a global trait."),
            t("Self-respect", "Pride in who you are, moral courage, and standards for how you allow yourself to be treated."),
            t("Self-concept", "Cognitive map of who you are (see 1.1) — distinct from esteem and efficacy."),
        ],
        "concepts": [
            "Esteem = global worth; efficacy = task-specific confidence; respect = dignity/treatment standards.",
            "You can have high esteem but low efficacy on a hard exam task (or the reverse).",
            "Faculty often test the esteem vs efficacy contrast with one concrete example.",
        ],
        "notes": [
            "LMR: “task-specific belief I can do X” → self-efficacy.",
            "LMR: “overall worth / like myself” → self-esteem.",
            "Don’t use self-concept when the stem is about worth or task confidence.",
            "One example ready: “I value myself (esteem) but doubt I can code this module (low efficacy).”",
        ],
    },
    "1.6": {  # LMR
        "terms": [
            t("Assertiveness", "Express thoughts/feelings truthfully while respecting others — between passivity and aggression."),
            t("Passive", "Withhold needs; avoid conflict at personal cost."),
            t("Aggressive", "Push needs without respect for others."),
            t("Assertive skill set", "Respect, Openness, Honesty, Accountability, Self-control, Delegation."),
        ],
        "concepts": [
            "Assertive ≠ aggressive: honesty plus respect is the differentiator.",
            "Delegation appears in the assertive skills list — not only a management technique.",
            "Links to EI (Module 2): self-regulation and social skill support assertiveness.",
        ],
        "notes": [
            "LMR: “between passive and aggressive” → assertiveness.",
            "Be ready to list 4–6 skills if asked (ROHASD mnemonic: Respect, Openness, Honesty, Accountability, Self-control, Delegation).",
            "If stem rewards “winning at all costs” → competing/aggression, not assertiveness.",
        ],
    },
    "1.7": {
        "terms": [
            t("Professional social media etiquette", "Respectful communication, privacy awareness, and appropriate sharing online."),
            t("Technology adoption", "How thoughtfully people take up tools in ways that affect reputation and norms."),
        ],
        "concepts": [
            "Online presence is part of workplace reputation — etiquette is professional behaviour, not optional manners.",
            "Oversharing and ignoring organisational norms are classic exam “wrong” cues.",
        ],
        "notes": [
            "Stem emphasises privacy / respectful posting / appropriate sharing → etiquette.",
            "Don’t answer with maximum authenticity-via-oversharing.",
        ],
    },
    "1.8": {  # LMR
        "terms": [
            t("ICEDIP (Geoff Petty)", "Inspiration, Clarification, Distillation, Perspiration, Evaluation, Incubation."),
            t("Incubation", "Stepping away so subconscious processing can occur."),
            t("Evaluation", "Judging strengths and flaws — not the same as incubation."),
            t("Visualization", "Mental rehearsal: combine outcome + process simulation; participant > observer perspective."),
        ],
        "concepts": [
            "ICEDIP phases can occur in any order and repeat; each phase has its own mind-set.",
            "Incubation ≠ evaluation — frequent mix-up.",
            "Visualization works better when you rehearse steps (process) not only the trophy (outcome).",
        ],
        "notes": [
            "LMR: expand all six ICEDIP letters once under exam pressure.",
            "“Step away / subconscious” → Incubation; “judge quality” → Evaluation.",
            "Visualization: participant perspective generally beats observer perspective.",
            "Order rule: any order, repeatable — don’t invent a fixed sequence as the only truth.",
        ],
    },
    "1.9": {
        "terms": [
            t("Problem sensitivity", "Capacity to notice when something is wrong or likely to go wrong."),
        ],
        "concepts": [
            "Sensitivity = recognition only; it does not include solving the problem.",
            "Distinct from cognitive flexibility (adapting strategies) and from Six Hats (structured thinking modes).",
        ],
        "notes": [
            "Stem “notice only / not solve” → problem sensitivity.",
            "If options include fixing the issue, that is problem solving — not sensitivity.",
        ],
    },
    "1.10": {  # LMR
        "terms": [
            t("Blue hat", "Process control — director of the thinking agenda."),
            t("White hat", "Facts and data only — no spin."),
            t("Red hat", "Feelings and intuition — no justification required in the moment."),
            t("Black hat", "Risks, caution, critical flaws — detached risk analysis."),
            t("Yellow hat", "Benefits and optimism."),
            t("Green hat", "Creativity and alternatives."),
        ],
        "concepts": [
            "Hats are parallel thinking modes — one mode at a time, not personality labels forever.",
            "Blue is meta-control: manages when other hats are used.",
            "Black ≠ “being a bad person”; it is disciplined caution.",
        ],
        "notes": [
            "LMR: map colour → function cold (Blue/White/Red/Black/Yellow/Green).",
            "“Facts only / detective” → White; “feelings” → Red; “risks” → Black; “ideas” → Green.",
            "Blue hat ≠ content expert — it runs the process.",
            "Don’t confuse hat colours with Tuckman stages or conflict styles.",
        ],
    },
    "1.11": {  # LMR
        "terms": [
            t("Cognitive flexibility", "Disengage from one task, hold several concepts, adapt strategies to new conditions — learnable."),
            t("Polarized / all-or-nothing", "Seeing only extremes; no middle ground."),
            t("Overgeneralization", "One event becomes a forever rule."),
            t("Mental filter", "Dwelling on one negative detail."),
            t("Emotional reasoning", "“I feel it, therefore it is true.”"),
            t("Mind reading / fortune telling", "Assuming others’ thoughts or predicting catastrophe as fact."),
        ],
        "concepts": [
            "SLM packs flexibility with Beck/Burns cognitive errors as one exam cluster.",
            "Flexibility is executive-function skill; errors are biased thinking patterns — related but not identical.",
            "Emotional reasoning is a high-yield named error with a one-line example.",
        ],
        "notes": [
            "LMR: name 4–5 errors with a tiny example each (especially emotional reasoning, all-or-nothing).",
            "“I feel anxious so the project is failing” → emotional reasoning.",
            "Flexibility stem focuses on adapting / switching sets, not listing biases.",
            "Don’t dump Six Hats colours as “cognitive errors.”",
        ],
    },
    "1.12": {
        "terms": [
            t("Social cognition", "How people perceive, recall, attend to, and use social information."),
            t("Schema", "Mental structure of general knowledge about a social object or situation."),
            t("Salience", "How much a cue stands out and grabs attention."),
            t("Priming", "Recent exposure makes a schema more accessible."),
            t("Social inference", "Inferring intentions, desires, emotions, traits from observed behaviour."),
        ],
        "concepts": [
            "Salience and priming both raise schema accessibility — different routes.",
            "Social inference supports social success; it is part of the social cognition family.",
            "Attribution (1.13) is a specialised form of causal inference about behaviour.",
        ],
        "notes": [
            "“Recent exposure makes idea come to mind” → priming.",
            "Don’t answer FAE when the stem is only about schemas/priming.",
        ],
    },
    "1.13": {  # LMR
        "terms": [
            t("Attribution", "Inferring causes of behaviour."),
            t("Internal / personal causes", "Personality, ability, effort."),
            t("External / situational causes", "Environment, luck, others’ actions."),
            t("Fundamental attribution error (FAE)", "For others: overestimate personal causes, underestimate situation."),
            t("Actor–observer difference", "For self as actor: emphasise external causes more than when observing others."),
            t("Self-serving bias", "Credit success internally; blame failure externally."),
        ],
        "concepts": [
            "FAE targets explanations of others; actor–observer is about self vs other perspectives; self-serving protects self-image.",
            "All three are attribution biases — learn the trio as a set.",
            "Internal vs external is the basic causal split before biases.",
        ],
        "notes": [
            "LMR trio: FAE · actor–observer · self-serving — one line each.",
            "“He failed because he’s lazy” (ignoring context) → FAE.",
            "“I failed because the exam was unfair” after “I passed because I’m smart” → self-serving.",
            "Don’t swap FAE with self-serving when the stem is about judging other people.",
        ],
    },
    "1.14": {  # LMR
        "terms": [
            t("Stereotype", "Cognitive generalization about a group (“pictures in our heads”)."),
            t("Prejudice", "Derogatory / evaluative attitude toward group members."),
            t("Discrimination", "Behaviour — unfair treatment based on group membership."),
            t("Contact hypothesis path", "Intergroup contact can reduce prejudice via knowledge, lower anxiety, empathy."),
        ],
        "concepts": [
            "Stereotype = cognitive; prejudice = evaluative attitude; discrimination = behaviour.",
            "Prejudice is not automatically the same as discriminatory acts.",
            "Accepting criticism skills (calm, restate, open perspectives) are packed on this map card with S-P-D.",
        ],
        "notes": [
            "LMR: “generalized idea about a group” → stereotype; “negative attitude” → prejudice; “unequal treatment” → discrimination.",
            "Contact reduces prejudice by knowledge + empathy + lower anxiety — not by increasing distance.",
            "Criticism steps: remain calm → reiterate (“So you’re saying…”) → open both views → polite exit if needed.",
            "Don’t call prejudice a behaviour; that’s discrimination.",
        ],
    },

    # ----- Module 2 -----
    "2.1": {
        "terms": [
            t("Attitude", "Evaluation of a person, idea, or object as favourable or unfavourable."),
        ],
        "concepts": [
            "Attitudes are evaluative orientations that influence perception and behaviour (Allport’s centrality in social psychology).",
            "Attitude object = whatever is being evaluated.",
        ],
        "notes": [
            "Definition stem → evaluation, not a Tuckman stage or sociometric pattern.",
        ],
    },
    "2.2": {  # LMR
        "terms": [
            t("Valence", "Magnitude of favourability or unfavourability."),
            t("Multiplicity", "Number of components in the attitude system (simple vs complex)."),
            t("Centrality", "Importance of the object to the person; central attitudes resist change."),
            t("Pervasiveness", "Attitudes show up across domains via socialization."),
            t("Invisible / acquired", "Inferred from effects; learned over life (often family-transmitted)."),
        ],
        "concepts": [
            "Characteristics pack: valence, multiplicity, needs served, centrality, pervasiveness, invisible, acquired.",
            "High centrality → hard to change; useful for persuasion and change questions.",
            "Valence is strength of +/−, not the same as multiplicity (how many pieces).",
        ],
        "notes": [
            "LMR: “strength of favour/unfavour” → valence; “importance / resists change” → centrality.",
            "Be ready to explain needs, pervasiveness, invisible, acquired in one line each.",
            "Don’t confuse valence with VI (Idealized Influence) or with emotion intensity alone.",
        ],
    },
    "2.3": {  # LMR
        "terms": [
            t("Cognitive component", "Beliefs and knowledge about the attitude object."),
            t("Affective component", "Feelings toward the object."),
            t("Behavioural component", "Action tendency / how one tends to act."),
        ],
        "concepts": [
            "Attitude ABC = Affective–Behavioural–Cognitive evaluation structure.",
            "Ellis ABC (Module 5) is Adversity–Beliefs–Consequences — different model, similar letters.",
            "Belief statement (“discrimination is wrong”) is mainly cognitive; anger about it is affective.",
        ],
        "notes": [
            "LMR: map stem language to A/B/C carefully.",
            "If Adversity/Activating event appears → Ellis, not Attitude ABC.",
            "TEA (1.2) is thoughts–emotions–actions influence, not the attitude ABC triad.",
        ],
    },
    "2.4": {
        "terms": [
            t("Emotion", "Powerful, often triggered, more intentional affective state."),
            t("Mood", "Prolonged, less intense, not necessarily triggered; may lack intentionality."),
            t("Healthy expression", "Less intense/lasting; life can continue."),
            t("Unhealthy expression", "High intensity, long duration, hard to control, disrupts daily life."),
        ],
        "concepts": [
            "SLM does not say “positive = good / negative = useless” — intensity, duration, and control matter.",
            "Self-awareness of emotion underpins EI (2.5).",
        ],
        "notes": [
            "Emotion vs mood: intensity + trigger + intentionality.",
            "Unhealthy ≠ simply “negative feeling.”",
        ],
    },
    "2.5": {  # LMR
        "terms": [
            t("Emotional intelligence", "Interpret, reason about, understand, and manage own and others’ emotions; stay stable and communicate."),
            t("Self-awareness", "Know your emotions as they happen."),
            t("Self-regulation", "Think before acting; manage disruptive impulses."),
            t("Motivation", "Drive toward goals with energy and persistence."),
            t("Empathy", "Understand others’ feelings."),
            t("Social skills", "Manage relationships and build networks."),
        ],
        "concepts": [
            "Goleman five: self-awareness, self-regulation, motivation, empathy, social skills.",
            "Personal competence = awareness/regulation/motivation; social competence = empathy + social skills.",
            "Faculty: EI usually outweighs interpersonal intelligence alone for exam priority.",
        ],
        "notes": [
            "LMR: list all five competencies cold.",
            "Sociometric starring / Tuckman / hat colours are not EI competencies.",
            "EI spans self and others; intrapersonal (2.6) focuses on self.",
        ],
    },
    "2.6": {
        "terms": [
            t("Interpersonal intelligence", "Understand others’ minds; communicate; form and sustain relationships."),
            t("Intrapersonal intelligence (Gardner)", "Understand oneself — interests, fears, abilities — and manage one’s life."),
        ],
        "concepts": [
            "Interpersonal = others; intrapersonal = self; EI covers both with emotion focus.",
            "Self-awareness underpins intrapersonal skill and EI.",
            "Exam priority cue from faculty: EI > interpersonal intelligence alone.",
        ],
        "notes": [
            "“Understanding myself to manage my life” → intrapersonal.",
            "“Reading others / rapport / social comfort” → interpersonal.",
            "If stem asks which faculty prioritises → EI over interpersonal alone.",
        ],
    },

    # ----- Module 4 -----
    "4.1": {
        "terms": [
            t("Conflict", "Incompatible goals, cognitions, or emotions within/between people or groups."),
            t("Goal conflict", "Incompatible desired outcomes."),
            t("Cognitive conflict", "Incompatible ideas or interpretations."),
            t("Affective conflict", "Incompatible emotions (e.g. anger between people)."),
            t("Latent stage", "Conditions with potential for conflict before open clash."),
            t("Manifest stage", "Open antagonistic behaviour."),
        ],
        "concepts": [
            "Stages often framed: Latent → Perceived → Felt → Manifest.",
            "Conflict is common and not always negative — resolution can yield constructive problem solving.",
            "Sources include unclear responsibilities, poor processes, communication problems.",
        ],
        "notes": [
            "“Incompatible feelings / anger at each other” → affective conflict.",
            "“Conditions exist but no open fight yet” → latent.",
            "Disagreement alone ≠ full conflict until opposition escalates.",
        ],
    },
    "4.2": {
        "terms": [
            t("Conflict impact", "Can harm trust/performance — or spur creativity if managed."),
            t("Ethical dilemma under pressure", "e.g. unrealistic goals that tempt cutting corners; toxic culture; misuse of time/tech."),
        ],
        "concepts": [
            "Impact is two-sided: damage vs constructive tension.",
            "Goal pressure is a classic ethics risk in conflict settings.",
        ],
        "notes": [
            "Unrealistic targets + corner-cutting → ethical dilemma framing.",
            "Don’t answer “conflict is always good.”",
        ],
    },
    "4.3": {
        "terms": [
            t("Competing", "High assertiveness, low cooperativeness — win at all costs."),
            t("Collaborating", "High assertiveness and cooperativeness — seek win–win."),
            t("Compromising", "Moderate on both — split the difference."),
            t("Avoiding", "Low assertiveness and cooperativeness — sidestep."),
            t("Accommodating", "Low assertiveness, high cooperativeness — yield."),
        ],
        "concepts": [
            "Match style to stakes: outcome-critical → competing; relationship + outcome → collaborate/compromise.",
            "Little time → avoiding / competing / accommodating; lots of time → collaborate / compromise.",
            "Styles are tools, not personality forever.",
        ],
        "notes": [
            "“Win at all costs / highly assertive, uncooperative” → competing.",
            "Relationship + outcome + time allows → collaborate or compromise.",
            "Don’t pick collaborating when the stem says emergency with no time.",
        ],
    },
    "4.4": {
        "terms": [
            t("Mediation", "Neutral facilitator helps parties; does not take sides or impose a verdict."),
            t("Interests under positions", "What people truly need vs the demands they state."),
            t("Intercultural conflict", "Culture shapes how disagreement, face-saving, and decisions are expressed."),
        ],
        "concepts": [
            "Mediator keeps process fair, focuses on interests, avoids blame, helps generate options.",
            "Preconditions: willingness to participate and a workable setting.",
            "Misreading cultural cues can escalate conflict.",
        ],
        "notes": [
            "Mediator ≠ judge or partisan advocate.",
            "Intercultural awareness is communication skill inside conflict resolution, not a separate “hat.”",
        ],
    },
    "4.5": {
        "terms": [
            t("Distributive negotiation", "Claim value — fixed pie."),
            t("Integrative negotiation", "Create value — expand joint gains."),
            t("Negotiation stages", "Often preparation → exchange/bargaining → closing → implementation."),
        ],
        "concepts": [
            "Purpose includes agreements, contracts, and solving joint problems.",
            "Integrative seeks mutual gains; distributive divides a limited resource.",
        ],
        "notes": [
            "“Expand joint gains / mutual value” → integrative.",
            "“Split a fixed amount” → distributive.",
        ],
    },
    "4.6": {
        "terms": [
            t("Pillar 1 — relationships", "Build productive relationships (Comprehend–Anticipate–Connect)."),
            t("Pillar 2 — outcomes", "Pursue outcomes, not debating points."),
            t("Pillar 3 — joint problem solving", "Shift from “your way/my way” to shared needs."),
            t("Pillar 4 — fairness", "Agreements people will carry out voluntarily."),
        ],
        "concepts": [
            "Persuasion, professional conduct, and clear closing support follow-through.",
            "Fairness and relationship quality affect whether deals stick.",
        ],
        "notes": [
            "“Pursue outcomes, not points” = check whether terms advance real goals.",
            "Comprehend–Anticipate–Connect → relationship pillar, not Black-hat criticism.",
        ],
    },

    # ----- Module 5 -----
    "5.1": {  # LMR
        "terms": [
            t("Values", "Fundamental beliefs directing desirable behaviour or end states."),
            t("Terminal values", "Desired end outcomes (e.g. freedom, true friendship)."),
            t("Instrumental values", "Preferred modes of behaviour/means (e.g. responsibility, independence)."),
            t("Ethics", "Moral right/wrong and codes of conduct (from ethos, “character”)."),
        ],
        "concepts": [
            "Instrumental values help reach terminal ends (means → ends).",
            "Values shape what is desirable; ethics judges right conduct — related but distinct.",
            "Organisations encode both in mission, vision, and policies.",
        ],
        "notes": [
            "LMR: terminal = ends; instrumental = means.",
            "“Being responsible to achieve true friendship” → instrumental serving terminal.",
            "Don’t confuse Rokeach types with Attitude valence or Tuckman stages.",
        ],
    },
    "5.2": {
        "terms": [
            t("Personal values (examples)", "Empathy, honesty, courage, commitment."),
            t("Core values (SLM set)", "Respect, responsibility, integrity, care, harmony."),
        ],
        "concepts": [
            "Moral values and moral icons support character / “new self-awareness.”",
            "Core values list is a frequent recall item.",
        ],
        "notes": [
            "Core values set: respect, responsibility, integrity, care, harmony.",
            "Don’t substitute Tuckman stage names for core values.",
        ],
    },
    "5.3": {  # LMR
        "terms": [
            t("Resilience", "Dynamic positive adaptation in the face of serious adversity."),
            t("Adversity", "Acute crises or chronic low-intensity workplace stress."),
        ],
        "concepts": [
            "Definition requires both adversity experience and positive adaptation.",
            "Viewed as trait, developable capability, and/or process.",
            "Links to EI, networks (5.5), and agility (5.6) without being identical to them.",
        ],
        "notes": [
            "LMR: both adversity + positive adaptation must appear in the answer.",
            "High valence attitudes alone ≠ resilience.",
            "Sociometric star ≠ resilience definition.",
        ],
    },
    "5.4": {  # LMR
        "terms": [
            t("Paradox of choice", "Many options can overwhelm decisions and reduce satisfaction."),
            t("Ellis ABC", "Adversity/Activating event → Beliefs → Consequences (emotions/behaviours)."),
        ],
        "concepts": [
            "Beliefs mediate reactions — events alone do not fully determine feelings.",
            "Ellis ABC ≠ Attitude ABC (affective–behavioural–cognitive).",
            "Choice paradox is a coping/uncertainty theme beside Ellis.",
        ],
        "notes": [
            "LMR: B = Beliefs in Ellis ABC.",
            "Attitude ABC centres on evaluation components; Ellis centres on beliefs about adversity.",
            "Don’t answer Blue hat or branding for Ellis “B.”",
        ],
    },
    "5.5": {
        "terms": [
            t("Resilience resources", "Personality/cognitive variables, family/social networks, work demands and resources."),
            t("Stress management", "Coping skills, support, and resource building."),
        ],
        "concepts": [
            "Family and social networks are framed as supports that can promote resilience.",
            "Stress shows models, symptoms, consequences — management is resource-based.",
        ],
        "notes": [
            "Networks in Unit 5.2 framing = resilience-promoting supports, not irrelevant.",
            "Don’t treat networks only as FAE sources.",
        ],
    },
    "5.6": {
        "terms": [
            t("VUCA", "Volatility, Uncertainty, Complexity, Ambiguity."),
            t("Agility", "Adapting methods and behaviours under turbulent, unpredictable conditions."),
            t("VUCA Prime (Johansen)", "e.g. Vision as a response pairing to Volatility."),
        ],
        "concepts": [
            "Agility answers VUCA; resilience answers adversity — complementary.",
            "U in VUCA = Uncertainty (not Utility/Urgency alone).",
        ],
        "notes": [
            "“U” → Uncertainty.",
            "Agility ≠ refusing change; ≠ only competing conflict style.",
            "Don’t enlarge Hidden Johari pane as an agility answer.",
        ],
    },
}


def load_m3_from_existing() -> dict:
    path = SUBJECTS / "bs605" / "_deep_notes.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if k == "m3_root" or k.startswith("3.")}


def write_bs605() -> None:
    m3 = load_m3_from_existing()
    out = dict(BS605)
    out.update(m3)  # keep handcrafted Module 3
    path = SUBJECTS / "bs605" / "_deep_notes.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"BS605: {len(out)} entries -> {path}")


def looks_like_toc(text: str) -> bool:
    if not text:
        return True
    ids = re.findall(r"\b\d+(?:\.\d+){1,3}\b", text)
    return len(ids) >= 2


def author_topic_deep(topic: dict, lmr: bool) -> dict:
    """Build Terms/Concepts/Notes that are deeper than Overview — never TOC junk."""
    terms: list[dict] = []
    concepts: list[str] = []
    notes: list[str] = []
    cards = topic.get("flashcards") or []
    mcqs = topic.get("mcqs") or []
    title = (topic.get("title") or topic.get("id") or "Topic").strip()
    tid = str(topic.get("id") or "")

    # Primary term = topic title + best definition card
    definition = ""
    for c in cards:
        back = (c.get("back") or "").strip()
        front = (c.get("front") or "").strip()
        if looks_like_toc(back):
            continue
        if front.lower().startswith("exam focus"):
            if back and not looks_like_toc(back):
                notes.append(back)
            continue
        if len(back) > len(definition):
            definition = back
        detail = (c.get("detail") or "").strip()
        if detail and not detail.startswith(tid):
            notes.append(detail)

    if definition:
        terms.append({"t": title, "d": definition})
    else:
        terms.append(
            {
                "t": title,
                "d": f"Syllabus topic {tid}: learn the definition, operations/steps, and one contrast with a neighbour concept.",
            }
        )

    # Extra terms: split definition on semicolons / "vs" style fragments when long
    if definition and ("." in definition or ";" in definition):
        parts = [p.strip() for p in re.split(r"(?<=[.|;])\s+", definition) if len(p.strip()) > 25]
        for i, part in enumerate(parts[1:3], start=2):
            terms.append({"t": f"Point {i}", "d": part})

    concepts.append(f"{title} sits in this module’s map — Overview is the short blurb; these terms are the exam definition.")
    if lmr:
        concepts.append("LMR: say the definition aloud, then one use-case, then one contrast with a related topic.")
    else:
        concepts.append("Link this topic to its unit neighbours so you can spot ‘which structure/method’ stems.")

    for q in mcqs:
        explain = (q.get("explain") or "").strip()
        if explain and not looks_like_toc(explain):
            notes.append(f"Exam cue: {explain}")

    # Specific trap note from title keywords
    low = title.lower()
    if "stack" in low:
        notes.append("Trap: Stack is LIFO (top) — do not confuse with Queue (FIFO).")
    elif "queue" in low:
        notes.append("Trap: Queue is FIFO — enqueue rear, dequeue front; not LIFO.")
    elif "list" in low:
        notes.append("Trap: Linked list uses pointers/nodes — not the same as a contiguous array.")
    elif "hash" in low:
        notes.append("Trap: Average O(1) assumes a good hash and load factor — worst case can degrade.")
    elif "sort" in low:
        notes.append("Trap: Compare time, space, and stability — not only ‘faster’.")
    elif "encrypt" in low or "cipher" in low:
        notes.append("Trap: Encryption protects confidentiality; integrity/authentication need other controls too.")
    elif "sample" in low:
        notes.append("Trap: Sample ≠ population; state the sampling frame when answering.")
    elif "hypothes" in low:
        notes.append("Trap: A hypothesis must be testable — not only a vague opinion.")

    if not any(n.startswith("Trap:") for n in notes):
        notes.append(f"Be ready to define {title} and give one use / one contrast — vague labels lose marks.")

    seen: set[str] = set()
    uniq: list[str] = []
    for n in notes:
        n = n.strip()
        if not n or n in seen or looks_like_toc(n):
            continue
        # drop useless “From course · id” only lines
        if re.match(r"^[\d.]+ · ", n) and len(n) < 60:
            continue
        seen.add(n)
        uniq.append(n)

    max_terms = 6 if lmr else 4
    max_concepts = 4 if lmr else 3
    max_notes = 7 if lmr else 4
    return {
        "terms": terms[:max_terms],
        "concepts": concepts[:max_concepts],
        "notes": uniq[:max_notes],
    }


def write_other_subject(subject_id: str) -> None:
    base = SUBJECTS / subject_id
    facts = json.loads((base / "_study_facts.json").read_text(encoding="utf-8"))
    maps = json.loads((base / "_module_maps.json").read_text(encoding="utf-8"))
    lmr_ids: set[str] = set()
    out: dict = {}

    for mod in maps["modules"]:
        root = mod["root"]
        out[root["id"]] = {
            "terms": [{"t": root["title"], "d": root.get("body") or ""}],
            "concepts": list(root.get("points") or [])[:4],
            "notes": [
                "Open topic cards for Terms · Concepts · Short notes.",
                "LMR cards (orange) are denser where marked.",
            ],
        }
        for level in mod["levels"]:
            for n in level["nodes"]:
                if n.get("lmr"):
                    lmr_ids.add(str(n.get("topicId") or n["id"]))

    for mod in facts["modules"]:
        for topic in mod["topics"]:
            tid = str(topic["id"])
            out[tid] = author_topic_deep(topic, lmr=(tid in lmr_ids))

    path = base / "_deep_notes.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{subject_id}: {len(out)} entries ({len(lmr_ids)} LMR) -> {path}")


def main() -> None:
    write_bs605()
    for sid in ("cse601", "csit654", "csit745"):
        write_other_subject(sid)
    # sanity: no generic filler
    bs = json.loads((SUBJECTS / "bs605" / "_deep_notes.json").read_text(encoding="utf-8"))
    bad = []
    for k, v in bs.items():
        for n in v.get("notes") or []:
            if "neighbouring topics that share similar vocabulary" in n.lower():
                bad.append(k)
            if n.startswith("Skim Overview") or n.startswith("LMR focus: be able"):
                bad.append(k)
            if n.startswith("Recall cue —"):
                bad.append(k)
    if bad:
        raise SystemExit(f"Filler still present in: {bad}")
    print("OK: no generic filler lines in BS605 deep notes")


if __name__ == "__main__":
    main()
