# Diagonal quota flow and invariant-preserving exchanges

Status: elementary integral-flow derivations for independent review.
No claim that integral-flow theory itself is new.

Let n>=3, k=n-2, q=2n-2 and M=(q)_k. Before choosing twins there are nM
equal-sector colorings and kM labeled equal views. Every coloring has k
incident views; every view has n hidden-color completions.

Use the network
source -> views -> equal colorings -> tuple fibres -> sink
with capacities 1,1,1,k. Sending 1 from source to each view, 1/n on
each view-coloring incidence, k/n from each coloring to its fibre,
and k from each fibre to sink is a feasible fractional flow of value kM.

Integral max-flow supplies an integral flow of that value. Every view is
assigned to one distinct coloring, and every tuple fibre receives exactly
k selected colorings. Its other two colors are legal distinct twin guesses.
The selected equal colorings are perfectly matched. This establishes
diagonal feasibility for every n, without any color group or prime-power
assumption.

The quotient application requires free vertex actions and preservation of
the incidence multiplicities. These were checked for the K8 pilot; no
automatic claim is made for other quotients.

## Orientation invariance

Swapping the two omitted colors at any collection of tuple fibres does not
alter the selected diagonal cells or their perfect matching. Thus
orientation search can preserve a fixed equal-sector certificate verbatim.

## Residual-cycle exchange lemma

Suppose f is an integral full-value quota flow. Augment by an integer amount
around a directed residual cycle, within all residual capacities. The
result is again a feasible integral flow of the same value.

All source-to-view capacities are saturated, since their sum is the full
flow value; the same holds for the fibre-to-sink capacities. Consequently,
every such new flow still matches every equal view to a distinct coloring
and selects exactly k colors per fibre. Recompute the two omitted colors
to obtain another diagonal-safe pair table.

Any two feasible integral full-value flows can be connected by finitely
many such residual-cycle augmentations: their difference is an integral
circulation, and the positive difference on residual arcs decomposes into
directed cycles. This statement is about full network flows, not an
unjustified single-element exchange property of the selected subsets.

Neither pair reversals nor flow-cycle changes guarantee the distinct
sector. That obligation must be checked separately, or discharged by an
orientation-envelope certificate that covers the allowed reversals.

The present finite results have one inherited diagonal-safe pair table,
seven freshly generated quota flows, and checked distinct completions for
17 orientations of each. The stronger 380-orbit family is proved by one
envelope matching, not by extrapolating from those 136 trials.
