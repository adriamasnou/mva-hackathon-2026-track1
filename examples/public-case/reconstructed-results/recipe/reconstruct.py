#!/usr/bin/env python3
"""Prepare NEW public FGFR2 jobs and a verified HG002 spike-in; never run inference."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BACKGROUND_SHA256 = 'adb4d4a50048aa13353a06b84fcfcbca09a5d17525efaa4cea44f8822e81175c'
HISTORICAL_SHA256 = 'b31aaad49f8af6ad8522df5931fccc141152f13b8ad6e823f5807ad90e71f745'
TEMPLATE_SHA256 = '50f83311418ed0e3276ccf0dfdf8766b8b0b5241b7cbc417e9e730a6f1ad31e4'
BACKGROUND_RECORDS = 4048342
SOURCE_URL = ('https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/'
              'AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/'
              'HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz')
SPIKE = ('chr10\t121517378\t.\tC\tT\t500\tPASS\t.\tGT:PS:DP:ADALL:AD:GQ\t'
         '0/1:.:93:2,56:2,38:99\n')
SPIKE_KEY = ('chr10', '121517378', 'C', 'T', '0/1')


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def batch_line(path):
    """BatchFileReader splits on whitespace; it does not interpret shell quotes."""
    value = str(path)
    if not value or any(c.isspace() or c in "\"'" for c in value):
        raise ValueError('Exomiser batch job paths must contain no whitespace or quotes')
    return '--analysis ' + value


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def header(path):
    with gzip.open(path, 'rt') as stream:
        lines = []
        for line in stream:
            if not line.startswith('#'):
                break
            lines.append(line)
    if not lines or lines[-1].rstrip().split('\t')[9:] != ['HG002']:
        raise ValueError('Expected the single public HG002 sample')
    return lines


def records(path):
    with gzip.open(path, 'rt') as stream:
        for line in stream:
            if not line.startswith('#'):
                yield line


def allele_gt(line):
    fields = line.rstrip('\n').split('\t')
    if len(fields) != 10:
        raise ValueError('Expected one-sample VCF record')
    gt = fields[9].split(':')[fields[8].split(':').index('GT')]
    return fields[0], fields[1], fields[3], fields[4], gt


def audit_background(source, spiked):
    """Require every background coordinate/REF/ALT/phased-GT string to be unchanged."""
    source_header = header(source)
    if source_header[-1] != header(spiked)[-1]:
        raise ValueError('Sample columns changed')
    contigs = [re.match(r'##contig=<ID=([^,>]+)', line).group(1)
               for line in source_header if line.startswith('##contig=<ID=')]
    order = {name: i for i, name in enumerate(contigs)}
    previous = (-1, -1)
    original = iter(records(source))
    count = inserted = different_lines = 0
    keys = hashlib.sha256()
    for line in records(spiked):
        key = allele_gt(line)
        position = (order[key[0]], int(key[1]))
        if position < previous:
            raise ValueError('Spike-in input is not coordinate sorted')
        previous = position
        if key == SPIKE_KEY:
            if line != SPIKE:
                raise ValueError('Spike FORMAT/QUAL or synthetic values changed')
            inserted += 1
            continue
        expected = next(original, None)
        if expected is None or allele_gt(expected) != key:
            raise ValueError(f'Background coordinate/REF/ALT/GT changed at row {count + 1}')
        different_lines += expected != line
        keys.update(('\t'.join(key) + '\n').encode())
        count += 1
    if next(original, None) is not None or count != BACKGROUND_RECORDS or inserted != 1:
        raise ValueError('Wrong background count or spike multiplicity')
    return {'background_records': count, 'inserted_records': inserted,
            'total_records': count + inserted, 'all_background_coordinate_ref_alt_gt_equal': True,
            'background_record_lines_differing': different_lines,
            'scope': 'Ordered coordinate, REF, ALT and literal phased GT. Header and other FORMAT '
                     'bytes may change, including omitted trailing PS becoming a dot.',
            'background_coordinate_ref_alt_gt_sha256': keys.hexdigest()}


def compare_historical(rebuilt, historical):
    """Semantic comparison deliberately excludes old headers and non-GT FORMAT fields."""
    if sha(historical) != HISTORICAL_SHA256:
        raise ValueError('Historical input hash does not match the retained public fixture')
    old = iter(records(historical))
    count = 0
    digest = hashlib.sha256()
    for line in records(rebuilt):
        other = next(old, None)
        key = allele_gt(line)
        if other is None or allele_gt(other) != key:
            raise ValueError(f'Historical coordinate/REF/ALT/GT mismatch at row {count + 1}')
        digest.update(('\t'.join(key) + '\n').encode())
        count += 1
    if next(old, None) is not None:
        raise ValueError('Historical file has extra records')
    return {'historical_sha256': HISTORICAL_SHA256, 'records': count,
            'coordinate_ref_alt_gt_sha256': digest.hexdigest(), 'all_equal': True,
            'scope': 'Ordered coordinate, REF, ALT and literal phased GT; not other fields or headers.'}


def build_genome(background, output, commands):
    lines = header(background)
    contigs = [re.match(r'##contig=<ID=([^,>]+)', line).group(1)
               for line in lines if line.startswith('##contig=<ID=')]
    order = {name: i for i, name in enumerate(contigs)}
    target = (order['chr10'], 121517378)
    command = ['bcftools', 'view', '--no-version', '-Oz', '-']
    commands.append({'argv': command, 'stdin': 'Unchanged background rows with one sorted spike',
                     'stdout': str(output), 'stderr': str(output.parent / 'bcftools.log')})
    # Stream directly into BGZF: no uncompressed genome, concat copy or sort scratch file.
    with output.open('xb') as out, (output.parent / 'bcftools.log').open('xb') as log:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=log)
        try:
            for line in lines[:-1]:
                process.stdin.write(line.encode())
            process.stdin.write(b'##source=FGFR2_reconstruction_synthetic_spike_read_support_not_measurements\n')
            process.stdin.write(lines[-1].encode())
            inserted = False
            previous = (-1, -1)
            for line in records(background):
                chrom, pos = line.split('\t', 2)[:2]
                position = (order[chrom], int(pos))
                if position < previous:
                    raise ValueError('Public background is not coordinate sorted')
                if position == target:
                    raise ValueError('Spike position already present; refusing to replace any background')
                if not inserted and position > target:
                    process.stdin.write(SPIKE.encode())
                    inserted = True
                process.stdin.write(line.encode())
                previous = position
            if not inserted:
                process.stdin.write(SPIKE.encode())
            process.stdin.close()
            if process.wait() != 0:
                raise RuntimeError('bcftools failed; see retained bcftools.log')
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    command = ['bcftools', 'index', '--csi', str(output)]
    commands.append({'argv': command})
    subprocess.run(command, check=True)


def prepare(background, out, data_dir, historical=None, reuse_genome=None):
    import yaml

    # Validate before hashing the genome or creating any output.
    batch_lines = [batch_line(out / 'jobs' / (case + '.yml')) for case in ('mini', 'genome')]
    if out.exists():
        raise FileExistsError('Choose a NEW output directory; partial runs are retained too')
    if sha(background) != BACKGROUND_SHA256:
        raise ValueError('Only the exact pinned public HG002 background is accepted')
    if sha(ROOT / 'job-template.yml') != TEMPLATE_SHA256:
        raise ValueError('Reconstruction template changed; review before making a new protocol')
    if any(c in str(data_dir) for c in '\n\r\\'):
        raise ValueError('Data-directory path is not safe for this Java properties recipe')
    version = subprocess.run(['bcftools', '--version'], capture_output=True, text=True, check=True).stdout
    out.mkdir(parents=True)
    commands = []
    try:
        inputs = out / 'inputs'
        mini, unused_job = load_module('public_case_prepare', ROOT / 'prepare.py').prepare(inputs)
        genome = reuse_genome or inputs / 'HG002_spiked.vcf.gz'
        if not reuse_genome:
            build_genome(background, genome, commands)
        audit = audit_background(background, genome)
        if historical:
            audit['historical_semantic_comparison'] = compare_historical(genome, historical)
        (out / 'jobs').mkdir()
        jobs = []
        for case, vcf, sample in [('mini', mini, 'smoke'), ('genome', genome, 'HG002')]:
            job = yaml.safe_load((ROOT / 'job-template.yml').read_text())
            job['phenopacket']['id'] = case
            job['phenopacket']['subject']['id'] = sample
            job['phenopacket']['htsFiles'][0]['uri'] = str(vcf)
            job['outputOptions'].update(outputDirectory=str(out / 'results'), outputFileName=case)
            path = out / 'jobs' / (case + '.yml')
            with path.open('x') as stream:
                yaml.safe_dump(job, stream, sort_keys=False)
            jobs.append({'case_id': case, 'gene': 'FGFR2', 'stratum': 'constructed_FGFR2_known_variant',
                         'arm': 'original', 'primary_autosomal': False, 'vcf': str(vcf),
                         'vcf_sha256': sha(vcf), 'job': str(path), 'job_sha256': sha(path),
                         'result_jsonl': str(out / 'results' / (case + '.jsonl'))})
        write_json(out / 'jobs-manifest.json', jobs)
        with (out / 'batch.txt').open('x') as stream:
            stream.writelines(line + '\n' for line in batch_lines)
        with (out / 'runtime.properties').open('x') as stream:
            stream.write(f'exomiser.data-directory={data_dir}\n'
                         'exomiser.hg38.data-version=2512\nexomiser.phenotype.data-version=2512\n'
                         'spring.cache.type=caffeine\nspring.cache.caffeine.spec=maximumSize=60000\n'
                         'logging.level.com.zaxxer.hikari=ERROR\n')
        write_json(out / 'protocol-before-inference.json', {
            'recorded_utc': datetime.now(timezone.utc).isoformat(), 'results_seen': False,
            'purpose': 'NEW FGFR2 reconstructed execution controls; August YAML was not recovered.',
            'template_sha256': TEMPLATE_SHA256, 'exomiser_version': '15.1.0',
            'data_versions': {'hg38': '2512', 'phenotype': '2512'},
            'limits': ['Known FGFR2 alleles and specific HPO terms; not blinded diagnostic accuracy.',
                       'ClinVar whitelist setting is left at runtime default, as in the queued FGFR2 jobs.',
                       'Synthetic spike QUAL/DP/ADALL/AD/GQ values are fixture fields, not measurements.',
                       'VCF compression/header bytes may differ from August despite equivalent alleles/GT.']})
        write_json(out / 'preparation-receipt.json', {
            'status': 'prepared_not_executed', 'created_utc': datetime.now(timezone.utc).isoformat(),
            'invocation': sys.argv, 'bcftools_version': version, 'pyyaml_version': yaml.__version__,
            'source_url': SOURCE_URL, 'background': str(background), 'background_sha256': BACKGROUND_SHA256,
            'genome': str(genome), 'genome_sha256': sha(genome),
            'genome_preparation': 'Reused after full semantic verification' if reuse_genome else 'Streamed rebuild',
            'spike_vcf_record': SPIKE.rstrip('\n'), 'spike_values_are_synthetic': True,
            'verification': audit, 'commands': commands,
            'recipe_sha256': {p.name: sha(p) for p in [Path(__file__), ROOT / 'prepare.py',
                              ROOT / 'job-template.yml', ROOT / 'clinvar-smoke-variants.tsv']},
            'file_sha256': {str(p.relative_to(out)): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}})
    except Exception as error:
        write_json(out / 'preparation-failed.json', {'error': str(error), 'commands': commands,
                                                   'instruction': 'Retained partial work; use a new destination.'})
        raise
    return out / 'preparation-receipt.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--background', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--data-dir', type=Path, required=True, help='Bundle location; no inference or DB read')
    parser.add_argument('--historical-genome', type=Path, help='Optional retained public fixture to compare, read-only')
    parser.add_argument('--reuse-genome', type=Path, help='Avoid a redundant copy: verify and reference an existing public spike-in')
    args = parser.parse_args()
    print(prepare(args.background.resolve(), args.out.resolve(), args.data_dir.resolve(),
                  args.historical_genome.resolve() if args.historical_genome else None,
                  args.reuse_genome.resolve() if args.reuse_genome else None))
