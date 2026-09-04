# Twin completion and the coordinate-line criterion

Let `G_n=K_n-e`. Denote the two nonadjacent vertices by `a,b`, and order the remaining clique vertices as

\[
c_1,\ldots,c_k,\qquad k=n-2.
\]

Use

\[
q=2n-2
\]

colours. Let `T` be the set of injective ordered `k`-tuples of colours. A legal pair of twin rules is

\[
\alpha,\beta:\mathcal T\to[q]
\]

with `alpha(T), beta(T)` outside the colour set of `T`.

Fix a clique coordinate `i` and an injective ordered `(k-1)`-tuple `S` on the other coordinates. Let `set(S)` denote its underlying colour set and put

\[
D=[q]\setminus\operatorname{set}(S),\qquad |D|=n+1.
\]

For `r in D`, let `T_r` be the full ordered clique tuple obtained by inserting `r` at coordinate `i`, and define

\[
f(r)=\alpha(T_r),\qquad g(r)=\beta(T_r).
\]

Legality gives `f(r),g(r) in D\setminus{r}`.

## Twin-completion lemma

Suppose that on every coordinate line:

- when the observed twin colours `x != y`, at least one candidate `r in D\setminus{x,y}` satisfies `f(r)=x` or `g(r)=y`;
- when `x=y`, at least two distinct candidates `r in D\setminus{x}` satisfy `f(r)=x` or `g(r)=x`.

Then

\[
\mathrm{HG}_{P}(K_n-e)=2n-2.
\]

### Proof

Call a proper colouring *residual* if neither twin guesses correctly. Form a bipartite graph whose left vertices are residual colourings and whose right vertices are **labelled pairs**

\[
(\text{clique vertex},\text{attainable local view}).
\]

Join each residual colouring to the `k=n-2` labelled clique views it induces. Every left degree is exactly `k`.

Fix a right vertex. The view determines `S` and the twin colours `x,y`.

- If `x != y`, there are `n-1` proper candidate colours for the unseen clique vertex, and at least one is nonresidual.
- If `x=y`, there are `n` proper candidates, and at least two are nonresidual.

Thus every right degree is at most `n-2=k`. For every set `X` of left vertices,

\[
k|X|=e(X,N(X))\le k|N(X)|,
\]

so Hall's theorem supplies a matching saturating all residual colourings. Assign each matched clique view the colour occurring at that clique vertex in its matched colouring; fill unmatched views arbitrarily with a legal colour. The twins cover every nonresidual colouring, and the matching covers every residual colouring.

The general upper bound gives

\[
\mathrm{HG}_{P}(K_n-e)\le n+(n-1)-1=2n-2,
\]

so equality follows. `square`

## Coordinate-line permutation criterion

The twin-completion hypotheses hold if, on every line `D`,

1. `f` and `g` are permutations of `D`;
2. `f(r) != g(r)` for every `r`;
3. `g o f` has no fixed point.

Both maps are automatically fixed-point-free because legality gives `f(r),g(r) != r`.

### Proof

If `x != y` and no proper candidate is twin-covered, then the unique preimages `f^{-1}(x)` and `g^{-1}(y)` both lie in `{x,y}`. Fixed-point freedom forces

\[
f^{-1}(x)=y,\qquad g^{-1}(y)=x,
\]

so `(g o f)(y)=y`, contradiction.

If `x=y`, the two legal candidates `f^{-1}(x)` and `g^{-1}(x)` are distinct by pointwise inequality, so at least two candidates are covered. `square`

## Converse on one line

For legal maps `f,g:D->D`, the one/two-extension conditions force the same three permutation conditions on that line.

If `f` omitted a colour `x`, then equal-twin at `x` would force at least two preimages of `x` under `g`, while distinct-twin `(x,y)` would force at least one preimage of every `y != x`; this requires at least `|D|+1` inputs. Hence `f` is surjective, and symmetrically so is `g`. The equal-twin condition forces their unique preimages of every colour to differ, which is equivalent to pointwise inequality. A fixed point of `g o f` creates a distinct-twin context in which the only two covering preimages are excluded candidates, and conversely.

This converse characterizes the local twin-completion condition on a line. It does **not** characterize every globally winning strategy for `K_n-e`: clique players could, in principle, compensate for twin rules outside this Hall framework.