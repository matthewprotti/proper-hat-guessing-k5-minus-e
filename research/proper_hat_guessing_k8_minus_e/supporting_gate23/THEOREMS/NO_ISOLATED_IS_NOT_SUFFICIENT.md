# No isolated equal view is not sufficient

The diagonal obstruction shows that an isolated equal-twin right view is
fatal.  The converse is false.

The certificate `DATA/K8_A1_noisol_rules.tsv` specifies two deleted diagonal
colours in each of the 990 normalized clique-tail fibres; interpret them as
the two distinct twin guesses.  Every one of the 5,940 equal-twin right views
has at least one retained neighbour.

Let `A` consist of the single retained equal-twin colouring

```text
tail = (2,3,4)
common twin colour = 5.
```

Two normalized labelled right views have this colouring as their unique
retained neighbour:

```text
(vertex, rem0, rem1, common colour) = (0,10,8,12)
(vertex, rem0, rem1, common colour) = (1, 2,3, 4).
```

Thus

\[
|A|=1,
\qquad
|\mathcal C(A)|=2.
\]

Equivalently, with `S=L_{=}\setminus A`,

\[
|S|=5939,
\qquad
|N(S)|=5938.
\]

Hall fails by one although no equal right view is isolated.  A complete
matching computation also gives:

```text
equal-sector deficiency:     1
distinct-sector deficiency:  0
full residual deficiency:    1.
```

Therefore any proposed mixing theorem must exclude higher-order trapped-view
concentration, not only zero-degree right vertices.
