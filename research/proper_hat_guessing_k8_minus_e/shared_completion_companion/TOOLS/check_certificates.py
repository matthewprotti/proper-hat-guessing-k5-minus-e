#!/usr/bin/env python3
"""Data-only verifier for K8 diagonal-safe and orientation-envelope certificates.
Standard library only. Does not import the builder, SciPy, or a matching solver.
Normalization is reconstructed by listing invertible projective matrices.
"""
from pathlib import Path
from itertools import permutations,product
from collections import Counter
import argparse,json,hashlib

P=13; Q=14; BASE=(13,0,1); TAILS=tuple(permutations(range(2,13),3))
def require(ok,msg):
    if not ok: raise ValueError(msg)
def encode(j,u,v,x,y):
    out=j
    for digit in (u,v,x,y):out=14*out+digit
    return out

def charts():
    out={}
    for a,b,c,d in product(range(13),repeat=4):
        raw=(a,b,c,d)
        if not any(raw) or next(x for x in raw if x)!=1 or (a*d-b*c)%13==0:continue
        h=[]
        for x in range(14):
            num,den=(a,c) if x==13 else (a*x+b,c*x+d)
            num%=13;den%=13
            h.append(13 if not den else num*pow(den,-1,13)%13)
        require(len(set(h))==14,'singular projective map')
        triple=(h.index(13),h.index(0),h.index(1))
        require(triple not in out,'nonunique normalizer')
        out[triple]=tuple(h)
    require(set(out)==set(permutations(range(14),3)),'incomplete normalizers')
    return out

