# Copyright (c) 2024 Andrii Shekhovtsov
import os
from typing import Callable
from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import ArrayLike

from itertools import combinations
from ...validators import validate_pairwise_matrix, validate_scoring


class PairwiseWeightsBase(ABC):
    """
    A base class for managing pairwise comparison weighting methods using different input formats.

    This abstract base class supports the initialization, validation, and processing of
    pairwise comparison data using one of several input options: ranking, scoring, object names,
    pairwise comparison matrices, or a file. It is designed for extension in derived classes,
    which must override its abstract methods.

    Abstract Methods
    -----------------
    _answer_mapper(ans: float) -> float
        Maps a user-provided answer value to its corresponding inverse value.
    _matrix_to_weights() -> np.ndarray
        Calculates the weights based on the pairwise comparison matrix.
    _compare_ranking(i: int, j: int) -> float
        Compares two objects based on their ranking.
    _question(a: str, b: str) -> str
        Generates a question string for comparing two objects during manual comparison process.

    Attributes
    ----------
    tie_value : float or int, optional
        Value representing ties in pairwise comparisons. Default is None.
        This should be defined or overridden in derived classes.
    user_answer_map : dict of str to float or int, optional
        A mapping of user-provided answers to corresponding numerical values.
        This should be defined or overridden in derived classes.
    weights : np.ndarray, optional
        The calculated pairwise comparison weights. Initially set to None.

    Parameters
    ----------
    ranking : ArrayLike, optional
        Array representing the ranking of objects. Only one of `ranking`, `scoring`,
        `object_names`, `matrix`, or `filename` must be provided.
    scoring : ArrayLike, optional
        Array representing the scoring of objects.
    object_names : list of str, optional
        List of names corresponding to the objects being compared. This triggers
        manual pairwise comparison.
    matrix : ArrayLike, optional
        Predefined pairwise comparison matrix.
    filename : str, optional
        Path to a CSV file containing a pairwise comparison matrix.

    Methods
    -------
    __call__() -> np.ndarray
        Generates or retrieves the calculated weights from the pairwise comparison matrix.
    _compare_pairwise(i: int, j: int) -> float
        Performs a pairwise comparison between two objects based on user input.
    _identify(objects: list, comparison_func: Callable) -> np.ndarray
        Constructs a pairwise comparison matrix using the provided objects and a
        comparison function.
    to_csv(filename: str, allow_overwrite: bool = False)
        Saves the pairwise comparison matrix to a CSV file.

    Raises
    ------
    ValueError
        If none or more than one of `ranking`, `scoring`, `object_names`, `matrix`, or
        `filename` is provided.
    ValueError
        If the pairwise comparison matrix fails validation.
    FileExistsError
        If the specified output file already exists and `allow_overwrite` is False.

    Notes
    -----
    - The `tie_value` and `user_answer_map` attributes must be defined in derived classes.
    - Derived classes must override all abstract methods to provide specific functionality.
    - The class supports manual pairwise comparisons, matrix-based identification, and automated
      matrix generation from rankings or scores.
    """
    tie_value: float | int = None
    user_answer_map: dict[str, float | int] = None

    def __init__(self,
                 ranking: ArrayLike = None,
                 scoring: ArrayLike = None,
                 object_names: list[str] = None,
                 matrix: ArrayLike = None,
                 filename: str = None):
        """
        Initializes the PairwiseWeightsBase instance with one of the input formats.

        Parameters
        ----------
        ranking : ArrayLike, optional
            Array representing the ranking of objects. Only one of `ranking`, `scoring`,
            `object_names`, `matrix`, or `filename` must be provided.
        scoring : ArrayLike, optional
            Array representing the scoring of objects.
        object_names : list of str, optional
            List of names corresponding to the objects being compared. This triggers
            manual pairwise comparison.
        matrix : ArrayLike, optional
            Predefined pairwise comparison matrix.
        filename : str, optional
            Path to a CSV file containing a pairwise comparison matrix.

        Raises
        ------
        ValueError
            If none or more than one of `ranking`, `scoring`, `object_names`, `matrix`, or
            `filename` are provided.
        """

        if sum(obj is not None for obj in (ranking, scoring, object_names, matrix, filename)) != 1:
            raise ValueError('One of the arguments `ranking`, `scoring`, `object_names`,'
                             '`matrix` or `filename` should be provided!')

        if scoring is not None:
            scoring = np.array(scoring)  # Make copy here because we will modify it
            validate_scoring(scoring)
            idx = np.argsort(scoring)
            scoring[idx] = scoring[idx][::-1]
            self.ranking = scoring
        elif ranking is not None:
            ranking = np.asarray(ranking)
            validate_scoring(ranking)
            self.ranking = ranking
        else:
            self.ranking = None

        self.object_names = object_names

        if filename is not None:
            matrix = np.loadtxt(filename, delimiter=',')

        if matrix is not None:
            validate_pairwise_matrix(matrix, self.user_answer_map.values(), self._answer_mapper)
            self.matrix = matrix
        else:
            self.matrix = None

        self.weights = None

    def __call__(self) -> np.ndarray:
        # If we already have weights, then just return them
        if self.weights is not None:
            return self.weights

        if self.matrix is None:
            # If we don't have matrix or weights, then calculate matrix and weights
            # either from ranking or from pairwise comparison
            if self.ranking is not None:
                self.matrix = self._identify(self.ranking, self._compare_ranking)
            elif self.object_names is not None:
                self.matrix = self._identify(self.object_names, self._compare_pairwise)

        # Now we should have matrix, therefore we can create weights
        # As the matrix is created with internal functions
        # or validated in init we don't need any validators here
        self.weights = self._matrix_to_weights()
        return self.weights

    def _compare_pairwise(self, i: int, j: int) -> float:
        """
        Performs a pairwise comparison between two objects based on user input.

        Parameters
        ----------
        i : int
            Index of the first object in the pair.
        j : int
            Index of the second object in the pair.

        Returns
        -------
        float
            The user's response, mapped to a numerical value.

        Raises
        ------
        KeyError
            If the user's input is not found in `user_answer_map`.
        """
        print(self._question(self.object_names[i], self.object_names[j]))

        ans = self.user_answer_map.get(input('\nYour answer: ').strip(), None)
        while ans is None:
            print(f'Provide valid option: {self.user_answer_map.keys()}!')
            ans = self.user_answer_map.get(input('\nYour answer: ').strip(), None)
        return ans

    def _identify(self, objects: list, comparison_func: Callable) -> np.ndarray:
        """
        Constructs a pairwise comparison matrix using a list of objects and a comparison function.
        Comparing function is either _compare_pariwise() or _compare_ranking(). This function
        will be applied to objects from `objects`.

        Parameters
        ----------
        objects : list
            A list of objects to compare.
        comparison_func : Callable
            A function to perform pairwise comparisons between objects.

        Returns
        -------
        np.ndarray
            The constructed pairwise comparison matrix.
        """
        n = len(objects)
        matrix = np.diag([float(self.tie_value)] * n)

        for i, j in combinations(range(n), 2):
            ans = comparison_func(i, j)
            matrix[i, j] = ans
            matrix[j, i] = self._answer_mapper(ans)

        return matrix

    def to_csv(self, filename: str, allow_overwrite: bool = False):
        """
        Saves the pairwise comparison matrix to a CSV file.

        Parameters
        ----------
        filename : str
            The name of the file where the matrix will be saved.
        allow_overwrite : bool, optional
            If `True`, allows overwriting of existing files. Default is `False`.

        Raises
        ------
        ValueError
            If the pairwise comparison matrix is not identified yet.
        FileExistsError
            If the specified file already exists and `allow_overwrite` is `False`.
        """
        if self.matrix is None:
            raise ValueError('Matrix is not identified yet.')

        if not filename.endswith('.csv'):
            filename = filename + '.csv'

        if os.path.exists(filename) and not allow_overwrite:
            raise FileExistsError(f'{filename} is exist! To override run the method with allow_overwrite=True.')

        np.savetxt(filename, self.matrix, delimiter=',', fmt='%0.6f')

    @abstractmethod
    def _answer_mapper(self, ans: float) -> float:
        """
        Maps a user-provided answer value to its corresponding inverse or paired value.

        For example, if we have values {0, 0.5, 1} as possible answers, it should map 0 to 1,
        1 to 0 and so on.

        Parameters
        ----------
        ans : float
            The numerical value to map.

        Returns
        -------
        float
            The mapped numerical value (usually reversed value for matrix).

        Notes
        -----
        This method must be implemented in subclasses.
        """

        pass

    @abstractmethod
    def _matrix_to_weights(self) -> np.ndarray:
        """
        Converts the pairwise comparison matrix into weights.

        Returns
        -------
        np.ndarray
            The calculated weights based on the pairwise comparison matrix.

        Notes
        -----
        This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def _compare_ranking(self, i: int, j: int) -> float:
        """
        Compares two objects based on their positions in the ranking.

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

        Notes
        -----
        This method must be implemented in subclasses.
        """
        pass

    @staticmethod
    @abstractmethod
    def _question(a: str, b: str) -> str:
        """
        Generates a question string for comparing two objects.
        This is used during manual identification process.

        Parameters
        ----------
        a : str
            The name of the first object.
        b : str
            The name of the second object.

        Returns
        -------
        str
            A question string prompting the user to compare the two objects.

        Notes
        -----
        This method must be implemented in subclasses.
        """
        pass

