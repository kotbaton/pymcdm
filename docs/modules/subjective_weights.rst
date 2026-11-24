.. _subjective_weights:

==================
Subjective weights
==================

AHP
=======================
:class:`AHP` is designed to evaluate decision criteria according to the following steps:

**Step 1.** Define the Hierarchical Structure.

The expert establishes a hierarchical framework for the criteria. This hierarchy facilitates systematic comparison of
different aspects of the decision problem.

**Step 2.** Perform Pairwise Comparisons of Criteria.

For each pair of criteria, the expert assesses their relative importance using a scale typically ranging from 1 to 9, where:

- **1** indicates equal importance,
- **3** moderate importance,
- **5** strong importance,
- **7** very strong importance,
- **9** extreme importance.

Reciprocals of these values are used when one criterion is less important than the other.

**Step 3.** Construct the Pairwise Comparison Matrix.

The Pairwise Comparison Matrix (:math:`A`) is a symmetric matrix where each element :math:`a_{ij}` represents the
importance of criterion :math:`C_i` relative to criterion :math:`C_j`.

.. math::
    :label: ahp_matrix

    A =
    \begin{bmatrix}
        1 & a_{12} & a_{13} & \ldots & a_{1n} \\
        \frac{1}{a_{12}} & 1 & a_{23} & \ldots & a_{2n} \\
        \frac{1}{a_{13}} & \frac{1}{a_{23}} & 1 & \ldots & a_{3n} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        \frac{1}{a_{1n}} & \frac{1}{a_{2n}} & \frac{1}{a_{3n}} & \ldots & 1
    \end{bmatrix}

**Step 4.** Calculate the Priority Vector of Criteria.

By default (``prioritization='eigenvector'``), the weights vector (:math:`w`) is the principal right eigenvector of the
pairwise comparison matrix, normalized to sum up to one:

.. math::
    :label: ahp_priority_vector

    A w = \lambda_{\max} w, \qquad \sum_{i=1}^{n} w_i = 1

With ``prioritization='geometric_mean'``, the weights are derived with the Logarithmic Least Squares Method (LLSM), i.e.
as the normalized geometric mean of each row in the pairwise comparison matrix:

.. math::
    :label: ahp_priority_vector_llsm

    w_i = \frac{\prod_{j=1}^{n} \left(a_{ij}\right)^{\frac{1}{n}}}{\sum_{k=1}^{n} \prod_{j=1}^{n} \left(a_{kj}\right)^{\frac{1}{n}}}

Both methods give the same weights for a fully consistent matrix and for any matrix with three criteria. The method can
also be changed later by setting the ``prioritization`` attribute.


**Step 5.** Check the Consistency of the Matrix.

To ensure the reliability of the pairwise comparisons, calculate the Consistency Index (:math:`CI`):

.. math::
    :label: ahp_consistency

    CI = \frac{\lambda_{\max} - n}{n - 1}

where

.. math::
    \lambda_{\max} = \frac{1}{n} \sum_{i=1}^{n} \frac{(A w)_i}{w_i}

and the Consistency Ratio (:math:`CR`):

.. math::
    CR = \frac{CI}{RI}

where :math:`RI` is the Random Consistency Index, which depends on the number of criteria.

If :math:`CR < 0.1`, the pairwise comparison matrix is considered acceptably consistent.

RANCOM
=======================
:class:`RANCOM` is designed to evaluate decision criteria according to the following steps:

**Step 1.** Define the criteria ranking.

The expert determines the position of the criteria regarding other factors. The designated ranking should be defined as
lower values assigned to more significant criteria. Additionally, the criteria may have equal positions in the ranking,
which means that ties are allowed during the expert judgment. The criteria ranking could be defined with subsequent
values (i.e., [1, 2, 3, 4, 5] for five criteria) or could consist of more diverse values (i.e., [1, 5, 9, 12, 18] for
five criteria). However, the differences that occurred in the ranking vector would not affect the calculated weights
unless they include different criteria hierarchy.

**Note:** It is also possible for an expert to compare pairwise criteria in a MAC matrix without indicating a ranking.


**Step 2.** Establish the Matrix of Ranking Comparison.

The Matrix of Ranking Comparison (:math:`MAC`) is determined using pairwise comparisons of the positions of criteria
provided by the expert or based on the expert's rankings. The comparison result is determined as :math:`\alpha_{ij}`.
Based on that, the :math:`MAC` matrix can be represented as (:eq:`mac`):

