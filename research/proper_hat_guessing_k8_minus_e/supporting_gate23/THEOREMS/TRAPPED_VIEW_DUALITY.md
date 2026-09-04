# The trapped-view dual of Hall

Let `B=(L,R;E)` be either residual sector.  Put

\[
\Delta=|R|-|L|.
\]

For `A subseteq L`, define the trapped-view set

\[
\mathcal C(A)=\{r\in R:N(r)\subseteq A\}.
\]

Take `S=L\setminus A`.  A right vertex is outside `N(S)` precisely when all of
its neighbours lie in `A`, so

\[
R\setminus N(S)=\mathcal C(A).
\]

Therefore

\[
|N(S)|-|S|
=\Delta+|A|-|\mathcal C(A)|.
\]

It follows that Hall is equivalent to the family of inequalities

\[
\boxed{|\mathcal C(A)|\le |A|+\Delta\quad\text{for every }A\subseteq L.}
\]

For the balanced equal sector, this becomes

\[
|\mathcal C(A)|\le |A|.
\]

For the normalized `K8-e` distinct sector, it becomes

\[
|\mathcal C(A)|\le |A|+4950.
\]

This is the useful inequality-facing formulation.  It says that a mixing
hypothesis must control *concentration of whole right fibres inside a small
left set*, not merely legality or average degree.

## Mixing hierarchy

Define

\[
\kappa_m=\max_{|A|=m}|\mathcal C(A)|.
\]

Then equal-sector Hall is exactly `kappa_m <= m` for every `m`.

- the 23 original bad rules fail already at `m=0`: one equal right view is
  isolated;
- the explicit no-isolated counterexample in this package fails at `m=1`:
  two right views have the same unique retained neighbour;
- the accepted explicit `K8-e` rule has minimum equal-right degree two and an
  exact connected-core enumeration finds no obstruction through `m=12`.

The full sequence `kappa_m` is still a restatement of Hall, not yet a closed
form theorem.  Its value is that low-order failures have concrete geometric
meaning and can be attacked separately.

## Exact deficiency formula

Writing `nu(B)` for the maximum matching size, Hall's deficiency formula and
the complement identity give
\[
|L|-\nu(B)=\max_{A\subseteq L}
\bigl(|\mathcal C(A)|-|A|-\Delta\bigr).
\]
The maximum is nonnegative, since A=L gives zero. This is an exact
reformulation, not an independent expansion or mixing hypothesis.

The unrestricted low-order spectrum of the accepted rule, as corrected and
replayed, is kappa_m=floor(m/2) for 0<=m<=12. The connected-union maxima are
different quantities. See CONNECTED_CORE_REDUCTION_AND_SPECTRUM.md.
