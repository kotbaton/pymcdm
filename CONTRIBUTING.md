# Contributing to PyMCDM

In this document we describe some rules on contributing to the PyMCDM library.

## Checklist for adding the new MCDA method to the library

Suppose you want to add method XYZ to the library.

* Add implementation of the new method to `pymcdm/methods/xyz.py`. Method should be implemented as a class, with all parameters in constructor. Method's class should be inherited from `MCDA_Method` (`mcda_METHOD.py`). Docstring of the class should contain paper for the reference implementation.

* Add import of the new method in `pymcdm/method/__init__.py` so it could be imported properly with the rest of the method.

* Add the unit test to `test/test_mcdm.py` file. See how test for another methods are made. Test should be based on the scientific paper with numerical example of the method using.

* Add the reference and the method acronym and the full name to the `README.md`. Use APA citation style.