.. math::
    :label: mac

    MAC =
    \begin{array}{cccc}
     & \begin{array}{ccccc}
    & C_1 & C_2 & \ldots & C_n
    \end{array} \\
    \begin{array}{c}
    C_1 \\
    C_2 \\
    \vdots \\
    C_n
    \end{array} &
        \left[
        \begin{array}{cccc}
             \alpha_{11} & \alpha_{12} & \ldots & \alpha_{1n} \\
             \alpha_{21} & \alpha_{22} & \ldots & \alpha_{2n} \\
             \vdots & \vdots & \ddots & \vdots \\
             \alpha_{n1} & \alpha_{n2} & \ldots & \alpha_{nn}
        \end{array}
        \right] &
    \end{array}


where :math:`n` is the number of criteria taken into account in the problem, and :math:`\alpha_{ij}` is determined from
(:eq:`p1`):

.. math::
    :label: p1

    \alpha_{ij} = \left\{ \begin{array}{lccr}
        IF & f \left( C_i\right)   <  f \left( C_j\right) & THEN & 1  \\
        IF & f \left( C_i\right) =  f \left( C_j\right) & THEN & 0.5 \\
        IF & f \left( C_i\right)  >   f \left( C_j\right) & THEN & 0  \\
    \end{array}
    \right.

where :math:`f \left(C\right)` is a position in ranking for criterion :math:`C` (lower value is better).

**Step 3.** Calculate the Summed Criteria Weights.

Based on the obtained :math:`MAC`, the horizontal vector of the Summed Criteria Weights (:math:`SCW`) is obtained as
follows:

.. math::

    SCW_i=\sum^{n}_{j=1}\alpha_{ij}


**Step 4.** Calculate the final criteria weights.

Finally, values of preference are approximated for each criterion. As a result, the horizontal vector :math:`W` is obtained,
where the :math:`i-th` row contains the approximate preference value for :math:`C_i`. The weights for the set of
criteria are obtained as:

.. math::

        w_{i} = \frac{SCW_{i}}{\sum^{n}_{i=1} SCW_{i}}

SWARA
=======================
:class:`SWARA` (Step-wise Weight Assessment Ratio Analysis) is designed to evaluate decision criteria according to the
following steps:

**Step 1.** Rank the criteria.

The expert orders the criteria from the most to the least important one (parameter ``s``).

**Step 2.** Determine the comparative importance of the criteria.

Starting from the second criterion, the expert states how much more important the previous criterion is than the
current one. The comparative importance :math:`s_j \geq 0` is given for every criterion except the first (parameter
``s_v``).

**Step 3.** Calculate the coefficients.

.. math::
    :label: swara_k

    k_j = \begin{cases} 1 & j = 1 \\ s_j + 1 & j > 1 \end{cases}

**Step 4.** Calculate the recalculated weights.

.. math::
    :label: swara_q

    q_j = \begin{cases} 1 & j = 1 \\ \frac{q_{j-1}}{k_j} & j > 1 \end{cases}

**Step 5.** Calculate the final criteria weights.

.. math::
    :label: swara_w

    w_j = \frac{q_j}{\sum_{k=1}^{n} q_k}

PIPRECIA
=======================
:class:`PIPRECIA` (PIvot Pairwise RElative Criteria Importance Assessment) is designed to evaluate decision criteria
according to the following steps:

**Step 1.** List the criteria.

Unlike SWARA, the criteria do not have to be sorted by their expected significance (parameter ``s`` gives the order in
which they are evaluated).

**Step 2.** Determine the relative importance of the criteria.

Starting from the second criterion, the expert compares each criterion with the previous one (parameter ``s_v``):

.. math::
    :label: piprecia_s

    s_j = \begin{cases} > 1 & \text{if } C_j \succ C_{j-1} \\ 1 & \text{if } C_j = C_{j-1} \\
    < 1 & \text{if } C_j \prec C_{j-1} \end{cases}

with :math:`0 < s_j < 2`.

**Step 3.** Calculate the coefficients.

.. math::
    :label: piprecia_k

    k_j = \begin{cases} 1 & j = 1 \\ 2 - s_j & j > 1 \end{cases}

**Step 4.** Calculate the recalculated weights.

.. math::
    :label: piprecia_q

    q_j = \begin{cases} 1 & j = 1 \\ \frac{q_{j-1}}{k_j} & j > 1 \end{cases}

**Step 5.** Calculate the final criteria weights.

.. math::
    :label: piprecia_w

    w_j = \frac{q_j}{\sum_{k=1}^{n} q_k}

**Simplified PIPRECIA (PIPRECIA-S).** Some respondents find it easier to always compare a criterion with the first
one. In PIPRECIA-S (``comparison='first'``) :math:`s_j` compares the criterion :math:`C_j` with :math:`C_1`, the
coefficients :math:`k_j` are calculated with Eq. :eq:`piprecia_k`, and the recalculated weights are relative to the
first criterion:

.. math::
    :label: piprecia_s_q

    q_j = \frac{1}{k_j}

The final weights are obtained with Eq. :eq:`piprecia_w`.

In group decision-making, the weights obtained from :math:`R` experts can be aggregated with the geometric mean
:math:`w_j = \left(\prod_{r=1}^{R} w_j^r\right)^{1/R}` and normalized to sum to one.

FUCOM
=======================
:class:`FUCOM` (FUll COnsistency Method) is designed to evaluate decision criteria according to the following steps:

**Step 1.** Rank the criteria.

The expert orders the criteria from the most to the least important one (parameter ``o``). Criteria of equal
importance are allowed.

**Step 2.** Determine the comparative priorities of the ranked criteria.

The comparative priority :math:`\varphi_{k/(k+1)}` states how much more important the criterion at position :math:`k`
is than the criterion at position :math:`k+1`. The priorities are given directly (parameter ``i``) or computed from
significance scores :math:`v_k` of the ranked criteria (parameter ``v``), where the first criterion has the score 1:

.. math::
    :label: fucom_phi

    \varphi_{k/(k+1)} = \frac{v_{k+1}}{v_k}

**Step 3.** Calculate the weights.

The weights should satisfy :math:`w_k / w_{k+1} = \varphi_{k/(k+1)}` and the condition of mathematical transitivity
:math:`w_k / w_{k+2} = \varphi_{k/(k+1)} \cdot \varphi_{(k+1)/(k+2)}`. The weights closest to these conditions are
obtained from the model:

.. math::
    :label: fucom_model

    \begin{aligned}
    \min \ & \chi \\
    \text{s.t.} \ & \left| \frac{w_k}{w_{k+1}} - \varphi_{k/(k+1)} \right| \leq \chi, \quad \forall k \\
    & \left| \frac{w_k}{w_{k+2}} - \varphi_{k/(k+1)} \cdot \varphi_{(k+1)/(k+2)} \right| \leq \chi, \quad \forall k \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}

