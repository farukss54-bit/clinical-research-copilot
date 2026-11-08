---
name: quick-gap-check
description: >-
  Optional lightweight Phase 0: a quick originality and gap check for a clinical research idea before hypothesis formulation. Recommends heavier tools when available (lr-ai plugin, clinical-evidence skill). Not for systematic or scoping reviews. Use for "has this been studied", "novelty check", "find a research gap". (Türkçe - hızlı literatür kontrolü, özgünlük, araştırma boşluğu.)
---

# Quick Gap Check (optional Phase 0)

## Purpose

Give the user a fast, honest answer to "has this been done, and where is the room?" before they invest in a hypothesis and design. This phase is **optional**: the pipeline can start at `01_hypothesis.md`.

This is deliberately not a systematic review. If the user needs a defensible literature base (grant, thesis, systematic/scoping review), recommend a dedicated tool instead.

## Step 1 — Ask which route the user wants (do not just mention it, and do not search yet)

If `research-advisor` already asked and the user chose the light check, or the user invoked this skill directly for a quick check, skip to Step 2. Otherwise check which of these are available in this session and **ask the user to choose** (a multiple-choice question, recommended option first, one line per option, plain clinical language):

- The **lr-ai** plugin (`lr-ai:lit-review`): full seed search, database search, snowballing, screening and categorization. Best for a real literature review (thesis, grant, registration). Its sources are OpenAlex, Semantic Scholar and arXiv, not PubMed: after it runs, offer the `pubmed-bridge` skill of this plugin to add a MeSH-aware PubMed search to the same run.
- A **clinical-evidence** style skill, if installed: retrieves referenced answers to focused clinical questions.
- Literature connectors (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv), if connected.
- The **light check** below: fast, not systematic.
- **Skip phase 0** for now (note the reason in `decisions.md`).

Wait for the answer before running any search. If the user picks a dedicated tool, hand over to it and ask them to save the result (or a short summary) as `research/<slug>/00_gap_analysis.md`. Then stop; do not duplicate its work.

## Step 2 — Light check (only after the user chose it, or when nothing else is available)

1. Ask for the topic, population/setting, and the type of study they have in mind (one short question, not a questionnaire).
2. Search at least two sources (for example PubMed plus a second source via a connector or WebSearch). Start broad, then narrow; overly restrictive AND-chains return nothing. Never search with identifiable patient data.
3. Map what you find along four axes: population/health-system coverage, method (classical statistics vs ML, internal vs external validation), consistency of results, outcome and time window.
4. Propose 2–3 candidate research questions. For each: which axis is empty, how well it fits the user's own advantages (local population, data access, case volume), and the originality risk.

## Output

Write `research/<slug>/00_gap_analysis.md` containing:

- Queries run and sources used (for transparency)
- Key studies found (title, year, population, method, finding, link)
- Gap map along the four axes
- Ranked candidate questions with rationale
- A one-line caveat: this was a light check, not a systematic search

## Quality rules

- Every statement about the literature must trace to a retrieved source; no "the literature shows" from memory.
- Never claim "nobody has studied this". Say "I could not find X in this search; indexing or terminology may differ".
- If two sources disagree, say so.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
