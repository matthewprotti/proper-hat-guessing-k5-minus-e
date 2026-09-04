#!/usr/bin/env python3
"""Read-only package verifier for the K8-e theorem candidate."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
CERT=ROOT/'CERTIFICATES'
EXPECTED={
 'K8_e_q14_twin_rules.tsv':'6a9ee969be6f7ae217d6b103d03b117cb2b56142df9b5c2fab4c2084c8cc849d',
 'K8_e_q14_clique_rules.tsv':'c899e85b4e52825509baf8e00572555f713e27f881be2800ad8a4371f4b37acb',
 'K8_e_q14_residual_orbit_matching.tsv':'b739d1fecabfce888a7cd25f3ed0da1c329c0f29ffb772283ff99b8dd61a8982',
}
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def fail(msg): raise SystemExit('FAIL: '+msg)
def run(cmd,**kw):
 p=subprocess.run(cmd,text=True,capture_output=True,**kw)
 if p.returncode: fail(f"command failed {cmd}\nstdout:\n{p.stdout}\nstderr:\n{p.stderr}")
 return p.stdout
def manifest_check():
 expected={}
 for no,line in enumerate((ROOT/'MANIFEST.sha256').read_text().splitlines(),1):
  if not line.strip():continue
  try:d,rel=line.split('  ',1)
  except ValueError:fail(f'bad manifest line {no}')
  pp=PurePosixPath(rel)
  if pp.is_absolute() or '..' in pp.parts or '.' in pp.parts or '\\' in rel or rel in expected:fail(f'unsafe/duplicate path {rel!r}')
  if len(d)!=64 or any(c not in '0123456789abcdef' for c in d):fail(f'bad digest line {no}')
  expected[rel]=d
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256' and '__pycache__' not in p.parts}
 if set(expected)!=actual:fail(f'manifest inventory mismatch missing={sorted(set(expected)-actual)} extra={sorted(actual-set(expected))}')
 for rel,d in expected.items():
  if sha(ROOT/rel)!=d:fail(f'manifest hash mismatch {rel}')
 print(f'manifest_files={len(expected)} PASS')
def compile_cpp(src:Path,out:Path):
 cxx=shutil.which('g++')
 if not cxx:fail('g++ not found')
 run([cxx,'-O3','-std=c++20',str(src),'-o',str(out)])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--negative-controls',action='store_true');a=ap.parse_args()
 manifest_check()
 for name,d in EXPECTED.items():
  if sha(CERT/name)!=d:fail(f'locked certificate hash mismatch {name}')
 with tempfile.TemporaryDirectory(prefix='k8e_verify_') as td:
  t=Path(td);builder=t/'builder';regen=t/'regen';regen.mkdir()
  compile_cpp(ROOT/'MACHINE/build_k8e_strategy.cpp',builder)
  out=run([str(builder),str(regen)])
  if 'FOUND K8-e q=14 PGL-equivariant strategy' not in out:fail('builder did not report construction')
  for name,d in EXPECTED.items():
   if sha(regen/name)!=d:fail(f'generated certificate mismatch {name}')
  sealed=json.loads((ROOT/'RESULTS/builder_summary.json').read_text());fresh=json.loads((regen/'summary.json').read_text())
  if sealed!=fresh:fail('builder summary mismatch')
  orbit_text=run([sys.executable,'-B',str(ROOT/'MACHINE/verify_k8e_orbits.py'),str(CERT)])
  orbit=json.loads(orbit_text)
  if not orbit.get('verified') or orbit.get('coverage_failures')!=0 or orbit.get('matching_size')!=48510:fail('orbit verifier result mismatch')
  fullbin=t/'fullverify';compile_cpp(ROOT/'MACHINE/verify_k8e_all_colourings.cpp',fullbin)
  full=json.loads(run([str(fullbin),str(CERT)]))
  if not full.get('verified') or full.get('proper_colourings_checked')!=138378240 or full.get('coverage_failures')!=0:fail('full-colouring verifier mismatch')
  print('builder_regeneration=PASS')
  print('orbit_and_matching_verification=PASS')
  print('full_138378240_colouring_verification=PASS')
 if a.negative_controls:
  out=run([sys.executable,'-B',str(ROOT/'MACHINE/run_negative_controls.py'),str(ROOT)])
  print(out,end='')
 print('claim_candidate=HG_P(K8-e)=14')
 print('review_status=INDEPENDENT_ADVERSARIAL_REVIEW_PENDING')
 print('K8E_PACKAGE_VERIFICATION=PASS')
if __name__=='__main__':main()
