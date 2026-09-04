#!/usr/bin/env python3
"""Diagonal-safe flow synthesis, followed by exact distinct-sector certificates.
No claims of a universal compatibility theorem are made. The search engine uses
SciPy; every result is reduced to small explicit incidence witnesses.
"""
from pathlib import Path
import argparse,csv,json,hashlib,time,sys,platform
import numpy as np,scipy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from geometry import Geometry,SplitMix64,orient,match,TAILS

def load_rules(path):
    with Path(path).open(newline='') as f:
        rd=csv.DictReader(f,delimiter='\t')
        rows=list(rd)
    d={tuple(int(r[k]) for k in ('a','b','c')):(int(r['alpha']),int(r['beta'])) for r in rows}
    assert len(rows)==990 and set(d)==set(TAILS)
    return np.array([d[t] for t in TAILS],dtype=np.int16)

def matching_positions(adj,m):
    assert np.all(m>=0)
    eq=(adj==m[:,None])
    assert np.all(eq.sum(axis=1)==1)
    return np.argmax(eq,axis=1).astype(np.uint8)

def quota_flow(geo,seed):
    nR=5940;nL=7920;nT=990
    r0=1;l0=r0+nR;t0=l0+nL;sink=t0+nT
    rng=SplitMix64(seed)
    rp=list(range(r0,l0));lp=list(range(l0,t0));tp=list(range(t0,sink))
    for p in (rp,lp,tp):rng.shuffle(p)
    rp=np.array(rp);lp=np.array(lp);tp=np.array(tp)
    rr=np.concatenate([np.zeros(nR,dtype=int),rp[geo.eq_edges.ravel()],lp,tp])
    cc=np.concatenate([rp,np.repeat(lp,6),tp[np.repeat(np.arange(990),8)],np.full(990,sink)])
    cap=np.concatenate([np.ones(len(rr)-990,dtype=np.int64),np.full(990,6,dtype=np.int64)])
    C=csr_matrix((cap,(rr,cc)),shape=(sink+1,sink+1))
    sol=maximum_flow(C,0,sink)
    assert sol.flow_value==5940
    layer=sol.flow[rp,:][:,lp].tocoo()
    use=(layer.data==1);left=layer.col[use];right=layer.row[use]
    assert len(left)==5940 and len(set(map(int,left)))==5940 and len(set(map(int,right)))==5940
    retained=np.zeros(7920,dtype=bool);retained[left]=True
    assert set(retained.reshape(990,8).sum(axis=1))=={6}
    pairs=geo.available[~retained.reshape(990,8)].reshape(990,2)
    pairmap={int(l):int(r) for l,r in zip(left,right)}
    chosen=np.flatnonzero(retained)
    eqj=matching_positions(geo.eq_edges[chosen],np.array([pairmap[int(l)] for l in chosen]))
    return pairs,eqj

def sha(raw):return hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inherited-rules',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();root=args.output.resolve()
    root.mkdir(parents=True,exist_ok=False)
    data=root/'DATA';data.mkdir()
    t0=time.monotonic();geo=Geometry();rows=[];flows=[]
    for fseed in range(8):
        if fseed==0:
            pairs=np.sort(load_rules(args.inherited_rules),axis=1)
            _,eqadj,_=geo.residual(pairs,'equal')
            eqj=matching_positions(eqadj,match(eqadj,5940))
            basis='inherited frozen quota-flow omitted pairs; fresh checked equal matching'
        else:
            pairs,eqj=quota_flow(geo,fseed)
            basis='fresh quota flow; SplitMix64 relabeling seed '+str(fseed)
        fdir=data/f'flow_{fseed:02d}';fdir.mkdir()
        pbytes=pairs.astype(np.uint8).tobytes();ebytes=eqj.tobytes()
        (fdir/'omitted_pairs.bin').write_bytes(pbytes)
        (fdir/'equal_match_j.bin').write_bytes(ebytes)
        eqids,eqadj,nr=geo.residual(pairs,'equal')
        eqr=eqadj[np.arange(len(eqadj)),eqj]
        assert len(eqr)==len(set(map(int,eqr)))==5940
        deg=np.bincount(eqadj.ravel(),minlength=nr)
        flows.append({'id':fseed,'basis':basis,'pair_sha256':sha(pbytes),
                      'equal_matching_sha256':sha(ebytes),
                      'equal_min_right_degree':int(deg.min()),
                      'equal_right_degree_histogram':{str(i):int(sum(deg==i)) for i in range(9) if sum(deg==i)},
                      'equal_matching_size':5940})
        for ose in [None]+list(range(16)):
            name='sorted' if ose is None else f'seed_{ose:02d}'
            rules=orient(pairs,ose)
            bits=(rules[:,0]!=pairs[:,0]).astype(np.uint8).tobytes()
            (fdir/f'orientation_{name}.bin').write_bytes(bits)
            ids,adj,nr=geo.residual(rules,'distinct');m=match(adj,nr)
            got=int(sum(m>=0))
            row={'flow_id':fseed,'orientation':name,'orientation_seed':ose,'distinct_left':len(adj),
                 'distinct_right':nr,'matching_size':got,'deficiency':len(adj)-got,
                 'orientation_bitmap_sha256':sha(bits)}
            if got==len(adj):
                raw=matching_positions(adj,m).tobytes()
                (fdir/f'distinct_match_{name}.bin').write_bytes(raw)
                row['matching_sha256']=sha(raw)
            else:
                np.save(fdir/f'partial_{name}.npy',m)
            rows.append(row)
        print('flow',fseed,'distinct sizes',sorted({r['matching_size'] for r in rows if r['flow_id']==fseed}),
              'elapsed',round(time.monotonic()-t0,3),flush=True)
    result={'status':'FINITE_COMPATIBILITY_CERTIFICATES_NOT_UNIVERSAL',
            'flows':flows,'trials':rows,'trial_count':len(rows),
            'complete_trials':sum(r['deficiency']==0 for r in rows),
            'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
            'elapsed_seconds':time.monotonic()-t0}
    (root/'PILOT_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
