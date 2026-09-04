# `HG_P(K_8-e)=14` — adversarial-review package

This package contains a complete computer-assisted proof candidate that the
proper hat-guessing number of the complete graph on eight vertices with one
edge removed is fourteen.

```text
MATHEMATICAL STATUS: complete candidate
REVIEW STATUS: independent adversarial review pending
PUBLICATION STATUS: private
```

## Verify

From the package root:

```bash
python3 -B VERIFY_PACKAGE.py
python3 -B VERIFY_PACKAGE.py --negative-controls
```

The default command:

- verifies the package manifest;
- compiles and reruns the deterministic C++ builder in a temporary directory;
- compares all three regenerated certificate tables byte-for-byte;
- runs the independent data-only orbit verifier; and
- compiles and runs the independent C++ verifier over all 138,378,240 proper
  colourings.

## Read first

- `THEOREMS/K8E_PGL_EQUIVARIANT_MATCHING_CLOSURE.md`
- `REPORTS/K8E_RESULT_REPORT.md`
- `REVIEW/ADVERSARIAL_REVIEWER_PROMPT.md`
- `REVIEW/CLAIM_AND_DEPENDENCY_MATRIX.md`

## Certificate files

```text
K8_e_q14_twin_rules.tsv                  990 rows
K8_e_q14_clique_rules.tsv             53,460 rows
K8_e_q14_residual_orbit_matching.tsv  48,510 rows
```

The compact twin rule is given symbolically in the theorem. The larger clique
table is induced by the explicit residual-orbit matching.

## Nonclaims

This package does not prove the general `K_n-e` formula, claim conventional
peer review, or treat a solver timeout as evidence. It makes no public-priority
claim by its private existence.
