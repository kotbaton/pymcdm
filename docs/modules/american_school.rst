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
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat1

**Step 2.** Definition of a extended decision matrix, where decision matrix :math:`X` is extended with
optimal value :math:`x_0` (:eq:`equ:emat1`). Optimal solution can be defined as the optimal (expected) values for
each of the criteria. If it is not defined maximum value will be chosen for profit criteria and minimum value for the
cost criteria.

.. math::
    \begin{equation}
    X^{\prime} = [x_{i j}]=\left[\begin{array}{llll}
    x_{01} & x_{02} & \ldots & x_{0 m} \\
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:emat1

**Step 3.** Normalization the extended decision matrix, where for profit criteria use the equation (:eq:`equ:profita`),
and for cost, criteria use the equation (:eq:`equ:costa`). In ``pymcdm``, the Sum normalization method is used as the
default normalization in the ARAS method. Optimal solution is normalized as other values.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sum_m^{i=0}x_{ij}}
    \end{equation}
    :label: equ:profita

.. math::
    \begin{equation}
        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=0}\frac{1}{x_{ij}}}
    \end{equation}
    :label: equ:costa

**Step 4.** Building a weighted normalized extended decision matrix :math:`v_{ij}` based on the normalized extended
decision matrix and criteria weights :math:`w_{j}` using Equation (:eq:`weighted`).

.. math::
    \begin{equation}
        v_{ij} = w_{j}r_{ij} \label{weighted}
    \end{equation}
    :label: weighted

**Step 5.** Determining values of optimality function :math:`S_i` using the Equation (:eq:`opf`).
Note, that value :math:`S_i` is also calculated for optimal solution.

.. math::
    \begin{equation}
        S_i = \sum_{j=1}^{n} v_{ij}
    \end{equation}
    :label: opf

**Step 6.** Calculate the utility degree :math:`K_i` based on Equation (:eq:`ud`). ``pymcdm`` calculates
this value for the optimal solution but it is not showed in the verbose results.

.. math::
    \begin{equation}
        K_i = \frac{S_i}{S_0}
    \end{equation}
    :label: ud

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
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_cocoso

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profit`), and for
cost, criteria use the equation (:eq:`equ:cost`). In the ``pymcdm``, The Minimum-Maximum normalization method is used
as default normalization method.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij} - \min_{i}{x_{ij}}}{\max_{i}{x_{ij}} - \min_{i}{x_{ij}}}
    \end{equation}
    :label: equ:profit

.. math::
    \begin{equation}
        r_{ij} = \frac{\max_{i}{x_{ij}} - x_{ij}}{\max_{i}{x_{ij}} - \min_{i}{x_{ij}}}
    \end{equation}
    :label: equ:cost


**Step 3.** Calculation of the weighted sum of the comparison sequence and the total power weight of the comparison
sequences for each alternative. The values of :math:`S_i` are based on the grey relationship generation method
(:eq:`equ:SI`), and for :math:`P_i` the values are achieved according to the multiplicative WASPAS setting
(:eq:`equ:PI`).


.. math::
    \begin{equation}
        S_i = \sum_{j=1}^{n} (w_j r_{ij})
    \end{equation}
    :label: equ:SI

.. math::
    \begin{equation}
        P_i = \sum_{j=1}^{n} (r_{ij})^{w_j}
    \end{equation}
    :label: equ:PI


**Step 4.** Computation of the relative weights of alternatives using aggregation strategies. The formulas determine the
strategies (:eq:`equ:s1`)-(:eq:`equ:s3`), where the first strategy expresses the average of the sums of WSM and WPM s
cores (:eq:`equ:s1`), the second strategy expresses the sum of WSM and WPM scores over the best (:eq:`equ:s2`), and the
third strategy expresses the compromise strategy of WSM and WPM by using the :math:`\lambda` value (:eq:`equ:s3`).
Be default, ``pymcdm`` uses a :math:`\lambda` value of 0.5.

.. math::
    \begin{equation}
    k_{i a}=\frac{P_{i}+S_{i}}{\sum_{i=1}^{m}\left(P_{i}+S_{i}\right)}
    \end{equation}
    :label: equ:s1

.. math::
    \begin{equation}
    k_{i b}=\frac{S_{i}}{\min _{i} S_{i}}+\frac{P_{i}}{\min _{i} P_{i}}
    \end{equation}
    :label: equ:s2

.. math::
    \begin{equation}
    k_{i c}=\frac{\lambda\left(S_{i}\right)+(1-\lambda)\left(P_{i}\right)}{\left(\lambda \max _{i} S_{i}+(1-\lambda) \max _{i} P_{i}\right)} ; \quad 0 \leqslant \lambda \leqslant 1
    \end{equation}
    :label: equ:s3

**Step 5.** Establish the final ranking of alternatives based on :math:`k_i` values defined using the formula
(:eq:`equ:ki`). The higher the :math:`k_i` value, the higher the position of the alternative in the ranking.

.. math::
    \begin{equation}
    k_{i}=\left(k_{i a} k_{i b} k_{i c}\right)^{\frac{1}{3}}+\frac{1}{3}\left(k_{i a}+k_{i b}+k_{i c}\right)
    \end{equation}
    :label: equ:ki

CODAS
=======================

``CODAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat2`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat2

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profitc`), and for
cost, criteria use the equation (:eq:`equ:costc`). This normalization method (Linear normalization) is used as
a default normalization method in ``pymcdm``.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\max_i x_{ij}}
    \end{equation}
    :label: equ:profitc

.. math::
    \begin{equation}
        r_{ij} = \frac{\min_i x_{ij}}{x_{ij}}
    \end{equation}
    :label: equ:costc

**Step 3.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weightedc`).

.. math::
    \begin{equation}
        v_{ij} = w_{j}r_{ij} \label{weightedc}
    \end{equation}
    :label: weightedc

**Step 4.** Determine the negative-ideal solution (point) based on Equation (:eq:`nip`).

.. math::
    \begin{equation}
        ns_j = \min_i {v_ij}
    \end{equation}
    :label: nip

**Step 5.** Calculate the Euclideana :math:`E_i` and Taxicab :math:`T_i` distances of alternatives
from the negative-ideal solution, shown as follows:

