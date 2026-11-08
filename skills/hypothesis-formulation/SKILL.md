---
name: hypothesis-formulation
description: >-
  Turns a topic or candidate gap into a testable research question in PICO/PICOT form with explicit hypotheses or a performance target. Use when the user says "formulate a hypothesis", "sharpen the research question", "PICO", or after an optional gap check. (Türkçe: hipotez, araştırma sorusu.)
---

# Hypothesis and Research Question Formulation

## Purpose

Reduce a broad or fuzzy topic to a question sharp enough to determine the design and the analysis.

## Input

`research/<slug>/00_gap_analysis.md` if it exists (it is optional), plus whatever the user tells you about their interest, setting and constraints.

## Steps

1. Put the chosen candidate into **PICO(T)**:
   - **P** — exactly who: age range, diagnostic criteria, route of presentation, exclusions.
   - **I/E** — what is applied or measured: an intervention, an exposure, a clinical feature, a prediction model.
   - **C** — compared with what: standard care, another model, another group. A prediction-model study without a comparator is valid, but say so explicitly.
   - **O** — exactly what, over which time window (for example "in-hospital mortality", "72-hour return visit", "30-day readmission").
   - **T** — follow-up period, if relevant.
2. Write the **primary research question in one sentence**. List secondary questions separately, but keep the primary one unambiguous.
3. State the hypotheses: H0 and H1 (with the expected direction if there is one). For prediction-model studies, a **primary performance objective** can replace classical H0/H1 (for example "discrimination and calibration acceptable in an external sample"); choose whichever fits the study type and say why. For prediction models, also record the intended use: who will use the prediction, at what moment, to decide what.
4. Write 2–3 sentences linking the question to the gap: why it matters, what is known, what is missing. Use only background the user supplied or that is in `00_gap_analysis.md` (with sources); otherwise leave a labelled placeholder ("background needs a source") rather than writing it from memory.
5. **Measurability check**: for every term (outcome, exposure, predictor) is there a concrete, extractable source (a registry field, a laboratory value, a documented note)? If not, rephrase the question or warn the user now.
6. **Refutation criterion**: ask what observed result would make the user give up the hypothesis (for a prediction model: the performance below which it would not be useful). A hypothesis that no result could contradict is not yet a hypothesis; rephrase it.
7. **Scope boundary**: write one plain line on what this study does **not** investigate (related questions deliberately left out). If the material contains two or more studies that need their own design, registration or ethics application, say so now and ask whether to split them.

## Output

`research/<slug>/01_hypothesis.md`:

- PICO(T) table
- Primary research question (one sentence); secondary questions if any
- H0/H1 or performance objective (and, for prediction models, the intended use)
- Link to the gap / rationale
- Measurability notes (first impressions of where each variable would come from; detailed feasibility is the next phase)
- Refutation criterion (what result would make you reject the hypothesis)
- Not investigated (one line of scope boundary)

## Quality checks

- Self-review before saving: scan for placeholders ("TBD", "relevant literature" with no specifics), terms that could mean two things, and numbers with no source and no "assumed" label.

- One primary outcome only. Multiple primary outcomes complicate the sample-size calculation and the analysis. For a prediction-model study, the outcome is one, but name the primary performance measure (for example calibration slope or C-statistic) that will drive the sample size.
- The outcome has a time window; "mortality" alone is not enough.
- Constraints the user has already mentioned (for example limits on follow-up, data access or case volume) are respected. If they conflict with the hypothesis, catch it now, not two phases later.
- If the study is a prediction-model or ML study, suggest the `prediction-model-design` skill as the next step after design/feasibility.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
