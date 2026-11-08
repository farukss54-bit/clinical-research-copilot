#!/usr/bin/env python3
"""Behaviour probes: run research-advisor headlessly in a temp folder and check what it did.

THIS CALLS THE MODEL AND COSTS MONEY (a few tenths of a dollar per probe; each run is capped
with --max-budget-usd). The deterministic tests (python -m unittest discover -s tests) are free.

Usage:
  python tests/run_behavior_probes.py p3            # phase 0 is asked, nothing searched
  python tests/run_behavior_probes.py p4            # a two-study protocol triggers a split question
  python tests/run_behavior_probes.py p2 --fixture research/<slug>
                                                   # a decision is logged and propagated in phase order
  options: --model sonnet --budget 0.6 --keep (keep the temp folder)

Checks are on tool use and files (deterministic). The assistant's text is printed for you to read,
because wording is not asserted. Needs the `claude` CLI on PATH.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "hooks", "scripts"))
AGENT = "clinical-research-copilot:research-advisor"

PROMPTS = {
    "p3": "Tek bir çalışma planlıyorum, kapsam net: acil tıp asistanlarında HINTS eğitiminin simülasyonda "
          "hekim performansına etkisi. Başlayalım.",
    "p4": "Elimde bir protokol var: Faz 1'de asistanlara simülasyonda üç farklı eğitim yöntemi uygulayıp randomize "
          "karşılaştıracağım. Faz 2'de bir yıl sonra kazanan yöntemi tüm asistanlara uygulayıp gerçek hasta "
          "dosyalarında BT istem oranını önce-sonra tarayacağım. Bunu baştan sona tasarlayalım.",
    "p2": "Karar verdim: merkezdeki uygun ve istekli asistan sayısı 75 değil, 60. Başka hiçbir şey değişmedi. "
          "Bunu çalışmaya işle.",
}
SEARCH_LIKE = ("WebSearch", "WebFetch", "Skill", "Agent")


def run_claude(prompt, cwd, model, budget, edits):
    cmd = [shutil.which("claude") or "claude", "-p", prompt, "--plugin-dir", ROOT, "--agent", AGENT,
           "--model", model, "--max-budget-usd", str(budget), "--no-session-persistence",
           "--output-format", "stream-json", "--verbose"]
    if edits:
        cmd += ["--permission-mode", "acceptEdits"]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, timeout=900)
    calls, texts, cost = [], [], None
    for line in proc.stdout.splitlines():
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    calls.append((b.get("name", ""), b.get("input", {})))
                elif b.get("type") == "text" and b.get("text", "").strip():
                    texts.append(b["text"].strip())
        elif ev.get("type") == "result":
            cost = ev.get("total_cost_usd")
            if ev.get("result"):
                texts.append(ev["result"].strip())
    return calls, texts, cost


def verdict(ok, label, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{(': ' + detail) if detail else ''}")
    return ok


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("probe", choices=sorted(PROMPTS))
    ap.add_argument("--fixture", help="p2: a research/<slug> study folder to copy")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--budget", type=float, default=None)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    if a.probe == "p2" and not a.fixture:
        sys.exit("p2 needs --fixture research/<slug>")
    budget = a.budget or (1.5 if a.probe == "p2" else 0.6)

    work = tempfile.mkdtemp(prefix="probe-")
    study = None
    if a.probe == "p2":
        study = os.path.join(work, "research", os.path.basename(os.path.normpath(a.fixture)))
        shutil.copytree(a.fixture, study, ignore=shutil.ignore_patterns("lit-review-*", "*.py", "__pycache__"))
        before = {n: os.path.getmtime(os.path.join(study, n)) for n in os.listdir(study) if n.endswith(".md")}
    t0 = time.time()
    calls, texts, cost = run_claude(PROMPTS[a.probe], work, a.model, budget, edits=a.probe == "p2")
    names = [c[0] for c in calls]
    print(f"probe {a.probe}: {len(calls)} tool calls, cost ${cost}, {time.time() - t0:.0f}s, folder {work}")
    ok = True
    if a.probe in ("p3", "p4"):
        bad = [n for n in names if n in SEARCH_LIKE or n.startswith("mcp__")]
        ok &= verdict(not bad, "no search, skill or agent call before the user answered", ", ".join(bad))
        wrote = [n for n in names if n in ("Write", "Edit")]
        if a.probe == "p4":
            ok &= verdict(not wrote, "no phase file written before the scope question is answered", ", ".join(wrote))
    else:
        from phase_state import PHASES  # noqa: E402
        ok &= verdict(os.path.isfile(os.path.join(study, "decisions.md")), "decisions.md exists")
        changed = sorted((os.path.getmtime(os.path.join(study, n)), n) for n in before
                         if os.path.getmtime(os.path.join(study, n)) > before[n] + 1 and n[:2].isdigit())
        order = [n for _, n in changed]
        ok &= verdict(order == sorted(order), "affected files were edited in ascending phase order", " > ".join(o[:2] for o in order))
        import check_study_folder as csf  # noqa: E402
        stale = [f for f in csf.check(study) if "may be out of date" in f[2]]
        ok &= verdict(not stale, "no stale-file warning after the update", "; ".join(f"{f[1]}" for f in stale))
        new_hist = [f for f in csf.check(study) if "change history" in f[2]]
        print(f"  info  change-history lines still in phase files: {len(new_hist)} (fixture may contain old ones)")
    print("\nassistant text (read it; wording is not asserted):")
    print("\n\n".join(texts[-2:])[:2500])
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
