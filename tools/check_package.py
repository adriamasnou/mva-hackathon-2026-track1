#!/usr/bin/env python3
"""Offline package checks: files, internal links and machine-readable public evidence."""
import argparse,csv,hashlib,json,re,sys,zipfile
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['README.md','submissions/adriamasnou_track2_report.md','submissions/adriamasnou_track2_report.pdf','submissions/adriamasnou_methods_description.xlsx','submissions/notes-for-judges.md','submissions/pgtm-navigator.html','submissions/pitch/pitch-narrated.mp4','submissions/pitch/pitch-silent.mp4','submissions/pitch/pitch-editable.pptx','submissions/pitch/pitch-captions.srt','submissions/pitch-video-script.md','canary/measured-results-2026-10-23.txt']
def provenance_errors(root):
 errors=[]
 crosswalk=root/'submissions/hfea-pgtm-gene-crosswalk.csv'
 coverage=root/'submissions/expert-coverage.json'
 if not crosswalk.is_file() or not coverage.is_file():
  return ['Missing crosswalk or coverage provenance']
 sources=json.loads(coverage.read_text()).get('sources',[])
 matching=[s for s in sources if s.get('file')==crosswalk.name]
 if len(matching)!=1 or matching[0].get('sha256')!=hashlib.sha256(crosswalk.read_bytes()).hexdigest():
  errors.append('Coverage provenance does not match the shipped crosswalk')
 return errors
def check(root):
 errors=[]
 errors.extend(provenance_errors(root))
 for name in REQUIRED:
  p=root/name
  if not p.is_file() or not p.stat().st_size:errors.append('Missing/empty required file: '+name)
 for p in root.rglob('*.md'):
  if '.git' in p.parts:continue
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
   target=target.strip('<>');u=urlsplit(target)
   if u.scheme or target.startswith('#') or not u.path:continue
   dest=(p.parent/unquote(u.path)).resolve()
   if not dest.is_relative_to(root.resolve()) or not dest.exists():errors.append(f'Broken/internal link: {p.relative_to(root)} -> {target}')
 notes=(root/'submissions/notes-for-judges.md').read_text().split('\n',2)[-1]
 if len(notes.split())>150:errors.append('Notes exceed 150 words')
 for name in ['submissions/adriamasnou_methods_description.xlsx','submissions/pitch/pitch-editable.pptx']:
  if (root/name).exists():
   with zipfile.ZipFile(root/name) as z:
    bad=z.testzip()
    if bad:errors.append('Corrupt Office member: '+bad)
 timing=json.loads((root/'submissions/pitch/timing.json').read_text())
 if len(timing)!=6 or timing[-1]['end_seconds']>=180:errors.append('Invalid pitch timeline')
 for p in root.rglob('*'):
  if '.git' in p.parts or not p.is_file():continue
  if p.name.endswith(('.vcf','.vcf.gz','.cram','.bam','.fastq','.fastq.gz','.fasta','.fna')):errors.append('Unexpected genomic input in delivery: '+str(p.relative_to(root)))
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);a=p.parse_args();errors=check(a.root)
 for e in errors:print('FAIL:',e)
 print(f'Package check: {len(errors)} failure(s)');sys.exit(bool(errors))
