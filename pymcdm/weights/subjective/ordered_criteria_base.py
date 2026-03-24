# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .subjective_weights_base import SubjectiveWeightsBase


class OrderedCriteriaWeightsBase(SubjectiveWeightsBase):
    """
    Base class for subjective weighting methods that operate on a ranked/ordered
    sequence of criteria indices (e.g. SWARA, PIPRECIA, FUCOM).

    Provides common validation of the ordering vector and a helper to map
    locally-computed weights back to original criterion indices.

    Parameters
    ----------
    order : np.ndarray | list | tuple
        Criteria indices in decreasing order of importance.
    **kwargs
        Forwarded to :class:`SubjectiveWeightsBase` (cooperative inheritance).
    """

    def __init__(self, order, **kwargs):
        super().__init__(**kwargs)
        self.order = np.asarray(order, dtype=int)
        self._validate_order()

    def _validate_order(self):
        """Validate the ordering vector."""
        if self.order.ndim != 1:
            raise ValueError("order must be one-dimensional.")
        if len(self.order) == 0:
            raise ValueError("order cannot be empty.")
        if np.any(self.order < 0):
            raise ValueError("Criterion indices in order must be >= 0.")
        if len(np.unique(self.order)) != len(self.order):
            raise ValueError("order cannot contain duplicate indices.")
        if np.max(self.order) != len(self.order) - 1:
            raise ValueError("order must contain every criterion index from 0 to "
                             f"{len(self.order) - 1} exactly once, but got {self.order.tolist()}.")

    @property
    def n(self):
        """Number of criteria in the ordering."""
        return len(self.order)

    @property
    def n_criteria(self):
        """Total number of criteria (max index + 1)."""
        return int(np.max(self.order)) + 1

    def _reindex_from_order(self, ordered_weights: np.ndarray) -> np.ndarray:
        """
        Map weights computed in ranking order back to original criterion indices.

        Parameters
        ----------
        ordered_weights : np.ndarray
            Weights in the same order as ``self.order``.

        Returns
        -------
        np.ndarray
            Weight vector of length ``n_criteria``, indexed by criterion id.
        """
        w = np.zeros(self.n_criteria, dtype=float)
        w[self.order] = ordered_weights
        return w
