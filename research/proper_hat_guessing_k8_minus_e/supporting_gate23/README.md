# K8-e Gate 2/3 — repaired reseal v2

Date: 4 September 2026. The supplied independent review returned
ACCEPT_WITH_EXPLICIT_REPAIRS. This package makes those repairs while preserving
the original frozen construction data and the review itself.

The accepted K8-e=14 result is unchanged. This package concerns the surrounding
Hall-obstruction analysis, not a new full-game theorem.

## Mathematical and finite conclusions

The equal sector is balanced. The distinct sector has surplus (n-3)(q)_k.
Every one of the 23 frozen bad rules has one absent equal view and exactly
one orbit of matching deficiency. The nonisolated part of each such equal
graph is connected; the full graph also contains the isolated right vertex.

The exact 2,000-rule experiment has 1,843 successful rules and 157 deficient
rules: 153 of deficiency one and four of deficiency two, with no distinct
sector failure. This is a sampled finite classification, not a universal
theorem.

For the accepted rule, the corrected unrestricted trapped spectrum is
kappa_m=floor(m/2), 0<=m<=12. The previously printed connected-union values
remain correct under their proper label.

## Read-only verification

Inspect the code before execution. After authenticating the ZIP using the
detached digest provided with the handoff:

```
python3 -B VERIFY_PACKAGE.py
python3 -B VERIFY_PACKAGE.py --full
```

The default checks the manifest, 23 frozen absent-view predicates, and the
singleton Hall witness. It does not pretend to reconstruct the 2,000 samples.
The full mode additionally replays the reviewer’s independently written
geometry, matchings, connected census, and sampled rules. Dependencies for
full mode: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, GCC/libstdc++ 14.2.0.
Only Python standard library is needed for the default.

Every generated file goes to disposable scratch. The source manifest is
checked before and after. No network or external repository input is needed.

## Evidence boundaries

The review in REVIEW is user-supplied evidence, not a claim of conventional
peer review. Its scope is Gate23 v1. The repairs are documented in
REPAIR_DISPOSITION.md. New quota-flow and robustness results are in a separate
package pending their own review.
