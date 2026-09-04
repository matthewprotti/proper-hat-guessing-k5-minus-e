# Structural theorems for `K_n-e`

## 1. Twin-completion and coordinate-line criterion

Let

\[
G_n=K_n-e,\qquad k=n-2,\qquad q=2n-2.
\]

Write `a,b` for the nonadjacent twins and label the remaining `k` vertices as
an ordered clique. Let \(\mathcal T\) be the ordered injective `k`-tuples of
colours. Any legal maps

\[
\alpha,\beta:\mathcal T\to\Omega,
\qquad
\alpha(T),\beta(T)\notin\operatorname{set}(T),
\]

define the twin part of a strategy.

Assume that, after fixing a clique vertex, the other `k-1` clique colours, and
the two twin colours `x,y`, the legal colours for the unseen clique vertex
satisfy:

- if \(x\ne y\), at least one extension makes a twin correct;
- if \(x=y\), at least two distinct extensions make a twin correct.

Then

\[
\boxed{\mathrm{HG}_P(K_n-e)=2n-2.}
\]

Indeed, make a bipartite graph whose left vertices are the proper colourings
missed by both twins and whose right vertices are **labelled** clique views,
meaning pairs `(clique vertex, visible colour tuple)`. Every left degree is
`k`. The local hypothesis reduces every right degree to at most `k`, so Hall's
condition follows by edge counting. A matching assigns consistent clique
guesses. The general upper bound gives equality.

Fix one coordinate position and freeze the other `k-1` clique colours. Put
\(D=\Omega\setminus S\), so \(|D|=n+1\), and let `f,g` be the restrictions
of the twin rules to that coordinate line. It is sufficient that, on every
line:

1. `f` and `g` are permutations of `D`;
2. both are fixed-point-free;
3. \(f(r)\ne g(r)\) for all \(r\in D\); and
4. \(g\circ f\) has no fixed point.

For distinct twin colours, a complete miss would force a fixed point of
\(g\circ f\). For equal twin colours, \(f^{-1}(x)\) and \(g^{-1}(x)\) are
two distinct legal covered extensions. Conversely, on one fixed line, the
one/two-extension property forces exactly this compatible-derangement
structure. This is a characterization only within this residual-Hall
framework, not of all possible winning strategies.

## 2. Disjoint completion-design theorem

Suppose two block-disjoint Steiner systems

\[
\mathcal D_0,\mathcal D_1\cong S(n-2,n-1,2n-2)
\]

exist on the same colour set. For every `(n-2)`-set \(B\), let \(f_i(B)\)
be the unique point completing `B` to a block of \(\mathcal D_i\), and pull
these set maps back to ordered clique tuples.

On each coordinate line, every completion map is a fixed-point-free
involution. Block-disjointness makes the maps pointwise unequal. For
involutions,

\[
(g\circ f)(r)=r\iff f(r)=g(r),
\]

so the composition is fixed-point-free. The coordinate-line criterion gives

\[
\boxed{\mathrm{HG}_P(K_n-e)=2n-2.}
\]

This is sufficient, not necessary.

## 3. Even-`n` obstruction to set-symmetric line-permutation twins

Let `n >= 4` be even. There is no legal set-symmetric twin rule whose
restriction to every coordinate line is a permutation inside the sufficient
framework above.

For a fixed output colour `y`, the preimages would form a Steiner system

\[
S(n-3,n-2,2n-3).
\]

The number of blocks through a fixed `(n-4)`-set would have to be

\[
\frac{n+1}{2},
\]

which is not an integer for even `n`.

This does not prove that every upper-endpoint winning strategy for even `n`
must use clique order; another strategy could use weaker twins and stronger
clique rules.

## 4. Prime admissibility of the Steiner-completion parameters

For `n >= 3`, the standard divisibility conditions for

\[
S(n-2,n-1,2n-2)
\]

hold if and only if `n` is prime.

Writing \(j=t-s\), the required multiplicities are

\[
\lambda_s
=\frac{\binom{n+j}{j}}{j+1}
=\frac1n\binom{n+j}{j+1}.
\]

For prime `n`, Lucas's theorem gives integrality for
\(1\le j\le n-2\). If `n` is composite and `p` is its least prime factor,
take \(j=p-1\); then

\[
\binom{n+p-1}{p-1}\equiv1\pmod p,
\]

so the corresponding multiplicity is not integral.

If such a design exists, its block count is

\[
\frac1n\binom{2n-2}{n-1}=C_{n-1}.
\]

This is an admissibility theorem only. It does not establish design existence
for larger primes.