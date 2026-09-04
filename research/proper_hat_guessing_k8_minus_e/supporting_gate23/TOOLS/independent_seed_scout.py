#!/usr/bin/env python3
"""Independent geometry/matching check of the 2000 seeded rules.
Requires independent_audit.py in the same directory.
First compile and run emit_seeded_rules.cpp to produce binary guesses.
"""
from __future__ import annotations
import argparse,csv,json,time
from pathlib import Path
from collections import Counter
import numpy as np
from independent_audit import Geometry,checked_matching,read_tsv,require

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('package',type=Path);ap.add_argument('binary_rules',type=Path)
    ap.add_argument('--out',type=Path,default=Path('.'))
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);t0=time.monotonic()
    data=np.fromfile(a.binary_rules,dtype=np.uint8).reshape(-1,990,2)
    g=Geometry();out=[]
    frozen=read_tsv(a.package/'DATA/bad_rules_23_combined.tsv')
    for r in frozen:
        require(tuple(data[int(r['seed'])-1,int(r['tail_id'])])==(int(r['alpha']),int(r['beta'])),'seed generator mismatch')
    print('Seed stream matches frozen rule tables; independent matching reconstruction starts',flush=True)
    for i,rules in enumerate(data):
        # Validate every sampled guess, not just the frozen bad tables.
        require(all(x!=y and x in av and y in av for (x,y),av in zip(rules,g.available)),'illegal guess')
        eq,off=g.masks(rules)
        missing=int((np.bincount(g.eq_edges[eq].ravel(),minlength=5940)==0).sum())
        em,_=checked_matching(g.eq_edges[eq],5940);om,_=checked_matching(g.off_edges[off],47520)
        de=5940-int((em>=0).sum());do=42570-int((om>=0).sum())
        require(de==missing and do==0,f'seed {i+1}: asserted mechanism failed')
        if de or do or missing:
            out.append({'seed':i+1,'missing_eq_right':missing,'def_eq':de,'def_off':do,'def_full':de+do})
        if (i+1)%250==0:print('Independently checked',i+1,'seeds',flush=True)
    expected=[{k:int(v) for k,v in r.items()} for r in read_tsv(a.package/'DATA/extended_2000_failures.tsv')]
    require(out==expected,'extended table discrepancy')
    with (a.out/'independent_2000_failures.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['seed','missing_eq_right','def_eq','def_off','def_full'],delimiter='\t');w.writeheader();w.writerows(out)
    res={'seeds':len(data),'perfect':len(data)-len(out),'deficient':len(out),
         'deficiency_histogram':dict(Counter(r['def_full'] for r in out)),
         'off_diagonal_deficiencies':0,'mismatches':0,
         'two_missing_view_seeds':[r['seed'] for r in out if r['def_full']==2],
         'all_matching_edges_explicitly_checked':True,'elapsed_seconds':time.monotonic()-t0}
    (a.out/'independent_2000_summary.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))

if __name__=='__main__':main()
