---
name: ethics-application
description: >-
  Drafts an ethics committee / IRB application for non-interventional or retrospective clinical research from the design, sample-size and data-dictionary files, with a data-protection section. Country-independent core; Turkey-specific guidance (KVKK, committee naming) is in references/turkey-kvkk.md. Use when the user says "ethics application", "IRB", "consent waiver", "KVKK", "etik kurul başvurusu". Always a draft.
---

# Ethics Committee / IRB Application (draft)

## Purpose

Turn the design and data documents into an application draft the institution's ethics committee can review. The output is **always a draft** and must be checked against the institution's own form and the applicable law.

## Input

`research/<slug>/02_design_feasibility.md`, `03_sample_size.md`, `04_data_dictionary.md`, `05_sap.md`; also `01_hypothesis.md`, `00_gap_analysis.md`, `02a_prediction_model_plan.md`, `04a_llm_extraction_protocol.md` if they exist.

## Steps

1. Check which input files exist. If something is missing, say so and mark the corresponding section "not specified"; do not invent facts or numbers.
2. Ask (briefly) which country/institution this is for. If the institution has its own form, follow its headings. For **Turkey**, also read `references/turkey-kvkk.md` in this skill's folder. For other jurisdictions, use the general headings below and tell the user which local laws to check (for example GDPR in the EU/UK, HIPAA in the US).
3. Draft these sections:
   - Purpose and background (from the gap analysis, if available)
   - Research question / hypothesis
   - Design (retrospective vs prospective, single vs multicentre)
   - Inclusion and exclusion criteria
   - Data sources and variables (from the data dictionary)
   - Sample size and its justification
   - Data collection, storage, retention, de-identification or pseudonymization plan, who has access
   - **Data protection**: what categories of personal data (health data is a special category in most laws), legal basis, whether informed consent is required or a **waiver of consent** is requested and on what grounds (typically: retrospective, minimal risk, impracticable to obtain consent, appropriate safeguards — but this is the committee's decision)
   - Risks and mitigations (retrospective observational studies are usually minimal risk, which the committee decides)
   - Expected scientific / clinical benefit
   - Conflicts of interest and funding
4. If free text will be processed by an LLM, add a separate paragraph: where the model runs, whether text leaves the institution, de-identification applied, and the validation plan (from `04a_llm_extraction_protocol.md`).
5. Put this note at the very top of the draft: *"This is a draft. It must be reviewed against your institution's current ethics application format and applicable law, and confirmed with the ethics committee secretariat or institutional data-protection officer before submission."*
6. Language: write the draft in the language the institution's form requires (ask if unsure); keep it in English only if the form is in English.
7. For a deeper data-protection pass, `ethics-drafter` can review the draft as a second reader.

## Output

`research/<slug>/06_ethics_application.md` using the sections above.

## Quality checks

- Do not claim legal certainty ("fully compliant", "will be approved"). Use "typically", "depends on the institution's assessment".
- Do not put identifiable patient data into the document.
- Do not send or submit anything on the user's behalf; produce documents only.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
