# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .pairwise_weights_base import PairwiseWeightsBase


class RANCOM(PairwiseWeightsBase):
    """
    A subclass of PairwiseWeightsBase implementing the RANCOM (RANking COMparison) method [#rancom1]_.

    The RANCOM class computes weights for pairwise comparisons based on rankings or user-provided
    input.

    Parameters
    ----------
    ranking : np.ndarray | list | tuple, optional
        Array representing the ranking of objects. Only one of `ranking`, `scoring`,
        `object_names`, `matrix`, or `filename` must be provided.
    scoring : np.ndarray | list | tuple, optional
        Array representing the scoring of objects.
    object_names : list of str, optional
        List of names corresponding to the objects being compared. This triggers
        manual pairwise comparison.
    matrix : np.ndarray | list | tuple, optional
        Predefined pairwise comparison matrix.
    filename : str, optional
        Path to a CSV file containing a pairwise comparison matrix.

    Examples
    --------
    >>> from pymcdm.weights.subjective import RANCOM
    >>> rancom = RANCOM(ranking=[1, 2, 4, 3]) # Identify weights for four criteria based on ranking
    >>> weights = rancom()
    [0.4375 0.3125 0.0625 0.1875]
    >>> rancom = RANCOM(object_names=['Price', 'Mileage', 'HP', 'Year']) # Identify weights based on manual comparisons
    >>> weights = rancom()
    [0.4375 0.3125 0.0625 0.1875]

    References
    ----------
    .. [#rancom1] Więckowski, J., Kizielewicz, B., Shekhovtsov, A., & Sałabun, W. (2023). RANCOM: A novel approach to
                  identifying criteria relevance based on inaccuracy expert judgments. Engineering Applications of
                  Artificial Intelligence, 122, 106114.
    """
    tie_value = 0.5
    user_answer_map = {'0': 0, '1/2': 0.5, '0.5': 0.5, '1': 1}

    def _answer_mapper(self, ans: float) -> float:
        """
        Maps a numerical answer value to its corresponding inverse value.

        In case of RANCOM the mapping is as follows:
        0 -> 1
        0.5 -> 0.5
        1 -> 0

        Parameters
        ----------
        ans : float
            The numerical value to map.

        Returns
        -------
        float
            The inverse value of the input, calculated as `1 - ans`.
        """
        return 1 - ans

    def _matrix_to_weights(self) -> np.ndarray:
        """
        Converts the pairwise comparison matrix into weights.

        Returns
        -------
        np.ndarray
            The normalized weights derived from the pairwise comparison matrix.
        """
        s = np.sum(self.matrix, axis=1)
        return s / s.sum()

    def _compare_ranking(self, i: int, j: int) -> float:
        """
        Compares two objects based on their ranking values.

        In the ranking, smaller values represent better options. The comparison returns:
        - `1` if the first object is ranked better than the second.
        - `0` if the second object is ranked better than the first.
        - `0.5` if the two objects are equally ranked.

        Parameters
        ----------
        i : int
            Index of the first object in the ranking.
        j : int
            Index of the second object in the ranking.

        Returns
        -------
        float
            The result of the comparison: 1, 0.5, or 0.
        """
        # Smaller value in the ranking represent better option
        if self.ranking[i] < self.ranking[j]:
            return 1
        elif self.ranking[i] > self.ranking[j]:
            return 0
        else:
            return 0.5

    @staticmethod
    def _question(a: str, b: str) -> str:
        """
        Generates a question string for comparing two objects.

        The question prompts the user to compare the importance of two objects and choose one of
        the following options:
        - `1`: The first object is more important than the second.
        - `1/2`: The two objects are equally important.
        - `0`: The second object is more important than the first.

        Parameters
        ----------
        a : str
            The name of the first object.
        b : str
            The name of the second object.

        Returns
        -------
        str
            A formatted question string prompting the user to compare the two objects.
        """
        return (f'Please compare two objects:\n'
                f'Choose:\n'
                f'  1: if "{a}" is more important than "{b}";\n' 
                f'1/2: if "{a}" is equally important to "{b}";\n'
                f'  0: if "{b}" is more important than "{a}".')
