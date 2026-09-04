# The proper hat-guessing number of `K_7-e`

## Theorem

\[
\boxed{\mathrm{HG}_P(K_7-e)=12.}
\]

The disclosure gives two distinct lower-bound constructions:

1. two explicit block-disjoint copies of the small Witt design
   \(S(5,6,12)\), producing set-symmetric twin rules; and
2. a direct orbit-map construction from an explicitly regenerated sharply
   five-transitive twelve-point group, producing one set-symmetric and one
   order-sensitive twin rule.

Neither construction depends on accepting the conventional identification of
the generated permutation group as \(M_{12}\).

## Upper bound

The graph `K_7-e` has seven vertices and chromatic number six. The general
bound from Adriaensen et al. gives

\[
\mathrm{HG}_P(K_7-e)\le 7+6-1=12.
\]

It remains to construct a winning strategy with twelve colours.

## Proof I: two explicit disjoint Witt designs

Let the colour set be \(\Omega=\{0,1,\ldots,11\}\). The first certificate
contains 132 six-subsets and directly completes each of the
\(\binom{12}{5}=792\) pentads exactly once, so it is an explicit
\(S(5,6,12)\), denoted \(\mathcal W_A\).

Define

\[
\pi=(0\ 1\ 2\ 4\ 5\ 3),
\]

fixing the other six points, and put
\(\mathcal W_B=\pi(\mathcal W_A)\). Direct comparison gives

\[
|\mathcal W_A|=|\mathcal W_B|=132,
\qquad
\mathcal W_A\cap\mathcal W_B=\varnothing.
\]

For each five-set \(B\), let \(f_A(B)\) and \(f_B(B)\) be the unique
completing points in the two designs. Pull these functions back to ordered
five-tuples by ignoring order. On every one of the 495 frozen four-set lines:

- both completion maps have cycle type \((2,2,2,2)\);
- they are pointwise unequal;
- their composition has no fixed point;
- the composition has type \((4,4)\) on 330 lines and
  \((2,2,2,2)\) on 165 lines; and
- all 31,680 equal/different-twin local contexts satisfy the required
  two-extension/one-extension property.

The disjoint completion-design theorem and Hall's theorem therefore give a
winning twelve-colour strategy.

## Proof II: a sharply five-transitive orbit construction

Consider the permutations of \(\Omega\)

\[
\begin{aligned}
a&=(0\ 1\ 2\ 3\ 4\ 5\ 6\ 7\ 8\ 9\ 10),\\
b&=(2\ 6\ 10\ 7)(3\ 9\ 4\ 5),\\
c&=(0\ 11)(1\ 10)(2\ 5)(3\ 7)(4\ 8)(6\ 9).
\end{aligned}
\]

Let \(G=\langle a,b,c\rangle\). Breadth-first closure gives exactly 95,040
permutations. Their images of \((0,1,2,3,4)\) are all 95,040 ordered
injective five-tuples, so sharp five-transitivity is proved as a finite fact.

For every \(y\in\{5,6,7,8,9,10,11\}\), define

\[
F_y(g(0),g(1),g(2),g(3),g(4))=g(y).
\]

The complete coordinate-line classification is:

- \(F_6\) has type \((2,2,2,2)\) on all 59,400 ordered lines;
- each of \(F_5,F_7,F_8,F_9,F_{10},F_{11}\) has type \((4,4)\) on all
  59,400 lines;
- every pair of distinct functions is pointwise unequal; and
- exactly the six pairs \(\{F_6,F_y\}\), for
  \(y\in\{5,7,8,9,10,11\}\), have fixed-point-free composition on every
  line.

Choose \(\alpha=F_6\) and \(\beta=F_5\). Then
\(\beta\circ\alpha\) has type \((4,4)\) on every line. A direct check of all

\[
59{,}400\cdot8^2=3{,}801{,}600
\]

local twin-colour contexts gives zero failures. The coordinate-line criterion
and Hall's theorem again give a winning twelve-colour strategy.

## Relationship between the proofs

The orbit of \(\{0,1,2,3,4,6\}\) under \(G\) is exactly
\(\mathcal W_A\), and

\[
F_6(T)=f_A(\operatorname{set}(T))
\]

for every ordered pentad \(T\). Thus \(F_6\) is a Witt-design completion
map. The partner \(F_5\) is genuinely order-sensitive: its 120 orderings of
each pentad realize six different outputs. The two lower-bound proofs are
therefore genuinely different.

## Hall census

For either construction, there are \((12)_5=95,040\) ordered clique
colourings. The twins each have seven legal colours. Since their guesses are
distinct, they cover \(7+7-1=13\) of the 49 twin-colour pairs and leave 36.
Hence

```text
proper twelve-colourings: 4,656,960
twin-covered:             1,235,520
residual:                  3,421,440
residual left degree:              5
residual edges:            17,107,200
maximum right degree:              5
```

Hall supplies the clique rules. No 3.4-million-row matching is required as a
proof object.

Combining either lower bound with the upper bound proves the theorem. \(\square\)
