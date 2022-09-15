.. _american_school:

=============
American school
=============



ARAS
=======================

:class:`ARAS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat`).

.. math::
    \begin{equation}
    x_{i j}=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profita`), and for
cost, criteria use the equation (:eq:`equ:costa`). In this study, The Sum normalization method was used.

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

**Step 3.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weighted`).

.. math::
    \begin{equation}
        v_{ij} = w_{j}r_{ij} \label{weighted}
    \end{equation}
    :label: weighted

**Step 4.** Determining values of optimality function using the Equation (:eq:`opf`).


.. math::
    \begin{equation}
        S_i = \sum_{j=1}^{n} v_{ij}
    \end{equation}
    :label: opf

**Step 5.** Calculate the utility degree :math:`K_i` based on Equation (:eq:`ud`).

.. math::
    \begin{equation}
        K_i = \frac{S_i}{S_0}
    \end{equation}
    :label: ud

where :math:`S_i` and :math:`S_0` are the optimality criterion values.


COCOSO
=======================

:class:`COCOSO` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat`).

.. math::
    \begin{equation}
    x_{i j}=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat



**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profit`), and for
cost, criteria use the equation (:eq:`equ:cost`). In this study, The Minimum-Maximum normalization method was used.

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
In this study, a :math:`\lambda` value of 0.5 was used.

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
(:eq:`equ:ki`). The higher the :math:`k_i` value, the higher the ranking.

.. math::
    \begin{equation}
    k_{i}=\left(k_{i a} k_{i b} k_{i c}\right)^{\frac{1}{3}}+\frac{1}{3}\left(k_{i a}+k_{i b}+k_{i c}\right)
    \end{equation}
    :label: equ:ki

CODAS
=======================

:class:`CODAS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Definition of a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of
alternatives, and :math:`m` is the number of criteria (:eq:`equ:mat`).

.. math::
    \begin{equation}
    x_{i j}=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat

**Step 2.** Normalization the decision matrix, where for profit criteria use the equation (:eq:`equ:profitc`), and for
cost, criteria use the equation (:eq:`equ:costc`). In this study, The Linear normalization method was used.

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

**Step 5.** Calculate the Euclidean and Taxicab distances of alternatives from the negative-ideal solution, shown as
follows:

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

where :math:`k \in \left \{ 1,2,\cdots,n \right \}` and :math:`psi` denotes a threshold function to recognize the
equality of the Euclidean distances of two alternatives, and is defined as follows:

.. math::
    \begin{equation}
        \psi(x)=\left\{\begin{array}{lll}
        1 & \text { if } & |x| \geq \tau \\
        0 & \text { if } & |x|<\tau
        \end{array}\right.
    \end{equation}

In this function, :math:`\tau` is the threshold parameter that can be set by decisionmaker. It is suggested to set this
parameter at a value between 0.01 and 0.05.

**Step 7.** Calculate the assessment score of each alternative, shown as follows:

.. math::
    \begin{equation}
    \mathrm{H}_{i}=\sum_{k=1}^{n} h_{i k}
    \end{equation}

**Step 8.** Rank the alternatives according to the decreasing values of assessment.

COPRAS
=======================

:class:`COPRAS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Calculate normalized decision matrix using equation (:eq:`eq:copras_sum`).

.. math::
    \begin{equation}
        r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{m} x_{i j}}
    \end{equation}
    :label: eq:copras_sum


**Step 2.** Calculate difficult normalized decision matrix, which represents multiplication of the normalized decision
matrix elements with the appropriate weight coefficients using equation (:eq:`eq:copras_e`).

.. math::
    \begin{equation}
        v_{ij} = r_{ij} \cdot w_j
    \end{equation}
    :label: eq:copras_e

**Step 3.** Determine the sums of difficult normalized values which was calculated previously. Equation
(:eq:`eq:copras_splus`) should be used for profit criteria and equation (:eq:`eq:copras_sminus`) for cost criteria.

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

