#!/usr/bin/env python3
"""Behaviour probes: run research-advisor headlessly in a temp folder and check what it did.

THIS CALLS THE MODEL AND COSTS MONEY (a few tenths of a dollar per probe; each run is capped
with --max-budget-usd). The deterministic tests (python -m unittest discover -s tests) are free.

Usage:
  python tests/run_behavior_probes.py p3            # phase 0 is asked, nothing searched
  python tests/run_behavior_probes.py p4            # a two-study protocol triggers a split question
  python tests/run_behavior_probes.py p2 --fixture research/<slug>
                                                   # a decision is logged and propagated in phase order
  python tests/run_behavior_probes.py p6 --fixture research/<slug>
                                                   # a reviewer report is saved verbatim with an Advisor response
  options: --model sonnet --budget 0.6 --keep (keep the temp folder)

Checks are on tool use and files (deterministic). The assistant's text is printed for you to read,
because wording is not asserted. Needs the `claude` CLI on PATH.
"""
import argparse
import json
import os
import re
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
    "p6": "02_design_feasibility.md hazır. Tasarımı methodology-critic ile eleştirel biçimde incelet ve raporu "
          "çalışmaya kaydet. Çalışma dosyalarını (00-07) değiştirme.",
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
    calls, texts, cost, results = [], [], None, {}
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
                    calls.append((b.get("name", ""), b.get("input", {}), b.get("id")))
                elif b.get("type") == "text" and b.get("text", "").strip():
                    texts.append(b["text"].strip())
        elif ev.get("type") == "user":
            content = ev.get("message", {}).get("content", [])
            for b in content if isinstance(content, list) else []:
                if b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    results[b.get("tool_use_id")] = c or ""
        elif ev.get("type") == "result":
            cost = ev.get("total_cost_usd")
            if ev.get("result"):
                texts.append(ev["result"].strip())
    return calls, texts, cost, results


def _norm(s):
    return " ".join(str(s).split())


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
    if a.probe in ("p2", "p6") and not a.fixture:
        sys.exit(f"{a.probe} needs --fixture research/<slug>")
    budget = a.budget or (1.5 if a.probe in ("p2", "p6") else 0.6)

    work = tempfile.mkdtemp(prefix="probe-")
    study = None
    if a.probe in ("p2", "p6"):
        study = os.path.join(work, "research", os.path.basename(os.path.normpath(a.fixture)))
        skip = ["lit-review-*", "*.py", "__pycache__"] + (["reviews"] if a.probe == "p6" else [])
        shutil.copytree(a.fixture, study, ignore=shutil.ignore_patterns(*skip))
        before = {n: os.path.getmtime(os.path.join(study, n)) for n in os.listdir(study) if n.endswith(".md")}
    t0 = time.time()
    calls, texts, cost, results = run_claude(PROMPTS[a.probe], work, a.model, budget, edits=a.probe in ("p2", "p6"))
    names = [c[0] for c in calls]
    print(f"probe {a.probe}: {len(calls)} tool calls, cost ${cost}, {time.time() - t0:.0f}s, folder {work}")
    ok = True
    if a.probe in ("p3", "p4"):
        bad = [n for n in names if n in SEARCH_LIKE or n.startswith("mcp__")]
        ok &= verdict(not bad, "no search, skill or agent call before the user answered", ", ".join(bad))
        wrote = [n for n in names if n in ("Write", "Edit")]
        if a.probe == "p4":
            ok &= verdict(not wrote, "no phase file written before the scope question is answered", ", ".join(wrote))
    elif a.probe == "p6":
        import check_study_folder as csf  # noqa: E402
        agent_calls = [c for c in calls if c[0] in ("Agent", "Task") and "methodology-critic" in json.dumps(c[1])]
        ok &= verdict(bool(agent_calls), "the methodology-critic agent was called")
        report = os.path.join(study, "reviews", "methodology-critic.md")
        have = os.path.isfile(report)
        ok &= verdict(have, "reviews/methodology-critic.md was written")
        text = open(report, encoding="utf-8").read() if have else ""
        ok &= verdict(bool(re.search(r"(?im)^#{1,3}\s*advisor response", text)), "report has an 'Advisor response' section")
        ids = set(re.findall(r"\bM\d{1,2}\b", text))
        ok &= verdict(len(ids) >= 3, "findings carry IDs (M1, M2, ...)", f"{len(ids)} found")
        ok &= verdict(bool(re.search(r"\b(Critical|High|Medium|Low)\b", text)), "findings carry a severity")
        if agent_calls and agent_calls[0][2] in results and len(_norm(results[agent_calls[0][2]])) > 400:
            res = _norm(results[agent_calls[0][2]])
            mid = res[len(res) // 2: len(res) // 2 + 150]
            ok &= verdict(mid in _norm(text), "the reviewer's report was saved verbatim (middle slice found in the file)")
        else:
            print("  info  verbatim check skipped (no usable reviewer result captured)")
        untouched = [n for n in before if n[:2].isdigit() and os.path.getmtime(os.path.join(study, n)) > before[n] + 1]
        ok &= verdict(not untouched, "phase files 00-07 were not modified", ", ".join(untouched))
        own = [f for f in csf.check(study) if f[1] == "reviews/methodology-critic.md"]
        ok &= verdict(not own, "no checker finding for the report file", "; ".join(f[2] for f in own))
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
