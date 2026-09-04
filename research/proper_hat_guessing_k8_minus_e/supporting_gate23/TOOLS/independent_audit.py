#!/usr/bin/env python3
"""Independent reconstruction of the uploaded K8-e Gate 2/3 data.

Normalization is obtained by enumerating all invertible 2x2 matrices over F_13
up to scalar, NOT by using the package's determinant/cross-ratio formula.
SciPy computes candidate matchings, each of which is explicitly checked.
A candidate matching plus a Hall witness proves the claimed deficiency,
without relying on SciPy's assertion that the matching is maximum.

Usage: python independent_audit.py PATH_TO_EXTRACTED_PACKAGE --out OUTPUT_DIR
Dependencies: numpy, scipy (tested with 2.3.5 and 1.17.0).
"""
from __future__ import annotations
import argparse, csv, itertools, json, math, sys, time
from collections import Counter, defaultdict, deque
from pathlib import Path
import numpy as np
import scipy
from scipy.sparse import csr_matrix, bmat
from scipy.sparse.csgraph import maximum_bipartite_matching, connected_components

P=13; INF=13; Q=14; K=6


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def enumerate_normalizations():
    """Map each ordered triple to its unique (infinity,0,1) normalizer."""
    result={}
    for raw in itertools.product(range(P), repeat=4):
        if not any(raw) or next(z for z in raw if z)!=1:
            continue
        a,b,c,d=raw
        if (a*d-b*c)%P==0:
            continue
        perm=[]
        for x in range(Q):
            numerator, denominator = (a,c) if x==INF else (a*x+b,c*x+d)
            numerator%=P; denominator%=P
            perm.append(INF if denominator==0 else numerator*pow(denominator,-1,P)%P)
        require(len(set(perm))==14,'projective map is not a permutation')
        base=(perm.index(INF),perm.index(0),perm.index(1))
        require(base not in result, 'nonunique normalizer')
        result[base]=tuple(perm)
    require(len(result)==2184,'wrong projective group size')
    return result


class Geometry:
    def __init__(self):
        self.norm=enumerate_normalizations()
        self.tails=list(itertools.permutations(range(2,13),3))
        self.cliques=[(INF,0,1)+t for t in self.tails]
        self.available=[tuple(x for x in range(Q) if x not in C) for C in self.cliques]
        self.eq_meta=[]; self.off_meta=[]; eq_keys=[]; off_keys=[]
        for tid,C in enumerate(self.cliques):
            normalizers=[]; visible=[]
            for j in range(K):
                remaining=C[:j]+C[j+1:]
                f=self.norm[remaining[:3]]
                normalizers.append(f)
                visible.append((j,f[remaining[3]],f[remaining[4]]))
            for x in self.available[tid]:
                self.eq_meta.append((tid,x))
                eq_keys.append([visible[j]+(normalizers[j][x],) for j in range(K)])
                for y in self.available[tid]:
                    if x==y: continue
                    self.off_meta.append((tid,x,y))
                    off_keys.append([visible[j]+(normalizers[j][x],normalizers[j][y]) for j in range(K)])
        self.eq_right=sorted({r for E in eq_keys for r in E})
        self.off_right=sorted({r for E in off_keys for r in E})
        eq_index={r:i for i,r in enumerate(self.eq_right)}
        off_index={r:i for i,r in enumerate(self.off_right)}
        self.eq_edges=np.array([[eq_index[r] for r in E] for E in eq_keys],dtype=np.int32)
        self.off_edges=np.array([[off_index[r] for r in E] for E in off_keys],dtype=np.int32)
        self.eq_meta=np.array(self.eq_meta,dtype=np.int32)
        self.off_meta=np.array(self.off_meta,dtype=np.int32)
        self.eq_pre=[[] for _ in self.eq_right]
        for left,E in enumerate(self.eq_edges):
            for r in E: self.eq_pre[r].append(left)
        require(self.eq_edges.shape==(7920,6),'full equal size')
        require(self.off_edges.shape==(55440,6),'full distinct size')
        require(len(self.eq_right)==5940 and len(self.off_right)==47520,'full right counts')
        require(Counter(map(len,self.eq_pre))=={8:5940},'equal preimage counts')
        require(all(len({int(self.eq_meta[v,0]) for v in E})==8 for E in self.eq_pre),'preimages in same tail')
        require(set(np.bincount(self.off_edges.ravel()))=={7},'distinct full degree')
        self.eq_lookup={tuple(v):i for i,v in enumerate(self.eq_meta.tolist())}

    def masks(self,rules):
        a=np.array([r[0] for r in rules]); b=np.array([r[1] for r in rules])
        t,x=self.eq_meta.T
        eq=(x!=a[t]) & (x!=b[t])
        t,x,y=self.off_meta.T
        off=(x!=a[t]) & (y!=b[t])
        require(eq.sum()==5940 and off.sum()==42570,'residual sizes')
        return eq,off

    def validate_rules(self,rows,has_tid=True):
        require(len(rows)==990,'rule table length')
        rules=[]
        for tid,row in enumerate(rows):
            if has_tid: require(int(row['tail_id'])==tid,'tail id/order')
            require(tuple(int(row[k]) for k in ('a','b','c'))==self.tails[tid],'tail metadata')
            a,b=int(row['alpha']),int(row['beta'])
            require(a!=b and a in self.available[tid] and b in self.available[tid],'illegal twin guesses')
            if 'alpha_index' in row:
                require(self.available[tid][int(row['alpha_index'])]==a,'alpha index')
                require(self.available[tid][int(row['beta_index'])]==b,'beta index')
            rules.append((a,b))
        return rules


