"""Shared phase map and staleness check for the plugin hooks (stdlib only).

Imported by post_write.py and session_start_status.py. The hooks run with
`python -I`, which keeps the script's own folder off sys.path, so they add this
folder to sys.path explicitly before importing.

Staleness is advisory and based on file modification times: a phase file is
"possibly out of date" when one of the files it was built from was modified
after it. File times can be changed by copying or cloud sync, so the wording
that reaches the user is always "may be out of date", never "is".
"""
import os

# Required phases. 00 (gap check) and the 02a/04a/06a module files are optional.
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

# file -> files it is built from. A file missing on disk is simply skipped.
INPUTS = {
    "01_hypothesis.md": ["00_gap_analysis.md"],
    "02_design_feasibility.md": ["01_hypothesis.md"],
    "02a_prediction_model_plan.md": ["01_hypothesis.md", "02_design_feasibility.md"],
    "03_sample_size.md": ["01_hypothesis.md", "02_design_feasibility.md", "02a_prediction_model_plan.md"],
    "04_data_dictionary.md": ["01_hypothesis.md", "02_design_feasibility.md", "02a_prediction_model_plan.md"],
    "04a_llm_extraction_protocol.md": ["02_design_feasibility.md", "04_data_dictionary.md"],
    "05_sap.md": [
        "01_hypothesis.md", "02_design_feasibility.md", "02a_prediction_model_plan.md",
        "03_sample_size.md", "04_data_dictionary.md", "04a_llm_extraction_protocol.md",
    ],
    "06_ethics_application.md": [
        "01_hypothesis.md", "02_design_feasibility.md", "03_sample_size.md",
        "04_data_dictionary.md", "04a_llm_extraction_protocol.md", "05_sap.md",
        "06a_committee_requirements.md",
    ],
    "07_manuscript_plan.md": [
        "01_hypothesis.md", "02_design_feasibility.md", "03_sample_size.md", "05_sap.md",
    ],
}

# An input must be newer than the dependent file by more than this many seconds.
# Two files written one after the other in the same working session are not stale.
TOLERANCE_SECONDS = 2


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def stale_files(study_dir):
    """Return {file name: [names of inputs that are newer than it]}.

    Only files that exist are considered, both as dependents and as inputs.
    """
    result = {}
    for name, inputs in INPUTS.items():
        own = _mtime(os.path.join(study_dir, name))
        if own is None:
            continue
        newer = []
        for inp in inputs:
            t = _mtime(os.path.join(study_dir, inp))
            if t is not None and t - own > TOLERANCE_SECONDS:
                newer.append(inp)
        if newer:
            result[name] = newer
    return result
