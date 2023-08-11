Correlation module
------------------


Spearman correlation coefficient
================================

The Spearman coefficient for the rank values :math:`rgX` and :math:`rgY` can be represented by the formula (\ref{equ:spearm}), where
the vectors :math:`rgX` and :math:`rgY` must have the same number of rank values. When rankings have unique preference values that do
not repeat, and all variants have different rankings, the Equation (:eq:`equ:spearm2`) can be used to calculate the
Spearman coefficient.

.. math::
    \begin{equation}
    r_{s}=\frac{\operatorname{cov}\left(r g_{X}, r g_{Y}\right)}{\sigma_{r g_{X}} \sigma_{r g_{Y}}}
    \end{equation}
    :label: equ:spearm

.. math::
    \begin{equation}
    r_{s}=1-\frac{6 \cdot \sum_{i=1}^{N}\left(r g_{X_{i}}-r g_{Y_{i}}\right)}{N\left(N^{2}-1\right)}
    \end{equation}
    :label: equ:spearm2

where :math:`N` denotes the number of rank.



Weighted Spearman correlation coefficient
=========================================

The weighted Spearman correlation coefficient (:math:`r_w`) is being used to make a comparison between two rankings. This
coefficient has the benefit of considering the highest ranked alternative as the most important. It can be shown by the
Equation (:eq:`wSpearCoeff`).

.. math::
    \begin{equation}
        r_{w} = 1 - \frac{6\sum_{i=1}^{N}(x_{i} - y_{i})^{2} ((N - x_{i} + 1) + (N - y_{i} + 1))}{N^{4} + N^{3} - N^{2} - N}
    \end{equation}
    :label: wSpearCoeff

where :math:`x` and :math:`y` are the rank vectors, and :math:`N` is their dimension.

Kendall rank correlation coefficient
====================================
The Kendall rank correlation coefficient is used to evaluate two rank vectors, determining the strength of their
relationship. Kendall's rank correlation coefficient values are in the range :math:`[-1, 1]`. An increase in the value of
the coefficient indicates an increase in the ranks of both variables, where the value of the coefficient decreases. This
means that the rank of one variable is increasing and the rank of the other variable is decreasing.
Kendall's rank correlation coefficient can be represented by the Equation (:eq:`eq:kendall`).

.. math::
    \begin{equation}
        \tau_{b} = \frac{
        \sum\limits^{N}_{i=1}
        \sum\limits^{N}_{j=1}
        x_{ij} y_{ij}
        }{
        \sqrt{
        \sum\limits^{N}_{i=1}
        \sum\limits^{N}_{j=1}
        x_{ij}^{2}
        \sum\limits^{N}_{i=1}
        \sum\limits^{N}_{j=1}
        y_{ij}^{2}
        }
        }
    \end{equation}
    :label: eq:kendall

where :math:`N` denotes the number of ranks, :math:`x_{ij}` and :math:`y_{ij}` denote the values of the respective
rankings :math:`x` and :math:`y`.

Ranking similarity coefficient
==============================
The ranking similarity coefficient :math:`WS` is an asymmetric measure created to assess the similarity of the rankings of two
vectors :math:`x` and :math:`y`. The weight of the comparison is determined according to the relevance of the :math:`x`
ranking position. The higher the rank, the higher the significance for the coefficient :math:`WS`. The values of the
ranking similarity coefficient are in the range :math:`[0, 1]` and can be represented by the Equation (:eq:`equ:ws`).


.. math::
    \begin{equation}
    W S=1-\sum_{i=1}^{N} 2^{-x_{i}} \frac{\left|x_{i}-y_{i}\right|}{\max \left(\left|x_{i}-1\right|,\left|x_{i}-N\right|\right)}
    \end{equation}
    :label: equ:ws

where :math:`N` denotes the number of ranks, :math:`x_i` and :math:`y_i` denote the :math:`i-th` ranks of the :math:`x`
and :math:`y` vectors.


Pearson’s correlation coefficient
=================================
The Pearson correlation coefficient compares two data sets using covariance and standard deviation.
Its value ranges from $-$1 to 1. The smaller the Pearson correlation coefficient value, the less correlation between the
data, while the more significant the value, the greater the correlation. Equation (:eq:`equ:pearson`) can represent it.

.. math::
    \begin{equation}
    r(x, y)=\frac{\sum_{i=1}^{N}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right)}{\sqrt{\sum_{i=1}^{N}\left(x_{i}-\bar{x}\right)^{2}} \sqrt{\sum_{i=1}^{N}\left(y_{i}-\bar{y}\right)^{2}}}
    \end{equation}
    :label: equ:pearson

where :math:`N` is the number of samples and :math:`x` and :math:`y` are vectors of values.

Goodman-Kruskal correlation coefficient
=======================================

The Goodman-Kruskal Gamma Correlation Coefficient is a measure of rank correlation that measures the strength of association
from cross-tabulations. This measure is applied to ordinal variables that are either continuous variables or discrete variables.
The values of this measure are in the range [-1,1] and can be represented as follows:

.. math::
    \begin{equation}
    G=\frac{N_{s}-N_{d}}{N_{s}+N_{d}}
    \end{equation}

where :math:`N_s` is the number of compatible pairs and :math:`N_d` is the number of non-compliant pairs.

Weighted Similarity Coefficient
=======================================

Weighted Similarity Coefficient was created because of the difficulty involved in determining the similarity of two
criterion weight vectors. For this purpose, the knowledge that the sum of the weights should be equal to one was used,
providing a normalized version of this equation. In addition, it was based on the Manhattan distance metric and can be
represented as follows:

.. math::
    \begin{equation} \label{eq:wsc}
    WSC = 1 - \frac{d_1(\mathbf{w},\mathbf{v})}{2 \cdot (1 - min(\mathbf{w}))} = 1 - \frac{\sum_{i=1}^N |w_i - v_i|}{2 \cdot (1 - {min}_{i} w_i)}
    \end{equation}

where :math:`w_i` and :math:`v_i` are the criterion weights.

However, if we deal with the decision problems with a small number of criteria, such as 2, 3, and 4, it can be observed
that the differences between weights values are naturally bigger in this case. That means that the possibility of
achieving maximum distance 2 is different for weight vectors of different lengths. Therefore, the better way to normalize
the distance is based on the minimum value on one of the weight vectors (:eq:`equ:wsc2`).

.. math::
    \begin{equation} \label{eq:wsc2}
    \textit{WSC}_2 = 1 - \frac{d_1(\mathbf{w},\mathbf{v})}{2} = 1 - \frac{\sum_{i=1}^N |w_i - v_i|}{2}
    \end{equation}
    :label: equ:wsc2