:class:`EDAS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat2`).

.. math::
    \begin{equation}
    X_{i j}=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat2

**Step 2.** Calculate the average solution for each criterion according to the formula (:eq:`equ:av`).

.. math::
    \begin{equation}
    A V_{j}=\frac{\sum_{i=1}^{n} X_{i j}}{n}
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
    \mathrm{A} SP_{i}=\sum_{j=1}^{m} w_{j} P D A_{i j}
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

MABAC
=======================
:class:`MABAC` is designed to evaluate decision alternatives according to the following steps:


**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat4`).

.. math::
    \begin{equation}
    x_{i j}=\left[\begin{array}{llll}
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
(:eq:`equ:wema`).

.. math::
    \begin{equation}
    v_{i j}=w_{i} \cdot\left(n_{i j}+1\right)
    \end{equation}
    :label: equ:wema


**Step 4.** Boundary approximation area (:math:`G`) matrix determination. The Boundary Approximation Area (:math:`BAA`)
for all criteria can be determined using the formula (:eq:`equ:boundma`).

.. math::
    \begin{equation}
    g_{i}=\left(\prod_{j=1}^{m} v_{i j}\right)^{1 / m}
    \end{equation}
    :label: equ:boundma


**Step 5.** Distance calculation of alternatives from the boundary approximation area for matrix elements (:math:`Q`) by
equation (:math:`equ:qma`).

.. math::
    \begin{equation}
    Q=\left[\begin{array}{cccc}
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

:class:`MAIRCA` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define a decision matrix of dimension :math:`n \times m`, where :math:`n` is the number of alternatives,
and :math:`m` is the number of criteria (:eq:`equ:mat3`).

.. math::
    \begin{equation}
    x_{i j}=\left[\begin{array}{llll}
    x_{11} & x_{12} & \ldots & x_{1 m} \\
    x_{21} & x_{22} & \ldots & x_{2 m} \\
    \ldots & \ldots & \ldots & \ldots \\
    x_{n 1} & x_{n 2} & \ldots & x_{n m}
    \end{array}\right]
    \end{equation}
    :label: equ:mat3


**Step 2.** Determining the preference for choosing alternatives using the vector :math:`P_{Ai}` using the formula
(:eq:`equ:pia`).

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

:class:`MARCOS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.**  Based on the decision matrix, create an augmented decision matrix with the ideal solution (AI) defined in
the last row and the anti-ideal (AAI) solution defined in the first row. This can be represented by the Equation (:eq:`equ:extdecmat`).

.. math::
    \begin{equation}
        M = \left[\begin{array}{cccc}
                  x_{aa1} & x_{aa2} & \dots & x_{aan} \cr
                   x_{11} & x_{12} & \dots & x_{1n} \cr
                  x_{21} & x_{22} & \dots & x_{2n} \cr
                   \dots & \dots & \dots & \dots \cr
                   x_{m1} & x_{m2} & \dots & x_{mn} \cr
                   x_{ai1} & x_{ai2} & \dots & x_{ain} \end{array}\right]
    \end{equation}
    :label: equ:extdecmat

The ideal and anti-ideal solution values for the cost (C) and benefit (B) criteria are defined as follows:

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


**Step 4.** Calculating the degrees of utility of alternatives Ki relative to the ideal and anti-ideal solution using
Equations (:eq:`equ:kiplu`), (:eq:`equ:kimin`).


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

where :math:`S_i` :math:`(i=1,2,\dots,m)` represents the sum of the elements of weighted matrix $V$, Equation
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

MOORA
=======================

:class:`MOORA` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Normalize the decision matrix based on the Equation (:eq:`normm`).

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m}{x_{ij}^2}}}
    \end{equation}
    :label: normm

where :math:`x_{ij}` can be called the value of the :math:`i-th` alternative for the :math:`j-th` criterion.

**Step 2.** Determine weighted normalized decision matrix based on Equation (:eq:`weigh`).

