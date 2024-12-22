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

The weights vector (:math:`w`) is derived as the geometric mean of each row in the pairwise comparison matrix:

.. math::
    :label: ahp_priority_vector

    \begin{equation}
    w_i = \frac{\prod_{j=1}^{n} \left(a_{ij}\right)^{\frac{1}{n}}}{\sum_{k=1}^{n} \prod_{j=1}^{n} \left(a_{kj}\right)^{\frac{1}{n}}}
    \end{equation}


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
