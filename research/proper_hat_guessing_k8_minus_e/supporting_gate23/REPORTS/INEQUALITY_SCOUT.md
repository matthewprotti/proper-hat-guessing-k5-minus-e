# Inequality scout

The useful exact inequality is the trapped-view dual

\[
|\mathcal C(A)|\le |A|+\Delta.
\]

It separates the two sectors sharply:

```text
equal sector:     Delta=0
distinct sector:  Delta=4950.
```

The 23 random failures violate the equal inequality at `A=empty`.  The
crafted rule violates it at `|A|=1`, showing that degree positivity is too
weak.

## Accepted K8 rule: low-order trapped-core census

For the explicit accepted index rule, the equal-right residual degree
histogram is:

```text
degree 2:    7
degree 3:   57
degree 4:  345
degree 5: 1308
degree 6: 2377
degree 7: 1495
degree 8:  351.
```

There are no degree-zero or degree-one equal views.

Every inclusion-minimal Hall violation can be reduced to a connected union of
trapped right neighbourhoods.  An exact enumeration of all 95,096 connected
unions using at most 12 left vertices produced the following maximum trapped
view counts:

| `|A|` | maximum over connected neighborhood unions only |
|---:|---:|
| 1 | no connected union; unrestricted value 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 2 |
| 7 | 3 |
| 8 | 3 |
| 9 | 3 |
| 10 | 3 |
| 11 | 4 |
| 12 | 4 |

The unrestricted spectrum is instead kappa_m=floor(m/2) for 0<=m<=12.
The component-reduction proof and attainment witnesses are supplied in
THEOREMS/CONNECTED_CORE_REDUCTION_AND_SPECTRUM.md. Thus the accepted rule
has low-order Hall slack; no complement witness
of size at most 12 exists.  The already accepted 48,510-row matching remains
the proof for all sizes.

## Geometry behind a possible proof

Before twin deletions, the normalized equal sector is a `(6,8)`-biregular
incidence graph:

```text
full equal left vertices:   7920
right views:                5940
left degree:                   6
right degree:                  8.
```

Exact incidence checks show:

- two distinct left vertices share at most one right view;
- two distinct right views share at most one left vertex; and
- the incidence graph has no 4- or 6-cycle.

This is the appropriate finite geometry for a projection inequality.  It may
allow bounds on connected trapped cores, but it does not by itself prove
Hall.  In particular, a proposed hypothesis must control degree-one and then
larger trapped configurations.

## Current theorem target

A realistic family theorem should give checkable algebraic conditions on the
twin rule implying

\[
|\mathcal C(A)|\le |A|
\]

in the equal sector and

\[
|\mathcal C(A)|\le |A|+4950
\]

in the distinct sector.  Conditions that merely restate these inequalities
would be tautological.  The next discovery task is to connect coefficient or
cross-ratio mixing to explicit upper bounds on trapped-view cores.

The earlier minimum-degree-two research question was refuted in a separate
cube addendum. That addendum is not covered by this Gate23 review.
