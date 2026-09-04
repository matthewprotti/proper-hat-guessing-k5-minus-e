# Classification of the 23 deficient random rules

## Exact reconstruction

The original experiment used `std::mt19937(seed)` and, independently in each
of the 990 normalized tail fibres, `std::shuffle` of the eight available
colours; the first two shuffled colours were the distinct twin guesses.

For seeds 1 through 300 the exact deficient list is:

```text
1, 6, 17, 18, 21, 25, 45, 49, 64, 90, 99, 104,
116, 120, 123, 124, 128, 191, 192, 219, 238, 266, 296.
```

The result is exactly 277 perfect residual matchings and 23 matching
deficiencies of one.

## One mechanism, 23 instances

For every deficient rule:

- the Hall witness lies entirely in the equal-twin sector;
- exactly one of the 5,940 possible normalized equal-twin right views is
  absent;
- the equal residual graph on its present vertices is connected, with 5,940
  left and 5,939 right vertices;
- all 990 clique-tail fibres occur, with six retained diagonal cells per
  fibre; and
- the distinct-twin sector has a left-saturating matching.

Every possible equal right view has exactly eight full diagonal preimages,
one for each hidden clique colour, in eight distinct tail fibres.  For the
missing view, all eight preimages were deleted by the two twin guesses.  The
alpha/beta hit split varies:

```text
4+4: 7 rules
3+5: 6 rules
6+2: 4 rules
5+3: 3 rules
1+7: 2 rules
2+6: 1 rule.
```

Thus the obstruction is not tied to one twin or one clique coordinate.  It is
complete local overcoverage of an equal view.

## Extended scout

The same exact implementation was run through seed 2,000:

```text
perfect full matching:                1843
deficient full matching:               157
one absent equal view / deficiency 1:  153
two absent equal views / deficiency 2:   4
no distinct-sector deficiency:            0
classification mismatch:                 0.
```

This extended run is exploratory evidence, not a universal theorem.  It
supports the exact diagnosis that the random failures are diagonal
surjectivity failures.

## Random-model explanation

In an ideal product model, each tail independently chooses an ordered pair of
distinct guesses uniformly from its eight available colours.  For a fixed
equal right view, each of its eight hidden-colour completions uses a distinct
tail fibre, and the common twin colour is selected by at least one twin with
probability `2/8=1/4`.  Hence

\[
\Pr(\text{that right view is absent})=(1/4)^8=1/65536.
\]

The expected number of absent equal views is therefore

\[
5940/65536\approx0.09064.
\]

A Poisson heuristic predicts the probability of at least one absent equal view near
`1-exp(-0.09064) ~= 0.0867`; the observed 23/300 is 0.0767.  This explains the
scale of the phenomenon but is not part of any theorem.

Other Hall failures can occur without an absent view. The Poisson expression
is not the probability of arbitrary Hall failure. The sampled equivalence is
an exact result for those 2,000 rules only.

All reported deficiencies are normalized orbit deficiencies. The full equal
graph has its connected present part plus the isolated right vertices.
