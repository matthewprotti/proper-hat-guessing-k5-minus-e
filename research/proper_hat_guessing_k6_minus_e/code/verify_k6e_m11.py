#!/usr/bin/env python3
"""Dependency-free verifier for the K6-e proper hat-guessing construction.

This program regenerates the finite group from two displayed permutations,
classifies every orbit label under deletion of point 10, identifies all
compatible repaired pairs, and verifies the pair (4,6) used to prove
HG_P(K6-e)=10 through the twin-completion/Hall criterion.

Only Python's standard library is required.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

OMEGA = tuple(range(11))
COLORS = tuple(range(10))
BASE = (0, 1, 2, 3)
DELETED = 10
LABELS = tuple(range(4, 11))
K = 4

Perm = Tuple[int, ...]
Tuple4 = Tuple[int, int, int, int]


def cycle_permutation(n: int, cycles: Iterable[Sequence[int]]) -> Perm:
    p = list(range(n))
    for cyc in cycles:
        for i, x in enumerate(cyc):
            p[x] = cyc[(i + 1) % len(cyc)]
    return tuple(p)


def compose(p: Perm, q: Perm) -> Perm:
    """Return p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def generate_group() -> List[Perm]:
    a = cycle_permutation(11, [tuple(range(11))])
    b = cycle_permutation(11, [(2, 6, 10, 7), (3, 9, 4, 5)])
    identity = tuple(range(11))
    seen = {identity}
    order = [identity]
    queue: deque[Perm] = deque([identity])
    while queue:
        g = queue.popleft()
        for h in (a, b):
            z = compose(h, g)
            if z not in seen:
                seen.add(z)
                order.append(z)
                queue.append(z)
    return order


def orbit_function(group: Sequence[Perm], label: int) -> Dict[Tuple4, int]:
    out: Dict[Tuple4, int] = {}
    for g in group:
        t = (g[0], g[1], g[2], g[3])
        y = g[label]
        if t in out and out[t] != y:
            raise AssertionError((label, t, out[t], y))
        out[t] = y
    return out


def repair_function(F: Dict[Tuple4, int]) -> Tuple[Dict[Tuple4, int] | None, dict]:
    repaired: Dict[Tuple4, int] = {}
    deleted_count = 0
    inconsistent = 0
    illegal = 0
    hist: Counter[int] = Counter()
    examples: List[dict] = []
    for t in itertools.permutations(COLORS, K):
        tt: Tuple4 = t  # type: ignore[assignment]
        y = F[tt]
        if y != DELETED:
            repaired[tt] = y
            continue
        deleted_count += 1
        vals = []
        for pos in range(K):
            u = list(tt)
            u[pos] = DELETED
            vals.append(F[tuple(u)])  # type: ignore[arg-type]
        if len(set(vals)) != 1:
            inconsistent += 1
            if len(examples) < 3:
                examples.append({"tuple": list(tt), "replacement_values": vals})
            continue
        z = vals[0]
        if z == DELETED or z in tt or z not in COLORS:
            illegal += 1
            if len(examples) < 3:
                examples.append({"tuple": list(tt), "illegal_replacement": z})
            continue
        repaired[tt] = z
        hist[z] += 1
    ok = inconsistent == 0 and illegal == 0 and len(repaired) == 5040
    return (repaired if ok else None), {
        "repairable": ok,
        "deleted_output_tuples": deleted_count,
        "inconsistent_repairs": inconsistent,
        "illegal_repairs": illegal,
        "replacement_histogram": dict(sorted(hist.items())),
        "examples": examples,
    }


def coordinate_lines():
    for pos in range(K):
        for frozen in itertools.permutations(COLORS, K - 1):
            domain = [c for c in COLORS if c not in frozen]
            rows = [frozen[:pos] + (r,) + frozen[pos:] for r in domain]
            yield pos, frozen, domain, rows


def cycle_type(domain: Sequence[int], mapping: Dict[int, int]) -> Tuple[int, ...]:
    unseen = set(domain)
    lengths: List[int] = []
    while unseen:
        start = min(unseen)
        x = start
        length = 0
        while x in unseen:
            unseen.remove(x)
            x = mapping[x]
            length += 1
        if x != start:
            raise AssertionError((domain, mapping, start, x))
        lengths.append(length)
    return tuple(sorted(lengths))


