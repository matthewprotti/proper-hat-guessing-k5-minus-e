# Free-action quotient, lifting, and units

Let a finite group G preserve a bipartite graph B=(L,R;E), acting freely on
both vertex parts. Form the simple orbit incidence graph. Multiple edge
orbits, if present, do not create extra vertex capacity.

A matching of orbit pairs lifts: choose one edge for each matched orbit pair
and take every G-translate. Freeness makes those translated edges a matching
covering the two full vertex orbits. Distinct orbit pairs do not share
vertices.

Conversely, a set S of left orbits lifts to the union of its full vertex
orbits. Its neighborhood is precisely the union of the adjacent right
orbits. Thus its Hall shortage is multiplied by |G|.

Let d_bar be maximum left deficiency of the quotient. A maximum quotient
matching lifts to show d(B)<=|G|d_bar. A quotient Hall-deficiency witness lifts
to show d(B)>=|G|d_bar. Therefore
\[
d(B)=|G|d(\overline B).
\]
In particular, saturation is equivalent in the full and quotient graphs.

For the K8 construction, all relevant vertices expose at least three distinct
labeled clique colors, so the PGL(2,13) stabilizer is trivial. The group has
2,184 elements. An orbit deficiency of 1 or 2 is consequently a full
coloring deficiency of 2,184 or 4,368, not one or two individual colorings.

This theorem is about a fixed equivariant twin rule and its residual graph.
It does not supply Hall expansion or assert that all twin rules work.