def read_tsv(path):
    with path.open(newline='') as f: return list(csv.DictReader(f,delimiter='\t'))


def graph_matrix(edges,nright):
    nleft=len(edges)
    return csr_matrix((np.ones(nleft*6,dtype=np.int32),edges.ravel(),np.arange(0,nleft*6+1,6,dtype=np.int32)),shape=(nleft,nright))


def checked_matching(edges,nright):
    graph=graph_matrix(edges,nright)
    match=maximum_bipartite_matching(graph,perm_type='column')
    require(len(match)==len(edges),'matching orientation')
    selected=np.flatnonzero(match>=0)
    require(len(set(match[selected].tolist()))==len(selected),'matching repeats a right vertex')
    require(bool(np.all(np.any(edges[selected]==match[selected,None],axis=1))),'non-edge in matching')
    return match,graph


def left_description(g: Geometry,full_id: int):
    tid,x=map(int,g.eq_meta[full_id]);return {'tail_id':tid,'tail':list(g.tails[tid]),'colour':x}


def encode_equal(r):
    j,a,b,x=map(int,r)
    return ((((j*Q+a)*Q+b)*Q+x)*Q+x)


def incidence_geometry_checks(g):
    pair_to_right={}
    adjacency=[{} for _ in range(7920)]
    for r,ns in enumerate(g.eq_pre):
        for x,y in itertools.combinations(ns,2):
            require((x,y) not in pair_to_right,'4-cycle found')
            pair_to_right[x,y]=r
            adjacency[x][y]=r;adjacency[y][x]=r
    # A 6-cycle would be a triangle in left adjacency using three distinct views.
    triangles=0
    for x,ns in enumerate(adjacency):
        for y,rxy in ns.items():
            if y<=x:continue
            for z in ns.keys() & adjacency[y].keys():
                if z<=y:continue
                rs=(rxy,ns[z],adjacency[y][z])
                if len(set(rs))==3:
                    triangles+=1
    require(triangles==0,'6-cycle found')
    return {'equal_full_left':7920,'equal_full_right':5940,'left_degree':6,'right_degree':8,
            'distinct_preimage_tails_per_equal_view':8,'four_cycles':0,'six_cycles':triangles}


