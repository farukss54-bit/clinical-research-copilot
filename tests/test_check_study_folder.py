"""Offline tests for tests/check_study_folder.py on synthetic study folders."""
import importlib.util
import os
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_study_folder", os.path.join(HERE, "check_study_folder.py"))
csf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csf)

GOOD_HYP = ("# 01\n\nRefutation criterion: a difference below 5 points would reject the hypothesis.\n"
            "Not investigated: long-term outcomes.\n")


def write(d, name, text="x\n", mtime=None):
    path = os.path.join(d, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    if mtime is not None:
        os.utime(path, (mtime, mtime))
    return path


def msgs(findings, sev=None):
    return [(f[1], f[2]) for f in findings if sev is None or f[0] == sev]


class Checker(unittest.TestCase):
    def test_empty_folder_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(csf.check(d)[0][0], "ERROR")

    def test_clean_folder_has_no_findings(self):
        with tempfile.TemporaryDirectory() as d:
            t = time.time() - 1000
            write(d, "01_hypothesis.md", GOOD_HYP, t)
            write(d, "02_design_feasibility.md", "# 02\n", t + 10)
            write(d, "decisions.md", "# log\n", t + 20)
            self.assertEqual(csf.check(d), [])

    def test_missing_decisions_log_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", GOOD_HYP)
            write(d, "02_design_feasibility.md")
            self.assertIn(("decisions.md", "missing: decisions and skipped steps have no log"),
                          msgs(csf.check(d), "ERROR"))

    def test_review_without_advisor_response(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", GOOD_HYP)
            write(d, "decisions.md")
            write(d, "reviews/methodology-critic.md", "# Review\n\nM1 High ...\n")
            write(d, "reviews/biostatistics-reviewer.md", "# Review\n\n## Advisor response\n\n| M1 | accepted |\n")
            errs = msgs(csf.check(d), "ERROR")
            self.assertEqual(len(errs), 1)
            self.assertEqual(errs[0][0], "reviews/methodology-critic.md")

    def test_history_narrative_and_placeholder_are_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", GOOD_HYP)
            write(d, "decisions.md")
            write(d, "03_sample_size.md", "# 03\n\n## Update 2026-11-08: Phase 2 leaves\n\n**Correction after biostatistics review.** TBD\n")
            w = [m for _, m in msgs(csf.check(d), "WARN")]
            self.assertTrue(any("change history" in m and "Update 2026-11-08" in m for m in w))
            self.assertTrue(any("Correction after" in m for m in w))
            self.assertTrue(any("placeholder 'TBD'" in m for m in w))

    def test_open_recompute_markers_are_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", GOOD_HYP)
            write(d, "decisions.md")
            write(d, "06_ethics_application.md", "Güç değerleri yeniden hesaplanacak.\nPower: to be recomputed for N = 60.\n")
            w = [m for n, m in msgs(csf.check(d), "WARN") if n == "06_ethics_application.md"]
            self.assertEqual(w, ["2 open 'to be recomputed' marker(s): resolve before submission"])

    def test_hypothesis_without_refutation_or_scope(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", "# 01\n\nH1: A beats B.\n")
            write(d, "decisions.md")
            w = [m for _, m in msgs(csf.check(d), "WARN")]
            self.assertTrue(any("refutation" in m for m in w))
            self.assertTrue(any("scope boundary" in m for m in w))

    def test_stale_file_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            t = time.time() - 1000
            write(d, "01_hypothesis.md", GOOD_HYP, t + 100)
            write(d, "02_design_feasibility.md", "# 02\n", t)
            write(d, "decisions.md", "# log\n", t + 200)
            w = [(n, m) for n, m in msgs(csf.check(d), "WARN")]
            self.assertIn(("02_design_feasibility.md", "may be out of date: older than 01_hypothesis.md"), w)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "01_hypothesis.md", "# 01\n")
            write(d, "02_design_feasibility.md")
            import contextlib
            import io
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(csf.main([d]), 1)  # missing decisions.md is an error


if __name__ == "__main__":
    unittest.main()
