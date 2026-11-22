.. _american_school:

===============
American school
===============



ARAS
=======================

``ARAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat1`).

.. math::
    :label: equ:mat1

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Definition of a extended decision matrix, where decision matrix :math:`X` is extended with
optimal value :math:`x_0` (:eq:`equ:emat1`). Optimal solution can be defined as the optimal (expected) values for
each of the criteria. If it is not defined maximum value will be chosen for profit criteria and minimum value for the
cost criteria.

.. math::
    :label: equ:emat1

    X^{\prime} = [x_{i j}]=\left[\begin{array}{llll}
    x_{01} & x_{02} & \ldots & x_{0 m} \\
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 3.** Normalization the extended decision matrix, where for profit criteria use the equation (:eq:`equ:profita`),
and for cost, criteria use the equation (:eq:`equ:costa`). In ``pymcdm``, the Sum normalization method is used as the
default normalization in the ARAS method. Optimal solution is normalized as other values.

.. math::
    :label: equ:profita

        r_{ij} = \frac{x_{ij}}{\sum_m^{i=0}x_{ij}}

.. math::
    :label: equ:costa

        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=0}\frac{1}{x_{ij}}}

**Step 4.** Building a weighted normalized extended decision matrix :math:`v_{ij}` based on the normalized extended
decision matrix and criteria weights :math:`w_{j}` using Equation (:eq:`weighted`).

.. math::
    :label: weighted

        v_{ij} = w_{j}r_{ij} \label{weighted}

**Step 5.** Determining values of optimality function :math:`S_i` using the Equation (:eq:`opf`).
Note, that value :math:`S_i` is also calculated for optimal solution.

.. math::
    :label: opf

        S_i = \sum_{j=1}^{n} v_{ij}

**Step 6.** Calculate the utility degree :math:`K_i` based on Equation (:eq:`ud`). ``pymcdm`` calculates
this value for the optimal solution but it is not showed in the verbose results.

.. math::
    :label: ud

        K_i = \frac{S_i}{S_0}

where :math:`S_i` and :math:`S_0` are the optimality criterion values. Better alternatives are represented
with larger values of the utility degree :math:`K_i`.

AROMAN
======

*Bošković et al. (2023)* propose the *Alternative Ranking Order Method Accounting for
Two-Step Normalization* (AROMAN) as a novel multi-criteria decision-making (MCDM) method.
The core contribution of AROMAN lies in coupling two normalization techniques
(linear and vector normalization) and aggregating them into an averaged normalized
decision-making matrix, followed by an original final ranking formula that explicitly
accounts for both minimization and maximization criteria.

Assume a set of :math:`m` alternatives :math:`A_i \ (i=1,\dots,m)` evaluated with respect
to :math:`n` criteria :math:`C_j \ (j=1,\dots,n)`, with criteria weights
:math:`w_j` such that :math:`\sum_{j=1}^{n} w_j = 1`. Criteria may be of *benefit*
(maximization) or *cost* (minimization) type.

Steps of the AROMAN Method
--------------------------

**Step 1: Construct the initial decision matrix**

The decision problem is represented by the matrix:

.. math::

   X = [x_{ij}], \quad i = 1,\dots,m,\; j = 1,\dots,n

where :math:`x_{ij}` denotes the performance of alternative :math:`A_i` with respect to
criterion :math:`C_j`.

**Step 2: Normalize the input data**

Two normalization techniques are applied.

**Step 2.1: Linear normalization**

.. math::

   t_{ij} =
   \frac{x_{ij} - x_{ij}^{\min}}
        {x_{ij}^{\max} - x_{ij}^{\min}},
   \quad i = 1,2,\dots,m;\; j = 1,2,\dots,n

**Step 2.2: Vector normalization**

.. math::

   t_{ij}^{*} =
   \frac{x_{ij}}
        {\sqrt{\sum_{i=1}^{m} x_{ij}^{2}}},
   \quad i = 1,2,\dots,m;\; j = 1,2,\dots,n

Both normalization techniques are applied regardless of whether the criteria are of
*min* or *max* type.

**Step 2.3: Aggregated averaged normalization**

The two normalized matrices are aggregated using the arithmetic mean:

.. math::

   t_{ij}^{\text{norm}} =
   \frac{\beta t_{ij} + (1-\beta) t_{ij}^{*}}{2},
   \quad i = 1,2,\dots,m;\; j = 1,2,\dots,n

where :math:`\beta \in [0,1]` is a trade-off parameter. In the original study,
:math:`\beta = 0.5`.

**Step 3: Construct the weighted normalized decision-making matrix**

The aggregated averaged normalized matrix is multiplied by the criteria weights
:math:`W_j`:

.. math::

   \hat{t}_{ij} = W_j \cdot t_{ij}^{\text{norm}},
   \quad i = 1,2,\dots,m;\; j = 1,2,\dots,n

**Step 4: Separate aggregation of min and max criteria**

For each alternative :math:`i`, the normalized weighted values are summed separately
for criteria of *min* and *max* type:

- Sum of all minimization criteria:

.. math::

   L_i =
   \sum_{j=1}^{n} \hat{t}_{ij}^{(\min)},
   \quad i = 1,2,\dots,m

- Sum of all maximization criteria:

.. math::

   A_i =
   \sum_{j=1}^{n} \hat{t}_{ij}^{(\max)},
   \quad i = 1,2,\dots,m

**Step 5: Final ranking of alternatives**

The final ranking value :math:`R_i` for each alternative is calculated as:

.. math::

   R_i = L_i^{\lambda} + A_i^{(1-\lambda)},
   \quad i = 1,2,\dots,m

where :math:`\lambda` is the coefficient representing the proportion of minimization
criteria. When both criterion types are present in equal importance,
:math:`\lambda = 0.5`.

Alternatives are ranked in descending order of :math:`R_i`. A higher value of
:math:`R_i` indicates a more preferable alternative.

**Reference**

Bošković, S., Švadlenka, L., Jovčić, S., Dobrodolac, M., Simić, V., & Bacanin, N. (2023).
*An alternative ranking order method accounting for two-step normalization (AROMAN)—A
case study of the electric vehicle selection problem*. IEEE Access, 11, 39496–39507.


COCOSO
=======================

``COCOSO`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_cocoso`).

.. math::
    :label: equ:mat_cocoso

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profit`), and for
cost, criteria use the equation (:eq:`equ:cost`). In the ``pymcdm``, The Minimum-Maximum normalization method is used
as default normalization method.

.. math::
    :label: equ:profit

        r_{ij} = \frac{x_{ij} - \min_{i}{x_{ij}}}{\max_{i}{x_{ij}} - \min_{i}{x_{ij}}}


.. math::
    :label: equ:cost

        r_{ij} = \frac{\max_{i}{x_{ij}} - x_{ij}}{\max_{i}{x_{ij}} - \min_{i}{x_{ij}}}



**Step 3.** Calculation of the weighted sum of the comparison sequence and the total power weight of the comparison
sequences for each alternative. The values of :math:`S_i` are based on the grey relationship generation method
(:eq:`equ:SI`), and for :math:`P_i` the values are achieved according to the multiplicative WASPAS setting
(:eq:`equ:PI`).


.. math::
    :label: equ:SI

        S_i = \sum_{j=1}^{n} (w_j r_{ij})

.. math::
    :label: equ:PI

        P_i = \sum_{j=1}^{n} (r_{ij})^{w_j}


**Step 4.** Computation of the relative weights of alternatives using aggregation strategies. The formulas determine the
strategies (:eq:`equ:s1`)-(:eq:`equ:s3`), where the first strategy expresses the average of the sums of WSM and WPM s
cores (:eq:`equ:s1`), the second strategy expresses the sum of WSM and WPM scores over the best (:eq:`equ:s2`), and the
third strategy expresses the compromise strategy of WSM and WPM by using the :math:`\lambda` value (:eq:`equ:s3`).
Be default, ``pymcdm`` uses a :math:`\lambda` value of 0.5.

.. math::
    :label: equ:s1

    k_{i a}=\frac{P_{i}+S_{i}}{\sum_{i=1}^{m}\left(P_{i}+S_{i}\right)}

.. math::
    :label: equ:s2

    k_{i b}=\frac{S_{i}}{\min _{i} S_{i}}+\frac{P_{i}}{\min _{i} P_{i}}

.. math::
    :label: equ:s3

    k_{i c}=\frac{\lambda\left(S_{i}\right)+(1-\lambda)\left(P_{i}\right)}{\left(\lambda \max _{i} S_{i}+(1-\lambda) \max _{i} P_{i}\right)} ; \quad 0 \leqslant \lambda \leqslant 1

**Step 5.** Establish the final ranking of alternatives based on :math:`k_i` values defined using the formula
(:eq:`equ:ki`). The higher the :math:`k_i` value, the higher the position of the alternative in the ranking.

.. math::
    :label: equ:ki

    k_{i}=\left(k_{i a} k_{i b} k_{i c}\right)^{\frac{1}{3}}+\frac{1}{3}\left(k_{i a}+k_{i b}+k_{i c}\right)

CODAS
=======================

``CODAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat2`).

.. math::
    :label: equ:mat2

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profitc`), and for
cost, criteria use the equation (:eq:`equ:costc`). This normalization method (Linear normalization) is used as
a default normalization method in ``pymcdm``.

.. math::
    :label: equ:profitc

        r_{ij} = \frac{x_{ij}}{\max_i x_{ij}}

.. math::
    :label: equ:costc

        r_{ij} = \frac{\min_i x_{ij}}{x_{ij}}

