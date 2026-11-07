---
name: data-dictionary-crf
description: >-
  Builds a data dictionary / case report form (CRF) from the variable list: definition, type, source (structured field vs free text), coding, missing-data handling. Decides manual vs LLM abstraction for free-text variables and defines the manual abstraction protocol; LLM extraction itself goes to llm-extraction-validation. Use for "data dictionary", "CRF", "code the variables". (Türkçe - veri sözlüğü, vaka rapor formu, veri toplama formu.)
---

# Data Dictionary / CRF

## Purpose

Produce a dataset definition that is analyzable, consistent, and can be handed to another researcher or a biostatistician.

## Input

`research/<slug>/02_design_feasibility.md` (variable list and, for each variable, whether it is structured or free text); `01_hypothesis.md` for outcome definitions; and, for prediction studies, `02a_prediction_model_plan.md` (predictor and outcome definitions, leakage assessment, prediction time point).

## Steps

1. Build one row per variable: **Name | Definition | Type (continuous / ordinal / categorical / binary / date-time / free text) | Source (system field / free-text note type / external registry) | Coding (for example 0 = absent, 1 = present; category list; units) | Missing-data code and handling**.
2. For **free-text variables**, write an abstraction protocol:
   - Which note types to read (triage note, consultation note, radiology report, discharge summary).
   - An explicit, repeatable rule, for example "record the score if it is stated in the note, otherwise mark 'not documented'; do not infer".
   - Method: (a) fully manual abstraction (gold standard, time-consuming), or (b) LLM-assisted extraction, which requires a manually validated held-out sample with independent annotation and pre-specified acceptance thresholds. If (b) is chosen, **use the `llm-extraction-validation` skill** and do not proceed without its validation plan.
3. Set a general **missing-data strategy** (complete-case, imputation, "missingness as a category") and note that the SAP will make it formal.
4. Check that the coding suits the planned analysis: do not categorize continuous variables without a reason, and make sure coding works as model input (one-hot, ordinal, continuous) if a model is planned.
5. **Privacy**: confirm there are no direct identifiers in the analysis dataset, that a study-specific ID is used, and that the linkage key is stored separately with restricted access. Also handle quasi-identifiers: use relative days instead of exact dates, top-code extreme ages, review rare diagnoses, and strip names from free-text fields.

## Output

`research/<slug>/04_data_dictionary.md`:

- Full variable table with the columns above
- Free-text abstraction protocol (rules, who abstracts, how disagreements are resolved)
- Missing-data strategy
- Privacy note (identifiers removed, ID scheme, where the key is stored)

## Quality checks

- Every variable's coding must be compatible with the statistical or ML method planned in the SAP.
- Never recommend LLM-assisted extraction on its own; it always needs a manually validated held-out sample (see `llm-extraction-validation`).
- Never put real patient identifiers into this document or into any search.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
