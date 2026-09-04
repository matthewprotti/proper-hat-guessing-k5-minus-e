#!/usr/bin/env python3
"""Semantic negative controls; every mutation is made only in temporary copies."""
import json,tempfile,shutil,argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_certificates import CheckerGeometry,verify_family

def main():
    ap=argparse.ArgumentParser();ap.add_argument('family',type=Path);a=ap.parse_args()
    g=CheckerGeometry()
    verify_family(g,a.family)
    outcomes=[]
    for label in ['illegal_omitted_pair','truncated_matching','duplicate_right_via_legal_position','changed_mutable_tail_set']:
        with tempfile.TemporaryDirectory(prefix='k8-family-negative-') as td:
            f=Path(td)/'family';shutil.copytree(a.family,f)
            if label=='illegal_omitted_pair':
                p=f/'omitted_pairs.bin';b=bytearray(p.read_bytes());b[1]=b[0];p.write_bytes(b)
            elif label=='truncated_matching':
                p=f/'distinct_envelope_match_j.bin';p.write_bytes(p.read_bytes()[:-1])
            elif label=='duplicate_right_via_legal_position':
                p=f/'equal_match_j.bin';b=bytearray(p.read_bytes());b[0]=(b[0]+1)%6;p.write_bytes(b)
            else:
                p=f/'family_spec.json';s=json.loads(p.read_text());m=s['mutable_tail_ids']
                old=m[0];new=next(t for t in range(990) if t not in m)
                s['mutable_tail_ids']=sorted([t for t in m if t!=old]+[new])
                p.write_text(json.dumps(s))
            try:
                verify_family(g,f)
            except ValueError as e:
                outcomes.append({'mutation':label,'status':'REJECTED','reason':str(e)})
            else:
                raise RuntimeError('negative control accepted: '+label)
    print(json.dumps({'positive_control':'PASS','negative_controls':outcomes,'all_rejected':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
