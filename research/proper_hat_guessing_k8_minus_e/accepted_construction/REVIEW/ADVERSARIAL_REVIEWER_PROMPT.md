# Independent adversarial review prompt: `HG_P(K_8-e)=14`

You are reviewing a theorem candidate, not a program that printed `PASS`.
The claimed theorem is

\[
\mathrm{HG}_P(K_8-e)=14.
\]

## Required first actions

1. Inspect ZIP paths, duplicate members, symlinks, CRCs, and the external ZIP
   hash before executing package code.
2. Run `python3 -B VERIFY_PACKAGE.py` only after that inspection.
3. Use `REVIEW/CLAIM_AND_DEPENDENCY_MATRIX.md` as a mandatory checklist.
4. Return a Markdown report plus every independent script or certificate used.

## Mathematical review

Independently check:

- the source upper bound and `chi(K8-e)=7`;
- the definition of the proper-colouring hat game;
- that each twin and clique rule depends only on that player's visible hats;
- the cross-ratio normalizer and sharp three-transitivity on 14 colours;
- the compact twin formula, including the integer-label convention after
  normalization;
- all 990 twin rows, 53,460 clique-view orbits, and legal guess domains;
- the residual count `990*49=48,510`;
- every matching edge, distinct right endpoint, and hidden target;
- why a matching on free `PGL(2,13)` orbits lifts to a full local strategy;
- all 63,360 normalized proper-colouring orbits; and
- preferably all 138,378,240 full proper colourings in an independent
  implementation.

Try specifically to find:

- two different views mapping to one normalized key but requiring different
  guesses;
- a nontrivial stabilizer that breaks the orbit lift;
- a matching row that is not incident to its residual colouring;
- a clique guess equal to a visible neighbour colour;
- an uncovered colouring hidden by normalization; or
- a count that mistakenly treats twin colours as necessarily distinct.

## Computational independence

Do not accept the builder as its own verifier. At minimum, parse the frozen
TSV files with an independently written checker. The supplied Python verifier
and C++ full enumeration intentionally use different data paths; inspect both.
Mutation controls must reject a corrupted twin rule, an illegal clique guess,
and a truncated matching.

## Scope

The result is computer-assisted and unrefereed. It does not solve the general
`K_n-e` problem, prove that the orbit matching mechanism is necessary, or give
a symbolic formula for the 53,460 clique choices.

## Required disposition

Return exactly one:

```text
ACCEPT_K8E_THEOREM
ACCEPT_WITH_EXPLICIT_REPAIRS
REJECT_K8E_THEOREM
INDETERMINATE_INSUFFICIENT_EVIDENCE
```

For every defect, identify the first invalid inference, exact file/section,
concrete counterexample or calculation, minimal repair, and effect on the
boxed theorem.
