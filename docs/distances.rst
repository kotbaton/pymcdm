Distance module
----------------


draWS Distance
==============

*Sałabun and Shekhovtsov (2023)* introduced the **drastic weighted similarity distance (draWS distance)** as a normalized metric for quantifying dissimilarity between rankings.
The measure is derived from the Weighted Similarity (WS) coefficient and is designed to emphasize errors occurring at the top of a ranking, where discrepancies are typically more impactful in decision-making contexts.

Unlike traditional distance measures that scale penalties according to the magnitude of rank differences, the draWS distance adopts a *drastic* approach:
every mismatch between positions is treated equally as an error.
However, these errors are weighted by positional importance using an exponentially decreasing sequence, ensuring that disagreements in higher-ranked positions contribute more heavily to the final distance.

Given two rankings :math:`x` and :math:`y`, each of length :math:`N`, the draWS distance is defined as:

.. math::

   d_{\mathrm{draWS}}(x, y)
   = \frac{\displaystyle\sum_{i=1}^{N} 2^{-i}\, f(x_i, y_i)}
          {1 - 2^{-N}}

where the binary disagreement function is:

.. math::

   f(x_i, y_i) =
   \begin{cases}
      0, & \text{if } x_i = y_i,\\
      1, & \text{if } x_i \ne y_i.
   \end{cases}

The numerator aggregates all positional mismatches between the two rankings, weighted by the geometric sequence :math:`2^{-i}`.
The denominator normalizes the metric to the interval :math:`[0, 1]`, making the measure directly comparable across rankings of different lengths.

The draWS distance satisfies all axioms of a true metric—**non-negativity**, **identity of indiscernibles**, **symmetry**, and **triangle inequality**—ensuring mathematical rigor and reliability.
By combining a drastic treatment of mismatches with a principled weighting scheme, it captures ranking differences accurately and intuitively, particularly in applications where top-ranked positions carry greater significance.

**Reference**

Sałabun, W., & Shekhovtsov, A. (2023). *An innovative drastic metric for ranking similarity in decision-making problems*.
Proceedings of the 18th Conference on Computer Science and Intelligence Systems, 731–738.


Kemeny Distance
===============

*Kemeny and Snell (1962)* introduced the Kemeny distance as an axiomatic measure
of dissimilarity between two rankings based on pairwise preference disagreements.
The distance counts how many pairwise orderings differ between two rankings and
is invariant to labeling of alternatives.

Let :math:`\mathbf{M}_1` and :math:`\mathbf{M}_2` be the preference-score matrices
associated with two rankings, where each entry takes values in
:math:`\{-1, 0, 1\}`. The Kemeny distance is defined as:

.. math::

   d_K(\mathbf{M}_1, \mathbf{M}_2)
   = \frac{1}{2} \sum_{i=1}^{n} \sum_{j=1}^{n}
     \left| M_1(i,j) - M_2(i,j) \right|

A lower value of :math:`d_K` indicates greater similarity between rankings.

**Reference**

Kemeny, J. G., & Snell, J. L. (1962). *Mathematical models in the social sciences*.
MIT Press.

Frobenius Distance Between Rankings
===================================

*Dezert, Shekhovtsov, and Sałabun (2024)* proposed the Frobenius distance as a
matrix-norm-based measure for comparing rankings via their preference-score
matrices. The method is invariant under indexing and satisfies the properties
of a true metric.

Given two preference-score matrices :math:`\mathbf{M}_1` and :math:`\mathbf{M}_2`,
the Frobenius distance is defined as:

.. math::

   d_F(\mathbf{M}_1, \mathbf{M}_2)
   = \| \mathbf{M}_1 - \mathbf{M}_2 \|_F
   = \sqrt{\sum_{i=1}^{n} \sum_{j=1}^{n}
   \left( M_1(i,j) - M_2(i,j) \right)^2}

This distance measures the overall magnitude of disagreement between all
pairwise preferences.

**Reference**

Dezert, J., Shekhovtsov, A., & Sałabun, W. (2024).
A new distance between rankings. *Heliyon*, 10, e28265.
