---
name: study-design-feasibility
description: >-
  Chooses the study design (records-based, prospective, interventional, educational or simulation-based, diagnostic or prediction), lists variables (exposure, outcome, confounders) and audits feasibility: where each variable lives in the records, or recruitment, consent, blinding and contamination for a prospective study. Use for "choose a design", "is this feasible", "which data do I need". (Türkçe: çalışma tasarımı, fizibilite, hangi çalışma tasarımı, bu çalışma yapılabilir mi, hangi verilere ihtiyacım var, retrospektif, calisma tasarimi.)
---

# Study Design and Feasibility Audit

## Purpose

Turn the abstract question into a plan that can really be executed. A feasibility problem found late is the most expensive mistake in a study, so this skill leans on **asking questions and auditing what is available**, not on producing solutions quickly.

## Input

`research/<slug>/01_hypothesis.md` and, if it exists, `research/<slug>/decisions.md` (scope and earlier choices; do not ask again what is already decided there).

## Steps

Ask the user **one question at a time**. Skip any question the user or `01_hypothesis.md` has already answered. For every choice the user owns (the design, the arms, the primary outcome, the scope), propose two or three options with your recommendation and a one-line reason each, ask the user to confirm, and note the confirmed choice in `research/<slug>/decisions.md`. Never settle these silently.

0. **Scope check first.** Does the material describe more than one study (for example a trial and a later real-world audit, or development and validation of a model)? If `decisions.md` already records a scope decision, reuse it. Otherwise say it here and ask whether to split them into separate `research/<slug>/` folders before sample size, ethics and SAP are written for a mixed protocol.
1. **Pick and justify the design.** Options: retrospective cohort, prospective cohort, ambispective cohort, case-control, cross-sectional, case series, diagnostic accuracy, prognostic/prediction-model development and/or validation, randomized trial, non-randomized or quasi-experimental study (before-after, interrupted time series), educational or simulation-based intervention study, survey or qualitative study. Make sure it fits the outcome and time window in the hypothesis. A prediction-model study is usually a (retrospective) cohort with model development and validation; say so. If the question turns out to be a systematic or scoping review, stop here: record the decision in `decisions.md` and hand over to a dedicated review tool such as the lr-ai plugin.
2. **List the variables**: outcome(s), main exposure(s) or predictor(s), confounders, demographic and clinical covariates. For each: definition, timing relative to the outcome, and data source. Propose confounders from clinical reasoning and label them "proposed, needs a source or the user's confirmation"; cite a source only if you retrieved it.
3. **Feasibility audit.** Use the branch that fits the design, one question at a time, in this order, and stop at the first serious blocker.

   *Records-based studies (retrospective or ambispective):*
   - Is each variable in a **structured field** of the hospital information system / EHR, or only in **free text**? Free-text variables need an extraction strategy (manual abstraction form, or LLM-assisted extraction with a validation subsample, which needs an environment your institution has approved); flag it now, detail it in the data-dictionary phase.
   - Are critical **timestamps** system-generated (logs, PACS, laboratory systems) or manually entered?
   - Is **follow-up** for the outcome realistic? Apply constraints the user has already stated; fall back to in-hospital or discharge outcomes when long follow-up is impossible.
   - Do **annual case volume and the retrospective window** plausibly reach the sample size the study will need? (A rough estimate now; the exact one comes next.)
   - Do the inclusion/exclusion criteria **create selection bias** (for example by excluding the sickest patients)? `methodology-critic` will look deeper later; flag the obvious ones here.
   - **Single centre or multicentre**? If multicentre, are data definitions harmonized?
   - Does the **prediction time point** exist in the data (all predictors available before the moment the model would be used)?

   *Prospective, interventional, educational or simulation-based studies:*
   - How many eligible participants exist at the centre, how many will agree (eligible **and** willing), and over what period can they be recruited?
   - Consent and dependency: are participants trainees or staff of the investigators, so that participation could feel obligatory? Who recruits them?
   - Who delivers each intervention, and how will it be standardised (same trainer, script, material)?
   - Can allocation be randomised and concealed, and what can be blinded (participants, assessors, analysts)? What cannot?
   - How likely is contamination between arms (shared shifts, shared material), and how will it be limited?
   - Who measures the outcome, with what instrument, and is a second independent rater available?
   - Time, funding, equipment (for example a simulation centre) and the ethics route.

   If the user does not know an answer, record "unknown — pilot needed" and, for records, propose a small pilot chart review only after confirming with the ethics committee secretariat or data-protection contact whether even a pilot record review needs approval. In the session, the user brings only **counts, field names and aggregate impressions**, never patient records.
4. If you find a serious blocker (for example the key outcome is not recorded, or too few participants are available), say so plainly and suggest going back to the hypothesis phase. Going back and forth is normal and cheap at this stage.

## Output

`research/<slug>/02_design_feasibility.md`:

- Chosen design and rationale, and which feasibility branch was used (records-based or prospective/interventional)
- Variable table (outcome / exposure or predictor / confounder, source, structured vs free text; confounders labelled "proposed" unless sourced)
- Feasibility audit answers
- Identified risks and proposed mitigations
- Pilot proposal when uncertainty is high (how many records or participants)
- If it is a prediction-model or ML study: note that `prediction-model-design` should run before sample size

## Quality checks

- Do not assume "this data probably exists" or "participants will probably agree". Ask. If the user does not know, record "unknown — pilot needed".
- Keep the design consistent with the outcome and time window in the hypothesis.
- Self-review before saving, and fix what you find: placeholders; terms that could mean two things; numbers with no source and no "assumed" label; claims that no retrieved source supports.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Reply in the user's language; write the document in English unless the user asks otherwise.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