.. math::
    \begin{equation}
        v_{ij} =  r_{ij} w_{j}
    \end{equation}
    :label: weigh

where :math:`w_j` can be called the weight for :math:`j-th` criterion.

**Step 3.** Calculate the value of :math:`y_i` based on the values from the normalized weighted decision matrix :math:`v_{ij}`
by using Equation (:eq:`yii`).

.. math::
    \begin{equation}
        y_i = \sum_{j=1}^g v_{ij} - \sum_{j=g+1}^n v_{ij}
    \end{equation}
    :label: yii

where type of beneficial and cost criteria are represented as follows :math:`j = 1, 2, \dots, g` and :math:`j = g + 1, g + 2,\dots,n`.

OCRA
=======================

:class:`OCRA` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Create a decision matrix.

**Step 2.** Normalize the decision matrix using the min-max method.

**Step 3.** Create normalized weighted decision matrix.

**Step 4.** Determination of preferences for cost-type and profit-type criteria sequentially according to the Equations
(:eq:`costI`),(:eq:`profO`).

.. math::
    \begin{equation}
    \overline{\bar{I}}_{i}=\bar{I}_{i}-\min \left(\bar{I}_{i}\right)
    \end{equation}
    :label: costI

.. math::
    \begin{equation}
    \overline{\overline{O_{i}}}={\overline{O_{i}}}^{-} \min \left(\bar{O}_{i}\right)
    \end{equation}
    :label: profO

where :math:`\bar{I}_{i}` is a measure of relative performance for the :math:`i-th` alternative and cost-type criteria,
and :math:`\bar{O}_{i}` is a measure of of relative performance for the :math:`i-th` alternative and profit-type criteria.

**Step 5.** Determine the overall preference of the considered alternatives using the Equation (:eq:`ocrapref`).

.. math::
    \begin{equation}
    P_i = \overline{\bar{I}}_{i} + \overline{\overline{O_{i}}} - \min \left ( \overline{\bar{I}}_{i} + \overline{\overline{O_{i}}}\right )
    \end{equation}
    :label: ocrapref


SPOTIS
=======================

