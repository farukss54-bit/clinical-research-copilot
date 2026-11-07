#!/usr/bin/env python3
"""PostToolUse hook for Write|Edit.

1. If research/<slug>/NN_*.md was written, remind the user of the next pipeline step.
2. If the written file looks like patient-level data, remind about KVKK / de-identification.

Advisory only: never blocks. PostToolUse stdout is NOT shown to the model unless it is
JSON with hookSpecificOutput.additionalContext, so that is what this prints.
"""
import json
import os
import re
import sys

NEXT_STEP = {
    "00_gap_analysis.md": "Next: run hypothesis-formulation to turn the best gap into a PICO question.",
    "01_hypothesis.md": "Next: run study-design-feasibility to check design and data feasibility.",
    "02_design_feasibility.md": (
        "Next: run sample-size-power. You can also have methodology-critic stress-test the design now."
    ),
    "03_sample_size.md": (
        "Next: run data-dictionary-crf. Consider having biostatistics-reviewer verify the calculation."
    ),
    "04_data_dictionary.md": "Next: run sap-builder to write the statistical analysis plan.",
    "05_sap.md": (
        "Next: run ethics-application. Consider having biostatistics-reviewer review the SAP first."
    ),
    "06_ethics_application.md": "Next: run journal-manuscript for venue choice and manuscript outline.",
    "07_manuscript_plan.md": "All pipeline phases have a file for this study.",
}

# Path tokens (split on non-alphanumerics) that suggest patient-level data.
SENSITIVE_TOKENS = {
    "hasta", "hastalar", "patient", "patients", "hbys", "ehr", "emr", "vaka", "vakalar",
}
DATA_EXT = {".csv", ".xlsx", ".xls", ".json", ".tsv", ".parquet", ".sav", ".dta"}


def _tokens(path):
    return {t for t in re.split(r"[^0-9a-zA-ZÀ-ɏ]+", path.lower()) if t}


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
    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    norm = file_path.replace("\\", "/")
    fname = norm.rsplit("/", 1)[-1]

    messages = []
    if fname in NEXT_STEP and "research" in norm.split("/"):
        messages.append(f"[clinical-research-copilot] {fname} updated. {NEXT_STEP[fname]}")

    ext = os.path.splitext(fname)[1].lower()
    if ext in DATA_EXT and (_tokens(norm) & SENSITIVE_TOKENS):
        messages.append(
            "[clinical-research-copilot] Privacy reminder: this file may contain patient-level "
            "health data. Make sure it has no direct identifiers (name, national ID, phone), is "
            "de-identified, and is not sent to services outside your institution's approval."
        )

    if messages:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "\n".join(messages),
            }
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
