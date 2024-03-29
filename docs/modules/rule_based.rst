.. _rule_based:

=============
Rule based
=============



COMET
=======================

:class:`COMET` is designed to evaluate decision alternatives according to the following steps:


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

where :math:`t` is the count of :math:`CO` and is equal to (:eq:`equ:tprod`):

.. math::
    \begin{equation}
        t=\prod_{i=1}^{r} c_{i}
    \end{equation}
    :label: equ:tprod


**Step 3.** Evaluation of the characteristic objects - the expert determines the Matrix of Expert Judgment (:math:`MEJ`) by
comparing the :math:`CO` pairwise. The matrix is presented below (:eq:`equ:mej`):

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
:math:`A_{i} = \{\alpha_{i1},\alpha_{i2},\alpha_{ri}\}`. This set corresponds to the criteria :math:`C_{1}, C_{2}, \ldots, C_{r}`.
Mamdani’s fuzzy inference method is used to compute the preference of the :math:`i - th` alternative. The rule base
guarantees that the obtained results are unequivocal. The bijection makes the COMET completely rank reversal free.

Compromise COMET
----------------
Compromise COMET approach creates a COMET compromise model using evaluated samples from different MCDA approaches. It use a voting mechanism for evaluating characteristic objects, where the defined MCDA methods determine preferences of the evaluated Characteristic Objects. Voting consists of counting responses when comparing characteristic objects, where depending on the number of votes, a given comparison in the MEJ matrix is assigned a value of 0, 0.5, or 1. This procedure can be defined as follows:

.. math::
    \alpha_{ij} = \left\{ \begin{array}{ll}
    0.0 , &  n_{votes} > \frac{N}{2} \\ \\
    0.5 , &   n_{votes} = \frac{N}{2} \\\\
    1.0 , &   n_{votes} < \frac{N}{2} 
    \end{array} \right.
   :label: equ:comp

where :math:`N` denotes the maximum number of possible votes (e.g. number of the method for compromise), :math:`n_{votes}` denotes the votes cast for comparisons of Characteristic Objects (:math:`CO_i > CO_j`). Instead of :math:`\frac{N}{2}` any other values in range :math:`[1 < N]` can be used.

ESP Expert COMET
----------------
:class:`ESPExpert` is designed to evaluate characteristic objects in the :class:`COMET` method using the Expected Solution Points provided by an expert. Each ESP is defined as a vector with a length equal to the number of the criteria in decision problem. Then, characteristic objects are compared based on distances from those Expected Solution Points.

When using :class:`ESPExpert` it is possible to define several ESP, define the function which will calculate the distance between them, and define the function which will aggregate distances from different ESP for each CO.


Function Expert COMET
---------------------
:class:`FunctionExpert` is designed to evaluate characteristic objects in the :class:`COMET` method using the function provided by an expert.

If :class:`FunctionExpert` is used, then **Step 2** is omitted in the COMET procedure and then in **Step 3** Equation (:eq:`equ:funcexpt`) is used instead of (:eq:`equ:sj`).

.. math::
    \begin{equation}
    S J_{i} = f_{expert function} (C O_{i})
    \end{equation}
    :label: equ:funcexpt

Method Expert COMET
-------------------
:class:`MethodExpert` is designed to evaluate characteristic objects in the :class:`COMET` method using another MCDA methods, such as TOPSIS, VIKOR, PROMETHEE, etc. Those methods require definitions of the criteria weights and types.

If :class:`MethodExpert` is used, then **Step 2** is omitted in the COMET procedure and then in **Step 3** Equation (:eq:`equ:methodexp`) is used instead of (:eq:`equ:sj`).

.. math::
   S J = MCDA\_Method(CO, weights, types)
   :label: equ:methodexp

Structural COMET
-------------------
Structural COMET approach aims to lover the number of pairwise comparisons by splitting the decision problem into smaller problems.

For example, let's suppose that we have a decision problem with 4 criteria A, B, C and D. For each criterion we have define 3 characteristic values, which give as :math:`3^4 = 81` characteristic objects and therefore :math:`\frac{81 \cdot (81 - 1)}{2} = 3240` pairwise comparisons to made.

However, we can split this problem into smaller ones using Structural COMET approach. If we group criteria A and B into sub-problem to get preference :math:`P_{AB}` from it, and then group criteria C, D into sub-problem to calculate preferences :math:`P_{CD}`, we can then identify and use the model :math:`P` which use :math:`P_{AB}` and :math:`P_{CD}` as criteria. This way, we have to identify 3 sub-problems and each of them has :math:`3^2 = 9` characteristic objects that gives as :math:`\frac{9 \cdot (9 - 1)}{2} = 36` pairwise comparison for the single sub-model or :math:`36 \cdot 3 = 108` pairwise comparison to evaluate all three sub-models.

Triads Consistency for MEJ
--------------------------

Let suppose that we have four objects which are pairwise comparison, i.e., A, B, C, and D. Based on this pairwise comparison, and we obtain the following judgment matrix (:eq:`equ:eq11`}):