The optimal value :math:`\chi` is the Deviation from Full Consistency (attribute ``dfc``). The value 0 means full
consistency of the comparisons.

For a fixed :math:`\chi` the constraints are linear in the weights, so the model is solved to its global optimum by
bisection on :math:`\chi`, each step being a linear feasibility problem.

BWM
=======================
:class:`BWM` (Best-Worst Method) is designed to evaluate decision criteria according to the following steps:

**Step 1.** Determine the set of decision criteria.

**Step 2.** Determine the best (most important) and the worst (least important) criterion.

**Step 3.** Determine the preference of the best criterion over all the other criteria.

The comparisons are made on a scale from 1 to 9 and give the Best-to-Others vector (parameter ``a_b``), where
:math:`a_{BB} = 1`:

.. math::
    :label: bwm_ab

    A_B = \left( a_{B1}, a_{B2}, \ldots, a_{Bn} \right)

**Step 4.** Determine the preference of all the criteria over the worst criterion.

This gives the Others-to-Worst vector (parameter ``a_w``), where :math:`a_{WW} = 1`:

.. math::
    :label: bwm_aw

    A_W = \left( a_{1W}, a_{2W}, \ldots, a_{nW} \right)

**Step 5.** Calculate the weights.

The weights minimize the maximum absolute difference between the weight ratios and the comparisons:

.. math::
    :label: bwm_model

    \begin{aligned}
    \min \ & \xi \\
    \text{s.t.} \ & \left| \frac{w_B}{w_j} - a_{Bj} \right| \leq \xi, \quad \forall j \\
    & \left| \frac{w_j}{w_W} - a_{jW} \right| \leq \xi, \quad \forall j \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}

