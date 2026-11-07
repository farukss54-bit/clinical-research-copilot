# Changelog

## 0.4.0 (in progress)

- Stage 1: `prediction-model-design/references/guidelines-and-sample-size.md` now holds PubMed-verified citations for TRIPOD+AI, PROBAST+AI, the Riley et al. development and external-validation sample-size criteria, and Collins 2016 / Snell 2021. Items not yet checked (STROBE/RECORD, STARD-AI, TRIPOD-LLM, the `pmsampsize` software citation, ML-specific sample-size simulations) stay marked unverified.
- Stage 2: added PubMed-verified citations for TRIPOD-LLM, STARD 2015, STARD-AI (with its Author Correction, content not checked), STROBE and RECORD; `sap-builder` and `llm-extraction-validation` now name them. Open: TRIPOD-AI supersession and any post-2015 RECORD update.
- Restored the executable bit on `hooks/run.sh` and `hooks/scripts/session_start_status.py` (lost when the archive was extracted on Windows).
- Pending: stage 2 (TRIPOD-LLM, STARD-AI, RECORD) and stage 3 (KVKK items).

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
