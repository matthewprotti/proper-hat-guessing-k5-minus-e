# Adversarial mathematical review: K8-e Gate 2/3

**Disposition: ACCEPT_WITH_EXPLICIT_REPAIRS**

## Scope and integrity

Reviewed archive: `HGP_K8E_GATE23_DIAGONAL_DM_ANALYSIS_20260904_v1.zip`.

- Observed size: **153,165 bytes**, matching the supplied size.
- Observed SHA-256: `9e5e9deddefe442e38456b4da1ae6a284f737e07b19f811ce00c7afc84b627ab`, matching the supplied digest.
- All 32 manifest-listed files passed the package's integrity check. `VERIFY_PACKAGE.py` passed, including a second check after the audit.

I found no error in the main sector counts, diagonal obstruction, trapped-view duality, or the explicit no-isolated-view counterexample. I independently reconstructed the geometry and matching calculations, including all 2,000 sampled rules. The reported finite matching classifications reproduce.

The principal mathematical presentation repair is to distinguish **maxima over connected unions** from the unrestricted quantity `kappa_m`. The existing census values are correct for connected unions. They are false as unrestricted maxima. The report's introductory paragraph does mention connected unions, so this is a scope/labeling issue, not a failure of the enumeration or of the claimed absence of small Hall obstructions.

The package also needs a more explicit normalization argument, clearer verification coverage, and portable analysis entry points. The separate assertion `HG_P(K8-e)=14` is not fully re-proved here; its upper bound and original acceptance history are outside this archive's stated scope.

## 1. Independent reconstruction and finite results

I did not merely rerun the supplied scripts.

The independent checker enumerates the invertible 2-by-2 matrices over `F_13`, modulo nonzero scalar multiples. It obtains all 2,184 projective permutations and constructs normalization maps from those permutations. This is a different implementation from the determinant/cross-ratio formula copied across the package's Python and C++ sources.

From that independently generated incidence structure, I constructed residual graphs and used SciPy's separately implemented matching routine. Every returned matching was then checked for actual adjacency and for distinct right endpoints. For a deficient graph, a checked matching supplies the lower bound on maximum matching size, and the independently checked Hall witness supplies the upper bound. Thus the exact deficiency claims do not depend on blindly trusting the matching routine's maximality claim.

The seeded-rule generator necessarily uses the specified `std::mt19937`/`std::shuffle` setup to reproduce that experiment. The geometry and matching checks applied to the generated rules are independent of the supplied C++ scouts.

| Claim | Independent outcome |
|---|---|
| Full equal geometry | 7,920 left vertices; 5,940 right vertices; degrees 6 and 8 |
| Full equal-view preimages | Eight preimages in eight distinct tail fibres, for every view |
| Short cycles | No 4-cycles or 6-cycles |
| All 23 frozen bad rules | Exactly one absent equal view; all eight preimages deleted |
| Exact matching sizes for each bad rule | 5,939 equal; 42,570 distinct |
| Present equal graph for each bad rule | Connected, with 5,940 left and 5,939 right vertices |
| Frozen complement witnesses | Reconstructed and checked against their stored right sets |
| Seeds 1 through 300 | 277 saturating residual matchings; 23 deficiencies of one |
| Seeds 1 through 2,000 | 1,843 saturating matchings; 153 deficiencies of one; four of two |
| Distinct-sector deficiencies in all 2,000 seeds | Zero |
| Crafted no-isolated rule | No isolated equal view; full normalized deficiency exactly one |
| Included accepted rule table | Independently checked full matching of size 48,510 |
| Accepted connected-core census | Exactly 95,096 connected unions through size 12 |

The four deficiency-two seeds are **741, 1440, 1502, and 1746**. All have exactly two missing equal views. There was no mismatch between missing-view count and equal-sector deficiency in the 2,000 tested rules.

The original 300-seed witness-emitting program was also rerun. Its entire summary matched `DATA/bad_seed_DM_summary.tsv`, and all **22,770** frozen twin-rule rows matched the regenerated rows. The original 2,000-seed scout's failure table also matched exactly.

These are exact finite results for the tested rules, not a universal assertion about other twin rules.

## 2. General sector-count theorem

Assume `n >= 3`, let `k=n-2`, and let `q=2n-2`. For every ordered injective clique coloring `T`, assume the two guesses are legal and distinct.