For a fixed :math:`\xi` the constraints are linear in the weights, so the model is solved to its global optimum by
bisection on :math:`\xi`. If several criteria have the value 1 in :math:`A_B` (or :math:`A_W`), the best (worst)
criterion is the one for which :math:`a_{BW}` is the largest.

**Step 6.** Check the consistency of the comparisons.

The optimal value :math:`\xi^*` (method ``get_xi``) indicates the consistency of the comparisons; the value 0 means full
consistency. It can be divided by the Consistency Index, the largest possible :math:`\xi` for the given :math:`a_{BW}`,
to obtain the Consistency Ratio:

.. list-table::
   :header-rows: 1

   * - :math:`a_{BW}`
     - 1
     - 2
     - 3
     - 4
     - 5
     - 6
     - 7
     - 8
     - 9
   * - Consistency Index
     - 0.00
     - 0.44
     - 1.00
     - 1.63
     - 2.30
     - 3.00
     - 3.73
     - 4.47
     - 5.23

**Multiple optimal solutions.** For not fully consistent comparisons of more than three criteria the model may have
multiple optimal solutions. The range of the weight :math:`w_j` among them (method ``get_weight_intervals``) is
obtained by minimizing and maximizing :math:`w_j` subject to the constraints of the model with :math:`\xi = \xi^*`.
The centers of the intervals can be used as representative weights. The intervals can also be compared with the
degree of preference (method ``get_interval_preference_degrees``):

.. math::
    :label: bwm_dp

    P(A > B) = \frac{\max(0, a^R - b^L) - \max(0, a^L - b^R)}{(a^R - a^L) + (b^R - b^L)}

where :math:`A = [a^L, a^R]` and :math:`B = [b^L, b^R]`. The criteria are ranked by the number of criteria over
which their degree of preference exceeds 0.5.

**Linear model.** With ``model='linear'`` the weights are obtained from the linear model, which always has a unique
solution:

.. math::
    :label: bwm_linear

    \begin{aligned}
    \min \ & \xi^L \\
    \text{s.t.} \ & \left| w_B - a_{Bj} w_j \right| \leq \xi^L, \quad \forall j \\
    & \left| w_j - a_{jW} w_W \right| \leq \xi^L, \quad \forall j \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}

The value :math:`\xi^L` (method ``get_xi``) is used directly as the indicator of consistency; values close to 0 show
high consistency.

LBWA
=======================
:class:`LBWA` (Level Based Weight Assessment) is designed to evaluate decision criteria according to the following
steps:

**Step 1.** Determine the most important criterion :math:`C_1`.

**Step 2.** Group the criteria by levels of significance.

The level :math:`S_i` contains the criteria whose significance is from :math:`i` to :math:`i + 1` times lower than
the significance of :math:`C_1`; the most important criterion belongs to :math:`S_1`. Levels may be empty. The
criteria grouped by levels are given as a list of lists (parameter ``i``), e.g. ``[[1, 4], [], [0, 2]]``.

**Step 3.** Compare the criteria within the levels.

Each criterion :math:`C_{i_p}` of the level :math:`S_i` is assigned an integer :math:`I_{i_p} \in \{0, 1, \ldots, r\}`
(parameter ``l``, in the order of the criteria in ``i``), where :math:`I = 0` for the most important criterion,
a more important criterion gets a smaller value and equally important criteria get equal values. The largest value
of the scale is the size of the largest level:

.. math::
    :label: lbwa_r

    r = \max \left\{ |S_1|, |S_2|, \ldots, |S_k| \right\}

**Step 4.** Define the elasticity coefficient :math:`r_0 > r` (parameter ``r0``, by default :math:`r + 1`).

**Step 5.** Calculate the influence function of the criteria.

.. math::
    :label: lbwa_f

    f(C_{i_p}) = \frac{r_0}{i \cdot r_0 + I_{i_p}}

**Step 6.** Calculate the weights.

.. math::
    :label: lbwa_w

    w_1 = \frac{1}{1 + f(C_2) + \ldots + f(C_n)}, \quad w_j = f(C_j) \cdot w_1

SIMOS
=======================
:class:`SIMOS` (the original Simos procedure, also called the cards method) is designed to evaluate decision criteria
according to the following steps:

