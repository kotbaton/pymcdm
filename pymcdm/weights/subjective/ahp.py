# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .pairwise_weights_base import PairwiseWeightsBase


class AHP(PairwiseWeightsBase):
    """
    A subclass of PairwiseWeightsBase implementing the AHP (Analytic Hierarchy Process) method [#ahp1]_.

    RI values for determination of the consistency are taken from [#ahp2]_.

    The AHP class computes weights for pairwise comparisons based on rankings or user-provided
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
    >>> from pymcdm.weights.subjective import AHP
    >>> ahp = AHP(ranking=[1, 2, 4, 3]) # Identify weights for four criteria based on ranking
    >>> weights = ahp()
    [0.48144852 0.21998235 0.13073309 0.16783605]
    >>> ahp = AHP(object_names=['Price', 'Mileage', 'HP', 'Year']) # Identify weights based on manual comparisons
    >>> weights = ahp()
    >>> print(weights)
    [0.52407767 0.26268171 0.03742414 0.17581648]
    >>> print(ahp.get_cr())  # To calculate CR use get_cr() method
    0.5021601824872032

    References
    ----------
    .. [#ahp1] Saaty, T. L. (2004). Decision making—the analytic hierarchy and network processes (AHP/ANP).
               Journal of systems science and systems engineering, 13, 1-35.
    .. [#ahp2] Rao Tummala, V. M., & Ling, H. (1998). A note on the computation of the mean random consistency index
               of the analytic hierarchy process (AHP). Theory and decision, 44(3), 221-230.
    """
    tie_value = 1
    user_answer_map = {f'1/{v}': 1 / v for v in range(2, 10)} | {str(v): v for v in range(1, 10)}
    RI_M = [0, 0, 0.5799, 0.8921, 1.1159, 1.2358, 1.3322, 1.3952, 1.4537, 1.4882, 1.5117, 1.5356, 1.5571, 1.5714,
            1.5831]

    def get_cr(self):
        """
        Calculate Consistency Ratio (CR) coefficient based on the created pairwise comparison matrix.

        Raises
        ------
        ValueError
            If matrix is not existed (model is not identified) or if matrix is too big.
        """
        m = self.matrix
        if m is None:
            ValueError('Matrix is not existed. Model if not identified yet!')

        if m.shape[0] < 3:
            return 0
        if m.shape[0] > len(self.RI_M):
            ValueError(f"Can't calculate CR for the matrix of this size. Max size is {len(self.RI_M)}.")

        eig, _ = np.linalg.eig(m)
        lambda_max = max(eig.real)
        ci = (lambda_max - m.shape[0]) / (m.shape[0] - 1)
        ri = AHP.RI_M[m.shape[0] - 1]
        return ci / ri

    def check_cr(self, cr_threshold: float = 0.1):
        """
        Calculate Consistency Ratio (CR) coefficient based on the created pairwise comparison matrix
        and return True if calculated CR is lower than cr_threshold parameter (default is 0.1), or False if bigger,
        indicating if the created matrix should be considered consistent.

        Parameters
        ----------
        cr_threshold : float, optional
            CR threshold which determines if matrix with given CR is consistent (calculated CR is lower than threshold)
            or not (calculated CR is larger than threshold). Default is 0.1.

        Raises
        ------
        ValueError
            If matrix is not existed (model is not identified) or if matrix is too big.
        """
        return self.get_cr() <= cr_threshold

    def _answer_mapper(self, ans: float) -> float:
        """
        Maps a numerical answer value to its corresponding inverse value.

        In case of AHP the mapping is as follows:
        1 -> 1
        2 -> 1/2
        1/2 -> 2
        and so on.

        Parameters
        ----------
        ans : float
            The numerical value to map.

        Returns
        -------
        float
            The inverse value of the input, calculated as `1 / ans`.
        """
        return 1 / ans

    def _matrix_to_weights(self) -> np.ndarray:
        """
        Converts the pairwise comparison matrix into weights.

        Returns
        -------
        np.ndarray
            The normalized weights derived from the pairwise comparison matrix.
        """
        eig, eig_w = np.linalg.eig(self.matrix)
        w = eig_w[:, np.argmax(np.abs(eig))].real
        return w / w.sum()

    def _compare_ranking(self, i: int, j: int) -> float:
        """
        Compares two objects based on their ranking values.

        This function takes into account differences between values in the ranking/scoring.
        If one criterion A has value 9 and criterion B 1 it means that B is nine times better than A.
        Therefore result of the comparison will be A and B will be 1/9.
        In case of A (1) and B (9) the result will be 9, because B is nine times worse than A.

        The differences are limited to 9, to fit in the AHP dictionary.

        Parameters
        ----------
        i : int
            Index of the first object in the ranking.
        j : int
            Index of the second object in the ranking.

        Returns
        -------
        float
            The result of the comparison.
        """
        if self.ranking[i] == self.ranking[j]:
            return 1

        # Find how
        d = int(max(self.ranking[i], self.ranking[j]) / min(self.ranking[i], self.ranking[j]))
        d = min(d, 9)
        # Smaller value in the ranking represent better option
        if self.ranking[i] < self.ranking[j]:
            return d
        else:
            return 1/d

    @staticmethod
    def _question(a: str, b: str) -> str:
        """
        Generates a question string for comparing two objects.

        The question prompts the user to compare the importance of two objects and choose one of
        the options for two criteria a anb b.

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
                f'Choose values in scale from 1 to 9 where:\n'
                f'  1: if "{a}" is equally important to "{b}";\n'
                f'  3: if "{a}" is weakly preferred than to "{b}";\n'
                f'  5: if "{a}" is strongly preferred than to "{b}";\n'
                f'  7: if "{a}" is very strongly preferred than to "{b}";\n'
                f'  9: if "{a}" is extremely more important than "{b}";\n'
                f'OR value in scale 1 to 1/9 where:\n'
                f'  1: if "{b}" is equally important to "{a}";\n'
                f'1/3: if "{b}" is weakly preferred than to "{a}";\n'
                f'1/5: if "{b}" is strongly preferred than to "{a}";\n'
                f'1/7: if "{b}" is very strongly preferred than to "{a}";\n'
                f'1/9: if "{b}" is extremely more important than "{a}".')
