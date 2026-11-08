#!/usr/bin/env python3
"""PubMed search for the lr-ai bridge (Python standard library only).

Sub-commands (search, add; sample prints a fair look at the titles):

  search  Run one or more PubMed queries through NCBI E-utilities, de-duplicate by PMID and
          write the records to <out>/records.jsonl plus <out>/queries.json and summary.json.
          Prints a short summary only (counts), never the records, so it costs almost no
          model tokens.
  add     Add the DOIs from records.jsonl to an existing lr-ai run with `lr.py add`, skipping
          DOIs the run already has. lr-ai resolves them through OpenAlex and tags them
          "manual"; filters, screening and snowballing then treat them like any other paper.

Environment (all optional, never printed):
  NCBI_API_KEY   raises the NCBI limit from 3 to 10 requests per second
  NCBI_EMAIL     identifies you to NCBI (recommended by NCBI for scripts)

Queries must be generic search concepts. Never put patient data into a query.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "clinical-research-copilot"
SUMMARY_CHUNK = 150
# Publication types dropped by default (mirrors lr-ai's exclude_types for opinion-type records).
# Each name was checked against PubMed ("Retraction of Publication"[pt] is not recognised, so it is not listed).
DEFAULT_EXCLUDED_TYPES = ["Editorial", "Letter", "Comment", "News", "Published Erratum", "Retracted Publication"]

_last_call = [0.0]


def _interval():
    return 0.11 if os.environ.get("NCBI_API_KEY") else 0.34


def _get_json(endpoint, params):
    """GET an E-utilities endpoint as JSON, with a rate limit and a few retries."""
    params = dict(params, retmode="json", tool=TOOL)
    if os.environ.get("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    if os.environ.get("NCBI_EMAIL"):
        params["email"] = os.environ["NCBI_EMAIL"]
    url = EUTILS + endpoint + "?" + urllib.parse.urlencode(params)
    last_err = None
    for attempt in range(4):
        wait = _last_call[0] + _interval() - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": TOOL})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code not in (429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = type(e).__name__
        time.sleep(2 ** attempt)
    # The URL is deliberately not printed: it may carry the API key.
    raise SystemExit(f"NCBI request to {endpoint} failed ({last_err}).")


def build_term(query, lang="en", keep_all_types=False):
    """Wrap a user query with the language and publication-type limits."""
    term = f"({query})"
    if lang and lang.lower() not in ("any", "none"):
        names = {"en": "English", "tr": "Turkish", "de": "German", "fr": "French", "es": "Spanish"}
        term += f" AND {names.get(lang.lower(), lang)}[lang]"
    if not keep_all_types:
        term += " NOT (" + " OR ".join(f'"{t}"[pt]' for t in DEFAULT_EXCLUDED_TYPES) + ")"
    return term


def parse_esearch(data):
    """esearchresult dict -> (matches, pmids, how PubMed read the query, warnings and errors it returned)."""
    if data.get("ERROR"):
        raise SystemExit(f"PubMed rejected the query: {data['ERROR']}")
    notes = {k: data[k] for k in ("warninglist", "errorlist") if data.get(k)}
    return int(data.get("count", 0)), list(data.get("idlist", [])), data.get("querytranslation", ""), notes


def esearch(term, limit, year_from=None, year_to=None):
    params = {"db": "pubmed", "term": term, "retmax": limit, "sort": "relevance"}
    if year_from or year_to:
        params.update(datetype="pdat", mindate=str(year_from or 1900), maxdate=str(year_to or 3000))
    return parse_esearch(_get_json("esearch.fcgi", params).get("esearchresult", {}))


def pick_sample(records, n):
    """n records spread evenly over the list (not just its first entries)."""
    if n <= 0 or not records:
        return []
    if n >= len(records):
        return list(records)
    step = len(records) / n
    return [records[int(i * step)] for i in range(n)]


_DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)


def norm_doi(value):
    if not value:
        return None
    m = _DOI_RE.search(str(value))
    return m.group(0).rstrip(".,;)").lower() if m else None


def parse_summary(uid, item):
    """One esummary record -> our compact record."""
    doi = None
    for aid in item.get("articleids") or []:
        if aid.get("idtype") == "doi":
            doi = norm_doi(aid.get("value"))
            break
    if not doi:
        doi = norm_doi(item.get("elocationid"))
    year_match = re.match(r"(\d{4})", item.get("pubdate") or item.get("epubdate") or "")
    return {
        "pmid": str(uid),
        "doi": doi,
        "title": " ".join((item.get("title") or "").split()),
        "year": int(year_match.group(1)) if year_match else None,
        "journal": item.get("source") or None,
        "pubtypes": item.get("pubtype") or [],
    }


def esummary(pmids):
    records = []
    for i in range(0, len(pmids), SUMMARY_CHUNK):
        chunk = pmids[i:i + SUMMARY_CHUNK]
        result = _get_json("esummary.fcgi", {"db": "pubmed", "id": ",".join(chunk)}).get("result", {})
        for uid in chunk:
            if uid in result and isinstance(result[uid], dict):
                records.append(parse_summary(uid, result[uid]))
    return records


def load_existing_dois(papers_jsonl):
    """DOIs already in an lr-ai papers.jsonl (empty set if the file is missing)."""
    dois = set()
    if not papers_jsonl or not os.path.isfile(papers_jsonl):
        return dois
    with open(papers_jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = norm_doi(json.loads(line).get("doi"))
            except (json.JSONDecodeError, AttributeError):
                continue
            if d:
                dois.add(d)
    return dois


def chunked(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def cmd_search(args):
    queries = list(args.query)
    if args.queries_file:
        with open(args.queries_file, encoding="utf-8") as f:
            queries += [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    if not queries:
        raise SystemExit("Give at least one --query (or --queries-file).")
    os.makedirs(args.out, exist_ok=True)
    existing = load_existing_dois(args.existing)

    log, by_pmid = [], {}
    for n, query in enumerate(queries, 1):
        term = build_term(query, args.lang, args.keep_all_types)
        total, ids, translation, notes = esearch(term, args.limit, args.year_from, args.year_to)
        log.append({"n": n, "query": query, "term": term, "pubmed_translation": translation, "pubmed_notes": notes,
                    "matches": total, "fetched": len(ids), "truncated": total > len(ids)})
        for pmid in ids:
            by_pmid.setdefault(pmid, []).append(n)

    records = esummary(list(by_pmid))
    for r in records:
        r["queries"] = by_pmid[r["pmid"]]
        r["in_run"] = bool(r["doi"] and r["doi"] in existing)

    with open(os.path.join(args.out, "records.jsonl"), "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(args.out, "queries.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    with_doi = [r for r in records if r["doi"]]
    summary = {
        "date": time.strftime("%Y-%m-%d"),
        "queries": len(queries),
        "unique_pmids": len(records),
        "with_doi": len(with_doi),
        "without_doi": len(records) - len(with_doi),
        "already_in_run": sum(1 for r in with_doi if r["in_run"]),
        "new_with_doi": sum(1 for r in with_doi if not r["in_run"]),
        "per_query": [{"n": e["n"], "matches": e["matches"], "fetched": e["fetched"], "truncated": e["truncated"],
                       "pubmed_notes": bool(e["pubmed_notes"])} for e in log],
        "truncated_queries": [e["n"] for e in log if e["truncated"]],
        "zero_hit_queries": [e["n"] for e in log if e["matches"] == 0],
        "queries_with_pubmed_warnings": [e["n"] for e in log if e["pubmed_notes"]],
    }
    with open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(f"Records: {os.path.join(args.out, 'records.jsonl')}")


def cmd_add(args):
    records = []
    with open(args.records, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    existing = load_existing_dois(os.path.join(args.run, "papers.jsonl"))
    todo, seen = [], set()
    for r in records:
        d = r.get("doi")
        if d and d not in existing and d not in seen:
            todo.append(d)
            seen.add(d)
    skipped_no_doi = sum(1 for r in records if not r.get("doi"))
    print(f"To add: {len(todo)} DOIs (already in run: {sum(1 for r in records if r.get('doi') in existing)}, "
          f"no DOI, not added: {skipped_no_doi}).")
    if args.dry_run or not todo:
        return
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    added_lines, resolved, new = [], 0, 0
    for chunk in chunked(todo, args.chunk):
        proc = subprocess.run([sys.executable, args.lr_script, "add", "--run", args.run] + chunk,
                              capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        out = (proc.stdout or "").strip().splitlines()
        added_lines.extend(out[:1] + [ln for ln in out[1:] if "not found" in ln or "failed" in ln][:5])
        for ln in out:
            m = re.search(r"Added (\d+) papers? \((\d+) new\)", ln)
            if m:
                resolved += int(m.group(1))
                new += int(m.group(2))
        if proc.returncode != 0:
            print((proc.stderr or "").strip()[-400:])
            raise SystemExit(f"lr.py add failed with exit code {proc.returncode}.")
    for ln in added_lines:
        print(ln)
    print(f"Attempted {len(todo)} DOIs; lr-ai resolved {resolved} and added {new} new papers to the run.")
    with open(os.path.join(os.path.dirname(os.path.abspath(args.records)), "add-log.json"), "w", encoding="utf-8") as f:
        json.dump({"date": time.strftime("%Y-%m-%d"), "attempted": len(todo), "resolved": resolved,
                   "added_new": new, "lr_output": added_lines}, f, indent=2)


def cmd_sample(args):
    records = []
    with open(args.records, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    for r in pick_sample(records, args.n):
        print(f"{r.get('pmid')}  {r.get('year')}  {(r.get('title') or '')[:110]}")


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="search PubMed and save the records")
    s.add_argument("--out", required=True, help="output folder (created)")
    s.add_argument("--query", action="append", default=[], help="PubMed query; repeat for several")
    s.add_argument("--queries-file", help="text file, one query per line (# starts a comment)")
    s.add_argument("--limit", type=int, default=100, help="records per query, most relevant first")
    s.add_argument("--year-from", type=int)
    s.add_argument("--year-to", type=int)
    s.add_argument("--lang", default="en", help="language limit, or 'any'")
    s.add_argument("--keep-all-types", action="store_true", help="do not drop editorials, letters, comments")
    s.add_argument("--existing", help="lr-ai papers.jsonl, to count what is already in the run")
    s.set_defaults(func=cmd_search)
    a = sub.add_parser("add", help="add the DOIs to an lr-ai run with lr.py add")
    a.add_argument("--records", required=True, help="records.jsonl written by 'search'")
    a.add_argument("--run", required=True, help="lr-ai run folder (contains config.yaml and papers.jsonl)")
    a.add_argument("--lr-script", required=True, help="path to lr-ai's scripts/lr.py")
    a.add_argument("--chunk", type=int, default=40, help="DOIs per lr.py call")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_add)
    m = sub.add_parser("sample", help="print titles of records spread evenly over the file (a fair look)")
    m.add_argument("--records", required=True)
    m.add_argument("--n", type=int, default=8)
    m.set_defaults(func=cmd_sample)
    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
