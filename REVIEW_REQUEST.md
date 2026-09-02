# Independent review request

## Claim

\[
\mathrm{HG}_{P}(K_5-e)=8.
\]

## Proof-only checklist

Please independently check:

1. applicability of `HG_P(G) <= |V(G)| + chi(G) - 1`;
2. legality of both twin guesses;
3. all 42 evaluations in the seven cycle decompositions of `phi_w`;
4. the `A != B` right-degree argument;
5. the `A = B` right-degree argument;
6. the degree-count proof of Hall's condition; and
7. conversion of a saturating matching into consistent clique-player guesses.

## From-scratch computational checklist

Without importing the generated matching or strategy, independently confirm:

```text
proper eight-colorings of K5-e: 8,400
twin-covered colorings:          3,024
residual colorings:              5,376
residual left degree:                 3
maximum residual right degree:        3
winning strategy failures:            0
```

## Requested disposition

Return one of:

```text
ACCEPT_THEOREM
ACCEPT_WITH_EXPLICIT_REPAIRS
REJECT_THEOREM
INDETERMINATE_INSUFFICIENT_EVIDENCE
```

For each defect, identify the first invalid inference, a concrete counterexample or calculation, the minimal repair, and whether the theorem survives.
