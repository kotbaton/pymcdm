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

    \begin{equation}
    A w = \lambda_{\max} w, \qquad \sum_{i=1}^{n} w_i = 1
    \end{equation}

With ``prioritization='geometric_mean'``, the weights are derived with the Logarithmic Least Squares Method (LLSM), i.e.
as the normalized geometric mean of each row in the pairwise comparison matrix:

.. math::
    :label: ahp_priority_vector_llsm

    \begin{equation}
    w_i = \frac{\prod_{j=1}^{n} \left(a_{ij}\right)^{\frac{1}{n}}}{\sum_{k=1}^{n} \prod_{j=1}^{n} \left(a_{kj}\right)^{\frac{1}{n}}}
    \end{equation}

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

    \begin{equation}
        \alpha_{ij} = \left\{ \begin{array}{lccr}
            IF & f \left( C_i\right)   <  f \left( C_j\right) & THEN & 1  \\
            IF & f \left( C_i\right) =  f \left( C_j\right) & THEN & 0.5 \\
            IF & f \left( C_i\right)  >   f \left( C_j\right) & THEN & 0  \\
        \end{array}
        \right.
    \end{equation}

where :math:`f \left(C\right)` is a position in ranking for criterion :math:`C` (lower value is better).

**Step 3.** Calculate the Summed Criteria Weights.

Based on the obtained :math:`MAC`, the horizontal vector of the Summed Criteria Weights (:math:`SCW`) is obtained as
follows:

.. math::
    \begin{equation}
    SCW_i=\sum^{n}_{j=1}\alpha_{ij}
    \end{equation}


**Step 4.** Calculate the final criteria weights.

Finally, values of preference are approximated for each criterion. As a result, the horizontal vector :math:`W` is obtained,
where the :math:`i-th` row contains the approximate preference value for :math:`C_i`. The weights for the set of
criteria are obtained as:

.. math::
    \begin{equation}
        w_{i} = \frac{SCW_{i}}{\sum^{n}_{i=1} SCW_{i}}
    \end{equation}

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

    \begin{equation}
    k_j = \begin{cases} 1 & j = 1 \\ s_j + 1 & j > 1 \end{cases}
    \end{equation}

**Step 4.** Calculate the recalculated weights.

.. math::
    :label: swara_q

    \begin{equation}
    q_j = \begin{cases} 1 & j = 1 \\ \frac{q_{j-1}}{k_j} & j > 1 \end{cases}
    \end{equation}

**Step 5.** Calculate the final criteria weights.

.. math::
    :label: swara_w

    \begin{equation}
    w_j = \frac{q_j}{\sum_{k=1}^{n} q_k}
    \end{equation}

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

    \begin{equation}
    \varphi_{k/(k+1)} = \frac{v_{k+1}}{v_k}
    \end{equation}

**Step 3.** Calculate the weights.

The weights should satisfy :math:`w_k / w_{k+1} = \varphi_{k/(k+1)}` and the condition of mathematical transitivity
:math:`w_k / w_{k+2} = \varphi_{k/(k+1)} \cdot \varphi_{(k+1)/(k+2)}`. The weights closest to these conditions are
obtained from the model:

.. math::
    :label: fucom_model

    \begin{equation}
    \begin{aligned}
    \min \ & \chi \\
    \text{s.t.} \ & \left| \frac{w_k}{w_{k+1}} - \varphi_{k/(k+1)} \right| \leq \chi, \quad \forall k \\
    & \left| \frac{w_k}{w_{k+2}} - \varphi_{k/(k+1)} \cdot \varphi_{(k+1)/(k+2)} \right| \leq \chi, \quad \forall k \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}
    \end{equation}

The optimal value :math:`\chi` is the Deviation from Full Consistency (attribute ``dfc``). The value 0 means full
consistency of the comparisons.

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

    \begin{equation}
    A_B = \left( a_{B1}, a_{B2}, \ldots, a_{Bn} \right)
    \end{equation}

**Step 4.** Determine the preference of all the criteria over the worst criterion.

This gives the Others-to-Worst vector (parameter ``a_w``), where :math:`a_{WW} = 1`:

.. math::
    :label: bwm_aw

    \begin{equation}
    A_W = \left( a_{1W}, a_{2W}, \ldots, a_{nW} \right)
    \end{equation}

**Step 5.** Calculate the weights.

The weights minimize the maximum absolute difference between the weight ratios and the comparisons:

.. math::
    :label: bwm_model

    \begin{equation}
    \begin{aligned}
    \min \ & \xi \\
    \text{s.t.} \ & \left| \frac{w_B}{w_j} - a_{Bj} \right| \leq \xi, \quad \forall j \\
    & \left| \frac{w_j}{w_W} - a_{jW} \right| \leq \xi, \quad \forall j \\
    & \sum_{j=1}^{n} w_j = 1, \quad w_j \geq 0, \quad \forall j
    \end{aligned}
    \end{equation}

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
