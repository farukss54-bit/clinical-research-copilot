---
name: hypothesis-formulation
description: >-
  Turns a topic or candidate gap into a testable research question in PICO/PICOT form with explicit hypotheses, a performance target or an estimation aim, plus a refutation criterion and a scope boundary. Use when the user says "formulate a hypothesis", "sharpen the research question", "PICO", or wants to start the study design. (Türkçe: hipotez, araştırma sorusu, araştırma sorusunu netleştir, PICO yaz, hipotez kur, arastirma sorusu, hipotez.)
---

# Hypothesis and Research Question Formulation

## Purpose

Reduce a broad or fuzzy topic to a question sharp enough to determine the design and the analysis.

## Input

`research/<slug>/00_gap_analysis.md` if it exists (it is optional), `research/<slug>/decisions.md` if it exists (scope and earlier choices; do not ask again what is already decided there), plus whatever the user tells you about their interest, setting and constraints.

## Steps

Ask the user **one question at a time**. For every choice the user owns (the study question, the primary outcome, the form of the hypothesis, the refutation threshold), propose two or three options with your recommendation and a one-line reason each, ask the user to confirm, and note the confirmed choice in `research/<slug>/decisions.md`. Never settle these silently.

0. **Scope check first.** Does the material describe one study, or several that need their own design, registration or ethics application (for example a trial and a later real-world audit, or development and validation of a model)? If `decisions.md` already records a scope decision, reuse it. Otherwise ask whether to split them into separate `research/<slug>/` folders before going on.
1. Put the chosen candidate into **PICO(T)**:
   - **P** — exactly who: age range, diagnostic criteria, route of presentation, exclusions.
   - **I/E** — what is applied or measured: an intervention, an exposure, a clinical feature, a prediction model.
   - **C** — compared with what: standard care, another model, another group. A prediction-model study without a comparator is valid, but say so explicitly.
   - **O** — exactly what, over which time window (for example "in-hospital mortality", "72-hour return visit", "30-day readmission").
   - **T** — follow-up period, if relevant.
2. Write the **primary research question in one sentence**. List secondary questions separately, but keep the primary one unambiguous.
3. State the hypotheses: H0 and H1 (with the expected direction if there is one). Three forms exist; propose the one that fits and say why:
   - classical **H0/H1** for a comparison or an association;
   - for a prediction-model study, a **primary performance objective** (for example "discrimination and calibration acceptable in an external sample") and the intended use: who will use the prediction, at what moment, to decide what;
   - for a descriptive question (prevalence, incidence, a rate), an **estimation aim** with the target precision (for example the width of the 95% confidence interval) instead of H0/H1.
4. Write 2–3 sentences linking the question to the gap: why it matters, what is known, what is missing. Use only background the user supplied or that is in `00_gap_analysis.md` (with sources). Where a source is missing, leave a labelled placeholder ("background needs a source") and list it under "Open items" in the output; point the user to `quick-gap-check` or `pubmed-bridge` to fill it. Never write it from memory.
5. **Measurability check**: for every term (outcome, exposure, predictor) is there a concrete, extractable source (a registry field, a laboratory value, a documented note)? If not, rephrase the question or warn the user now.
6. **Refutation criterion**: ask what observed result would make the user abandon H1, that is, conclude there is no useful effect. Put it in measurable form: a minimal clinically important difference, a non-inferiority margin, or (for a prediction model) a minimum C-statistic or calibration. Label the number "user-supplied" or "assumed". A hypothesis that no result could contradict is not yet a hypothesis; rephrase it. (Not to be confused with "rejecting H0", which is the supportive result.)
7. **Scope boundary**: write one plain line on what this study does **not** investigate (related questions deliberately left out).

## Output

`research/<slug>/01_hypothesis.md`:

- PICO(T) table
- Primary research question (one sentence); secondary questions if any
- H0/H1, performance objective or estimation aim (and, for prediction models, the intended use)
- Link to the gap / rationale
- Measurability notes (first impressions of where each variable would come from; detailed feasibility is the next phase)
- Refutation criterion (what observed result would make you abandon H1, in measurable form)
- Not investigated (one line of scope boundary)
- Open items (labelled placeholders and anything the user still has to supply), or "none"

## Quality checks

- Self-review before saving, and fix what you find: placeholders ("TBD", "relevant literature" with no specifics) that are not listed under Open items; terms that could mean two things; numbers with no source and no "assumed" label; claims that no retrieved source supports; a missing statement of what the study does not investigate.
- One primary outcome only. Multiple primary outcomes complicate the sample-size calculation and the analysis. For a prediction-model study, the outcome is one, but name the primary performance measure (for example calibration slope or C-statistic) that will drive the sample size.
- The outcome has a time window; "mortality" alone is not enough.
- Constraints the user has already mentioned (for example limits on follow-up, data access or case volume) are respected. If they conflict with the hypothesis, catch it now, not two phases later.
- If the study is a prediction-model or ML study, suggest the `prediction-model-design` skill as the next step after design/feasibility.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Reply in the user's language; write the document in English unless the user asks otherwise.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