**Step 3.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weightedc`).

.. math::
    :label: weightedc

        v_{ij} = w_{j}r_{ij} \label{weightedc}

**Step 4.** Determine the negative-ideal solution (point) based on Equation (:eq:`nip`).

.. math::
    :label: nip

        ns_j = \min_i {v_ij}

**Step 5.** Calculate the Euclideana :math:`E_i` and Taxicab :math:`T_i` distances of alternatives
from the negative-ideal solution, shown as follows:

.. math::

        E_i = \sqrt{\sum_{i=1}^m \left ( v_{ij} - ns_j \right)^2}


.. math::

        T_i = \sum_{j=1}^m \left | v_{ij} - ns_j \right |


**Step 6.** Construct the relative assessment matrix, shown as follows:

.. math::

        h_{i k}=\left(E_{i}-E_{k}\right)+\left(\psi\left(E_{i}-E_{k}\right) \times\left(T_{i}-T_{k}\right)\right)


where :math:`k \in \left \{ 1,2,\cdots,n \right \}` and :math:`\psi` denotes a threshold function to recognize the
equality of the Euclidean distances of two alternatives, and is defined as follows:

.. math::

        \psi(x)=\left\{\begin{array}{lll}
        1 & \text { if } & |x| \geq \tau \\
        0 & \text { if } & |x|<\tau
        \end{array}\right.


In this function, :math:`\tau` is the threshold parameter that can be set by decision maker. It is suggested to set this
parameter at a value between 0.01 and 0.05. Default value in the ``pymcdm`` is :math:`\tau = 0.02`.

**Step 7.** Calculate the assessment score of each alternative, shown as follows:

.. math::

    \mathrm{H}_{i}=\sum_{k=1}^{n} h_{i k}


**Step 8.** Rank the alternatives according to the decreasing values of assessment (larger value of assessment score
means better alternative).

COPRAS
=======================

``COPRAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_copras`).

.. math::
    :label: equ:mat_copras

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Calculate normalized decision matrix values :math:`r_{i j}`
using equation (:eq:`eq:copras_sum`).

.. math::
    :label: eq:copras_sum

        r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{m} x_{i j}}



**Step 3.** Calculate weighted normalized decision matrix, which represents multiplication of the normalized decision
matrix elements with the appropriate weight coefficients using equation (:eq:`eq:copras_e`).

.. math::
    :label: eq:copras_e

        v_{ij} = r_{ij} \cdot w_j


**Step 4.** Determine the sums of weighted normalized values which was calculated previously. Equation
(:eq:`eq:copras_splus`) should be used for profit criteria and equation (:eq:`eq:copras_sminus`) for cost criteria.
It is assumed, that criteria ordered in the way that first :math:`k` criteria are profit
and other are cost. However, in ``pymcdm`` criteria can be in other order, because their types are determined
based on the ``types`` list in arguments.

.. math::
    :label: eq:copras_splus

        S_{+i}=\sum_{j=1}^{k} v_{i j}

.. math::
    :label: eq:copras_sminus

        S_{-i}=\sum_{j=k+1}^{n} v_{i j}

where :math:`k` is the number of attributes that must be maximized. The rest of attributes from :math:`k+1` to n prefer
lower values. The :math:`S_{+i}` and :math:`S_{-i}` values show level of the goal achievement for alternatives. Higher
value of :math:`S_{+i}` means that this alternative is better and the lower value of :math:`S_{-i}` also points to
better alternative.

**Step 4.** Calculate the relative significance of alternatives using equation (:eq:`eq:copras_q`).

.. math::
    :label: eq:copras_q

        \label{eq:copras_q}
        Q_{i}=S_{+i}+\frac{S_{-\min } \cdot \sum_{i=1}^{m} S_{-i}}{S_{-i} \cdot \sum_{i=1}^{m}\left(\frac{S_{-\min }}{S_{-i}}\right)}

**Step 5.** Final ranking is performed according :math:`U_i` values (:eq:`eq:copras_u`).

.. math::
    :label: eq:copras_u

        U_i = \frac{Q_i}{Q^{max}_i} \cdot 100\%

Where :math:`Q^{max}_i` stands for maximum value of the utility function. Better alternatives has higher :math:`U_i`
value.

CRADIS
=======================

