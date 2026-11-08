#!/usr/bin/env python3
"""SessionStart hook: if the working directory contains research/<slug>/ projects,
print a short reminder of which phase each one is in, and which phase files may be
out of date because a file they were built from changed later (advisory, never blocks)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_state import OPTIONAL, PHASES, stale_files  # noqa: E402


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
        # Silent when nothing is stale: a quiet session start is the correct output.
        for fname, newer in sorted(stale_files(study_dir).items()):
            lines.append(f"    may be out of date: {fname} (older than {', '.join(newer)})")

    if lines:
        print("[clinical-research-copilot] Research projects in progress:")
        print("\n".join(lines))
        if any(line.startswith("    may be out of date") for line in lines):
            print(
                "Check each flagged file against the newer file(s) and update it, or add a line "
                "'Checked against <file> on <date>: no change needed' (saving it clears the flag). "
                "Record the decision in research/<slug>/decisions.md."
            )


if __name__ == "__main__":
    main()
