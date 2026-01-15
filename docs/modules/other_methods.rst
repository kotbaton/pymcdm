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

