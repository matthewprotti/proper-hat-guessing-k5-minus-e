# A twin-completion reduction for `K_n-e`

The `K5-e` proof isolates a general sufficient condition for attaining the
upper endpoint in the source paper's dichotomy.

## Setup

Let \(G=K_n-e\), with nonadjacent twins \(a,b\) and an \((n-2)\)-vertex
clique \(C\). Put

\[
q=2n-2.
\]

For every ordered injective clique colouring \(T\), choose legal twin guesses

\[
\alpha(T),\beta(T)\in[q]\setminus T.
\]

Fix a clique vertex \(v\), a local view at \(v\), and let \(R\) be the set of
colours that could legally be placed at \(v\) while preserving that view. For
\(r\in R\), let \(T_r\) be the resulting ordered clique colouring.

The candidate set has size

\[
|R|=
\begin{cases}
n-1,&a\ne b,\\
n,&a=b.
\end{cases}
\]

## Twin-completion lemma

Suppose the twin rules satisfy the following condition at every clique local
view:

- if the observed twin colours are distinct, at least one \(r\in R\) obeys
  \(\alpha(T_r)=a\) or \(\beta(T_r)=b\);
- if the observed twin colours are equal, at least two distinct \(r\in R\)
  obey \(\alpha(T_r)=a\) or \(\beta(T_r)=b\).

Then

\[
\mathrm{HG}_{P}(K_n-e)=2n-2.
\]

## Proof

Let \(L\) be the proper colourings not covered by either twin. Let \(R'\) be
the attainable clique local views, and join each residual colouring to its
\(n-2\) induced clique views.

Every left vertex has degree \(n-2\). At a right vertex, the completion
condition removes at least one of the \(n-1\) candidate extensions when the
twins differ, and at least two of the \(n\) extensions when they agree.
Therefore every right degree is at most \(n-2\).

For every \(S\subseteq L\),

\[
(n-2)|S|=e(S,N(S))\le(n-2)|N(S)|,
\]

so Hall's condition holds. A matching saturating \(L\) assigns one consistent
clique guess to every residual colouring. Together with the twin rules this
is a winning \((2n-2)\)-colour strategy.

The general upper bound gives

\[
\mathrm{HG}_{P}(K_n-e)\le n+\chi(K_n-e)-1
=n+(n-1)-1=2n-2,
\]

so equality follows. \(\square\)

## What the `n=5` construction supplies

For \(n=5\), the \(\mathbb F_2^3\) twin rules in `THEOREM_K5E.md` verify the
completion condition through the fixed-point-free permutations \(\phi_w\).
This turns the general `K_n-e` problem into a concrete design problem:
construct two legal twin rules satisfying the one-extension/two-extension
condition above.

No claim is made here that the \(\mathbb F_2^3\) construction extends to all
\(n\). The lemma is the reusable part; finding an appropriate colour geometry
or combinatorial design for other values of \(n\) is the next mathematical
frontier.
