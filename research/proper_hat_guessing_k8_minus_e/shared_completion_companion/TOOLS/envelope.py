#!/usr/bin/env python3
"""Construct a shared clique completion for a 380-dimensional orientation family."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from geometry import Geometry,SplitMix64,match
from pilot import load_rules,matching_positions

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rules',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    g=Geometry();pairs=np.sort(load_rules(a.rules),axis=1)
    ids,eqadj,_=g.residual(pairs,'equal')
    eqj=matching_positions(eqadj,match(eqadj,5940))
    order=list(range(990));SplitMix64(1000).shuffle(order)
    mutable=sorted(order[:380])
    keep=g.retained_mask(pairs)&g.off_mask
    keep[mutable]=g.off_mask[mutable]
    offadj=g.off_rmap[g.edges[keep]]
    m=match(offadj,47520);offj=matching_positions(offadj,m)
    assert len(m)==47510
    assert len(set(map(int,m)))==47510
    (out/'omitted_pairs.bin').write_bytes(pairs.astype(np.uint8).tobytes())
    (out/'equal_match_j.bin').write_bytes(eqj.tobytes())
    (out/'distinct_envelope_match_j.bin').write_bytes(offj.tobytes())
    spec={
        'format':'K8-orientation-envelope-v1',
        'palette_size':14,'field_order':13,'infinity':13,'base_clique_triple':[13,0,1],
        'clique_size':6,'tail_order':'lexicographic permutations of 2,...,12 of length 3',
        'pair_order':'smaller colour alpha outside mutable tails',
        'mutable_tail_ids':mutable,'mutable_selection':'first 380 of Fisher-Yates SplitMix64(seed=1000) shuffle of 0,...,989, then sorted',
        'matching_order':'tail, twin0 colour, twin1 colour; ascending available colours, restricted to the named sector',
        'matching_encoding':'one uint8 hidden-clique-position 0..5 for each residual/envelope colouring',
        'equal_residual_left':5940,'distinct_envelope_left':47510,'distinct_right':47520,
        'family_dimension':380,'family_size_exact':str(2**380),
        'capacity_upper_bound':380,
        'next_dimension_left_count':42570+13*381,
        'independent_review':'PENDING'
    }
    (out/'family_spec.json').write_text(json.dumps(spec,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:spec[k] for k in ('family_dimension','equal_residual_left','distinct_envelope_left','distinct_right','capacity_upper_bound')},sort_keys=True))
if __name__=='__main__':main()
