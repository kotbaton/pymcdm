# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .subjective_weights_base import SubjectiveWeightsBase


class DecisionMatrixWeightsBase(SubjectiveWeightsBase):
    """
    Base class for subjective weighting methods that require a decision matrix
    (alternatives × criteria) as input (e.g. ITARA, OWCM).

    Overrides ``__call__`` to accept an optional ``matrix`` argument, storing
    it for the subsequent weight calculation.

    .. note::
        This class intentionally extends the ``__call__`` signature of
        :class:`SubjectiveWeightsBase` to accept a ``matrix`` parameter.
        Methods in this family may require the matrix either at construction
        time or at call time.

    Parameters
    ----------
    matrix : np.ndarray, optional
        Decision matrix of shape ``(m, n)``.  If provided, it is stored and
        validated immediately.
    **kwargs
        Forwarded to :class:`SubjectiveWeightsBase` (cooperative inheritance).
    """

    def __init__(self, matrix=None, **kwargs):
        super().__init__(**kwargs)
        self._matrix = None
        if matrix is not None:
            self.set_matrix(matrix)

    def set_matrix(self, matrix):
        """
        Store and validate a new decision matrix, clearing cached weights.

        Parameters
        ----------
        matrix : np.ndarray | list | tuple
            Decision matrix of shape ``(m, n)``.
        """
        matrix = np.asarray(matrix, dtype=float)
        if matrix.ndim != 2:
            raise ValueError(
                f"Decision matrix must be 2-dimensional, got shape {matrix.shape}."
            )
        self._matrix = matrix
        self._weights = None  # invalidate cache

    def __call__(self, matrix=None) -> np.ndarray:
        """
        Calculate and return criteria weights.

        Parameters
        ----------
        matrix : np.ndarray, optional
            If provided, replaces the stored matrix and clears the cache.

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        if matrix is not None:
            self.set_matrix(matrix)
        if self._matrix is None:
            raise ValueError("Decision matrix must be provided.")
        return super().__call__()

    @property
    def matrix(self):
        """The currently stored decision matrix."""
        return self._matrix

    @property
    def n_criteria(self):
        """Number of criteria (columns in the decision matrix)."""
        if self._matrix is None:
            raise ValueError("Decision matrix has not been set yet.")
        return self._matrix.shape[1]