**Step 1.** Rank the criteria.

The decision-maker ranks the cards with the criteria from the least to the most important one; criteria of equal
importance are placed in one subset of ex aequo (parameter ``r``, e.g. ``[[2, 6], 3, [0, 1]]``).

**Step 2.** Insert white cards.

The larger the difference of importance between two successive subsets, the more white cards are inserted between
them (parameter ``w_c``).

**Step 3.** Assign positions.

Every criterion and every white card receives a position: the least important card has the position 1, the next one
the position 2, and so on.

**Step 4.** Calculate the non-normalized weights.

The non-normalized weight of a subset of ex aequo is the average of the positions of its criteria.

**Step 5.** Calculate the normalized weights.

The non-normalized weight of each criterion is divided by the sum of the positions of all criteria (white cards are
not included).

SRF
=======================
:class:`SRF` (the revised Simos procedure, Simos-Roy-Figueira) collects the same information as :class:`SIMOS`
(parameters ``r`` and ``w_c``) and additionally asks how many times the most important criterion is more important
than the least important one (parameter ``z`` >= 1). The weights are determined according to the following steps:

**Step 1.** Calculate the units.

With :math:`e'_r` white cards between the ranks :math:`r` and :math:`r + 1` and :math:`\bar{n}` ranks:

.. math::
    :label: srf_u

    e_r = e'_r + 1, \quad e = \sum_{r=1}^{\bar{n}-1} e_r, \quad u = \frac{z - 1}{e}

**Step 2.** Calculate the non-normalized weights of the ranks.

.. math::
    :label: srf_k

    k(r) = 1 + u \left( e_0 + e_1 + \ldots + e_{r-1} \right), \quad e_0 = 0

The value :math:`u` is rounded to six and :math:`k(r)` to two decimal places. All criteria of the rank :math:`r`
receive the weight :math:`k'_i = k(r)`.

**Step 3.** Calculate the normalized weights.

.. math::
    :label: srf_kstar

    k^*_i = \frac{100}{K'} k'_i, \quad K' = \sum_{i=1}^{n} k'_i

**Step 4.** Round the normalized weights.

The weights :math:`k^*_i` are truncated to :math:`w` decimal places (parameter ``w``) and the missing amount up to 100
is distributed among the criteria with the smallest relative rounding errors, so that the rounded weights sum to
exactly 100. The weights returned by the method are divided by 100.

COBRAC
=======================
:class:`COBRAC` (COmparisons Between RAnked Criteria) is designed to evaluate decision criteria according to the
following steps:

**Step 1.** Rank the criteria from the most to the least important one.

**Step 2.** Compare the adjacent criteria.

For each pair of adjacent criteria the decision-maker gives the share :math:`\xi_{j,j+1} \in (0, 1)` of the more
important criterion, e.g. :math:`\xi = 0.72` means that it takes 72% and the less important criterion 28% of the
interval :math:`[0, 1]`; :math:`\xi = 0.5` means equal importance. The compared pairs (parameter ``pairs``) do not have
to be adjacent, and the shares are given with the parameter ``xis``. This gives the relations:

.. math::
    :label: cobrac_ratio

    w_j : w_{j+1} = \xi_{j,j+1} : \left( 1 - \xi_{j,j+1} \right)

**Step 3.** Calculate the weights.

.. math::
    :label: cobrac_model

    \begin{aligned}
    \min \ & \partial \\
    \text{s.t.} \ & \left| \frac{w_j}{w_{j+1}} - \frac{\xi_{j,j+1}}{1 - \xi_{j,j+1}} \right| \leq \partial,
    \quad \forall j \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}

For a fixed :math:`\partial` the constraints are linear in the weights, so the model is solved to its global optimum
by bisection on :math:`\partial`. The optimal value (method ``get_delta``) is 0 when the comparisons are consistent,
which is always the case when only adjacent criteria are compared.

ITARA
=======================
:class:`ITARA` (Indifference Threshold-based Attribute RAtio Analysis) uses the decision matrix and the indifference
thresholds given by the decision-maker. Criteria whose values differ more than the thresholds receive higher
weights. The weights are determined according to the following steps:

**Step 1.** Determine the decision matrix and the indifference threshold :math:`IT_j` of each criterion
(parameter ``t``).

**Step 2.** Normalize the decision matrix and the indifference thresholds.