.. math::
   \begin{array}{ccccc}~~~~~~~~~&~A~&~B~&~C~&~D~\end{array}
.. math::
   MEJ= 
   \begin{array}{c}A\\B\\C\\D\end{array} \left ( \begin{array}{cccc}
   \alpha_{11} & \alpha_{12} & \alpha_{13} & \alpha_{14}\\
   \alpha_{21} & \alpha_{22} & \alpha_{23} & \alpha_{24}\\
   \alpha_{31} & \alpha_{32} & \alpha_{33} & \alpha_{34}\\
   \alpha_{41} & \alpha_{42} & \alpha_{43} & \alpha_{44}
   \end{array} \right )
   :label: equ:eq11

In this case, an expert needs answering to six questions on preferences of the following pairs: :math:`(A, B)`, :math:`(A, C)`, :math:`(A, D)`, :math:`(B, C)`, :math:`(B, D)`, and :math:`(C, D)`. Triad is called a collection consisting of three objects. For this example, we can list four triads: :math:`(A, B, C)`, :math:`(A, B, D)`, :math:`(A, C, D)`, and :math:`(B, C, D)`. In general, the number of all possible triads :math:`(T)` from the :math:`t-element` set can be determined from the formula (:eq:`equ:xsw`}):

.. math::
   T=\frac{t!}{(t-3)!3!}
   :label: equ:xsw


Assuming that each characteristic objects have a certain unknown evaluation (constant over time), the expert's preferences must be a transitive relation. If we take the triad :math:`(A, B, C)` then we can formulate seven rules of transitivity (:eq:`equ:ttt`):

.. math::
   \begin{array}{l}
    if  \quad A>B \quad   and  \quad B>C \quad  then  \quad A>C \\
   { if } \quad A>B \quad  { and } \quad B=C \quad  { then } \quad A>C\\
   { if } \quad A=B \quad  { and } \quad B>C \quad  { then } \quad A>C\\
   { if } \quad A=B \quad  { and } \quad B<C \quad  { then } \quad A<C\\
   { if } \quad A<B \quad  { and } \quad B<C \quad  { then } \quad A<C\\
   { if } \quad A<B \quad  { and } \quad B=C \quad  { then } \quad A<C\\
   { if } \quad A=B \quad  { and } \quad B=C \quad  { then } \quad A=C
   \end{array}
   :label: equ:ttt

Equation (:eq:`equ:xsw`) presents the relationship between the number of characteristic objects (t) and the number of all possible triads (T). The number of all possible triads is much higher than the number of all upper triangular matrix elements. However, equation (:eq:`equ:ttt`}) presents only seven rules, and we have 27 possible. The term that another 20 rules mean inconsistent triads is not right. Therefore, all 27 rules will be analysed in the next subsection concerning the MEJ matrix.

Based on (:eq:`equ:eq11`) and (:eq:`equ:ttt`), we are determined a set of consistent triads :math:`(CO_{i}`, :math:`CO_{j}`, :math:`CO_{k})` for which one of the seven conditions is met (:eq:`equ:w2`). The number of all consistent triads is written as :math:`T_{con}`.

.. math::
    \begin{array}{l}
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.5\\
    \end{array}
   :label: equ:w2

