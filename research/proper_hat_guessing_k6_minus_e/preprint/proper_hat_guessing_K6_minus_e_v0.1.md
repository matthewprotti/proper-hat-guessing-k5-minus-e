---
title: "The Proper Hat-Guessing Number of $K_6-e$"
author: "Matthew Protti (Independent Researcher)"
date: "3 September 2026 - public research disclosure v0.1"
geometry: margin=1in
fontsize: 11pt
header-includes:
  - \usepackage{amsmath,amssymb,booktabs}
---

# Abstract

We prove that the proper hat-guessing number of the complete graph on six vertices with one edge removed is ten. The lower bound uses two order-sensitive twin-player rules obtained by deleting and repairing one point of an explicit sharply four-transitive permutation group on eleven points. On every coordinate line the repaired rules are derangement permutations, are pointwise unequal, and have fixed-point-free composition. A Hall-matching argument then completes the strategy on the four clique vertices. We also classify all seven orbit labels under the deletion repair and prove that for even $n$ no set-symmetric twin rule can be a permutation on every coordinate line. A dependency-free verifier regenerates the complete finite core.

# 1. Setting and upper bound

Let $K_n-e$ have two nonadjacent twin vertices and an $(n-2)$-vertex clique. The proper hat-guessing number $\mathrm{HG}_P(G)$ is the largest number of colours for which players can choose deterministic local guessing rules such that every proper colouring makes at least one guess correct.

Adriaensen et al. proved

$$
\mathrm{HG}_P(G)\le |V(G)|+\chi(G)-1.
$$

For $K_6-e$, this gives

$$
\mathrm{HG}_P(K_6-e)\le 6+5-1=10.
$$

It remains to construct a winning ten-colour strategy.

# 2. Twin completion

Let $k=n-2$, $q=2n-2$, and let $\alpha,\beta$ be legal rules for the two twins on injective ordered $k$-tuples of clique colours. Fix a clique coordinate and freeze the other $k-1$ coordinates. If $D$ is the set of $n+1$ remaining colours, let $f,g:D\to D$ be the induced line maps.

Suppose that on every line:

1. $f$ and $g$ are permutations;
2. $f(r)\ne g(r)$ for every $r$;
3. $g\circ f$ has no fixed point.

Then, when the twins have different colours, at least one possible completion of the unseen clique coordinate is already covered by a twin; when the twins have the same colour, at least two completions are covered.

Form the residual incidence graph. Its left vertices are residual proper colourings. Its right vertices are labelled pairs $(\text{clique vertex},\text{attainable local view})$. Every left degree is $n-2$, and the preceding local condition makes every right degree at most $n-2$. Hall's theorem supplies a matching saturating the residual colourings, and hence consistent guesses for the clique vertices. Therefore the three line conditions imply

$$
\mathrm{HG}_P(K_n-e)=2n-2.
$$

This is a sufficient construction framework, not a characterization of every winning strategy.

# 3. Explicit eleven-point action

Let $\Omega=\{0,1,\ldots,10\}$ and generate $G\le S_{11}$ by

$$
a=(0\ 1\ 2\ 3\ 4\ 5\ 6\ 7\ 8\ 9\ 10)
$$

and

$$
b=(2\ 6\ 10\ 7)(3\ 9\ 4\ 5).
$$

Breadth-first closure gives exactly $7,920$ permutations, and the images of $(0,1,2,3)$ are all $7,920$ injective ordered four-tuples. Thus every such tuple $T$ determines a unique element $g_T$.

For $y\notin\{0,1,2,3\}$, set

$$
F_y(T)=g_T(y).
$$

Each $F_y$ is a fixed-point-free permutation on every eight-point coordinate line. The generated action is the standard eleven-point Mathieu action, but that identification is not used as a premise.

# 4. Delete point 10 and repair

Delete point $10$. For an ordered four-tuple $T$ over the ten retained colours, retain $F_y(T)$ unless it equals $10$. If it does, replace each coordinate of $T$ in turn by $10$ and evaluate $F_y$ on the four resulting tuples.

For $y=4$ and $y=6$, the four replacement values agree in all 720 repair cases and are legal. Write

$$
\alpha=\overline F_4,\qquad \beta=\overline F_6.
$$

On each seven-point retained line, the input that formerly mapped to the deleted point is redirected to the retained value formerly attained at input $10$. Hence the repaired map remains a derangement permutation.

The complete line check gives:

- $\alpha(T)\ne\beta(T)$ on all 5,040 ordered four-tuples;
- both repaired functions have cycle type $(3,4)$ on all 2,880 lines;
- $\beta\circ\alpha$ is a 7-cycle on all 2,880 lines.

The twin-completion criterion therefore yields a winning ten-colour strategy. Combining this with the upper bound proves

$$
\boxed{\mathrm{HG}_P(K_6-e)=10}.
$$

# 5. Classification of the repair labels

The same finite reconstruction classifies all seven labels outside the base tuple:

| class | labels |
|---|---|
| coherently repairable | $4,5,6,7,8,10$ |
| not repairable | $9$ |

Every repairable label has 720 repair tuples, a flat 72-per-colour replacement histogram, and cycle type $(3,4)$ on every retained line.

Among the fifteen pairs of repairable functions, exactly

$$
\{4,6\},\qquad\{5,10\},\qquad\{7,8\}
$$

satisfy the line criterion. These three pairs form one orbit under the setwise stabilizer of the base tetrad.

The tetrad stabilizer has order 24 and orbits

$$
\{9\},\qquad\{4,5,6,7,8,10\}.
$$

The orbit of $\{0,1,2,3,9\}$ has 66 five-element blocks, and every four-subset of the eleven-point set lies in exactly one block. Thus label $9$ is the distinguished Witt-design completion of the base tetrad; it is precisely the non-repairable label.

# 6. Even-n obstruction

Assume $n$ is even and one twin rule depends only on the unordered set $B$ of the $n-2$ clique colours, while restricting to a permutation on every coordinate line. For each output colour $y$, the fibres

$$
\mathcal B_y=\{B:A(B)=y\}
$$

form a Steiner system $S(n-3,n-2,2n-3)$. Counting blocks through an $(n-4)$-subset gives replication number

$$
\frac{n+1}{2},
$$

which is nonintegral. Therefore no such rule exists for even $n$.

This obstructs only set-symmetric line-permutation twin rules inside the Hall-completion framework. It does not obstruct the value $2n-2$ itself and does not characterize all possible winning strategies.

# 7. Verification and status

The dependency-free verifier regenerates the group, every repair, all coordinate lines, the label classification, the Witt-design check, and the complete residual right-degree census. It checks all 181,440 proper ten-colourings and obtains maximum residual right degree four.

The theorem has survived a separate adversarial review that independently regenerated the principal finite core and required the scope repairs reflected here. Conventional journal peer review is not claimed.

# AI-use disclosure

OpenAI GPT-5.6 Pro contributed substantively to literature search, construction search, proof development, code generation, exact verification, adversarial critique, and manuscript preparation. Matthew Protti selected and framed the target, directed and evaluated the research, required exact checks, determined the claim scope, approved disclosure, and accepts responsibility.

# Reference

S. Adriaensen et al., *Hat guessing with proper colorings*, arXiv:2603.04909v4, 2026.
