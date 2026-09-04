# Low-degree obstruction and contraction lemma

**Status:** elementary graph-theoretic derivation for review. This is not
claimed as a new theorem of general matching theory.

Let B=(L,R;E) be balanced: |L|=|R|. A degree-zero right vertex immediately
precludes a perfect matching.

For every right vertex of degree one, put a loop on its unique left
neighbour. For every right vertex of degree two, put an edge between its two
left neighbours. Retain all left vertices, including isolated ones. The
result is a multigraph J on L, with one edge object for each low-degree
right vertex.

1. If a component U of J has more edge objects than vertices, those right
   vertices have their entire B-neighbourhood in U. Hence |C(U)|>|U| and
   Hall fails.
2. Otherwise every component is a tree (including an isolated vertex) or a
   unicyclic component (including a loop or a parallel-edge cycle).
3. Every unicyclic component can match all its edge objects to all its
   vertices: orient its cycle consistently and its attached trees outward.
   It leaves no capacity for other right vertices.
4. Every tree component can match its edge objects to all but any chosen
   root: root the tree there and assign each edge to its child. It leaves
   precisely one vertex free, and that vertex can be chosen arbitrarily.

Form a smaller bipartite graph with one unit-capacity vertex for each tree
component and one right object for each original right vertex of degree at
least three. Join a high-degree right object to a tree component iff it had
a neighbour in that component. Original B has a perfect matching iff this
smaller graph has a matching saturating all high-degree right objects.

For the forward direction, the low-degree objects consume all vertices in a
unicyclic component and all but one in a tree, so distinct high-degree right
objects must use distinct tree components. For the reverse direction, choose
as root the actual neighbour of the assigned high-degree object in each
matched tree, and fill the low-degree objects as above. Balance implies that
the number of high-degree right objects equals the number of tree components.

The planted cube is detected by step 1: its eight vertices support twelve
degree-two right objects. The previous one-left/two-singleton-view example is
the two-loops-on-one-vertex case. Isolated-view failures occur before step 1.

Passing this reduction does not by itself establish Hall: the remaining
higher-degree quotient still needs a matching or an expansion proof.
