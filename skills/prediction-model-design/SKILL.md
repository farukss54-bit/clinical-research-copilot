---
name: prediction-model-design
description: >-
  ML/prediction-model module. Plans development or validation of a clinical prediction or machine-learning model: intended use, predictors and leakage, baseline regression model, sample size for development and external validation, validation design, discrimination, calibration, clinical utility, reporting frameworks. Use for "prediction model", "machine learning model", "model validation", "EPV", "calibration". Not for the accuracy of a single diagnostic test (use sample-size-power). (Türkçe - tahmin modeli, makine öğrenmesi, model validasyonu.)
---

# Prediction Model / ML Module

An optional module on top of the core pipeline. Run it after `study-design-feasibility` and **before** `sample-size-power` finishes: for prediction models the sample-size logic lives here.

> Methodology note: `references/guidelines-and-sample-size.md` holds citations verified against PubMed on the date it states, and marks what is still unverified. Guidelines and numerical criteria change over time, so check that file's date and confirm the current version before citing anything in a protocol or paper.

## Input

`research/<slug>/01_hypothesis.md`, `02_design_feasibility.md`.

## Steps

1. **Intended use.** Who uses the prediction, at what time point, to make which decision? Which cut-offs or actions follow? Without this, performance metrics cannot be judged.
2. **Predictors and leakage check.** For each candidate predictor: is it available *at the prediction time point*? Is it a proxy for the outcome or recorded because of the outcome (for example a test ordered after the event)? Remove or justify. Define the outcome precisely, including its time window, and who determines it.
3. **Baseline first.** Always include a regularized or standard regression model as the reference. A flexible ML algorithm is justified only if it beats the baseline in discrimination, calibration, and clinical utility on held-out data. Choose 1–2 ML algorithms at most, with a reason for each.
4. **Sample size.**
   - For development, do not rely on a rule of thumb alone (such as events-per-variable). Use a formal approach based on the number of candidate predictor parameters, outcome prevalence, expected model performance and a target for overfitting (shrinkage). Published criteria (Riley and colleagues) and software exist; the `pmsampsize` package in R/Stata implements them. Verified citations are in `references/guidelines-and-sample-size.md`; the `pmsampsize` software citation itself is still unverified. Flexible ML algorithms usually need more events than regression for stable results, but no simulation study has been verified for this yet.
   - For external validation, use the dedicated criteria listed in `references/guidelines-and-sample-size.md` (binary and time-to-event outcomes), which target precision of calibration, discrimination and net benefit rather than a fixed event count. State the number of events and non-events needed.
   - Compute in code and save the script as `research/<slug>/02a_sample_size_calc.R` (or `.py`).
   - Which performance measure drives the sample-size calculation is the "primary" metric for the study; name it in the plan (for example calibration slope, or precision of the C-statistic).
5. **Validation design.** Report **both** when feasible: internal validation of the development step using resampling with optimism correction (bootstrap or repeated cross-validation) on the *whole* development sample, **and** external validation in another site or a later period (temporal). External validation is stronger evidence, but it does not replace reporting the optimism-corrected development performance. A single random train/test split wastes data and gives a noisy estimate in modest samples; if used, say why. Keep every data-driven step (feature selection, tuning, imputation) inside the validation loop to avoid optimistic bias.
6. **Performance measures to pre-specify:**
   - Discrimination (AUC / C-statistic with confidence interval)
   - **Calibration**: calibration plot, calibration-in-the-large and slope; summary measures such as Brier score. Calibration is often the weak point and must not be skipped.
   - **Clinical utility**: decision curve analysis / net benefit over plausible threshold probabilities.
   - Performance in clinically relevant subgroups (age, sex, site, period) to look for unfairness.
7. **Imbalance and thresholds.** Be cautious with resampling to fix class imbalance: it distorts calibrated probabilities. Choose thresholds from the intended use, not from the best point on the ROC curve.
8. **Reporting and appraisal.** Plan to report with TRIPOD+AI (BMJ 2024), which supersedes the TRIPOD 2015 checklist, and anticipate appraisal with PROBAST+AI (BMJ 2025). Citations are in `references/guidelines-and-sample-size.md`. If the model uses a large language model, also consider TRIPOD-LLM (citation and caveat in the reference file; check which modules apply).
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
