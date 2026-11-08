---
name: study-design-feasibility
description: >-
  Chooses the study design, lists variables (exposure, outcome, confounders) and audits feasibility: where each variable lives in the records, timestamp reliability, follow-up, case volume, selection bias. Use for "choose a design", "is this feasible", "which data do I need". (Türkçe - çalışma tasarımı, fizibilite.)
---

# Study Design and Feasibility Audit

## Purpose

Turn the abstract question into a plan that can really be executed. A feasibility problem found late is the most expensive mistake in a study, so this skill leans on **asking questions and auditing the available data**, not on producing solutions quickly.

## Input

`research/<slug>/01_hypothesis.md`.

## Steps

1. **Pick and justify the design**: retrospective cohort, case-control, cross-sectional, prospective cohort, diagnostic accuracy, prognostic/prediction-model development and/or validation. (Systematic or scoping reviews are out of scope here: use a dedicated review tool such as the lr-ai plugin.) Make sure it fits the outcome and time window in the hypothesis. A prediction-model study is usually a (retrospective) cohort with model development and validation; say so.
2. **List the variables**: outcome(s), main exposure(s) or predictor(s), known confounders (from the literature), demographic and clinical covariates. For each: definition, timing relative to the outcome, and data source.
3. **Feasibility audit.** Ask the user these questions (if they know the answers, ask for them directly; if they do not, propose a small pilot chart review, and first confirm with the ethics committee secretariat or data-protection contact whether even a pilot record review needs approval):
   - Is each variable in a **structured field** of the hospital information system / EHR, or only in **free text**? Free-text variables need an extraction strategy (manual abstraction form, or LLM-assisted extraction with a validation subsample); flag it now, detail it in the data-dictionary phase.
   - Are critical **timestamps** system-generated (logs, PACS, laboratory systems) or manually entered?
   - Is **follow-up** for the outcome realistic? Apply constraints the user has already stated; fall back to in-hospital or discharge outcomes when long follow-up is impossible.
   - Do **annual case volume and the retrospective window** plausibly reach the sample size the study will need? (A rough estimate now; the exact one comes next.)
   - Do the inclusion/exclusion criteria **create selection bias** (for example by excluding the sickest patients)? `methodology-critic` will look deeper later; flag the obvious ones here.
   - **Single centre or multicentre**? If multicentre, are data definitions harmonized?
   - Does the **prediction time point** exist in the data (all predictors available before the moment the model would be used)?
4. If you find a serious blocker (for example the key outcome is not recorded), say so plainly and suggest going back to the hypothesis phase. Going back and forth is normal and cheap at this stage.
5. **Scope check**: does the material describe more than one study (for example a trial and a later real-world audit, or development and validation of a model)? If so, say it here and ask whether to split them into separate `research/<slug>/` folders before sample size, ethics and SAP are written for a mixed protocol.

## Output

`research/<slug>/02_design_feasibility.md`:

- Chosen design and rationale
- Variable table (outcome / exposure or predictor / confounder, source, structured vs free text)
- Feasibility audit answers
- Identified risks and proposed mitigations
- Pilot chart-review proposal when uncertainty is high (how many records)
- If it is a prediction-model or ML study: note that `prediction-model-design` should run before sample size

## Quality checks

- Do not assume "this data probably exists". Ask. If the user does not know, record "unknown — pilot review needed".
- Keep the design consistent with the outcome and time window in the hypothesis.
- Self-review before saving: scan for placeholders, terms that could mean two things, and numbers with no source and no "assumed" label.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
