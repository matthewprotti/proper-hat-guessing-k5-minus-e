# The proper hat-guessing number of `K5-e`

> **Public research disclosure v0.1 - 2 September 2026**  
> **Status:** theorem proved in the manuscript and executable disclosure; independent review pending.

## Result

Let `K5-e` be the complete graph on five vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_{P}(K_5-e)=8}.
\]

This resolves the five-vertex instance of the `K_n-e` problem posed in *Hat guessing with proper colorings* (Adriaensen et al., arXiv:2603.04909v4).

The lower bound uses an explicit construction over \(\mathbb F_2^3\). Two nonadjacent twin players cover part of every proper coloring. The residual-coloring/local-view incidence graph has left degree three and right degree at most three, so Hall's theorem supplies consistent guesses for the three clique players. The general upper bound gives eight.

## Trusted proof core

The conceptual proof reduces to:

1. seven explicit choices of \(\delta(U)\) for the seven two-dimensional subspaces of \(\mathbb F_2^3\);
2. 42 direct evaluations showing that seven maps \(\phi_w\) are fixed-point-free permutations; and
3. a degree-count proof of Hall's condition.

The verifier reconstructs a residual saturating matching and the complete 6,720-entry strategy, then checks all 8,400 proper eight-colorings. Those computations are redundant verification layers rather than premises of the conceptual proof.

## Verify

Only Python 3 and its standard library are required:

```bash
python3 VERIFY_PACKAGE.py
```

The focused verifier checks the manifest, regenerates the exact CNF instance, reconstructs the matching and strategy from the seven-entry certificate, checks all 8,400 proper colorings, verifies the independent matching certificate, checks the frozen CNF assignment, runs a known-q=7 positive control, and rejects a corrupted delta certificate.

## Main files

- `preprint/proper_hat_guessing_K5_minus_e_v0.1.pdf` - rendered review-pending manuscript.
- `preprint/proper_hat_guessing_K5_minus_e_v0.1.md` - manuscript source.
- `THEOREM.md` - self-contained proof.
- `GENERAL_KNE_REDUCTION.md` - reusable twin-completion lemma for `K_n-e`.
- `code/verify_k5e_fano_hall.py` - dependency-free constructor/verifier.
- `certificates/K5_e_q8_fano_delta.json` - compact seven-entry certificate.
- `AI_USE_AND_PROVENANCE.md` - contribution and AI-use disclosure.
- `REVIEW_REQUEST.md` - independent-review checklist.
- `NOVELTY_SEARCH_20260902.md` - same-day targeted search record.

## Scope

This release proves only the exact value for `K5-e` and a general sufficient twin-completion lemma. It does **not** solve the full `K_n-e` family, determine `HG_P(C5)`, claim peer review, or claim exhaustive novelty clearance.

## Public chronology

The first public GitHub timestamp was made at commit:

```text
cc9f874ce1f5fa91db42c84bf3e38e8170309a8d
2026-09-02 20:13:36 UTC
```

The standalone repository should preserve that prior timestamp in its README and release notes.
