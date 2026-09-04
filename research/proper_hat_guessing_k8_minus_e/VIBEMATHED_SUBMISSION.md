# VibeMathed submission - `HG_P(K8-e)=14`

**Name:** The proper hat-guessing number of $K_8-e$

**Short name:** $\mathrm{HG}_P(K_8-e)=14$

**Result:** Proved

**Statement:** Determine the exact proper hat-guessing number of the complete graph on eight vertices with one edge removed. The general bounds leave $\mathrm{HG}_P(K_8-e)\in\{13,14\}$.

**Solve date:** 2026-09-04

**Source:** Use the immutable public commit on branch `k8e-v0.1-public` in `matthewprotti/proper-hat-guessing-k5-minus-e`.

**AI contribution:** AI co-developed

**Model/vendor:** GPT-5.6 Pro / OpenAI

**What the AI did:** OpenAI GPT-5.6 Pro contributed substantively to literature search, target selection, construction search, proof development, code generation, exact verification, adversarial critique, certificate design, and manuscript and release preparation. Matthew Protti selected and framed the target, directed and evaluated the work, commissioned review, required exact checks, determined the public scope, approved disclosure, and accepts responsibility.

**Verification:** Select `Unreviewed`. Explain that the computer-assisted theorem is accepted in the project's adversarial review process and has replayable certificates, but no named independent domain expert, Lean verification, or conventional peer review is claimed. The shared-completion companion remains pending its own independent review.

**Publication:** Announcement

**Field bucket:** Combinatorics

**Field detail:** Graph theory; hat-guessing games; finite geometry; matching theory

**Method:** Computation (finite certificate)

**Status:** Candidate (review pending)

**Posed by / year:** Adriaensen et al. / 2026

**What was actually shown:** We prove $\mathrm{HG}_P(K_8-e)=14$ using an explicit $\mathrm{PGL}(2,13)$-equivariant strategy. A compact formula fixes 990 normalized twin decisions, and a 48,510-edge residual-orbit matching induces consistent rules on 53,460 labelled clique-view orbits. Independent implementations regenerate the certificate and check all 138,378,240 proper fourteen-colourings with zero failures. Unlike the $n=5,6,7$ constructions, residual right degrees reach eight, so the explicit global matching is load-bearing. A separately labelled companion exhibits one fixed clique completion compatible with $2^{380}$ equivariant twin-rule pairs and proves 380 optimal within the stated independent whole-tail reversal model; that companion's independent review is pending. The release does not solve the general $K_n-e$ family or $K_9-e$.

**Verification note:** The sealed main package passes manifest verification, deterministic regeneration, an independent data-only orbit-and-matching checker, three rejecting mutation controls, and an independent C++ sweep of all 138,378,240 proper colourings. The theorem is accepted within the project's adversarial review process, but this is not named expert verification or journal peer review. The shared-completion companion separately passes its standard-library certificate checker, all 136 frozen pilot certificates, and four semantic negative controls; its new $2^{380}$ result remains independently unreviewed.

**Reviewer note:** Related to the existing $K_5-e$, $K_6-e$, and $K_7-e$ entries, but this is the distinct $K_8-e$ exact case. The primary theorem and the shared-completion companion have deliberately different review statuses. Do not treat the Gate 2/3 diagnostics or the companion as inheriting acceptance from the headline theorem.
