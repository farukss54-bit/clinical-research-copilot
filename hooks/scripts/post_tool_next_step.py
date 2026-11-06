#!/usr/bin/env python3
"""PostToolUse hook: research/<slug>/NN_*.md dosyalarindan biri yazildiginda/
duzenlendiginde, pipeline'daki bir sonraki mantikli adimi nazikce hatirlatir.
Engelleyici degildir, sadece bilgilendirir."""
import json
import os
import sys

NEXT_STEP = {
    "00_gap_analysis.md": "Siradaki adim: hypothesis-formulation skill ile PICO/hipotezi netlestir.",
    "01_hypothesis.md": "Siradaki adim: study-design-feasibility skill ile tasarim ve fizibiliteyi denetle.",
    "02_design_feasibility.md": (
        "Siradaki adim: sample-size-power skill ile orneklem/guc hesabi yap. "
        "Istersen methodology-critic alt-agent'iyla tasarimi simdi de sinatabilirsin."
    ),
    "03_sample_size.md": (
        "Siradaki adim: data-dictionary-crf skill ile veri sozlugu/CRF olustur. "
        "(biostatistics-reviewer ile bu hesabi dogrulatmayi dusun.)"
    ),
    "04_data_dictionary.md": "Siradaki adim: sap-builder skill ile istatistiksel analiz planini yaz.",
    "05_sap.md": (
        "Siradaki adim: ethics-application skill ile etik kurul basvuru taslagini hazirla. "
        "(biostatistics-reviewer ile SAP'i gozden gecirmeyi dusun.)"
    ),
    "06_ethics_application.md": "Siradaki adim: journal-manuscript skill ile dergi/kongre secimi ve makale iskeletini olustur.",
    "07_manuscript_plan.md": "Bu calismanin tum fazlari tamamlandi.",
}


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    fname = os.path.basename(file_path)

    if fname in NEXT_STEP and "research" in file_path.replace("\\", "/").split("/"):
        print(f"[clinical-research-copilot] {fname} guncellendi. {NEXT_STEP[fname]}")


if __name__ == "__main__":
    main()
