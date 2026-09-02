#!/usr/bin/env python3
"""Check that a proper-hat strategy induces a total satisfying assignment of a DIMACS CNF.

This checker is deliberately mechanical: it does not enumerate colorings or know the
hat game.  It uses the emitted variable map to translate each strategy decision to
Boolean literals, then evaluates every DIMACS clause.  It therefore cross-checks the
independent game verifier through a different representation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def parse_cnf(path: Path):
    nvars = nclauses = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    for line_no, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ["p", "cnf"]:
                raise ValueError(f"bad DIMACS header at line {line_no}")
            nvars, nclauses = map(int, parts[2:])
            continue
        if nvars is None:
            raise ValueError("clause before DIMACS header")
        for tok in line.split():
            lit = int(tok)
            if lit == 0:
                clauses.append(pending)
                pending = []
            else:
                if abs(lit) > nvars:
                    raise ValueError(f"literal {lit} outside 1..{nvars}")
                pending.append(lit)
    if pending:
        raise ValueError("unterminated DIMACS clause")
    if nvars is None or nclauses is None:
        raise ValueError("missing DIMACS header")
    if len(clauses) != nclauses:
        raise ValueError(f"header says {nclauses} clauses, parsed {len(clauses)}")
    return nvars, clauses


def key(vertex: int, view: list[int] | tuple[int, ...], guess: int):
    return vertex, tuple(view), guess


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf", type=Path)
    ap.add_argument("mapping", type=Path)
    ap.add_argument("strategy", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--model", type=Path)
    args = ap.parse_args()

    nvars, clauses = parse_cnf(args.cnf)
    mapping = json.loads(args.mapping.read_text())
    strategy_obj = json.loads(args.strategy.read_text())

    variables = mapping["variables"]
    if len(variables) != nvars:
        raise SystemExit(f"mapping has {len(variables)} variables; CNF has {nvars}")
    id_by_key = {}
    view_groups: dict[tuple[int, tuple[int, ...]], list[int]] = {}
    for item in variables:
        vid = int(item["id"])
        k = key(int(item["vertex"]), item["view"], int(item["guess"]))
        if k in id_by_key:
            raise SystemExit(f"duplicate map key {k}")
        id_by_key[k] = vid
        view_groups.setdefault((k[0], k[1]), []).append(vid)

    selected: dict[tuple[int, tuple[int, ...]], int] = {}
    for item in strategy_obj["strategy"]:
        vg = (int(item["vertex"]), tuple(map(int, item["view"])))
        guess = int(item["guess"])
        if vg in selected:
            raise SystemExit(f"duplicate strategy view {vg}")
        selected[vg] = guess

    missing = sorted(set(view_groups) - set(selected))
    extra = sorted(set(selected) - set(view_groups))
    illegal = []
    true_vars: set[int] = set()
    for vg, guess in selected.items():
        k = (vg[0], vg[1], guess)
        vid = id_by_key.get(k)
        if vid is None:
            illegal.append([vg[0], list(vg[1]), guess])
        else:
            true_vars.add(vid)

    bad_clauses = []
    if not (missing or extra or illegal):
        for idx, clause in enumerate(clauses, 1):
            if not any((lit > 0 and lit in true_vars) or (lit < 0 and -lit not in true_vars)
                       for lit in clause):
                bad_clauses.append({"index": idx, "clause": clause})
                if len(bad_clauses) >= 25:
                    break

    winning = not (missing or extra or illegal or bad_clauses)
    report = {
        "format": "proper-hat-cnf-assignment-verification-v1",
        "graph": mapping.get("graph"),
        "q": mapping.get("q"),
        "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
        "map_sha256": hashlib.sha256(args.mapping.read_bytes()).hexdigest(),
        "strategy_sha256": hashlib.sha256(args.strategy.read_bytes()).hexdigest(),
        "variables": nvars,
        "clauses": len(clauses),
        "true_variables": len(true_vars),
        "missing_views": [[v, list(p)] for v, p in missing[:25]],
        "extra_views": [[v, list(p)] for v, p in extra[:25]],
        "illegal_choices": illegal[:25],
        "first_unsatisfied_clauses": bad_clauses,
        "cnf_satisfied": winning,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text)
    if args.model and winning:
        lits = [str(i if i in true_vars else -i) for i in range(1, nvars + 1)]
        args.model.write_text("s SATISFIABLE\n" + "v " + " ".join(lits) + " 0\n")
    return 0 if winning else 1


if __name__ == "__main__":
    raise SystemExit(main())
