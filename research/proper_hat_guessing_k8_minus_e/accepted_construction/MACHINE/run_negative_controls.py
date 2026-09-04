#!/usr/bin/env python3
"""Mutation controls for the data-only K8-e verifier."""
from __future__ import annotations
import argparse, shutil, subprocess, sys, tempfile
from pathlib import Path

def run(verifier:Path, root:Path)->int:
    return subprocess.run([sys.executable,'-B',str(verifier),str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode

def mutate_line(path:Path, index:int, transform):
    lines=path.read_text().splitlines()
    lines[index]=transform(lines[index])
    path.write_text('\n'.join(lines)+'\n')

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('package_root',type=Path);a=ap.parse_args()
    root=a.package_root.resolve(); verifier=root/'MACHINE/verify_k8e_orbits.py'; cert=root/'CERTIFICATES'
    if run(verifier,cert)!=0: raise SystemExit('baseline verifier failed')
    results={}
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)/'cert';shutil.copytree(cert,t)
        # Break the compact twin formula and legality at the first row.
        def bad_twin(line):
            z=line.split('\t');z[3]=z[0];return '\t'.join(z)
        mutate_line(t/'K8_e_q14_twin_rules.tsv',1,bad_twin)
        results['corrupt_twin_rule_rejected']=run(verifier,t)!=0
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)/'cert';shutil.copytree(cert,t)
        # Force a clique rule to guess a visibly occupied normalized color.
        def bad_clique(line):
            z=line.split('\t');z[6]=z[2];return '\t'.join(z)
        mutate_line(t/'K8_e_q14_clique_rules.tsv',1,bad_clique)
        results['illegal_clique_guess_rejected']=run(verifier,t)!=0
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)/'cert';shutil.copytree(cert,t)
        p=t/'K8_e_q14_residual_orbit_matching.tsv';lines=p.read_text().splitlines();p.write_text('\n'.join(lines[:-1])+'\n')
        results['truncated_matching_rejected']=run(verifier,t)!=0
    for k,v in results.items():print(f'{k}={"PASS" if v else "FAIL"}')
    if not all(results.values()):return 1
    print('negative_controls=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
