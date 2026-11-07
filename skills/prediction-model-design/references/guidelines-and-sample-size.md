# Guideline and sample-size pointers (UNVERIFIED)

These are candidate names written from general knowledge, **not checked against current sources** when this file was written. Search for the current version of each before citing it in a protocol or paper. Do not quote numerical thresholds from here.

## Reporting guidelines

- Observational studies: STROBE; RECORD (extension for routinely collected health data).
- Diagnostic accuracy: STARD (an AI-specific extension may exist).
- Prediction models: the TRIPOD family. A combined TRIPOD+AI statement (2024) is believed to supersede the earlier TRIPOD and TRIPOD-AI.
- Studies that use a large language model: a TRIPOD-style extension for LLMs (2025) is believed to exist.
- Risk-of-bias appraisal for prediction models: PROBAST, with an AI-oriented update believed to exist.

## Sample size for prediction models

- Development: criteria by Riley and colleagues based on number of candidate predictor parameters, prevalence and expected performance, implemented in the `pmsampsize` package (R/Stata). Events-per-variable alone is a legacy rule of thumb.
- External validation: dedicated criteria by Riley and colleagues, and earlier simulation-based recommendations on the minimum number of events and non-events (Collins and colleagues). Check the current recommendations.
- Flexible ML algorithms generally need more events than regression for stable estimates; search for recent simulation studies.

## How to verify

Use a literature connector (PubMed, Consensus, Elicit) or the EQUATOR Network site for the current reporting guideline and its year, and record the citation in the protocol.
