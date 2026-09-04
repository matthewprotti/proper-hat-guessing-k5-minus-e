# The proper hat-guessing number of `K_8-e`

## Theorem

Let `K_8-e` be the complete graph on eight vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_P(K_8-e)=14.}
\]

The lower bound is computer-assisted. Its finite certificate is an explicit
`PGL(2,13)`-equivariant strategy encoded by 990 twin-view decisions and 53,460
clique-view decisions, together with a 48,510-edge residual-orbit matching.
The strategy is independently checked on all 138,378,240 proper fourteen-colour
assignments.

## 1. Upper bound

The source paper proves, for every graph `G`,

\[
\mathrm{HG}_P(G)\le |V(G)|+\chi(G)-1.
\]

Since `K_8-e` has eight vertices and chromatic number seven,

\[
\mathrm{HG}_P(K_8-e)\le 8+7-1=14.
\]

It remains to construct a winning strategy with fourteen colours.

## 2. Colour normalization

Use the colour set

\[
\Omega=\mathbb P^1(\mathbb F_{13})
       =\mathbb F_{13}\cup\{\infty\}.
\]

In the certificate, field elements are encoded by `0,...,12` and `infinity` by
`13`. Fractional linear transformations give the sharply three-transitive
action of

\[
G=\mathrm{PGL}(2,13)
\]

on `Omega`. Thus, for any ordered triple of distinct colours `(r,s,t)`, there
is a unique transformation `nu_{r,s,t}` sending it to

\[
(\infty,0,1).
\]

No classification theorem is needed: the verifier constructs the normalizer
by the cross-ratio formula and checks all

\[
(14)_3=2,184
\]

ordered triples and 2,184 distinct normalizing permutations.

Label the two nonadjacent vertices `u,v`, and label the six clique vertices
`c_0,...,c_5`.

## 3. Compact twin rules

Suppose the twins see the ordered clique colouring

\[
T=(t_0,t_1,t_2,t_3,t_4,t_5).
\]

Let `nu=nu_{t_0,t_1,t_2}` and write

\[
(a,b,c)=(\nu(t_3),\nu(t_4),\nu(t_5)).
\]

Then `a,b,c` are distinct members of `{2,...,12}`. Let

\[
D(a,b,c)=\Omega\setminus\{\infty,0,1,a,b,c\}
        =\{d_0<d_1<\cdots<d_7\},
\]

where the order is the integer encoding `0<1<...<13`.

Define

\[
i\equiv a+b+c\pmod 8,
\]

and first put

\[
j_0\equiv a+2b+3c+1\pmod 8.
\]

If `j_0` is different from `i`, set `j=j_0`; if `j_0=i`, set

\[
j\equiv j_0+1\pmod 8.
\]

The twin guesses are

\[
\alpha(T)=\nu^{-1}(d_i),
\qquad
\beta(T)=\nu^{-1}(d_j).
\]

Both guesses depend only on the common clique view of the twins, are legal,
and are distinct. The table
`CERTIFICATES/K8_e_q14_twin_rules.tsv` is the complete 990-row expansion of
this formula on normalized clique tuples.

## 4. Clique-view orbits

Fix a clique vertex `c_j`. It sees the other five clique colours and both twin
colours. Order the other clique vertices by their fixed labels, and let

\[
s_0,s_1,s_2,s_3,s_4
\]

be their colours in that order. Let `mu=nu_{s_0,s_1,s_2}`. The normalized
local-view key is

\[
\bigl(j,\mu(s_3),\mu(s_4),\mu(x),\mu(y)\bigr),
\]

where `x,y` are the twin colours. There are exactly 53,460 attainable such
keys. The certificate
`CERTIFICATES/K8_e_q14_clique_rules.tsv` assigns one legal normalized guess to
each key; the actual guess is its inverse image under `mu`.

This defines a genuine local strategy: every twin rule uses only the six
clique hats, and every clique rule uses only the other five clique hats and the
two twin hats.

## 5. Residual-orbit matching

Normalize every proper colouring by sending the first three clique colours to
`(infinity,0,1)`. Since the action is sharply three-transitive, each full
colouring has one normalized representative. The normalized universe has

\[
11\cdot10\cdot9\cdot 8^2=63,360
\]

proper-colouring orbits.

There are 990 normalized ordered clique tuples. For each tuple, the twins each
have eight available colours. Their two distinct fixed guesses cover one row
and one column of the `8 by 8` twin-colour array, hence

\[
8+8-1=15
\]

colourings, leaving

\[
64-15=49
\]

residual colourings. Therefore

\[
|L|=990\cdot49=48,510.
\]

Construct a bipartite graph whose left vertices are these residual normalized
colourings and whose right vertices are the 53,460 normalized labelled clique
views. A residual colouring is adjacent to the six clique views it induces.
The frozen file
`CERTIFICATES/K8_e_q14_residual_orbit_matching.tsv` contains a matching of
size 48,510 and therefore saturates every residual left vertex.

For each matched right view, assign its clique player the hidden colour in the
matched colouring. Because the matching uses each right view at most once,
these assignments are consistent. Fill unmatched attainable right views with
any legal guess. This is precisely the clique table supplied in the package.
Every residual colouring is covered by its matched clique player; every other
colouring was already covered by a twin.

## 6. Lifting from normalized orbits

The strategy was defined equivariantly by unique local normalization. Applying
a colour transformation in `PGL(2,13)` transports every view, guess, and
correctness relation. Because the first three clique colours are distinct, no
nonidentity group element fixes a proper colouring; every orbit has size

\[
|\mathrm{PGL}(2,13)|=14\cdot13\cdot12=2,184.
\]

Thus the 63,360 normalized representatives cover

\[
63,360\cdot2,184
=138,378,240
=(14)_6\,8^2
\]

proper colourings.

The independent C++ verifier does not rely only on this orbit-count argument:
it explicitly enumerates all 138,378,240 proper colourings, evaluates the
local rules, and finds no uncovered colouring.

## 7. Exact verification results

The data-only orbit verifier reconstructs the finite objects and reports:

```text
PGL normalizers:                    2,184
normalized clique orbits:             990
normalized proper-colouring orbits: 63,360
twin-covered orbits:               14,850
residual orbits:                    48,510
attainable clique-view orbits:      53,460
matching size:                      48,510
coverage failures:                       0
```

The independent full-colouring verifier reports:

```text
proper colourings checked:       138,378,240
exactly 1 correct guess:         126,099,792
exactly 2 correct guesses:        11,594,856
exactly 3 correct guesses:           672,672
exactly 4 correct guesses:            10,920
uncovered colourings:                       0
```

Hence a winning fourteen-colour strategy exists, so

\[
\mathrm{HG}_P(K_8-e)\ge 14.
\]

Together with the upper bound,

\[
\boxed{\mathrm{HG}_P(K_8-e)=14}.\qquad\square
\]

## Scope

This theorem does not prove the general formula for every `n`, provide a
closed symbolic formula for all six clique rules, or show that the earlier
coordinate-line twin-completion criterion is necessary. In fact, the present
strategy uses a global matching on residual view orbits; its residual right
degrees reach eight, above the clique size six. The full `K_n-e` problem
therefore remains open beyond the explicitly settled cases.
