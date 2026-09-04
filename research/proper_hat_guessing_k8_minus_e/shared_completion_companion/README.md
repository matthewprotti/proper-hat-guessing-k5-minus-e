# K8-e: diagonal-safe synthesis and a 380-orbit robust orientation family

Private research continuation, 4 September 2026.
Status: complete internally checked computer-assisted candidate; independent
adversarial review of the NEW results is pending.

The incoming Gate23 review has been incorporated in a SEPARATE repaired
reseal. Its acceptance does not extend automatically to this package.

## Principal result

One fixed set of clique guessing functions works for 2^380 distinct
PGL(2,13)-equivariant twin-rule pairs, obtained by independently reversing
the two omitted diagonal colors on 380 specified normalized clique tails.

The diagonal matching is unchanged for every member of the family. A single
47,510-row matching covers the union of all distinct-sector residuals.
Together they use 53,450 of 53,460 possible clique-view orbits.

380 is optimal in the explicitly defined model of independently reversible
WHOLE tail orbits sharing a common clique completion: a 381-orbit envelope
would contain 47,523 distinct residual orbits but only 47,520 right views.

This does NOT prove a general-n result or claim that every legal twin pair,
every diagonal-safe rule, or every 380-tail selection works.

## Verification without a solver or third-party package

Inspect the code and authenticate the ZIP against the supplied detached
SHA-256 before execution.

```
python3 -I -S -B VERIFY_PACKAGE.py
python3 -I -S -B VERIFY_PACKAGE.py --all-pilot
```

The first command checks every family matching edge, the full local-view
inventory, all 87,680 local coloring/orientation contexts, and four rejecting
mutation controls. The second additionally checks all 136 pilot matching
certificates. Both use only the Python standard library and write nothing
inside the package.

No new 138-million full-coloring sweep was run. The full domain follows from
the explicitly reconstructed free projective action and local-view lift.

## Regeneration

Search/construction uses NumPy 2.3.5 and SciPy 1.17.0:

```
python3 -B REPRODUCE.py --output /path/to/new/external/scratch
```

The output directory must not exist and must lie outside the package.
It regenerates the 8-flow/136-orientation panel and the envelope, then
requires byte equality of the frozen certificate data and independently
checks the regenerated certificates.

The first diagonal-safe selection is the inherited frozen pilot; the other
seven are fresh quota-flow constructions. The panel is corroboration. The
2^380 theorem follows from the envelope lemma and its one exact matching,
not from an extrapolation of the panel's success rate.

## Files

* THEOREMS/: the general flow and orientation-envelope lemmas, exact K8
  corollary, and scope limits.
* FAMILY/: four compact files defining the principal robust family.
* PILOT/: exact pairs, orientation bitmaps, and matching-position witnesses
  for all 136 finite trials.
* TOOLS/: separate builder and data-only checker implementations.
* RESULTS/: check receipts and semantic negative controls.
* REVIEW/: adversarial-review prompt and claim matrix.
* SOURCE/: immutable input identities and inherited pair data.

The builders and checkers were written/tested in the same assistant session.
They differ in normalization and data flow, but are NOT a blinded external
review. No GitHub, email, VibeMathed, or other public write was performed.