The clique uses `k` colors, so there are `q-k=n` colors available to each twin.

### Equal sector

For each `T`, the `n` common twin colors form the diagonal cells. The two distinct guesses remove exactly two cells. Consequently,

`|L_=| = (n-2)(q)_k = k(q)_k`.

An equal right view consists of a hidden clique label, an ordered coloring of the other `k-1` clique vertices, and a common twin color outside those visible colors. Therefore,

`|R_=| = k(q)_(k-1)[q-(k-1)] = k(q)_(k-1)(n+1) = k(q)_k`.

This confirms the balance exactly.

### Distinct sector

For a fixed `T`, there are `n(n-1)` ordered distinct twin pairs. The alpha row and beta column each contain `n-1` such pairs, and their intersection is the single allowed distinct pair `(alpha,beta)`. Hence the twins cover `2n-3` distinct cells, leaving

`n(n-1)-(2n-3) = n^2-3n+3`.

Thus,

`|L_neq| = (q)_k(n^2-3n+3)`.

For a right view, the two distinct twin colors can be selected in `(n+1)n` ordered ways after the visible clique has been colored:

`|R_neq| = k(q)_(k-1)(n+1)n = kn(q)_k`.

Subtracting yields

`|R_neq|-|L_neq| = (n-3)(q)_k`.

All of this algebra is correct. The surplus is zero for `n=3` and strictly positive for `n>=4`. Legality and distinctness of the twin guesses are essential, not cosmetic assumptions.

### Sector separation and diagonal obstruction

Every clique local view contains both twin colors. An edge therefore preserves whether those colors agree, and the two residual sectors are disjoint.

Take `R_=` to mean the **full legal right-view universe, including degree-zero views**. In a balanced bipartite graph, a matching saturating the left side must also saturate the right side. If `z` equal views have residual degree zero, then

`nu(B_=) <= |R_=|-z = |L_=|-z`.

Consequently, the equal-sector deficiency is at least `z`.

An equal view has exactly `q-(k-1)-1=n` legal hidden-color completions. If the twins cover all of them, that view is isolated in the residual graph, proving the advertised diagonal obstruction.

The distinction between `R` and `N(L)` should remain explicit. The full equal graph for an original bad seed is not connected: it has a connected nonisolated part plus one isolated right vertex. The detailed classification report correctly qualifies its connectivity assertion by restricting to present vertices; the README should use the same wording.

## 3. Normalization and units

The normalized counts are also correct:

`|PGL(2,13)| = 14*13*12 = 2184`,

and `(14)_6/2184 = 990`.

Therefore the normalized counts are

`equal: 5940 left, 5940 possible right`,

`distinct: 42570 left, 47520 possible right, surplus 4950`.

The package should explicitly explain why taking this quotient preserves the matching question. Here is the needed argument.

The projective group acts freely on the relevant left and right vertices: a projective transformation fixing three distinct labeled visible colors is the identity. There are more than enough visible clique colors in both kinds of vertex to ensure this condition.

For a matched edge between two quotient orbits, take one representative edge and all its group translates. Freeness makes those translates a matching covering both orbits. Different matched orbit pairs are disjoint, so a quotient matching lifts.

Conversely, a deficient quotient set lifts to the union of its entire left orbits. Its neighborhood is the union of the adjacent right orbits. All orbit sizes are 2,184, so the lifted set has the same strict Hall inequality multiplied by 2,184. A quotient Hall failure is therefore a genuine unnormalized failure, not merely a failure to find an equivariant strategy.

In particular, the reported deficiencies of one and two are **normalized** deficiencies. They should not be described as one or two individual unnormalized colorings.

## 4. Trapped-view duality

For a finite bipartite graph with `Delta=|R|-|L|`, define

`C(A) = {r in R : N(r) subseteq A}`.

Set `S=L\A`. Then, vertex by vertex,

`r notin N(S) <=> N(r) subseteq A`.

Thus `R\N(S)=C(A)`, and

`|N(S)|-|S| = (|R|-|C(A)|)-(|L|-|A|)`

`                 = Delta+|A|-|C(A)|`.

The identity and the claimed equivalence with Hall are correct, including the empty-set case. In particular, `C(empty)` is precisely the set of isolated right vertices. This is what connects the original failures to the zero-order trapped-view inequality.

