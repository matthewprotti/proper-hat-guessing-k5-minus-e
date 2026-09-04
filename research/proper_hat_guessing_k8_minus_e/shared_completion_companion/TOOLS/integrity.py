"""Read-only file inventory and manifest checks. Not a theorem prover."""
from pathlib import Path,PurePosixPath
import hashlib,stat

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def manifest_check(root):
    root=Path(root).resolve()
    expected={}
    for line in (root/'MANIFEST.sha256').read_text().splitlines():
        if not line:continue
        if len(line)<67 or line[64:66]!='  ':raise ValueError('bad manifest line')
        h,name=line[:64],line[66:]
        if len(h)!=64 or any(c not in '0123456789abcdef' for c in h):raise ValueError('bad digest')
        pp=PurePosixPath(name)
        if pp.is_absolute() or '\\' in name or any(ord(c)<32 for c in name) or any(x in ('','.','..') for x in name.split('/')):
            raise ValueError('unsafe path')
        if pp.as_posix()!=name or name in expected or name=='MANIFEST.sha256':raise ValueError('alias/duplicate manifest entry')
        p=root/name
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):raise ValueError('unsafe or missing member')
        expected[name]=h
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.sha256'}
    if actual!=set(expected):raise ValueError('manifest inventory mismatch')
    for name,h in expected.items():
        if digest(root/name)!=h:raise ValueError('hash mismatch: '+name)
    return expected
