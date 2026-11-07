# Guideline and sample-size references

Last verified: 2026-11-07, against PubMed records (title, authors, journal, year, DOI). Items marked **unverified** were not checked and must be looked up before they are cited in a protocol or paper. Numeric values below were read from the cited abstracts; do not apply them to a new study without recomputing for that study's own inputs.

## Reporting guidelines

Verified:
- **TRIPOD+AI** (prediction models, regression or machine learning). Collins GS, Moons KGM, Dhiman P, et al. *BMJ* 2024;385:e078378. [doi:10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378) (PMID 38626948). 27-item checklist plus a TRIPOD+AI for Abstracts checklist. The article states it supersedes the TRIPOD 2015 checklist, which should no longer be used.

**Unverified** (not yet checked; stage 2 of v0.4):
- Observational studies: STROBE; RECORD (routinely collected health data).
- Diagnostic accuracy: STARD, and whether an AI-specific extension (STARD-AI) exists.
- Studies using a large language model: TRIPOD-LLM (2025).
- Whether TRIPOD+AI also supersedes the earlier TRIPOD-AI: the TRIPOD+AI abstract does not say so; check the full text.

## Risk-of-bias and applicability appraisal

Verified:
- **PROBAST+AI**. Moons KGM, Damen JAA, Kaul T, et al. *BMJ* 2025;388:e082505. [doi:10.1136/bmj-2024-082505](https://doi.org/10.1136/bmj-2024-082505) (PMID 40127903). Two parts: model development (16 signalling questions, quality and applicability) and model evaluation (18 signalling questions, risk of bias and applicability); four domains in each (participants and data sources, predictors, outcome, analysis). The article says it may replace the original PROBAST.

## Sample size for prediction-model development

All verified; each is *Stat Med* unless stated.
- Continuous outcomes (Part I). Riley RD, Snell KIE, Ensor J, et al. 2019;38(7):1262-1275. [doi:10.1002/sim.7993](https://doi.org/10.1002/sim.7993) (PMID 30347470). Four criteria, including a global shrinkage factor of at least 0.9 and an absolute difference of at most 0.05 between apparent and adjusted R².
- Binary and time-to-event outcomes (Part II). Riley RD, Snell KIE, Ensor J, et al. 2019;38(7):1276-1296. [doi:10.1002/sim.7992](https://doi.org/10.1002/sim.7992) (PMID 30357870). Three criteria: shrinkage factor of at least 0.9, difference of at most 0.05 in apparent vs adjusted Nagelkerke R², precise estimate of overall risk. The authors state that rules of thumb such as 10 events per predictor parameter should be avoided. A published erratum exists (2019;38(30):5672, [doi:10.1002/sim.8409](https://doi.org/10.1002/sim.8409), PMID 31793031): cite the corrected version.
- Obtaining the anticipated Cox-Snell R² from a reported C statistic. Riley RD, Van Calster B, Collins GS. 2021;40(4):859-864. [doi:10.1002/sim.8806](https://doi.org/10.1002/sim.8806) (PMID 33283904).
- Multinomial outcomes. Pate A, Riley RD, Collins GS, et al. 2023;32(3):555-571 (*Stat Methods Med Res*). [doi:10.1177/09622802231151220](https://doi.org/10.1177/09622802231151220) (PMID 36660777). Its abstract states the criteria are to be embedded in the `pmsampsize` R library and Stata modules, which is the only `pmsampsize` evidence checked here; the software's own citation and current version are **unverified**.
- Practical summary. Riley RD, Ensor J, Snell KIE, et al. *BMJ* 2020;368:m441. [doi:10.1136/bmj.m441](https://doi.org/10.1136/bmj.m441) (PMID 32188600). Abstract not available in PubMed; content not checked beyond title and authorship.

## Sample size for external validation

All verified.
- Binary outcome. Riley RD, Debray TPA, Collins GS, et al. *Stat Med* 2021;40(19):4230-4251. [doi:10.1002/sim.9025](https://doi.org/10.1002/sim.9025) (PMID 34031906). Closed-form and iterative solutions targeting precision of calibration (observed/expected, calibration slope), C-statistic and net benefit.
- Time-to-event outcome. Riley RD, Collins GS, Ensor J, et al. *Stat Med* 2022;41(7):1280-1295. [doi:10.1002/sim.9275](https://doi.org/10.1002/sim.9275) (PMID 34915593). Simulation-based framework.
- Tutorial. Riley RD, Snell KIE, Archer L, et al. Evaluation of clinical prediction models (part 3). *BMJ* 2024;384:e074821. [doi:10.1136/bmj-2023-074821](https://doi.org/10.1136/bmj-2023-074821) (PMID 38253388). Recommends tailoring calculations to the model and setting rather than using rules of thumb.
- Older rule of thumb, for context only. Collins GS, Ogundimu EO, Altman DG. *Stat Med* 2016;35(2):214-226. [doi:10.1002/sim.6787](https://doi.org/10.1002/sim.6787) (PMID 26553135). Its abstract suggests at least 100 events and ideally 200 or more.
- Why the rule of thumb is not enough. Snell KIE, Archer L, Ensor J, et al. *J Clin Epidemiol* 2021;135:79-89. [doi:10.1016/j.jclinepi.2021.02.011](https://doi.org/10.1016/j.jclinepi.2021.02.011) (PMID 33596458). Reports that 100 or even 200 events and non-events can give imprecise estimates, especially for calibration, and proposes a simulation-based calculation. This is the simulation-based paper; the 100/200-event guidance is Collins 2016.

## Not covered by a verified reference

- Flexible ML algorithms needing more events than regression: no dedicated simulation study has been checked. The only support here is descriptive: a systematic review of ML prognostic models in oncology (Dhiman P, et al. *BMC Med Res Methodol* 2022;22:101, [doi:10.1186/s12874-022-01577-x](https://doi.org/10.1186/s12874-022-01577-x), PMID 35395724) reported a median of 3.4 events per predictor for non-regression ML models versus 8 for regression, and that sample size was justified in 5 of 62 studies. That describes practice, not a requirement; treat the claim as **unverified** until a simulation study is found.

## How to verify other items

Use a literature connector (PubMed, Consensus, Elicit) or the EQUATOR Network site for the current reporting guideline and its year, and record the citation in the protocol.
