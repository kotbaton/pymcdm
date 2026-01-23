.. _objective_weights:

=================
Objective weights
=================



Equal weights
=======================

The equal weights method assigns equal values to criteria according to their number. It can be represented by the Equation
(:eq:`equ:equal`).

.. math::
    \begin{equation}
    w_{j}=\frac{1}{n}
    \end{equation}
    :label: equ:equal

where :math:`n` denotes the number of criteria.

Entropy method
=======================

The entropy weighting method is based on Shannon's measure of information uncertainty. It has the advantage of reducing
risk and increasing efficiency. The entropy weights technique can be presented in the following steps:

**Step 1.** Normalisation of the decision matrix :math:`X={x_{ij}; i = 1, 2, \dots, m; j=1,2,\dots, n}`, where :math:`m`
is the number of alternatives, :math:`n` is the number of criteria. This normalization can be represented by the Equation (:eq:`equ:normentropy`).

.. math::
    \begin{equation}
    p_{i j}=\frac{x_{i j}}{\sum_{i=1}^{m} x_{i j}} \quad i=1, \ldots, m ; j=1, \ldots, n
    \end{equation}
    :label: equ:normentropy

**Step 2.** Calculation of the entropy measure :math:`E_j` for each criterion according to the Equation (:eq:`equ:entropy`).

.. math::
    \begin{equation}
    E_{j}=-\frac{\sum_{i=1}^{m} p_{i j} \ln \left(p_{i j}\right)}{\ln (m)} \quad j=1, \ldots, n
    \end{equation}
    :label: equ:entropy

**Step 3.** Derive weights based on the calculated entropy for each criterion (:eq:`equ:wentropy`).

.. math::
    \begin{equation}
    w_{j}=\frac{1-E_{j}}{\sum_{i=1}^{n}\left(1-E_{i}\right)} \quad j=1, \ldots, n
    \end{equation}
    :label: equ:wentropy



Standard deviation method
=========================

The standard deviation weighting method is based on the statistical measure of standard deviation. It assigns small weights
to a criterion that has similar values across variants. This method can be presented in two steps:

**Step 1.** Calculate the standard deviation measure for all criteria according to the Equation (:eq:`equ:odchylenie`).

.. math::
    \begin{equation}
    \label{equ:odchylenie}
    \sigma_{j}=\sqrt{\frac{\sum_{i=1}^{m}\left(x_{i j}-\overline{x_{j}}\right)^{2}}{m}} j=1, \ldots, n
    \end{equation}
    :label: equ:odchylenie

where :math:`x_{ij}` is the value from the decision matrix for :math:`i-th` alternative and :math:`j-th` criterion.

**Step 2.** Derive the weights based on the values of the standard deviation measure (:eq:`equ:wodchylenie`).

.. math::
    \begin{equation}
    w_{j}= \frac{\sigma_{j}}{\sum_{j=1}^{n} \sigma_{j}}  \quad j=1, \ldots, n
    \end{equation}
    :label: equ:wodchylenie


MEREC
=======================

**Step 1.** Create a decision matrix. The values of the matrix (:math:`x_{ij}`) must be greater than 0 and non-negative.
If such values are present, they must be transformed using an appropriate technique.

**Step 2.** Normalize the decision matrix using the Equation (:eq:`equ:merecs2`).

.. math::
    \begin{equation}
    n_{i j}^{x}=\left\{\begin{array}{lll}
    \frac{\min _{k} x_{k j}}{x_{i j}} & \text { if } & j \in B \\
    \frac{x_{i j}}{\max _{k j}} & \text { if } & j \in C
    \end{array}\right.
    \end{equation}
    :label: equ:merecs2


where :math:`B` means benefit criteria, and :math:`C` means cost criteria.

**Step 3.** Calculation of the overall performance of alternatives using a non-linear function according to (:eq:`equ:merecs3`).

.. math::
    \begin{equation}
    S_{i}=\ln \left(1+\left(\frac{1}{m} \sum_{j}\left|\ln \left(n_{i j}^{x}\right)\right|\right)\right)
    \end{equation}
    :label: equ:merecs3

**Step 4.** Calculation of the performance of the alternatives after the removal of each criterion. An :math:`m` set of results
is obtained for each criterion exclusion, to which the following Equation is applied:

.. math::
    \begin{equation}
    S_{i j}^{\prime}=\ln \left(1+\left(\frac{1}{m} \sum_{k, k \neq j}\left|\ln \left(n_{i k}^{x}\right)\right|\right)\right)
    \end{equation}
    :label: equ:merecs4


**Step 5.** Calculation of the sum of absolute deviations using the Equation (:eq:`equ:merecs5`).

.. math::
    \begin{equation}
    E_{j}=\sum_{i}\left|S_{i j}^{\prime}-S_{i}\right|
    \end{equation}
    :label: equ:merecs5

**Step 6.** Calculate the weights from the sum of the absolute deviations using the Equation (:eq:`equ:merecs6`).

.. math::
    \begin{equation}
    w_{j}=\frac{E_{j}}{\sum_{k} E_{k}}
    \end{equation}
    :label: equ:merecs6

CRITIC method
=======================

**Step 1.** Normalization of the initial decision matrix using Equation (:eq:`equ:critic1`) for benefit criteria:

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij} - x_{j}^{min}}{x_{j}^{max} - x_{j}^{min}}.
    \end{equation}
    :label: equ:critic1