``CRADIS`` (Compromise Ranking of Alternatives from Distance to Ideal Solution) combines steps of the ARAS, MARCOS and
TOPSIS methods [#cradisref1]_. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`X = [x_{ij}]` of dimension :math:`n \times m`.

**Step 2.** Normalize the decision matrix:

.. math::
        n_{ij} = \begin{cases} \dfrac{x_{ij}}{\max_i x_{ij}} & \text{for benefit criteria} \\[2ex]
        \dfrac{\min_i x_{ij}}{x_{ij}} & \text{for cost criteria} \end{cases}
    :label: cradis_norm

**Step 3.** Calculate the weighted normalized ("aggravated") decision matrix :math:`v_{ij} = w_j n_{ij}`.

**Step 4.** Determine the ideal solution :math:`t` and the anti-ideal solution :math:`t_a` as the largest and the
smallest element of the whole weighted normalized matrix (not of every criterion):

.. math::
        t = \max_{i, j} v_{ij}, \qquad t_a = \min_{i, j} v_{ij}
    :label: cradis_ideal

**Step 5.** Calculate the total deviations of every alternative from the ideal and the anti-ideal solution:

.. math::
        s_i^{+} = \sum_{j=1}^{m} (t - v_{ij}), \qquad s_i^{-} = \sum_{j=1}^{m} (v_{ij} - t_a)
    :label: cradis_dev

**Step 6.** Calculate the same deviations :math:`s_0^{+}` and :math:`s_0^{-}` for the optimal alternative, which has
the largest value :math:`\max_i v_{ij}` of every criterion, and the utility functions:

.. math::
        K_i^{+} = \frac{s_0^{+}}{s_i^{+}}, \qquad K_i^{-} = \frac{s_i^{-}}{s_0^{-}}
    :label: cradis_k

**Step 7.** Calculate the final score as the average of the utility functions:

.. math::
        Q_i = \frac{K_i^{+} + K_i^{-}}{2}
    :label: cradis_q

The alternative with the highest value of :math:`Q_i` is the best.

.. [#cradisref1] Puška, A., Stević, Ž., & Pamučar, D. (2022). Evaluation and selection of healthcare waste
   incinerators using extended sustainability criteria and multi-criteria analysis methods. Environment, Development
   and Sustainability, 24(9), 11195-11225.

DARP
=======================

``DARP`` (Distances to Aspiration Reference Points) measures the distance of every alternative from an aspiration
reference point [#darpref1]_. The reference point can be common for all alternatives (the best performance of the
alternatives, or external targets) or individual for each of them (e.g. national targets of countries), parameter
``reference``. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`X = [x_{ij}]`, the weights and the aspiration reference points
:math:`RP_i = [x_{i1}^{+}, \ldots, x_{im}^{+}]`.

**Step 2.** Determine the worst performance :math:`x_j^{-}` of every criterion (the minimum for benefit and the
maximum for cost criteria).

**Step 3.** Normalize the decision matrix between the worst performance and the aspiration level:

.. math::
        \bar{x}_{ij} = \begin{cases} \dfrac{x_{ij} - x_j^{-}}{x_{ij}^{+} - x_j^{-}} &
        \text{if } 0 \leq \dfrac{x_{ij} - x_j^{-}}{x_{ij}^{+} - x_j^{-}} < 1 \\[2ex] 1 & \text{otherwise} \end{cases}
    :label: darp_norm

The value 1 means that the aspiration level is reached, so a surplus on one criterion does not compensate
shortages on the others.

**Step 4.** Calculate the distance of the weighted normalized alternative from the weighted reference point
:math:`[w_1, \ldots, w_m]`:

.. math::
        d_{i0} = \sqrt{\sum_{j=1}^{m} \left(w_j \bar{x}_{ij} - w_j\right)^2}
    :label: darp_d

**Step 5.** Calculate the measure, which lies in :math:`[0, 1]`:

.. math::
        DARP_i = 1 - \frac{d_{i0}}{\sqrt{\sum_{j=1}^{m} w_j^2}}
    :label: darp_measure

The alternative with the highest value is the best; it is equal to 1 if all aspiration levels are reached.

.. [#darpref1] Roszkowska, E., Filipowicz-Chomko, M., & Wachowicz, T. (2020). Using individual and common reference
   points to measure the performance of alternatives in multiple criteria evaluation. Operations Research and
   Decisions, 30(3), 77-96.

EDAS
=======================

``EDAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_edas`).

.. math::
    :label: equ:mat_edas

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Calculate the average solution for each criterion according to the formula (:eq:`equ:av`).

.. math::
    :label: equ:av

    A V_{j}=\frac{\sum_{i=1}^{n} x_{i j}}{n}

**Step 3.** Calculating the positive distance from the mean solution and the negative distance from the mean solution
for the alternatives. When the criterion is of profit type, the negative distance and the positive distance are
calculated using equations (:eq:`equ:ndapr`) and (:eq:`equ:pdapr`), while when the criterion is of cost type, the
distances are calculated using formulas (:eq:`equ:ndacs`) and (:eq:`equ:pdacs`).

.. math::
    :label: equ:pdapr

    PDA_{i j} = \frac{\max \left(0,\left(X_{i j}-A V_{j}\right)\right)}{A V_{j}}

.. math::
    :label: equ:ndapr

    NDA_{i j}=\frac{\max \left(0,\left(A V_{j}-X_{i j}\right)\right)}{A V_{j}}

.. math::
    :label: equ:pdacs

    P D A_{i j}=\frac{\max \left(0,\left(A V_{j}-X_{i j}\right)\right)}{A V_{j}}

.. math::
    :label: equ:ndacs

    N D A_{i j}=\frac{\max \left(0,\left(X_{i j}-A V_{j}\right)\right)}{A V_{j}}

**Step 4.** Calculate the weighted sums of :math:`PDA` and :math:`NDA` for each decision variant using equations
(:eq:`equ:wsp`) and (:eq:`equ:wsn`).

.. math::
    :label: equ:wsp

    SP_{i}=\sum_{j=1}^{m} w_{j} P D A_{i j}

.. math::
    :label: equ:wsn

    SN_{i}=\sum_{j=1}^{m} w_{j} N D A_{i j}


**Step 5.** Normalize the weighted sums of negative and positive distances using equations (:eq:`equ:normsp`) and
(:eq:`equ:normsn`).

.. math::
    :label: equ:normsp

    N S P_{i}=\frac{S P_{i}}{\max _{i}\left(S P_{i}\right)}

.. math::
    :label: equ:normsn

    N S N_{i}=1-\frac{S N_{i}}{\max _{i}\left(S N_{i}\right)}


**Step 6.** Calculate the evaluation score (:math:`AS`) for each alternative using the formula (:eq:`equ:as`). A higher
point value determines a higher ranking alternative.

.. math::
    :label: equ:as

    A S_{i}=\frac{1}{2}\left(N S P_{i}+N S N_{i}\right)


ERVD
=======================
``ERVD`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_ervd`).

.. math::
    :label: equ:mat_ervd

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Define reference points :math:`\mu_j` for :math:`j=1,\ldots,n` for each decision criterion
Decision makers must decide which outcomes they consider equivalent for criterion :math:`j`, set
the reference point :math:`\mu_j` and then consider lesser outcomes as losses and greater ones as gains.

**Step 3.** Normalize the decision matrix using the sum method (:eq:`equ:ervd_sum`).

.. math::
    :label: equ:ervd_sum

        r_{ij} = \frac{x_{ij}}{\sum^m_{i=1} x_{ij}}

**Step 4.** Normalize the reference point with similar to the data in the matrix:

.. math::

        \varphi_{j} = \frac{\mu_{j}}{\sum^m_{i=1} x_{ij}}

**Step 5.** Calculate the value of alternative :math:`A_i` according to criterion :math:`C_j` by increasing value function
(for benefit criteria):

.. math::

    v_{i j}=\left\{\begin{array}{l}
    \left(r_{i j}-\varphi_j\right)^\alpha \quad \text { if } r_{i j}>\varphi_j \\
    -\lambda\left(\varphi_j-r_{i j}\right)^\alpha \text { otherwise }
    \end{array}\right.

and decreasing value function (for cost criteria):

.. math::

    v_{i j}=\left\{\begin{array}{l}
    \left(\varphi_j-r_{i j}\right)^\alpha \quad \text { if } r_{i j}<\varphi_j \\
    -\lambda\left(r_{i j}-\varphi_j\right)^\alpha \text { otherwise }
    \end{array}\right.

**Step 6.** Determine the ideal and negative ideal solutions :math:`A^+` (PIS) and :math:`A^-` (NIS), respectively:

.. math::

    A^{+}=\left\{v_1^{+}, \cdots v_n^{+}\right\}, A^{-}=\left\{v_1^{-}, \cdots v_n^{-}\right\}

where :math:`v_j^{+}=\max _i v_{i j}` and :math:`v_j^{-}=\min v_{i \vec{j}}`.

**Step 7.** Calculate the separation measures from PIS and NIS individually with help Minkowski metric:

.. math::

    S_i^{+}=\sum_{j=1}^n w_j \cdot\left|v_{i j}-v_j^{+}\right|, \text {for alternative } i, i=1 \ldots m

.. math::

    S_i^{-}=\sum_{j=1}^n w_j \cdot\left|v_{i j}-v_j^{-}\right|, \text {for alternative } i, i=1 \ldots m

**Step 8.** Calculate the relative closeness of each alternative to the ideal solution:

.. math::

    \phi_i=\frac{S_i^{-}}{S_i^{+}+S_i^{-}}, i=1, \ldots, m

Higher values of :math:`\phi_i` points to better alternatives.

LoPM
====

The Limits on Property method is a technique for selecting materials or making decisions based on setting boundaries
for desired characteristics. This method was described by Mahmoud Farag in his book.
It categorizes performance requirements into three groups:

* Lower-limit properties: These are the minimum acceptable values for a particular property.
  For instance, in selecting a material for a bridge, there would be a lower limit
  for strength to ensure the bridge can support its load.
* Upper-limit properties: These are the maximum acceptable values for a property.
  An example might be an upper limit on the weight of an aircraft wing material to optimize fuel efficiency.
* Target value properties: These are the ideal values for a property, where achieving them is most desirable.
  Compatibility between materials might require a specific target value
  for thermal expansion coefficient to minimize thermal stress.

The choice of whether a property is designated as a lower limit, upper limit, or target value depends on
the specific application. For example, In an electrical cable, conductivity would be a lower limit for the core
material to ensure proper current flow, while it would be an upper limit for the insulation layer to prevent leakage.
This method is particularly useful when dealing with a large number of potential alternatives because it allows for
efficient screening. By setting these limits, we can eliminate unsuitable alternatives from the set.

Once the initial screening is complete, the Limits on Property Method employs a merit value :math:`m` to further
refine the selection process. Merit value is calculated using the following formula:

.. math::

    m = \left( \sum_{i=1}^{n_l} w_i \frac{Y_i}{X_i} \right)
    + \left( \sum_{i=n_l + 1}^{n_l + n_u} w_i \frac{X_i}{Y_i} \right)
    + \left( \sum_{i=n_l + n_u + 1}^{N} w_i \left| \frac{X_i}{Y_i} - 1 \right| \right)

where :math:`n_l, n_u, n_t` denote the number of lower-limit, upper-limit, and target value properties, respectively,
while :math:`N` represents total number of the criteria. Next, :math:`w_i` represent the criteria weights and :math:`X_i`
represents the alternative value properties, while :math:`Y_i` represents the specified limits (lower, upper or target)
respectively. Notice, that this formula assumes, that criteria are sorted and grouped
in the following order: lower, upper, target.

A lower merit value :math:`m` indicates a better alternative according to the defined limits and weightings.
Alternatives with properties exceeding the upper limits or falling short of the lower limits will receive
significant penalties in the calculation, driving their merit value up. In other words, lower values of :math:`m`
suggest better alternatives.
By comparing the merit values of the remaining alternatives after screening, we can identify the most
suitable option for the specific application.

GRA
=======================

``GRA`` (Grey Relational Analysis) evaluates the similarity of every alternative to the reference sequence of ideal
values [#graref1]_. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`Y = [y_{ij}]` of dimension :math:`m \times n`.

**Step 2.** Grey relational generating: translate the performance values into comparability sequences
:math:`x_{ij} \in [0, 1]`. For the larger-the-better and the smaller-the-better criteria:

.. math::
        x_{ij} = \frac{y_{ij} - \min_i y_{ij}}{\max_i y_{ij} - \min_i y_{ij}}, \qquad
        x_{ij} = \frac{\max_i y_{ij} - y_{ij}}{\max_i y_{ij} - \min_i y_{ij}}
    :label: gra_gen

For the closer-to-the-desired-value-the-better criteria with a desired value :math:`y_j^*` (parameter ``targets``):

.. math::
        x_{ij} = 1 - \frac{|y_{ij} - y_j^*|}{\max(\max_i y_{ij} - y_j^*, \; y_j^* - \min_i y_{ij})}
    :label: gra_target

**Step 3.** Calculate the grey relational coefficients with respect to the reference sequence :math:`x_{0j} = 1`,
where :math:`\Delta_{ij} = |x_{0j} - x_{ij}|`, :math:`\Delta_{\min}` and :math:`\Delta_{\max}` are the smallest and
the largest :math:`\Delta_{ij}` of the whole matrix, and :math:`\zeta \in (0, 1]` is the distinguishing coefficient
(parameter ``zeta``, 0.5 by default):

.. math::
        \gamma(x_{0j}, x_{ij}) = \frac{\Delta_{\min} + \zeta \Delta_{\max}}{\Delta_{ij} + \zeta \Delta_{\max}}
    :label: gra_coef

**Step 4.** Calculate the grey relational grade:

.. math::
        \Gamma(X_0, X_i) = \sum_{j=1}^{n} w_j \gamma(x_{0j}, x_{ij})
    :label: gra_grade

The alternative with the highest grade is the best.

.. [#graref1] Kuo, Y., Yang, T., & Huang, G. W. (2008). The use of grey relational analysis in solving multiple
   attribute decision-making problems. Computers & Industrial Engineering, 55(1), 80-93.

Hellwig's method
=======================

``HELLWIG`` (taxonomic measure of development) [#hellwigref1]_ ranks the alternatives by their distance from the
pattern of development, built from the best value of every criterion. The method evaluates decision alternatives
according to the following steps:

**Step 1.** Definition of a decision matrix :math:`X = [x_{ij}]` of dimension :math:`m \times n` and of the weights.

**Step 2.** Normalize the decision matrix. The original method uses the standardization (default):

.. math::
        z_{ij} = \frac{x_{ij} - \bar{x}_j}{S_j}, \qquad
        S_j = \sqrt{\frac{1}{m} \sum_{i=1}^{m} (x_{ij} - \bar{x}_j)^2}
    :label: hellwig_std

Other normalizations, e.g. the vector, max-min or sum normalization, can be used with the parameter
``normalization_function``; they are applied to all criteria in the same way.

**Step 3.** Calculate the weighted normalized matrix :math:`\tilde{x}_{ij} = w_j z_{ij}` and the pattern of
development :math:`\tilde{x}_j^{+}`, the largest value for benefit and the smallest value for cost criteria.

**Step 4.** Calculate the Euclidean distances of the alternatives from the pattern:

.. math::
        d_i = \sqrt{\sum_{j=1}^{n} \left(\tilde{x}_{ij} - \tilde{x}_j^{+}\right)^2}
    :label: hellwig_d

**Step 5.** Calculate the critical distance and Hellwig's measure:

.. math::
        d_0 = \bar{d} + 2 S_d, \qquad H_i = 1 - \frac{d_i}{d_0}
    :label: hellwig_h

where :math:`\bar{d}` and :math:`S_d` are the mean and the (population) standard deviation of the distances. The
alternative with the highest value of :math:`H_i` is the best.

With ``distance='mahalanobis'`` [#hellwigref2]_ the distance from the pattern takes into account the correlations
between criteria:

.. math::
        d_i = \sqrt{(A_i - I) W C^{-1} W^T (A_i - I)^T}
    :label: hellwig_mahalanobis

where :math:`C` is the sample covariance matrix of the decision matrix and :math:`W = diag(\sqrt{w_1}, \ldots,
\sqrt{w_n})`. This variant is computed on the decision matrix (the ``normalization_function`` is not used); by Property 2 of
[#hellwigref2]_ its result is the same for the linear normalizations considered there. It requires more alternatives
than criteria. Note that the two variants weight the criteria differently:
the Euclidean distance of :math:`\tilde{x}_{ij} = w_j z_{ij}` weights the squared differences by :math:`w_j^2`, the
Mahalanobis distance with :math:`W` by :math:`w_j`.

.. [#hellwigref1] Hellwig, Z. (1968). Zastosowanie metody taksonomicznej do typologicznego podziału krajów ze
   względu na poziom ich rozwoju oraz zasoby i strukturę wykwalifikowanych kadr. Przegląd Statystyczny, 4, 307-326.

.. [#hellwigref2] Roszkowska, E. (2024). Modifying Hellwig's method for multi-criteria decision-making with
   Mahalanobis distance for addressing asymmetrical relationships. Symmetry, 16(1), 77.

MIDIA
=======================

``MIDIA`` (Multi-criteria method Integrating Distances to Ideal and Anti-ideal points) [#midiaref1]_ extends
Hellwig's method with the distance to the anti-ideal solution. After Steps 1-3 of Hellwig's method, which give the
weighted normalized ideal :math:`\tilde{x}_j^{+}` and anti-ideal :math:`\tilde{x}_j^{-}` solutions, the Euclidean
distances :math:`dI_i` and :math:`dAI_i` of the alternatives from them and the distance :math:`d^{+-}` between them
are calculated. The closeness to the ideal and to the anti-ideal solution are aggregated with the coefficient
:math:`\alpha \in [0, 1]` (parameter ``alpha``):

.. math::
        DI_i = 1 - \frac{dI_i}{d^{+-}}, \qquad DAI_i = \frac{dAI_i}{d^{+-}}, \qquad
        D(\alpha)_i = \alpha DI_i + (1 - \alpha) DAI_i
    :label: midia

:math:`\alpha = 1` gives the pure aggressive (ideal-based) and :math:`\alpha = 0` the pure conservative
(anti-ideal-based) strategy. The alternative with the highest value of :math:`D(\alpha)_i` is the best.

.. [#midiaref1] Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances to
   ideal and anti-ideal points. Symmetry, 16(8), 1025.

MABAC
=======================
``MABAC`` is designed to evaluate decision alternatives according to the following steps:


**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat4`).

.. math::
    :label: equ:mat4

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Normalization of the decision matrix, where for criteria of type profit use equation (:eq:`equ:profitma`)
and for criteria of type cost use equation (:eq:`equ:costma`).

.. math::
    :label: equ:profitma

    n_{i j}=\frac{x_{i j}- \min x_{i}}{\max x_{i}- \min x_{i}}

.. math::
    :label: equ:costma

    n_{i j}=\frac{x_{i j}- \max x_{i}}{\min x_{i} - \max x_{i}}

**Step 3.** Create a weighted matrix based on the values from the normalized matrix according to the formula
(:eq:`equ:wema_mabac`).

.. math::
    :label: equ:wema_mabac

    v_{i j}=w_{i} \cdot\left(n_{i j}+1\right)


**Step 4.** Boundary approximation area (:math:`G`) matrix determination. The Boundary Approximation Area (:math:`BAA`)
for all criteria can be determined using the formula (:eq:`equ:boundma`).

.. math::
    :label: equ:boundma

    g_{j}=\left(\prod_{j=1}^{m} v_{i j}\right)^{1 / m}


**Step 5.** Distance calculation of alternatives from the boundary approximation area for matrix elements (:math:`Q`) by
equation (:math:`equ:qma`).

.. math::
    :label: equ:qma

    Q = [q_{i j}]=\left[\begin{array}{cccc}
    v_{11}-g_{1} & v_{12}-g_{2} & \ldots & v_{1 n}-g_{n} \\
    v_{21}-g_{1} & v_{22}-g_{2} & \ldots & v_{2 n}-g_{n} \\
    \ldots & \ldots & \ldots & \ldots \\
    v_{m 1}-g_{1} & v_{m 2}-g_{2} & \ldots & v_{m n}-g_{n}
    \end{array}\right]=\left[\begin{array}{cccc}
    q_{11} & q_{12} & \ldots & q_{1 n} \\
    q_{21} & q_{22} & & q_{2 n} \\
    \ldots & \ldots & \ldots & \ldots \\
    q_{m 1} & q_{m 2} & \ldots & q_{m n}
    \end{array}\right]

The membership of a given alternative :math:`A_i` to the approximation area (:math:`G`, :math:`G^{+}` or :math:`G^{-}`)
is established by (:eq:`equ:aproxma`).

.. math::
    :label: equ:aproxma

    A_{i} \in\left\{\begin{array}{lll}
    G^{+} & \text {if } & q_{i j}>0 \\
    G & \text { if } & q_{i j}=0 \\
    G^{-} & \text {if } & q_{i j}<0
    \end{array}\right.

**Step 6.** Ranking the alternatives according to the sum of the distances of the alternatives from the areas of
approximation of the borders (:eq:`equ:sima`).

.. math::
    :label: equ:sima

    S_{i}=\sum_{j=1}^{n} q_{i j}, \quad j=1,2, \ldots, n, \quad i=1,2, \ldots, m

MAIRCA
=======================

``MAIRCA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat3`).

.. math::
    :label: equ:mat3

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Determining the preference for choosing alternatives using the vector :math:`P_{Ai}` using the formula
(:eq:`equ:pia`). In ``pymcdm``, all criteria treated equally, with no option for providing preferences for the
alternatives (second option).

.. math::
    :label: equ:pia

    P_{A i}=\frac{1}{n} ; \sum_{i=1}^{n} P_{A i}=1, i=1,2, \ldots, n

If the decision-maker is neutral in choosing an alternative, the vector :math:`P_{Ai}` should have the same values
(:eq:`equ:pia2`).

.. math::
    :label: equ:pia2

    P_{A 1}=P_{A 2}=\ldots=P_{A n}


**Step 3.** Creating a theoretical ranking matrix :math:`T_p`. The elements of this matrix are the multiplied priorities
of alternatives by the criteria weights. The form of this matrix can be represented by the formula (:eq:`equ:tp`).

.. math::
    :label: equ:tp

    T_{p}=\left[\begin{array}{cccc}
    t_{p 11} & t_{p 12} & \ldots & t_{p 1 m} \\
    t_{p 21} & t_{p 22} & \ldots & t_{p 2 m} \\
    \ldots & \cdots & \ldots & \ldots \\
    t_{p n 1} & t_{p n 2} & \ldots & t_{p n m}
    \end{array}\right] = \left[\begin{array}{cccc}
    P_{A 1} \cdot w_{1} & P_{A 1} \cdot w_{2} & \ldots & P_{A 1} \cdot w_{m} \\
    P_{A 2} \cdot w_{1} & P_{A 2} \cdot w_{2} & \ldots & P_{A m} \cdot w_{m} \\
    \ldots & \ldots & \ldots & \ldots \\
    P_{A n} \cdot w_{1} & P_{A n} \cdot w_{2} & \ldots & P_{A n} \cdot w_{m}
    \end{array}\right]

When the preferences determined for the alternatives by the decision-maker are equal, the theoretical ranking matrix is
represented by a theoretical ranking vector using the formula (:eq:`equ:tpwe`).

.. math::
    :label: equ:tpwe

    T_p =
    \left[\begin{array}{cccc}
    t_{p 11} & t_{p 12} & \ldots & t_{p 1 n}
    \end{array}\right]=
    \left[\begin{array}{llll}
    p_{A 1} . w_{1} & p_{A 1} \cdot w_{2} & \ldots & p_{A 1} \cdot w_{n}
    \end{array}\right]


**Step 4.** Create the real rating matrix, which is shown by the formula (:eq:`equ:tr`).

.. math::
    :label: equ:tr

    T_r =
    \left[\begin{array}{cccc}
    t_{r 11} & t_{r 12} & \ldots & t_{r 1 m} \\
    t_{r 21} & t_{r 22} & \ldots & t_{r 2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    t_{r n 1} & t_{r n 2} & \ldots & t_{r n m}
    \end{array}\right]


The values of the real rating matrix are determined depending on the criterion of profit type or cost type, sequentially
according to the formulas (:eq:`equ:trpr`) and (:eq:`equ:trcs`).

.. math::
    :label: equ:trpr

    \label{equ:trpr}
    t_{r i j}=t_{p i j} \cdot\left(\frac{x_{i j}-\min x_{j}}{\max x_{j}-\min x_{j}}\right)

.. math::
    :label: equ:trcs

    \label{equ:trcs}
    t_{r i j}=t_{p i j} \cdot\left(\frac{x_{i j}-\max x_{j}}{\min x_{j}-\max x_{j}}\right)

**Step 5.** Calculating the total gap matrix (:math:`G`) by taking the difference between the theoretical grade matrix
(:math:`Tp`) and the actual grade matrix (:math:`Tr`) using the formula (:eq:`equ:gap`).

.. math::
    :label: equ:gap

    G=T_{p}-T_{r}= \left[\begin{array}{cccc}
    t_{p 11}-t_{r 11} & t_{p 12}-t_{r 12} & \ldots & t_{p 1 m}-t_{r 1 m} \\
    t_{p 21}-t_{r 21} & t_{p 21}-t_{r 21} & \ldots & t_{p 2 m}-t_{r 2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    t_{p n 1}-t_{r n 1} & t_{p n 2}-t_{r n 2} & \ldots & t_{p n m}-t_{r n m}
    \end{array}\right]

**Step 6.** Calculating the final values of the criterion functions (:math:`Q_i`) for the alternatives using the sum of
the rows of the gap matrix (:math:`G`) using the formula (:eq:`equ:qima`). The alternative with the lowest value of
:math:`Q_i` has the highest ranking.

.. math::
    :label: equ:qima

    \label{equ:qima}
    Q_{i}=\sum_{j=1}^{m} g_{i j} \quad i=1,2, \ldots, n

MARCOS
=======================

``MARCOS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.**  Based on the decision matrix, create an augmented decision matrix with the ideal solution (AI) defined in
the last row and the anti-ideal (AAI) solution defined in the first row. This can be represented by
the Equation (:eq:`equ:extdecmat`).

.. math::
    :label: equ:extdecmat

        M = \left[\begin{array}{cccc}
                  x_{11} & x_{12} & \dots & x_{1n} \cr
                  x_{21} & x_{22} & \dots & x_{2n} \cr
                  \dots & \dots & \dots & \dots \cr
                  x_{m1} & x_{m2} & \dots & x_{mn} \cr
                  x_{ai1} & x_{ai2} & \dots & x_{ain} \cr
                  x_{aa1} & x_{aa2} & \dots & x_{aan} \cr
            \end{array}\right]

The ideal :math:`AI` and anti-ideal :math:`AAI` solution values for the cost (C) and benefit (B) criteria are defined
as follows:

.. math::
    :label: equ:aai

      AAI = \left  \{ \begin{array}{cc}
            \min_i x_{ij} &  if \quad j \in B\\
           \max_i x_{ij}  & if \quad j \in C
        \end{array} \right .

.. math::
    :label: equ:ai

      AI = \left  \{ \begin{array}{cc}
            \max_i x_{ij} &  if \quad j \in B\\
           \min_i x_{ij}  & if \quad j \in C
        \end{array} \right .

**Step 2.** Normalization of the extended decision matrix using Equation (:eq:`equ:normext`).

.. math::
    :label: equ:normext

        n_{ij} = \left  \{
        \begin{array}{cc}
         \frac{x_{ai}}{x_{ij}} & if \quad j \in C \\
         \frac{x_{x_{ij}}}{x_{ai}} & if \quad j \in B
        \end{array}\right .


**Step 3.** Create a weighted matrix based on the values from the normalized extended matrix according to the formula
(:eq:`equ:wema`).

.. math::
    :label: equ:wema

    v_{i j}=w_{i} \cdot\left(n_{i j}+1\right)


**Step 4.** Calculating the degrees of utility of alternatives :math:`K_i` relative to the ideal and anti-ideal
solution using Equations (:eq:`equ:kiplu`), (:eq:`equ:kimin`).


.. math::
    :label: equ:kiplu

        K_{i}^{+} = \frac{S_i}{S_{ai}}

.. math::
    :label: equ:kimin

        K_{i}^{-} = \frac{S_i}{S_{aai}}

where :math:`S_i` :math:`(i=1,2,\dots,m)` represents the sum of the elements of weighted matrix :math:`V`, Equation
(:eq:`equ:summ`).

.. math::
    :label: equ:summ

        S_i = \sum_{i=1}^n v_{ij}

**Step 5.** Determination of the utility function for the decision options considered according to (:eq:`equ:utilll`).

.. math::
    :label: equ:utilll

    f\left(K_{i}\right)=\frac{K_{i}^{+}+K_{i}^{-}}{1+\frac{1-f\left(K_{i}^{+}\right)}{f\left(K_{i}^{+}\right)}+\frac{1-f\left(K_{i}^{-}\right)}{f\left(K_{i}^{-}\right)}}

where :math:`f(K_{i}^{-})` denotes the utility function relative to the anti-ideal solution, while
:math:`f(K_{i}^{+})` denotes the utility function relative to the ideal solution, which can be determined using
the Equations respectively (:eq:`equ:kmf`) and (:eq:`equ:kpf`).

.. math::
    :label: equ:kmf

    f\left(K_{i}^{-}\right)=\frac{K_{i}^{+}}{K_{i}^{+}+K_{i}^{-}}

.. math::
    :label: equ:kpf

    f\left(K_{i}^{+}\right)=\frac{K_{i}^{-}}{K_{i}^{+}+K_{i}^{-}}

Note, that alternatives with smaller values of :math:`f(K_i)` are determined as better alternatives.

MOORA
=======================

``MOORA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_moora`).

.. math::
    :label: equ:mat_moora

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Normalize the decision matrix based on the Equation (:eq:`normm`).

.. math::
    :label: normm

        r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m}{x_{ij}^2}}}

