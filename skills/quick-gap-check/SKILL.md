---
name: quick-gap-check
description: >-
  Optional lightweight Phase 0: a quick originality and gap check for a clinical research idea before hypothesis formulation. Asks the user to choose between a full review with the lr-ai plugin, this light check, or skipping. Not for systematic or scoping reviews. Use for "has this been studied", "novelty check", "find a research gap". (Türkçe: hızlı literatür kontrolü, özgünlük, araştırma boşluğu, daha önce çalışılmış mı, literatürde var mı, özgün mü, ozgunluk, arastirma boslugu.)
---

# Quick Gap Check (optional Phase 0)

## Purpose

Give the user a fast, honest answer to "has this been done, and where is the room?" before they invest in a hypothesis and design. This phase is **optional**: the pipeline can start at `01_hypothesis.md`.

This is deliberately not a systematic review. If the user needs a defensible literature base (grant, thesis, registration, systematic or scoping review), recommend a dedicated tool instead.

## Input

`research/<slug>/decisions.md` if it exists (a phase-0 choice or scope decision may already be recorded there; do not ask again what is already decided), plus whatever the user told you about the idea.

## Step 1 — Ask which route the user wants (do not just mention it, and do not search yet)

Skip this step only if `research-advisor` already asked and the user chose the light check, or the user **explicitly** asked for a quick or light check. A request such as "has this been studied?" does not by itself mean "quick": ask.

Ask one multiple-choice question (plain clinical language, one line per option, recommended option first). Three options, at most four:

1. **A full literature review with the lr-ai plugin** (`lr-ai:lit-review`): seed search, database search, snowballing, screening and categorization. Recommend it first when the work is a thesis, a grant, a registration or a review. Its sources are OpenAlex, Semantic Scholar and arXiv, not PubMed: after it runs, offer the `pubmed-bridge` skill of this plugin to add a MeSH-aware PubMed search to the same run. Offer this option only if the plugin is installed.
2. **The light check below**: fast, not systematic. Recommend it first for a personal check of an idea. It uses the literature connectors that are connected (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv) and falls back to WebSearch.
3. **Skip phase 0 for now.** Record the reason under "Skipped or overridden" in `research/<slug>/decisions.md`.

Wait for the answer before running any search. If the user picks lr-ai, hand over to it; when `research-advisor` is running the session, write the result (or a short summary with the run folder) to `research/<slug>/00_gap_analysis.md`, otherwise tell the user to save it there. Then stop; do not duplicate its work.

## Step 2 — Light check (only after the user chose it, or when nothing else is available)

1. Ask for what is still missing, **one thing at a time** and only what you do not already know from the intake, `01_hypothesis.md` or `decisions.md`: the topic, the population or setting, the type of study in mind. Ask for concepts only; if the user volunteers an identifiable detail, rewrite it as a generic term before using it anywhere.
2. Search at least two sources (for example PubMed plus a second source via a connector or WebSearch). Start broad, then narrow; overly restrictive AND-chains return nothing. Keep the search budget small: a handful of queries, and read titles and abstracts, not full texts. Never search with identifiable patient data.
3. Map what you find along four axes: population/health-system coverage, method (classical statistics vs ML, internal vs external validation), consistency of results, outcome and time window.
4. Propose 2–3 candidate research questions. For each: which axis is empty, how well it fits the user's own advantages (local population, data access, case volume), and the originality risk. These are proposals; the user decides.

## Output

Write `research/<slug>/00_gap_analysis.md` containing:

- Date of the search, queries run and sources used (for transparency), and how many records were looked at per query
- Key studies found (at most about ten: title, year, population, method, finding, link)
- Gap map along the four axes
- Candidate questions with rationale, labelled "advisor proposal; the user decides"
- A one-line caveat: this was a light check, not a systematic search

## Quality rules

- Every statement about the literature must trace to a retrieved source; no "the literature shows" from memory.
- Never claim "nobody has studied this". Say "I could not find X in this search; indexing or terminology may differ".
- If two sources disagree, say so.

## Conventions

- `<slug>` is the study's short folder name. If none exists, ask the user for one (or derive a short kebab-case name from the topic) and create `research/<slug>/`.
- If an input file listed above is missing, say so, continue with what the user tells you, and mark the gap as "not specified" in the output. Do not invent data, numbers or sources.
- Reply in the user's language; write the document in English unless the user asks otherwise.
- Show the current state only. Change history ("updated after review", "second round") does not belong in this file; record decisions in `research/<slug>/decisions.md` (create it if missing) and note which later phase files the change affects.
- Never put identifiable patient data into this session or into any search.
