#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, itertools, json
from collections import Counter, defaultdict, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=13;INF=13;Q=14;K=6;TV=list(range(2,13))
def inv(a):return pow(a,P-2,P)
def proj(x):return (1,0) if x==INF else (x,1)
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%P
def mb(x,a,b,c):
 X,A,B,C=map(proj,(x,a,b,c));num=det(X,B)*det(C,A)%P;den=det(X,A)*det(C,B)%P
 return INF if den==0 else num*inv(den)%P
def key(j,r0,r1,nx):return (j,r0,r1,nx)
tails=[]
for ia in range(11):
 for ib in range(11):
  if ib==ia:continue
  for ic in range(11):
   if ic in (ia,ib):continue
   C=(INF,0,1,TV[ia],TV[ib],TV[ic]);av=tuple(z for z in range(Q) if z not in C);tails.append((C,av))
assert len(tails)==990
N={};pre=defaultdict(list)
for tid,(C,av) in enumerate(tails):
 for x in av:
  row=[]
  for j in range(K):
   o=[i for i in range(K) if i!=j];a,b,c=C[o[0]],C[o[1]],C[o[2]]
   r=key(j,mb(C[o[3]],a,b,c),mb(C[o[4]],a,b,c),mb(x,a,b,c));row.append(r);pre[r].append((tid,x))
  N[(tid,x)]=tuple(row)
assert len(pre)==5940 and Counter(map(len,pre.values()))==Counter({8:5940})
rows=list(csv.DictReader((ROOT/'DATA/bad_rules_23_combined.tsv').open(),delimiter='\t'))
byseed=defaultdict(dict)
for r in rows:byseed[int(r['seed'])][int(r['tail_id'])]=(int(r['alpha']),int(r['beta']))
expected=[1,6,17,18,21,25,45,49,64,90,99,104,116,120,123,124,128,191,192,219,238,266,296]
assert sorted(byseed)==expected and all(len(x)==990 for x in byseed.values())
missing=[]
for seed in expected:
 rules=byseed[seed];image=set();L=[]
 for tid,(C,av) in enumerate(tails):
  ga,gb=rules[tid];assert ga!=gb and ga in av and gb in av
  for x in av:
   if x not in (ga,gb):
    L.append((tid,x));image.update(N[(tid,x)])
 miss=set(pre)-image
 assert len(L)==5940 and len(image)==5939 and len(miss)==1
 r=next(iter(miss));assert all(x in rules[tid] for tid,x in pre[r])
 missing.append((seed,r))
# crafted no-isolated rule
rr=list(csv.DictReader((ROOT/'DATA/K8_A1_noisol_rules.tsv').open(),delimiter='\t'))
rules={int(r['tail_id']):(int(r['alpha']),int(r['beta'])) for r in rr}
image=set();L=[]
for tid,(C,av) in enumerate(tails):
 ga,gb=rules[tid];assert ga!=gb and ga in av and gb in av
 for x in av:
  if x not in (ga,gb):L.append((tid,x));image.update(N[(tid,x)])
assert len(L)==5940 and len(image)==5940
A=(0,5);assert A in L
S=[x for x in L if x!=A];NS={r for x in S for r in N[x]}
assert len(S)==5939 and len(NS)==5938
B=set(pre)-NS;assert len(B)==2 and all([x for x in pre[r] if x in L]==[A] for r in B)
result={'format':'K8-e-Gate23-frozen-verification-v2','coverage':'23 frozen absent-view witnesses and singleton complement Hall witness; not matching replays or 2000-seed census','bad_rules':23,'bad_seed_list':expected,'full_equal_right_views':5940,'full_preimages_per_equal_view':8,'bad_rule_missing_views_each':1,'crafted_noisolated_rule':{'isolated_equal_views':0,'S':len(S),'N':len(NS),'deficiency':len(S)-len(NS),'trapped_views':len(B)},'verified':True}

print(json.dumps(result,indent=2,sort_keys=True))
