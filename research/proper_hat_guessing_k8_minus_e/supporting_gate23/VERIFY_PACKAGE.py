#!/usr/bin/env python3
"""Read-only Gate23 verification, with explicit coverage modes."""
from pathlib import Path
import argparse,json,subprocess,sys,tempfile,os
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'TOOLS'))
from integrity import manifest_check
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--full',action='store_true',help='Replay independent geometry, all frozen matchings, connected census, and the 2000-rule experiment')
    a=ap.parse_args();before=manifest_check(ROOT)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def run(cmd):
        r=subprocess.run(cmd,text=True,capture_output=True,env=env)
        if r.returncode:
            print(r.stdout);print(r.stderr,file=sys.stderr)
            raise RuntimeError('phase failed: '+repr(cmd))
        return r.stdout
    out={'manifest_files':len(before),'full_requested':a.full}
    out['frozen_predicates']=json.loads(run([sys.executable,'-B',str(ROOT/'TOOLS/verify_frozen_analysis.py')]))
    if a.full:
        with tempfile.TemporaryDirectory(prefix='k8-gate23-check-') as td:
            t=Path(td)
            run([sys.executable,'-B',str(ROOT/'TOOLS/independent_audit.py'),str(ROOT),'--out',str(t/'audit')])
            audit=json.loads((t/'audit/independent_results.json').read_text())
            out['geometry']=audit['geometry']
            out['frozen_matching_reconstruction']=len(audit['bad_rules'])
            out['accepted_rule_census']=audit['accepted']['census']
            compiler=run(['g++','-dumpfullversion']).strip()
            if compiler!='14.2.0':raise RuntimeError('Exact historical shuffle replay requires g++/libstdc++ 14.2.0; frozen-data check remains available')
            run(['g++','-std=c++20','-O2',str(ROOT/'TOOLS/emit_seeded_rules.cpp'),'-o',str(t/'emit')])
            with (t/'rules.bin').open('wb') as f:
                subprocess.run([str(t/'emit'),'2000'],stdout=f,check=True,env=env)
            run([sys.executable,'-B',str(ROOT/'TOOLS/independent_seed_scout.py'),str(ROOT),str(t/'rules.bin'),'--out',str(t/'scout')])
            out['sampled_2000']=json.loads((t/'scout/independent_2000_summary.json').read_text())
    after=manifest_check(ROOT)
    if before!=after:raise RuntimeError('source tree mutated')
    out['read_only']=True
    out['scope']='FULL_GATE23_FINITE_REPLAY' if a.full else '23_ABSENT_VIEW_AND_SINGLETON_HALL_WITNESS_PREDICATES_ONLY'
    out['status']='PASS'
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