where :math:`x_{ij}` can be called the value of the :math:`i-th` alternative for the :math:`j-th` criterion.

**Step 3.** Determine weighted normalized decision matrix based on Equation (:eq:`weigh`).

.. math::
    :label: weigh

        v_{ij} =  r_{ij} w_{j}

where :math:`w_j` can be called the weight for :math:`j-th` criterion.

**Step 4.** Calculate the value of :math:`P_i` based on the values from the normalized weighted decision matrix :math:`v_{ij}`
by using Equation (:eq:`yii`).

.. math::
    :label: yii

        P_i = \sum_{j=1}^g v_{ij} - \sum_{j=g+1}^n v_{ij}

where type of beneficial and cost criteria are represented as
follows :math:`j = 1, 2, \dots, g` and :math:`j = g + 1, g + 2,\dots,n`.

Higher values of :math:`P_i` corresponds to better alternatives.

MULTIMOORA
=======================

``MULTIMOORA`` combines three approaches on the matrix normalized as in MOORA [#multimooraref1]_ and aggregates their
rankings with the dominance theory [#multimooraref2]_. It is designed to evaluate decision alternatives according to
the following steps:

**Step 1.** Normalize the decision matrix.

.. math::
    :label: multimoora1

    x^*_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}

**Step 2.** Calculate the ratio system: benefit criteria are added and cost criteria are subtracted.

.. math::
    :label: multimoora2

    y^*_i = \sum_{j \in G^+} w_j x^*_{ij} - \sum_{j \in G^-} w_j x^*_{ij}

**Step 3.** Calculate the reference point: the maximal (benefit criteria) or minimal (cost criteria) normalized
values :math:`r_j`, and the largest weighted deviation from it (Min-Max metric of Tchebycheff).

.. math::
    :label: multimoora3

    z_i = \max_j w_j \left| r_j - x^*_{ij} \right|

**Step 4.** Calculate the full multiplicative form.

.. math::
    :label: multimoora4

    U_i = \frac{\prod_{j \in G^+} x_{ij}^{w_j}}{\prod_{j \in G^-} x_{ij}^{w_j}}

**Step 5.** Rank the alternatives in each part (descending :math:`y^*_i` and :math:`U_i`, ascending :math:`z_i`) and
aggregate the three rankings with the dominance theory: alternative :math:`a` dominates :math:`b` if it is better in
at least two of the three rankings (absolute dominance, better in all three, is a special case), and dominance is
transitive: if :math:`a` dominates :math:`b` and :math:`b` dominates :math:`c`, then :math:`a` dominates :math:`c`.
Alternatives in a circular dominance get the same rank. The preference :math:`P_i` is the number of alternatives
minus the number of alternatives which dominate :math:`A_i`, directly or through transitivity, outside its circle;
higher values correspond to better alternatives, so an alternative is always ranked above every alternative it
dominates. Alternatives which neither dominate each other nor are in one circle (e.g. because of ties in the rankings)
may share a position.

The original method uses no weights; equal weights give the same rankings.

.. [#multimooraref1] Brauers, W. K. M., & Zavadskas, E. K. (2010). Project management by MULTIMOORA as an instrument
   for transition economies. Technological and Economic Development of Economy, 16(1), 5-24.

.. [#multimooraref2] Brauers, W. K. M., & Zavadskas, E. K. (2011). MULTIMOORA optimization used to decide on a bank
   loan to buy property. Technological and Economic Development of Economy, 17(1), 174-188.

OCRA
=======================

``OCRA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_ocra`).

.. math::
    :label: equ:mat_ocra

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Normalize the decision matrix based on the Equation (:eq:`norm_ocra`) for the cost criteria (assuming
that there is :math:`g` cost criteria) and (:eq:`norm_ocra2`) for the profit criteria.

.. math::
    :label: norm_ocra

        \overline{I}_i = \sum_{j=1}^{g} w_j \frac{\max(x_{ij}) - x_{ij}}{\min(x_{ij})} \quad (i = 1, 2, \ldots, m; \, j = 1, 2, \ldots, g)

.. math::
    :label: norm_ocra2

        \overline{O}_i = \sum_{j=g+1}^{n} w_j \frac{x_{ij} - \min(x_{ij})}{\min(x_{ij})} \quad (i = 1, 2, \ldots, m; \, j = g+1, g+2, \ldots, n)

**Step 4.** Determination of preferences for cost-type and profit-type criteria sequentially according to the Equations
(:eq:`costI`),(:eq:`profO`).

.. math::
    :label: costI

    \overline{\overline{I}}_{i}=\overline{I}_{i}-\min \left(\overline{I}_{i}\right)

.. math::
    :label: profO

    \overline{\overline{O_{i}}}={\overline{O_{i}}} \min \left(\overline{O}_{i}\right)

where :math:`\overline{I}_{i}` is a measure of relative performance for the :math:`i-th` alternative and cost-type criteria,
and :math:`\overline{O}_{i}` is a measure of of relative performance for the :math:`i-th` alternative and profit-type criteria.

**Step 5.** Determine the overall preference of the considered alternatives using the Equation (:eq:`ocrapref`).

.. math::
    :label: ocrapref

    P_i = \overline{\overline{I}}_{i} + \overline{\overline{O_{i}}} - \min \left ( \overline{\overline{I}}_{i} + \overline{\overline{O_{i}}}\right )

Alternatives with the highest overall performance rating receives the first rank.

PROBID
=======================

``PROBID`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_probid`).

.. math::
    :label: equ:mat_probid

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Normalize the decision matrix using the vector method.

.. math::

    r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^{n} x_{kj}^2}} \quad i \in \{1, 2, \ldots, n\}; \, j \in \{1, 2, \ldots, m\}


**Step 3.** Create normalized weighted decision matrix.

.. math::

        v_{ij} =  r_{ij} w_{j}


**Step 4.** Sort the normalized weighted decision matrix by criteria taking into account their type. This will a matrix
of successively Positive Ideal Solutions (1st, 2nd, ..., mth PIS) will be formed. It can be presented by using the
following formula:

.. math::

    \begin{aligned}
    A_{(k)} & =\left\{\left(\operatorname{Large}\left(v_j, k\right) \mid j \in J\right),\left(\operatorname{Small}\left(v_j, k\right) \mid j \in J^{\prime}\right)\right\} \\
    & =\left\{v_{(k) 1}, v_{(k) 2}, v_{(k) 3}, \ldots, v_{(k) j}, \ldots, v_{(k) n}\right\}
    \end{aligned}


where :math:`k \in \{1,2, \ldots, n\}`, :math:`J` is the set of benefit criteria and :math:`J^{\prime}` is the set of cost
criteria.

Then, find the average value of each objective column as follow:

.. math::

    \bar{v}_j=\frac{\sum_{k=1}^n v_{(k) j}}{n} \quad \text { for } j \in\{1,2, \ldots, m\}


The average solution is then given by

.. math::

    \bar{A}=\left\{\bar{v}_1, \bar{v}_2, \bar{v}_3, \ldots, \bar{v}_j, \ldots, \bar{v}_m\right\}


**Step 5.** Iteratively calculate the Euclidean distance of each solution to each of the m ideal solutions as well as to
the average solution. The distance to ideal solutions is found as:

.. math::

    S_{i(k)}=\sqrt{\sum_{j=1}^m\left(v_{i j}-v_{(k) j}\right)^2}


**Step 6.** Determine the overall positive-ideal distance and negative-ideal distance as follow:

.. math::

    S_{i(\text { pos-ideal })}=\left\{\begin{array}{l}
    \sum_{k=1}^{(n+1) / 2} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \\
    \text { is an odd number } \\
    \sum_{k=1}^{n / 2} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \\
    \text { is an even number }
    \end{array}\right.


.. math::

    S_{i(\text { neg-ideal })}
    \quad=\left\{\begin{array}{l}
    \sum_{k=(n+1) / 2}^n \frac{1}{n-k+1} S_{i(k)} \\
    i \in\{1,2, \ldots, n\} \text { when } n \text { is an odd number } \\
    \sum_{k=n / 2+1}^n \frac{1}{n-k+1} S_{i(k)} \\
    i \in\{1,2, \ldots, n\} \text { when } n \text { is an even number }
    \end{array}\right.


There is also simplified provedure for calculating overall positive-ideal and negative-ideal distances.
In this case, the method is called sPROBID and the procedure is as follows:

.. math::

    S_{i(\text { pos-ideal })}=\left\{\begin{array}{l}
    \sum_{k=1}^{n \backslash 4} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \geq 4 \\
    S_{i(1)} \quad i \in\{1,2, \ldots, n\} \text { when } 0<n<4
    \end{array}\right.


.. math::

    S_{i(\text { neg-ideal })}=\left\{\begin{array}{l}
    \sum_{k=n+1-(n \ 4)}^n \frac{1}{n-k+1} S_{i(k)} \\
    \quad i \in\{1,2, \ldots, n\} \text { when } n \geq 4 \\
    S_{i(n)} \quad i \in\{1,2, \ldots, n\} \text { when } 0<n<4
    \end{array}\right.


**Step 7.** Calculate the pos-ideal/neg-ideal ratio (:math:`R_i`) and then the performance score (:math:`P_i`) of each
solution as follows:

.. math::

    R_i=\frac{S_{i(\text { pos-ideal })}}{S_{i(\text { neg-ideal })}}


.. math::

    P_i=\frac{1}{1+R_i^2}+S_{i(\mathrm{avg})}


Alternatives with the highest preference value receives the first rank.

RAM
=======================

``RAM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_ram`).

.. math::
    :label: equ:mat_ram

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]

**Step 2.** Calculate normalized decision matrix values :math:`r_{i j}`
using equation (:eq:`eq:ram_sum`).

.. math::
    :label: eq:ram_sum

        r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{n} x_{i j}}