.. math::
    \begin{equation}
        E_i = \sqrt{\sum_{i=1}^m \left ( v_{ij} - ns_j \right)^2}
    \end{equation}

.. math::
    \begin{equation}
        T_i = \sum_{j=1}^m \left | v_{ij} - ns_j \right |
    \end{equation}

**Step 6.** Construct the relative assessment matrix, shown as follows:

.. math::
    \begin{equation}
        h_{i k}=\left(E_{i}-E_{k}\right)+\left(\psi\left(E_{i}-E_{k}\right) \times\left(T_{i}-T_{k}\right)\right)
    \end{equation}

where :math:`k \in \left \{ 1,2,\cdots,n \right \}` and :math:`\psi` denotes a threshold function to recognize the
equality of the Euclidean distances of two alternatives, and is defined as follows:

.. math::
    \begin{equation}
        \psi(x)=\left\{\begin{array}{lll}
        1 & \text { if } & |x| \geq \tau \\
        0 & \text { if } & |x|<\tau
        \end{array}\right.
    \end{equation}

In this function, :math:`\tau` is the threshold parameter that can be set by decision maker. It is suggested to set this
parameter at a value between 0.01 and 0.05. Default value in the ``pymcdm`` is :math:`\tau = 0.02`.

**Step 7.** Calculate the assessment score of each alternative, shown as follows:

.. math::
    \begin{equation}
    \mathrm{H}_{i}=\sum_{k=1}^{n} h_{i k}
    \end{equation}

**Step 8.** Rank the alternatives according to the decreasing values of assessment (larger value of assessment score
means better alternative).

COPRAS
=======================

``COPRAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_copras`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_copras

**Step 2.** Calculate normalized decision matrix values :math:`r_{i j}`
using equation (:eq:`eq:copras_sum`).

.. math::
    \begin{equation}
        r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{m} x_{i j}}
    \end{equation}
    :label: eq:copras_sum


**Step 3.** Calculate weighted normalized decision matrix, which represents multiplication of the normalized decision
matrix elements with the appropriate weight coefficients using equation (:eq:`eq:copras_e`).

.. math::
    \begin{equation}
        v_{ij} = r_{ij} \cdot w_j
    \end{equation}
    :label: eq:copras_e

**Step 4.** Determine the sums of weighted normalized values which was calculated previously. Equation
(:eq:`eq:copras_splus`) should be used for profit criteria and equation (:eq:`eq:copras_sminus`) for cost criteria.
It is assumed, that criteria ordered in the way that first :math:`k` criteria are profit
and other are cost. However, in ``pymcdm`` criteria can be in other order, because their types are determined
based on the ``types`` list in arguments.

.. math::
    \begin{equation}
        S_{+i}=\sum_{j=1}^{k} v_{i j}
    \end{equation}
    :label: eq:copras_splus

.. math::
    \begin{equation}
        S_{-i}=\sum_{j=k+1}^{n} v_{i j}
    \end{equation}
    :label: eq:copras_sminus

where :math:`k` is the number of attributes that must be maximized. The rest of attributes from :math:`k+1` to n prefer
lower values. The :math:`S_{+i}` and :math:`S_{-i}` values show level of the goal achievement for alternatives. Higher
value of :math:`S_{+i}` means that this alternative is better and the lower value of :math:`S_{-i}` also points to
better alternative.

**Step 4.** Calculate the relative significance of alternatives using equation (:eq:`eq:copras_q`).

.. math::
    \begin{equation}
        \label{eq:copras_q}
        Q_{i}=S_{+i}+\frac{S_{-\min } \cdot \sum_{i=1}^{m} S_{-i}}{S_{-i} \cdot \sum_{i=1}^{m}\left(\frac{S_{-\min }}{S_{-i}}\right)}
    \end{equation}
    :label: eq:copras_q

**Step 5.** Final ranking is performed according :math:`U_i` values (:eq:`eq:copras_u`).

.. math::
    \begin{equation}
        U_i = \frac{Q_i}{Q^{max}_i} \cdot 100\%
    \end{equation}
    :label: eq:copras_u

Where :math:`Q^{max}_i` stands for maximum value of the utility function. Better alternatives has higher :math:`U_i`
value.

EDAS
=======================

``EDAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_edas`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_edas

**Step 2.** Calculate the average solution for each criterion according to the formula (:eq:`equ:av`).

.. math::
    \begin{equation}
    A V_{j}=\frac{\sum_{i=1}^{n} x_{i j}}{n}
    \end{equation}
    :label: equ:av

**Step 3.** Calculating the positive distance from the mean solution and the negative distance from the mean solution
for the alternatives. When the criterion is of profit type, the negative distance and the positive distance are
calculated using equations (:eq:`equ:ndapr`) and (:eq:`equ:pdapr`), while when the criterion is of cost type, the
distances are calculated using formulas (:eq:`equ:ndacs`) and (:eq:`equ:pdacs`).

.. math::
    \begin{equation}
    PDA_{i j} = \frac{\max \left(0,\left(X_{i j}-A V_{j}\right)\right)}{A V_{j}}
    \end{equation}
    :label: equ:pdapr

.. math::
    \begin{equation}
    NDA_{i j}=\frac{\max \left(0,\left(A V_{j}-X_{i j}\right)\right)}{A V_{j}}
    \end{equation}
    :label: equ:ndapr

.. math::
    \begin{equation}
    P D A_{i j}=\frac{\max \left(0,\left(A V_{j}-X_{i j}\right)\right)}{A V_{j}}
    \end{equation}
    :label: equ:pdacs

.. math::
    \begin{equation}
    N D A_{i j}=\frac{\max \left(0,\left(X_{i j}-A V_{j}\right)\right)}{A V_{j}}
    \end{equation}
    :label: equ:ndacs

**Step 4.** Calculate the weighted sums of :math:`PDA` and :math:`NDA` for each decision variant using equations
(:eq:`equ:wsp`) and (:eq:`equ:wsn`).

.. math::
    \begin{equation}
    SP_{i}=\sum_{j=1}^{m} w_{j} P D A_{i j}
    \end{equation}
    :label: equ:wsp

.. math::
    \begin{equation}
    SN_{i}=\sum_{j=1}^{m} w_{j} N D A_{i j}
    \end{equation}
    :label: equ:wsn


**Step 5.** Normalize the weighted sums of negative and positive distances using equations (:eq:`equ:normsp`) and
(:eq:`equ:normsn`).

.. math::
    \begin{equation}
    N S P_{i}=\frac{S P_{i}}{\max _{i}\left(S P_{i}\right)}
    \end{equation}
    :label: equ:normsp

.. math::
    \begin{equation}
    N S N_{i}=1-\frac{S N_{i}}{\max _{i}\left(S N_{i}\right)}
    \end{equation}
    :label: equ:normsn


**Step 6.** Calculate the evaluation score (:math:`AS`) for each alternative using the formula (:eq:`equ:as`). A higher
point value determines a higher ranking alternative.

.. math::
    \begin{equation}
    A S_{i}=\frac{1}{2}\left(N S P_{i}+N S N_{i}\right)
    \end{equation}
    :label: equ:as

ERVD
=======================
``ERVD`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_ervd`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_ervd

**Step 2.** Define reference points :math:`\mu_j` for :math:`j=1,\ldots,n` for each decision criterion
Decision makers must decide which outcomes they consider equivalent for criterion :math:`j`, set
the reference point :math:`\mu_j` and then consider lesser outcomes as losses and greater ones as gains.

**Step 3.** Normalize the decision matrix using the sum method (:eq:`equ:ervd_sum`).

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sum^m_{i=1} x_{ij}}
    \end{equation}
    :label: equ:ervd_sum