.. math::
    :label: itara_norm

    \alpha_{ij} = \frac{a_{ij}}{\sum_{i=1}^{m} a_{ij}}, \quad NIT_j = \frac{IT_j}{\sum_{i=1}^{m} a_{ij}}

**Step 3.** Sort the normalized values of each criterion in ascending order, obtaining
:math:`\beta_{1j} \leq \beta_{2j} \leq \ldots \leq \beta_{mj}`.

**Step 4.** Calculate the distances between adjacent values.

.. math::
    :label: itara_gamma

    \gamma_{ij} = \beta_{i+1,j} - \beta_{ij}, \quad i = 1, 2, \ldots, m - 1

**Step 5.** Calculate the considerable differences.

.. math::
    :label: itara_delta

    \delta_{ij} = \begin{cases} \gamma_{ij} - NIT_j & \gamma_{ij} > NIT_j \\ 0 & \gamma_{ij} \leq NIT_j \end{cases}

**Step 6.** Calculate the weights with the :math:`l_p` metric (parameter ``p``, :math:`p = \infty` gives the largest
:math:`\delta_{ij}`).

.. math::
    :label: itara_w

    \omega_j = \frac{v_j}{\sum_{j=1}^{n} v_j}, \quad v_j = \left( \sum_{i=1}^{m-1} \delta_{ij}^p \right)^{1/p}

BCM
=======================
:class:`BCM` (Base-Criterion Method) is designed to evaluate decision criteria according to the following steps:

**Step 1.** Determine the set of decision criteria.

**Step 2.** Select the base-criterion.

Unlike in BWM, the base-criterion does not have to be the best or the worst criterion; it can be any criterion
preferred by the decision-maker.

**Step 3.** Determine the relative importance of the base-criterion over the other criteria.

The comparisons are made on a scale from 1/9 to 9 and give the base-comparison vector (parameter ``a_b``), where
:math:`a_{BB} = 1`. If several elements are equal to 1, the base-criterion has to be indicated with the parameter
``base_index``.

.. math::
    :label: bcm_ab

    A_B = \left( a_{B1}, a_{B2}, \ldots, a_{Bn} \right)

The other comparisons (final comparisons, method ``get_full_matrix``) follow from the base-comparisons, so the
decision-maker should choose them so that they stay within the scale:

.. math::
    :label: bcm_aij

    a_{ij} = \frac{a_{Bj}}{a_{Bi}}, \quad \frac{1}{9} \leq a_{ij} \leq 9

**Step 4.** Calculate the weights.

.. math::
    :label: bcm_model

    \begin{aligned}
    \min \ & \xi \\
    \text{s.t.} \ & \left| \frac{w_B}{w_j} - a_{Bj} \right| \leq \xi, \quad \forall j \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}

For a fixed :math:`\xi` the constraints are linear in the weights, so the model is solved to its global optimum by
bisection on :math:`\xi`. Because only the base-comparisons are given, the comparisons are always fully consistent
(:math:`\xi = 0`, method ``get_xi``) and :math:`w_j \propto 1 / a_{Bj}`.

VIMM
=======================
:class:`VIMM` (Vital-Immaterial-Mediocre Method) is designed to evaluate decision criteria according to the following
steps (the first scenario, one decision-making goal):

**Step 1.** Determine the vital and the immaterial criteria.

The vital criterion has the largest and the immaterial criterion the smallest impact on the decision (parameters
``vital_index`` and ``immaterial_index``). They receive the scores :math:`\alpha_1 = 5` and :math:`\beta_1 = 1`.

**Step 2.** Compare the remaining criteria with the vital and the immaterial criteria.

The comparisons are made on a scale from 2 (less importance) through 5 (equal importance) to 9 (more importance);
fractions are allowed. The comparisons of round :math:`x` are given as ``c_vital[x]`` and ``c_immaterial[x]``, in the
order of the indices of the remaining criteria.

**Step 3.** Calculate the distances.

The distance :math:`d^+_{xy}` of the criterion :math:`y` from the immaterial criterion and the distance
:math:`d^-_{xy}` from the vital criterion in round :math:`x` are:

.. math::
    :label: vimm_d

    d^+_{xy} = c^{I}_{xy} - 1, \quad d^-_{xy} = 10 - c^{V}_{xy}

