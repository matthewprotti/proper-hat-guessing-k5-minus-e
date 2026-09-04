# A common-completion theorem for orientation families

Status: new derivation, internally checked, independent adversarial review
pending. This is a sufficient construction mechanism with an exact capacity
bound. No novelty clearance in matching theory is claimed.

## Setting

Let n>=3, k=n-2, q=2n-2, and M=(q)_k. For each ordered injective clique
tuple T, fix an unordered pair P_T={p_T,q_T} of two distinct available colors.
Fix an orientation of this pair outside a set F of f tuple fibres; in every
fibre of F, allow either orientation independently.

All clique players must use ONE common collection of local guessing
functions, valid for every allowed orientation of the twin guesses.

## The orientation envelope

The equal residual cells are always the n-2 common colors outside P_T,
independent of orientation. Let L_= be their union.

For a fixed orientation (p,q), a distinct twin cell (x,y) is residual exactly
when x!=p and y!=q. There are n^2-3n+3 such cells per tuple.

For a mutable tuple, the union of the two distinct residual sets is the
entire n(n-1) off-diagonal board. Indeed, for (x,y) to be twin-covered in
both orientations, one needs
\[
(x=p\ \text{or}\ y=q)\ \text{and}\ (x=q\ \text{or}\ y=p).
\]
The four possibilities force either p=q or x=y. Both are excluded.

Let L_* be the resulting distinct-sector union. Its size is
\[
|L_*|=M(n^2-3n+3)+(2n-3)f.
\]

Build its incidence graph to the full labeled distinct clique-view universe
R_neq, which has |R_neq|=knM.

## Common-completion equivalence

If L_= has a perfect matching and L_* has a left-saturating matching, those
two matchings define common clique guesses. Fill unused legal views with any
legal guess. Equal and distinct view universes are disjoint, so no conflict
arises. Every coloring missed by either permitted twin orientation lies in
the relevant envelope and is covered by the common clique rules. This proves
all 2^f strategies simultaneously.

Conversely, any common clique strategy valid for the whole orientation family
must cover every coloring in these two residual unions. A labeled clique
view plus its chosen guess specifies at most one full proper coloring,
because a clique player sees all other vertices. Assign each envelope
coloring to one successful clique view. Distinct colorings cannot be assigned
the same view, so this gives the required matching.

This converse concerns the explicitly fixed twin-pair family and common
clique rules. It does not assert the local line-permutation criterion is
necessary for arbitrary winning strategies.

## Capacity bound

The distinct envelope must fit in R_neq. Therefore
\[
(2n-3)f\le(n-3)M,\qquad
\boxed{f\le\left\lfloor\frac{(n-3)M}{2n-3}\right\rfloor}.
\]

This is necessary for a COMMON clique completion over independently
reversible pair orientations. It is not a bound when the clique strategy
may change with the twin orientations, nor does counting alone prove
existence below the bound.

## Free-action orbit form

The same argument applies to a fixed free color-action quotient when clique
tuples, full colorings, and labeled views have equal orbit sizes. Here M is
the number of clique-tuple orbits and F is a set of whole tuple orbits.
A matched quotient edge lifts through the free action to an unambiguous
local guessing function. Counts above are then in orbit units.

The n=8 certificate uses the explicitly enumerated PGL(2,13) action,
M=990, |R_neq|=47,520, and
\[
|L_*|=42,570+13f.
\]
Its capacity bound is f<=380.