**Step 4.** Normalize the reference point with similar to the data in the matrix:

.. math::
    \begin{equation}
        \varphi_{j} = \frac{\mu_{j}}{\sum^m_{i=1} x_{ij}}
    \end{equation}

**Step 5.** Calculate the value of alternative :math:`A_i` according to criterion :math:`C_j` by increasing value function
(for benefit criteria):

.. math::
    \begin{equation}
    v_{i j}=\left\{\begin{array}{l}
    \left(r_{i j}-\varphi_j\right)^\alpha \quad \text { if } r_{i j}>\varphi_j \\
    -\lambda\left(\varphi_j-r_{i j}\right)^\alpha \text { otherwise }
    \end{array}\right.
    \end{equation}

and decreasing value function (for cost criteria):

.. math::
    \begin{equation}
    v_{i j}=\left\{\begin{array}{l}
    \left(\varphi_j-r_{i j}\right)^\alpha \quad \text { if } r_{i j}<\varphi_j \\
    -\lambda\left(r_{i j}-\varphi_j\right)^\alpha \text { otherwise }
    \end{array}\right.
    \end{equation}

**Step 6.** Determine the ideal and negative ideal solutions :math:`A^+` (PIS) and :math:`A^-` (NIS), respectively:

.. math::
    \begin{equation}
    A^{+}=\left\{v_1^{+}, \cdots v_n^{+}\right\}, A^{-}=\left\{v_1^{-}, \cdots v_n^{-}\right\}
    \end{equation}

where :math:`v_j^{+}=\max _i v_{i j}` and :math:`v_j^{-}=\min v_{i \vec{j}}`.

**Step 7.** Calculate the separation measures from PIS and NIS individually with help Minkowski metric:

.. math::
    \begin{equation}
    S_i^{+}=\sum_{j=1}^n w_j \cdot\left|v_{i j}-v_j^{+}\right|, \text {for alternative } i, i=1 \ldots m
    \end{equation}

.. math::
    \begin{equation}
    S_i^{-}=\sum_{j=1}^n w_j \cdot\left|v_{i j}-v_j^{-}\right|, \text {for alternative } i, i=1 \ldots m
    \end{equation}

**Step 8.** Calculate the relative closeness of each alternative to the ideal solution:

.. math::
    \begin{equation}
    \phi_i=\frac{S_i^{-}}{S_i^{+}+S_i^{-}}, i=1, \ldots, m
    \end{equation}

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
    \begin{equation}
    m = \left( \sum_{i=1}^{n_l} w_i \frac{Y_i}{X_i} \right)
    + \left( \sum_{i=n_l + 1}^{n_l + n_u} w_i \frac{X_i}{Y_i} \right)
    + \left( \sum_{i=n_l + n_u + 1}^{N} w_i \left| \frac{X_i}{Y_i} - 1 \right| \right)
    \end{equation}

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

MABAC
=======================
``MABAC`` is designed to evaluate decision alternatives according to the following steps:


**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat4`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat4


**Step 2.** Normalization of the decision matrix, where for criteria of type profit use equation (:eq:`equ:profitma`)
and for criteria of type cost use equation (:eq:`equ:costma`).

.. math::
    \begin{equation}
    n_{i j}=\frac{x_{i j}- \min x_{i}}{\max x_{i}- \min x_{i}}
    \end{equation}
    :label: equ:profitma

.. math::
    \begin{equation}
    n_{i j}=\frac{x_{i j}- \max x_{i}}{\min x_{i} - \max x_{i}}
    \end{equation}
    :label: equ:costma

**Step 3.** Create a weighted matrix based on the values from the normalized matrix according to the formula
(:eq:`equ:wema_mabac`).

.. math::
    \begin{equation}
    v_{i j}=w_{i} \cdot\left(n_{i j}+1\right)
    \end{equation}
    :label: equ:wema_mabac


**Step 4.** Boundary approximation area (:math:`G`) matrix determination. The Boundary Approximation Area (:math:`BAA`)
for all criteria can be determined using the formula (:eq:`equ:boundma`).

.. math::
    \begin{equation}
    g_{j}=\left(\prod_{j=1}^{m} v_{i j}\right)^{1 / m}
    \end{equation}
    :label: equ:boundma


**Step 5.** Distance calculation of alternatives from the boundary approximation area for matrix elements (:math:`Q`) by
equation (:math:`equ:qma`).

.. math::
    \begin{equation}
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
    \end{equation}
    :label: equ:qma

The membership of a given alternative :math:`A_i` to the approximation area (:math:`G`, :math:`G^{+}` or :math:`G^{-}`)
is established by (:eq:`equ:aproxma`).

.. math::
    \begin{equation}
    A_{i} \in\left\{\begin{array}{lll}
    G^{+} & \text {if } & q_{i j}>0 \\
    G & \text { if } & q_{i j}=0 \\
    G^{-} & \text {if } & q_{i j}<0
    \end{array}\right.
    \end{equation}
    :label: equ:aproxma

**Step 6.** Ranking the alternatives according to the sum of the distances of the alternatives from the areas of
approximation of the borders (:eq:`equ:sima`).

.. math::
    \begin{equation}
    S_{i}=\sum_{j=1}^{n} q_{i j}, \quad j=1,2, \ldots, n, \quad i=1,2, \ldots, m
    \end{equation}
    :label: equ:sima

MAIRCA
=======================

``MAIRCA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat3`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat3


**Step 2.** Determining the preference for choosing alternatives using the vector :math:`P_{Ai}` using the formula
(:eq:`equ:pia`). In ``pymcdm``, all criteria treated equally, with no option for providing preferences for the
alternatives (second option).

.. math::
    \begin{equation}
    P_{A i}=\frac{1}{n} ; \sum_{i=1}^{n} P_{A i}=1, i=1,2, \ldots, n
    \end{equation}
    :label: equ:pia

If the decision-maker is neutral in choosing an alternative, the vector :math:`P_{Ai}` should have the same values
(:eq:`equ:pia2`).

.. math::
    \begin{equation}
    P_{A 1}=P_{A 2}=\ldots=P_{A n}
    \end{equation}
    :label: equ:pia2


**Step 3.** Creating a theoretical ranking matrix :math:`T_p`. The elements of this matrix are the multiplied priorities
of alternatives by the criteria weights. The form of this matrix can be represented by the formula (:eq:`equ:tp`).

.. math::
    \begin{equation}
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
    \end{equation}
    :label: equ:tp

When the preferences determined for the alternatives by the decision-maker are equal, the theoretical ranking matrix is
represented by a theoretical ranking vector using the formula (:eq:`equ:tpwe`).

.. math::
    \begin{equation}
    T_p =
    \left[\begin{array}{cccc}
    t_{p 11} & t_{p 12} & \ldots & t_{p 1 n}
    \end{array}\right]=
    \left[\begin{array}{llll}
    p_{A 1} . w_{1} & p_{A 1} \cdot w_{2} & \ldots & p_{A 1} \cdot w_{n}
    \end{array}\right]
    \end{equation}
    :label: equ:tpwe


**Step 4.** Create the real rating matrix, which is shown by the formula (:eq:`equ:tr`).

.. math::
    \begin{equation}
    T_r =
    \left[\begin{array}{cccc}
    t_{r 11} & t_{r 12} & \ldots & t_{r 1 m} \\
    t_{r 21} & t_{r 22} & \ldots & t_{r 2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    t_{r n 1} & t_{r n 2} & \ldots & t_{r n m}
    \end{array}\right]
    \end{equation}
    :label: equ:tr


The values of the real rating matrix are determined depending on the criterion of profit type or cost type, sequentially
according to the formulas (:eq:`equ:trpr`) and (:eq:`equ:trcs`).

.. math::
    \begin{equation}
    \label{equ:trpr}
    t_{r i j}=t_{p i j} \cdot\left(\frac{x_{i j}-\min x_{j}}{\max x_{j}-\min x_{j}}\right)
    \end{equation}
    :label: equ:trpr

.. math::
    \begin{equation}
    \label{equ:trcs}
    t_{r i j}=t_{p i j} \cdot\left(\frac{x_{i j}-\max x_{j}}{\min x_{j}-\max x_{j}}\right)
    \end{equation}
    :label: equ:trcs

**Step 5.** Calculating the total gap matrix (:math:`G`) by taking the difference between the theoretical grade matrix
(:math:`Tp`) and the actual grade matrix (:math:`Tr`) using the formula (:eq:`equ:gap`).

.. math::
    \begin{equation}
    G=T_{p}-T_{r}= \left[\begin{array}{cccc}
    t_{p 11}-t_{r 11} & t_{p 12}-t_{r 12} & \ldots & t_{p 1 m}-t_{r 1 m} \\
    t_{p 21}-t_{r 21} & t_{p 21}-t_{r 21} & \ldots & t_{p 2 m}-t_{r 2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    t_{p n 1}-t_{r n 1} & t_{p n 2}-t_{r n 2} & \ldots & t_{p n m}-t_{r n m}
    \end{array}\right]
    \end{equation}
    :label: equ:gap

**Step 6.** Calculating the final values of the criterion functions (:math:`Q_i`) for the alternatives using the sum of
the rows of the gap matrix (:math:`G`) using the formula (:eq:`equ:qima`). The alternative with the lowest value of
:math:`Q_i` has the highest ranking.

.. math::
    \begin{equation}
    \label{equ:qima}
    Q_{i}=\sum_{j=1}^{m} g_{i j} \quad i=1,2, \ldots, n
    \end{equation}
    :label: equ:qima

MARCOS
=======================

``MARCOS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.**  Based on the decision matrix, create an augmented decision matrix with the ideal solution (AI) defined in
the last row and the anti-ideal (AAI) solution defined in the first row. This can be represented by
the Equation (:eq:`equ:extdecmat`).

.. math::
    \begin{equation}
        M = \left[\begin{array}{cccc}
                  x_{11} & x_{12} & \dots & x_{1n} \cr
                  x_{21} & x_{22} & \dots & x_{2n} \cr
                  \dots & \dots & \dots & \dots \cr
                  x_{m1} & x_{m2} & \dots & x_{mn} \cr
                  x_{ai1} & x_{ai2} & \dots & x_{ain} \cr
                  x_{aa1} & x_{aa2} & \dots & x_{aan} \cr
            \end{array}\right]
    \end{equation}
    :label: equ:extdecmat

The ideal :math:`AI` and anti-ideal :math:`AAI` solution values for the cost (C) and benefit (B) criteria are defined
as follows:

.. math::
    \begin{equation}
      AAI = \left  \{ \begin{array}{cc}
            \min_i x_{ij} &  if \quad j \in B\\
           \max_i x_{ij}  & if \quad j \in C
        \end{array} \right .
    \end{equation}
    :label: equ:aai

.. math::
    \begin{equation}
      AI = \left  \{ \begin{array}{cc}
            \max_i x_{ij} &  if \quad j \in B\\
           \min_i x_{ij}  & if \quad j \in C
        \end{array} \right .
    \end{equation}
    :label: equ:ai

**Step 2.** Normalization of the extended decision matrix using Equation (:eq:`equ:normext`).

.. math::
    \begin{equation}
        n_{ij} = \left  \{
        \begin{array}{cc}
         \frac{x_{ai}}{x_{ij}} & if \quad j \in C \\
         \frac{x_{x_{ij}}}{x_{ai}} & if \quad j \in B
        \end{array}\right .
    \end{equation}
    :label: equ:normext

**Step 3.** Create a weighted matrix based on the values from the normalized extended matrix according to the formula
(:eq:`equ:wema`).

.. math::
    \begin{equation}
    v_{i j}=w_{i} \cdot\left(n_{i j}+1\right)
    \end{equation}
    :label: equ:wema


**Step 4.** Calculating the degrees of utility of alternatives :math:`K_i` relative to the ideal and anti-ideal
solution using Equations (:eq:`equ:kiplu`), (:eq:`equ:kimin`).


.. math::
    \begin{equation}
        K_{i}^{+} = \frac{S_i}{S_{ai}}
    \end{equation}
    :label: equ:kiplu

.. math::
    \begin{equation}
        K_{i}^{-} = \frac{S_i}{S_{aai}}
    \end{equation}
    :label: equ:kimin

where :math:`S_i` :math:`(i=1,2,\dots,m)` represents the sum of the elements of weighted matrix :math:`V`, Equation
(:eq:`equ:summ`).

.. math::
    \begin{equation}
        S_i = \sum_{i=1}^n v_{ij}
    \end{equation}
    :label: equ:summ

**Step 5.** Determination of the utility function for the decision options considered according to (:eq:`equ:utilll`).

.. math::
    \begin{equation}
    f\left(K_{i}\right)=\frac{K_{i}^{+}+K_{i}^{-}}{1+\frac{1-f\left(K_{i}^{+}\right)}{f\left(K_{i}^{+}\right)}+\frac{1-f\left(K_{i}^{-}\right)}{f\left(K_{i}^{-}\right)}}
    \end{equation}
    :label: equ:utilll

where :math:`f(K_{i}^{-})` denotes the utility function relative to the anti-ideal solution, while
:math:`f(K_{i}^{+})` denotes the utility function relative to the ideal solution, which can be determined using
the Equations respectively (:eq:`equ:kmf`) and (:eq:`equ:kpf`).

.. math::
    \begin{equation}
    f\left(K_{i}^{-}\right)=\frac{K_{i}^{+}}{K_{i}^{+}+K_{i}^{-}}
    \end{equation}
    :label: equ:kmf

.. math::
    \begin{equation}
    f\left(K_{i}^{+}\right)=\frac{K_{i}^{-}}{K_{i}^{+}+K_{i}^{-}}
    \end{equation}
    :label: equ:kpf

Note, that alternatives with smaller values of :math:`f(K_i)` are determined as better alternatives.

MOORA
=======================

``MOORA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_moora`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_moora

**Step 2.** Normalize the decision matrix based on the Equation (:eq:`normm`).

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m}{x_{ij}^2}}}
    \end{equation}
    :label: normm

where :math:`x_{ij}` can be called the value of the :math:`i-th` alternative for the :math:`j-th` criterion.

**Step 3.** Determine weighted normalized decision matrix based on Equation (:eq:`weigh`).

.. math::
    \begin{equation}
        v_{ij} =  r_{ij} w_{j}
    \end{equation}
    :label: weigh

where :math:`w_j` can be called the weight for :math:`j-th` criterion.

**Step 4.** Calculate the value of :math:`P_i` based on the values from the normalized weighted decision matrix :math:`v_{ij}`
by using Equation (:eq:`yii`).

.. math::
    \begin{equation}
        P_i = \sum_{j=1}^g v_{ij} - \sum_{j=g+1}^n v_{ij}
    \end{equation}
    :label: yii

where type of beneficial and cost criteria are represented as
follows :math:`j = 1, 2, \dots, g` and :math:`j = g + 1, g + 2,\dots,n`.

Higher values of :math:`P_i` corresponds to better alternatives.

OCRA
=======================

``OCRA`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_ocra`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_ocra

**Step 2.** Normalize the decision matrix based on the Equation (:eq:`norm_ocra`) for the cost criteria (assuming
that there is :math:`g` cost criteria) and (:eq:`norm_ocra2`) for the profit criteria.

.. math::
    \begin{equation}
        \overline{I}_i = \sum_{j=1}^{g} w_j \frac{\max(x_{ij}) - x_{ij}}{\min(x_{ij})} \quad (i = 1, 2, \ldots, m; \, j = 1, 2, \ldots, g)
    \end{equation}
    :label: norm_ocra

.. math::
    \begin{equation}
        \overline{O}_i = \sum_{j=g+1}^{n} w_j \frac{x_{ij} - \min(x_{ij})}{\min(x_{ij})} \quad (i = 1, 2, \ldots, m; \, j = g+1, g+2, \ldots, n)
    \end{equation}
    :label: norm_ocra2

**Step 4.** Determination of preferences for cost-type and profit-type criteria sequentially according to the Equations
(:eq:`costI`),(:eq:`profO`).

.. math::
    \begin{equation}
    \overline{\overline{I}}_{i}=\overline{I}_{i}-\min \left(\overline{I}_{i}\right)
    \end{equation}
    :label: costI

.. math::
    \begin{equation}
    \overline{\overline{O_{i}}}={\overline{O_{i}}} \min \left(\overline{O}_{i}\right)
    \end{equation}
    :label: profO

where :math:`\overline{I}_{i}` is a measure of relative performance for the :math:`i-th` alternative and cost-type criteria,
and :math:`\overline{O}_{i}` is a measure of of relative performance for the :math:`i-th` alternative and profit-type criteria.

**Step 5.** Determine the overall preference of the considered alternatives using the Equation (:eq:`ocrapref`).

.. math::
    \begin{equation}
    P_i = \overline{\overline{I}}_{i} + \overline{\overline{O_{i}}} - \min \left ( \overline{\overline{I}}_{i} + \overline{\overline{O_{i}}}\right )
    \end{equation}
    :label: ocrapref

Alternatives with the highest overall performance rating receives the first rank.

PROBID
=======================

``PROBID`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat_probid`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_probid

**Step 2.** Normalize the decision matrix using the vector method.

.. math::
    \begin{equation}
    r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^{n} x_{kj}^2}} \quad i \in \{1, 2, \ldots, n\}; \, j \in \{1, 2, \ldots, m\}
    \end{equation}

**Step 3.** Create normalized weighted decision matrix.

.. math::
    \begin{equation}
        v_{ij} =  r_{ij} w_{j}
    \end{equation}

**Step 4.** Sort the normalized weighted decision matrix by criteria taking into account their type. This will a matrix
of successively Positive Ideal Solutions (1st, 2nd, ..., mth PIS) will be formed. It can be presented by using the
following formula:

.. math::
    \begin{equation}
    \begin{aligned}
    A_{(k)} & =\left\{\left(\operatorname{Large}\left(v_j, k\right) \mid j \in J\right),\left(\operatorname{Small}\left(v_j, k\right) \mid j \in J^{\prime}\right)\right\} \\
    & =\left\{v_{(k) 1}, v_{(k) 2}, v_{(k) 3}, \ldots, v_{(k) j}, \ldots, v_{(k) n}\right\}
    \end{aligned}
    \end{equation}

where :math:`k \in \{1,2, \ldots, n\}`, :math:`J` is the set of benefit criteria and :math:`J^{\prime}` is the set of cost
criteria.

Then, find the average value of each objective column as follow:

.. math::
    \begin{equation}
    \bar{v}_j=\frac{\sum_{k=1}^n v_{(k) j}}{n} \quad \text { for } j \in\{1,2, \ldots, m\}
    \end{equation}

The average solution is then given by

.. math::
    \begin{equation}
    \bar{A}=\left\{\bar{v}_1, \bar{v}_2, \bar{v}_3, \ldots, \bar{v}_j, \ldots, \bar{v}_m\right\}
    \end{equation}

**Step 5.** Iteratively calculate the Euclidean distance of each solution to each of the m ideal solutions as well as to
the average solution. The distance to ideal solutions is found as:

.. math::
    \begin{equation}
    S_{i(k)}=\sqrt{\sum_{j=1}^m\left(v_{i j}-v_{(k) j}\right)^2}
    \end{equation}

**Step 6.** Determine the overall positive-ideal distance and negative-ideal distance as follow:

.. math::
    \begin{equation}
    S_{i(\text { pos-ideal })}=\left\{\begin{array}{l}
    \sum_{k=1}^{(n+1) / 2} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \\
    \text { is an odd number } \\
    \sum_{k=1}^{n / 2} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \\
    \text { is an even number }
    \end{array}\right.
    \end{equation}

.. math::
    \begin{equation}
    S_{i(\text { neg-ideal })}
    \quad=\left\{\begin{array}{l}
    \sum_{k=(n+1) / 2}^n \frac{1}{n-k+1} S_{i(k)} \\
    i \in\{1,2, \ldots, n\} \text { when } n \text { is an odd number } \\
    \sum_{k=n / 2+1}^n \frac{1}{n-k+1} S_{i(k)} \\
    i \in\{1,2, \ldots, n\} \text { when } n \text { is an even number }
    \end{array}\right.
    \end{equation}

There is also simplified provedure for calculating overall positive-ideal and negative-ideal distances.
In this case, the method is called sPROBID and the procedure is as follows:

.. math::
    \begin{equation}
    S_{i(\text { pos-ideal })}=\left\{\begin{array}{l}
    \sum_{k=1}^{n \backslash 4} \frac{1}{k} S_{i(k)} \quad i \in\{1,2, \ldots, n\} \text { when } n \geq 4 \\
    S_{i(1)} \quad i \in\{1,2, \ldots, n\} \text { when } 0<n<4
    \end{array}\right.
    \end{equation}

.. math::
    \begin{equation}
    S_{i(\text { neg-ideal })}=\left\{\begin{array}{l}
    \sum_{k=n+1-(n \ 4)}^n \frac{1}{n-k+1} S_{i(k)} \\
    \quad i \in\{1,2, \ldots, n\} \text { when } n \geq 4 \\
    S_{i(n)} \quad i \in\{1,2, \ldots, n\} \text { when } 0<n<4
    \end{array}\right.
    \end{equation}

**Step 7.** Calculate the pos-ideal/neg-ideal ratio (:math:`R_i`) and then the performance score (:math:`P_i`) of each
solution as follows:

.. math::
    \begin{equation}
    R_i=\frac{S_{i(\text { pos-ideal })}}{S_{i(\text { neg-ideal })}}
    \end{equation}

.. math::
    \begin{equation}
    P_i=\frac{1}{1+R_i^2}+S_{i(\mathrm{avg})}
    \end{equation}

Alternatives with the highest preference value receives the first rank.

RAM
=======================

``RAM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_ram`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_ram

**Step 2.** Calculate normalized decision matrix values :math:`r_{i j}`
using equation (:eq:`eq:ram_sum`).

.. math::
    \begin{equation}
        r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{n} x_{i j}}
    \end{equation}
    :label: eq:ram_sum


**Step 3.** Calculate weighted normalized decision matrix, which represents multiplication of the normalized decision
matrix elements with the appropriate weight coefficients using equation (:eq:`eq:ram_e`).

.. math::
    \begin{equation}
        v_{ij} = r_{ij} \cdot w_j
    \end{equation}
    :label: eq:ram_e

**Step 4.** Calculate the sums of weighted normalized scores of beneficial (:math:`+i`) and cost (:math:`-i`) criteria
of :math:`i-th` alternative by the following equations:

.. math::
    \begin{equation}
    S_{+i} = \sum^{m}_{j=1} v_{+ij}
    \end{equation}

.. math::
    \begin{equation}
    S_{-i} = \sum^{m}_{j=1} v_{-ij}
    \end{equation}

**Step 5.** Determine the overall score of each alternative using the following aggreating function:

.. math::
    \begin{equation}
    RI_{i} = \sqrt[{2 + S_{-i}}]{2 + S_{+i}}
    \end{equation}

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
    \begin{equation}
    f(x,[A, B],[C, D]) = \left\{\begin{array}{lll}
    1 &\textit{IF}& x \in[C, D] \\
    1-\frac{d_{\min }(x,[C, D])}{|A-C|} &\textit{IF}& x \in[A, C] \wedge A \neq C \\
    1-\frac{d_{\min }(x,[C, D])}{|D-B|} &\textit{IF}& x \in[D, B] \wedge D \neq B
    \end{array}\right.,
    \end{equation}
    :label: eq:rmnorm

where :math:`[A, B]` is range of criteria, :math:`[C, D]` is the reference ideal, and :math:`x \in [A, B]`, :math:`[C, D] \subset [A, B]`. Function :math:`d_{min}(x, [C, D])` is defined as (:eq:`eq:d_min`).

.. math::
    \begin{equation}
        d_{min}(x, [C, D]) = min(|x - C|, |x - D|)
    \end{equation}
    :label: eq:d_min

This normalization allows to map value :math:`x` to range :math:`[0, 1]` in the criteria domain with regard to the ideal reference interval. The normalization process is defined as follows (:eq:`eq:rim_nmatrix`).

.. math::
    \begin{equation}
    Y = [ y_{ij} ]_{M \times N} = [ f(x_{ij}, t_j, s_j) ]_{M \times N}
    \end{equation}
    :label: eq:rim_nmatrix

**Step 3.** Calculate the weighted normalized matrix :math:`Y^\prime` using (:eq:`eq:rim_wnmatrix`).

.. math::
    \begin{equation}
        Y^\prime = [ y_{ij}^{\prime} ] = Y \otimes W = [ y_{ij} \cdot w_{j} ]_{M \times N}
    \end{equation}
    :label: eq:rim_wnmatrix

**Step 4.** Compute the variation to the normalized reference ideal for each alternative :math:`A_i` using Equations (:eq:`eq:rim_iplus`) and (:eq:`eq:rim_iminus`).

.. math::
    \begin{equation}
        I_i^{+}=\sqrt{\sum_{j=1}^n\left(y^{\prime}{ }_{i j}-w_j\right)^2}% \quad i \in \{1, 2, \ldots M\}, \quad j \in \{1, 2, \ldots N\}
    \end{equation}
    :label: eq:rim_iplus

.. math::
    \begin{equation}
        I_i^{-}=\sqrt{\sum_{j=1}^n\left(y^{\prime}\right)^2}% \quad i \in \{1, 2, \ldots M\}, \quad j \in \{1, 2, \ldots N\}
    \end{equation}
    :label: eq:rim_iminus

**Step 5.** Calculate the relative index of each alternative :math:`A_i`, using the Equation (:eq:`eq:rim_r`).

.. math::
    \begin{equation}
        P_i = \frac{I_i^-}{I_i^+ + I_i^-} %\quad i \in \{1, 2, \ldots M\}
    \end{equation}
    :label: eq:rim_r

Order the alternative :math:`A_i` in descending order with regard to :math:`P_i`. The alternatives with the bigger value
of :math:`P_i` are more preferred ones.


SPOTIS
=======================

``SPOTIS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_spotis`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_spotis

**Step 2.** Define the bounds of the problem - min and max bounds of classical MCDM problem must be defined to transform
MCDM problem form ill-defined to well-defined.

.. math::
    \begin{equation}
    \left[S_{j}^{\min }, S_{j}^{\max }\right], j \in \{1, 2, \ldots, m\}
    \end{equation}

where, :math:`n` - criterion number, :math:`x_1` - min bound, :math:`x_2` - max bound.

**Step 3.** Define the ideal solution point - define vector which includes maximum or minimum from bounds for specific
criterion depending on criterion type. For profit type, the max value should be taken, for cost type, min value.

.. math::
    \begin{equation}
    S^{\star}_{j}=\begin{cases}
        S_{j}^{\min} & \text{if j-th criterion is cost}\\
        S_{j}^{\max} & \text{if j-th criterion is profit}
    \end{cases}
    \end{equation}

**Step 4.** Compute normalized distance matrix - for each alternative :math:`A_{i}` (i= 1, :math:`\ldots` , M),compute
its normalized distance with respect to ideal solution for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ).

.. math::
    \begin{equation}
    d_{i j}=\frac{\left|A_{i j}-S_{j}^{*}\right|}{\left|S_{j}^{\max }-S_{j}^{\min }\right|}
    \end{equation}

**Step 5.** Compute normalized averaged distance - for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ) take into
account its weight and calculate final preference by executing following Equation.

.. math::
    \begin{equation}
    P_{i}=\sum_{j=1}^{N} w_{j} d_{i j}
    \end{equation}

As the :math:`P_i` value is interpreted as distance from the ideal or expected solution, alternatives with smaller
value of :math:`P_i` are preferred.

TOPSIS
=======================

``TOPSIS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_topsis`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_topsis

**Step 2.** Normalize the decision matrix by using min-max normalization. The values of benefit type criteria are
normalized using the (:eq:`sumProfit`) formula, while the values of cost type criteria are normalized using the
(:eq:`sumCost`) formula.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)}\
    \end{equation}
    :label: sumProfit

.. math::
    \begin{equation}
        r_{ij} = \frac{\max(x_j) - x_{ij}}{\max(x_j) - \min(x_j)}
    \end{equation}
    :label: sumCost

**Step 3.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weightedsds`).

.. math::
    \begin{equation}
        v_{ij} = w_{j}r_{ij}
    \end{equation}
    :label: weightedsds

**Step 4.** Derive a positive ideal solution :math:`PIS` and a negative ideal solution :math:`NIS`. The ideal positive
solution is calculated as the maximum value for each criterion (:eq:`pis`), while the ideal negative solution is
calculated as the least value for each criterion (:eq:`nis`).

.. math::
    \begin{equation}
        v_{j}^{+} =  \{v_{1}^{+},  v_{2}^{+},  \dots,  v_{m}^{+} \} = \{\max_{j}(v_{ij}) \}
    \end{equation}
    :label: pis

.. math::
    \begin{equation}
        v_{j}^{-} = \{v_{1}^{-},  v_{2}^{-},  \dots,  v_{m}^{-} \}=  \{\min_{j}(v_{ij}) \}
    \end{equation}
    :label: nis

**Step 5.** Determine the Euclidean distance for each normalized weighted alternative from the :math:`PIS` (:eq:`sqrtPIS`)
and :math:`NIS` (:eq:`sqrtNIS`) solution.

.. math::
    \begin{equation}
        D_{i}^{+} = \sqrt{\sum_{j=1}^{m}(v_{ij}-v_{j}^{+})^{2}}
    \end{equation}
    :label: sqrtPIS

.. math::
    \begin{equation}
        D_{i}^{-} = \sqrt{\sum_{j=1}^{m}(v_{ij}-v_{j}^{-})^{2}}
    \end{equation}
    :label: sqrtNIS

**Step 6.** Calculate final preference value according to the Equation:

.. math::
    \begin{equation}
        P_i = \frac{D^{-}_{i}}{D^{-}_{i} + D^{+}_{i}}
    \end{equation}

Alternative with the highest value of :math:`P_i` considered the best.

VIKOR
=======================

``VIKOR`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_vikor`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_vikor

**Step 2.** Determinate the best :math:`f_{j}^{*}` and the worst :math:`f_{j}^{-}` value for the function of a particular
criterion. For profit criteria, the Equation is used (:eq:`VikorBestProfit`).

.. math::
    \begin{equation}
        f_{j}^{*} = \max_i x_{ij},\; \; \;  f_{j}^{-} = \min_i x_{ij}
    \end{equation}
    :label: VikorBestProfit

where in the case of the cost criteria, the following Equation is used (:eq:`VikorBestCost`).

.. math::
    \begin{equation}
        f_{j}^{*} = \min_i x_{ij},\; \; \;  f_{j}^{-} = \max_i x_{ij}
    \end{equation}
    :label: VikorBestCost

**Step 3.** Calculate :math:`S_{i}` and :math:`R_{i}` with using Equations (:eq:`VikorSi`) and (:eq:`VikorRi`).

.. math::
    \begin{equation}
        S_{i} = \sum_{j=1}^{m}w_{j}(f_{j}^{*}-x_{ij})/(f_{j}^{*}-f_{j}^{-})
    \end{equation}
    :label: VikorSi

.. math::
    \begin{equation}
        R_{i} = \max_j \left [w_{j}(f_{j}^{*}-x_{ij})/(f_{j}^{*}-f_{j}^{-}) \right ]
    \end{equation}
    :label: VikorRi

**Step 4.** Calculate :math:`Q_{i}` with using Equation (:eq:`VikorQi`).

.. math::
    \begin{equation}
        Q_{i} = v(S_{i}-S^{*}) / (S^{-}-S^{*}) + (1 - v)(R_{i}-R^{*}) / (R^{-}-R^{*}) \label{VikorQi}
    \end{equation}
    :label: VikorQi

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

WASPAS
=======================

``WASPAS`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_waspas`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_waspas

**Step 2.** Normalize the decision matrix using the linear normalization method, according to:

.. math::
    \begin{equation}
    r_{ij} = \frac{x_{ij}}{\max_i x_{ij}}, \text{if j-th criterion is profit}
    \end{equation}

.. math::
    \begin{equation}
    r_{ij} = \frac{\min x_{ij}}{x_{ij}}, \text{if j-th criterion is cost}
    \end{equation}


**Step 3.** Calculate WSM and WPM as follow:

.. math::
    \begin{equation}
    W S M=\sum_{j=1}^n r_{i j} w_j
    \end{equation}

.. math::
    \begin{equation}
    W P M=\prod_{j=1}^n\left(r_{i j}\right)^{w_j}
    \end{equation}

where :math:`w_j` denote the weights for the criteria, and :math:`r_ij` denote the values of the decision options from
the normalized decision matrix.

**Step 4.** Calculation of total relative importance for each alternative as follow:

.. math::
    \begin{equation}
    Q_i=\lambda WSM+(1-\lambda) WPM=\lambda \sum_{j=1}^n r_{i j} w_j+(1-\lambda) \prod_{j=1}^n\left(r_{i j}\right)^{w_j}
    \end{equation}

Higher values of :math:`Q_i` points to better alternatives.


WPM
=======================

``WPM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_wpm`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_wpm

**Step 2.** Normalize the decision matrix using the sum method.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sum_m^{i=1}x_{ij}}, \text{if j-th criterion is profit}
    \end{equation}

.. math::
    \begin{equation}
        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=1}\frac{1}{x_{ij}}}, \text{if j-th criterion is cost}
    \end{equation}

**Step 3.** Calculate WPM as follow:

.. math::
    \begin{equation}
    W P M=\prod_{j=1}^n\left(r_{i j}\right)^{w_j}
    \end{equation}

where :math:`w_j` denote the weights for the criteria, and :math:`x_{ij}` denote the values of the decision options from
the normalized decision matrix.

WSM
=======================

``WSM`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat_wsm`).

.. math::
    \begin{equation}
    X = [x_{i j}]=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat_wsm

**Step 2.** Normalize the decision matrix using the sum method.

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sum_m^{i=1}x_{ij}}, \text{if j-th criterion is profit}
    \end{equation}

.. math::
    \begin{equation}
        r_{ij} = \frac{\frac{1}{x_{ij}}}{\sum_m^{i=1}\frac{1}{x_{ij}}}, \text{if j-th criterion is cost}
    \end{equation}

**Step 3.** Calculate WSM as follow:

.. math::
    \begin{equation}
    W S M=\sum_{j=1}^n r_{i j} w_j
    \end{equation}

where :math:`w_j` denote the weights for the criteria, and :math:`x_{ij}` denote the values of the decision options from
the normalized decision matrix.