A useful exact strengthening, with `d(B)=|L|-nu(B)`, is

`d(B) = max_(A subseteq L) (|C(A)|-|A|-Delta)`.

The maximum is nonnegative because `A=L` gives zero. The inequalities are an exact reformulation of Hall, not an independent mixing theorem. The package itself correctly acknowledges this limitation.

## 5. The no-isolated-view counterexample survives

I reconstructed the rule in `DATA/K8_A1_noisol_rules.tsv`, rather than relying on the JSON's summary assertions.

All 990 rows specify two distinct legal guesses. Every one of the 5,940 possible equal views has a retained neighbor.

Let

`A = {((2,3,4); common twin color 5)}`.

For the two right views

`(0,10,8,12)` and `(1,2,3,4)`,

the unique retained neighbor is that element of `A`. Moreover, there are exactly two trapped views for this singleton. Accordingly,

`|A|=1`, `|C(A)|=2`,

and, on taking the complement,

`|S|=5939`, `|N(S)|=5938`.

This proves deficiency at least one without any matching algorithm. Independently checked matchings of sizes 5,939 and 42,570 in the two sectors prove that the full normalized deficiency is exactly one.

The example genuinely disproves the implication “no isolated equal right view implies Hall” within the package's residual framework.

## 6. The low-order spectrum must be labeled correctly

Location: `REPORTS/INEQUALITY_SCOUT.md`, lines 37-55, read alongside the unrestricted definition of `kappa_m` in `THEOREMS/TRAPPED_VIEW_DUALITY.md`.

The spectrum program starts from individual right neighborhoods and adds only neighborhoods that meet the current union. It therefore enumerates **connected unions of right neighborhoods**, not all left subsets of a given cardinality.

I reproduced both the count 95,096 and the printed connected maxima. Those computations are correct. But the table must not be read as the unrestricted `kappa_m=max_(|A|=m)|C(A)|`. Its preceding paragraph already mentions connected unions; adding the restriction directly to the table's label would remove the ambiguity.

### An explicit counterexample to an unrestricted reading

For the included accepted rule, the following are the complete residual neighborhoods:

| Right view | Residual neighbors, written `(tail; common color)` |
|---|---|
| `(0,3,2,9)` | `((10,4,2);7)`, `((12,5,4);3)` |
| `(0,6,3,10)` | `((3,4,12);9)`, `((5,10,3);11)` |

The two neighborhoods are disjoint. Their union `A` has four left vertices and traps exactly these two views. Hence

`|A|=4`, `|C(A)|=2`,

whereas the printed entry at size four is one. The printed entry is a connected-union maximum, not a global maximum. This four-vertex set is **not a Hall violation**, since two is less than four; it challenges only an unrestricted reading of that table entry. The accompanying certificate records all eight full preimages and the retained/deleted status for each of these views.

### The corrected unrestricted spectrum

The independent reconstruction finds seven pairwise disjoint degree-two right neighborhoods. In addition, every connected union in the enumerated range satisfies

`|C(U)| <= |U|/2`.

For an arbitrary `A`, remove any vertices not belonging to the neighborhood of a trapped view, and partition the remaining union into connected components `U_i` of the trapped-neighborhood hypergraph. The left sets are disjoint; each trapped right neighborhood belongs wholly to one component. Applying the enumerated bound to each component gives

`|C(A)| = sum_i |C(U_i)| <= (sum_i |U_i|)/2 <= |A|/2`,

whenever `|A|<=12`.

Conversely, a union of `r` of the disjoint degree-two neighborhoods has size `2r` and traps at least `r` views. Padding by one extra left vertex handles odd sizes. Thus the exact global values, supported by this finite enumeration, are

**`kappa_m = floor(m/2)` for `0<=m<=12`.**

For sizes 1 through 12, these are

`0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6`.

### Why the no-small-obstruction claim remains valid

Even without calculating the corrected maxima, connected enumeration is sufficient to exclude all trapped-view violations of small size.

Given any violating set `A`, replace it by `U=union_(r in C(A)) N(r)`. This does not change its trapped-view set and does not increase its size. Partition `U` into connected trapped-neighborhood components. If the total trapped-view count exceeds the total left count, at least one component has the same strict inequality. That component is a connected union, no larger than `A`, that the enumeration must visit.

