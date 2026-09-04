# Connected-core reduction and corrected low-order spectrum

Let C(A) be the right views whose entire residual neighborhoods lie inside
A. Isolated right views are handled separately. For a set A define
U=union_{r in C(A)} N(r). Then U is contained in A and C(U)=C(A).

Partition U into connected components of the hypergraph of its trapped
right neighborhoods. The component left sets U_i are disjoint, and every
trapped neighborhood belongs wholly to one component. Moreover
C(U_i) is exactly that component's trapped right objects. Hence
\[
|\mathcal C(A)|=\sum_i|\mathcal C(U_i)|.
\]
If |C(A)|>|A|, then some component has |C(U_i)|>|U_i|. It is no larger than A.

Every connected finite family of neighborhoods can be ordered so that each
new neighborhood meets the union of its predecessors, by traversing a
spanning tree of its intersection graph. Every intermediate union is a
subset of the final union. Thus enumerating connected unions by overlapping
extensions, with a left-cardinality cutoff, is complete for detecting a
violating connected union within that cutoff.

This does NOT identify connected-union maxima with unrestricted kappa_m.

## The accepted K8 rule: exact finite conclusion through 12

The independently supplied and freshly replayed census visits exactly 95,096
connected unions of residual right neighborhoods of size at most 12. Its
connected maxima, for sizes 2 through 12, are
\[
1,1,1,2,2,3,3,3,3,4,4.
\]
There is no size-one connected union because every right degree is at least
two. Every visited union U satisfies 2|C(U)|<=|U|.

The component decomposition therefore proves |C(A)|<=floor(|A|/2) for every
A with |A|<=12, including disconnected A.

There are seven pairwise disjoint degree-two right neighborhoods. Taking r
of them attains at least r trapped views on 2r left vertices. Adding one
arbitrary unused left vertex covers the odd sizes; the upper bound prevents
a larger value. The empty case has no isolated right views. Therefore
\[
\boxed{\kappa_m=\lfloor m/2\rfloor\quad(0\le m\le12).}
\]

This is a finite, rule-specific spectrum theorem supported by the complete
connected census and explicit degree-two neighborhoods in
RESULTS/review_audit_replayed.json. It is not an all-size formula or a claim
about other twin rules.