**Step 2.** Calculation of the correlation among criteria pairs by using Equation (:eq:`equ:critic2`):

.. math::
    \begin{equation}
        \rho _{jk} = \frac{\sum_{i=1}^{m}(r_{ij} - \overline{r}_{j})(r_{ik} - \overline{r}_{k})}{\sqrt{\sum_{i=1}^{m}(r_{ij} - \overline{r}_{j})^{2} \sum_{i=1}^{m}(r_{ik} - \overline{r}_{k})^{2}}}.
    \end{equation}
    :label: equ:critic2

**Step 3.** Computation of weights of criteria by using Equation (:eq:`equ:critic3`) and (:eq:`equ:critic4`).

.. math::
    \begin{equation}
        c_{j} = \sigma _{j} \sum_{k=1}^{n} (1 - \rho _{jk});
    \end{equation}
    :label: equ:critic3

.. math::
    \begin{equation}
        w_{j} = \frac{c_{j}}{\sum_{k=1}^{n}c_{k}},
    \end{equation}
    :label: equ:critic4

where :math:`i = 1, 2, \ldots, m; \;  j, k = 1, 2, \ldots, n.`

CILOS method
=======================

**Step 1.** Convert cost-type criteria to profit-type criteria according to the Equation (:eq:`equ:cilos1`).

.. math::
    \begin{equation}
        r_{i j}=\frac{\min _{i} x_{i j}}{x_{i j}}
    \end{equation}
    :label: equ:cilos1


**Step 2.** Create a relative loss matrix P based on the square matrix A, in which each row corresponds to the row in
which the criteria have the highest value. The Equation (:eq:`equ:cilos2`) can represent this.

.. math::
    \begin{equation}
    P_{i j}=\frac{A_{i i}-A_{i j}}{A_{i i}}, \quad P_{i i}=0
    \end{equation}
    :label: equ:cilos2

**Step 3.** Calculation of the :math:`F` matrix based on the relative loss matrix (:eq:`equ:cilos3`).

.. math::
    \begin{equation}
    F=\left(\begin{array}{cccc}
    -\sum_{i=1}^{m} P_{i 1} & P_{12} & \ldots & P_{1 m} \\
    P_{21} & -\sum_{i=1}^{m} P_{i 2} &  & P_{2 m} \\
    & \cdots & \\
    P_{m 1} & P_{m 2} & \cdots & -\sum_{i=1}^{m} P_{i m}
    \end{array}\right)
    \end{equation}
    :label: equ:cilos3

This leads to an equation that results in weights that require normalization.

.. math::
    \begin{equation}F w^{T}=0\end{equation}
    :label: equ:cilos4

IDOCRIW method
=======================

The IDOCRIW method aggregates weights acquired by the execution of the CILOS method and the entropy method.
Aggregation proceeds as follows:

.. math::
    \begin{equation}
        w_{j}=\frac{q_{j} W_{j}}{\sum_{j=1}^{m} q_{j} W_{j}}
    \end{equation}
    :label: equ:idocriw1

where :math:`W_j` are entropy weights and :math:`q_j` are CILOS weights.

Angular method
=======================


Angular weight selection method is based on an approach that uses the angle between criteria to determine their importance
in a decision problem. Hence, it can be presented using the following steps:

**Step 1.** Calculate the angle between the :math:`j-th` criterion and the reference criterion based on Equation (:eq:`angl`).

.. math::
    \begin{equation}
    \label{angl}
        u_j = \arccos\left({  \frac{\sum_{i=1}^m \left ( \frac{b_{ij}}{m} \right )  }{ \sqrt{\sum_{i=1}^m  \left ( b_{ij} \right )^2 }  \sqrt{\sum_{i=1}^m  \left ( \frac{1}{m} \right )^2 }                       }}\right)
    \end{equation}
    :label: angl

