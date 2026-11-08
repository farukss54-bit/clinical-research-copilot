#!/usr/bin/env python3
"""Deterministic checks for a study folder (research/<slug>/), standard library only, no model tokens.

Usage:  python tests/check_study_folder.py research/<slug> [--strict]

It checks that the conventions of this plugin were followed:
  - decisions.md exists once the study has phase files
  - reviewer reports in reviews/ carry an "Advisor response" section
  - phase files show the current state, not a change history ("update", "second round", ...)
  - phase files are not older than the files they were built from (same rule as the hooks)
  - 01_hypothesis.md has a refutation criterion and a "not investigated" line
  - no leftover placeholders

Exit code: 1 if there is any ERROR (or any finding with --strict), otherwise 0.
Findings are advisory heuristics; a human decides.
"""
import os
import re
import sys

HOOKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks", "scripts")
sys.path.insert(0, HOOKS)
from phase_state import INPUTS, PHASES, stale_files  # noqa: E402

PHASE_FILES = [name for name, _ in PHASES] + [
    "00_gap_analysis.md", "02a_prediction_model_plan.md", "04a_llm_extraction_protocol.md", "06a_committee_requirements.md",
]

# Headings or lead-ins that narrate history instead of stating the current state.
HISTORY = re.compile(
    r"(?i)(\bupdate[ds]?\b[^\n]{0,40}\d{4}-\d{2}-\d{2}"
    r"|\bsecond round\b"
    r"|\bcorrection after\b"
    r"|\bafter the [`\w-]+ review\b"
    r"|\bauthor decisions? of\b"
    r"|\badditions after\b)"
)
PLACEHOLDER = re.compile(r"\b(TBD|TODO|FIXME)\b|to be clarified")
REFUTATION = re.compile(r"(?i)refut|falsif|would make (you|us|the \w+) (reject|abandon|give up)")
SCOPE = re.compile(r"(?i)not investigated|out of scope|scope boundar|does not investigate")


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _heading_or_lead_lines(text):
    """Yield (line number, line) for headings and for lines that start a bold lead-in."""
    for i, line in enumerate(text.splitlines(), 1):
        s = line.lstrip()
        if s.startswith("#") or s.startswith("**") or s.startswith("> **") or s.startswith("- **"):
            yield i, line.strip()


def check(study_dir):
    """Return a list of (severity, file, message) with severity 'ERROR' or 'WARN'."""
    out = []
    present = [n for n in PHASE_FILES if os.path.isfile(os.path.join(study_dir, n))]
    if not present:
        return [("ERROR", ".", "no phase files found; is this a research/<slug> folder?")]

    if len(present) >= 2 and not os.path.isfile(os.path.join(study_dir, "decisions.md")):
        out.append(("ERROR", "decisions.md", "missing: decisions and skipped steps have no log"))

    reviews = os.path.join(study_dir, "reviews")
    if os.path.isdir(reviews):
        for name in sorted(os.listdir(reviews)):
            if name.endswith(".md"):
                text = _read(os.path.join(reviews, name))
                if not re.search(r"(?im)^#{1,3}\s*advisor response", text):
                    out.append(("ERROR", f"reviews/{name}", "no 'Advisor response' section (dispositions not recorded)"))

    for name in present:
        text = _read(os.path.join(study_dir, name))
        for i, line in _heading_or_lead_lines(text):
            if HISTORY.search(line):
                out.append(("WARN", name, f"line {i}: change history in a phase file: {line[:90]}"))
        for m in PLACEHOLDER.finditer(text):
            out.append(("WARN", name, f"placeholder '{m.group(0)}'"))
            break

    hyp = _read(os.path.join(study_dir, "01_hypothesis.md"))
    if hyp:
        if not REFUTATION.search(hyp):
            out.append(("WARN", "01_hypothesis.md", "no refutation criterion (what result would reject the hypothesis)"))
        if not SCOPE.search(hyp):
            out.append(("WARN", "01_hypothesis.md", "no 'not investigated' / scope boundary line"))

    for name, newer in sorted(stale_files(study_dir).items()):
        out.append(("WARN", name, "may be out of date: older than " + ", ".join(newer)))
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    strict = "--strict" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if len(paths) != 1:
        raise SystemExit(__doc__)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    findings = check(paths[0])
    for sev, name, msg in findings:
        print(f"{sev:5} {name}: {msg}")
    errors = sum(1 for f in findings if f[0] == "ERROR")
    print(f"\n{errors} error(s), {len(findings) - errors} warning(s).")
    return 1 if errors or (strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
