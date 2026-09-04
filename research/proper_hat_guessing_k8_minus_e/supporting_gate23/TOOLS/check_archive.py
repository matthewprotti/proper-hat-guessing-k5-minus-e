#!/usr/bin/env python3
"""Data-only ZIP identity, safety, inventory and member-hash inspection.
Does not extract files or execute any content from the archive.
"""
import argparse,hashlib,zipfile,stat
from pathlib import PurePosixPath
def safe(name):
    p=PurePosixPath(name.rstrip('/'))
    if p.is_absolute() or '\\' in name or any(ord(c)<32 for c in name):
        raise ValueError('unsafe member name')
    if any(x in ('','.','..') for x in name.rstrip('/').split('/')):
        raise ValueError('noncanonical member name')
    return p
def main():
    a=argparse.ArgumentParser();a.add_argument('archive');a.add_argument('--sha256',required=True)
    ns=a.parse_args()
    with open(ns.archive,'rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    if actual!=ns.sha256:raise SystemExit('outer SHA-256 mismatch')
    with zipfile.ZipFile(ns.archive) as z:
        names=set();total=0
        for i in z.infolist():
            safe(i.filename)
            if i.filename in names:raise ValueError('duplicate member')
            names.add(i.filename);total+=i.file_size
            mode=i.external_attr>>16
            if stat.S_ISLNK(mode) or i.flag_bits&1:raise ValueError('symlink or encrypted member')
            typ=stat.S_IFMT(mode)
            if typ not in (0,stat.S_IFREG,stat.S_IFDIR):raise ValueError('special member')
        if total>256*1024*1024:raise ValueError('uncompressed size bound exceeded')
        if z.testzip() is not None:raise ValueError('CRC error')
        roots={PurePosixPath(n).parts[0] for n in names}
        if len(roots)!=1:raise ValueError('not a single rooted archive')
        root=next(iter(roots))+'/'
        mn=root+'MANIFEST.sha256'
        if mn not in names:raise ValueError('manifest absent')
        expected={}
        for line in z.read(mn).decode().splitlines():
            h,rel=line.split('  ',1);safe(rel)
            if len(h)!=64 or any(c not in '0123456789abcdef' for c in h) or rel in expected:
                raise ValueError('bad manifest entry')
            expected[rel]=h
        files={n[len(root):] for n in names if not n.endswith('/') and n!=mn}
        if files!=set(expected):raise ValueError('inventory mismatch')
        for rel,h in expected.items():
            if hashlib.sha256(z.read(root+rel)).hexdigest()!=h:raise ValueError('member digest mismatch')
    print('DATA_ONLY_ZIP_CHECK PASS',actual,'members',len(names),'manifest_files',len(expected))
if __name__=='__main__':main()