**Step 3.** Calculate weighted normalized decision matrix, which represents multiplication of the normalized decision
matrix elements with the appropriate weight coefficients using equation (:eq:`eq:ram_e`).

.. math::
    :label: eq:ram_e

        v_{ij} = r_{ij} \cdot w_j

**Step 4.** Calculate the sums of weighted normalized scores of beneficial (:math:`+i`) and cost (:math:`-i`) criteria
of :math:`i-th` alternative by the following equations:

.. math::

    S_{+i} = \sum^{m}_{j=1} v_{+ij}


.. math::

    S_{-i} = \sum^{m}_{j=1} v_{-ij}


**Step 5.** Determine the overall score of each alternative using the following aggreating function:

.. math::

    RI_{i} = \sqrt[{2 + S_{-i}}]{2 + S_{+i}}


**Step 6.** Rank the alternatives using the value of :math:`RI_i`. The alternatives with the bigger value
of :math:`RI_i` are more preferred ones.


RAFSI
=====

*Žižović et al. (2020)* introduce the *Ranking of Alternatives through Functional mapping of
criterion Sub-intervals into a Single Interval* (RAFSI) method as a multi-attribute decision-making
(MADM) approach designed to eliminate the rank reversal problem. The key idea of RAFSI is to
map all criterion values from their original domains into a common, predefined interval using
functional transformations based on **ideal** and **anti-ideal** reference points. The resulting
normalized values are aggregated using a weighted linear function to obtain a stable ranking of
alternatives.

