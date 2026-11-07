---
name: sample-size-power
description: >-
  Sample size and power for classical hypothesis tests (two-group comparisons, proportions, survival, correlation/regression, non-inferiority, diagnostic accuracy of a single test), including what to report when N is fixed by retrospective data. For prediction/ML models it hands off to prediction-model-design. Use for "how many patients do I need", "minimum number of patients", "powered", "power analysis", "sample size". (Türkçe - örneklem büyüklüğü, güç analizi.)
---

# Sample Size and Power

## Purpose

Answer "how many patients do I need?" with a method that matches the study type and is defensible, then compare the target with the case volume actually available.

## Input

`research/<slug>/02_design_feasibility.md` (design, primary outcome, annual case volume estimate) and `01_hypothesis.md`.

## Steps

1. **Choose the method by study type.**
   - Classical comparison (difference in means or proportions, odds/risk/hazard ratio): standard power calculation. State the expected effect size (with source: literature or pilot), alpha (usually 0.05), power (0.80–0.90), one- or two-sided, allocation ratio.
   - Diagnostic accuracy: target precision (confidence-interval width) for sensitivity and specificity, adjusted for prevalence.
   - Correlation, regression coefficients, non-inferiority/equivalence margins, matched or clustered designs (for example repeat visits by the same patient: account for the design effect), and precision-based sizing for purely descriptive studies each have their own formulas; state which one is used and why.
   - **Prediction model development or validation, or any ML model**: do **not** use a classical power calculation or a rule of thumb alone. Run `prediction-model-design` (it computes the sample size in `02a_prediction_model_plan.md`). Then still write `03_sample_size.md`: summarize the 02a result and apply steps 3–6 below using *events* rather than patients, so later phases find the file they expect.
   - **Effect sizes and prevalences**: use only values the user supplied or that were retrieved with a citation. If neither exists, write a labelled placeholder ("effect size unverified, needs a source") instead of supplying a number from memory.
2. **Show the calculation step by step** (inputs → formula or logic → result) so the user, or a biostatistician, can check it. **Run the numbers in code** (Python with `statsmodels`/`scipy`, or R) rather than computing by hand, and save the script next to the output (`research/<slug>/03_sample_size_calc.py` or `.R`). If code cannot be run, say that the figures are unverified.
3. **If N is fixed** by the available retrospective data (the usual case), do not compute post hoc observed power. Report the precision achievable (confidence-interval width) or the minimum detectable effect at the available N.
   **Inflate for attrition**: expected missing data, exclusions, and loss to follow-up (state the percentage and why).
4. **Compare with availability**: annual case volume × retrospective window. Say how long (or how many years) the target takes to reach. If the user's centre has high volume for this condition, note that as a clear feasibility advantage; if the target is out of reach, say so directly and discuss options (longer window, multicentre, a different design, a more modest objective).
5. List **assumptions and uncertainties** explicitly (for example "effect size taken from study X, may differ in your population").
6. Recommend a biostatistician review of the result.

## Output

`research/<slug>/03_sample_size.md`:

- Method chosen and why
- Step-by-step calculation (inputs → logic → result) and the script file name
- Final target sample after attrition adjustment
- Comparison with available case volume / time to accrue
- Assumptions and uncertainties
- Reviewer recommendation or result (if `biostatistics-reviewer` was run)

## Quality checks

- Never output a sample size without a stated basis. "That should be enough" is not a basis.
- Do not mix classical-test logic with prediction-model logic. Use the rules of whichever applies.
- If a prediction or ML model is involved, state that calibration and external/temporal validation planning continues in the SAP phase.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
