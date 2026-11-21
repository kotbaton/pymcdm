# Contributing to PyMCDM

In this document we describe some rules on contributing to the PyMCDM library.

## Checklist for adding the new MCDA method to the library

Suppose you want to add method XYZ to the library.

* Add implementation of the new method to `pymcdm/methods/xyz.py`. Method should be implemented as a class,
  with all parameters in constructor. Method's class should be inherited from `MCDA_Method` (`mcda_METHOD.py`).
  Docstring of the class should contain paper for the reference implementation.

* Add import of the new method in `pymcdm/method/__init__.py` so it could be imported properly with the rest of the method.

* Add the unit test to a new `test/methods/test_xyz.py` file (one file per method, mirroring `pymcdm/methods/xyz.py`).
  See how tests for other methods are made in the `test/methods/` directory. Test should be based on the scientific
  paper with numerical example of the method using.

* Prefer tests based on original authors and original examples. Add at least one unit test that uses a numerical case
  from an earlier/ foundational paper for the method (not only examples from your own work).

* Add the reference and the method acronym and the full name to the `README.md`. Use APA citation style.

* Add the method to the documentation index `docs/pymcdm.methods.rst` in the same manner as existing methods so it appears in built docs.

* Add a brief description to the User Guide similar to other methods and, if relevant,
  include cross-references to module guides such as `docs/modules/european_school.rst`.

## Additional recommendations for new methods addition

* Avoid duplicating existing utilities. For example, if your method requires a normalization that is already 
  implemented (e.g., sum normalization), verify whether a new normalization is truly different.
  If it is redundant, remove the duplicate implementation and its tests.

* Ensure your implementation follows the original paper's definitions and notation where possible.
  State in the method docstring which reference you used as the authoritative source.
