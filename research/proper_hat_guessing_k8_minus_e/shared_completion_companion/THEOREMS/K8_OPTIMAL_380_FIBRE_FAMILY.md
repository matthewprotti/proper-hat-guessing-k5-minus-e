# K8: an optimal 380-orbit orientation family with one clique completion

Status: complete computer-assisted theorem candidate, independent review
pending. The accepted HG_P(K8-e)=14 result is unchanged.

Use the normalized palette {0,...,13}, with 13=infinity and first three
clique colors (13,0,1). The tails are the 990 lexicographically ordered
injective triples from {2,...,12}.

The file FAMILY/omitted_pairs.bin lists two available colors per tail in
increasing order. They are the omitted diagonal cells of the previously
constructed quota-flow pilot. The 380 mutable tail IDs are explicitly listed
in FAMILY/family_spec.json. Their construction rule (a specified portable
shuffle followed by taking 380 entries) is provenance, not a premise of
certificate acceptance.

Outside those tails, assign the smaller omitted color to alpha and the
larger to beta. Within those tails, independently choose either orientation.
The clique strategy remains fixed.

Two byte strings list matching endpoints by hidden clique position:

* equal_match_j.bin: all 5,940 equal residual coloring orbits;
* distinct_envelope_match_j.bin: all 47,510 distinct envelope orbits.

Each entry is a position 0,...,5. Rows are in lexicographic tail, twin-0 color,
twin-1 color order within the specified residual universe. The checker
reconstructs every view from explicit projective matrices, verifies endpoint
injectivity, and assigns its actual hidden color as the clique guess.
Unmatched views receive the least legal color.

The finite checker establishes:
\[
|L_=|=5,940,\quad |R_=|=5,940,\quad
|L_*|=47,510,\quad |R_{\ne}|=47,520.
\]
The two right sectors are disjoint; together the matchings use 53,450 of
53,460 possible clique-view orbits.

The orientation-envelope lemma proves that this SINGLE clique policy works
for all
\[
\boxed{2^{380}}
\]
distinct equivariant twin-rule pairs in the family.

As a direct redundant check, the verifier tests the 63,360 normalized proper
colorings and both local twin orientations wherever allowed: 87,680 local
coloring/orientation checks, with zero failures. This does not enumerate
2^380 strategies, and does not need to. Each coloring tests only the twin
orientation at its own visible clique tuple.

The unique-normalizer/free-action proof lifts every strategy to the full
138,378,240 proper colorings. A new full 138-million sweep was NOT run.

## Exact optimality within the stated model

At 381 independently mutable WHOLE normalized tail orbits, the distinct
envelope would have
\[
42,570+13\cdot381=47,523
\]
left vertices but only 47,520 right views. A common clique strategy is
impossible by the capacity argument. The exhibited 380-orbit family attains
the greatest possible number of mutable whole orbits in this model.

This is not an optimality theorem for arbitrary strategy encodings,
non-orbitwise freedom, or families that allow their clique policy to vary.
It does not prove the general Kn-e upper-endpoint conjecture or a uniform
PGL expansion theorem.
