#!/usr/bin/env python3
"""Pinned, dependency-free verifier for a K5-e q=8 twin+matching certificate."""
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path);ap.add_argument('--strategy-output',type=Path);ap.add_argument('--report',type=Path);a=ap.parse_args()
 raw=a.certificate.read_bytes();obj=json.loads(raw)
 q=8;n=5;edges=[(u,v) for u in range(n) for v in range(u+1,n) if (u,v)!=(0,1)]
 N=[tuple(w for w in range(n) if w!=v and (min(v,w),max(v,w)) in edges) for v in range(n)]
 proper=[]
 for T in itertools.permutations(range(q),3):
  R=[x for x in range(q) if x not in T]
  for aa in R:
   for bb in R:proper.append((aa,bb,*T))
 # Pin metadata rather than trusting it.
 errors=[]
 if obj.get('graph')!='K5-e' or obj.get('q')!=q:errors.append('wrong graph/q metadata')
 if obj.get('edges')!=[list(e) for e in edges]:errors.append('wrong edge metadata')
 if obj.get('neighbor_order')!=[list(x) for x in N]:errors.append('wrong neighbor order')
 twin={}
 for e in obj.get('twin_strategy',[]):
  k=(int(e['vertex']),tuple(map(int,e['view'])));g=int(e['guess'])
  if k in twin:errors.append(f'duplicate twin view {k}')
  twin[k]=g
 expected_twins={(v,tuple(c[w] for w in N[v])) for c in proper for v in (0,1)}
 if set(twin)!=expected_twins:errors.append(f'twin domain mismatch missing={len(expected_twins-set(twin))} extra={len(set(twin)-expected_twins)}')
 for (v,p),g in twin.items():
  if v not in (0,1) or not 0<=g<q or g in p:errors.append(f'illegal twin decision {(v,p,g)}')
 residual=[]
 for c in proper:
  if not any(twin[(v,tuple(c[w] for w in N[v]))]==c[v] for v in (0,1)):residual.append(c)
 cert={};used_views={};clique_guesses={}
 for e in obj.get('residual_matching',[]):
  c=tuple(map(int,e['coloring']));v=int(e['vertex'])
  if c in cert:errors.append(f'duplicate residual coloring {c}')
  cert[c]=v
  if v not in (2,3,4):errors.append(f'bad clique vertex {v}')
  elif len(c)!=5:errors.append(f'bad coloring length {c}')
  else:
   p=tuple(c[w] for w in N[v]);key=(v,p)
   if key in used_views and used_views[key]!=c:errors.append(f'matching reuses clique view {key}')
   used_views[key]=c
   if key in clique_guesses and clique_guesses[key]!=c[v]:errors.append(f'inconsistent matched guess {key}')
   clique_guesses[key]=c[v]
 if set(cert)!=set(residual):errors.append(f'residual set mismatch missing={len(set(residual)-set(cert))} extra={len(set(cert)-set(residual))}')
 for c,v in cert.items():
  if len(c)!=5 or any(not 0<=x<q for x in c) or any(c[u]==c[w] for u,w in edges):errors.append(f'not a proper q-coloring {c}')
  elif v in (2,3,4):
   p=tuple(c[w] for w in N[v])
   if c[v] in p:errors.append(f'illegal matched guess {c,v}')
 # Complete unmatched clique views arbitrarily with least legal color.
 attainable={(v,tuple(c[w] for w in N[v])) for c in proper for v in (2,3,4)}
 for key in attainable:
  if key not in clique_guesses:
   clique_guesses[key]=next(g for g in range(q) if g not in key[1])
 S={**twin,**clique_guesses};hist=Counter();uncovered=[]
 for c in proper:
  hits=sum(S[(v,tuple(c[w] for w in N[v]))]==c[v] for v in range(n));hist[hits]+=1
  if hits==0:uncovered.append(c)
 if uncovered:errors.append(f'reconstructed strategy leaves {len(uncovered)} uncovered')
 strategy={'format':'proper-hat-strategy-v1','graph':'K5-e','q':q,'vertices':list(range(n)),'edges':[list(e) for e in edges],
           'neighbor_order':[list(x) for x in N],
           'strategy':[{'vertex':v,'view':list(p),'guess':g} for (v,p),g in sorted(S.items())]}
 if a.strategy_output:a.strategy_output.write_text(json.dumps(strategy,indent=2,sort_keys=True)+'\n')
 report={'format':'K5-e-q8-residual-matching-verification-v1','certificate_sha256':hashlib.sha256(raw).hexdigest(),
         'proper_colorings_checked':len(proper),'twin_entries':len(twin),'twin_covered':len(proper)-len(residual),
         'residual_colorings':len(residual),'matched_clique_views':len(used_views),'all_clique_views':len(attainable),
         'reconstructed_strategy_entries':len(S),'correct_guess_histogram':dict(sorted(hist.items())),
         'verified':not errors,'errors':errors[:25]}
 text=json.dumps(report,indent=2,sort_keys=True)+'\n';print(text,end='')
 if a.report:a.report.write_text(text)
 return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
