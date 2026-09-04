# Equality-sector balance and diagonal overcoverage

Assume `n>=3`. Let `G=K_n-e`.  Write `a,b` for the nonadjacent twins, let the ordered clique
have size

\[
k=n-2,
\]

and take the upper-endpoint palette

\[
q=2n-2.
\]

For every ordered injective clique colouring `T`, let the two legal twin guesses
be `alpha(T), beta(T)`, and assume they are distinct.  Form the usual residual
bipartite graph: left vertices are proper colourings missed by both twins;
right vertices are labelled clique local views; every left vertex is adjacent
to its `k` clique views.

Throughout, each right part is the full legal local-view universe, including
vertices of residual degree zero; it is not defined to equal `N(L)`.

## Sector decomposition

Split residual colourings according as the twins receive equal or distinct
colours.  The same split applies to clique local views, because the local view
contains both twin colours.  Every edge preserves the equality relation.
Hence the residual graph is the disjoint union

\[
B=B_{=}\sqcup B_{\ne}.
\]

## Equal sector

There are `(q)_k` ordered clique colourings.  For a fixed clique colouring,
there are `n` available common twin colours.  The two distinct twin guesses
remove exactly two diagonal cells, so `k=n-2` equal-twin residual colourings
remain.  Therefore

\[
|L_{=}|=k(q)_k.
\]

An equal-twin right view is specified by:

- the labelled hidden clique vertex (`k` choices);
- an ordered colouring of the other `k-1` clique vertices (`(q)_{k-1}`
  choices); and
- a common twin colour not among those visible clique colours (`n+1`
  choices).

Thus

\[
|R_{=}|=k(q)_{k-1}(n+1)=k(q)_k=|L_{=}|.
\]

Consequently, any matching saturating all residual colourings must restrict to
a perfect matching on the equal sector.  In particular,

\[
N(L_{=})=R_=.
\]

Fix an equal-twin right view.  Exactly `n` hidden clique colours complete it to
a proper colouring.  If the twins cover all `n` completions, that right view
has residual degree zero and is absent from `N(L_{=})`.  Since the two sides of
the equal sector have equal size, Hall fails immediately.

> **Diagonal overcoverage obstruction.** Within the residual-Hall framework
> with distinct twin guesses, every equal-twin clique view must leave at least
> one of its `n` hidden-colour completions residual.  Complete twin coverage of
> one equal view is fatal.

More quantitatively, if `z` equal right views are absent, the matching
deficiency is at least `z`.

## Distinct sector

For a fixed clique colouring there are `n(n-1)` ordered distinct twin-colour
pairs.  The alpha row and beta column cover

\[
(n-1)+(n-1)-1=2n-3
\]

of them, leaving

\[
n^2-3n+3
\]

residual cells.  Hence

\[
|L_{\ne}|=(q)_k(n^2-3n+3).
\]

The number of distinct-twin right views is

\[
|R_{\ne}|=k(q)_{k-1}(n+1)n=kn(q)_k.
\]

Therefore

\[
|R_{\ne}|-|L_{\ne}|=(n-3)(q)_k.
\]

The equal sector is exactly balanced. The distinct surplus is zero for n=3
and positive for n>=4.  At `n=8`, after dividing by the free `PGL(2,13)` action, these counts
are

```text
equal:     |L|=5940,  |R|=5940
distinct:  |L|=42570, |R|=47520, surplus=4950.
```

The displayed n=8 counts and deficiencies are in orbit units. See
`FREE_ACTION_QUOTIENT_AND_DEFICIENCY.md` for the two-way lifting argument.
