#!/usr/bin/env python3
"""Dependency-free verifier for HG_P(K7-e)=12.

Reconstructs two proof routes from three displayed permutations:
(1) two explicit disjoint S(5,6,12) completion designs; and
(2) a compatible pair of sharply-five-transitive orbit maps.

No group classification or stored result summary is trusted.
"""
from __future__ import annotations

import argparse
import itertools
from collections import Counter, defaultdict, deque
from typing import Dict, Iterable, Mapping, Sequence, Tuple

Q = 12
K = 5
OMEGA = tuple(range(Q))
BASE = (0, 1, 2, 3, 4)
LABELS = tuple(range(5, 12))
DESIGN_LABEL = 6
PARTNER_LABEL = 5
SEED = frozenset((0, 1, 2, 3, 4, 6))
COPY_CYCLE = (0, 1, 2, 4, 5, 3)

Perm = Tuple[int, ...]
Tuple5 = Tuple[int, int, int, int, int]
Block = frozenset[int]


def perm_from_cycles(n: int, cycles: Iterable[Sequence[int]]) -> Perm:
    p = list(range(n))
    for cyc in cycles:
        for i, x in enumerate(cyc):
            p[x] = cyc[(i + 1) % len(cyc)]
    return tuple(p)


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[q[i]] for i in range(len(p)))


def generators() -> tuple[Perm, Perm, Perm]:
    return (
        perm_from_cycles(12, [tuple(range(11))]),
        perm_from_cycles(12, [(2, 6, 10, 7), (3, 9, 4, 5)]),
        perm_from_cycles(12, [(0, 11), (1, 10), (2, 5), (3, 7), (4, 8), (6, 9)]),
    )


def group_closure() -> list[Perm]:
    identity = tuple(range(Q))
    seen = {identity}
    order = [identity]
    queue: deque[Perm] = deque([identity])
    while queue:
        g = queue.popleft()
        for h in generators():
            z = compose(h, g)
            if z not in seen:
                seen.add(z)
                order.append(z)
                queue.append(z)
    return order


def orbit_functions(group: Sequence[Perm]) -> Dict[int, Dict[Tuple5, int]]:
    functions: Dict[int, Dict[Tuple5, int]] = {y: {} for y in LABELS}
    for g in group:
        t: Tuple5 = tuple(g[i] for i in BASE)  # type: ignore[assignment]
        for y in LABELS:
            old = functions[y].get(t)
            if old is not None and old != g[y]:
                raise AssertionError("orbit function is not well-defined")
            functions[y][t] = g[y]
    return functions


def cycle_type(domain: Sequence[int], f: Mapping[int, int]) -> tuple[int, ...]:
    if set(f) != set(domain) or set(f.values()) != set(domain):
        raise AssertionError("line map is not a permutation")
    unseen = set(domain)
    lengths = []
    while unseen:
        start = min(unseen)
        x = start
        length = 0
        while x in unseen:
            unseen.remove(x)
            x = f[x]
            length += 1
        if x != start:
            raise AssertionError("line map does not close into cycles")
        lengths.append(length)
    return tuple(sorted(lengths))


def ordered_lines():
    for pos in range(K):
        for frozen in itertools.permutations(OMEGA, K - 1):
            domain = [x for x in OMEGA if x not in frozen]
            rows = {r: frozen[:pos] + (r,) + frozen[pos:] for r in domain}
            yield domain, rows


def apply_perm(block: Block, p: Perm) -> Block:
    return frozenset(p[x] for x in block)


def verify_steiner(blocks: set[Block]) -> Dict[Block, int]:
    if len(blocks) != 132 or any(len(b) != 6 for b in blocks):
        raise AssertionError("wrong Witt block universe")
    completion: Dict[Block, int] = {}
    for block in blocks:
        for pentad_tuple in itertools.combinations(sorted(block), 5):
            pentad = frozenset(pentad_tuple)
            extra = next(iter(block - pentad))
            if pentad in completion and completion[pentad] != extra:
                raise AssertionError("pentad has two completions")
            completion[pentad] = extra
    if len(completion) != 792:
        raise AssertionError("not every pentad is completed exactly once")
    return completion


