---
title: "The Proper Hat-Guessing Number of $K_5-e$"
author: "Matthew Protti - Independent Researcher"
date: "2 September 2026 - Public research disclosure v0.1; independent review pending"
geometry: margin=1in
fontsize: 11pt
header-includes:
  - \usepackage{booktabs}
  - \usepackage{microtype}
---

**Abstract.** We prove that the proper hat-guessing number of the complete graph on five vertices with one edge removed is eight. The upper bound follows from the general inequality $\mathrm{HG}_P(G)\le |V(G)|+\chi(G)-1$. For the lower bound, we identify the eight colours with $\mathbb F_2^3$ and give two explicit rules for the nonadjacent twin vertices. The residual proper colourings and the attainable local views of the three clique vertices form a bipartite graph with left degree three and right degree at most three. Hall's theorem therefore completes the strategy. The only finite residue in the conceptual proof is a seven-row table comprising 42 direct evaluations. Dependency-free code reconstructs the strategy and verifies all 8,400 proper colourings.

Let `K5-e` be the complete graph on five vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_{P}(K_5-e)=8}.
\]

We label the two nonadjacent vertices by \(0,1\) and the three clique vertices
by \(2,3,4\).

## Upper bound

The graph has five vertices and chromatic number four. The general inequality

\[
\mathrm{HG}_{P}(G)\le |V(G)|+\chi(G)-1
\]

therefore gives

\[
\mathrm{HG}_{P}(K_5-e)\le 5+4-1=8.
\]

It remains to construct a winning strategy with eight colours.

## Colour geometry

Identify the colour set with

\[
V=\mathbb F_2^3,
\]

written additively; in the certificate and verifier, vectors are encoded by
integers \(0,\ldots,7\), and vector addition is bitwise XOR.

For each nonzero normal vector \(n\in V\), let

\[
U_n=\{x\in V:n\cdot x=0\},
\]

where \(\cdot\) is the standard dot product over \(\mathbb F_2\). Thus the
\(U_n\) are the seven two-dimensional linear subspaces of \(V\).

Choose \(\delta(U_n)\notin U_n\) by the following table.

| normal `n` | binary `n` | `delta(U_n)` | binary `delta` |
|---:|:---:|---:|:---:|
| 1 | 001 | 5 | 101 |
| 2 | 010 | 7 | 111 |
| 3 | 011 | 6 | 110 |
| 4 | 100 | 4 | 100 |
| 5 | 101 | 3 | 011 |
| 6 | 110 | 2 | 010 |
| 7 | 111 | 1 | 001 |

The condition \(n\cdot\delta(U_n)=1\) makes
\(\delta(U_n)\notin U_n\) immediate.

## The seven-row finite lemma

For every nonzero \(w\in V\), put

\[
D_w=V\setminus\{0,w\}
\]

and define

\[
\phi_w(r)=w+r+\delta(\langle w,r\rangle),\qquad r\in D_w.
\]

Here \(\langle w,r\rangle\) is the two-dimensional linear span of the two
independent vectors \(w,r\).

**Finite lemma.** Each \(\phi_w\) is a fixed-point-free permutation of
\(D_w\).

For the displayed delta table, the complete cycle decomposition is:

| `w` | cycles of `phi_w` on `D_w` |
|---:|:---|
| 1 | `(2 7 4)(3 6 5)` |
| 2 | `(1 7 6)(3 5 4)` |
| 3 | `(1 6 4)(2 5 7)` |
| 4 | `(1 2 3)(5 6 7)` |
| 5 | `(1 3 7)(2 4 6)` |
| 6 | `(1 5 2)(3 4 7)` |
| 7 | `(1 4 5)(2 6 3)` |

This table is the only finite search residue in the proof. It can be checked
by 42 direct evaluations, and `code/verify_k5e_fano_hall.py` checks it without
external dependencies.

## The two twin-player rules

Let

\[
T=(t_2,t_3,t_4)
\]

be the ordered triple of pairwise distinct colours on the clique. Define

\[
\sigma(T)=t_2+t_3+t_4,
\qquad
U(T)=\langle t_2+t_3,\ t_2+t_4\rangle.
\]

The four points \(t_2,t_3,t_4,\sigma(T)\) form the affine plane with direction
subspace \(U(T)\). In particular \(\sigma(T)\notin\{t_2,t_3,t_4\}\).

The two nonadjacent players use the guesses

\[
\alpha(T)=\sigma(T),
\qquad
\beta(T)=\sigma(T)+\delta(U(T)).
\]

Because \(\delta(U(T))\notin U(T)\), the second guess lies outside that affine
plane, so both twin guesses are legal.