def connected_core_census(g,eqmask,limit=12):
    retained=np.flatnonzero(eqmask)
    edges=g.eq_edges[eqmask]
    pre=[[] for _ in g.eq_right]
    for local,E in enumerate(edges):
        for r in E:pre[r].append(local)
    hedges=list(map(frozenset,pre))
    require(all(hedges),'isolated right view in accepted rule')
    seen=set(hedges); queue=deque(seen)
    best=[None]*(limit+1);best_sets=[None]*(limit+1)
    while queue:
        A=queue.popleft()
        if len(A)>limit:continue
        cand={int(r) for v in A for r in edges[v]}
        b=sum(hedges[r]<=A for r in cand)
        if best[len(A)] is None or b>best[len(A)]:
            best[len(A)]=b;best_sets[len(A)]=A
        for r in cand:
            U=A|hedges[r]
            if len(U)<=limit and U not in seen:
                seen.add(U);queue.append(U)
    small=[r for r,h in enumerate(hedges) if len(h)==2]
    explicit=[]
    for r,s in itertools.combinations(small,2):
        A=hedges[r]|hedges[s]
        if len(A)==4:
            trapped=[z for z,h in enumerate(hedges) if h<=A]
            explicit.append({'size':4,'trapped_count':len(trapped),
                'left':[left_description(g,int(retained[v])) for v in sorted(A)],
                'right_views':[list(g.eq_right[z]) for z in trapped]})
            break
    # Take combinations of all 7 size-two neighbourhoods, useful to refute
    # claimed global maxima at several larger sizes as well.
    disjoint_lower={}
    for mask in range(1,1<<len(small)):
        A=frozenset().union(*(hedges[small[i]] for i in range(len(small)) if mask>>i&1))
        if len(A)>limit:continue
        trapped=[r for r in {int(r) for v in A for r in edges[v]} if hedges[r]<=A]
        a=len(A); b=len(trapped)
        if b>disjoint_lower.get(a,0):disjoint_lower[a]=b
    at_most_half=all(b is None or 2*b<=a for a,b in enumerate(best))
    disjoint_pairs=len(set().union(*(hedges[r] for r in small)))==2*len(small)
    global_kappa=[a//2 for a in range(limit+1)] if (at_most_half and disjoint_pairs and 2*len(small)>=limit) else None
    if limit==12:
        require(len(seen)==95096,'connected-union census count')
        require(best[2:]==[1,1,1,2,2,3,3,3,3,4,4],'connected-union maxima')
        require(global_kappa==[a//2 for a in range(13)],'corrected global spectrum')
    return {'degree_histogram':dict(sorted(Counter(map(len,pre)).items())),
        'connected_unions':len(seen),'connected_maxima':best,
        'no_connected_violation_through':limit,
        'degree_two_right_views':[{'right':list(g.eq_right[r]),'left':[left_description(g,int(retained[v])) for v in sorted(hedges[r])]} for r in small],
        'counterexample_to_reported_global_maximum':explicit,
        'global_lower_bounds_from_degree_two_unions':disjoint_lower,
        'all_connected_counts_at_most_half_size':at_most_half,
        'degree_two_neighbourhoods_pairwise_disjoint':disjoint_pairs,
        'corrected_global_kappa_0_through_12':global_kappa,
        'all_connected_inequalities_pass':all(b is None or b<=a for a,b in enumerate(best))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path)
    parser.add_argument('--out',type=Path,default=Path('independent_audit_output'))
    parser.add_argument('--skip-cores',action='store_true')
    args=parser.parse_args();root=args.package;args.out.mkdir(parents=True,exist_ok=True)
    t0=time.monotonic();g=Geometry();print('Independent projective geometry reconstructed',flush=True)
    results={'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
             'geometry':incidence_geometry_checks(g),'bad_rules':[]}
    print('No 4- or 6-cycles; all equal fibres have 8 distinct tail preimages',flush=True)
    byseed=defaultdict(list)
    for r in read_tsv(root/'DATA/bad_rules_23_combined.tsv'):byseed[int(r['seed'])].append(r)
    expected=[1,6,17,18,21,25,45,49,64,90,99,104,116,120,123,124,128,191,192,219,238,266,296]
    require(sorted(byseed)==expected,'seed list')
    frozen_missing={r['seed']:r for r in json.loads((root/'DATA/missing_equal_views_with_preimages.json').read_text())}
    frozen_cores={r['seed']:r for r in json.loads((root/'DATA/alternating_complement_cores.json').read_text())}
    for seed in expected:
        rules=g.validate_rules(byseed[seed]);eq,off=g.masks(rules)
        deg=np.bincount(g.eq_edges[eq].ravel(),minlength=5940)
        missing=np.flatnonzero(deg==0);require(len(missing)==1,f'seed {seed}: missing count')
        r=int(missing[0]);key=g.eq_right[r];pre=g.eq_pre[r]
        require(all(int(g.eq_meta[v,1]) in rules[int(g.eq_meta[v,0])] for v in pre),'undeleted preimage')
        alpha=sum(int(g.eq_meta[v,1])==rules[int(g.eq_meta[v,0])][0] for v in pre)
        mr=frozen_missing[seed]
        require(mr['missing_key']==encode_equal(key),'stored missing key')
        require((mr['alpha_hits'],mr['beta_hits'])==(alpha,8-alpha),'stored hit split')
        computed_pre=[]
        for v in pre:
            tid,x=map(int,g.eq_meta[v]);a,b=rules[tid]
            computed_pre.append({'tail_id':tid,'tail':list(g.tails[tid]),'equal_colour':x,
               'hidden_colour':g.cliques[tid][key[0]],'alpha':a,'beta':b,'hit':'alpha' if x==a else 'beta'})
        require(computed_pre==mr['preimages'],'stored preimages')
        em,eg=checked_matching(g.eq_edges[eq],5940)
        om,og=checked_matching(g.off_edges[off],47520)
        require(int((em>=0).sum())==5939,'equal matching size')
        require(int((om>=0).sum())==42570,'distinct matching size')
        # A complete checked matching of every present R proves exact deficiency 1.
        present=eg[:,deg>0]
        block=bmat([[None,present],[present.T,None]],format='csr')
        ncomp,labels=connected_components(block,directed=False)
        require(ncomp==1,'equal present graph disconnected')
        # Independently check frozen complement-core certificates.
        core=frozen_cores[seed]
        A={g.eq_lookup[(r['tail_id'],r['colour'])] for r in core['A']}
        require(all(eq[v] for v in A),'nonresidual complement vertex')
        S=np.array(eq,copy=True);S[list(A)]=False
        NS=set(g.eq_edges[S].ravel().tolist())
        B=set(range(5940))-NS
        require({encode_equal(g.eq_right[v]) for v in B}=={r['key'] for r in core['B']},'stored complement right set')
        require(len(B)==len(A)+1,'complement witness deficit')
        for br in core['B']:
            z=next(v for v in B if encode_equal(g.eq_right[v])==br['key'])
            require(sum(v in A for v in g.eq_pre[z])==br['degree_from_A'],'stored core degree')
        results['bad_rules'].append({'seed':seed,'missing_right':list(key),'preimages':computed_pre,
            'alpha_hits':alpha,'beta_hits':8-alpha,'equal_matching':5939,'distinct_matching':42570,
            'equal_present_components':ncomp,'equal_deficiency':1,'distinct_deficiency':0,
            'frozen_complement_A_size':len(A),'frozen_complement_B_size':len(B)})
        print('frozen seed',seed,'verified; matching sizes 5939 / 42570',flush=True)
    rules=g.validate_rules(read_tsv(root/'DATA/K8_A1_noisol_rules.tsv'))
    eq,off=g.masks(rules);deg=np.bincount(g.eq_edges[eq].ravel(),minlength=5940)
    require(int((deg==0).sum())==0,'crafted rule has isolated view')
    A=g.eq_lookup[(0,5)];require(bool(eq[A]),'crafted A is not residual')
    S=eq.copy();S[A]=False;NS=set(g.eq_edges[S].ravel().tolist());B=set(range(5940))-NS
    require(len(B)==2 and len(NS)==5938,'crafted witness')
    require(sorted(g.eq_right[r] for r in B)==[(0,10,8,12),(1,2,3,4)],'crafted right keys')
    require(all([v for v in g.eq_pre[r] if eq[v]]==[A] for r in B),'crafted unique neighbour')
    em,_=checked_matching(g.eq_edges[eq],5940);om,_=checked_matching(g.off_edges[off],47520)
    require(int((em>=0).sum())==5939 and int((om>=0).sum())==42570,'crafted exact matching')
    results['crafted']={'isolated_equal_views':0,'S':5939,'N':5938,'A':left_description(g,A),
        'trapped_right':[list(g.eq_right[r]) for r in sorted(B)],'equal_matching':5939,'distinct_matching':42570,'full_deficiency':1}
    print('Crafted no-isolated counterexample verified',flush=True)
    rules=g.validate_rules(read_tsv(root/'DATA/accepted_K8_twin_rules.tsv'),has_tid=False)
    eq,off=g.masks(rules)
    em,_=checked_matching(g.eq_edges[eq],5940);om,_=checked_matching(g.off_edges[off],47520)
    require(int((em>=0).sum())==5940 and int((om>=0).sum())==42570,'accepted rule matching')
    results['accepted']={'equal_matching':5940,'distinct_matching':42570,'full_matching':48510}
    print('Included accepted rule admits independently checked matching of 48,510',flush=True)
    if not args.skip_cores:
        results['accepted']['census']=connected_core_census(g,eq)
        print('Connected-core census:',results['accepted']['census']['connected_unions'],flush=True)
        print('Counterexample to global maxima:',results['accepted']['census']['counterexample_to_reported_global_maximum'],flush=True)
    results['elapsed_seconds']=time.monotonic()-t0
    (args.out/'independent_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print('Independent audit completed:',args.out/'independent_results.json',flush=True)

if __name__=='__main__':
    main()
