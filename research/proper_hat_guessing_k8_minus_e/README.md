# The proper hat-guessing number of `K8-e`

> **Public research disclosure v0.1 (4 September 2026)**  
> **Headline status:** `HG_P(K8-e)=14` is accepted in the project's adversarial review process; the proof is computer-assisted, unrefereed, and not peer-reviewed.  
> **Companion status:** the capacity-optimal `2^380` shared-completion family is a complete internally checked computer-assisted candidate; independent review is pending.

## Headline result

Let `K8-e` be the complete graph on eight vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_{P}(K_8-e)=14}.
\]

The source upper bound gives `HG_P(K8-e) <= 14`. The lower bound uses an
explicit `PGL(2,13)`-equivariant strategy: a compact formula supplies the twin
rules, and a certified matching completes the six clique-player rules on the
residual normalized colouring orbits.

The finite proof package records:

```text
PGL(2,13) order:                         2,184
normalized clique tuples:                  990
normalized proper-colouring orbits:     63,360
residual orbits:                         48,510
attainable clique-view orbits:           53,460
saturating residual matching:            48,510
full proper colourings checked:     138,378,240
coverage failures:                            0
```

Unlike the `n=5,6,7` constructions, this proof does not establish the result
through a uniform residual right-degree bound. Its right degrees reach eight,
above the clique size six; the explicit global matching is load-bearing.

The exact sealed construction is in [`accepted_construction/`](accepted_construction/).
Run its read-only verifier from that directory:

```bash
python3 -B VERIFY_PACKAGE.py
```

## Shared-completion companion

The separately labelled companion in
[`shared_completion_companion/`](shared_completion_companion/) exhibits one
fixed collection of clique-player rules that wins with `2^380` equivariant
twin-rule pairs. The pairs are obtained by independently reversing the two
guesses on 380 specified normalized clique-tuple orbits.

The number 380 is optimal **within the stated model** of independently
reversible whole-tail orbits sharing one common clique completion: 380 mutable
tails require 47,510 distinct-sector residual orbits, for which a saturating
matching is supplied; 381 would require 47,523, exceeding the 47,520 available
distinct-sector clique-view orbits.

This is not a bound on all winning-strategy families, on every choice of 380
tails, or on families whose clique rules may change. Its independent review is
still pending and it does not inherit the headline theorem's project-review
status.

Run the companion's standard-library verifier with:

```bash
python3 -I -S -B VERIFY_PACKAGE.py --all-pilot
```

## Supporting Hall-obstruction analysis

[`supporting_gate23/`](supporting_gate23/) preserves the repaired Gate 2/3
analysis, the supplied adversarial review, the corrected connected-core versus
unrestricted-spectrum distinction, and scoped counterexamples. Its disposition
is `ACCEPT_WITH_EXPLICIT_REPAIRS`, with those repairs applied. It concerns the
surrounding Hall-obstruction analysis and is not a separate proof of the full
`K8-e` theorem.

## Evidence boundary

The sealed package directories are preserved without edits so their manifests
remain meaningful. Their internal status files record their status at sealing;
this landing page states the later public-disclosure boundary.

Under VibeMathed's taxonomy the conservative verification label remains
**Unreviewed**: no named independent domain expert, Lean verification, or
conventional peer review is claimed. The repository materials provide exact
certificates, replayable verifiers, negative controls, and explicit limitations.

## Scope

This disclosure does **not** solve the general `K_n-e` family, settle `K9-e`,
claim that the earlier coordinate-line criterion is necessary, or establish a
general envelope-matching theorem. The shared-completion family is a narrowly
defined `K8-e` result, not a commercial or operational guarantee.

Until an archival DOI or arXiv identifier is assigned, cite the immutable
public commit containing this disclosure.
