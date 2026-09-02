#!/usr/bin/env python3
"""Generate exact CNF instances for proper-coloring hat guessing.

Variable x[v, view, g] is true iff vertex v guesses color g on the
attainable ordered neighbor-color view.  We restrict to guesses not visible
in the view; this is w.l.o.g. for proper colorings because a visible color can
never equal the player's own color.

CNF:
  * exactly one legal guess for every attainable local view;
  * at least one correct vertex for every proper q-coloring.

The script also emits a JSON map sufficient to decode and independently check
SAT models.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Coloring = Tuple[int, ...]
View = Tuple[int, ...]
Key = Tuple[int, View, int]


@dataclass(frozen=True)
class Graph:
    name: str
    n: int
    edges: Tuple[Tuple[int, int], ...]

    @property
    def neighbors(self) -> Tuple[Tuple[int, ...], ...]:
        ns: List[List[int]] = [[] for _ in range(self.n)]
        for u, v in self.edges:
            ns[u].append(v)
            ns[v].append(u)
        return tuple(tuple(sorted(a)) for a in ns)


def get_graph(name: str, n: int | None = None) -> Graph:
    if name.startswith("C"):
        n0 = int(name[1:]) if len(name) > 1 else n
        if n0 is None or n0 < 3:
            raise ValueError("cycle requires n>=3")
        edges = tuple(sorted({tuple(sorted((i, (i + 1) % n0))) for i in range(n0)}))
        return Graph(f"C{n0}", n0, edges)
    if name == "K5-e":
        n0 = 5
    elif name == "K4-e":
        n0 = 4
    elif name == "Kn-e":
        if n is None or n < 3:
            raise ValueError("Kn-e requires --n >= 3")
        n0 = n
    else:
        raise ValueError(f"unknown graph {name}")
    # The omitted edge is {0,1}; these are the nonadjacent twins.
    edges = tuple((u, v) for u in range(n0) for v in range(u + 1, n0) if (u, v) != (0, 1))
    return Graph(f"K{n0}-e", n0, edges)


def proper_colorings(g: Graph, q: int) -> List[Coloring]:
    # Specialized enumeration for K_n-e avoids q^n scanning.
    if g.name.startswith("K") and g.name.endswith("-e"):
        clique = tuple(range(2, g.n))
        out: List[Coloring] = []
        for clique_colors in itertools.permutations(range(q), len(clique)):
            used = set(clique_colors)
            remaining = [c for c in range(q) if c not in used]
            for a in remaining:
                for b in remaining:
                    c = [0] * g.n
                    c[0], c[1] = a, b
                    for v, col in zip(clique, clique_colors):
                        c[v] = col
                    out.append(tuple(c))
        return out
    return [
        c
        for c in itertools.product(range(q), repeat=g.n)
        if all(c[u] != c[v] for u, v in g.edges)
    ]


def canonical_sb_unit(g: Graph, q: int, var: Dict[Key, int]) -> int | None:
    """A sound global-color-symmetry breaker.

    For cycles: map a same-color view and its (different) guess to (0,0)->1.
    For K_n-e: map twin 0's ordered clique view and its guess to
    (0,1,...,n-3)->n-2.  This is w.l.o.g. under one global color permutation.
    """
    if g.name.startswith("C"):
        key = (0, (0, 0), 1)
    elif g.name.startswith("K") and g.name.endswith("-e"):
        view = tuple(range(g.n - 2))
        key = (0, view, g.n - 2)
    else:
        return None
    return var.get(key)


def generate(g: Graph, q: int, outdir: Path, symmetry_break: bool) -> dict:
    ns = g.neighbors
    colorings = proper_colorings(g, q)
    views: List[set[View]] = [set() for _ in range(g.n)]
    for c in colorings:
        for v in range(g.n):
            views[v].add(tuple(c[w] for w in ns[v]))

    keys: List[Key] = []
    var: Dict[Key, int] = {}
    for v in range(g.n):
        for p in sorted(views[v]):
            for guess in range(q):
                if guess not in p:
                    key = (v, p, guess)
                    var[key] = len(keys) + 1
                    keys.append(key)

    clauses: List[List[int]] = []
    clause_kind: List[str] = []

    # Exactly one guess per attainable view: ALO + pairwise AMO.
    local_view_count = 0
    for v in range(g.n):
        for p in sorted(views[v]):
            local_view_count += 1
            lits = [var[(v, p, guess)] for guess in range(q) if (v, p, guess) in var]
            assert lits
            clauses.append(lits)
            clause_kind.append("view_at_least_one")
            for i in range(len(lits)):
                for j in range(i + 1, len(lits)):
                    clauses.append([-lits[i], -lits[j]])
                    clause_kind.append("view_at_most_one")

    # Winning condition for every proper coloring.
    for c in colorings:
        lits = []
        for v in range(g.n):
            p = tuple(c[w] for w in ns[v])
            key = (v, p, c[v])
            assert key in var, (c, v, p, c[v])
            lits.append(var[key])
        clauses.append(lits)
        clause_kind.append("coloring_covered")

    sb_lit = None
    if symmetry_break:
        sb_lit = canonical_sb_unit(g, q, var)
        if sb_lit is None:
            raise RuntimeError("requested symmetry breaker unavailable")
        clauses.append([sb_lit])
        clause_kind.append("global_color_symmetry_break")

    outdir.mkdir(parents=True, exist_ok=True)
    stem = f"{g.name.replace('-', '_')}_q{q}" + ("_sb" if symmetry_break else "")
    cnf_path = outdir / f"{stem}.cnf"
    map_path = outdir / f"{stem}.map.json"
    meta_path = outdir / f"{stem}.meta.json"

    with cnf_path.open("w", encoding="ascii") as f:
        f.write(f"c proper hat guessing instance: {g.name}, q={q}\n")
        f.write("c variables x[v,ordered-neighbor-view,guess]\n")
        f.write(f"p cnf {len(keys)} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")

    mapping = {
        "format": "proper-hat-cnf-map-v1",
        "graph": g.name,
        "q": q,
        "vertices": list(range(g.n)),
        "edges": [list(e) for e in g.edges],
        "neighbor_order": [list(a) for a in ns],
        "variables": [
            {"id": i + 1, "vertex": v, "view": list(p), "guess": guess}
            for i, (v, p, guess) in enumerate(keys)
        ],
        "symmetry_break_literal": sb_lit,
    }
    map_path.write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n")

    counts = {k: clause_kind.count(k) for k in sorted(set(clause_kind))}
    meta = {
        "format": "proper-hat-instance-metadata-v1",
        "graph": g.name,
        "q": q,
        "proper_colorings": len(colorings),
        "local_views": local_view_count,
        "legal_one_hot_variables": len(keys),
        "clauses": len(clauses),
        "clause_counts": counts,
        "symmetry_break": symmetry_break,
        "symmetry_break_literal": sb_lit,
        "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        "map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    return {**meta, "cnf": str(cnf_path), "map": str(map_path), "meta": str(meta_path)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("graph", help="C5, K5-e, Kn-e")
    ap.add_argument("q", type=int)
    ap.add_argument("--n", type=int)
    ap.add_argument("--outdir", type=Path, default=Path("instances"))
    ap.add_argument("--symmetry-break", action="store_true")
    args = ap.parse_args()
    g = get_graph(args.graph, args.n)
    meta = generate(g, args.q, args.outdir, args.symmetry_break)
    print(json.dumps(meta, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