def verify_repaired(f: Dict[Tuple4, int]) -> dict:
    illegal = sum(y in t or y not in COLORS for t, y in f.items())
    bad_lines = 0
    cycle_hist: Counter[Tuple[int, ...]] = Counter()
    for _pos, _frozen, domain, rows in coordinate_lines():
        vals = [f[t] for t in rows]
        if sorted(vals) != domain:
            bad_lines += 1
            continue
        mapping = {domain[i]: vals[i] for i in range(len(domain))}
        cycle_hist[cycle_type(domain, mapping)] += 1
    return {
        "illegal_values": illegal,
        "coordinate_lines": 2880,
        "bad_lines": bad_lines,
        "line_cycle_type_histogram": {str(k): v for k, v in sorted(cycle_hist.items())},
        "verified": illegal == 0 and bad_lines == 0,
    }


def verify_pair(alpha: Dict[Tuple4, int], beta: Dict[Tuple4, int]) -> dict:
    pointwise_equal = sum(alpha[t] == beta[t] for t in alpha)
    composition_fixed = 0
    composition_cycles: Counter[Tuple[int, ...]] = Counter()
    completion_failures = 0
    completion_contexts = 0
    for _pos, _frozen, domain, rows in coordinate_lines():
        by_input = {domain[i]: rows[i] for i in range(len(domain))}
        comp: Dict[int, int] = {}
        for r in domain:
            a = alpha[by_input[r]]
            z = beta[by_input[a]]
            comp[r] = z
            if z == r:
                composition_fixed += 1
        composition_cycles[cycle_type(domain, comp)] += 1
        for x in domain:
            for y in domain:
                candidates = [r for r in domain if r != x and r != y]
                covered = sum(
                    alpha[by_input[r]] == x or beta[by_input[r]] == y
                    for r in candidates
                )
                completion_contexts += 1
                if covered < (1 if x != y else 2):
                    completion_failures += 1
    return {
        "pointwise_equal_inputs": pointwise_equal,
        "composition_fixed_points": composition_fixed,
        "composition_cycle_type_histogram": {
            str(k): v for k, v in sorted(composition_cycles.items())
        },
        "completion_contexts": completion_contexts,
        "completion_failures": completion_failures,
        "verified": pointwise_equal == 0 and composition_fixed == 0 and completion_failures == 0,
    }


def setwise_stabilizer_orbits(group: Sequence[Perm]) -> dict:
    base_set = frozenset(BASE)
    stab = [g for g in group if frozenset(g[i] for i in BASE) == base_set]
    unseen = set(LABELS)
    orbits: List[List[int]] = []
    while unseen:
        x = min(unseen)
        orbit = {g[x] for g in stab}
        orbit &= set(LABELS)
        orbits.append(sorted(orbit))
        unseen -= orbit
    pair_orbit = {
        tuple(sorted(g[x] for x in (4, 6)))
        for g in stab
    }
    return {
        "order": len(stab),
        "orbits_on_remaining_labels": sorted(orbits),
        "orbit_of_pair_4_6": [list(p) for p in sorted(pair_orbit)],
    }


def witt_completion_check(group: Sequence[Perm]) -> dict:
    seed = (0, 1, 2, 3, 9)
    blocks = {tuple(sorted(g[i] for i in seed)) for g in group}
    four_count: Counter[Tuple[int, ...]] = Counter()
    for block in blocks:
        for subset in itertools.combinations(block, 4):
            four_count[subset] += 1
    return {
        "seed_block": list(seed),
        "blocks": len(blocks),
        "four_subsets": len(four_count),
        "four_subset_multiplicity_histogram": dict(sorted(Counter(four_count.values()).items())),
        "is_S_4_5_11": len(blocks) == 66 and len(four_count) == 330 and set(four_count.values()) == {1},
    }


