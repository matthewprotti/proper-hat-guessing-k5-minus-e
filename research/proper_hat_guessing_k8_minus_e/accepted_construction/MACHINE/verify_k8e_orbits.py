#!/usr/bin/env python3
"""Independent data-only verifier for the frozen PGL(2,13)-equivariant K8-e strategy."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json
from collections import Counter
from pathlib import Path
P=13; INF=13; Q=14; BASE=(INF,0,1); K=6

def inv(a):
    a%=P
    if not a: raise ZeroDivisionError
    return pow(a,P-2,P)
def proj(x): return (1,0) if x==INF else (x,1)
def det(u,v): return (u[0]*v[1]-u[1]*v[0])%P
def norm(x,a,b,c):
    X,A,B,C=map(proj,(x,a,b,c))
    num=det(X,B)*det(C,A)%P; den=det(X,A)*det(C,B)%P
    return INF if den==0 else num*inv(den)%P
def key_id(j,r0,r1,x,y): return ((((j*Q+r0)*Q+r1)*Q+x)*Q+y)
def view_for(C,x,y,j):
    oth=[i for i in range(K) if i!=j]
    a,b,c=(C[i] for i in oth[:3])
    return (key_id(j,norm(C[oth[3]],a,b,c),norm(C[oth[4]],a,b,c),norm(x,a,b,c),norm(y,a,b,c)), norm(C[j],a,b,c))

def read_twin(path):
    out={}
    with path.open(newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            t=(int(r['a']),int(r['b']),int(r['c']))
            val=(int(r['alpha']),int(r['beta']))
            if t in out: raise AssertionError(('duplicate twin row',t))
            out[t]=val
    return out

def read_clique(path):
    out={}; masks={}; matched={}
    with path.open(newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            i=int(r['right_key']); coords=tuple(int(r[z]) for z in ('vertex','rem0','rem1','twin0','twin1'))
            if i != key_id(*coords): raise AssertionError(('bad key encoding',i,coords))
            if i in out: raise AssertionError(('duplicate clique row',i))
            out[i]=int(r['guess']);masks[i]=int(r['domain_mask']);matched[i]=int(r['matched'])
    return out,masks,matched

def verify_group_normalization():
    triples=0; maps=set()
    for a in range(Q):
      for b in range(Q):
       if b==a:continue
       for c in range(Q):
        if c==a or c==b:continue
        h=tuple(norm(x,a,b,c) for x in range(Q))
        assert (h[a],h[b],h[c])==BASE
        assert len(set(h))==Q
        maps.add(h);triples+=1
    assert triples==14*13*12==2184 and len(maps)==2184
    return {'ordered_distinct_triples':triples,'distinct_normalizers':len(maps)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path); ap.add_argument('--report',type=Path); a=ap.parse_args();root=a.root
    twin=read_twin(root/'K8_e_q14_twin_rules.tsv');clique,masks,matched=read_clique(root/'K8_e_q14_clique_rules.tsv')
    expected_tails=set(itertools.permutations(range(2,13),3))
    assert set(twin)==expected_tails and len(twin)==990
    assert len(clique)==53460 and sum(matched.values())==48510
    group=verify_group_normalization()
    proper=tcovered=residual=fail=0;hit_hist=Counter();used_keys=set();expected_res=[]
    for tail in sorted(twin):
        C=BASE+tail;av=[z for z in range(Q) if z not in C]
        alpha,beta=twin[tail]
        i=(tail[0]+tail[1]+tail[2])%8
        j=(tail[0]+2*tail[1]+3*tail[2]+1)%8
        if j==i: j=(j+1)%8
        assert (alpha,beta)==(av[i],av[j]), ('twin formula mismatch',tail,(alpha,beta),(av[i],av[j]))
        assert alpha in av and beta in av and alpha!=beta
        for x in av:
         for y in av:
            proper+=1;views=[];hits=(alpha==x)+(beta==y)
            for j in range(K):
                i,target=view_for(C,x,y,j);views.append((i,target));used_keys.add(i)
                assert i in clique
                # Independently derive legal domain by varying the hidden clique colour.
                coords=[]; q=i
                for _ in range(4):coords.append(q%Q);q//=Q
                jj=q; ny,nx,r1,r0=coords
                visible={INF,0,1,r0,r1,nx,ny}
                legal=set(range(Q))-visible
                assert clique[i] in legal and target in legal
                assert masks[i]==sum(1<<z for z in legal)
                hits += clique[i]==target
            if alpha==x or beta==y:tcovered+=1
            else:
                residual+=1;expected_res.append((C,x,y,views))
            hit_hist[hits]+=1
            if hits==0:fail+=1
    assert proper==63360 and tcovered==14850 and residual==48510 and fail==0
    assert used_keys==set(clique)
    # Matching certificate: each residual is paired to a distinct one of its six view orbits.
    seen_right=set();match_count=0
    with (root/'K8_e_q14_residual_orbit_matching.tsv').open(newline='') as f:
      rows=list(csv.DictReader(f,delimiter='\t'))
    assert len(rows)==len(expected_res)
    for u,(row,exp) in enumerate(zip(rows,expected_res)):
        assert int(row['left'])==u
        C,x,y,views=exp
        assert tuple(map(int,row['clique'].split(',')))==C
        assert int(row['twin0_colour'])==x and int(row['twin1_colour'])==y
        rid=int(row['right_key']);j=int(row['vertex']);target=int(row['target'])
        assert 0<=j<K and views[j]==(rid,target)
        assert clique[rid]==target and matched[rid]==1
        assert rid not in seen_right;seen_right.add(rid);match_count+=1
    assert match_count==48510
    full=proper*2184
    out={'format':'K8-e-q14-independent-data-verification-v1','claim_candidate':'HG_P(K8-e)=14','twin_rows':len(twin),'clique_view_rows':len(clique),'normalized_proper_colouring_orbits':proper,'twin_covered_orbits':tcovered,'residual_orbits':residual,'matching_size':match_count,'coverage_failures':fail,'correct_guess_histogram':dict(sorted(hit_hist.items())),'group_normalization':group,'full_proper_colourings_represented':full,'verified':True,'file_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.tsv'))}}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'; print(text,end='');
    if a.report: a.report.write_text(text)
if __name__=='__main__':main()
