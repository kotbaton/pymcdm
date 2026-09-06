.. _linear_ratio_based:

==================
Linear ratio based
==================



Max normalization
=======================

The maximum method considers the maximum ratings of the given criteria in normalization. This normalization can
be defined by the Equation (:eq:`equ:maxben`) for profit-type criteria and by the Equation (:eq:`equ:maxcost`) for cost-type
criteria.

.. math::
    :label: equ:maxben

    r_{i j}=\frac{x_{i j}}{\max _{j}\left(x_{i j}\right)}

.. math::
    :label: equ:maxcost

    r_{i j}=1-\frac{x_{i j}}{\max _{j}\left(x_{i j}\right)}


where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.


Linear normalization
=======================

The linear normalization method is similar to max normalization, where profit-type criteria are normalized as in max
normalization, while cost-type criteria are normalized using the Equation (:eq:`equ:mmcost`).


.. math::
    :label: equ:mmcost

    r_{i j}=\frac{\min _{j}\left(x_{i j}\right)}{x_{i j}}

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.


Nonlinear normalization
=======================

The nonlinear method considers the normalization of the maximum and minimum ratings of the criteria in question and
exponentiation. This normalization can be defined by the Equation (:eq:`equ:nieben`) for profit-type criteria and by the
Equation (:eq:`equ:niekost`) for cost-type criteria.

.. math::
    :label: equ:nieben

    r_{i j}= \left ( \frac{x_{ij} }{ \max_i x_{ij}}  \right )^2

.. math::
    :label: equ:niekost

    r_{i j}= \left ( \frac{ \min_i x_{ij}}{ x_{ij}}  \right )^3

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.