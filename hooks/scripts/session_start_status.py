#!/usr/bin/env python3
"""SessionStart hook: eger cwd icinde research/<slug>/ projeleri varsa,
hangi fazda olunduguna dair kisa bir hatirlatma yazdirir (yumusak, engellemeyen)."""
import json
import os
import sys

PHASES = [
    ("00_gap_analysis.md", "Literatur bosluk taramasi"),
    ("01_hypothesis.md", "Hipotez/arastirma sorusu"),
    ("02_design_feasibility.md", "Tasarim ve fizibilite"),
    ("03_sample_size.md", "Orneklem/guc hesabi"),
    ("04_data_dictionary.md", "Veri sozlugu/CRF"),
    ("05_sap.md", "Istatistiksel analiz plani"),
    ("06_ethics_application.md", "Etik kurul basvurusu"),
    ("07_manuscript_plan.md", "Makale/dergi plani"),
]


def main():
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
        current = missing[0] if missing else "tum fazlar tamam"
        lines.append(f"- {slug}: {len(done)}/{len(PHASES)} faz tamam. Siradaki: {current}")

    if lines:
        print("[clinical-research-copilot] Devam eden arastirma projeleri:")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
