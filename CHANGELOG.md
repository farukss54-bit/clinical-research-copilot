# Changelog

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
