#!/usr/bin/env python3
"""Record/replay three existing synthetic fixtures using the real decision CLI.

Standard library only. No decision logic is implemented here or in the viewer.
All receipt paths and commands are relative to the repository root.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEMO = "examples/rescue-decision-demo"
IMPLEMENTATION = "analysis/rescue_decision/decision.py"
SCHEMA = "analysis/rescue_decision/README.md"
SCOPE = (
    "SYNTHETIC SOFTWARE EXAMPLES. Three existing frozen-case materializations, "
    "not additional independent validation cases, drug data, experiments or "
    "evidence of rescue or clinical benefit. Intervals and qualification flags "
    "are supplied assertions, not estimates fitted or authenticated by this program."
)
CASES = (
    ("abundance_rise_benefit_ruled_out", "Protein rise, benefit ruled out",
     "Shows why a protein increase alone cannot override the supplied functional-benefit interval.",
     "WORTHWHILE_BENEFIT_RULED_OUT"),
    ("selective_killing_despite_better_survivors", "Selective killing",
     "Shows why a better fraction among survivors cannot override a failed death bound and detected selection.",
     "DO_NOT_ADVANCE"),
    ("failed_exposure_measurement", "Failed exposure measurement",
     "Shows why an unqualified exposure measurement prevents biological interpretation, even with an apparently favourable interval.",
     "TECHNICALLY_INDETERMINATE"),
)
SOURCE_PATHS = (
    IMPLEMENTATION, SCHEMA, f"{DEMO}/replay.py", f"{DEMO}/demo-receipt.json",
    *(f"{DEMO}/{case[0]}.json" for case in CASES),
)


class ReplayError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReplayError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_hashes(root):
    return {name: digest((root / name).read_bytes()) for name in SOURCE_PATHS}


def collect(root=ROOT):
    """Execute decision.py three times; assert the already specified expectations."""
    before = source_hashes(root)
    records = []
    for case_id, title, purpose, expected in CASES:
        source = f"{DEMO}/{case_id}.json"
        input_bytes = (root / source).read_bytes()
        argv = ["python3", "-B", "-S", IMPLEMENTATION, source]
        run = subprocess.run(
            [sys.executable, *argv[1:]], cwd=root, capture_output=True,
            timeout=15, check=False,
        )
        require(not run.stderr, f"{case_id}: unexpected stderr: {run.stderr!r}")
        output_text = run.stdout.decode("utf-8")
        output = json.loads(output_text)
        require(run.returncode == 0 and output.get("input_valid") is True,
                f"{case_id}: decision.py rejected the fixture")
        observed = [row["decision"] for row in output["contrasts"]]
        require(observed == [expected], f"{case_id}: expected {[expected]}, got {observed}")
        require(output["replication_candidate_ids"] == [],
                f"{case_id}: unexpected replication candidate")
        records.append({
            "id": case_id, "title": title, "purpose": purpose,
            "input_path": source, "input_sha256": digest(input_bytes),
            "input_text": input_bytes.decode("utf-8"),
            "implementation_path": IMPLEMENTATION,
            "implementation_sha256": before[IMPLEMENTATION],
            "argv": argv, "command": " ".join(argv),
            "exit_code": run.returncode, "stdout_sha256": digest(run.stdout),
            "stdout_text": output_text,
            "expected_decisions": [expected], "fixture_assertions_passed": True,
        })
    require(source_hashes(root) == before, "Source changed during execution; no checkpoint published")
    return {
        "receipt_version": 1, "scope": SCOPE,
        "path_base": "repository root", "hash_algorithm": "SHA256",
        "hash_scope": "Exact file bytes; stdout_text hashes include its final newline",
        "execution": "Each stdout_text was captured from the real Python decision.py CLI; exit 0 means valid input only",
        "source_hashes": before, "cases": records,
    }


HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; base-uri 'none'; form-action 'none'">
<title>False rescue signals | Synthetic software replay</title>
<style>
:root{font:16px/1.55 system-ui,sans-serif;color:#17333e;background:#f2f5f4}*{box-sizing:border-box}body{margin:0}header{background:#153a42;color:#fff;padding:38px max(24px,calc((100vw - 1100px)/2))}header p{max-width:810px;color:#d0e2df;margin-bottom:0}.eyebrow{font-size:12px;font-weight:750;letter-spacing:.13em;color:#80d5bc}h1{font-size:clamp(30px,5vw,48px);line-height:1.12;margin:14px 0}main{max-width:1148px;margin:auto;padding:24px}h2{font-size:24px;line-height:1.3;margin:0 0 8px}h3{font-size:17px;margin:0 0 14px}.subtle{color:#526971;font-size:14px}a{color:#096b62}button{font:inherit;cursor:pointer;border:1px solid #cadad6;border-radius:8px;background:#fff;color:#176c63;padding:14px 16px;text-align:left}button[aria-pressed="true"]{background:#176c63;color:#fff;border-color:#176c63}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #c99429;outline-offset:3px}.chooser{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0 22px}.notice{background:#fff9e7;border-left:4px solid #c99429;padding:14px 18px;margin:0 0 22px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;border:1px solid #dae2df;border-radius:10px;padding:22px;min-width:0}.outcome{border-top:4px solid #176c63}.tag{display:inline-block;background:#e8f3ef;border-radius:4px;padding:3px 8px;font-size:12px;font-weight:650}.decision{display:block;font-size:clamp(17px,2.1vw,23px);line-height:1.45;overflow-wrap:anywhere;margin:16px 0 20px;font-weight:750}dl{margin:0}dl>div{display:flex;justify-content:space-between;gap:18px;border-top:1px solid #e4ebe8;padding:10px 0}dt{font-size:14px;max-width:70%}dd{margin:0;text-align:right;font-family:ui-monospace,monospace;font-size:14px}code,pre{font-family:ui-monospace,monospace;font-size:13px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f4;border-radius:6px;padding:13px;line-height:1.55}li{margin:7px 0;overflow-wrap:anywhere}.command{background:#17333e;color:#edf8f4}details{margin-top:16px}summary{cursor:pointer;font-size:14px;font-weight:650}details pre{max-height:440px;overflow:auto}.hash{overflow-wrap:anywhere}.section{margin-top:22px}.links{display:flex;flex-wrap:wrap;gap:16px}.small{font-size:13px}footer{border-top:1px solid #ccd9d4;margin-top:28px;padding:20px 0;font-size:14px}#purpose{margin:6px 0 18px;max-width:850px}#selection-status{margin:0}.raw{margin-top:18px}
@media(max-width:720px){main{padding:16px}.grid,.chooser{grid-template-columns:1fr}.card{padding:18px}header{padding:28px 20px}dl>div{gap:10px}dt{max-width:65%}}
</style></head><body>
<header><div class="eyebrow">SYNTHETIC SOFTWARE EXAMPLES</div>
<h1>When an apparent rescue is misleading</h1>
<p>Inspect three existing fixtures and their recorded Python decisions. The tool makes supplied decision rules inspectable; these examples contain no drug results or experimental evidence.</p></header>
<main>
<div class="notice"><strong>Recorded results viewer.</strong> Choosing a case changes the displayed record. It does not execute the algorithm. The replay script below reruns the real <code>decision.py</code>.</div>
<p id="selection-status" class="subtle" role="status" aria-live="polite">Choose an existing synthetic fixture.</p>
<nav class="chooser" aria-label="Choose a synthetic fixture" id="choices"></nav>
<section aria-labelledby="case-title"><h2 id="case-title"></h2><p id="purpose"></p>
<div class="grid">
<article class="card"><h3>Input evidence · supplied</h3><dl id="evidence"></dl>
<p class="subtle">Intervals use absolute probability units; protein is a ratio. The 95% intervals, thresholds, counts and qualification flags are illustrative inputs. This code neither fits the intervals from the counts nor authenticates the referenced records.</p>
<a id="input-link">Open source fixture JSON</a>
<details><summary>Complete input · exact source text</summary><pre id="input-json"></pre></details></article>
<article class="card outcome"><span class="tag">Actual recorded Python output</span>
<code class="decision" id="decision"></code>
<h3>Reason codes returned by Python</h3><ul id="reasons"></ul>
<p>Replication candidate IDs: <code id="candidates"></code></p>
<p class="subtle" id="validity"></p>
<details open><summary>Criteria returned by Python</summary><pre id="criteria"></pre></details>
<details><summary>Complete output · exact captured stdout</summary><pre id="output-json"></pre></details>
</article></div></section>
<section class="card section" aria-labelledby="rerun-title"><h2 id="rerun-title">Rerun this fixture</h2>
<p>From the repository root, with Python 3.9+ and its standard library:</p><pre class="command" id="command"></pre>
<p class="small">This terminal command executes Python. Exit 0 means structurally valid input, including a negative or indeterminate decision.</p>
<div class="links"><a href="../../analysis/rescue_decision/decision.py">Decision implementation</a><a href="../../analysis/rescue_decision/README.md">Schema and interpretation limits</a><a href="replay-results.json">Portable replay receipts</a><a href="README.md">Replay instructions</a></div>
<details><summary>Exact-byte provenance · SHA256</summary><div id="provenance" class="small hash"></div>
<p class="subtle">These are recorded hashes, not a browser verification or an external signature. The offline verification command checks current source bytes, reruns all three fixtures and checks this HTML against the receipts.</p></details>
<p class="small">Verify the saved demo and rerun all three cases:</p><pre class="command">python3 -B -S examples/rescue-decision-demo/replay.py --verify</pre>
</section>
<footer><strong>Scope:</strong> Three materializations from the existing frozen casebook, not three new independent validation cases. No clinical benefit, N1002K defect, causal mechanism or treatment recommendation is established. The strongest possible prototype output concerns eligibility for independent research replication.</footer>
<noscript><p>This offline viewer needs JavaScript to select a recorded case. Read <a href="replay-results.json">the receipts</a> or rerun Python using <a href="README.md">the README</a>.</p></noscript>
</main><script id="replay-data" type="application/json">__REPLAY_DATA__</script>
<script>
'use strict';
const receipt=JSON.parse(document.getElementById('replay-data').textContent);
const $=id=>document.getElementById(id);
const element=(tag,text)=>{const node=document.createElement(tag);node.textContent=text;return node};
function selectCase(index){
  const record=receipt.cases[index], input=JSON.parse(record.input_text), output=JSON.parse(record.stdout_text);
  const contrast=input.contrasts[0], result=output.contrasts[0];
  $('case-title').textContent=record.title;
  $('purpose').textContent=record.purpose;
  $('selection-status').textContent='Recorded case '+(index+1)+' of '+receipt.cases.length+' · selection does not run Python';
  document.querySelectorAll('[data-case]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.case)===index)));
  $('evidence').replaceChildren();
  const fields=[
    ['Protein ratio',contrast.assays.protein_ratio],
    ['Normal-survivor fraction change',contrast.assays.survivor_normal_fraction_change],
    ['Supplied functional-benefit CI',contrast.analysis.benefit_ci],
    ['Illustrative worthwhile-benefit threshold',input.plan.smallest_worthwhile_reduction],
    ['Supplied excess-death CI',contrast.fate.excess_death_ci],
    ['Illustrative maximum excess death',input.plan.fate_bounds.maximum_excess_death],
    ['Exposure measurement qualified',contrast.exposure.measurement_qualified],
    ['Within qualified exposure window',contrast.exposure.within_qualified_window],
    ['Supplied selection assessment',contrast.fate.selection_assessment]
  ];
  for(const [label,value] of fields){const row=element('div','');row.append(element('dt',label),element('dd',JSON.stringify(value)));$('evidence').append(row)}
  $('input-link').href=record.id+'.json';
  $('input-link').textContent='Source: '+record.id+'.json';
  $('input-json').textContent=record.input_text;
  $('output-json').textContent=record.stdout_text;
  $('decision').textContent=result.decision;
  $('reasons').replaceChildren(...result.reason_codes.map(code=>element('li',code)));
  $('candidates').textContent=JSON.stringify(output.replication_candidate_ids);
  $('criteria').textContent=JSON.stringify(result.criteria,null,2);
  $('validity').textContent='Recorded input_valid: '+JSON.stringify(output.input_valid)+' · process exit: '+record.exit_code;
  $('command').textContent=record.command;
  $('provenance').replaceChildren();
  for(const [label,hash] of [['Input file',record.input_sha256],['Decision implementation',record.implementation_sha256],['Captured stdout',record.stdout_sha256],['Replay generator',receipt.source_hashes['examples/rescue-decision-demo/replay.py']]]){
    const p=element('p',label+' SHA256: ');p.append(element('code',hash));$('provenance').append(p)
  }
}
receipt.cases.forEach((record,index)=>{const button=element('button',(index+1)+'. '+record.title);button.type='button';button.dataset.case=String(index);button.setAttribute('aria-pressed','false');button.addEventListener('click',()=>selectCase(index));$('choices').append(button)});
selectCase(0);
</script></body></html>
'''


def render(bundle):
    # Escape script delimiters; all displayed source content uses textContent.
    data = json.dumps(bundle, ensure_ascii=True, separators=(",", ":"))
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return HTML.replace("__REPLAY_DATA__", data).encode("utf-8")


def write_atomic(path, data):
    pending = path.with_suffix(path.suffix + ".pending")
    pending.write_bytes(data)
    os.replace(pending, path)


def generate(root=ROOT):
    bundle = collect(root)
    write_atomic(root / DEMO / "replay-results.json",
                 (json.dumps(bundle, indent=2, ensure_ascii=True) + "\n").encode("utf-8"))
    write_atomic(root / DEMO / "replay.html", render(bundle))
    return bundle


def verify(root=ROOT):
    """Detect changed sources before execution, then compare exact rerun outputs."""
    bundle = json.loads((root / DEMO / "replay-results.json").read_bytes())
    current = source_hashes(root)
    require(bundle.get("source_hashes") == current,
            "Source SHA256 mismatch: input, implementation, schema, generator or original receipt changed")
    for case in bundle.get("cases", []):
        require(digest(case["input_text"].encode("utf-8")) == case["input_sha256"],
                f"{case['id']}: embedded input SHA256 mismatch")
        require(digest(case["stdout_text"].encode("utf-8")) == case["stdout_sha256"],
                f"{case['id']}: captured stdout SHA256 mismatch")
    rerun = collect(root)
    require(bundle == rerun, "Receipt mismatch against actual decision.py rerun")
    require((root / DEMO / "replay.html").read_bytes() == render(bundle),
            "HTML mismatch against receipts and current renderer")
    return bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true", help="Rerun real code and replace the two generated demo files")
    mode.add_argument("--verify", action="store_true", help="Check hashes, rerun real code, compare exact outputs and HTML; no writes")
    args = parser.parse_args(argv)
    try:
        bundle = generate() if args.generate else verify()
    except (ReplayError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"Replay failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"mode": "generated" if args.generate else "verified",
                      "fixtures": len(bundle["cases"]),
                      "decisions": [json.loads(case["stdout_text"])["contrasts"][0]["decision"]
                                    for case in bundle["cases"]],
                      "replication_candidate_ids": []}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
