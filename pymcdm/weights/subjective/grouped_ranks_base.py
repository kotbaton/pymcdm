# Copyright (c) 2026 Bartłomiej Kizielewicz

import numpy as np
from .subjective_weights_base import SubjectiveWeightsBase


def _validate_criteria(criteria, name):
    """ Check that every criterion index from 0 to n - 1 is given exactly once. """
    criteria = list(criteria)
    if not criteria:
        raise ValueError(f'{name} cannot be empty.')
    if any(int(c) != c or c < 0 for c in criteria):
        raise ValueError(f'Criterion indices in {name} must be non-negative integers.')
    if len(set(criteria)) != len(criteria):
        raise ValueError(f'{name} cannot contain duplicate criterion indices.')
    if max(criteria) != len(criteria) - 1:
        raise ValueError(f'{name} must contain every criterion index from 0 to {len(criteria) - 1} exactly once, '
                         f'but got {sorted(criteria)}.')


class GroupedRanksBase(SubjectiveWeightsBase):
    """
    Base class for subjective weighting methods that operate on ranked groups
    of criteria with white-card gaps (e.g. SIMOS, SRF).

    Provides common parsing of nested rank lists, validation of the gap vector,
    and a helper to expand per-rank values to per-criterion weights.

    Parameters
    ----------
    ranks : list | tuple
        Criteria indices from least to most important.  Use inner lists for
        ties (e.g. ``[[0, 1], 2, 3]``).
    gaps : np.ndarray | list | tuple
        Number of white cards between consecutive rank positions.
        Length must be ``number_of_rank_groups - 1``.  All values >= 0.
    **kwargs
        Forwarded to :class:`SubjectiveWeightsBase` (cooperative inheritance).
    """

    def __init__(self, ranks, gaps, **kwargs):
        super().__init__(**kwargs)
        self.ranks = ranks
        self.gaps = np.asarray(gaps, dtype=float)
        self.positions = self._parse_ranks(ranks)
        self._validate_gaps()

    @staticmethod
    def _parse_ranks(ranks):
        """Normalise rank input into a list of lists."""
        positions = []
        for item in ranks:
            if isinstance(item, (list, tuple, np.ndarray)):
                positions.append(list(item))
            else:
                positions.append([item])
        return positions

    def _validate_gaps(self):
        """Validate the gap vector against the rank groups."""
        if len(self.gaps) != len(self.positions) - 1:
            raise ValueError(
                f'gaps should have length {len(self.positions) - 1} '
                f'(number of rank groups - 1), '
                f'but has length {len(self.gaps)}.'
            )
        if np.any(self.gaps < 0) or np.any(self.gaps != np.round(self.gaps)):
            raise ValueError('All values in gaps (numbers of white cards) must be non-negative integers.')
        _validate_criteria([c for group in self.positions for c in group], 'ranks')

    @property
    def n_criteria(self):
        """Total number of criteria (max index + 1)."""
        return max(c for group in self.positions for c in group) + 1

    def _expand_rank_values(self, rank_values: np.ndarray) -> np.ndarray:
        """
        Map one value per rank group to a per-criterion weight vector.

        Parameters
        ----------
        rank_values : np.ndarray
            One value per rank group (length = number of groups).

        Returns
        -------
        np.ndarray
            Weight vector of length ``n_criteria``, indexed by criterion id.
        """
        w = np.zeros(self.n_criteria, dtype=float)
        for r_idx, group in enumerate(self.positions):
            for criterion in group:
                w[criterion] = rank_values[r_idx]
        return w
