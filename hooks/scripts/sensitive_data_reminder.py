#!/usr/bin/env python3
"""PostToolUse hook: hasta/saglik verisi icerebilecek dosya adlariyla eslesen
Write/Edit islemlerinde KVKK/anonimlik hatirlatmasi yazdirir. Engelleyici degildir."""
import json
import re
import sys

PATTERN = re.compile(r"(hasta|patient|hbys|ehr|vaka)[^/\\]*\.(csv|xlsx|xls|json|tsv)$", re.IGNORECASE)


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""

    if PATTERN.search(file_path):
        print(
            "[clinical-research-copilot] KVKK hatirlatmasi: bu dosya hasta/saglik verisi "
            "icerebilir. Dogrudan tanimlayici (ad-soyad, TC no, telefon) icermedigini, "
            "kimliksizlestirildigini ve kurum disi/bulut servislerine yuklenmediginden emin ol."
        )


if __name__ == "__main__":
    main()
