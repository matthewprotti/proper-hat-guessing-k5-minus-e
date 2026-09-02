#!/usr/bin/env python3
"""Minimal pinned verifier for the claimed K5-e, q=8 winning strategy."""
from __future__ import annotations
import hashlib
import itertools
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: verify_K5_e_q8_pinned.py STRATEGY.json")
path = Path(sys.argv[1])
raw = path.read_bytes()
obj = json.loads(raw)
S = {}
for e in obj.get("strategy", []):
    k = (int(e["vertex"]), tuple(map(int, e["view"])))
    if k in S:
        raise SystemExit(f"duplicate decision {k}")
    S[k] = int(e["guess"])

q, n = 8, 5
edges = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) != (0, 1)]
N = [tuple(w for w in range(n) if w != v and (min(v, w), max(v, w)) in edges)
     for v in range(n)]
proper = []
for c234 in itertools.permutations(range(q), 3):
    rem = [x for x in range(q) if x not in c234]
    for a in rem:
        for b in rem:
            proper.append((a, b, *c234))

attainable = {(v, tuple(c[w] for w in N[v])) for c in proper for v in range(n)}
assert len(proper) == 8400
assert len(attainable) == 6720
if set(S) != attainable:
    raise SystemExit(f"strategy domain mismatch: missing={len(attainable-set(S))}, extra={len(set(S)-attainable)}")
for (v, p), g in S.items():
    if not (0 <= g < q) or g in p:
        raise SystemExit(f"illegal guess at {(v,p)}: {g}")

hist = [0] * 6
for c in proper:
    hits = sum(S[(v, tuple(c[w] for w in N[v]))] == c[v] for v in range(n))
    hist[hits] += 1
    if hits == 0:
        raise SystemExit(f"uncovered proper coloring: {c}")
print(json.dumps({
    "claim": "HGP(K5-e)>=8",
    "q": 8,
    "proper_colorings_checked": len(proper),
    "strategy_entries": len(S),
    "correct_guess_histogram": {str(i): x for i, x in enumerate(hist) if x},
    "strategy_sha256": hashlib.sha256(raw).hexdigest(),
    "verified": True,
}, indent=2, sort_keys=True))
