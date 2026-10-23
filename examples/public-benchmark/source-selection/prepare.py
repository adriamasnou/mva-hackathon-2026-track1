#!/usr/bin/env python3
"""Freeze public phenopacket-derived inputs without running or reading Exomiser.

Standard library only. Local source ZIP is hash-pinned. --download fetches only
the 11.6 MB public archive. Outputs contain public literature data, never MVA.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
STATES = {"GENO:0000135": "heterozygous", "GENO:0000136": "homozygous",
          "GENO:0000134": "hemizygous"}
AUTOSOMES = {str(i) for i in range(1, 23)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def parse_case(member, raw, plan):
    p = json.loads(raw)
    ints = p.get("interpretations", [])
    if len(ints) != 1 or ints[0].get("progressStatus") != "SOLVED":
        return None, "not_one_solved_interpretation"
    gis = ints[0].get("diagnosis", {}).get("genomicInterpretations", [])
    if len(gis) not in (1, 2):
        return None, "not_one_or_two_genomic_interpretations"
    variants, genes = [], set()
    for gi in gis:
        if gi.get("interpretationStatus") != "CAUSATIVE":
            return None, "not_all_causative"
        v = gi.get("variantInterpretation", {}).get("variationDescriptor", {})
        g = v.get("geneContext", {})
        if not g.get("symbol") or not g.get("valueId", "").startswith("HGNC:"):
            return None, "missing_gene_identity"
        genes.add((g["symbol"], g["valueId"]))
        r = v.get("vcfRecord", {})
        if r.get("genomeAssembly") != "hg38":
            return None, "no_explicit_hg38_vcf_record"
        chrom = r.get("chrom", "").removeprefix("chr")
        if chrom not in AUTOSOMES | {"X"}:
            return None, "non_autosome_or_X"
        try:
            pos = int(r["pos"])
        except (KeyError, ValueError, TypeError):
            return None, "invalid_position"
        ref, alt = r.get("ref", ""), r.get("alt", "")
        if pos < 1 or ref == alt or any(not re.fullmatch("[ACGT]{1,49}", s) for s in (ref, alt)):
            return None, "not_explicit_small_sequence_variant"
        state = v.get("allelicState", {})
        if state.get("id") not in STATES or STATES[state["id"]] != state.get("label"):
            return None, "unsupported_or_inconsistent_allelic_state"
        variants.append({"chrom": chrom, "pos": pos, "ref": ref, "alt": alt,
                         "genome_assembly": "GRCh38", "allelic_state": state,
                         "genotype": {"heterozygous": "0/1", "homozygous": "1/1", "hemizygous": "1"}[state["label"]],
                         "expressions": v.get("expressions", [])})
    if len(genes) != 1:
        return None, "multiple_genes"
    gene, hgnc = next(iter(genes))
    if gene in plan["excluded_genes"]:
        return None, "predeclared_gene_exclusion"
    keys = {(v["chrom"], v["pos"], v["ref"], v["alt"]) for v in variants}
    if len(keys) != len(variants):
        return None, "duplicate_causal_record"
    labels = [v["allelic_state"]["label"] for v in variants]
    chroms = {v["chrom"] for v in variants}
    sex = p.get("subject", {}).get("sex", "UNKNOWN_SEX")
    if len(chroms) != 1:
        return None, "causal_records_on_different_chromosomes"
    if chroms <= AUTOSOMES:
        lookup = {("heterozygous",): "autosomal_single_heterozygous",
                  ("homozygous",): "autosomal_homozygous",
                  ("heterozygous", "heterozygous"): "autosomal_two_heterozygous"}
        stratum = lookup.get(tuple(labels))
    elif labels == ["heterozygous"] and sex == "FEMALE":
        stratum = "X_heterozygous_female"
    elif labels == ["hemizygous"] and sex == "MALE":
        stratum = "X_hemizygous_male"
    else:
        stratum = None
    if not stratum:
        return None, "unsupported_genotype_sex_stratum"
    features = p.get("phenotypicFeatures", [])
    observed = sorted({f["type"]["id"] for f in features if not f.get("excluded", False)
                       and re.fullmatch(r"HP:\d{7}", f.get("type", {}).get("id", ""))})
    excluded = sorted({f["type"]["id"] for f in features if f.get("excluded", False)
                       and re.fullmatch(r"HP:\d{7}", f.get("type", {}).get("id", ""))})
    if len(observed) < 3:
        return None, "fewer_than_three_observed_HPO_terms"
    if set(observed) & set(excluded):
        return None, "same_HPO_present_and_absent"
    refs = p.get("metaData", {}).get("externalReferences", [])
    if not any(re.fullmatch(r"PMID:\d+", r.get("id", "")) for r in refs):
        return None, "no_PubMed_source_reference"
    return {"case_id": p["id"], "subject_id": p.get("subject", {}).get("id"),
            "gene": gene, "hgnc_id": hgnc, "stratum": stratum, "sex": sex,
            "causal_variants": variants, "hpo_ids": observed, "excluded_hpo_ids": excluded,
            "source_phenotypic_features": features,
            "source_diagnosis": ints[0]["diagnosis"]["disease"],
            "source_references": refs, "source_member": member, "source_sha256": sha(raw),
            "truth_status": "source-curated SOLVED/CAUSATIVE; not independently re-adjudicated from every original case report"}, None


def choose(candidates, plan):
    rank = lambda *x: sha("|".join([plan["seed"], *x]).encode())
    chosen, used = [], set()
    for stratum, quota in plan["quotas_in_selection_order"]:
        groups = collections.defaultdict(list)
        for c in candidates:
            if c["stratum"] == stratum and c["gene"] not in used:
                groups[c["gene"]].append(c)
        ordered = sorted(groups, key=lambda g: (rank("gene", stratum, g), g))
        if len(ordered) < quota:
            raise ValueError(f"Insufficient unique genes for frozen quota {stratum}: {len(ordered)} < {quota}")
        for g in ordered[:quota]:
            c = min(groups[g], key=lambda c: (rank("case", c["source_member"]), c["source_member"]))
            chosen.append(c)
            used.add(g)
    donors = sorted(chosen, key=lambda c: (rank("donor", c["case_id"]), c["case_id"]))
    for i, c in enumerate(donors):
        donor = donors[(i + 1) % len(donors)]
        c["arms"] = {"original": c["hpo_ids"],
                     "half_missing": sorted(sorted(c["hpo_ids"], key=lambda hp: (rank("drop", c["case_id"], hp), hp))[:math.ceil(len(c["hpo_ids"]) / 2)]),
                     "swapped": donor["hpo_ids"], "none": []}
        c["swapped_donor_case_id"] = donor["case_id"]
        c["swapped_donor_gene"] = donor["gene"]
    return chosen


def vcf_text(c):
    rows = ["##fileformat=VCFv4.2", "##reference=GRCh38",
            "##source=PhenopacketStore_0.1.19_causal_only_spike_ingredients",
            '##FORMAT=<ID=GT,Number=1,Type=String,Description="Source zygosity; phase unasserted">',
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPUBLIC_CASE"]
    for v in sorted(c["causal_variants"], key=lambda v: (23 if v["chrom"] == "X" else int(v["chrom"]), v["pos"], v["ref"], v["alt"])):
        rows.append("\t".join(map(str, [v["chrom"], v["pos"], ".", v["ref"], v["alt"], ".", "PASS", ".", "GT", v["genotype"]])))
    return "\n".join(rows) + "\n"


def reference_check(cases, reference):
    fai = Path(str(reference) + ".fai")
    idx = {}
    for line in fai.read_text().splitlines():
        name, length, offset, bases, width = line.split("\t")[:5]
        idx[name] = tuple(map(int, (length, offset, bases, width)))
    checks = []
    with reference.open("rb") as f:
        for c in cases:
            for v in c["causal_variants"]:
                chrom = v["chrom"] if v["chrom"] in idx else "chr" + v["chrom"]
                length, offset, bases, width = idx[chrom]
                start = v["pos"] - 1
                if start < 0 or start + len(v["ref"]) > length:
                    raise ValueError("Reference coordinate out of bounds")
                seq = b""
                for p in range(start, start + len(v["ref"])):
                    f.seek(offset + (p // bases) * width + p % bases)
                    seq += f.read(1)
                actual = seq.decode().upper()
                checks.append({"case_id": c["case_id"], "chrom": chrom, "pos": v["pos"],
                               "expected_ref": v["ref"], "observed_ref": actual, "matches": actual == v["ref"]})
    return {"reference_path": str(reference.resolve()), "reference_bytes": reference.stat().st_size,
            "fai_sha256": sha(fai.read_bytes()), "whole_reference_hashed": False,
            "checks": checks, "all_match": all(c["matches"] for c in checks)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--output-dir", type=Path, default=ROOT / "prepared")
    ap.add_argument("--reference", type=Path)
    args = ap.parse_args()
    plan_path = ROOT / "selection-plan.json"
    plan = json.loads(plan_path.read_text())
    archive = ROOT / "source" / "all_phenopackets-0.1.19.zip"
    if args.download and not archive.exists():
        urllib.request.urlretrieve(plan["archive_url"], archive)
    raw_zip = archive.read_bytes()
    if sha(raw_zip) != plan["archive_sha256"] or len(raw_zip) != plan["archive_bytes"]:
        raise ValueError("Public source archive checksum/size mismatch")
    candidates, audit, selected_raw = [], [], {}
    with zipfile.ZipFile(archive) as z:
        for member in sorted(z.namelist()):
            if not member.endswith(".json"):
                continue
            raw = z.read(member)
            c, reason = parse_case(member, raw, plan)
            audit.append({"member": member, "sha256": sha(raw), "eligible": c is not None,
                          "reason": reason, "gene": c["gene"] if c else None,
                          "stratum": c["stratum"] if c else None})
            if c:
                candidates.append(c)
        cases = choose(candidates, plan)
        for c in cases:
            selected_raw[c["source_member"]] = z.read(c["source_member"])
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for c in cases:
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", c["case_id"])
        c["local_source"] = f"source/selected/{safe}.json"
        destination = ROOT / c["local_source"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(selected_raw[c["source_member"]])
        c["causal_only_vcf"] = f"causal-only/{safe}.vcf"
        vcf = out / c["causal_only_vcf"]
        vcf.parent.mkdir(parents=True, exist_ok=True)
        vcf.write_text(vcf_text(c))
        c["causal_only_vcf_sha256"] = sha(vcf.read_bytes())
        for arm, hp in c["arms"].items():
            dump(out / "phenotypes" / f"{safe}.{arm}.json", {"case_id": c["case_id"], "arm": arm, "hpoIds": hp})
    counts = collections.Counter(c["stratum"] for c in candidates)
    manifest = {"schema_version": "1.0", "frozen_at_utc": plan["frozen_at_utc"],
                "selection_plan_sha256": sha(plan_path.read_bytes()), "selection_plan": plan,
                "source": {"name": "Phenopacket Store", "version": plan["release"], "url": plan["archive_url"],
                           "sha256": plan["archive_sha256"], "bytes": len(raw_zip),
                           "license": "BSD-3-Clause", "license_file": "source/LICENSE-phenopacket-store.txt",
                           "paper_pmid": "39394689", "paper_doi": "10.1016/j.xhgg.2024.100371"},
                "selection_counts": {"source_cases": len(audit), "eligible_cases": len(candidates),
                                     "eligible_genes": len({c["gene"] for c in candidates}),
                                     "eligible_by_stratum": dict(counts), "selected_cases": len(cases),
                                     "selected_genes": len({c["gene"] for c in cases}),
                                     "rejection_counts": dict(collections.Counter(a["reason"] for a in audit if not a["eligible"]))},
                "cases": cases}
    dump(out / "cases.json", manifest)
    dump(out / "eligibility-audit.json", audit)
    if args.reference:
        rc = reference_check(cases, args.reference)
        dump(out / "reference-check.json", rc)
        if not rc["all_match"]:
            raise ValueError("Reference mismatch; keep the selected case and report failure, do not replace it")
    files = {str(p.relative_to(out)): sha(p.read_bytes()) for p in sorted(out.rglob("*")) if p.is_file() and p.name != "checksums.json"}
    dump(out / "checksums.json", files)
    print(json.dumps({"cases": len(cases), "genes": [c["gene"] for c in cases], "manifest": str(out / "cases.json"),
                      "manifest_sha256": sha((out / "cases.json").read_bytes()), "reference_checked": args.reference is not None}))


if __name__ == "__main__":
    main()
