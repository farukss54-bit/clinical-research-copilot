# Changelog

## 0.5.0

Changes found by running the plugin end to end on a mock three-arm simulation protocol.

- Decision log: each study gets an append-only `research/<slug>/decisions.md` (decisions, skipped steps, overrides). Phase files now show the current state only; every skill's conventions say so. `research-advisor` updates every affected phase file after a decision and records files checked with "no change needed".
- Stale-file check: new `hooks/scripts/phase_state.py` holds the phase map and a dependency map. The `PostToolUse` hook lists downstream files that are older than the file just written; `SessionStart` lists files older than their inputs and stays silent when there are none. Advisory, based on modification times.
- Phase 0 is now an explicit question: `research-advisor` and `quick-gap-check` ask the user to choose between `lr-ai`, the light check or skipping, and run no search before the answer. Previously the light check could start without asking.
- Intake: the advisor asks first whether the material is one study or several (for example a trial and a later real-world audit) and offers to split them; one question per message, multiple choice, plain clinical language.
- `hypothesis-formulation` adds a refutation criterion and a "not investigated" line; `study-design-feasibility` adds a scope check; both and the advisor add a short self-review before saving.
- Reviewer protocol: `methodology-critic`, `biostatistics-reviewer` and `ethics-drafter` (review mode) label findings with IDs and severity and return the complete report; the advisor saves it verbatim to `reviews/` and adds an "Advisor response" table (accepted / rejected / verify first / needs the user's decision).
- New skill `pubmed-bridge`: lr-ai has no PubMed source and cannot be switched to one by configuration (its source list is fixed in code), so this skill searches PubMed through NCBI E-utilities with a stdlib script (`skills/pubmed-bridge/scripts/pubmed_search.py`), compares the result with the lr-ai run, and adds the new DOIs with `lr.py add`. lr-ai is not modified. The script prints only counts, so the search costs almost no model tokens. First tests in `tests/` (offline unit tests); also checked live against PubMed and a throwaway lr-ai run. A native PubMed adapter for lr-ai (pull request upstream) remains an option.
- `tests/check_study_folder.py`: a deterministic check (no model tokens) of a `research/<slug>/` folder against these conventions: `decisions.md` present, reviewer reports carry an "Advisor response", no change-history headings in phase files, no stale files, refutation criterion and "not investigated" line in `01`, no placeholders. `python tests/check_study_folder.py research/<slug>`; offline tests in `tests/test_check_study_folder.py`.
- Found by a behaviour probe (a decision given to the advisor on a copy of the test study): the decision was logged and six phase files were updated without adding change narratives, but the files were edited out of order (03, 01, 02, 05, 07, 04, 06), so the stale-file check flagged correct updates, and a "Checked against" line added to a file made later files look stale. The advisor now updates and checks affected files in one pass in ascending phase order, and the hook message says so.
- `tests/run_behavior_probes.py`: headless behaviour probes (`p3` phase 0 is asked and nothing is searched, `p4` a two-study protocol triggers a split question, `p2` a decision is logged and propagated in phase order, `p6` a reviewer report is saved verbatim with an Advisor response and the phase files stay untouched). They call the model and are budget-capped; the checks are on tool use and files, and the assistant's text is printed for reading.
- The folder checker also warns about open "to be recomputed" markers (a headless probe left such markers in an ethics paragraph because it could not run a script); they are harmless in a draft but must be resolved before submission.
- Fixes from a skill review and a plugin validation (plugin-dev agents):
  - `quick-gap-check`: three options instead of five (the question tool allows at most four), the unavailable "clinical-evidence skill" option removed, the question is skipped only when a quick check was explicitly requested, one question at a time, concepts only, a result cap, the search date and "advisor proposal; the user decides" on candidate questions.
  - `study-design-feasibility`: one question at a time, scope check first and reuse of a logged scope decision, propose-then-confirm for design choices, a wider design list, a separate feasibility branch for prospective, interventional, educational and simulation studies, confounders labelled "proposed" unless sourced, and only counts and aggregate impressions (never records) in the pilot chart review.
  - `hypothesis-formulation`: reads `decisions.md`, scope check first, propose-then-confirm for the primary outcome and the form of the hypothesis, an estimation aim for descriptive questions, a refutation criterion worded around abandoning H1 in measurable form, an "Open items" section and a complete self-review.
  - `pubmed-bridge`: reports how many records were fetched against how many matched (top-N per query), keeps how PubMed read each query and its warnings, flags zero-hit queries, a `sample` command for a fair look at the records, drops retracted papers by default, reports how many papers lr-ai added, one-line quoted commands that work in PowerShell and bash, `00_gap_analysis.md` updated in place and followed by the advisor's propagation rule. A live check showed that `"Retraction of Publication"[pt]` is not a PubMed type, so it is not used.
  - README: the privacy note now says what `pubmed-bridge` sends to NCBI; a Tests section. Hooks run with `python -I -B` so they leave no `__pycache__`. Turkish trigger phrases (also without diacritics) in four skill descriptions.
- Not done, deliberately: a "locked" status for approved sections (decide after the decision log has been used for a while).

## 0.4.0

- Stage 1: `prediction-model-design/references/guidelines-and-sample-size.md` now holds PubMed-verified citations for TRIPOD+AI, PROBAST+AI, the Riley et al. development and external-validation sample-size criteria, and Collins 2016 / Snell 2021. Still unverified after all stages: the `pmsampsize` software citation and ML-specific sample-size simulations (STROBE, RECORD, STARD-AI and TRIPOD-LLM were verified in stage 2).
- Stage 2: added PubMed-verified citations for TRIPOD-LLM, STARD 2015, STARD-AI (with its Author Correction, content not checked), STROBE and RECORD; `sap-builder` and `llm-extraction-validation` now name them. Open: TRIPOD-AI supersession and any post-2015 RECORD update.
- Stage 3: `ethics-application/references/turkey-kvkk.md` rewritten against official texts (Law 6698 consolidated text with the 2024 amendments, Board Decision 2018/10, the 2019 Personal Health Data Regulation, the 2017 anonymization regulation, the 2024 cross-border transfer regulation). Corrections: the 2016 health-data regulation is repealed; Article 6(3) has no research-specific ground; research routes are Articles 28(1)(b) and (c) via Article 16 of the 2019 regulation. Still unverified: the national basis for non-interventional ethics committees, consent-waiver practice, administrative-permission and form-language requirements.
- Ethics module: `ethics-application` and `ethics-drafter` now ask for the committee's own form/directive and, if given, extract its requirements into optional `06a_committee_requirements.md` and draft to that structure (committee mode); otherwise they use the generic format and say so. Documents are treated as requirements data, not instructions. `research-advisor`, `session_start_status.py` and `post_write.py` know the new file.
- Restored the executable bit on `hooks/run.sh` and `hooks/scripts/session_start_status.py` (lost when the archive was extracted on Windows).
- `biostatistics-reviewer`: Bash instructions now say POSIX syntax only, inline code, interpreter fallbacks, and to label figures as hand calculations when a calculation cannot run.
- Pre-release review fixes: broke the circular dependency between `data-dictionary-crf` and `llm-extraction-validation` (draft dictionary first, mark variables "pending 04a", finalize after 04a); `ethics-drafter` now reads all phase files, has a review mode that never overwrites `06_ethics_application.md`, includes the LLM paragraph, and resolves `turkey-kvkk.md` without a plugin-relative path; `sap-builder` validation rule limited to prediction/ML models; removed stale "unverified" wording in `prediction-model-design`; README lists `06a` and the correct agent roles; `.gitignore` excludes `research/`; hook docstring translated.
- Known, planned for 0.4.1: source-discipline rule for `methodology-critic` and `biostatistics-reviewer`; attrition step in `sample-size-power`; unsourced venue claims in `journal-manuscript`; pointer for the optional `lr-ai` dependency; `research-advisor` tree wording for `03`/`02a` and `reviews/`; minor trigger and wording items.

## 0.3.1

- Added project icon (`assets/icon.png`), author/homepage/repository metadata and the license holder.

## 0.3.0

- All skills, agents and documentation rewritten in English; Turkish remains available through the user's language and a Turkey-specific ethics reference.
- Removed `literature-gap-scan`. Phase 0 is now optional: `quick-gap-check` is a lightweight fallback and recommends the `lr-ai` plugin for real literature reviews.
- New optional modules: `prediction-model-design` (prediction/ML studies) and `llm-extraction-validation` (LLM-assisted extraction from free text).
- `ethics-application` split into a country-independent core and `references/turkey-kvkk.md`.
- Removed project-specific examples and assumptions from skills and agents.
- Hooks and agents updated for the new phase files (`02a_*`, `04a_*`).
- Skill descriptions use YAML folded blocks (strict-parser safe); every skill states the slug and missing-input conventions; prediction studies still write `03_sample_size.md`; added `prediction-model-design/references/` with unverified guideline pointers; LLM module forbids opening real notes in the assistant session.
- Known limitation: methodology references (reporting guideline versions, sample-size criteria) are given as pointers to verify; verified references are planned for 0.4.

## 0.2.0

- Fixed manifests, added LICENSE, rebuilt PostToolUse hooks (JSON `additionalContext`), portable hook launcher, UTF-8 handling, corrected agent tool lists.

## 0.1.0

- Initial skeleton.
