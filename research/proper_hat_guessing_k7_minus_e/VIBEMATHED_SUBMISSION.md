# VibeMathed submission — `HG_P(K7-e)=12`

**Name:** The proper hat-guessing number of $K_7-e$

**Short name:** $\mathrm{HG}_P(K_7-e)=12$

**Result:** Proved

**Statement:** Determine the exact proper hat-guessing number of the complete graph on seven vertices with one edge removed. The general bounds leave $\mathrm{HG}_P(K_7-e)\in\{11,12\}$.

**Solve date:** 2026-09-03

**Source:** Use the immutable public `k7e-v0.1-reviewed` commit in `matthewprotti/proper-hat-guessing-k5-minus-e`.

**AI contribution:** AI co-developed

**Model/vendor:** GPT-5.6 Pro / OpenAI

**Verification:** Preprint (unrefereed), with an independent adversarial review accepted. Do not select independently expert-verified unless the reviewer is named and meets the site's expert-independence criteria.

**Publication:** Announced; update to Preprint after an archival manuscript deposit.

**Field:** Graph theory; hat-guessing games; Steiner systems; permutation groups

**Method:** Construction

**Status:** Candidate (review accepted; conventional peer review pending)

**What was actually shown:** We prove $\mathrm{HG}_P(K_7-e)=12$. One lower-bound proof uses two explicit block-disjoint $S(5,6,12)$ Witt designs. A second uses orbit maps from an explicitly regenerated sharply five-transitive twelve-point permutation group, combining one set-symmetric and one order-sensitive rule. Both satisfy a general coordinate-line twin-completion criterion, and Hall's theorem completes the clique strategy. The release also proves a disjoint completion-design theorem, an even-$n$ obstruction scoped to set-symmetric line-permutation twins in this sufficient framework, and a prime-admissibility theorem for the design parameters. It does not solve the general $K_n-e$ problem or $K_8-e$.

**Verification note:** The independent reviewer rebuilt both 132-block designs, all 792 pentad completions, design disjointness, the 95,040-element group, sharp five-transitivity, all 495 set lines, all 59,400 ordered lines, and both Hall-degree censuses, and returned `ACCEPT_K7E_THEOREM`. The public package includes the review, compact certificate, dependency-free verifier, explicit block lists, and rejecting negative controls.
