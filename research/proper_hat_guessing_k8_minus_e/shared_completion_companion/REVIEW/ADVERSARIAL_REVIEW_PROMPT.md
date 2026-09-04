# Review request: diagonal-safe synthesis and a robust K8 strategy family

Return ACCEPT_NEW_ORIENTATION_ENVELOPE_RESULT, ACCEPT_WITH_EXPLICIT_REPAIRS,
REJECT_NEW_ORIENTATION_ENVELOPE_RESULT, or INDETERMINATE.

Do not inherit acceptance from the Gate23 review or the previously accepted
K8-e strategy. This package's exact robust family is new.

Reconstruct the mathematics before running the supplied programs:
1. Verify the diagonal quota-flow capacities and fractional flow.
2. Verify preservation under pair reversals and residual-cycle exchanges.
3. Prove that the union of the two distinct residual boards is all
   n(n-1) off-diagonal cells, and rederive the 2n-3 cost per mutable fibre.
4. Check the common-completion matching equivalence, especially the fact
   that one labeled clique view/guess covers at most one coloring orbit.
5. Check free-action/local-view lift and the units of the quotient counts.
6. Independently read all 990 omitted pairs and the explicit mutable set.
7. Check all 5,940 equal and 47,510 envelope matching rows. A matching
   algorithm is unnecessary: every edge and unique right endpoint is data.
8. Independently check all local orientations in all 63,360 normalized
   proper colorings (87,680 contexts total).
9. Confirm that 381 mutable orbits are impossible IN THIS COMMON-CLIQUE
   MODEL, not in every possible strategy-family model.
10. Confirm that the 136 pilots are only finite corroboration and that
    neither a general-n existence theorem nor a new full coloring sweep
    is claimed.

Optional implementation checks:
- Run VERIFY_PACKAGE.py --all-pilot after source inspection.
- Run the four rejecting controls.
- Regenerate in new scratch with the pinned NumPy/SciPy versions.
- Confirm the source-tree hashes are unchanged after verification.

Identify the first invalid implication for any defect. Keep mathematical,
computational, independence, and publication status separate.