For each fixed clique triple, the twins may independently receive any of the
five remaining colours. The rule \(\alpha\) covers one full row of this
\(5\times5\) array and \(\beta\) covers one full column. Thus the twins cover
\(5+5-1=9\) pairs and leave \(16\) residual pairs. Across all
\((8)_3=336\) ordered clique triples, there are

\[
336\cdot16=5,376
\]

residual proper colourings.

## The residual incidence graph

Construct a bipartite graph \(B=(L,R;E)\):

- \(L\) is the set of 5,376 residual proper colourings;
- \(R\) is the set of attainable local views at the three clique vertices;
- a residual colouring is adjacent to the three clique views it induces.

Every left vertex has degree exactly three. We prove that every right vertex
has degree at most three.

Fix a clique vertex and one of its local views. Let \(x,y\) be the colours on
the other two clique vertices, and let \(a,b\) be the two twin colours.
Translate all colours by \(x\), and write

\[
w=y+x,\qquad A=a+x,\qquad B=b+x.
\]

Then \(w\ne0\) and \(A,B\in D_w\). If the unseen clique vertex has translated
colour \(R\), its proper candidate set is

\[
D_w\setminus\{A,B\}\quad\text{when }A\ne B
\]

and

\[
D_w\setminus\{A\}\quad\text{when }A=B.
\]

For a candidate extension:

- twin 0 is correct precisely when
  \[
  R=A+w;
  \]
- twin 1 is correct precisely when
  \[
  \phi_w(R)=B.
  \]

Let \(J_w(A)=A+w\).

### Case 1: `A != B`

There are four proper candidate colours. Suppose none of them is covered by a
twin. Then both distinguished candidates

\[
J_w(A),\qquad \phi_w^{-1}(B)
\]

must lie in \(\{A,B\}\). Since \(J_w(A)\ne A\), we get
\(J_w(A)=B\). Since \(\phi_w\) is fixed-point-free,
\(\phi_w^{-1}(B)\ne B\), so \(\phi_w^{-1}(B)=A\). Hence

\[
\phi_w(A)=B=A+w.
\]

But by definition

\[
\phi_w(A)=A+w+\delta(\langle w,A\rangle)\ne A+w,
\]

because delta is nonzero. This is a contradiction. Therefore at least one of
the four candidate extensions is twin-covered, leaving at most three residual
extensions.

### Case 2: `A = B`

There are five proper candidate colours. The candidates

\[
J_w(A),\qquad \phi_w^{-1}(A)
\]

are both allowed because \(J_w\) and \(\phi_w\) have no fixed points. They are
also distinct: equality would imply

\[
\phi_w(A+w)=A,
\]

whereas

\[
\phi_w(A+w)
=A+\delta(\langle w,A\rangle)
\ne A.
\]

Thus at least two candidate extensions are twin-covered, again leaving at most
three residual extensions.

We have proved that every right vertex of \(B\) has degree at most three.

## Hall's theorem and the clique rules

For every \(S\subseteq L\), exactly \(3|S|\) edges leave \(S\). Since every
right vertex has degree at most three,

\[
3|S|\le3|N(S)|,
\]

and therefore \(|S|\le|N(S)|\). Hall's theorem gives a matching saturating
all of \(L\).

For each matched residual colouring, assign the matched clique vertex to guess
its own colour on that matched local view. No local view is used twice, so the
assignments are consistent. Fill unmatched attainable clique views with any
legal guess.

Every residual colouring is now covered by its matched clique player, while
every nonresidual colouring was already covered by a twin. This is a winning
strategy with eight colours, proving

\[
\mathrm{HG}_{P}(K_5-e)\ge8.
\]

Together with the upper bound, this yields

\[
\boxed{\mathrm{HG}_{P}(K_5-e)=8}.\qquad\square
\]

## Verification layers

The package contains four redundant layers:

1. the compact seven-entry delta certificate;
2. the degree/Hall verifier, which reconstructs a matching and strategy;
3. an independent direct checker over all 8,400 proper colourings;
4. an independently generated one-hot CNF check over 28,560 variables and
   62,161 clauses.

The frozen complete strategy has 6,720 local-view decisions. Its exhaustive
correct-guess histogram is:

| correct guesses | proper colourings |
|---:|---:|
| 1 | 7,479 |
| 2 | 840 |
| 3 | 75 |
| 4 | 6 |


## AI-use disclosure

OpenAI GPT-5.6 Pro was used substantively in literature search, construction search, proof development, code generation, verification, adversarial critique, and manuscript preparation. Matthew Protti selected and framed the problem, directed and evaluated the work, approved the final scope, and accepts responsibility.
