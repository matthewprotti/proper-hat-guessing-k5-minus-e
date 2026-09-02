# VibeMathed submission fields

## Recommended timing

Submit immediately after the standalone GitHub repository is public. Then email the curator in the existing thread with the submitted entry and permanent repository URL.

## Core fields

- **Name:** The proper hat-guessing number of $K_5-e$
- **Short name:** $\mathrm{HG}_P(K_5-e)=8$
- **Result:** Proved
- **Solve date:** 2026-09-02
- **Source:** https://github.com/matthewprotti/proper-hat-guessing-k5-minus-e
- **AI contribution:** AI co-developed
- **Model:** GPT-5.6 Pro
- **Vendor:** OpenAI
- **Verification:** Unreviewed
- **Publication:** Announced
- **Field:** Combinatorics
- **Field detail:** Graph theory; hat-guessing games
- **Status:** Candidate (review pending)
- **Method:** Construction

## Statement

Determine the exact proper hat-guessing number of the complete graph on five vertices with one edge removed. The existing bounds left $\mathrm{HG}_P(K_5-e)$ in $\{7,8\}$.

## What was shown

The exact value is $\mathrm{HG}_P(K_5-e)=8$. The lower bound uses explicit legal twin-player rules over $\mathbb F_2^3$. After those rules cover 3,024 of the 8,400 proper colorings, the residual-coloring/local-view incidence graph has left degree three and right degree at most three; Hall's theorem supplies consistent guesses for the three clique players. The release also proves a general sufficient twin-completion lemma for $K_n-e$. It does not solve the full $K_n-e$ family or determine $\mathrm{HG}_P(C_5)$.

## AI contribution text

OpenAI GPT-5.6 Pro contributed substantively to literature search, problem selection, construction search, proof development, code generation, computational verification, adversarial critique, and manuscript preparation. The central $\mathbb F_2^3$ construction and Hall-completion proof were developed in a model-assisted process. Matthew Protti selected and framed the target, directed and evaluated the work, required exact checks, set the scope, approved disclosure, and accepts responsibility.

## Verification note

No independent mathematical review yet. The public disclosure contains a self-contained proof, a seven-entry finite certificate, and a dependency-free Python verifier. The verifier reconstructs the residual incidence graph, a saturating matching, and a complete 6,720-entry strategy, then checks all 8,400 proper colorings. Peer review and exhaustive novelty clearance are not claimed.
