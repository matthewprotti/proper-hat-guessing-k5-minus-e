#!/usr/bin/env python3
"""Focused one-command integrity and mathematical verification for K5-e."""
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PY=sys.executable

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20), b''): h.update(chunk)
    return h.hexdigest()

def fail(msg): raise SystemExit('FAIL: '+msg)

def manifest_check():
    m=ROOT/'MANIFEST.sha256'
    expected={}
    for i,line in enumerate(m.read_text().splitlines(),1):
        if not line.strip(): continue
        try:digest,rel=line.split('  ',1)
        except ValueError: fail(f'malformed manifest line {i}')
        p=Path(rel)
        if p.is_absolute() or '..' in p.parts or rel in expected: fail(f'unsafe/duplicate path {rel!r}')
        if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest): fail(f'bad digest line {i}')
        expected[rel]=digest
    actual={
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob('*')
        if p.is_file()
        and p.name!='MANIFEST.sha256'
        and '.git' not in p.relative_to(ROOT).parts
    }
    if set(expected)!=actual: fail(f'manifest set mismatch missing={sorted(set(expected)-actual)[:5]} extra={sorted(actual-set(expected))[:5]}')
    for rel,d in expected.items():
        if sha(ROOT/rel)!=d: fail(f'hash mismatch {rel}')
    return len(expected)

def run(label,args,expect=True):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
    if expect and p.returncode: fail(f'{label} failed\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}')
    if not expect and p.returncode==0: fail(f'negative control {label} was accepted')
    return p

def same(label,a,b):
    if a.read_bytes()!=b.read_bytes(): fail(f'{label} differs')

def main():
    n=manifest_check()
    with tempfile.TemporaryDirectory(prefix='k5e-verify-') as td:
        t=Path(td)
        regen=t/'regen'
        run('regenerate exact CNF',[PY,'code/generate_instance.py','K5-e','8','--outdir',str(regen),'--symmetry-break'])
        for name in ('K5_e_q8_sb.cnf','K5_e_q8_sb.map.json','K5_e_q8_sb.meta.json'):
            same('regenerated '+name,regen/name,ROOT/'instances'/name)
        strat=t/'strategy.json'; match=t/'matching.json'; rep=t/'fano.json'
        run('Fano/Hall constructor',[PY,'code/verify_k5e_fano_hall.py','certificates/K5_e_q8_fano_delta.json','--strategy-output',str(strat),'--matching-output',str(match),'--report',str(rep)])
        same('strategy',strat,ROOT/'certificates/K5_e_q8_fano_strategy.json')
        same('matching',match,ROOT/'certificates/K5_e_q8_fano_matching.json')
        same('Fano report',rep,ROOT/'results/K5_e_q8_fano_verification.json')
        bad=json.loads((ROOT/'certificates/K5_e_q8_fano_delta.json').read_text()); bad['delta_by_normal'][0]['delta']=2
        bp=t/'bad.json'; bp.write_text(json.dumps(bad))
        run('corrupted delta',[PY,'code/verify_k5e_fano_hall.py',str(bp)],expect=False)
        p=run('pinned game checker',[PY,'code/verify_k5e_q8_pinned.py','certificates/K5_e_q8_fano_strategy.json'])
        if json.loads(p.stdout)['proper_colorings_checked']!=8400: fail('pinned checker count')
        run('generic game checker',[PY,'code/verify_strategy.py','certificates/K5_e_q8_fano_strategy.json'])
        cr=t/'cnf.json'
        run('CNF assignment checker',[PY,'code/verify_cnf_assignment.py','instances/K5_e_q8_sb.cnf','instances/K5_e_q8_sb.map.json','certificates/K5_e_q8_fano_strategy.json','--report',str(cr)])
        same('CNF report',cr,ROOT/'results/K5_e_q8_fano_cnf_verification.json')
        mr=t/'matching_report.json'; ms=t/'matching_strategy.json'
        run('matching checker',[PY,'code/verify_k5e_residual_matching.py','certificates/K5_e_q8_fano_matching.json','--strategy-output',str(ms),'--report',str(mr)])
        same('matching report',mr,ROOT/'results/K5_e_q8_fano_matching_verification.json')
        run('matching strategy checker',[PY,'code/verify_strategy.py',str(ms)])
        run('q=7 positive control',[PY,'code/verify_strategy.py','controls/K5_e_q7_strategy.json'])
    print(f'PASS: {n} frozen files matched MANIFEST.sha256')
    print('PASS: HG_P(K5-e)=8 construction checked on all 8,400 proper colourings')
    print('PASS: Fano lemma, Hall matching, direct witness, and 62,161-clause CNF agree')
    return 0
if __name__=='__main__': raise SystemExit(main())
