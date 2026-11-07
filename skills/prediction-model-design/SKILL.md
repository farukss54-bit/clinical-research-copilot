---
name: prediction-model-design
description: >-
  ML/prediction-model module. Plans development or validation of a clinical prediction or machine-learning model: intended use, predictors and leakage, baseline regression model, sample size for development and external validation, validation design, discrimination, calibration, clinical utility, reporting frameworks. Use for "prediction model", "machine learning model", "model validation", "EPV", "calibration". Not for the accuracy of a single diagnostic test (use sample-size-power). (Türkçe - tahmin modeli, makine öğrenmesi, model validasyonu.)
---

# Prediction Model / ML Module

An optional module on top of the core pipeline. Run it after `study-design-feasibility` and **before** `sample-size-power` finishes: for prediction models the sample-size logic lives here.

> Methodology note: guideline names, versions and numerical criteria change over time and were not re-verified when this skill was written. See `references/guidelines-and-sample-size.md` for pointers, and verify the current version with a literature search before citing anything in a protocol or paper.

## Input

`research/<slug>/01_hypothesis.md`, `02_design_feasibility.md`.

## Steps

1. **Intended use.** Who uses the prediction, at what time point, to make which decision? Which cut-offs or actions follow? Without this, performance metrics cannot be judged.
2. **Predictors and leakage check.** For each candidate predictor: is it available *at the prediction time point*? Is it a proxy for the outcome or recorded because of the outcome (for example a test ordered after the event)? Remove or justify. Define the outcome precisely, including its time window, and who determines it.
3. **Baseline first.** Always include a regularized or standard regression model as the reference. A flexible ML algorithm is justified only if it beats the baseline in discrimination, calibration, and clinical utility on held-out data. Choose 1–2 ML algorithms at most, with a reason for each.
4. **Sample size.**
   - For development, do not rely on a rule of thumb alone (such as events-per-variable). Use a formal approach based on the number of candidate predictor parameters, outcome prevalence, expected model performance and a target for overfitting (shrinkage). Published criteria and software exist (the `pmsampsize` package in R/Stata is one implementation; verify the reference). Flexible ML algorithms usually need substantially more events than regression for stable results.
   - For external validation, dedicated sample-size criteria exist; check the current ones and state the number of events and non-events needed.
   - Compute in code and save the script as `research/<slug>/02a_sample_size_calc.R` (or `.py`).
   - Which performance measure drives the sample-size calculation is the "primary" metric for the study; name it in the plan (for example calibration slope, or precision of the C-statistic).
5. **Validation design.** Report **both** when feasible: internal validation of the development step using resampling with optimism correction (bootstrap or repeated cross-validation) on the *whole* development sample, **and** external validation in another site or a later period (temporal). External validation is stronger evidence, but it does not replace reporting the optimism-corrected development performance. A single random train/test split wastes data and gives a noisy estimate in modest samples; if used, say why. Keep every data-driven step (feature selection, tuning, imputation) inside the validation loop to avoid optimistic bias.
6. **Performance measures to pre-specify:**
   - Discrimination (AUC / C-statistic with confidence interval)
   - **Calibration**: calibration plot, calibration-in-the-large and slope; summary measures such as Brier score. Calibration is often the weak point and must not be skipped.
   - **Clinical utility**: decision curve analysis / net benefit over plausible threshold probabilities.
   - Performance in clinically relevant subgroups (age, sex, site, period) to look for unfairness.
7. **Imbalance and thresholds.** Be cautious with resampling to fix class imbalance: it distorts calibrated probabilities. Choose thresholds from the intended use, not from the best point on the ROC curve.
8. **Reporting and appraisal.** Plan to report with the current TRIPOD-family statement for prediction models (including the AI/ML extension) and anticipate appraisal with a risk-of-bias tool for prediction studies. Confirm current versions.
9. **Model use and updating.** State how the model would be implemented, monitored and updated; do not claim clinical readiness from a single-centre retrospective study.

## Output

`research/<slug>/02a_prediction_model_plan.md`:

- Intended use and prediction time point
- Predictor list with availability/leakage assessment
- Outcome definition
- Baseline model and candidate ML algorithms (with reasons)
- Sample-size approach, inputs, result, and script name (then summarize it in `03_sample_size.md`)
- Validation design (internal and external/temporal)
- Pre-specified performance measures and subgroup checks
- Reporting guideline and appraisal tool, with versions verified or flagged as unverified

## Quality checks

- Never present discrimination alone as evidence the model works.
- Never skip the regression baseline.
- State openly that a single-centre, retrospective study limits generalizability.
- Carry the validation and performance plan into `05_sap.md`.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