class CheckerGeometry:
    def __init__(self):
        hs=charts()
        self.rows=[];self.legal={};self.av=[]
        for tid,t in enumerate(TAILS):
            C=BASE+t;av=[x for x in range(14) if x not in C];self.av.append(av)
            frames=[]
            for j in range(6):
                v=C[:j]+C[j+1:];h=hs[v[:3]]
                frames.append((j,h[v[3]],h[v[4]],h,h[C[j]]))
            rows=[]
            for x,y in product(av,repeat=2):
                keys=[];targets=[]
                for j,u,v,h,target in frames:
                    xx,yy=h[x],h[y];key=encode(j,u,v,xx,yy)
                    domain=tuple(z for z in range(14) if z not in BASE+(u,v,xx,yy))
                    require(target in domain,'illegal hidden target')
                    if key in self.legal:require(self.legal[key]==domain,'inconsistent right domain')
                    self.legal[key]=domain;keys.append(key);targets.append(target)
                rows.append((x,y,tuple(keys),tuple(targets)))
            self.rows.append(rows)
        require(len(self.legal)==53460,'wrong right universe')
        self.equal_right={r for r in self.legal if r%14==(r//14)%14}
        self.distinct_right=set(self.legal)-self.equal_right
        require(len(self.equal_right)==5940 and len(self.distinct_right)==47520,'right sector counts')
        self.normalizers=len(hs)

    def read_pairs(self,path):
        raw=Path(path).read_bytes()
        require(len(raw)==1980,'wrong pair table byte count')
        pairs=[tuple(raw[2*i:2*i+2]) for i in range(990)]
        require(all(p<q and p in self.av[i] and q in self.av[i] for i,(p,q) in enumerate(pairs)),
                'illegal or noncanonical omitted pair')
        return pairs

    def matching(self,pairs,raw,sector,mutable=frozenset(),bits=None):
        require(sector in ('equal','distinct'),'unknown sector')
        if bits is None:bits=bytes(990)
        require(len(bits)==990 and all(v in (0,1) for v in bits),'bad orientation bitmap')
        used={};at=0
        for tid,rows in enumerate(self.rows):
            a,b=pairs[tid]
            if bits[tid]:a,b=b,a
            for x,y,keys,targets in rows:
                if sector=='equal':
                    eligible=x==y and x not in (a,b)
                else:
                    eligible=x!=y and (tid in mutable or (x!=a and y!=b))
                if not eligible:continue
                require(at<len(raw),'truncated matching')
                j=raw[at];require(0<=j<6,'invalid matching position')
                key=keys[j]
                require(key not in used,'repeated right endpoint')
                used[key]=targets[j];at+=1
        require(at==len(raw),'trailing matching bytes')
        expected=5940 if sector=='equal' else 42570+13*len(mutable)
        require(at==expected,'wrong matching size')
        if sector=='equal':require(set(used)==self.equal_right,'incomplete equal matching')
        else:require(set(used)<=self.distinct_right,'matching crosses sectors')
        return used

def verify_family(g,root):
    spec=json.loads((root/'family_spec.json').read_text())
    require(spec['format']=='K8-orientation-envelope-v1','unknown family format')
    for key,value in {'palette_size':14,'field_order':13,'infinity':13,'clique_size':6,
                      'family_dimension':380,'equal_residual_left':5940,
                      'distinct_envelope_left':47510,'distinct_right':47520,
                      'capacity_upper_bound':380,'next_dimension_left_count':47523,
                      'family_size_exact':str(2**380)}.items():
        require(spec.get(key)==value,'contradictory family metadata: '+key)
    require(spec.get('base_clique_triple')==[13,0,1],'wrong base triple')
    mutable=spec['mutable_tail_ids']
    require(len(mutable)==380 and mutable==sorted(set(mutable)) and all(0<=t<990 for t in mutable),
            'bad mutable-tail set')
    mutable=frozenset(mutable)
    pairs=g.read_pairs(root/'omitted_pairs.bin')
    em=g.matching(pairs,(root/'equal_match_j.bin').read_bytes(),'equal')
    om=g.matching(pairs,(root/'distinct_envelope_match_j.bin').read_bytes(),'distinct',mutable)
    require(not (set(em)&set(om)),'sector intersection')
    clique={**em,**om}
    require(len(clique)==53450,'wrong total matching count')
    for r,domain in g.legal.items():
        clique.setdefault(r,min(domain))
        require(clique[r] in domain,'illegal clique guess')
    failures=contexts=0;base_hist=Counter()
    for tid,rows in enumerate(g.rows):
        p,q=pairs[tid]
        for x,y,keys,targets in rows:
            clique_hits=sum(clique[key]==target for key,target in zip(keys,targets))
            base_hits=clique_hits+int(x==p)+int(y==q)
            base_hist[base_hits]+=1
            options=((p,q),(q,p)) if tid in mutable else ((p,q),)
            for a,b in options:
                contexts+=1
                if clique_hits+int(x==a)+int(y==b)==0:failures+=1
    require(failures==0 and contexts==87680,'family coverage failed')
    require(sum(base_hist.values())==63360 and base_hist.get(0,0)==0,'baseline coverage failed')
    return {
        'check':'STDLIB_MATRIX_NORMALIZED_SHARED_CLIQUE_FAMILY',
        'normalizers':g.normalizers,'mutable_tail_orbits':380,
        'family_size_exact':str(2**380),'equal_matching':len(em),'distinct_envelope_matching':len(om),
        'all_right_views':len(clique),'unused_matching_right_views':10,
        'orientation_local_contexts_checked':contexts,'coverage_failures':failures,
        'normalized_colourings_per_strategy':63360,
        'full_colourings_per_strategy_by_free_orbit_lift':63360*2184,
        'full_sweep_executed':False,
        'baseline_correct_guess_histogram':dict(sorted(base_hist.items())),
        'capacity_bound':(47520-42570)//13,
        'verified':True}

def verify_pilot(g,root):
    rec=json.loads((root/'PILOT_RECEIPT.json').read_text())
    require(len(rec['flows'])==8 and len(rec['trials'])==136,'wrong pilot inventory')
    rules={};eqchecked=0;offchecked=0
    for fid in range(8):
        fd=root/'DATA'/f'flow_{fid:02d}'
        pairs=g.read_pairs(fd/'omitted_pairs.bin');rules[fid]=pairs
        m=g.matching(pairs,(fd/'equal_match_j.bin').read_bytes(),'equal')
        require(len(m)==5940,'bad flow matching');eqchecked+=1
    expected={(f,o) for f in range(8) for o in ['sorted']+[f'seed_{s:02d}' for s in range(16)]}
    observed=set()
    for row in rec['trials']:
        fid=row['flow_id'];name=row['orientation'];key=(fid,name)
        require(key in expected and key not in observed,'pilot duplicate or missing identity')
        observed.add(key)
        fd=root/'DATA'/f'flow_{fid:02d}'
        bits=(fd/f'orientation_{name}.bin').read_bytes()
        m=g.matching(rules[fid],(fd/f'distinct_match_{name}.bin').read_bytes(),'distinct',bits=bits)
        require(len(m)==42570,'bad distinct pilot matching');offchecked+=1
    require(observed==expected,'incomplete pilot')
    return {'check':'STDLIB_ALL_FROZEN_PILOT_MATCHINGS','flows':eqchecked,
            'distinct_sector_certificates':offchecked,'matching_size_each':42570,'verified':True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--family',type=Path,required=True)
    ap.add_argument('--pilot',type=Path)
    ap.add_argument('--report',type=Path)
    a=ap.parse_args();g=CheckerGeometry();result={'family':verify_family(g,a.family)}
    if a.pilot:result['pilot']=verify_pilot(g,a.pilot)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n';print(text,end='')
    if a.report:
        out=a.report.resolve()
        for root in [a.family,a.pilot]:
            if root is not None:
                rr=root.resolve();require(out!=rr and rr not in out.parents,'report must be outside certificate root')
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
if __name__=='__main__':main()
