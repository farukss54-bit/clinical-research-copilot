---
name: llm-extraction-validation
description: >-
  LLM module. Designs and validates LLM-assisted (automatic) extraction of study variables from free-text clinical notes: schema, privacy and hosting, gold-standard annotation, development vs held-out sets, agreement metrics with confidence intervals, error analysis, reproducibility. Use when an LLM, GPT or language model will extract or abstract variables from notes. Manual-only abstraction is handled in data-dictionary-crf. (Türkçe - LLM ile veri çıkarımı.)
---

# LLM-Assisted Extraction: Protocol and Validation

An optional module. Run it during the data-dictionary phase whenever a variable will be taken from free-text notes with an LLM.

> Methodology note: TRIPOD-LLM (Gallifant et al., Nat Med 2025) is the reporting guideline for studies using large language models; the citation and a caveat are in `../prediction-model-design/references/guidelines-and-sample-size.md`. Its abstract does not say whether it covers extraction-validation studies, so read the modules and apply those that fit. It is a living document: check for updates before submission.

## Input

`research/<slug>/02_design_feasibility.md` (which variables are free text) and `04_data_dictionary.md` (a draft is enough; the dictionary is finalized after this module has produced `04a_llm_extraction_protocol.md`).

## Steps

1. **Privacy first.** Do patient notes leave the institution when the model is called? Decide *before* any extraction: (a) a locally hosted model on institution-controlled hardware, or (b) an institution-approved endpoint with a data-processing agreement, or (c) de-identified text only. Do not send identifiable notes to a general consumer service. Record the decision in the ethics application.

   **This assistant session is itself such a service** unless your institution's deployment covers it. Draft and tune prompts on synthetic or invented example notes here. Do not open, paste or read real notes or annotation files in this session unless the hosting decision above explicitly covers this assistant.

   If you rely on de-identification (option c), de-identification of free text leaks (names, dates, national ID numbers, rare diagnoses). Plan a residual-identifier audit on a random sample before treating the text as de-identified.
2. **Extraction schema.** For each variable: allowed values, the "not documented" value, explicit rules for ambiguity ("extract only what is stated; do not infer"), and the note types it may come from.
3. **Gold standard.** Have at least two trained humans independently annotate a random validation sample; adjudicate disagreements; report human-human agreement as the ceiling. Sample size should be large enough for acceptable confidence intervals around each variable's metrics, and large enough to include enough positive cases for rare variables (stratify or oversample if needed).
4. **Separate sets.** Use a **development set** to write and tune prompts, and a **held-out test set** that no prompt change ever sees. Freeze the prompt, model, version, date and decoding settings before touching the test set.
5. **Metrics per variable**, each with a 95% confidence interval: precision, recall, F1, accuracy, and Cohen's kappa (or weighted kappa for ordinal). Percent agreement alone is not enough. Kappa behaves poorly for rare variables (high agreement, low kappa); add positive and negative agreement, or Gwet's AC1 / PABAK, for those. Hosted models are often not deterministic even at temperature 0: repeat the held-out run at least 2–3 times and report run-to-run variability. For numeric values, report exact-match and tolerance-based agreement.
6. **Error analysis.** Categorize errors (hallucinated value, missed mention, negation errors, wrong time point, copy-forward text). Decide whether errors are random or systematic and whether they could correlate with the outcome.
7. **Downstream effect.** Plan a sensitivity analysis: rerun the main analysis on the manually abstracted subset, or propagate extraction error (for example correction for misclassification) to check that conclusions survive.
8. **Reproducibility record.** Store model name and version, hosting, date, temperature/seed, full prompt, schema and post-processing code with the dataset.
9. **Acceptance criteria.** Pre-specify the minimum performance per variable for it to be used; below that, fall back to manual abstraction.

## Output

`research/<slug>/04a_llm_extraction_protocol.md`:

- Privacy/hosting decision
- Schema and rules per variable
- Annotation plan (annotators, sample size, adjudication)
- Dev/test separation and freeze procedure
- Metrics and confidence intervals to be reported; acceptance thresholds
- Error-analysis and sensitivity-analysis plan
- Reproducibility record contents

## Quality checks

- Never rely on LLM extraction without a manually validated held-out sample.
- Report model and prompt details in the methods; they affect reproducibility.
- Carry the validation plan into `05_sap.md` and the extraction description into the ethics application.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