Let there be :math:`m` alternatives :math:`A_i \ (i=1,\dots,m)` evaluated with respect to
:math:`n` criteria :math:`C_j \ (j=1,\dots,n)` with weights :math:`w_j`, where
:math:`\sum_{j=1}^n w_j = 1`. Criteria can be of *maximization* or *minimization* type.

Steps of the RAFSI Method
-------------------------

**Step 1: Define ideal and anti-ideal values**

For each criterion :math:`C_j`, define:

- :math:`a_j^I` – ideal (best) value
- :math:`a_j^N` – anti-ideal (worst acceptable) value

For maximization criteria: :math:`a_j^I > a_j^N`
For minimization criteria: :math:`a_j^I < a_j^N`

**Step 2: Functional mapping to a common interval**

All criterion values are mapped into a fixed numerical interval
:math:`[n_1, n_{2k}]`, where :math:`n_1` and :math:`n_{2k}` represent the relative preference of
the ideal over the anti-ideal value (e.g. :math:`n_1 = 1`, :math:`n_{2k} = 6`).

Each element :math:`x` of the initial decision matrix is transformed using the linear mapping
function:

.. math::

   f_s(x) =
   \frac{n_{2k} - n_1}{a_j^I - a_j^N} \, x
   + \frac{a_j^I n_1 - a_j^N n_{2k}}{a_j^I - a_j^N}

This produces the standardized decision matrix
:math:`S = [s_{ij}]`, where :math:`s_{ij} \in [n_1, n_{2k}]`.

**Step 3: Compute arithmetic and harmonic means**

Using the boundary values of the common interval, compute:

.. math::

   A = \frac{n_1 + n_{2k}}{2}

.. math::

   H = \frac{2}{\frac{1}{n_1} + \frac{1}{n_{2k}}}

**Step 4: Normalize the standardized matrix**

The elements of matrix :math:`S` are normalized into the interval :math:`[0,1]`:

- For *maximization* criteria:

.. math::

   \hat{s}_{ij} = \frac{s_{ij}}{2A}

- For *minimization* criteria:

.. math::

   \hat{s}_{ij} = \frac{H}{2 s_{ij}}

This yields the normalized decision matrix
:math:`\hat{S} = [\hat{s}_{ij}]`.

**Step 5: Calculate the overall performance score**

The final performance (criteria function) of each alternative is computed as a weighted sum:

.. math::

   V(A_i) = \sum_{j=1}^{n} w_j \, \hat{s}_{ij}

Alternatives are ranked in descending order of :math:`V(A_i)`. A higher value indicates a more
preferred alternative. Due to the functional mapping and normalization scheme, the RAFSI method
exhibits strong resistance to rank reversal when alternatives are added or removed.

**Reference**

Žižović, M., Pamučar, D., Albijanić, M., Chatterjee, P., & Pribićević, I. (2020).
*Eliminating rank reversal problem using a new multi-attribute model—the RAFSI method*.
Mathematics, 8(6), 1015.


RIM
=======================

``RIM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define the following values, which determine the problem's context and the problem itself.

- Criteria weights: :math:`w_j, j \in \{1, 2, \ldots N\}` and the sum of the criteria weights should
  be equal to one: :math:`\sum^N_{j = 1} w_j = 1`.

- Decision matrix: :math:`X = [ x_{ij} ]_{M \times N}` which contains information
  about :math:`M` alternatives evaluated under :math:`N` criteria.

- The Criteria Range: :math:`t_j = [t_{j}^{(min)}, t_{j}^{(max)}]`, :math:`j \in \{1, 2, \ldots N\}` which
  defines the arbitrary chosen bounds of the criteria.

- The Reference Ideal: :math:`s_j = [s_{j}^{(min)}, s_{j}^{(max)}]`,
  :math:`j \in \{1, 2, \ldots N\}` and :math:`[s_{j}^{(min)}, s_{j}^{(max)}] \subset [t_{j}^{(min)}, t_{j}^{(max)}]`.
  Reference Ideal define most preferred interval of values for each criterion. It can be either derived from criteria
  range, or define expected outcome of decision process.


**Step 2.** After defining the problem we should normalize the decision matrix :math:`X` using the RIM normalization
function :math:`f(x,[A, B],[C, D])` defined as (:eq:`eq:rmnorm`). This normalization requires a definition
of the criteria range :math:`[A. B]` and the reference ideal :math:`[C, D]`.

