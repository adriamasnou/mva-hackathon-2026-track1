#!/usr/bin/env python3
"""Extract selected ORIGINAL source records for review; never queries the navigator.

No production parser is imported. This is a collection aid, not a clinical oracle
and not a generator of frozen expected answers. Source-specific terms still apply.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def workbook_rows(path):
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(path) as archive:
        strings = ["".join(item.itertext()) for item in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    rows = []
    for item in sheet.iter(ns + "row"):
        cells = {}
        for cell in item.findall(ns + "c"):
            value = cell.findtext(ns + "v", "")
            if cell.get("t") == "s":
                value = strings[int(value)]
            elif cell.get("t") == "inlineStr":
                value = "".join(element.text or "" for element in cell.iter(ns + "t"))
            cells[cell.attrib["r"]] = value
        number = int(item.attrib["r"])
        if number < 5 or not cells.get(f"A{number}", "").strip():
            continue
        raw = cells.get(f"C{number}", "").strip()
        rows.append({"row": number, "cells": {f"{column}{number}": cells.get(f"{column}{number}", "") for column in "ABC"},
                     "condition": cells[f"A{number}"].strip(), "status": cells.get(f"B{number}", "").strip(),
                     "omim_raw": raw, "mims": [value for value in re.findall(r"\d+", raw) if len(value) == 6]})
    if not rows or rows[0]["condition"] == "Condition name":
        raise ValueError("Workbook row assumptions changed; inspect before continuing")
    return rows


def mapping_records(path):
    name = path.name
    lines = path.read_text().splitlines()
    records = []
    header = next((line for line in lines if not line.startswith("#")), "") if name == "genes_to_disease.txt" else lines[0]
    for number, line in enumerate(lines, 1):
        values = line.split("\t")
        associations = []
        if name == "gene_condition_source_id":
            if number == 1:
                continue
            if len(values) != 9:
                raise ValueError(f"Unexpected ClinVar width at {number}")
            mim = values[7]
            for index, field in ((1, "AssociatedGenes"), (2, "RelatedGenes")):
                for gene in re.split(r"[;,|]", values[index]):
                    if gene.strip() and gene.strip() != "-":
                        associations.append({"gene": gene.strip(), "field": field, "role": field})
            extra = {"source_disease_name": values[4], "upstream": values[5], "source_id": values[6]}
        elif name == "genes_to_disease.txt":
            if number == 1:
                continue
            if len(values) != 5:
                raise ValueError(f"Unexpected HPO width at {number}")
            mim = values[3].removeprefix("OMIM:") if values[3].startswith("OMIM:") else ""
            if values[1] and values[1] != "-":
                associations = [{"gene": values[1], "field": "gene_symbol", "role": values[2]}]
            extra = {"upstream": values[4]}
        else:
            if line.startswith("#"):
                continue
            mim = values[0]
            if len(values) < 4:
                raise ValueError(f"Unexpected OMIM width at {number}")
            if values[1] == "gene" and values[3]:
                associations = [{"gene": values[3], "field": "Approved Gene Symbol (HGNC)", "role": "gene-identifier-only"}]
            extra = {"entry_type": values[1], "not_a_phenotype_mapping": True}
        if mim.isdigit():
            records.append({"line": number, "text": line, "mim": mim, "associations": associations, **extra})
    return header, records


def collect(hfea, source_dir):
    selection = json.loads((HERE / "selection-plan.json").read_text())
    receipt = json.loads((HERE / "selection-freeze.json").read_text())
    if sha(HERE / "selection-plan.json") != receipt["sha256"]:
        raise ValueError("Selection freeze mismatch")
    provenance = json.loads((REPO / "submissions/hfea-pgtm-provenance.json").read_text())
    sources, mappings = {}, {}
    for source in provenance["sources"]:
        path = hfea if source["name"].endswith(".xlsx") else source_dir / source["name"]
        if sha(path) != source["sha256"]:
            raise ValueError("Source hash differs: " + source["name"])
        sources[source["name"]] = {key: source[key] for key in ("url", "sha256", "bytes")}
        if not source["name"].endswith(".xlsx"):
            header, records = mapping_records(path)
            mappings[source["name"]] = {"header": header, "records": records}
    rows = workbook_rows(hfea)
    candidates, selected = [], set()
    for task in selection["queries"]:
        query = task["query"].strip().upper()
        symbol = "BUB1B" if query == "BUBR1" else query
        identifiers = {record["mim"] for source in mappings.values() for record in source["records"]
                       if any(item["gene"] == symbol for item in record["associations"])}
        gene_rows = [row["row"] for row in rows if identifiers.intersection(row["mims"])]
        text_rows = [row["row"] for row in rows if query and query in row["condition"].upper()]
        id_rows = [row["row"] for row in rows if query in row["mims"]]
        selected.update(gene_rows + text_rows + id_rows)
        candidates.append({**task, "source_symbol": symbol, "source_association_rows": gene_rows,
                           "condition_text_rows": text_rows, "identifier_rows": id_rows})
    selected_rows = [row for row in rows if row["row"] in selected]
    mims = sorted({mim for row in selected_rows for mim in row["mims"]})
    for source in mappings.values():
        source["context_records"] = [record for record in source["records"]
                                     if record["mim"] in ("230900", "231000", "277900", "606463", "606882")]
        source["records"] = [record for record in source["records"] if record["mim"] in mims]
    return {"schema_version": 1, "scope": "Original source excerpts collected before navigator execution; not yet manual adjudication.",
            "selection_sha256": receipt["sha256"], "sources": sources,
            "source_terms": "Selected excerpts only; no whole mapping source redistributed. OMIM copyright Johns Hopkins University; use subject to https://omim.org/help/agreement . Observe all upstream source terms.",
            "selection_mims": mims, "query_source_candidates": candidates,
            "hfea_rows": selected_rows,
            "context_rows": [row for row in rows if row["row"] in (853, 854)],
            "context_scope": "Pre-query source follow-up for GBA and ATP7B no-match candidates. GBA1 and Wilson-condition names were inspected in sources only, not added to the navigator query set. All five context MIMs include every retained mapping line.",
            "mapping_records": mappings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hfea", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(collect(args.hfea, args.source_dir), indent=2))
