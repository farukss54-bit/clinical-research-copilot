# clinical-research-copilot

A Claude Code plugin that guides a clinician-researcher through the design of a clinical study: **hypothesis → design and feasibility → sample size → data dictionary → statistical analysis plan → ethics application → venue and manuscript outline.** It adds optional modules for **prediction-model / ML studies** and for **LLM-assisted extraction from free-text notes**, and four reviewer agents.

It does not replace a biostatistician, a data-protection officer, or your ethics committee. Its outputs are drafts.

## What is inside

| Folder | Contents |
|---|---|
| `skills/` core | `hypothesis-formulation`, `study-design-feasibility`, `sample-size-power`, `data-dictionary-crf`, `sap-builder`, `ethics-application`, `journal-manuscript` |
| `skills/` optional | `quick-gap-check` (lightweight phase 0), `prediction-model-design` (ML module), `llm-extraction-validation` (LLM module) |
| `agents/` | `research-advisor` (coordinator) plus reviewers `biostatistics-reviewer`, `methodology-critic`, `ethics-drafter` |
| `hooks/` | Soft reminders: project status at session start, next-step suggestion, patient-data reminder |

## Project convention

Each study lives in `research/<study-slug>/` in your working directory:

```
00_gap_analysis.md              optional   literature / gap check
01_hypothesis.md
02_design_feasibility.md
02a_prediction_model_plan.md    optional   prediction / ML studies
03_sample_size.md
04_data_dictionary.md
04a_llm_extraction_protocol.md  optional   LLM-assisted extraction
05_sap.md
06_ethics_application.md
07_manuscript_plan.md
```

Several studies can run in parallel, each in its own folder. The advisor works out the current phase from which files exist.

### Literature review (phase 0)

Phase 0 is optional. For a real literature review (thesis, grant, systematic or scoping review) use a dedicated tool: the **lr-ai** plugin is recommended, and other literature connectors (PubMed, Consensus, Elicit) work too. Save the result as `00_gap_analysis.md`. If you only need a quick originality check, the lightweight `quick-gap-check` skill does that.

## Install

Try it for one session:

```
claude --plugin-dir /path/to/clinical-research-copilot
```

Persistent install through the bundled marketplace:

```
/plugin marketplace add /path/to/clinical-research-copilot      # or a GitHub repo: <user>/<repo>
/plugin install clinical-research-copilot@clinical-research-copilot-marketplace
```

Check the manifests with `claude plugin validate .`.

### Run the coordinator as the main agent

Subagents cannot spawn other subagents, so `research-advisor` can call the reviewer agents only when it is the session's main agent:

```
claude --agent clinical-research-copilot:research-advisor
```

The skills (for example `/clinical-research-copilot:sample-size-power`) can be used in any normal session.

## Language

Chat in whatever language you like. Research documents (SAP, manuscript plan) are written in English by default; an ethics application follows your institution's required language. Turkey-specific ethics and KVKK guidance is in `skills/ethics-application/references/turkey-kvkk.md`.

## Connectors

Skills use connected literature and data connectors (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv) when present and fall back to WebSearch. Connectors belong to your account and are not bundled with this plugin.

## Hooks

All hooks are soft: they never block an action; they only add information for Claude.

- `SessionStart`: summarizes the phase of each project under `research/`.
- `PostToolUse` (Write/Edit): after a phase file is written, suggests the next step; if the path or file name suggests patient-level data (tokens such as `hasta`, `patient`, `hbys`, `ehr`, `vaka` plus a data extension such as csv/xlsx/json), adds a privacy reminder. It only sees files Claude writes; data created via `Bash` or already on disk is not covered.

Hooks start through `hooks/run.sh`, which uses the first working interpreter among `python3`, `python` and `py -3` (on Windows `python3` is often a Microsoft Store stub, so each candidate is probed). If none works, the hook is skipped silently. On Windows, `sh` requires Git for Windows (Git Bash). There are no dependencies beyond the Python standard library.

## Privacy and limits

- This plugin does not upload anything itself and only produces local markdown documents. **But everything Claude reads and everything you type is sent to the model provider.** Do not have Claude read patient-level data unless your institution has approved it and the data are de-identified. The hooks only remind; they cannot enforce this.
- Ethics and data-protection outputs are **drafts**; confirm them with your institution.
- Sample-size and SAP outputs should be reviewed by a biostatistician. `biostatistics-reviewer` is a first-pass check, not a substitute.
- Names and versions of reporting guidelines and numeric criteria in the ML modules are pointers to verify; check current versions before citing.
- LLM-assisted extraction from notes must always be used with a manually validated sample.

## License

MIT, see `LICENSE`.
