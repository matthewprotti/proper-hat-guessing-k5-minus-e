#!/usr/bin/env python3
"""Independent exhaustive verifier for proper-hat strategy JSON files."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

View = Tuple[int, ...]


def enumerate_proper(n: int, q: int, edges: List[Tuple[int, int]]):
    # Deliberately independent simple implementation.
    for c in itertools.product(range(q), repeat=n):
        if all(c[u] != c[v] for u, v in edges):
            yield c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("strategy", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    raw = args.strategy.read_bytes()
    obj = json.loads(raw)
    if obj.get("format") != "proper-hat-strategy-v1":
        raise SystemExit("unsupported strategy format")
    q = int(obj["q"])
    vertices = list(map(int, obj["vertices"]))
    n = len(vertices)
    if vertices != list(range(n)):
        raise SystemExit("vertices must be 0..n-1")
    edges = [tuple(map(int, e)) for e in obj["edges"]]
    neighbor_order = [tuple(map(int, x)) for x in obj["neighbor_order"]]

    expected_ns = [[] for _ in range(n)]
    for u, v in edges:
        if not (0 <= u < v < n):
            raise SystemExit(f"invalid or noncanonical edge {(u,v)}")
        expected_ns[u].append(v)
        expected_ns[v].append(u)
    expected_ns = [tuple(sorted(x)) for x in expected_ns]
    if neighbor_order != expected_ns:
        raise SystemExit("neighbor_order does not match edges")

    strategy: Dict[Tuple[int, View], int] = {}
    malformed = []
    for e in obj["strategy"]:
        key = (int(e["vertex"]), tuple(map(int, e["view"])))
        guess = int(e["guess"])
        if key in strategy:
            malformed.append({"duplicate": [key[0], list(key[1])]})
        strategy[key] = guess

    attainable = [set() for _ in range(n)]
    colorings = list(enumerate_proper(n, q, edges))
    for c in colorings:
        for v in range(n):
            attainable[v].add(tuple(c[w] for w in neighbor_order[v]))

    missing = []
    extra = []
    illegal = []
    for v in range(n):
        for p in attainable[v]:
            key = (v, p)
            if key not in strategy:
                missing.append([v, list(p)])
            else:
                g = strategy[key]
                if not (0 <= g < q) or g in p:
                    illegal.append([v, list(p), g])
    for (v, p), g in strategy.items():
        if not (0 <= v < n) or p not in attainable[v]:
            extra.append([v, list(p), g])

    failures = []
    histogram: Counter[int] = Counter()
    if not (malformed or missing or extra or illegal):
        for c in colorings:
            correct = 0
            for v in range(n):
                p = tuple(c[w] for w in neighbor_order[v])
                correct += int(strategy[(v, p)] == c[v])
            histogram[correct] += 1
            if correct == 0 and len(failures) < 25:
                failures.append(list(c))

    report = {
        "format": "proper-hat-verification-v1",
        "strategy_file": args.strategy.name,
        "strategy_sha256": hashlib.sha256(raw).hexdigest(),
        "graph": obj.get("graph"),
        "q": q,
        "proper_colorings_checked": len(colorings),
        "attainable_local_views": sum(map(len, attainable)),
        "strategy_entries": len(strategy),
        "malformed": malformed[:25],
        "missing": missing[:25],
        "extra": extra[:25],
        "illegal": illegal[:25],
        "first_uncovered_colorings": failures,
        "correct_guess_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "winning": not (malformed or missing or extra or illegal or failures),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    return 0 if report["winning"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
