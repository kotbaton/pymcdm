.. _linear_maxmin:

====================
Linear max-min based
====================



Min-max normalization
=======================

The minimum-maximum method considers the maximum and minimum ratings of the given criteria in normalization. This
normalization can be defined by the Equation (:eq:`equ:minmaxben`) for profit-type criteria and by the Equation
(:eq:`equ:minmaxcost`) for cost-type criteria.

.. math::
    \begin{equation}
    r_{i j}=\frac{x_{i j}-\min _{j}\left(x_{i j}\right)}{\max _{j}\left(x_{i j}\right)-\min _{j}\left(x_{i j}\right)}
    \end{equation}
    :label: equ:minmaxben

.. math::
    \begin{equation}
    r_{i j}=\frac{\max _{j}\left(x_{i j}\right)-x_{i j}}{\max _{j}\left(x_{i j}\right)-\min _{j}\left(x_{i j}\right)}
    \end{equation}
    :label: equ:minmaxcost


where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.

Zavadskas and Turkis normalization
==================================

Zavadskas and Turskis in 2008 proposed a new normalization method. This normalization can be defined by the Equation
(:eq:`equ:ztben`) for profit-type criteria and by the Equation (:eq:`equ:ztkost`) for cost-type criteria.

.. math::
    \begin{equation}
     r_{i j}= 1 - \frac{\left | \max_j \left( x_{ij} \right) - x_{ij} \right |}{\max_j \left( x_{ij} \right)}
    \end{equation}
    :label: equ:ztben

.. math::
    \begin{equation}
     r_{i j}= 1 - \frac{\left | \min_j \left( x_{ij} \right) - x_{ij} \right |}{\min_j \left( x_{ij} \right)}
    \end{equation}
    :label: equ:ztkost

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.