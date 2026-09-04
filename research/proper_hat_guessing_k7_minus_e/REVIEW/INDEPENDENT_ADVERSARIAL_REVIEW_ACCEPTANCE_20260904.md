SHA-256 of the ZIP matches the advertised digest. I treated this as a theorem candidate, not as a program that printed PASS.

**Disposition:** ACCEPT_K7E_THEOREM

The boxed claim `\mathrm{HG}_P(K_7-e)=12` is proved by the source upper bound plus either of the two explicit constructions, through a Hall criterion that I checked both on paper and on the frozen objects.

## Integrity

| Check | Result |
|---|---|
| SHA-256 | `1490ab4349e1b909c3c3e741032d4354a29434fef27be4ff169f4f66b042d149` |
| Size | 640,879 bytes |
| Zip paths | single rooted tree, no traversal or absolute paths |
| Manifest | 30 files, hashes match |
| Package replay | `VERIFY_PACKAGE.py` PASS; Python and C++20 byte-identical regeneration |
| Negative controls | shared block, illegal output, and pointwise collision rejected |

I did not accept the sealed `RESULTS/*` files as evidence. I rebuilt the completions from the 132-block lists, checked the Steiner property directly, reconstructed design B from the displayed 6-cycle, and re-ran the line/Hall census on both the set designs and the ordered orbit tables.

## Accepted mathematical core

The source upper bound gives `HG_P(K7-e) <= 12`. The twin-completion/Hall theorem and coordinate-line criterion are correct and are sufficient, not a classification of all winning strategies.

The two explicit `S(5,6,12)` block lists each complete all 792 pentads exactly once, share no block, and yield compatible fixed-point-free involutions on every one of the 495 set-coordinate lines. All 31,680 local contexts pass.

The displayed three permutations generate 95,040 elements and give all 95,040 ordered images of the base pentad. On all 59,400 ordered coordinate lines, `F_6` has type `(2,2,2,2)` and the other six orbit maps have type `(4,4)`. The compatible pairs are exactly `{F_6,F_y}` for `y in {5,7,8,9,10,11}`. The selected pair has zero pointwise equalities, zero composition fixed points, and zero failures over 3,801,600 local contexts.

The cross-check holds: `F_6` is the first Witt-design completion map, while `F_5` is genuinely order-sensitive. The two lower-bound proofs are distinct.

The disjoint completion-design theorem, scoped even-`n` obstruction, and prime-admissibility theorem are also correct. Prime admissibility is not an existence theorem.

## Composition

Either explicit construction gives `HG_P(K7-e) >= 12`; the source upper bound gives `HG_P(K7-e) <= 12`. Therefore

\[
\boxed{\mathrm{HG}_P(K_7-e)=12}.
\]

## Non-mathematical cleanup noted

1. Neutral filenames are preferable because the group identification is not a premise.
2. Negative controls should be exposed through an obvious verifier command.
3. A leftover internal typo-guard field can be removed.
4. The novelty scan is chronology evidence, not a proof obligation.
5. No explicit residual matching is needed; the degree bound proves Hall.

None of these is a first invalid inference. No mathematical repair is required.
