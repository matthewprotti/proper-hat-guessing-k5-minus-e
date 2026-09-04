# Equivariant residual-orbit matching lemma

## Lemma

Let a finite group `G` act on a hat-colour set and hence on proper colourings
and labelled local views of a fixed graph. Suppose:

1. the action is free on the proper colourings under consideration;
2. every local-view orbit used in the construction is also free;
3. some players have already been assigned `G`-equivariant local rules;
4. `L` is the set of orbits of residual colourings missed by those rules;
5. `R` is the set of orbits of labelled local views of the remaining players;
6. a residual orbit is joined to a view orbit when a representative colouring
   induces that view and supplies a legal target guess; and
7. this orbit graph has a matching saturating `L`.

Then the matched assignments extend equivariantly to consistent local rules
for the remaining players and cover every residual colouring.

## Proof

Choose one matched representative edge for each left orbit. Freeness on the
right implies that transporting this edge through `G` assigns one target to
each full local view in the matched right orbit, with no internal collision.
Distinct matched right orbits are disjoint, so assignments from different left
orbits do not conflict. Fill every unmatched local-view orbit arbitrarily and
equivariantly with a legal guess. Every residual representative is covered by
its matched player, and equivariance transports that correctness to its entire
colouring orbit. `Square`.

## Application to `K_8-e`

For the fourteen-colour construction, `G=PGL(2,13)`. Every proper colouring
and every relevant clique view contains an ordered triple of distinct visible
clique colours, so its stabilizer is trivial. The finite matching has 48,510
left edges, exactly one for each residual proper-colouring orbit.