**Step 2.** Calculate the angle weight for the :math:`j-th` criterion using Equation (:eq:`wj`).

.. math::
    \begin{equation}
    \label{wj}
        w_j = u_j/\sum_{j=1}^n  u_j
    \end{equation}
    :label: wj

Gini Coeficient method
=======================

**Step 1.** Calculating the Gini coefficient :math:`G_k` for each criterion using the Equation (:eq:`equ:gini`).

.. math::
    \begin{equation}
        G_k = \sum^n_{i=1} \sum^n_{j=1} \frac{| Y_{ki} - Y_{kj} |}{2n^2\mu}
    \end{equation}
    :label: equ:gini

where :math:`k` denotes the given criterion, :math:`i` and :math:`j` denote the value of an alternative for the given
criterion, :math:`n` denotes the number of alternatives and :math:`\mu` denotes the expectation of the index
:math:`k` overall data.


**Step 2.** Determination of weights by using the Gini coefficient with Equation (:eq:`equ:giniw`).

.. math::
    \begin{equation}
    \label{equ:giniw}
        w_k = \frac{G_k}{\sum^m_{i=1}G_i}
    \end{equation}
    :label: equ:giniw

where :math:`m` is the number of Gini coefficients.

Statistical variance method
===========================

The statistical variance method is a method in which objective weights are obtained through mathematical-statistical
variance, which describes the spread of variables from their mean value. The method can be presented in the following
three steps:

**Step 1.** Normalizing the decision matrix with the selected method.

**Step 2.** Calculate each criterion's statistical variance from the normalized decision matrix according to Equation (:eq:`equ:stat2`).

.. math::
    \begin{equation}
    V_{j}=\left(\frac{1}{n}\right) \sum_{i=1}^{n}\left(r_{i j}-\overline{r_{i j}}\right)^{2}
    \end{equation}
    :label: equ:stat2

**Step 3.** Establishing the criterion weights on the basis of the calculated statistical variance.

.. math::
    \begin{equation}
    w_{j}=\frac{V_{j}}{\sum_{i=1}^{m} V_{j}}
    \end{equation}
    :label: equ:stat3

LOPCOW method
=======================

The LOgarithmic Percentage Change-driven Objective Weighting (LOPCOW) method is an objective criteria weighting approach that determines weights directly from data characteristics. It reduces scale effects, handles both benefit and cost criteria, and allows the use of negative values in the decision matrix.

**Step 1.** Construction of the initial decision matrix :math:`\mathbf{X} = [x_{ij}]`, where :math:`i = 1, 2, \ldots, m` denotes alternatives and :math:`j = 1, 2, \ldots, n` denotes criteria.

**Step 2.** Normalization of the decision matrix using linear max–min normalization. For benefit criteria, Equation (:eq:`equ:lopcow1`) is used:

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{ij} - x_{j}^{\min}}{x_{j}^{\max} - x_{j}^{\min}}.
    \end{equation}
    :label: equ:lopcow1

For cost criteria, Equation (:eq:`equ:lopcow2`) is applied:

.. math::
    \begin{equation}
        r_{ij} = \frac{x_{j}^{\max} - x_{ij}}{x_{j}^{\max} - x_{j}^{\min}}.
    \end{equation}
    :label: equ:lopcow2

**Step 3.** Computation of the percentage value of each criterion. First, the mean square value of the normalized criterion is calculated and expressed as a percentage of its standard deviation using Equation (:eq:`equ:lopcow3`):

.. math::
    \begin{equation}
        PV_{j} = \left| \ln \left( \frac{\sqrt{\frac{1}{m} \sum_{i=1}^{m} r_{ij}^{2}}}{\sigma_{j}} \right) \cdot 100 \right|.
    \end{equation}
    :label: equ:lopcow3

where :math:`\sigma_{j}` denotes the standard deviation of criterion :math:`j`.

**Step 4.** Determination of objective criteria weights using Equation (:eq:`equ:lopcow4`):

.. math::
    \begin{equation}
        w_{j} = \frac{PV_{j}}{\sum_{k=1}^{n} PV_{k}}.
    \end{equation}
    :label: equ:lopcow4

where :math:`\sum_{j=1}^{n} w_{j} = 1`.

References
-----------------------

Ecer, F., & Pamucar, D. (2022). *A novel LOPCOW‐DOBI multi‐criteria sustainability performance assessment methodology: An application in developing country banking sector*. **Omega**, 112, 102690.