The enumeration is complete for connected unions because their constituent neighborhoods admit an ordering in which each new neighborhood intersects the preceding union. Every intermediate union has size at most that of the final union, so the size cutoff cannot exclude a qualifying final set.

This reduction should appear as an explicit lemma. It justifies the use of connected enumeration for finding violations, but does not make connected maxima equal to unrestricted maxima. The size-one entry also deserves special treatment: no singleton connected union exists when minimum right degree is two; the unrestricted value zero follows separately.

## 7. Verification and reproducibility repairs

### State the coverage of PASS

`VERIFY_PACKAGE.py` checks the manifest and calls `MACHINE/verify_frozen_analysis.py`. The latter reconstructs the missing equal views for the 23 frozen rules and the crafted Hall witness.

It does **not** run the 300-seed classification, the 2,000-seed scout, exact matching calculations for all sectors, the component analysis, the accepted-rule spectrum, or the geometric short-cycle checks. A manifest authenticates the stored bytes; it does not independently prove all assertions in those bytes.

The narrow verifier is useful and passes. Its success message should name that scope, or a full-verification mode should be added. This review's independent calculations fill those gaps for the uploaded archive, but the package's own entry point still needs clearer coverage.

### Remove hard-coded external paths

Examples include:

- `MACHINE/accepted_rule_trapped_spectrum.py`, lines 13-14, reads a separate `/mnt/data/k8e_pkg/...` package, although the relevant rule table is present as `DATA/accepted_K8_twin_rules.tsv`.
- `analyze_missing_views.py`, `analyze_equal_components.py`, and `analyze_alternating_cores.py` read `/mnt/data/k8_dm_out` rather than package-relative inputs.

The latter scripts can silently analyze zero files if that external directory is absent. They should consume the combined frozen table or explicitly generated witness files and assert the expected seed inventory before reporting success.

For the accepted spectrum script, the direct repair is to set `ROOT=Path(__file__).resolve().parents[1]` and read `ROOT/'DATA/accepted_K8_twin_rules.tsv'`.

### Pin the sampling implementation

Reproduction used the same GCC 14.2.0 toolchain stated by the package. The C++ shuffle specification fixes distributional behavior, not a universal seed-to-permutation transcript across all standard-library implementations. Preserve the frozen tables, record the standard-library version, and ideally specify a concrete bounded-integer and shuffle algorithm for future cross-toolchain reproduction.

### Clarify the random-model heuristic

The exact ideal-product calculation `P(a fixed equal view is absent)=(1/4)^8` is correct: its eight completions use distinct tail fibres. Therefore the expected number of absent views is exactly `5940/65536`.

The Poisson expression `1-exp(-5940/65536)` approximates the probability of **at least one absent view**. Identifying that with the probability of every possible Hall failure needs an additional approximation that other failure mechanisms are negligible. The no-isolated example proves they are not impossible. The package already labels the Poisson discussion a heuristic; keeping its event explicitly named would make that qualification precise.

## Final assessment

Accept the general algebra, the diagonal obstruction, the trapped-view equivalence, the 23 frozen diagnoses, the crafted no-isolated counterexample, and the stated results of the finite 2,000-rule experiment.

Do not identify the connected census table with the unrestricted `kappa_m`, or treat the narrow package PASS as full verification of all reports. Label the connected table explicitly, add the connected-reduction and quotient arguments, make the analysis scripts portable, and specify the verifier's coverage.

No substantive redesign of the main mathematics is indicated by this audit. The required repairs concern a quantitative scope distinction and the completeness of the proof/reproduction presentation.

## Supporting audit files

- `independent_audit.py`: independent geometry, all frozen rules, witnesses, matching checks, and connected-core census.
- `independent_results.json`: detailed reconstructed results, including all missing-view preimages and corrected spectrum.
- `emit_seeded_rules.cpp`: seeded-rule generator for the specified C++ setup.
- `independent_seed_scout.py`: independent geometry/matching verification of all generated rules.
- `independent_2000_summary.json` and `independent_2000_failures.tsv`: independent extended-scout results.
- `spectrum_scope_counterexample.json`: complete preimage certificate for the four-vertex spectrum example.
- Rerun logs and summaries: direct comparisons with the supplied C++ programs.

Audit environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and g++ (Debian 14.2.0-19) 14.2.0.
