#!/usr/bin/env python3
"""SessionStart hook: if the working directory contains research/<slug>/ projects,
print a short reminder of which phase each one is in (advisory, never blocks)."""
import json
import os
import sys

# Required phases. 00 (gap check) and the 02a/04a module files are optional and not counted.
PHASES = [
    ("01_hypothesis.md", "hypothesis / research question"),
    ("02_design_feasibility.md", "design and feasibility"),
    ("03_sample_size.md", "sample size / power"),
    ("04_data_dictionary.md", "data dictionary / CRF"),
    ("05_sap.md", "statistical analysis plan"),
    ("06_ethics_application.md", "ethics application"),
    ("07_manuscript_plan.md", "manuscript / venue plan"),
]
OPTIONAL = [
    ("00_gap_analysis.md", "gap check"),
    ("02a_prediction_model_plan.md", "prediction-model plan"),
    ("04a_llm_extraction_protocol.md", "LLM extraction protocol"),
    ("06a_committee_requirements.md", "committee requirements"),
]


def main():
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    cwd = payload.get("cwd") or os.getcwd()
    research_dir = os.path.join(cwd, "research")
    if not os.path.isdir(research_dir):
        return

    lines = []
    for slug in sorted(os.listdir(research_dir)):
        study_dir = os.path.join(research_dir, slug)
        if not os.path.isdir(study_dir):
            continue
        done = [label for fname, label in PHASES if os.path.exists(os.path.join(study_dir, fname))]
        missing = [label for fname, label in PHASES if not os.path.exists(os.path.join(study_dir, fname))]
        extras = [label for fname, label in OPTIONAL if os.path.exists(os.path.join(study_dir, fname))]
        current = missing[0] if missing else "all phases have a file"
        extra_txt = f" (optional present: {', '.join(extras)})" if extras else ""
        lines.append(f"- {slug}: {len(done)}/{len(PHASES)} phases done. Next: {current}{extra_txt}")

    if lines:
        print("[clinical-research-copilot] Research projects in progress:")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
