# The proper hat-guessing number of `K7-e`

> **Public research disclosure v0.1 (4 September 2026)**  
> **Status:** theorem proved; independent adversarial review accepted; unrefereed and not peer-reviewed.

## Result

Let `K7-e` be the complete graph on seven vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_{P}(K_7-e)=12}.
\]

The upper bound is the general inequality

\[
\mathrm{HG}_{P}(G)\le |V(G)|+\chi(G)-1.
\]

The twelve-colour lower bound is proved in two genuinely different ways:

1. two explicit block-disjoint Steiner systems `S(5,6,12)`, giving two set-symmetric Witt-design completion rules;
2. two orbit maps from an explicitly regenerated sharply five-transitive twelve-point permutation group, one set-symmetric and one genuinely order-sensitive.

Both constructions satisfy a general coordinate-line twin-completion criterion. The residual-colouring/local-view incidence graph has left degree five and right degree at most five, so Hall's theorem supplies consistent guesses for the five clique vertices.

## Trusted finite core

The review package and independent reconstruction check:

```text
Witt blocks per design:                 132
pentads completed once per design:      792
common Witt blocks:                       0
set-coordinate lines:                   495
set local failures:                       0

generated group elements:            95,040
ordered five-tuple images:            95,040
ordered coordinate lines:             59,400
ordered local contexts:            3,801,600
ordered local failures:                    0

proper twelve-colourings:          4,656,960
maximum residual right degree:             5
```

No explicit 3.4-million-row Hall matching is needed: the degree inequality proves Hall's condition directly.

## Structural results

The disclosure also proves:

- a general twin-completion and coordinate-line criterion for `K_n-e`;
- a disjoint completion-design theorem: two block-disjoint `S(n-2,n-1,2n-2)` systems imply `HG_P(K_n-e)=2n-2`;
- an even-`n` obstruction to set-symmetric **line-permutation twin rules within this sufficient Hall framework**; and
- a prime-admissibility theorem for the necessary divisibility conditions of the completion designs.

Prime admissibility is not an existence theorem for larger primes.

## Review status

An independent adversarial review did not trust the sealed result summaries. It reconstructed both designs from the frozen block lists, verified all pentad completions and disjointness, regenerated the 95,040-element group in independent Python and C++ implementations, checked every coordinate line and local twin-colour context, and returned:

```text
ACCEPT_K7E_THEOREM
```

No mathematical repair was required. Release-hygiene cleanups are incorporated in the public disclosure.

## Scope

This release does **not** solve the full `K_n-e` family, establish design existence for every prime `n`, characterize all upper-endpoint strategies, settle `K8-e`, or claim conventional peer review or exhaustive novelty clearance.

## Citation

Until a standalone archival DOI or arXiv identifier is assigned, cite the exact public commit containing this disclosure.