More interesting are the triads, for which it is impossible to determine whether their relationship is logically consistent. At the same time, their inconsistency cannot be demonstrated. Let us assume that for 3 objects :math:`CO_i`, :math:`CO_j` and :math:`CO_k` we know their preference values as :math:`f_{CO_i}=0.67`,  :math:`f_{CO_j}=0.47` :math:`f_{CO_k}=0.52`. Therefore, we get :math:`\alpha_{ij} =1` (`0.67 > 0.47`), :math:`\alpha_{jk}=0` (`0.47<0.52`) and :math:`\alpha_{ik} =1` (`0.67>0.62`). For these triads, a binding conclusion cannot be established. Therefore, these triads will be referred to as unknown. It is worth noting that they cannot influence the decrease of the matrix's consistency because, as the example above shows, they may result from real expert knowledge.  The number of all unknown triads will be written as :math:`T_{unk}`, and each unknown triad must be satisfied one of the following rules (:eq:`equ:w3`}):

.. math::
    \begin{array}{c}
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=1.0\\
    \end{array}
   :label: equ:w3

The next group of triads is inconsistent triads, which we can divide into two subgroups: weak inconsistent and strong inconsistent triads. One more again, let us assume that for 3 objects :math:`CO_i`, :math:`CO_j` and :math:`CO_k` we know their preference values as :math:`f_{CO_i}=0.67`,  :math:`f_{CO_j}=0.66` :math:`f_{CO_k}=0.65`. Then :math:`\alpha_{ij} =1`, :math:`\alpha_{jk}=1` and :math:`\alpha_{ik} =1`. Let suppose that the expert gives the answer that :math:`\alpha_{ik} =0.5`. This answer is inconsistent, but if the expert answers that  :math:`\alpha_{ik} =0` it will be a bigger mistake. Both situations describe inconsistent triads. The weak inconsistent, we can describe as the following rules (:eq:`equ:w4`}):

.. math::
    \begin{array}{l}
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.5\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=0.5\\
    \end{array}
   :label: equ:w4

The number of all weak inconsistent triads is called  :math:`T_{inc}^{weak}` (:eq:`equ:w5`}). Finally, the last group is the strong inconsistent triads, which can be identify by using the following rules (\ref{w5}):

.. math::
    \begin{array}{l}
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=1.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=1.0 \quad { then } \quad \alpha_{i k}=0.0\\
    { if } \quad \alpha_{i j}=0.5 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.5 \quad { then } \quad \alpha_{i k}=1.0\\
    { if } \quad \alpha_{i j}=0.0 \quad  { and } \quad \alpha_{j k}=0.0 \quad { then } \quad \alpha_{i k}=1.0\\
    \end{array}
   :label: equ:w5

The number of all strong inconsistent triads is denoted as :math:`T_{inc}^{strong}`. 
Why are we showing two groups of inconsistent triads? It is more likely for very similar assessment values that an error will be classified as weak, inconsistent triads than as strong inconsistent triads. In this work, both groups will be represented as (:eq:`equ:ty`):

.. math::
    T_{inc}=T_{inc}^{weak}+T_{inc}^{strong}
    :label: equ:ty

Finally, we call :math:`\xi` the coefficient of consistence for the MEJ matrix, and it can be obtained as (:eq:`equ:er`):

.. math::
    \xi=1-\frac{T_{inc}}{T}
   :label: equ:er

Triad Supported COMET
---------------------
The approach implemented in :class:`TriadSupportedExpert` is based on the fact that we can use a partially filled MEJ matrix to fill in the rest. For example, if we asked the expert and got the values :math:`\alpha_{12} = 1` and :math:`\alpha_{25} = 1`. Therefore, we could tell that :math:`\alpha_{15} = 1` because we have a consistent triad like this. If the triad we try to use is inconsistent, we could use values :math:`\alpha_{13}` and :math:`\alpha_{35}` to determine the value of :math:`\alpha_{15}`. This means, that for filling up :math:`\alpha_{ik}` we could use values :math:`\alpha_{ij}` and :math:`\alpha_{jk}`, where :math:`i` and :math:`k` should be chose a priory and the :math:`j \in \{i+1, i+2, i+3, \ldots, k\}`.

The procedure of identification of the MEJ matrix using this expert function is similar to the :class:`ManualExpert` expert function. The user will be queried with pairwise comparison question which should be answered. When it will be possible, part of the MEJ will be filled-in using previous comparison results.

