.. _sum_based:

=============
Sum based
=============



Sum normalization
=======================

The sum method considers the sum of the ratings of the criteria in question when normalizing. This normalization can be
defined with the Equation (:eq:`equ:sumben`) for profit-type criteria and with the Equation (:eq:`equ:sumcost`) for
cost-type criteria.

.. math::
    \begin{equation}
    r_{i j}=\frac{x_{i j}}{\sum_{i=1}^{m} x_{i j}}
    \end{equation}
    :label: equ:sumben

.. math::
    \begin{equation}
    r_{i j}=\frac{\frac{1}{x_{i j}}}{\sum_{i=1}^{m} \frac{1}{x_{i j}}}
    \end{equation}
    :label: equ:sumcost

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.


Vector normalization
=======================

The vector method considers the root of the sum of squares of the ratings of the criteria in question when normalizing.
This normalization can be defined by the Equation (:eq:`equ:sumkben`) for profit-type criteria and by the Equation
(:eq:`equ:sumckost`) for cost-type criteria.

.. math::
    \begin{equation}
    r_{i j}=\frac{x_{i j}}{\sqrt{\sum_{i=1}^{m} x_{i j}^{2}}}
    \end{equation}
    :label: equ:sumkben

.. math::
    \begin{equation}
    r_{i j}=1-\frac{x_{i j}}{\sqrt{\sum_{i=1}^{m} x_{i j}^{2}}}
    \end{equation}
    :label: equ:sumckost

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.

Logarithmic normalization
=========================

The logarithmic method considers the natural logarithm to normalization. Values of the considered set are assumed to be
positive. The Equations are described for profit type (:eq:`equ:logprof`) and cost type (:eq:`equ:logcost`) respectively
as follows:

.. math::
    \begin{equation}
    r_{i j}=\frac{\ln \left(x_{i j}\right)}{\ln \left(\prod_{i=1}^{m} x_{i j}\right)}
    \end{equation}
    :label: equ:logprof

.. math::
    \begin{equation}
    r_{i j}=\frac{1-\frac{\ln \left(x_{i j}\right)}{\ln \left(\prod_{i=1}^{m} x_{i j}\right)}}{m-1}
    \end{equation}
    :label: equ:logcost

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.

Enhanced accuracy method
========================

Zeng and Yang proposed the enhanced accuracy method in 2013. It considers the maximum and minimum scores of the given
criteria in normalization. This normalization can be defined by the formula (:eq:`equ:zdben`) for profit-type criteria
and by the formula (:eq:`equ:zdkost`) for cost-type criteria.

.. math::
    \begin{equation}
    r_{i j}= 1 - \frac{\max_j(x_{ij}) - x_{ij}}{ \sum_{i=1}^{m} \left ( \max_j(x_{ij}) - x_{ij}) \right ) }
    \end{equation}
    :label: equ:zdben

.. math::
    \begin{equation}
    \label{equ:zdkost}
    r_{i j}= 1 - \frac{x_{ij} - \min_j(x_{ij})}{ \sum_{i=1}^{m} \left ( x_{ij} - \min_j(x_{ij}) \right ) }
    \end{equation}
    :label: equ:zdkost

where :math:`x_{ij}` is the :math:`i-th` value of the alternative and the :math:`j-th` value of the criterion in the
decision matrix.