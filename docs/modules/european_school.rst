.. _european_school:

===============
European school
===============



PROMETHEE II
=======================

``PROMETHEE II`` is designed to evaluate decision alternatives according to the following steps:

**Step 1.** After defining the problem, calculate the preference function values.
It is defined as (:eq:`promstep1a`) for profit criteria.

.. math::
    :label: promstep1a

        P(a,b) = F[d(a,b)], \;  \forall a, b \in A

where :math:`d(a, b)` is the difference between two actions (pairwise comparison):

.. math::
    :label: promstep1b

        d(a,b) = g(a) - g(b)

and the value of the preference function :math:`P` is always between 0 and 1. For cost criteria the difference is
reversed. Six types of preference functions (generalized criteria) are available [#promref1]_. They can be selected with
the ``preference_function`` parameter, either one for all criteria or a list with one function for each criterion, and
use the thresholds of indifference :math:`q`, preference :math:`p` and the parameter :math:`s` of the Gaussian
function (parameters ``q``, ``p`` and ``s``, with ``None`` for criteria that do not need them):

.. list-table::
   :header-rows: 1
   :widths: 10 22 12 56

   * - Type
     - ``preference_function``
     - Parameters
     - :math:`P(d)` for :math:`d > 0` (:math:`P(d) = 0` for :math:`d \leq 0`)
   * - I. Usual criterion
     - ``'usual'``
     - --
     - :math:`1`
   * - II. Quasi-criterion (U-shape)
     - ``'ushape'``
     - :math:`q`
     - :math:`0` if :math:`d \leq q`, otherwise :math:`1`
   * - III. Linear preference (V-shape)
     - ``'vshape'``
     - :math:`p`
     - :math:`d / p` if :math:`d \leq p`, otherwise :math:`1`
   * - IV. Level criterion
     - ``'level'``
     - :math:`q, p`
     - :math:`0` if :math:`d \leq q`, :math:`1/2` if :math:`q < d \leq p`, otherwise :math:`1`
   * - V. Linear preference and indifference area
     - ``'vshape_2'``
     - :math:`q, p`
     - :math:`0` if :math:`d \leq q`, :math:`(d - q) / (p - q)` if :math:`q < d \leq p`, otherwise :math:`1`
   * - VI. Gaussian criterion
     - ``'gaussian'``
     - :math:`s`
     - :math:`1 - e^{-d^2 / (2 s^2)}`

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

The positive and negative outranking flows are also returned by :class:`PROMETHEE_I`
(``pymcdm.methods.partial.PROMETHEE_I``). Alternative :math:`a` outranks :math:`b` in the PROMETHEE I partial preorder
if it is not worse in both flows and better in at least one of them; if it is better in one flow and worse in the
other, the alternatives are incomparable.

.. [#promref1] Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects: The PROMETHEE
   method. European Journal of Operational Research, 24(2), 228-238.


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


ELECTRE TRI
===========

:class:`ELECTRE_TRI` (``pymcdm.methods.sorting.ELECTRE_TRI``) is a sorting method: instead of ranking the
alternatives, it assigns each of them to one of :math:`k + 1` predefined, ordered categories
:math:`C_1, \ldots, C_{k+1}` (from the worst to the best) [#electretriref1]_, [#electretriref2]_. The categories are
separated by :math:`k` profiles :math:`b_1, \ldots, b_k` (parameter ``profiles``), where :math:`b_h` is the upper limit
of :math:`C_h` and the lower limit of :math:`C_{h+1}`. Each alternative is compared only with the profiles, so its
category does not depend on the other alternatives. The method returns the numbers of the categories.

The formulas below are written for benefit criteria; for cost criteria the evaluations and the profiles are
multiplied by :math:`-1`.

**Step 1.** Calculate the partial concordance indices with the indifference (:math:`q_j`) and preference
(:math:`p_j`) thresholds of the profile (parameters ``q`` and ``p``, one value for each criterion or one row for
each profile):

.. math::
    :label: electretri1

    c_j(a, b_h) = \left\{\begin{array}{ll}
    1, & g_j(a) \geq g_j(b_h) - q_j(b_h) \\
    0, & g_j(a) < g_j(b_h) - p_j(b_h) \\
    \frac{p_j(b_h) - (g_j(b_h) - g_j(a))}{p_j(b_h) - q_j(b_h)}, & \text{otherwise}
    \end{array}\right.

and analogously :math:`c_j(b_h, a)`. The comprehensive concordance index is the weighted average
:math:`c(a, b_h) = \sum_{j} w_j c_j(a, b_h)`.

**Step 2.** Calculate the partial discordance indices with the veto thresholds :math:`v_j` (parameter ``v``):

.. math::
    :label: electretri2

    d_j(a, b_h) = \left\{\begin{array}{ll}
    1, & g_j(a) < g_j(b_h) - v_j(b_h) \\
    0, & g_j(a) \geq g_j(b_h) - p_j(b_h) \\
    \frac{g_j(b_h) - g_j(a) - p_j(b_h)}{v_j(b_h) - p_j(b_h)}, & \text{otherwise}
    \end{array}\right.

**Step 3.** Calculate the credibility of the outranking :math:`a S b_h` (and analogously :math:`b_h S a`):

.. math::
    :label: electretri3

    \sigma(a, b_h) = c(a, b_h) \prod_{j: d_j(a, b_h) > c(a, b_h)} \frac{1 - d_j(a, b_h)}{1 - c(a, b_h)}

**Step 4.** Apply the cutting level :math:`\lambda \in [0.5, 1]` (parameter ``cutting_level``): :math:`a S b_h` is
valid if :math:`\sigma(a, b_h) \geq \lambda`. The alternative :math:`a` is preferred to :math:`b_h` if
:math:`a S b_h` and not :math:`b_h S a`, and incomparable with it if neither holds.

**Step 5.** Assign the alternatives to the categories (parameter ``procedure``):

* pessimistic (conjunctive) procedure: compare :math:`a` with :math:`b_k, b_{k-1}, \ldots, b_1`; if :math:`b_h` is the
  first profile such that :math:`a S b_h`, assign :math:`a` to :math:`C_{h+1}`, otherwise to :math:`C_1`;
* optimistic (disjunctive) procedure: compare :math:`a` with :math:`b_1, b_2, \ldots, b_k`; if :math:`b_h` is the
  first profile preferred to :math:`a`, assign :math:`a` to :math:`C_h`, otherwise to :math:`C_{k+1}`.

The optimistic procedure never assigns an alternative to a worse category than the pessimistic one; they differ for
alternatives incomparable with some profiles. With :math:`\lambda = 1` and no thresholds, the pessimistic procedure
assigns :math:`a` to a category only if it is at least as good as its lower limit on every criterion, and the
optimistic one if it is better on at least one criterion. The intermediate results (concordance and credibility
indices) are available with ``verbose=True``.

.. [#electretriref1] Mousseau, V., Słowiński, R., & Zielniewicz, P. (2000). A user-oriented implementation of the
   ELECTRE-TRI method integrating preference elicitation support. Computers & Operations Research, 27(7-8), 757-777.

.. [#electretriref2] Figueira, J. R., Mousseau, V., & Roy, B. (2016). ELECTRE methods. In S. Greco, M. Ehrgott, &
   J. R. Figueira (Eds.), Multiple Criteria Decision Analysis: State of the Art Surveys (pp. 155-185). Springer.
