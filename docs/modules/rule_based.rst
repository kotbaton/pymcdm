.. _rule_based:

=============
Rule based
=============



COMET
=======================


**Step 1.** Definition of the space of the problem - the expert determines the dimensionality of the problem by selecting
:math:`r` criteria, :math:`C_{1}, C_{2}, \ldots, C_{r}`. Then, a set of fuzzy numbers is selected for each criterion
:math:`C_{i}`, e.g., :math:`\{\tilde{C}_{i1}, \tilde{C}_{i2}, \ldots, \tilde{C}_{ic_{i}}\}` (:eq:`equ:criteria`):

.. math::
    \begin{equation}
    \label{equ:criteria}
    \begin{gathered}
    C_{1}=\left\{\tilde{C}_{11}, \tilde{C}_{12}, \ldots, \tilde{C}_{1 c_{1}}\right\} \\
    C_{2}=\left\{\tilde{C}_{21}, \tilde{C}_{22}, \ldots, \tilde{C}_{2 c_{2}}\right\} \\
    \cdots \\
    C_{r}=\left\{\tilde{C}_{r 1}, \tilde{C}_{r 2}, \ldots, \tilde{C}_{r c_{r}}\right\}
    \end{gathered}
    \end{equation}
    :label: equ:criteria

where :math:`C_{1}, C_{2}, \ldots, C_{r}` are the ordinals of the fuzzy numbers for all criteria.

**Step 2.** Generation of the characteristic objects - the characteristic objects (:math:`CO`) are obtained with the usage of the
Cartesian product of the fuzzy numbers’ cores of all the criteria (:eq:`equ:genco`):

.. math::
    \begin{equation}
        CO = \langle C\left(C_{1}\right) \times C\left(C_{2}\right) \times \cdots \times C\left(C_{r}\right) \rangle
    \end{equation}
    :label: equ:genco

As a result, an ordered set of all :math:`CO` is obtained (:eq:`equ:coorder`):

.. math::
    \begin{equation}
    \begin{gathered}
    CO_{1} = \langle C(\tilde{C}_{11}), C(\tilde{C}_{21}),\ldots,C(\tilde{C}_{r1}) \rangle \\
    CO_{2} = \langle C(\tilde{C}_{11}), C(\tilde{C}_{21}),\ldots,C(\tilde{C}_{r1}) \rangle \\
    \cdots \\
    CO_{t} = \langle C(\tilde{C}_{1c_{1}}), C(\tilde{C}_{2c_{2}}),\ldots,C(\tilde{C}_{rc_{r}}) \rangle
    \end{gathered}
    \end{equation}
    :label: equ:coorder

where :math:`t` is the count of :math:`CO`s and is equal to (:eq:`equ:tprod`):

.. math::
    \begin{equation}
        t=\prod_{i=1}^{r} c_{i}
    \end{equation}
    :label: equ:tprod


**Step 3.** Evaluation of the characteristic objects - the expert determines the Matrix of Expert Judgment (:math:`MEJ`) by
comparing the :math:`CO`s pairwise. The matrix is presented below (:eq:`equ:mej`):

.. math::
    \begin{equation}
    M E J=\left(\begin{array}{cccc}
    \alpha_{11} & \alpha_{12} & \cdots & \alpha_{1 t} \\
    \alpha_{21} & \alpha_{22} & \cdots & \alpha_{2 t} \\
    \cdots & \cdots & \cdots & \cdots \\
    \alpha_{t 1} & \alpha_{t 2} & \cdots & \alpha_{t t}
    \end{array}\right)\end{equation}
    :label: equ:mej

where :math:`\alpha_{ij}` is the result of comparing :math:`CO_{i}` and :math:`CO_{j}` by the expert. The function
:math:`f_{exp}` denotes the mental judgement function of the expert. It depends solely on the knowledge of the expert.
The expert’s preferences can be presented as (:eq:`equ:exppref`):

.. math::
    \begin{equation}
    \alpha_{i j}=\left\{\begin{array}{l}
    0.0, f_{\exp }\left(C O_{i}\right)<f_{\exp }\left(C O_{j}\right) \\
    0.5, f_{\exp }\left(C O_{i}\right)=f_{\exp }\left(C O_{j}\right) \\
    1.0, f_{\exp }\left(C O_{i}\right)>f_{e x p}\left(C O_{j}\right)
    \end{array}\right.\end{equation}
    :label: equ:exppref

After the MEJ matrix is prepared, a vertical vector of the Summed Judgments (:math:`SJ`) is obtained as follows (:eq:`equ:sj`):

.. math::
    \begin{equation}
    S J_{i}=\sum_{j=1}^{t} \alpha_{i j}\end{equation}
    :label: equ:sj

Eventually, the values of preference are approximated for each characteristic object. As a result, a vertical vector
:math:`P` is obtained, where the :math:`i-th` row contains the approximate value of preference for :math:`CO_{i}`.

**Step 4.** The rule base – each characteristic object and its value of preference is converted to a fuzzy rule as (:eq:`equ:fuzzyrule`):

.. math::
    \begin{equation}
    IF ~~ C\left(\tilde{C}_{1 i}\right) ~~AND~~ C\left(\tilde{C}_{2 i}\right) ~~AND~~ \ldots ~~THEN~~ P_{i}
    \end{equation}
    :label: equ:fuzzyrule

In this way, a complete fuzzy rule base is obtained.

**Step 5.** Inference and the final ranking - each alternative is presented as a set of crisp numbers, e.g.
:math:`A_{i} = \{\alpha_{i1},\alpha_{i2},\alpha_{ri}\}`$`. This set corresponds to the criteria :math:`C_{1}, C_{2}, \ldots, C_{r}`$`.
Mamdani’s fuzzy inference method is used to compute the preference of the :math:`i - th` alternative. The rule base
guarantees that the obtained results are unequivocal. The bijection makes the COMET completely rank reversal free.