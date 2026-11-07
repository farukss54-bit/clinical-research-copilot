---
name: journal-manuscript
description: >-
  Picks target journals or conferences based on the study, its findings and the author's goals (first publication, impact, indexing, career requirements), screens for predatory venues, and builds an IMRaD manuscript or abstract skeleton aligned to the reporting guideline. Use when the user says "where should we submit", "choose a journal", "draft the abstract", "manuscript outline". (Türkçe: dergi seçimi, makale taslağı.)
---

# Journal / Conference Selection and Manuscript Skeleton

## Purpose

Connect a finished (or nearly finished) study to a suitable venue and to a draft structure that fits that venue's expectations.

## Input

As many `research/<slug>/*.md` files as exist (at least hypothesis, design and SAP; also `02a`, `04a` and `06` when present; results if available). Reviewer reports (for example from `methodology-critic`) are used if the user saved them under `research/<slug>/reviews/`.

## Steps

1. **Profile the goal**: what matters most to the author — a first publication or conference presentation, high impact, a specific indexing database, an academic-promotion requirement? Ask what *counts* for them (for example required indexes or quartiles). This decides whether to aim ambitiously or realistically.
2. **Suggest 3–5 candidate venues** that match the topic and scope (original research / short report / proof of concept). For each: scope fit, rough acceptance difficulty, open-access policy and article processing charge (APC) if known, and indexing. **Do not quote an impact factor, quartile or APC from memory**: verify it with a search and cite the source, or say "check the current figure".
3. **Predatory-venue screen** for every suggestion: is it indexed in the databases the author needs, listed in a directory of open-access journals when it claims to be open access, with transparent peer review and editorial board? Warn about unsolicited-invitation journals.
4. **Reporting guideline**: use the checklist chosen in the SAP (STROBE, STARD, a TRIPOD-family statement for prediction models). It is usually a required submission attachment.
5. **IMRaD skeleton**, section by section:
   - Introduction: the gap and the research question.
   - Methods: design, variables, SAP summary, at the detail level the reporting guideline demands.
   - Results: if findings exist, a skeleton of the tables and figures; if not, placeholders and a list of what will be needed (Table 1 patient characteristics, Table 2 main results or model performance, Figure 1 flow diagram, calibration plot…).
   - Discussion: position relative to the literature, limitations (carry over `methodology-critic` findings from `research/<slug>/reviews/` if saved), clinical meaning.
6. If useful, also produce a **short abstract or poster skeleton**; a conference abstract is often the fastest first output.

## Output

`research/<slug>/07_manuscript_plan.md`:

- Author goal profile and venue candidates with rationale and verification notes
- Reporting guideline to follow
- IMRaD skeleton (what is ready vs not)
- Table/figure list
- Optional abstract/poster skeleton

## Quality checks

- No unverified or outdated impact-factor figures.
- If results do not exist, do not invent them; give structure only.
- Output language: manuscripts and abstracts in English unless the target venue requires otherwise.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Never put identifiable patient data into this session or into any search.