.. math::
    :label: eq:rmnorm

    f(x,[A, B],[C, D]) = \left\{\begin{array}{lll}
    1 &\textit{IF}& x \in[C, D] \\
    1-\frac{d_{\min }(x,[C, D])}{|A-C|} &\textit{IF}& x \in[A, C] \wedge A \neq C \\
    1-\frac{d_{\min }(x,[C, D])}{|D-B|} &\textit{IF}& x \in[D, B] \wedge D \neq B
    \end{array}\right.,

where :math:`[A, B]` is range of criteria, :math:`[C, D]` is the reference ideal, and :math:`x \in [A, B]`, :math:`[C, D] \subset [A, B]`. Function :math:`d_{min}(x, [C, D])` is defined as (:eq:`eq:d_min`).

.. math::
    :label: eq:d_min

        d_{min}(x, [C, D]) = min(|x - C|, |x - D|)


This normalization allows to map value :math:`x` to range :math:`[0, 1]` in the criteria domain with regard to the ideal reference interval. The normalization process is defined as follows (:eq:`eq:rim_nmatrix`).

.. math::
    :label: eq:rim_nmatrix

    Y = [ y_{ij} ]_{M \times N} = [ f(x_{ij}, t_j, s_j) ]_{M \times N}


**Step 3.** Calculate the weighted normalized matrix :math:`Y^\prime` using (:eq:`eq:rim_wnmatrix`).

.. math::
    :label: eq:rim_wnmatrix

        Y^\prime = [ y_{ij}^{\prime} ] = Y \otimes W = [ y_{ij} \cdot w_{j} ]_{M \times N}


**Step 4.** Compute the variation to the normalized reference ideal for each alternative :math:`A_i` using Equations (:eq:`eq:rim_iplus`) and (:eq:`eq:rim_iminus`).

.. math::
    :label: eq:rim_iplus

        I_i^{+}=\sqrt{\sum_{j=1}^n\left(y^{\prime}{ }_{i j}-w_j\right)^2}% \quad i \in \{1, 2, \ldots M\}, \quad j \in \{1, 2, \ldots N\}


.. math::
    :label: eq:rim_iminus

        I_i^{-}=\sqrt{\sum_{j=1}^n\left(y^{\prime}\right)^2}% \quad i \in \{1, 2, \ldots M\}, \quad j \in \{1, 2, \ldots N\}


**Step 5.** Calculate the relative index of each alternative :math:`A_i`, using the Equation (:eq:`eq:rim_r`).

.. math::
    :label: eq:rim_r

        P_i = \frac{I_i^-}{I_i^+ + I_i^-} %\quad i \in \{1, 2, \ldots M\}


Order the alternative :math:`A_i` in descending order with regard to :math:`P_i`. The alternatives with the bigger value
of :math:`P_i` are more preferred ones.


RPM
=======================

``RPM`` (Reference Point Method) with objective ranking [#rpmref1]_ [#rpmref2]_ evaluates every criterion with respect
to the reservation and aspiration levels and aggregates the partial achievements in a way determined mostly by the
worst of them. The method does not use weights; the importance of criteria is expressed by the parameters
:math:`\alpha` and :math:`\beta`. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`Q = [q_{ij}]`, of the lower and upper bounds :math:`q_j^{lo}`,
:math:`q_j^{up}` of the criteria (parameter ``bounds``, by default the minimum and the maximum of the data) and of
the reservation :math:`r_j` and aspiration :math:`a_j` levels. By default, they are determined statistically
(objective ranking), for benefit criteria:

.. math::
        q_j^{av} = \frac{1}{m} \sum_{i=1}^{m} q_{ij}, \qquad r_j = \frac{q_j^{lo} + q_j^{av}}{2}, \qquad
        a_j = \frac{q_j^{up} + q_j^{av}}{2}
    :label: rpm_levels

**Step 2.** Calculate the partial achievements on the scale 0-10, for benefit criteria (cost criteria are mirrored):

.. math::
        \sigma_{ij} = \begin{cases} \alpha_j \dfrac{q_{ij} - q_j^{lo}}{r_j - q_j^{lo}} & q_j^{lo} \leq q_{ij} < r_j
        \\[2ex] \alpha_j + (\beta_j - \alpha_j) \dfrac{q_{ij} - r_j}{a_j - r_j} & r_j \leq q_{ij} < a_j \\[2ex]
        \beta_j + (10 - \beta_j) \dfrac{q_{ij} - a_j}{q_j^{up} - a_j} & a_j \leq q_{ij} \leq q_j^{up} \end{cases}
    :label: rpm_partial

:math:`\alpha = 3`, :math:`\beta = 7` are the default (normal importance); (5, 9), (4, 8), (2, 6) and (1, 5)
express very low, low, high and very high importance of a criterion.

**Step 3.** Aggregate the partial achievements (parameter ``aggregation``):

* ``'achievement'`` (default), the overall achievement function with the regularizing coefficient :math:`\varepsilon`:

.. math::
        \sigma_i = \min_j \sigma_{ij} + \frac{\varepsilon}{n} \sum_{j=1}^{n} \sigma_{ij}
    :label: rpm_achievement

* ``'lorenz'``, the Lorenz quantile, the mean of the :math:`k` worst partial achievements :math:`\theta_{i1} \leq
  \theta_{i2} \leq \ldots` (parameter ``quantile``, by default :math:`n / 3`):

.. math::
        L_{ik} = \frac{1}{k} \sum_{l=1}^{k} \theta_{il}
    :label: rpm_lorenz

* ``'owa'``, the ordered weighted average :math:`\sigma_i^{owa} = \sum_{l=1}^{n} 2^{-l} \theta_{il}`.

The alternative with the highest value is the best.

.. [#rpmref1] Wierzbicki, A. P., Granat, J., & Makowski, M. (2007). Discrete decision problems with large number of
   criteria. IIASA Interim Report IR-07-025. International Institute for Applied Systems Analysis, Laxenburg.

.. [#rpmref2] Wierzbicki, A. P. (2007). Reference point approaches and objective ranking. In Practical Approaches to
   Multi-Objective Optimization, Dagstuhl Seminar Proceedings 06501.

SPOTIS
=======================

``SPOTIS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_spotis`).

.. math::
    :label: equ:mat_spotis

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Define the bounds of the problem - min and max bounds of classical MCDM problem must be defined to transform
MCDM problem form ill-defined to well-defined.

.. math::

    \left[S_{j}^{\min }, S_{j}^{\max }\right], j \in \{1, 2, \ldots, m\}


where, :math:`n` - criterion number, :math:`x_1` - min bound, :math:`x_2` - max bound.

**Step 3.** Define the ideal solution point - define vector which includes maximum or minimum from bounds for specific
criterion depending on criterion type. For profit type, the max value should be taken, for cost type, min value.

.. math::

    S^{\star}_{j}=\begin{cases}
        S_{j}^{\min} & \text{if j-th criterion is cost}\\
        S_{j}^{\max} & \text{if j-th criterion is profit}
    \end{cases}


**Step 4.** Compute normalized distance matrix - for each alternative :math:`A_{i}` (i= 1, :math:`\ldots` , M),compute
its normalized distance with respect to ideal solution for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ).

.. math::

    d_{i j}=\frac{\left|A_{i j}-S_{j}^{*}\right|}{\left|S_{j}^{\max }-S_{j}^{\min }\right|}


**Step 5.** Compute normalized averaged distance - for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ) take into
account its weight and calculate final preference by executing following Equation.

.. math::

    P_{i}=\sum_{j=1}^{N} w_{j} d_{i j}


As the :math:`P_i` value is interpreted as distance from the ideal or expected solution, alternatives with smaller
value of :math:`P_i` are preferred.

TOPSIS
=======================

``TOPSIS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_topsis`).

.. math::
    :label: equ:mat_topsis

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Normalize the decision matrix by using min-max normalization. The values of benefit type criteria are
normalized using the (:eq:`sumProfit`) formula, while the values of cost type criteria are normalized using the
(:eq:`sumCost`) formula.

.. math::
    :label: sumProfit

        r_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)}\


.. math::
    :label: sumCost

        r_{ij} = \frac{\max(x_j) - x_{ij}}{\max(x_j) - \min(x_j)}


**Step 3.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weightedsds`).

.. math::
    :label: weightedsds

        v_{ij} = w_{j}r_{ij}


**Step 4.** Derive a positive ideal solution :math:`PIS` and a negative ideal solution :math:`NIS`. The ideal positive
solution is calculated as the maximum value for each criterion (:eq:`pis`), while the ideal negative solution is
calculated as the least value for each criterion (:eq:`nis`).

.. math::
    :label: pis

        v_{j}^{+} =  \{v_{1}^{+},  v_{2}^{+},  \dots,  v_{m}^{+} \} = \{\max_{j}(v_{ij}) \}


.. math::
    :label: nis

        v_{j}^{-} = \{v_{1}^{-},  v_{2}^{-},  \dots,  v_{m}^{-} \}=  \{\min_{j}(v_{ij}) \}


**Step 5.** Determine the Euclidean distance for each normalized weighted alternative from the :math:`PIS` (:eq:`sqrtPIS`)
and :math:`NIS` (:eq:`sqrtNIS`) solution.

.. math::
    :label: sqrtPIS

        D_{i}^{+} = \sqrt{\sum_{j=1}^{m}(v_{ij}-v_{j}^{+})^{2}}


.. math::
    :label: sqrtNIS

        D_{i}^{-} = \sqrt{\sum_{j=1}^{m}(v_{ij}-v_{j}^{-})^{2}}


**Step 6.** Calculate final preference value according to the Equation:

.. math::

        P_i = \frac{D^{-}_{i}}{D^{-}_{i} + D^{+}_{i}}


Alternative with the highest value of :math:`P_i` considered the best.

R-TOPSIS
=======================

``RTOPSIS`` (Robust TOPSIS) removes the dependence of TOPSIS on the set of alternatives. Every criterion is normalized
on a domain :math:`[d_{1j}, d_{2j}]` given by the decision maker instead of on the values in the decision matrix, and the
ideal solutions are fixed at the ends of that domain. The evaluation of an alternative therefore does not change when
other alternatives are added or removed. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`X = [x_{ij}]` of dimension :math:`n \times m` and of a domain
:math:`D_j = [d_{1j}, d_{2j}]` for every criterion, where :math:`d_{1j} \leq x_{ij} \leq d_{2j}`.

**Step 2.** Normalize the decision matrix with the Max (:eq:`rtopsis_max`) or the Max-Min (:eq:`rtopsis_minmax`)
normalization. Both are applied in the same way to benefit and cost criteria.

.. math::
        n_{ij} = \frac{x_{ij}}{d_{2j}}
    :label: rtopsis_max

.. math::
        n_{ij} = \frac{x_{ij} - d_{1j}}{d_{2j} - d_{1j}}
    :label: rtopsis_minmax

**Step 3.** Calculate the weighted normalized decision matrix :math:`r_{ij} = w_j n_{ij}`.

**Step 4.** Set the positive and negative ideal solutions at the weighted normalized ends of the domain, where
:math:`N(\cdot)` is the normalization from Step 2:

.. math::
        r_{j}^{+} = \begin{cases} w_j N(d_{2j}) & \text{for benefit criteria} \\ w_j N(d_{1j}) & \text{for cost criteria} \end{cases}
        \qquad
        r_{j}^{-} = \begin{cases} w_j N(d_{1j}) & \text{for benefit criteria} \\ w_j N(d_{2j}) & \text{for cost criteria} \end{cases}
    :label: rtopsis_ideals

For the Max normalization this gives :math:`w_j` and :math:`w_j d_{1j}/d_{2j}`, as in the original method, and for the
Max-Min normalization :math:`w_j` and 0.

**Step 5.** Determine the Euclidean distances :math:`S_i^{+}` and :math:`S_i^{-}` of every alternative from the
:math:`PIS` and the :math:`NIS`, as in TOPSIS.

**Step 6.** Calculate the closeness coefficient :math:`CC_i = S_i^{-} / (S_i^{+} + S_i^{-})`. The alternative with the
highest value is the best.

Several other rank-reversal-free variants of TOPSIS differ from R-TOPSIS only in the source of the domain and can be
obtained with its parameters:

* NR-TOPSIS: historical minimum and maximum of every criterion (:meth:`RTOPSIS.make_bounds`) with the Max-Min
  normalization;
* the absolute mode of García-Cascales and Lamata: one common scale :math:`[Z_0, Z_t]` for all criteria with the Max
  normalization;
* the domain of IE-TOPSIS: observed extremes extended by :math:`\alpha` sample standard deviations
  (:meth:`RTOPSIS.expand_bounds`) with the Max-Min normalization; the domain should be computed once and kept fixed;
* TOPSIS-RAD: vetoed and desired performance levels as the domain, the Max-Min normalization and ``clip=True``, which
  clips performances above the desired levels; vetoed alternatives are removed from the decision matrix beforehand.

TOPSIS-Sort
=======================

:class:`TOPSIS_SORT` (``pymcdm.methods.sorting.TOPSIS_SORT``) is a sorting method based on R-TOPSIS: it assigns the
alternatives to predefined, ordered categories :math:`C_1, \ldots, C_q` (from the worst to the best) instead of
ranking them [#topsissortref1]_. Because the ideal and anti-ideal solutions are fixed by the domain of the criteria,
the category of an alternative does not depend on the other alternatives. Two variants are available (parameter
``profiles_type``):

* TOPSIS-Sort-B (``'boundary'``): :math:`q - 1` boundary profiles :math:`b_1, \ldots, b_{q-1}`, where :math:`b_h` is
  the upper limit of :math:`C_h` and the lower limit of :math:`C_{h+1}`;
* TOPSIS-Sort-C (``'characteristic'``): :math:`q` characteristic profiles :math:`p_1, \ldots, p_q`, where
  :math:`p_h` is a typical alternative of :math:`C_h`.

The profiles (parameter ``profiles``) are ordered from the worst category to the best one, and each profile should be
at least as good as the previous one on every criterion.

**Step 1.** Determine the domain of every criterion (parameter ``bounds``), as in Step 3 of R-TOPSIS.

**Step 2.** Calculate the closeness coefficients :math:`Cl(a_i)` of the alternatives and :math:`Cl(P_h)` of the
profiles with R-TOPSIS (normalization by the maximum or interval normalization, weighted normalized matrix,
distances to the ideal and anti-ideal solutions fixed at the ends of the domain).

**Step 3.** Assign the alternatives to the categories:

* TOPSIS-Sort-B: :math:`a_i \in C_1` if :math:`Cl(a_i) < Cl(b_1)`, :math:`a_i \in C_h` if
  :math:`Cl(b_{h-1}) \leq Cl(a_i) < Cl(b_h)`, and :math:`a_i \in C_q` if :math:`Cl(a_i) \geq Cl(b_{q-1})`;
* TOPSIS-Sort-C: :math:`a_i` is assigned to the category of the profile with the closest coefficient,
  :math:`\min_h |Cl(a_i) - Cl(p_h)|`; ties are resolved in favor of the better category.

The closeness coefficients of the alternatives and the profiles are available with ``verbose=True``.

.. [#topsissortref1] de Lima Silva, D. F., & de Almeida Filho, A. T. (2020). Sorting with TOPSIS through boundary and
   characteristic profiles. Computers & Industrial Engineering, 141, 106328.

VIKOR
=======================

``VIKOR`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_vikor`).

.. math::
    :label: equ:mat_vikor

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Determinate the best :math:`f_{j}^{*}` and the worst :math:`f_{j}^{-}` value for the function of a particular
criterion. For profit criteria, the Equation is used (:eq:`VikorBestProfit`).

.. math::
    :label: VikorBestProfit

        f_{j}^{*} = \max_i x_{ij},\; \; \;  f_{j}^{-} = \min_i x_{ij}


where in the case of the cost criteria, the following Equation is used (:eq:`VikorBestCost`).

.. math::
    :label: VikorBestCost

        f_{j}^{*} = \min_i x_{ij},\; \; \;  f_{j}^{-} = \max_i x_{ij}


**Step 3.** Calculate :math:`S_{i}` and :math:`R_{i}` with using Equations (:eq:`VikorSi`) and (:eq:`VikorRi`).

.. math::
    :label: VikorSi

        S_{i} = \sum_{j=1}^{m}w_{j}(f_{j}^{*}-x_{ij})/(f_{j}^{*}-f_{j}^{-})


.. math::
    :label: VikorRi

        R_{i} = \max_j \left [w_{j}(f_{j}^{*}-x_{ij})/(f_{j}^{*}-f_{j}^{-}) \right ]


**Step 4.** Calculate :math:`Q_{i}` with using Equation (:eq:`VikorQi`).

.. math::
    :label: VikorQi

        Q_{i} = v(S_{i}-S^{*}) / (S^{-}-S^{*}) + (1 - v)(R_{i}-R^{*}) / (R^{-}-R^{*}) \label{VikorQi}


where:

:math:`S^{*} = min_{i} S_{i},\; \; \; S^{-} = max_{i} S_{i}`,

:math:`R^{*} = min_{i} R_{i},\; \; \; R^{-} = max_{i} R_{i}`,

:math:`v` means the weight adopted for the strategy of ''most criteria''.

**Step 5.** Ranked alternatives :math:`S`, :math:`R` and :math:`Q` are ordered in ascending order. Three ranked
lists are the outcome.

**Step 6.** A compromise solution is proposed considering the conditions of good advantage and acceptable stability
within the three vectors obtained in the previous step. The best alternative is the one with the lowest value
of :math:`Q` and the leading position in the ranking :math:`Q`. In ``pymcdm`` only :math:`Q` ranking is returned by
default.

R-VIKOR
=======================

``RVIKOR`` (R-VIKOR) removes the dependence of VIKOR on the set of alternatives in the same way as R-TOPSIS does for
TOPSIS [#rvikorref1]_. Every criterion is normalized on its domain :math:`[m_j, M_j]` (historical or admissible minimum
and maximum, parameter ``bounds``) instead of on the values in the decision matrix, and the ideal solutions are fixed
at the ends of that domain. The score of an alternative therefore does not change when other alternatives are added,
removed or replaced, and the method is defined also when all alternatives have the same :math:`R_i` and classical
VIKOR divides by zero. The method evaluates decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix :math:`X = [f_{ij}]` of dimension :math:`n \times m` and of a domain
:math:`[m_j, M_j]` for every criterion, where :math:`m_j \leq f_{ij} \leq M_j`.

**Step 2.** Normalize the decision matrix on the domain:

.. math::
        n_{ij} = \begin{cases} \dfrac{f_{ij} - m_j}{M_j - m_j} & \text{for benefit criteria} \\[2ex]
        \dfrac{M_j - f_{ij}}{M_j - m_j} & \text{for cost criteria} \end{cases}
    :label: rvikor_norm

**Step 3.** Calculate the group utility :math:`S_i` and the individual regret :math:`R_i`:

.. math::
        S_i = \sum_{j=1}^{m} w_j (1 - n_{ij}), \qquad R_i = \max_j w_j (1 - n_{ij})
    :label: rvikor_sr

**Step 4.** Calculate the score of every alternative, where :math:`v \in [0, 1]` is the weight of the strategy of the
maximum group utility (parameter ``v``):

.. math::
        NQ_i = v S_i + (1 - v) \frac{R_i}{\max_j w_j}
    :label: rvikor_nq

For weights which sum to 1, both :math:`S_i` and :math:`R_i / \max_j w_j` lie in :math:`[0, 1]`, with 0 for the
positive ideal solution (otherwise :math:`S_i` lies in :math:`[0, \sum_j w_j]`). The
alternative with the lowest value of :math:`NQ_i` is the best. The domain can be obtained with
:meth:`RTOPSIS.make_bounds` or :meth:`RTOPSIS.expand_bounds`, and ``clip=True`` clips values outside of it.

.. [#rvikorref1] Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR. IEEE Access, 8,
   21261-21271.

WASPAS
=======================

``WASPAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_waspas`).

