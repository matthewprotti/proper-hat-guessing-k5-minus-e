# `K_8-e` result report

## Status

```text
CLAIM CANDIDATE:
HG_P(K8-e)=14

MATHEMATICAL STATUS:
COMPLETE COMPUTER-ASSISTED PROOF CANDIDATE

REVIEW STATUS:
INDEPENDENT ADVERSARIAL REVIEW PENDING

PUBLICATION STATUS:
PRIVATE / NOT PUBLICLY TIMESTAMPED BY THIS PACKAGE
```

## Executive result

The source upper bound gives `HG_P(K8-e) <= 14`. A complete explicit
`PGL(2,13)`-equivariant local strategy with fourteen colours has now been
constructed and independently checked. The strategy wins on all 138,378,240
proper colourings of `K8-e`.

Unlike the `n=5,6,7` constructions, the new proof does not force the residual
right degree below the clique size by a pair of compatible line permutations.
Instead, a compact formula fixes the twin rules and a global matching saturates
the 48,510 residual normalized colouring orbits. This is a genuine change of
mechanism.

## Compact twin formula

After unique projective normalization of the first three clique colours to
`(infinity,0,1)`, write the remaining three colours as `(a,b,c)` and list the
eight available colours increasingly as `d_0,...,d_7`. The twins select

```text
i = (a+b+c) mod 8
j = (a+2b+3c+1) mod 8
if j=i, replace j by j+1 mod 8
alpha = d_i
beta  = d_j
```

The pullback under the inverse normalizer gives the full twin rules.

## Exact finite objects

| Object | Count | SHA-256 |
|---|---:|---|
| Twin-rule rows | 990 | `6a9ee969be6f7ae217d6b103d03b117cb2b56142df9b5c2fab4c2084c8cc849d` |
| Clique-view rows | 53,460 | `c899e85b4e52825509baf8e00572555f713e27f881be2800ad8a4371f4b37acb` |
| Residual matching rows | 48,510 | `b739d1fecabfce888a7cd25f3ed0da1c329c0f29ffb772283ff99b8dd61a8982` |

## Workload and outcome

```text
PGL(2,13) order:                         2,184
normalized clique tuples:                  990
normalized proper-colouring orbits:     63,360
twin-covered orbits:                    14,850
residual orbits:                         48,510
attainable labelled clique-view orbits: 53,460
residual orbit edges:                   291,060
saturating matching size:                48,510
normalized coverage failures:                 0
full proper colourings represented: 138,378,240
full coverage failures:                       0
```

The residual right-degree distribution is:

```text
degree 1:     45
degree 2:    446
degree 3:  2,448
degree 4:  7,694
degree 5: 15,394
degree 6: 17,591
degree 7:  9,249
degree 8:    593
```

The maximum right degree is eight. Accordingly, the earlier local
`right-degree <= clique-size` sufficient criterion does not establish this
case. The explicit global matching does.

## Search record

Several stricter symmetry ansatzes were tested before the full matching was
found. In particular, an ordinary `PGL(2,13)`-equivariant coordinate-line
permutation selector is inconsistent already over `GF(2)`. Twisted/PSL and
SAT searches were exploratory and are not premises of the theorem. The
positive strategy was found by testing fixed equivariant twin rules against
the residual orbit matching problem. The displayed compact formula was the
first simple hand-specified index rule tested and produced a perfect matching.

A 300-seed random-twin scout found a perfect residual matching in 277 cases
and deficiency one in the remaining 23. That observation motivates a future
probabilistic or expansion theorem, but it is not used in the proof.

## Trust boundary

Load-bearing:

- the source upper bound;
- the projective normalization formula;
- the three frozen strategy/matching tables;
- the data-only verifier; and
- the direct full-colouring verifier.

Not load-bearing:

- SAT timeouts;
- random-search frequencies;
- group-classification terminology;
- unpublished search logs; or
- any conjecture for general `n`.

## Corrected count note

The exact number of proper fourteen-colourings is

\[
(14)_6\,8^2=138,378,240.
\]

An earlier exploratory note contained an extra factor of ten. The package,
certificates, and both final verifiers use the corrected value.
