.. _european_school:

===============
European school
===============



PROMETHEE II
=======================

``PROMEHTEE II`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** After defining the problem, calculate the preference function values.
It is defined as (:eq:`promstep1a`) for profit criteria.

.. math::
    :label: promstep1a

        P(a,b) = F[d(a,b)], \;  \forall a, b \in A

where :math:`d(a, b)` is the difference between two actions (pairwise comparison):

.. math::
    :label: promstep1b

        d(a,b) = g(a) - g(b)

and the value of the preference function :math:`P` is always between 0 and 1 and it is calculating for
each criterion according to the Equation~(:eq:`promstep1c`):

.. math::
    :label: promstep1c

        P(d) = \left\{\begin{array}{cc}
    0, & d \leq 0 \\
    1, & d > 0
    \end{array}\right.

**Step 2.** Calculate the aggregated preference indices (:eq:`promstep2a`).

.. math::
    :label: promstep2a

        \left\{\begin{array}{c}
    \pi(a,b) = \sum_{j=1}^{n} P_{j}(a,b)w_{j} \\
    \pi(b,a) = \sum_{j=1}^{n} P_{j}(b,a)w_{j}
    \end{array}\right.


where :math:`a` and :math:`b` are alternatives and :math:`\pi(a,b)` shows how much alternative :math:`a` is preferred to
:math:`b` over all of the criteria. There are some properties (:eq:`promstep2b`) which must be true for all
alternatives set :math:`A`.

.. math::
    :label: promstep2b

        \left\{\begin{array}{c}
    \pi(a,a) = 0 \\
    0 \leq \pi(a,b) \leq 1 \\
    0 \leq \pi(b,a) \leq 1 \\
    0 \leq \pi(a,b) + \pi(b,a) \leq 1
    \end{array}\right.

**Step 3.** Calculate positive (:eq:`promstep3a`) and negative (:eq:`promstep3b`) outranking flows.

.. math::
    :label: promstep3a

        \phi^{+}(a) = \frac{1}{m-1}\sum_{x \in A} \pi(a,x)

.. math::
    :label: promstep3b

        \phi^{-}(a) = \frac{1}{m-1}\sum_{x \in A} \pi(x,a)

**Step 4.** Ranking is based on the net flow :math:`\Phi` (:eq:`promstep4`).

.. math::
    :label: promstep4

        \Phi(a) = \Phi^{+}(a) - \Phi^{-}(a)

where larger value of :math:`\Phi(a)` means better alternative.


TODIM
=====

``TODIM`` (TOmada de Decisão Interativa e Multicritério) is a discrete multicriteria
method based on Prospect Theory [#todimref1]_. It evaluates alternatives through
pairwise dominance degrees that model the psychology of gains and losses. The method
proceeds as follows:

**Step 1.** Normalize the decision matrix using sum normalization (:eq:`todimstep1`).

.. math::
    :label: todimstep1

    P_{ic} = \frac{x_{ic}}{\sum_{i=1}^{n} x_{ic}}

For cost criteria, replace :math:`x_{ic}` with :math:`1/x_{ic}` before normalizing.

**Step 2.** Compute relative criterion weights (:eq:`todimstep2`), where :math:`w_r`
is the weight of the reference criterion (the criterion with the highest weight).

.. math::
    :label: todimstep2

    w_{rc} = \frac{w_c}{w_r}

**Step 3.** For each pair of alternatives :math:`(A_i, A_j)`, compute the overall
dominance degree (:eq:`todimstep3`).

.. math::
    :label: todimstep3

    \delta(A_i, A_j) = \sum_{c=1}^{m} \phi_c(A_i, A_j)

where the partial dominance on criterion :math:`c` (:eq:`todimstep3b`) reflects
prospect-theoretic gains and losses:

.. math::
    :label: todimstep3b

    \phi_c(A_i, A_j) = \begin{cases}
        \sqrt{\dfrac{w_{rc}(P_{ic} - P_{jc})}{\sum_{c=1}^{m} w_{rc}}}, & P_{ic} > P_{jc} \\[6pt]
        0, & P_{ic} = P_{jc} \\[6pt]
        -\dfrac{1}{\theta}\sqrt{\dfrac{\left(\sum_{c=1}^{m} w_{rc}\right) \cdot (P_{jc} - P_{ic})}{w_{rc}}}, & P_{ic} < P_{jc}
    \end{cases}

and :math:`\theta > 0` is the attenuation factor for losses (default 2.5).

**Step 4.** Normalize the row sums of the dominance matrix to [0, 1] (:eq:`todimstep4`).

.. math::
    :label: todimstep4

    \xi_i = \frac{\sum_{j=1}^{n} \delta(A_i, A_j) - \min_i \sum_{j=1}^{n} \delta(A_i, A_j)}
                 {\max_i \sum_{j=1}^{n} \delta(A_i, A_j) - \min_i \sum_{j=1}^{n} \delta(A_i, A_j)}

where larger :math:`\xi_i` indicates a better-performing alternative.

.. rubric:: References

.. [#todimref1] Gomes, L. F. A. M., & Rangel, L. A. D. (2009). An application of
   the TODIM method to the multicriteria rental evaluation of residential properties.
   *European Journal of Operational Research*, 193(1), 204–211.
   https://doi.org/10.1016/j.ejor.2007.10.046