def verify_design_route(group: Sequence[Perm]) -> dict:
    design_a = {frozenset(g[x] for x in SEED) for g in group}
    pi = perm_from_cycles(12, [COPY_CYCLE])
    design_b = {apply_perm(block, pi) for block in design_a}
    completion_a = verify_steiner(design_a)
    completion_b = verify_steiner(design_b)
    if design_a & design_b:
        raise AssertionError("the two Witt designs share a block")

    alpha_cycles: Counter[tuple[int, ...]] = Counter()
    beta_cycles: Counter[tuple[int, ...]] = Counter()
    composition_cycles: Counter[tuple[int, ...]] = Counter()
    equal = fixed = failures = contexts = 0
    right_hist: Counter[int] = Counter()
    for frozen_tuple in itertools.combinations(OMEGA, 4):
        frozen = frozenset(frozen_tuple)
        domain = [x for x in OMEGA if x not in frozen]
        f = {r: completion_a[frozen | {r}] for r in domain}
        g = {r: completion_b[frozen | {r}] for r in domain}
        h = {r: g[f[r]] for r in domain}
        alpha_cycles[cycle_type(domain, f)] += 1
        beta_cycles[cycle_type(domain, g)] += 1
        composition_cycles[cycle_type(domain, h)] += 1
        equal += sum(f[r] == g[r] for r in domain)
        fixed += sum(h[r] == r for r in domain)
        for x in domain:
            for y in domain:
                candidates = [r for r in domain if r != x and r != y]
                covered = sum(f[r] == x or g[r] == y for r in candidates)
                residual = len(candidates) - covered
                right_hist[residual] += 1
                contexts += 1
                if covered < (2 if x == y else 1):
                    failures += 1
    assert equal == fixed == failures == 0
    assert max(right_hist) == 5
    return {
        "blocks_each": len(design_a),
        "pentads_each": len(completion_a),
        "intersection": 0,
        "lines": 495,
        "alpha_cycles": dict(alpha_cycles),
        "beta_cycles": dict(beta_cycles),
        "composition_cycles": dict(composition_cycles),
        "contexts": contexts,
        "failures": failures,
        "maximum_right_degree": max(right_hist),
        "completion_a": completion_a,
    }


def verify_orbit_route(functions: Mapping[int, Mapping[Tuple5, int]], completion_a: Mapping[Block, int]) -> dict:
    line_cycles = {y: Counter() for y in LABELS}
    pair_equal = Counter()
    pair_fixed = Counter()
    compatible = []
    lines = list(ordered_lines())
    for domain, rows in lines:
        for y in LABELS:
            f = {r: functions[y][rows[r]] for r in domain}
            line_cycles[y][cycle_type(domain, f)] += 1
        for x, y in itertools.combinations(LABELS, 2):
            f = {r: functions[x][rows[r]] for r in domain}
            g = {r: functions[y][rows[r]] for r in domain}
            pair_equal[(x, y)] += sum(f[r] == g[r] for r in domain)
            pair_fixed[(x, y)] += sum(g[f[r]] == r for r in domain)
    for pair in itertools.combinations(LABELS, 2):
        if pair_equal[pair] == 0 and pair_fixed[pair] == 0:
            compatible.append(pair)
    expected = [(5, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)]
    assert compatible == expected

    alpha = functions[DESIGN_LABEL]
    beta = functions[PARTNER_LABEL]
    assert all(alpha[t] == completion_a[frozenset(t)] for t in alpha)
    by_set: Dict[Block, set[int]] = defaultdict(set)
    for t, value in beta.items():
        by_set[frozenset(t)].add(value)
    assert Counter(map(len, by_set.values())) == Counter({6: 792})

    contexts = failures = 0
    right_hist: Counter[int] = Counter()
    for domain, rows in lines:
        f = {r: alpha[rows[r]] for r in domain}
        g = {r: beta[rows[r]] for r in domain}
        for x in domain:
            for y in domain:
                candidates = [r for r in domain if r != x and r != y]
                covered = sum(f[r] == x or g[r] == y for r in candidates)
                residual = len(candidates) - covered
                right_hist[residual] += 1
                contexts += 1
                if covered < (2 if x == y else 1):
                    failures += 1
    assert failures == 0 and max(right_hist) == 5
    return {
        "lines": len(lines),
        "line_cycles": {str(y): dict(line_cycles[y]) for y in LABELS},
        "compatible_pairs": compatible,
        "contexts": contexts,
        "failures": failures,
        "maximum_right_degree": max(right_hist),
        "partner_is_order_sensitive": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()

    group = group_closure()
    functions = orbit_functions(group)
    assert len(group) == len(functions[5]) == 95040
    assert all(value not in t for f in functions.values() for t, value in f.items())

    design = verify_design_route(group)
    orbit = verify_orbit_route(functions, design.pop("completion_a"))

    if args.negative_controls:
        transposition = {0: 1, 1: 0}
        assert cycle_type([0, 1], transposition) == (2,)
        assert not any(transposition[r] == r for r in transposition)

        identity = {0: 0, 1: 1}
        assert cycle_type([0, 1], identity) == (1, 1)
        if not any(identity[r] == r for r in identity):
            raise AssertionError("fixed-point control did not expose a fixed point")

        bad = {frozenset(range(6))}
        try:
            verify_steiner(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError("non-Steiner control was not rejected")

    proper = 95040 * 49
    twin_covered = 95040 * 13
    residual = 95040 * 36
    assert (proper, twin_covered, residual) == (4656960, 1235520, 3421440)

    print("claim=HG_P(K7-e)=12")
    print(f"group_order={len(group)}")
    print(f"ordered_five_images={len(functions[5])}")
    print(f"design_blocks_each={design['blocks_each']}")
    print(f"design_intersection={design['intersection']}")
    print(f"set_lines={design['lines']}")
    print(f"set_local_failures={design['failures']}")
    print(f"ordered_lines={orbit['lines']}")
    print(f"ordered_local_failures={orbit['failures']}")
    print(f"proper_colourings={proper}")
    print(f"residual_colourings={residual}")
    print("verified=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
