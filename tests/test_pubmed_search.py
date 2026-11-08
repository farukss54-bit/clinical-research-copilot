"""Offline tests for skills/pubmed-bridge/scripts/pubmed_search.py (no network, no tokens).

Run from the repository root:  python -m unittest discover -s tests -v
"""
import importlib.util
import json
import os
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "pubmed-bridge", "scripts", "pubmed_search.py")
spec = importlib.util.spec_from_file_location("pubmed_search", SCRIPT)
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)


class BuildTerm(unittest.TestCase):
    def test_wraps_query_and_limits_language_and_types(self):
        t = ps.build_term('"status epilepticus" AND simulat*')
        self.assertTrue(t.startswith('("status epilepticus" AND simulat*)'))
        self.assertIn("AND English[lang]", t)
        self.assertIn('"Editorial"[pt]', t)
        self.assertIn("NOT (", t)

    def test_any_language_and_keep_all_types(self):
        t = ps.build_term("dizziness", lang="any", keep_all_types=True)
        self.assertEqual(t, "(dizziness)")


class Doi(unittest.TestCase):
    def test_normalisation(self):
        self.assertEqual(ps.norm_doi("10.1007/S00415-026-14058-8"), "10.1007/s00415-026-14058-8")
        self.assertEqual(ps.norm_doi("doi: 10.1002/aet2.10936."), "10.1002/aet2.10936")
        self.assertIsNone(ps.norm_doi(None))
        self.assertIsNone(ps.norm_doi("no doi here"))


class ParseSummary(unittest.TestCase):
    def test_doi_from_articleids(self):
        item = {"title": "  A  title ", "pubdate": "2026 Aug 19", "source": "J Neurol", "pubtype": ["Journal Article"],
                "articleids": [{"idtype": "pubmed", "value": "42618689"},
                               {"idtype": "doi", "value": "10.1007/s00415-026-14058-8"}]}
        r = ps.parse_summary("42618689", item)
        self.assertEqual(r["doi"], "10.1007/s00415-026-14058-8")
        self.assertEqual(r["year"], 2026)
        self.assertEqual(r["title"], "A title")
        self.assertEqual(r["pmid"], "42618689")

    def test_doi_from_elocationid_and_missing(self):
        r = ps.parse_summary("1", {"title": "x", "pubdate": "2020", "elocationid": "doi: 10.1000/abc.def", "articleids": []})
        self.assertEqual(r["doi"], "10.1000/abc.def")
        r2 = ps.parse_summary("2", {"title": "y", "pubdate": "", "articleids": []})
        self.assertIsNone(r2["doi"])
        self.assertIsNone(r2["year"])


class ExistingAndChunks(unittest.TestCase):
    def test_existing_dois_read_from_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "papers.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps({"doi": "10.1000/ABC"}) + "\n\n" + json.dumps({"doi": None}) + "\nnot json\n")
            self.assertEqual(ps.load_existing_dois(p), {"10.1000/abc"})
            self.assertEqual(ps.load_existing_dois(os.path.join(d, "missing.jsonl")), set())

    def test_chunked(self):
        self.assertEqual(list(ps.chunked([1, 2, 3, 4, 5], 2)), [[1, 2], [3, 4], [5]])


class AddDryRun(unittest.TestCase):
    def test_skips_existing_and_no_doi(self):
        with tempfile.TemporaryDirectory() as d:
            run = os.path.join(d, "run")
            os.makedirs(run)
            with open(os.path.join(run, "papers.jsonl"), "w", encoding="utf-8") as f:
                f.write(json.dumps({"doi": "10.1000/have"}) + "\n")
            rec = os.path.join(d, "records.jsonl")
            with open(rec, "w", encoding="utf-8") as f:
                for r in ({"doi": "10.1000/have"}, {"doi": "10.1000/new"}, {"doi": "10.1000/new"}, {"doi": None}):
                    f.write(json.dumps(r) + "\n")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ps.main(["add", "--records", rec, "--run", run, "--lr-script", "unused.py", "--dry-run"])
            self.assertIn("To add: 1 DOIs", buf.getvalue())
            self.assertIn("no DOI, not added: 1", buf.getvalue())


class EsearchSampleAndAdd(unittest.TestCase):
    def test_parse_esearch_keeps_translation_and_warnings(self):
        c, ids, tr, notes = ps.parse_esearch({
            "count": "3412", "idlist": ["1", "2"], "querytranslation": '"status epilepticus"[MeSH Terms]',
            "warninglist": {"phrasesnotfound": ["foo bar"]}})
        self.assertEqual((c, ids), (3412, ["1", "2"]))
        self.assertIn("MeSH", tr)
        self.assertEqual(notes, {"warninglist": {"phrasesnotfound": ["foo bar"]}})
        with self.assertRaises(SystemExit):
            ps.parse_esearch({"ERROR": "Invalid query"})

    def test_pick_sample_is_spread_over_the_whole_list(self):
        self.assertEqual(ps.pick_sample(list(range(100)), 5), [0, 20, 40, 60, 80])
        self.assertEqual(ps.pick_sample([1, 2], 8), [1, 2])
        self.assertEqual(ps.pick_sample([], 3), [])

    def test_retracted_papers_are_excluded_by_default(self):
        self.assertIn('"Retracted Publication"[pt]', ps.build_term("x"))
        self.assertNotIn("Retracted", ps.build_term("x", keep_all_types=True))

    def test_add_sums_lr_output_and_writes_log(self):
        with tempfile.TemporaryDirectory() as d:
            run = os.path.join(d, "run")
            os.makedirs(run)
            stub = os.path.join(d, "stub_lr.py")
            with open(stub, "w", encoding="utf-8") as f:
                f.write('print("Added 2 papers (1 new).")\n')
            rec = os.path.join(d, "records.jsonl")
            with open(rec, "w", encoding="utf-8") as f:
                for doi in ("10.1000/a", "10.1000/b", "10.1000/c"):
                    f.write(json.dumps({"doi": doi}) + "\n")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ps.main(["add", "--records", rec, "--run", run, "--lr-script", stub, "--chunk", "2"])
            self.assertIn("added 2 new papers", buf.getvalue())
            with open(os.path.join(d, "add-log.json"), encoding="utf-8") as f:
                log = json.load(f)
            self.assertEqual((log["attempted"], log["resolved"], log["added_new"]), (3, 4, 2))


if __name__ == "__main__":
    unittest.main()
