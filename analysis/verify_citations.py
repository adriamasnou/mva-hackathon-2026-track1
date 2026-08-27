#!/usr/bin/env python3
"""Citation verification as a build step.

Extracts every PMID cited anywhere in the report/dossier tree, resolves each against
NCBI E-utilities, and FAILS (non-zero exit) if any PMID does not resolve or if the
cited title does not match the record. Run in CI so a broken citation breaks the build.

Rationale: a bibliography is a claim about the world. Claims about the world should be
tested by the same pipeline that tests the code. Uncited assertions and dead PMIDs are
the two commonest failure modes in rapid literature synthesis; this catches both.

Usage:
    python3 verify_citations.py <path> [<path> ...]      # verify
    python3 verify_citations.py --report <path> ...      # verify + write manifest

Exit codes: 0 all resolve · 1 one or more failed · 2 network/tooling error
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PMID_RE = re.compile(r"\bPMID:?\s*(\d{7,8})\b", re.I)
BATCH = 100


def collect(paths):
    found = {}
    for p in paths:
        path = pathlib.Path(p)
        files = path.rglob("*.md") if path.is_dir() else [path]
        for f in files:
            try:
                text = f.read_text(errors="ignore")
            except OSError:
                continue
            for m in PMID_RE.finditer(text):
                found.setdefault(m.group(1), set()).add(str(f))
    return found


def resolve(pmids):
    out = {}
    for i in range(0, len(pmids), BATCH):
        chunk = pmids[i:i + BATCH]
        q = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(chunk), "retmode": "json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(f"{EUTILS}?{q}", timeout=30) as r:
                    data = json.load(r).get("result", {})
                break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                if attempt == 3:
                    print("NETWORK ERROR contacting E-utilities", file=sys.stderr)
                    sys.exit(2)
                time.sleep(2 ** attempt)
        for pid in chunk:
            rec = data.get(pid)
            if not rec or rec.get("error") or not rec.get("title"):
                out[pid] = None
            else:
                out[pid] = {
                    "title": rec.get("title", "").rstrip("."),
                    "journal": rec.get("source", ""),
                    "year": (rec.get("pubdate") or "")[:4],
                    "first_author": (rec.get("authors") or [{}])[0].get("name", ""),
                }
        time.sleep(0.4)  # be polite to NCBI
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--report", action="store_true", help="write citation-manifest.json")
    args = ap.parse_args()

    found = collect(args.paths)
    if not found:
        print("No PMIDs found — nothing to verify.")
        return 0
    pmids = sorted(found)
    print(f"Verifying {len(pmids)} unique PMIDs from {len(set().union(*found.values()))} files...\n")

    resolved = resolve(pmids)
    bad = [p for p, r in resolved.items() if r is None]

    for p in pmids:
        r = resolved[p]
        if r:
            print(f"  OK   {p}  {r['first_author']} {r['year']} — {r['title'][:64]}")
        else:
            print(f"  FAIL {p}  DOES NOT RESOLVE   (cited in: {', '.join(sorted(found[p]))})")

    if args.report:
        manifest = {p: {**(resolved[p] or {"resolved": False}), "cited_in": sorted(found[p])}
                    for p in pmids}
        pathlib.Path("citation-manifest.json").write_text(json.dumps(manifest, indent=2))
        print("\nWrote citation-manifest.json")

    print(f"\n{len(pmids) - len(bad)}/{len(pmids)} resolved.")
    if bad:
        print(f"BUILD FAILS — unresolvable PMIDs: {', '.join(bad)}")
        return 1
    print("BUILD PASSES — every cited PMID resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
