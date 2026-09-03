# Even-n obstruction for set-symmetric line-permutation twin rules

## Theorem

Let `n` be even. There is no legal twin rule for `K_n-e` that simultaneously:

1. depends only on the unordered set of the `n-2` clique colours; and
2. restricts to a permutation on every coordinate line.

Consequently, no construction for even `n` that runs through the twin-completion line-permutation criterion can use such a set-symmetric twin rule.

This is **not** an obstruction to the value `HG_P(K_n-e)=2n-2`, and it is not a statement about every conceivable winning strategy.

## Proof

Suppose a set-symmetric legal rule `A` exists. For each output colour `y`, define

\[
\mathcal B_y=
\left\{
B\in\binom{[2n-2]\setminus\{y\}}{n-2}: A(B)=y
\right\}.
\]

Fix an `(n-3)`-subset

\[
S\subseteq[2n-2]\setminus\{y\}.
\]

On the coordinate line obtained by varying the final clique colour, the permutation property gives exactly one input whose output is `y`. Legality rules out using `y` itself as the variable input. Hence exactly one block in `B_y` contains `S`.

Thus `B_y` is a Steiner system

\[
S(n-3,n-2,2n-3).
\]

Count its blocks through a fixed `(n-4)`-subset. The replication number is

\[
\frac{\binom{(2n-3)-(n-4)}{(n-3)-(n-4)}}
     {\binom{(n-2)-(n-4)}{(n-3)-(n-4)}}
=
\frac{n+1}{2},
\]

which is not an integer when `n` is even. Contradiction. `square`

## Interpretation

The obstruction explains why an unordered four-set ansatz for `K_6-e` is structurally impossible. It does not imply that the upper endpoint is impossible: the construction proving `HG_P(K_6-e)=10` is order-sensitive.