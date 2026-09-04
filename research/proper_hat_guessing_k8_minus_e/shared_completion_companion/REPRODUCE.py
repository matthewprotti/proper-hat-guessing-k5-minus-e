#!/usr/bin/env python3
"""Pinned regeneration; writes only to a newly created external directory."""
from pathlib import Path
import sys,subprocess,argparse,hashlib
import scipy,numpy
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    out=a.output.resolve()
    if out==ROOT or ROOT in out.parents or out.exists():raise SystemExit('output must be new and outside package')
    if (numpy.__version__,scipy.__version__)!=('2.3.5','1.17.0'):raise SystemExit('byte replay pinned to numpy 2.3.5/scipy 1.17.0; data-only checks do not require these')
    out.mkdir(parents=True)
    rules=ROOT/'SOURCE/inherited_quota_flow_twin_rules.tsv'
    subprocess.run([sys.executable,'-B',str(ROOT/'TOOLS/pilot.py'),'--inherited-rules',str(rules),'--output',str(out/'pilot')],check=True)
    subprocess.run([sys.executable,'-B',str(ROOT/'TOOLS/envelope.py'),'--rules',str(rules),'--output',str(out/'family')],check=True)
    compared=0
    for frozen,replay in [(ROOT/'PILOT/DATA',out/'pilot/DATA'),(ROOT/'FAMILY',out/'family')]:
        paths={p.relative_to(frozen) for p in frozen.rglob('*') if p.is_file()}
        got={p.relative_to(replay) for p in replay.rglob('*') if p.is_file()}
        if paths!=got:raise RuntimeError('replay inventory mismatch')
        for rel in sorted(paths):
            if sha(frozen/rel)!=sha(replay/rel):raise RuntimeError('regeneration mismatch: '+str(rel))
            compared+=1
    subprocess.run([sys.executable,'-I','-S','-B',str(ROOT/'TOOLS/check_certificates.py'),'--family',str(out/'family'),'--pilot',str(out/'pilot')],check=True)
    print('REGENERATED_CERTIFICATE_FILES_BYTE_IDENTICAL',compared)
    print('Elapsed-time/environment receipt text is not a byte-identity target.')
if __name__=='__main__':main()