**Step 4.** Normalize the distances and calculate the scores.

.. math::
    :label: vimm_s

    S_{xy} = \frac{d^+_{xy}}{\max_y d^+_{xy}} + \frac{\min_y d^-_{xy}}{d^-_{xy}}

The criterion with the highest score becomes the next vital criterion and the criterion with the lowest score the
next immaterial criterion.

**Step 5.** Repeat Steps 2–4 until two criteria (even number of criteria) or one criterion (odd number of criteria)
remain.

In each subsequent round, every vital criterion receives the score 5 and the latest immaterial criterion the score 1;
the earlier immaterial criteria receive 0. The last remaining criterion is treated as vital.

**Step 6.** Calculate the weights.

The total score :math:`S_j` of each criterion is the sum of its scores in all rounds (method ``get_scores``), and the
weights are:

.. math::
    :label: vimm_w

    W_j = \frac{S_j}{\sum_{j=1}^{n} S_j}

OWCM
=======================
:class:`OWCM` (Opinion Weight Criteria Method) derives the weights from the opinions of the decision-maker about the
alternatives, according to the following steps:

**Step 1.** Build the opinion matrix.

For each criterion, the decision-maker compares the value of each alternative with the ideal value of the criterion
(the maximum for benefit criteria, the minimum for cost criteria, or a critical value between them) and assesses the
difference on a five-point scale, which gives the crisp opinion matrix (parameter ``M``):

.. list-table::
   :header-rows: 1

   * - Linguistic term
     - No difference
     - Slight difference
     - Difference
     - Big difference
     - Huge difference
   * - Value
     - 1
     - 2
     - 3
     - 4
     - 5

**Step 2.** Normalize the opinion matrix.

.. math::
    :label: owcm_r

    R_{ij} = \frac{x_{ij}}{\max_i x_{ij}}

**Step 3.** Calculate the mean of each criterion.

.. math::
    :label: owcm_mean

    \bar{N}_j = \frac{1}{m} \sum_{i=1}^{m} R_{ij}

**Step 4.** Calculate the preference variation.

.. math::
    :label: owcm_phi

    \phi_j = \sum_{i=1}^{m} \left( R_{ij} - \bar{N}_j \right)^2

**Step 5.** Calculate the deviation of the preference values.

.. math::
    :label: owcm_omega

    \Omega_j = 1 - \phi_j

**Step 6.** Calculate the weights.

.. math::
    :label: owcm_w

    w_j = \frac{\Omega_j}{\sum_{j=1}^{n} \Omega_j}

ROC, RS, RR and RE
=======================

Rank-based (surrogate) weights need only the ranking of the criteria from the most to the least important
(parameter ``order``). With :math:`n` criteria, the weight of the criterion at position :math:`i` of the ranking is:

* :class:`ROC` (Rank Order Centroid) [#rocref1]_: the centroid of all weight vectors consistent with the ranking,

.. math::
    :label: roc_w

    w_i = \frac{1}{n} \sum_{k=i}^{n} \frac{1}{k}

* :class:`RS` (Rank Sum) [#rocref2]_:

.. math::
    :label: rs_w

    w_i = \frac{n - i + 1}{\sum_{k=1}^{n} (n - k + 1)} = \frac{2 (n - i + 1)}{n (n + 1)}

* :class:`RR` (Rank Reciprocal) [#rocref2]_:

.. math::
    :label: rr_w

    w_i = \frac{1 / i}{\sum_{k=1}^{n} 1 / k}

* :class:`RE` (Rank Exponent) [#rocref2]_:

.. math::
    :label: re_w

    w_i = \frac{(n - i + 1)^z}{\sum_{k=1}^{n} (n - k + 1)^z}

The exponent :math:`z \geq 0` is given directly (parameter ``z``) or found numerically from the weight of the most
important criterion judged by the decision maker (parameter ``w_top``). :math:`z = 0` gives equal weights and
:math:`z = 1` gives rank sum weights.

.. [#rocref1] Barron, F. H., & Barrett, B. E. (1996). Decision quality using ranked attribute weights. Management
   Science, 42(11), 1515-1523.

.. [#rocref2] Stillwell, W. G., Seaver, D. A., & Edwards, W. (1981). A comparison of weight approximation techniques
   in multiattribute utility decision making. Organizational Behavior and Human Performance, 28(1), 62-77.
