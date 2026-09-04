#!/usr/bin/env python3
"""Read-only manifest, mathematical certificate, and semantic-control verification."""
from pathlib import Path
import sys,subprocess,argparse,json,os
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'TOOLS'))
from integrity import manifest_check
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--all-pilot',action='store_true',help='Also check all 136 stored pilot matchings, not just the 2^380 family')
    a=ap.parse_args();before=manifest_check(ROOT)
    cmd=[sys.executable,'-I','-S','-B',str(ROOT/'TOOLS/check_certificates.py'),'--family',str(ROOT/'FAMILY')]
    if a.all_pilot:cmd.extend(['--pilot',str(ROOT/'PILOT')])
    def call(cmd):
        r=subprocess.run(cmd,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        if r.returncode:
            print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError('verification phase failed')
        return json.loads(r.stdout)
    result=call(cmd)
    result['controls']=call([sys.executable,'-I','-S','-B',str(ROOT/'TOOLS/negative_controls.py'),str(ROOT/'FAMILY')])
    if before!=manifest_check(ROOT):raise RuntimeError('source changed')
    result['inventory_files']=len(before);result['read_only']=True
    result['evidence_status']='INTERNAL_CERTIFICATE_CHECKS_NOT_BLINDED_REVIEW'
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
