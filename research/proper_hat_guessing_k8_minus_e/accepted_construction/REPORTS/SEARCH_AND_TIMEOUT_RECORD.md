# Search and timeout record

This file separates exploratory search from theorem evidence.

## Searches that did not settle the theorem

- Ordinary `PGL(2,13)`-equivariant coordinate-line permutation twins were
  attacked by SAT and exact linear-algebra relaxations. The strongest exact
  scout found a `GF(2)` inconsistency for a single line-permutation selector.
  That rules out only that strict symmetry/line ansatz and is not used in the
  positive proof.
- Twisted `PGL` / `PSL(2,13)` line-selector searches reached time limits. A
  timeout is no evidence for either existence or nonexistence.
- Full equivariant SAT instances also ran without a conclusive solver status
  before the explicit matching construction was found. They are not part of
  the proof.
- A direct local-search strategy reached small residual counts but did not
  produce the accepted strategy. Those heuristic residues are not evidence.

## Positive search path

For any fixed pair of equivariant twin rules, the remaining normalized
colourings form a bipartite matching problem against normalized labelled
clique views. The first deterministic `first/second available colour` rule had
matching deficiency 660. A pseudorandom seed-1 rule had deficiency one and
seed 2 had deficiency zero.

To remove dependence on a library-specific shuffle, the search then tested a
simple explicit index rule. The first hand-specified formula was:

```text
alpha_index = (a+b+c) mod 8
beta_index  = (a+2b+3c+1) mod 8
if equal, increment beta_index mod 8
```

It also yielded a perfect matching. This formula, not the earlier random
seed, is the construction sealed in the theorem package.

A separate 300-seed random experiment found 277 perfect matchings and 23
instances of deficiency one. This suggests a robust expansion phenomenon,
but no probabilistic theorem is claimed and the statistic is not load-bearing.