def residual_degree_check(alpha: Dict[Tuple4, int], beta: Dict[Tuple4, int]) -> dict:
    # Right vertices are labelled pairs (clique vertex, visible local view).
    right_degrees: Counter[Tuple[int, Tuple[int, ...]]] = Counter()
    proper = 0
    twin_covered = 0
    residual = 0
    for clique in itertools.permutations(COLORS, K):
        available = [c for c in COLORS if c not in clique]
        for x in available:
            for y in available:
                proper += 1
                tt: Tuple4 = clique  # type: ignore[assignment]
                if alpha[tt] == x or beta[tt] == y:
                    twin_covered += 1
                    continue
                residual += 1
                colors = (x, y) + clique
                for v in range(2, 6):
                    view = tuple(colors[w] for w in range(6) if w != v and not ({v, w} == {0, 1}))
                    right_degrees[(v, view)] += 1
    hist = Counter(right_degrees.values())
    return {
        "proper_colorings": proper,
        "twin_covered": twin_covered,
        "residual_colorings": residual,
        "residual_left_degree": 4,
        "right_vertices": len(right_degrees),
        "right_degree_histogram": dict(sorted(hist.items())),
        "maximum_right_degree": max(right_degrees.values(), default=0),
        "hall_degree_condition": max(right_degrees.values(), default=0) <= 4,
    }


def canonical_table(f: Dict[Tuple4, int]) -> str:
    return "".join(",".join(map(str, t)) + f":{f[t]}\n" for t in sorted(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    cert_bytes = args.certificate.read_bytes()
    cert = json.loads(cert_bytes)
    if cert.get("generators") != {
        "a": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        "b": [[2, 6, 10, 7], [3, 9, 4, 5]],
    }:
        raise SystemExit("certificate generator mismatch")
    if cert.get("base_tuple") != list(BASE) or cert.get("deleted_point") != DELETED:
        raise SystemExit("certificate base/deletion mismatch")

    group = generate_group()
    images = {(g[0], g[1], g[2], g[3]) for g in group}
    if len(group) != 7920 or len(images) != 7920:
        raise AssertionError((len(group), len(images)))

    repaired: Dict[int, Dict[Tuple4, int]] = {}
    label_report: Dict[str, dict] = {}
    for label in LABELS:
        F = orbit_function(group, label)
        f, repair = repair_function(F)
        entry = {"repair": repair}
        if f is not None:
            line = verify_repaired(f)
            entry["line_check"] = line
            if not line["verified"]:
                raise AssertionError((label, line))
            repaired[label] = f
        label_report[str(label)] = entry

    compatible: List[List[int]] = []
    pair_report: Dict[str, dict] = {}
    for x, y in itertools.combinations(sorted(repaired), 2):
        check = verify_pair(repaired[x], repaired[y])
        pair_report[f"{x},{y}"] = check
        if check["verified"]:
            compatible.append([x, y])

    expected_repairable = sorted(cert["expected_repairable_labels"])
    expected_pairs = sorted(sorted(p) for p in cert["expected_compatible_pairs"])
    if sorted(repaired) != expected_repairable:
        raise AssertionError((sorted(repaired), expected_repairable))
    if sorted(compatible) != expected_pairs:
        raise AssertionError((sorted(compatible), expected_pairs))

    main_labels = tuple(cert["main_pair"])
    alpha = repaired[main_labels[0]]
    beta = repaired[main_labels[1]]
    main_check = verify_pair(alpha, beta)
    residual = residual_degree_check(alpha, beta)
    if not main_check["verified"] or not residual["hall_degree_condition"]:
        raise AssertionError((main_check, residual))

    report = {
        "format": "K6-e-M11-public-verification-v1",
        "claim": "HG_P(K6-e)=10",
        "certificate_sha256": hashlib.sha256(cert_bytes).hexdigest(),
        "group_order": len(group),
        "distinct_ordered_four_images": len(images),
        "setwise_stabilizer": setwise_stabilizer_orbits(group),
        "witt_completion_label_9": witt_completion_check(group),
        "labels": label_report,
        "pairs": pair_report,
        "repairable_labels": sorted(repaired),
        "compatible_pairs": compatible,
        "main_pair": list(main_labels),
        "main_pair_check": main_check,
        "residual_degree_check": residual,
        "alpha_sha256": hashlib.sha256(canonical_table(alpha).encode()).hexdigest(),
        "beta_sha256": hashlib.sha256(canonical_table(beta).encode()).hexdigest(),
        "verified": True,
    }

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "verification_report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
        (args.output_dir / "alpha.tsv").write_text(canonical_table(alpha))
        (args.output_dir / "beta.tsv").write_text(canonical_table(beta))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
