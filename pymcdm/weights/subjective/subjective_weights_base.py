# Copyright (c) 2026 Bartłomiej Kizielewicz

from abc import ABC, abstractmethod
import numpy as np


class SubjectiveWeightsBase(ABC):
    """
    A base class for subjective weighting methods that do not rely on pairwise comparison matrices.

    This abstract base class provides a common interface for subjective weight determination methods
    such as SWARA, FUCOM, BWM, PIPRECIA, SIMOS, LBWA, and others. Subclasses must implement the
    `_calculate_weights` method which contains the specific algorithm logic.

    The weights are computed lazily on first call and cached for subsequent calls. Setting any public attribute
    (e.g. new judgments) clears the cached weights.
    """

    def __init__(self):
        self._weights = None

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        # Cached weights were derived from the previous judgments
        if not name.startswith('_') and '_weights' in self.__dict__:
            super().__setattr__('_weights', None)

    def __call__(self) -> np.ndarray:
        """
        Return weights if already calculated, otherwise calculate and cache them.

        Returns
        -------
        np.ndarray
            Vector of criteria weights summing to 1.
        """
        if self._weights is None:
            self._weights = self._calculate_weights()
        return self._weights

    @abstractmethod
    def _calculate_weights(self) -> np.ndarray:
        """
        Calculate weights based on the method-specific algorithm.

        Returns
        -------
        np.ndarray
            Vector of criteria weights.

        Notes
        -----
        This method must be implemented in subclasses.
        """
        pass
