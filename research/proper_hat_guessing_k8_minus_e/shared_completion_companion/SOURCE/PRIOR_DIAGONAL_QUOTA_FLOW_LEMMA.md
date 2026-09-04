# Diagonal quota-flow lemma

**Status:** a new derivation in this assessment, not yet independently
reviewed. The argument is an application of ordinary integral max flow; no
literature-novelty claim is made.

## Statement

For every n>=3, with k=n-2 clique vertices and q=2n-2 colours, one can choose
two distinct legal twin guesses on every ordered clique tuple so that the
resulting equal-twin residual graph has a perfect matching.

Consequently there is a strategy that wins on every proper colouring in
which the two twins have equal colours. This does NOT assert that the same
strategy wins when their colours differ, and does not solve the general
K_n-e problem.

## Proof

Let T be the set of ordered injective clique tuples; write M=|T|=(q)_k.
Before choosing any twin guesses, let X be all proper equal-twin colourings.
There are n possible common colours per clique tuple, so |X|=nM. Partition X
into fibres X_T of size n.

Let R be all labelled equal-twin local views of clique vertices. Every
colouring x in X has exactly k neighbouring views. Every r in R has exactly
n possible hidden-colour completions. Hence

\[
 |R|=kM,\qquad d_X=k,\qquad d_R=n.
\]

Use the capacitated network

\[
 s\longrightarrow R\longrightarrow X\longrightarrow \mathcal T
 \longrightarrow t,
\]

with capacities respectively 1, 1, 1, k. The R--X arcs are exactly the
incidences, and a colouring x has just one X--T arc, to its clique-tuple fibre.

There is a fractional flow of value kM: send 1 on each s--r arc, 1/n on each
r--x incidence, k/n on each x--T arc, and k on every T--t arc. Conservation
holds because each r has n completions, each x has k views, and each fibre
has n colourings. All capacities are respected, since k<n.

All capacities are integers, so the integral max-flow theorem gives an
integral flow of the same value kM. Every right view sends its unit to one
distinct colouring, since each x--T arc has capacity one. The sum of all
T--t capacities is kM, so all are saturated: exactly k colourings are selected
in each size-n fibre.

Take the other two common colours of the fibre as the distinct twin guesses.
Those two diagonal cells are covered by the twins. The k selected cells are
residual, and the flow matches them bijectively to R. Assigning the matched
hidden colour at each clique local view completes the strategy on the
entire equal-twin sector. QED.

## Equivariant use

The same network can be built on orbits when the colour action is free on
clique tuples, full equal colourings and their local views, and each
right-orbit has n distinct left-orbit completions. These conditions hold for
the current PGL normalization and were checked in the n=8 pilot. A general
quotient application should explicitly prove them rather than assume that
transitivity alone preserves counts.

The unquotiented lemma does not require a prime-power palette or a group.
The explicit full network grows rapidly with n; polynomial solvability in
network size is not a claim of polynomial complexity in n.

## n=8 corroboration

The normalized network has 14,852 vertices and 62,370 forward arcs. An
integral flow of 5,940 selects exactly six of the eight diagonal cells in
every one of 990 fibres. The frozen chosen twin rule and perfect equal
matching are included, with a separate standard-library incidence checker.

This pilot has 73 equal-right views of degree one, yet a perfect equal
matching. Thus low minimum degree is not necessarily an obstruction, just as
the cube shows that minimum degree two is not sufficient.

No off-diagonal test or claim is made in this corroboration.

## Research consequence

The two omitted colours can be assigned to alpha and beta in either order
without changing the equal sector. Thus, after a diagonal-safe quota flow,
there remain 2^M orientations of the twin pair, plus other feasible flows,
that can be searched to make the distinct-twin sector satisfy Hall.

The natural open problem becomes compatibility of an equal-sector-safe flow
with a distinct-sector completion, rather than existence of a good equal
sector by itself.