.. math::
    :label: equ:mat_waspas

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Normalize the decision matrix using the linear normalization method, according to:

.. math::

    r_{ij} = \frac{x_{ij}}{\max_i x_{ij}}, \text{if j-th criterion is profit}


.. math::

    r_{ij} = \frac{\min x_{ij}}{x_{ij}}, \text{if j-th criterion is cost}



**Step 3.** Calculate WSM and WPM as follow:

.. math::

    W S M=\sum_{j=1}^n r_{i j} w_j


.. math::

    W P M=\prod_{j=1}^n\left(r_{i j}\right)^{w_j}


where :math:`w_j` denote the weights for the criteria, and :math:`r_ij` denote the values of the decision options from
the normalized decision matrix.

**Step 4.** Calculation of total relative importance for each alternative as follow:

.. math::

    Q_i=\lambda WSM+(1-\lambda) WPM=\lambda \sum_{j=1}^n r_{i j} w_j+(1-\lambda) \prod_{j=1}^n\left(r_{i j}\right)^{w_j}


Higher values of :math:`Q_i` points to better alternatives.


WPM
=======================

``WPM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_wpm`).

.. math::
    :label: equ:mat_wpm

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Normalize the decision matrix using the sum method.

.. math::

        r_{ij} = \frac{x_{ij}}{\sum_m^{i=1}x_{ij}}, \text{if j-th criterion is profit}


.. math::

        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=1}\frac{1}{x_{ij}}}, \text{if j-th criterion is cost}


**Step 3.** Calculate WPM as follow:

.. math::

    W P M=\prod_{j=1}^n\left(r_{i j}\right)^{w_j}


where :math:`w_j` denote the weights for the criteria, and :math:`x_{ij}` denote the values of the decision options from
the normalized decision matrix.

WSM
=======================

``WSM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_wsm`).

.. math::
    :label: equ:mat_wsm

    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]


**Step 2.** Normalize the decision matrix using the sum method.

.. math::

        r_{ij} = \frac{x_{ij}}{\sum_m^{i=1}x_{ij}}, \text{if j-th criterion is profit}


.. math::

        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=1}\frac{1}{x_{ij}}}, \text{if j-th criterion is cost}


**Step 3.** Calculate WSM as follow:

.. math::

    W S M=\sum_{j=1}^n r_{i j} w_j


where :math:`w_j` denote the weights for the criteria, and :math:`x_{ij}` denote the values of the decision options from
the normalized decision matrix.
