#!/usr/bin/env python3
"""Build a dated candidate gene-to-condition index from public HFEA, ClinVar, HPO and OMIM files."""
import csv, json, pathlib, re, zipfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = ROOT / "data/derived/crosswalk-sources"
XLSX = ROOT / "data/derived/hfea_pgtm_2026-08-05.xlsx"

FEEDS = {
    "gene_condition_source_id": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id",
    "genes_to_disease.txt":     "https://purl.obolibrary.org/obo/hp/hpoa/genes_to_disease.txt",
    "mim2gene.txt":             "https://omim.org/static/omim/data/mim2gene.txt",
}


# ---------------------------------------------------------------- the HFEA register
def read_hfea():
    r"""
    Parse the register as it ACTUALLY IS, not as it ought to be.

    The OMIM column is not a number column. Across 2,063 rows it contains, verbatim:
      "612555, 600185"                  two MIMs, comma-separated
      "609307 & 193003"                 two MIMs, ampersand-separated
      "601728, 158350, 153480, 605309"  four MIMs
      "*182340", " *620823 "            OMIM's own GENE-entry prefix, plus stray whitespace
      "ARVC/D"                          free text where a number belongs
      "28000"                           five digits -- a malformed MIM (CHIME is 280000)
      " "                               blank

    An earlier version of this function ran re.sub(r"\D", "", cell), which glued
    "612555, 600185" into the single nonexistent MIM 612555600185 and silently dropped
    those rows as unmappable. That UNDERSTATED coverage -- the wrong direction for a
    claim about how findable something is. Every anomaly is now parsed and REPORTED.
    """
    z = zipfile.ZipFile(XLSX)
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    shared = [
        "".join(t.text or "" for t in si.iter(ns + "t"))
        for si in ET.fromstring(z.read("xl/sharedStrings.xml") if "xl/sharedStrings.xml" in z.namelist() else b"<sst/>")
    ]
    out, header_seen = [], False
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(ns + "row"):
        cells = {}
        for c in row.iter(ns + "c"):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            if c.get("t") == "inlineStr":
                cells[col] = "".join(t.text or "" for t in c.iter(ns + "t"))
                continue
            v = c.find(ns + "v")
            if v is None or v.text is None:
                continue
            cells[col] = shared[int(v.text)] if c.get("t") == "s" else v.text
        cond = cells.get("A", "").strip()
        status = cells.get("B", "").strip()
        raw = cells.get("C", "").strip()
        if not header_seen:
            # Anchor on the HEADER CELL ITSELF, never on a substring. The sheet's row-2
            # preamble contains the words "OMIM number" too, and matching that consumed the
            # real header row, letting "Condition name" through as a data row.
            if raw == "OMIM number" or cond == "Condition name":
                header_seen = True
            continue
        if not cond:
            continue
        mims = re.findall(r"\d{4,7}", raw)
        flags = []
        if not raw:
            flags.append("no-omim-cell")
        elif not mims:
            flags.append("text-not-a-number")
        if len(mims) > 1:
            flags.append(f"multi-omim({len(mims)})")
        if any(len(m) != 6 for m in mims):
            flags.append("malformed-mim-length")
        if "*" in raw:
            flags.append("asterisk-gene-entry")
        out.append({"condition": cond, "status": status, "omim_raw": raw,
                    "mims": [m for m in mims if len(m) == 6],
                    "bad_mims": [m for m in mims if len(m) != 6],
                    "flags": flags})
    z.close()
    if not header_seen:
        raise ValueError("HFEA header not found")
    return out


