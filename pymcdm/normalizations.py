# Copyright (c) 2020 Andrii Shekhovtsov
# Copyright (c) 2021 Bartłomiej Kizielewicz

import numpy as np

__all__ = [
    'minmax_normalization',
    'max_normalization',
    'sum_normalization',
    'vector_normalization',
    'logarithmic_normalization',
    'linear_normalization',
    'nonlinear_normalization',
    'enhanced_accuracy_normalization',
    'zavadskas_turskis_normalization'
]


def minmax_normalization(x, cost=False):
    """Calculate the normalized vector using the min-max method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if np.min(x) == np.max(x):  # If all values are equal
        return np.ones(x.shape)

    if cost:
        return (np.max(x) - x) / (np.max(x) - np.min(x))
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def max_normalization(x, cost=False):
    """Calculate the normalized vector using the max method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return 1 - x / np.max(x)
    return x / np.max(x)


def sum_normalization(x, cost=False):
    """Calculate the normalized vector using the sum method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return (1 / x) / np.sum(1 / x)
    return x / np.sum(x)


def vector_normalization(x, cost=False):
    """Calculate the normalized vector using the vector method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return 1 - (x / np.sqrt(sum(x ** 2)))
    return x / np.sqrt(np.sum(x ** 2))


def logarithmic_normalization(x, cost=False):
    """Calculate the normalized vector using the logarithmic method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    prod = np.prod(x)
    if cost:
        return (1 - (np.log(x) / np.log(prod))) / (x.shape[0] - 1)
    return np.log(x) / np.log(prod)


def linear_normalization(x, cost=False):
    """Calculate the normalized vector using the linear method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return np.min(x) / x
    return x / np.max(x)


def nonlinear_normalization(x, cost=False):
    """Calculate the normalized vector using the nonlinear method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return (np.min(x) / x) ** 3
    return (x / np.max(x)) ** 2


def enhanced_accuracy_normalization(x, cost=False):
    """Calculate the normalized vector using the enhanced accuracy method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return 1 - (x - np.min(x)) / np.sum(x - np.min(x))
    return 1 - (np.max(x) - x) / np.sum(np.max(x) - x)


def zavadskas_turskis_normalization(x, cost=False):
    """Calculate the normalized vector using the Zavadskas-Turskis method.

    Parameters
    ----------
        x : ndarray
            One-dimensional numpy array of values to be normalized

        cost : bool, optional
            Vector type. Default profit type.

    Returns
    -------
        ndarray
            One-dimensional numpy array of normalized values.
    """
    if cost:
        return 1 - np.abs((np.min(x) - x) / np.min(x))
    return 1 - np.abs((np.max(x) - x) / np.max(x))
