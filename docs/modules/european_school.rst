.. _european_school:

===============
European school
===============



PROMETHEE II
=======================

:class:`PROMEHTEE II` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** After defining the problem, calculate the preference function values.
It is defined as (:eq:`promstep1a`) for profit criteria.

.. math::
    \begin{equation}
        P(a,b) = F[d(a,b)], \;  \forall a, b \in A
    \end{equation}
    :label: promstep1a

where :math:`d(a, b)` is the difference between two actions (pairwise comparison):

.. math::
    \begin{equation}
        d(a,b) = g(a) - g(b)
    \end{equation}
    :label: promstep1b

and the value of the preference function :math:`P` is always between 0 and 1 and it is calculating for
each criterion according to the Equation~(:eq:`promstep1c`):

.. math::
    \begin{equation}
        P(d) = \left\{\begin{array}{cc}
    0, & d \leq 0 \\
    1, & d > 0
    \end{array}\right.
    \end{equation}
    :label: promstep1c

**Step 2.** Calculate the aggregated preference indices (:eq:`promstep2a`).

.. math::
    \begin{equation}
        \left\{\begin{array}{c}
    \pi(a,b) = \sum_{j=1}^{n} P_{j}(a,b)w_{j} \\
    \pi(b,a) = \sum_{j=1}^{n} P_{j}(b,a)w_{j}
    \end{array}\right.
    \end{equation}
    :label: promstep2a


where :math:`a` and :math:`b` are alternatives and :math:`\pi(a,b)` shows how much alternative :math:`a` is preferred to
:math:`b` over all of the criteria. There are some properties (:eq:`promstep2b`) which must be true for all
alternatives set :math:`A`.

.. math::
    \begin{equation}
        \left\{\begin{array}{c}
    \pi(a,a) = 0 \\
    0 \leq \pi(a,b) \leq 1 \\
    0 \leq \pi(b,a) \leq 1 \\
    0 \leq \pi(a,b) + \pi(b,a) \leq 1
    \end{array}\right.
    \end{equation}
    :label: promstep2b

**Step 3.** Calculate positive (:eq:`promstep3a`) and negative (:eq:`promstep3b`) outranking flows.

.. math::
    \begin{equation}
        \phi^{+}(a) = \frac{1}{m-1}\sum_{x \in A} \pi(a,x)
    \end{equation}
    :label: promstep3a

.. math::
    \begin{equation}
        \phi^{-}(a) = \frac{1}{m-1}\sum_{x \in A} \pi(x,a)
    \end{equation}
    :label: promstep3b

**Step 4.** Ranking is based on the net flow :math:`\Phi` (:eq:`promstep4`).

.. math::
    \begin{equation}
        \Phi(a) = \Phi^{+}(a) - \Phi^{-}(a)
    \end{equation}
    :label: promstep4

where larger value of :math:`\Phi(a)` means better alternative.
