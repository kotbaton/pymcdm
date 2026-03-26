# Copyright (c) 2026 Bartłomiej Kizielewicz
import numpy as np

from .pairwise_weights_base import PairwiseWeightsBase


class LLSM(PairwiseWeightsBase):
    """
    A subclass of PairwiseWeightsBase implementing the LLSM
    (Logarithmic Least Squares Method), also known as the
    geometric mean method (GM).

    The method computes weights from a pairwise comparison matrix
    as normalized geometric means of rows.

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
    >>> from pymcdm.weights.subjective import LLSM
    >>> llsm = LLSM(ranking=[1, 2, 4, 3])
    >>> weights = llsm()
    >>> print(weights)

    >>> llsm = LLSM(object_names=['Price', 'Mileage', 'HP', 'Year'])
    >>> weights = llsm()
    >>> print(weights)

    References
    ----------
    .. [#llsm1] Crawford, G., & Williams, C. (1985).
       A Note on the Analysis of Subjective Judgment Matrices.
       Journal of Mathematical Psychology, 29, 387-405.
    """

    tie_value = 1
    user_answer_map = {f'1/{v}': 1 / v for v in range(2, 10)} | {str(v): v for v in range(1, 10)}

    def _answer_mapper(self, ans: float) -> float:
        """
        Maps a numerical answer value to its reciprocal value.

        Parameters
        ----------
        ans : float
            The numerical value to map.

        Returns
        -------
        float
            Reciprocal of the input value.
        """
        return 1 / ans

    def _matrix_to_weights(self) -> np.ndarray:
        """
        Converts the pairwise comparison matrix into weights using LLSM.

        For matrix A = [a_ij], weights are computed as:
            w_i = (prod_j a_ij)^(1/n)
        and then normalized so that sum(w) = 1.

        Returns
        -------
        np.ndarray
            The normalized weights derived from the pairwise comparison matrix.
        """
        m = np.asarray(self.matrix, dtype=float)

        if m.ndim != 2 or m.shape[0] != m.shape[1]:
            raise ValueError("Pairwise comparison matrix must be square.")

        if np.any(m <= 0):
            raise ValueError("All matrix entries must be positive for LLSM.")

        # Numerically stable version of geometric mean:
        # gm_i = exp(mean(log(row_i)))
        log_m = np.log(m)
        w = np.exp(np.mean(log_m, axis=1))

        s = w.sum()
        if np.isclose(s, 0.0):
            raise ValueError("Sum of calculated weights is zero.")

        return w / s

    def get_residual_log_error(self) -> float:
        """
        Returns the mean squared residual in log-space for the LLSM fit.

        For estimated weights w, the fitted consistent matrix is:
            c_ij = w_i / w_j

        The residual measure is the mean of:
            (log(a_ij) - log(c_ij))^2

        Returns
        -------
        float
            Mean squared residual in log-space.
        """
        if self.matrix is None:
            raise ValueError("Matrix is not identified yet.")

        w = self()  # ensures weights are computed
        fitted = np.outer(w, 1 / w)

        residuals = np.log(self.matrix) - np.log(fitted)
        return float(np.mean(residuals ** 2))

    def _compare_ranking(self, i: int, j: int) -> float:
        """
        Compares two objects based on their ranking values.

        This follows the same ranking-to-pairwise logic as in AHP.

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

        d = int(max(self.ranking[i], self.ranking[j]) / min(self.ranking[i], self.ranking[j]))
        d = min(d, 9)

        # Smaller value in the ranking represents a better option
        if self.ranking[i] < self.ranking[j]:
            return d
        else:
            return 1 / d

    @staticmethod
    def _question(a: str, b: str) -> str:
        """
        Generates a question string for comparing two objects.

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
        return (f'Please compare two objects:\\n'
                f'Choose values in scale from 1 to 9 where:\\n'
                f'  1: if "{a}" is equally important to "{b}";\\n'
                f'  3: if "{a}" is weakly preferred than to "{b}";\\n'
                f'  5: if "{a}" is strongly preferred than to "{b}";\\n'
                f'  7: if "{a}" is very strongly preferred than to "{b}";\\n'
                f'  9: if "{a}" is extremely more important than "{b}";\\n'
                f'OR value in scale 1 to 1/9 where:\\n'
                f'  1: if "{b}" is equally important to "{a}";\\n'
                f'1/3: if "{b}" is weakly preferred than to "{a}";\\n'
                f'1/5: if "{b}" is strongly preferred than to "{a}";\\n'
                f'1/7: if "{b}" is very strongly preferred than to "{a}";\\n'
                f'1/9: if "{b}" is extremely more important than "{a}".')