# ---------------------------------------------------------------- phenotype -> gene
def checked_tsv(path, required):
    """Reject schema drift and partial rows instead of publishing plausible omissions.

    A missing RelatedGenes header used to pass the BUB1B control while silently
    discarding related-gene mappings. Whole-file completeness still requires the
    supplied source hashes; a syntactically complete truncated file is not detectable
    from TSV structure alone.
    """
    with open(path, encoding="utf8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or not set(required) <= set(headers):
            raise ValueError(f"{path.name}: unexpected TSV schema; required {sorted(required)}")
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{path.name}:{reader.line_num}: partial or extra-column TSV row")
            yield row


def add_evidence(mapping, mim, gene, record):
    """Keep distinct source roles/fields, deduplicating only identical evidence."""
    records = mapping.setdefault(mim, {}).setdefault(gene, [])
    if record not in records:
        records.append(record)


def gene_sets(mapping):
    return {mim: set(genes) for mim, genes in mapping.items()}


def read_clinvar_evidence():
    m = {}
    for r in checked_tsv(SRC / "gene_condition_source_id",
                         {"DiseaseMIM", "AssociatedGenes", "RelatedGenes"}):
        # Keep both fields: multi-gene phenotypes can use RelatedGenes exclusively.
        mim = r["DiseaseMIM"].strip()
        if mim.isdigit():
            for field in ("AssociatedGenes", "RelatedGenes"):
                for sym in re.split(r"[;,|]", r[field]):
                    sym = sym.strip()
                    if sym and sym != "-":
                        add_evidence(m, mim, sym, dict(source="ClinVar", omim=mim,
                                     source_field=field, association_type=None))
    return m


def read_hpo_evidence():
    m = {}
    for r in checked_tsv(SRC / "genes_to_disease.txt", {"disease_id", "gene_symbol", "association_type"}):
        did, sym = r["disease_id"].strip(), r["gene_symbol"].strip()
        # HPO's '-' sentinel is not a gene, even though it is truthy in Python.
        if did.startswith("OMIM:") and sym and sym != "-":
            add_evidence(m, did[5:], sym, dict(source="HPO", omim=did[5:],
                         source_field="gene_symbol", association_type=r["association_type"]))
    return m


def read_mim2gene_evidence():
    """GENE-MIM index only. Used to catch HFEA rows citing a gene MIM, never as phenotype->gene."""
    m = {}
    with open(SRC / "mim2gene.txt", encoding="utf8", errors="replace") as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4 and p[1].strip() == "gene" and p[3].strip():
                mim = p[0].strip()
                add_evidence(m, mim, p[3].strip(), dict(source="OMIM-geneMIM", omim=mim,
                             source_field="Approved Gene Symbol (HGNC)", entry_type=p[1].strip(),
                             association_type=None))
    return m


def read_clinvar():
    return gene_sets(read_clinvar_evidence())


def read_hpo():
    return gene_sets(read_hpo_evidence())


def read_mim2gene():
    return gene_sets(read_mim2gene_evidence())


def main():
    import argparse, hashlib, datetime
    global SRC, XLSX
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hfea', type=pathlib.Path, required=True)
    ap.add_argument('--source-dir', type=pathlib.Path, required=True)
    ap.add_argument('--snapshot-date', required=True, help='HFEA workbook date, ISO YYYY-MM-DD')
    ap.add_argument('--register-source-url', required=True, help='URL of the exact register workbook supplied')
    ap.add_argument('--out-dir', type=pathlib.Path, required=True)
    args = ap.parse_args()
    datetime.date.fromisoformat(args.snapshot_date)
    SRC, XLSX = args.source_dir, args.hfea
    files = [XLSX, *(SRC/n for n in FEEDS)]
    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        ap.error('Missing inputs: '+', '.join(missing))
    rows = read_hfea()
    cv, hp, gm = read_clinvar_evidence(), read_hpo_evidence(), read_mim2gene_evidence()
    if not rows or any(not m for m in (cv,hp,gm)):
        ap.error('An input parsed to zero records; refusing to publish')
    if 'BUB1B' not in (set(cv.get('257300',{})) | set(hp.get('257300',{}))):
        ap.error('BUB1B / OMIM 257300 positive control failed')
    out = []
    for row in rows:
        evidence = {}
        sets = []
        for name, mapping in [('ClinVar',cv),('HPO',hp),('OMIM-geneMIM',gm)]:
            genes = set()
            for mim in row['mims']:
                genes.update(mapping.get(mim,{}))
                for gene, records in mapping.get(mim,{}).items():
                    for record in records:
                        if record not in evidence.setdefault(gene,[]):
                            evidence[gene].append(record)
            sets.append(genes)
        a,b,c = sets
        genes = sorted(a|b|c)
        out.append(dict(condition=row['condition'], hfea_status=row['status'],
            omim=';'.join(row['mims']), omim_as_published=row['omim_raw'],
            genes=';'.join(genes), n_genes=len(genes),
            sources=','.join(n for n,g in zip(['ClinVar','HPO','OMIM-geneMIM'],sets) if g),
            clinvar_hpo=('both' if a==b else 'differ') if a and b else ('single' if a or b else ''),
            register_defect=';'.join(row['flags']), gene_evidence=json.dumps(evidence,sort_keys=True)))
    index = {}
    for row in out:
        for gene in filter(None,row['genes'].split(';')):
            index.setdefault(gene,[]).append(row['condition'])
    stats = dict(rows=len(out), mapped_rows=sum(bool(r['n_genes']) for r in out),
                 unmapped_rows=sum(not r['n_genes'] for r in out), genes=len(index),
                 source_disagreements=sum(r['clinvar_hpo']=='differ' for r in out),
                 genes_not_named_in_condition_text=sum(not any(re.search(r'\b'+re.escape(g)+r'\b',c,re.I) for c in cs) for g,cs in index.items()))
    provenance = dict(schema_version=2, register_snapshot=args.snapshot_date,
        generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        register_url='https://www.hfea.gov.uk/pgt-m-conditions/',
        warning='Candidate mappings from dated public sources. Not variant classification, eligibility or funding advice. No result is not evidence of ineligibility. Confirm with the regulator and clinic.',
        sources=[dict(name=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size,
                      local_file_mtime_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),
                      url=FEEDS.get(p.name,args.register_source_url)) for p in files],
        stats=stats)
    args.out_dir.mkdir(parents=True,exist_ok=True)
    with (args.out_dir/'hfea-pgtm-gene-crosswalk.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys(),lineterminator="\n"); w.writeheader(); w.writerows(out)
    (args.out_dir/'hfea-pgtm-gene-index.json').write_text(json.dumps(dict(_note=provenance['warning'],_register_snapshot=args.snapshot_date,index={k:sorted(set(v)) for k,v in sorted(index.items())}),indent=1)+'\n')
    (args.out_dir/'hfea-pgtm-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    payload = json.dumps(dict(provenance=provenance,rows=out),ensure_ascii=False).replace('<','\\u003c')
    template = pathlib.Path(__file__).with_name('template.html').read_text()
    (args.out_dir/'pgtm-navigator.html').write_text(template.replace('__DATA__',payload))
    print(json.dumps(stats,indent=2))

if __name__ == '__main__':
    main()
