---
name: sap-builder
description: >-
  Drafts a statistical analysis plan (SAP): descriptive and primary/secondary analyses, missing-data method, multiplicity, reporting guideline choice (STROBE, STARD, TRIPOD family). For prediction/ML studies it pulls the modelling and validation plan from the 02a file produced by prediction-model-design, which must run first. Use for "analysis plan", "SAP", "which statistical test". (Türkçe - istatistiksel analiz planı, SAP.)
---

# Statistical Analysis Plan (SAP)

## Purpose

Lock down **how the data will be analyzed before analysis starts**, which reduces outcome switching and p-hacking, and tie the study to the right reporting guideline.

## Input

`research/<slug>/01_hypothesis.md`, `02_design_feasibility.md`, `03_sample_size.md`, `04_data_dictionary.md`; for prediction/ML studies also `02a_prediction_model_plan.md` (**run `prediction-model-design` first; if it does not exist, route the user there rather than inventing a modelling plan**); and `04a_llm_extraction_protocol.md` if LLM extraction is used.

## Steps

1. **Descriptive plan**: how each variable is summarized (mean ± SD, median [IQR], n (%)) and which tests compare groups, chosen by distribution.
2. **Primary analysis**:
   - Classical hypothesis test: which test, one- or two-sided, adjustment for confounders (model, covariates and why), multiplicity correction if there is more than one primary comparison.
   - Prediction/ML model: do not write modelling details here from scratch. Pull them from `02a_prediction_model_plan.md` (algorithms, a regression baseline, predictor handling, validation design, performance measures including calibration and clinical utility), and make sure the SAP is consistent with it.
3. **Secondary and subgroup analyses**: define them in advance. Mark anything added after looking at the data as **exploratory / post hoc**.
4. **LLM-extracted variables** (if `04a` exists): carry the validation plan into the SAP, including how extraction error will be handled downstream (for example a sensitivity analysis on the manually abstracted subset, or misclassification correction).
5. **Missing data**: make the data-dictionary strategy formal (for example multiple imputation: number of imputations, variables included, assumptions about the missingness mechanism) and plan a sensitivity analysis.
6. **Reporting guideline**:
   - Observational cohort / case-control / cross-sectional → STROBE (and its extension for routinely collected health data, if the data come from records)
   - Diagnostic accuracy → STARD 2015; STARD-AI when the index test is an AI system
   - Prediction model development/validation, including ML → TRIPOD+AI, with PROBAST+AI as the appraisal tool (verified citations in `../prediction-model-design/references/guidelines-and-sample-size.md`)
   - Studies that use an LLM → TRIPOD-LLM (see `llm-extraction-validation` for which parts apply)
   List the main checklist headings and confirm the study will be able to report them. Confirm the current version of the guideline before citing it.
7. **Software**: name the language and packages (R/Python), matched to the user's stated statistical experience. Prefer a small, well-known toolset over an elaborate one.
8. Recommend a `biostatistics-reviewer` pass.

## Output

`research/<slug>/05_sap.md`:

- Descriptive plan
- Primary analysis (method and justification)
- Secondary / subgroup analyses (pre-specified vs exploratory)
- Missing-data method and sensitivity analysis
- Reporting guideline and key-heading checklist
- Software and packages
- Reviewer result, if available

## Quality checks

- The SAP must be written **before** data are analyzed. Say so; a post hoc SAP weakens credibility.
- Every SAP with a model must plan for **calibration and external or temporal validation**; reporting discrimination (AUC) alone is not enough.
- Check that analysis choices match the variable coding in the data dictionary.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
