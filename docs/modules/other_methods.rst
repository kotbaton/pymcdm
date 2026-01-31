.. _other_methods:

==================
Other MCDM Methods
==================

LoPM Method
============

*Farag (2020)* describes the *Limits on Property* method as a material selection
technique in which performance requirements are defined as **lower limits**,
**upper limits**, and **target values** for relevant properties.

Candidate materials (alternatives) are first screened to ensure that all properties
satisfy the specified bounds. The remaining materials are then ranked using
a merit parameter that incorporates weighting factors reflecting the relative
importance of each property. The merit parameter is defined as:

.. math::

   m = \sum_{i=1}^{n_l} \alpha_i \frac{Y_i}{X_i}
       + \sum_{j=1}^{n_u} \alpha_j \frac{X_j}{Y_j}
       + \sum_{k=1}^{n_t} \alpha_k \left| \frac{X_k}{Y_k} - 1 \right|

where :math:`l`, :math:`u`, and :math:`t` denote lower-limit, upper-limit, and
target-value properties, respectively; :math:`\alpha` are weighting factors;
:math:`X` are candidate material properties; and :math:`Y` are specified limits
or target values. A lower value of :math:`m` indicates a more suitable material.

Cost may be included either as an upper-limit property or as a modifier to the
merit parameter:

.. math::

   m' = m \frac{C_X}{C_Y}

where :math:`C_X` is the candidate material cost and :math:`C_Y` is the specified
cost limit.

**Reference**

Farag, M. M. (2020). *Materials and process selection for engineering design*.
CRC Press.

LMAW Method
===========

*Pamučar et al. (2021)* propose the *Logarithm Methodology of Additive Weights* (LMAW) as
a multi-criteria decision-making (MCDM) method that combines logarithmic
normalization, additive aggregation, and Bonferroni operator to provide stable
and reliable rankings of alternatives. A distinctive feature of LMAW is its logarithmic
framework for determining criteria weights and aggregating performance values, which
contributes to strong resistance to the rank reversal problem in dynamic decision
environments.

Assume a set of :math:`m` alternatives :math:`A_i \ (i=1,\dots,m)` evaluated with respect
to :math:`n` criteria :math:`C_j \ (j=1,\dots,n)`. Criteria weights are denoted by
:math:`w_j`, satisfying :math:`\sum_{j=1}^n w_j = 1`. Criteria may be of *benefit*
(maximization) or *cost* (minimization) type. Evaluations can be quantitative or
qualitative and may involve multiple experts.

Steps of the LMAW Method
------------------------

**Step 1: Form the initial decision matrix**

Alternatives are evaluated against all criteria, producing the initial decision matrix
:math:`X = [\vartheta_{ij}]`. When multiple experts are involved, individual matrices are
aggregated using the Bonferroni mean:

.. math::

   \vartheta_{ij} =
   \left(
   \frac{1}{k(k-1)}
   \sum_{x=1}^{k} (\vartheta_{ij}^{(x)})^{p}
   \sum_{\substack{y=1 \\ y \neq x}}^{k} (\vartheta_{ij}^{(y)})^{q}
   \right)^{\frac{1}{p+q}}

where :math:`p,q \ge 0` are Bonferroni stabilization parameters and :math:`k` is the
number of experts.

**Step 2: Standardize the decision matrix**

The elements of the decision matrix are standardized to obtain
:math:`\tilde{X} = [\tilde{x}_{ij}]`:

- For benefit criteria:

.. math::

   \tilde{\vartheta}_{ij} = \frac{\vartheta_{ij} + \max_i \vartheta_{ij}}{\max_i \vartheta_{ij}}

- For cost criteria:

.. math::

   \tilde{\vartheta}_{ij} = \frac{\vartheta_{ij} + \min_i \vartheta_{ij}}{\vartheta_{ij}}

This ensures comparability of criteria with different units and scales.

**Step 3: Determination of criteria weights**

The criteria weights in the LMAW method are obtained using a **logarithmic priority-based
procedure**, which allows experts to express the relative importance of criteria on a
predefined linguistic scale.

First, each expert :math:`e \ (e=1,\dots,k)` assigns priority values to the criteria,
forming a priority vector:

.. math::

   \mathbf{P}^e = (\gamma_1^e, \gamma_2^e, \dots, \gamma_n^e)

where :math:`\gamma_j^e` denotes the priority of criterion :math:`C_j` given by expert
:math:`e`. Higher values indicate higher importance.

**Step 3.1: Definition of the absolute anti-ideal point**

An absolute anti-ideal point :math:`\gamma_{\text{AIP}}` is introduced to ensure
logarithmic stability. It must be strictly smaller than the smallest priority value in
the priority vector:

.. math::

   \gamma_{\text{AIP}} = \frac{\min_j \gamma_j^e}{s}

where :math:`s` is a constant greater than the logarithm base (for natural logarithms,
:math:`s = 3` is recommended, in this case :math:`\gamma_{\text{AIP}} = 0.5`).

**Step 3.2: Construction of the relation vector**

For each criterion, the relation between its priority value and the absolute anti-ideal
point is calculated as:

.. math::

   \eta_j^e = \frac{\gamma_j^e}{\gamma_{\text{AIP}}}

This yields the relation vector:

.. math::

   \mathbf{R}^e = (\eta_1^e, \eta_2^e, \dots, \eta_n^e)

**Step 3.3: Calculation of criteria weights**

The weight of criterion :math:`C_j` for expert :math:`e` is computed using a logarithmic
transformation:

.. math::

   w_j^e = \frac{\log(\eta_j^e)}{\log\!\left(\prod_{j=1}^{n} \eta_j^e\right)}

When multiple experts participate in the evaluation, the final aggregated criteria weights
:math:`w_j` are obtained by applying the Bonferroni aggregator to the individual expert
weights :math:`w_j^e`:

.. math::

   w_j =
   \left(
   \frac{1}{k(k-1)}
   \sum_{x=1}^{k} \left(w_j^{(x)}\right)^p
   \sum_{\substack{y=1 \\ y \neq x}}^{k} \left(w_j^{(y)}\right)^q
   \right)^{\frac{1}{p+q}}



**Step 4: Construct the weighted matrix**

First, logarithmic normalization of standardized values is performed:

.. math::

   \varphi_{ij} =
   \frac{\ln(\tilde{\vartheta}_{ij})}
        {\ln\!\left(\prod_{i=1}^{m} \tilde{\vartheta}_{ij}\right)}

The weighted matrix :math:`N = [\xi_{ij}]` is then computed as:

.. math::

   \xi_{ij} =
   \frac{2 \varphi_{ij}^{w_j}}{(2 - \varphi_{ij})^{w_j} + \varphi_{ij}^{w_j}}

**Step 5: Compute the final performance score**

The overall performance index of each alternative is obtained by additive aggregation:

.. math::

   Q_i = \sum_{j=1}^{n} \xi_{ij}

Alternatives are ranked in descending order of :math:`Q_i`. A higher value of
:math:`Q_i` indicates a more preferable alternative. Due to its logarithmic weighting
scheme and aggregation structure, the LMAW method demonstrates strong robustness and
resistance to rank reversal.

**Reference**

Pamučar, D., Žižović, M., Biswas, S., & Božanić, D. (2021).
*A new logarithm methodology of additive weights (LMAW) for multi-criteria decision-making:
Application in logistics*. Facta Universitatis, Series: Mechanical Engineering, 19(3), 361–380.