:class:`SPOTIS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Define the bounds of the problem - min and max bounds of classical MCDM problem must be defined to transform
MCDM problem form ill-defined to well-defined.

.. math::
    \begin{equation}
    \left[S_{n}^{\min }, S_{n}^{\max }\right]=\left[x_{1}, x_{2}\right]
    \end{equation}

where, $n$ - criterion number, $x_1$ - min bound, $x_2$ - max bound.

**Step 2.** Define the ideal solution point - define vector which includes maximum or minimum from bounds for specific
criterion depending on criterion type. For profit type, the max value should be taken, for cost type, min value.

.. math::
    \begin{equation}
    S^{\star}=\left(S_{1}^{\star}, S_{2}^{\star}, S_{3}^{\star}\right)
    \end{equation}

**Step 3.** Compute normalized distance matrix - for each alternative :math:`A_{i}` (i= 1, :math:`\ldots` , M),compute
its normalized distance with respect to ideal solution for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ).

.. math::
    \begin{equation}
    d_{i j}=\frac{\left|A_{i j}-S_{j}^{*}\right|}{\left|S_{j}^{\max }-S_{j}^{\min }\right|}
    \end{equation}

**Step 4.** Compute normalized averaged distance - for each criteria :math:`C_{j}` (j= 1, :math:`\ldots` , N ) take into
account its weight and calculate final preference by executing following Equation.

.. math::
    \begin{equation}
    \bar{p}_{j}=\sum_{j=1}^{N} w_{j} d_{i j}
    \end{equation}

TOPSIS
=======================

:class:`TOPSIS` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Normalize the decision matrix by using min-max normalization. The values of benefit type criteria are
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

**Step 2.** Building a decision matrix :math:`v_{ij}` subjected to a weighting and normalization process using the
Equation (:eq:`weightedsds`).

.. math::
    \begin{equation}
        v_{ij} = w_{j}r_{ij}
    \end{equation}
    :label: weightedsds

**Step 3.** Derive a positive ideal solution :math:`PIS` and a negative ideal solution :math:`NIS`. The ideal positive
solution is calculated as the maximum value for each criterion (:eq:`pis`), while the ideal negative solution is
calculated as the least value for each criterion (:eq:`nis`).

.. math::
    \begin{equation}
        v_{j}^{+} =  \{v_{1}^{+},  v_{2}^{+},  \dots,  v_{n}^{+} \} = \{\max_{j}(v_{ij}) \}
    \end{equation}
    :label: pis

.. math::
    \begin{equation}
        v_{j}^{-} = \{v_{1}^{-},  v_{2}^{-},  \dots,  v_{n}^{-} \}=  \{\min_{j}(v_{ij}) \}
    \end{equation}
    :label: nis

**Step 4.** Determine the Euclidean distance for each normalized weighted alternative from the :math:`PIS` (:eq:`sqrtPIS`)
and :math:`NIS` (:eq:`sqrtNIS`) solution.

.. math::
    \begin{equation}
        D_{i}^{+} = \sqrt{\sum_{j=1}^{n}(v_{ij}-v_{j}^{+})^{2}}
    \end{equation}
    :label: sqrtPIS

.. math::
    \begin{equation}
        D_{i}^{-} = \sqrt{\sum_{j=1}^{n}(v_{ij}-v_{j}^{-})^{2}}
    \end{equation}
    :label: sqrtNIS

VIKOR
=======================

:class:`VIKOR` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** Determinate the best :math:`f_{j}^{*}` and the worst :math:`f_{j}^{-}` value for the function of a particular
criterion. For profit criteria, the Equation is used (:eq:`VikorBestProfit`).

.. math::
    \begin{equation}
        f_{j}^{*} = \max_i f_{ij},\; \; \;  f_{j}^{-} = \min_i f_{ij}
    \end{equation}
    :label: VikorBestProfit

where in the case of the cost criteria, the following Equation is used (:eq:`VikorBestCost`).

.. math::
    \begin{equation}
        f_{j}^{*} = \min_i f_{ij},\; \; \;  f_{j}^{-} = \max_i f_{ij}
    \end{equation}
    :label: VikorBestCost

**Step 2.** Calculate :math:`S_{i}` and :math:`R_{i}` with using Equations (:eq:`VikorSi`) and (:eq:`VikorRi`).

.. math::
    \begin{equation}
        S_{i} = \sum_{j=1}^{n}w_{j}(f_{j}^{*}-f_{ij})/(f_{j}^{*}-f_{j}^{-})
    \end{equation}
    :label: VikorSi

.. math::
    \begin{equation}
        R_{i} = \max_j \left [
    w_{j}(f_{j}^{*}-f_{ij})/(f_{j}^{*}-f_{j}^{-})
    \right ]
    \end{equation}
    :label: VikorRi

**Step 3.** Calculate :math:`Q_{i}` with using Equation (:eq:`VikorQi`).

.. math::
    \begin{equation}
        Q_{i} = v(S_{i}-S^{*}) / (S^{-}-S^{*}) + (1 - v)(R_{i}-R^{*}) / (R^{-}-R^{*}) \label{VikorQi}
    \end{equation}
    :label: VikorQi

where:

:math:`S^{*} = min_{i} S_{i},\; \; \; S^{-} = max_{i} S_{i}`,

:math:`R^{*} = min_{i} R_{i},\; \; \; R^{-} = max_{i} R_{i}`,

:math:`v` means the weight adopted for the strategy of ''most criteria''.

**Step 4.** Ranked alternatives :math:`S`, :math:`R` and :math:`Q` are ordered in ascending order. Three ranked
lists are the outcome.

**Step 5.** A compromise solution is proposed considering the conditions of good advantage and acceptable stability
within the three vectors obtained in the previous step. The best alternative is the one with the lowest value and the
leading position in the ranking :math:`Q`.