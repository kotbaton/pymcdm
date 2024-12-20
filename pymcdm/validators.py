# Copyright (c) 2024 Andrii Shekhovtsov
# Copyright (c) 2024 Bartłomiej Kizielewicz

from itertools import combinations
import numpy as np


def param_validator(param: float, name: str):
    """
    Validates if the parameter of a Multi-Criteria Decision Analysis (MCDA) method is within the range [0, 1].

    Parameters
    ----------
    param : float
        The parameter value to validate. Must be a numeric value within the range [0, 1].
    name : str
        The name of the parameter, used for constructing an informative error message if validation fails.

    Returns
    -------
    None
        This function does not return a value. It raises an error if the validation fails.

    Raises
    ------
    ValueError
        If `param` is not within the range [0, 1], a `ValueError` is raised with a descriptive error message.

    Examples
    --------
    >>> param_validator(0.5, "alpha") # No output, as validation passes.

    >>> param_validator(1.5, "alpha")
    Traceback (most recent call last):
        ...
    ValueError: alpha should be in range [0, 1], but its value is 1.5.
    """
    if not (0 <= param <= 1):
        raise ValueError(f'{name} should be in range [0, 1], but its value is {param}.')


def array_dimension_validator(array: np.ndarray, ndim: int, name: str) -> None:
    """
    Validates that the given array has the expected number of dimensions.

    Parameters
    ----------
    array : numpy.ndarray
        The array to validate. Must be a NumPy array.
    ndim : int
        The expected number of dimensions of the array.
    name : str
        The name of the array, used for constructing a descriptive error message if validation fails.

    Returns
    -------
    None
        This function does not return a value. It raises an error if the validation fails.

    Raises
    ------
    ValueError
        If the number of dimensions of `array` does not match `ndim`, a `ValueError` is
        raised with a descriptive error message.

    Examples
    --------
    >>> import numpy as np
    >>> array = np.array([[1, 2], [3, 4]])
    >>> array_dimension_validator(array, 2, "example_array") # No output, as validation passes.

    >>> array_dimension_validator(array, 3, "example_array")
    Traceback (most recent call last):
        ...
    ValueError: example_array should be 3d array, but it has shape (2, 2).
    """
    if len(array.shape) != ndim:
        raise ValueError(f'{name} should be {ndim}d array, but it has shape {array.shape}.')


def matrix_ref_point_validator(matrix: np.ndarray, ref_point: np.ndarray) -> None:
    """
    Validates that the reference point matches the criteria of the given decision matrix.

    This function checks two conditions:

    1. The `ref_point` must be a one-dimensional array.
    2. The length of the `ref_point` must match the number of columns (criteria) in the `matrix`.

    Parameters
    ----------
    matrix : numpy.ndarray
        A decision matrix where rows represent alternatives and columns represent criteria.
    ref_point : numpy.ndarray
        A reference point to validate. Must be a one-dimensional array,
        with its length matching the number of criteria in the matrix.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `ref_point` is not one-dimensional or if its length does not match
        the number of columns in `matrix`, a `ValueError` is raised.

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[1, 2, 3], [4, 5, 6]])
    >>> ref_point = np.array([0.5, 0.6, 0.7])
    >>> matrix_ref_point_validator(matrix, ref_point) # No output, as validation passes.

    >>> invalid_ref_point = np.array([0.5, 0.6])
    >>> matrix_ref_point_validator(matrix, invalid_ref_point)
    Traceback (most recent call last):
        ...
    ValueError: Len of the ref_point 2 should be the same as number of the criteria 3.
    """
    array_dimension_validator(ref_point, 1, 'ref_point')

    if ref_point.shape[0] != matrix.shape[1]:
        raise ValueError(
            f'Len of the ref_point {ref_point.shape[0]} should be the same'
            f'as number of the criteria {matrix.shape[1]}.')


def matrix_cvalues_validator(matrix: np.ndarray, cvalues: list[tuple] | list[list] | np.ndarray):
    """
    Validates that the characteristic values (`cvalues`) align with the criteria in the decision matrix.

    This function performs two validations:

        1. Ensures the number of criteria (columns) in the `matrix` matches
           the number of characteristic values in `cvalues`.
        2. Ensures that each value in the decision matrix falls within the corresponding bounds defined in `cvalues`.

    Parameters
    ----------
    matrix : numpy.ndarray
        A decision matrix where rows represent alternatives and columns represent criteria.
    cvalues : list[tuple] | list[list] | np.ndarray
        A list where each element is a tuple defining the characteristic values for the corresponding criterion.
        Each tuple should be of the form `(lower_bound, ..., other_cv, ... upper_bound)`.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If the number of criteria in `matrix` does not match the length of `cvalues`.
        If any value in `matrix` is outside the bounds defined in `cvalues`.

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[0.2, 0.5, 0.8], [0.3, 0.4, 0.7]])
    >>> cvalues = [(0, 1), (0, 0.6), (0.5, 1)]
    >>> matrix_cvalues_validator(matrix, cvalues) # No output, as validation passes.

    >>> invalid_matrix = np.array([[0.2, 0.7, 0.8], [0.3, 0.4, 1.2]])
    >>> matrix_cvalues_validator(invalid_matrix, cvalues)
    Traceback (most recent call last):
        ...
    ValueError: Some criteria values in alternative with index 0 are not in problem's domain, i.e. there are values that are bigger or smaller than bounds defined in cvalues.
    """
    if matrix.shape[1] != len(cvalues):
        ValueError(f'Number of criteria in matrix ({matrix.shape[1]}) is different from number of criteria in '
                   f'the characteristic values ({len(cvalues)}), but those values should be the same.')

    for i, alt in enumerate(matrix):
        if any(a < cv[0] or cv[-1] < a for a, cv in zip(alt, cvalues)):
            ValueError(f'Some criteria values in alternative with index {i} are not in problem\'s domain, '
                       'i.e. there are values that are bigger or smaller then bounds defined in cvalues.')


def ref_ideal_bounds_validator(ref_ideal: np.ndarray, bounds: np.ndarray):
    """
    Validates that the reference ideal (`ref_ideal`) aligns with the given bounds for each criterion.

    This function performs the following validations:

        1. Ensures the `ref_ideal` has a shape of `(M, 2)`, where `M` is the number of criteria,
           and each criterion is defined by a pair of identical values (e.g., `[0, 0]`).
        2. Ensures the shapes of `ref_ideal` and `bounds` are identical.
        3. Verifies that all `ref_ideal` values lie within the respective bounds
           and that the `ref_ideal` values are in ascending order `[min, max]`.

    Parameters
    ----------
    ref_ideal : np.ndarray
        A 2D array with shape `(M, 2)`, where each row corresponds to the reference ideal for a criterion.
        Each criterion's values should be ordered as `[min, max]`.
    bounds : np.ndarray
        A 2D array with shape `(M, 2)`, where each row defines the minimum and maximum allowed values for a criterion.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `ref_ideal` does not have the shape `(M, 2)`.
        If `ref_ideal` and `bounds` do not have the same shape.
        If any value in `ref_ideal` is outside the corresponding bounds.
        If the `ref_ideal` values are not ordered as `[min, max]`.

    Examples
    --------
    >>> import numpy as np
    >>> ref_ideal = np.array([[0, 0], [1, 1], [0.5, 0.5]])
    >>> bounds = np.array([[0, 0], [0, 1], [0, 1]])
    >>> ref_ideal_bounds_validator(ref_ideal, bounds) # No output, as validation passes.

    >>> invalid_ref_ideal = np.array([[0, 1], [1, 0], [0.5, 0.6]])
    >>> ref_ideal_bounds_validator(invalid_ref_ideal, bounds)
    Traceback (most recent call last):
        ...
    ValueError: ref_ideal values should be in range of min and max values (bounds) for each criterion...
    """
    if ref_ideal.shape[1] != 2:
        raise ValueError('Shape of the ref_ideal should be (M, 2),'
                         ' where M is a number of criteria. Single'
                         ' values should be provided duplicated, e.g.'
                         ' 0 should be added as [0, 0].')

    if ref_ideal.shape != bounds.shape:
        raise ValueError('Bounds and ref_ideal should have equal'
                         ' shapes.')

    min_, max_ = bounds[:, 0], bounds[:, 1]
    ref_min, ref_max = ref_ideal[:, 0], ref_ideal[:, 1]
    if (not np.all(np.logical_and(min_ <= ref_min, ref_max <= max_))) or np.any(ref_min > ref_max):
        raise ValueError('ref_ideal values should be in range of min and max values (bounds) for each criterion.'
                         'ref_ideal values should be ordered in [min, max] order.')


def matrix_bounds_validator(matrix: np.ndarray, bounds: np.ndarray):
    """
    Validates that all values in the decision matrix lie within the specified bounds for each criterion.

    This function checks that every value in each alternative (row of the matrix) is within the corresponding 
    minimum and maximum bounds defined for each criterion.

    Parameters
    ----------
    matrix : numpy.ndarray
        A 2D array where each row represents an alternative and each column represents a criterion.
    bounds : numpy.ndarray
        A 2D array with shape `(N, 2)`, where `N` is the number of criteria. Each row defines the minimum
        and maximum allowed values for a criterion as `[min, max]`.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If any value in `matrix` lies outside the bounds defined by `bounds`.

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[0.5, 0.7], [0.2, 0.6]])
    >>> bounds = np.array([[0, 1], [0.5, 1]])
    >>> matrix_bounds_validator(matrix, bounds) # No output, as validation passes.

    >>> invalid_matrix = np.array([[0.5, 1.2], [0.2, 0.6]])
    >>> matrix_bounds_validator(invalid_matrix, bounds)
    Traceback (most recent call last):
        ...
    ValueError: Every alternative values should be in range of min and max values (bounds) for each criterion.
    Some values of alternative with index 0 is out of range.
    """
    min_, max_ = bounds[:, 0], bounds[:, 1]

    for i, alt in enumerate(matrix):
        if not np.all(np.logical_and(min_ <= alt, alt <= max_)):
            raise ValueError('Every alternative values should be in range of min and max values (bounds) '
                             f'for each criterion. Some values of alternative with index {i} is out of range.')


def cvalues_validator(cvalues: list | tuple | np.ndarray):
    """
    Validates the characteristic values (`cvalues`) for each criterion.

    This function ensures that:

    1. Each element in `cvalues` is an iterable (e.g., a list, tuple, or numpy array).
    2. Each criterion has at least two characteristic values.
    3. The characteristic values for each criterion are sorted in strictly ascending order (no duplicates).

    Parameters
    ----------
    cvalues : list of iterable
        A list where each element is an iterable (e.g., list, tuple, or numpy array) representing the 
        characteristic values for a criterion.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If any element in `cvalues` is not iterable.
        If any criterion has fewer than two characteristic values.
        If the characteristic values for any criterion are not sorted in strictly ascending order.

    Examples
    --------
    >>> cvalues = [[0, 0.5, 1], [10, 20, 30]]
    >>> cvalues_validator(cvalues) # No output, as validation passes.

    >>> invalid_cvalues = [[0, 1], [10, 10, 30]]
    >>> cvalues_validator(invalid_cvalues)
    Traceback (most recent call last):
        ...
    ValueError: Characteristic values must be sorted in ascending order and does not contain repeated elements.
    Check criterion with index 1.

    >>> non_iterable_cvalues = [0, [10, 20]]
    >>> cvalues_validator(non_iterable_cvalues)
    Traceback (most recent call last):
        ...
    ValueError: Characteristic values should be represented with nested lists or other iterables.
    However, "0" is not iterable.
    """
    for i, cv in enumerate(cvalues):
        if not isinstance(cv, (np.ndarray, list, tuple)):
            raise ValueError(
                'Characteristic values should be represented with nested lists or other iterables.'
                f' However, "{cv}" is not iterable.'
            )

        if len(cv) < 2:
            raise ValueError(
                f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index '
                f'{i}.'
            )

        if any(cv[j] >= cv[j + 1] for j in range(len(cv) - 1)):
            raise ValueError(
                f'Characteristic values must be sorted in ascending order and does not contain repeated elements. '
                f'Check criterion with index {i}.'
            )


def bounds_validator(bounds: np.ndarray):
    """
    Validates the bounds array to ensure it contains valid minimum and maximum values for each criterion.

    This function performs the following validations:

    1. Ensures `bounds` is a two-dimensional array with shape `(N, 2)`, where `N` is the number of criteria.
    2. Ensures that for each row in `bounds`, the first value (minimum) is less than the second value (maximum).

    Parameters
    ----------
    bounds : np.ndarray
        A 2D array where each row defines the minimum and maximum values for a criterion in the format `[min, max]`.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `bounds` is not a 2D array with shape `(N, 2)`.
        If any row in `bounds` does not follow the `[min, max]` order (i.e., `min` >= `max`).

    Examples
    --------
    >>> import numpy as np
    >>> bounds = np.array([[0, 1], [10, 20], [5, 15]])
    >>> bounds_validator(bounds) # No output, as validation passes.

    >>> invalid_bounds = np.array([[0, 1], [20, 10], [5, 5]])
    >>> bounds_validator(invalid_bounds)
    Traceback (most recent call last):
        ...
    ValueError: Bounds should contain min and max values for each criterion, in order [min, max] in each row.
    """
    array_dimension_validator(bounds, 2, 'bounds')

    min_, max_ = bounds[:, 0], bounds[:, 1]

    if np.any(min_ >= max_):
        raise ValueError('Bounds should contain min and max values for each criterion, '
                         'in order [min, max] in each row.')


def esp_bounds_validator(esp: np.ndarray, bounds: np.ndarray):
    """
    Validates that the ESP (Expected Solution Point) values lie within the specified bounds for each criterion.

    This function ensures the following:

    1. The `esp` array is one-dimensional.
    2. Each value in the `esp` array lies within the corresponding minimum and maximum bounds defined in `bounds`.

    Parameters
    ----------
    esp : numpy.ndarray
        A 1D array representing the ESP values for each criterion.
    bounds : numpy.ndarray
        A 2D array with shape `(N, 2)`, where `N` is the number of criteria. Each row defines the minimum
        and maximum values for a criterion as `[min, max]`.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `esp` is not one-dimensional.
        If any value in `esp` lies outside the bounds defined by `bounds`.

    Examples
    --------
    >>> import numpy as np
    >>> esp = np.array([0.5, 0.7, 0.9])
    >>> bounds = np.array([[0, 1], [0.5, 1], [0, 1]])
    >>> esp_bounds_validator(esp, bounds) # No output, as validation passes.

    >>> invalid_esp = np.array([0.5, 1.2, 0.9])
    >>> esp_bounds_validator(invalid_esp, bounds)
    Traceback (most recent call last):
        ...
    ValueError: ESP values should be in range of min and max values (bounds) for each criterion.
    """
    array_dimension_validator(esp, 1, 'esp')

    min_, max_ = bounds[:, 0], bounds[:, 1]

    if not np.all(np.logical_and(min_ <= esp, esp <= max_)):
        raise ValueError('ESP values should be in range of min and max values (bounds) for each criterion.')


def matrix_validator(matrix: np.ndarray, types: list[int]):
    """
    Validates the decision matrix and checks for dominant or dominated alternatives.

    This function ensures that:

        1. The decision `matrix` is two-dimensional.
        2. It identifies and raises errors if any alternative is either dominant or dominated, which could cause
           numerical errors in some methods.

           - Dominant alternatives have the best values for all criteria.
           - Dominated alternatives have the worst values for all criteria.

    Parameters
    ----------
    matrix : numpy.ndarray
        A 2D array where each row represents an alternative, and each column represents a criterion.
    types : list of int
        A list indicating the type of optimization for each criterion. Each element should be:
        - `1` for maximization (profit) criteria.
        - `-1` for minimization (cost) criteria.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `matrix` is not two-dimensional.
        If any alternative in `matrix` is dominant (best in all criteria).
        If any alternative in `matrix` is dominated (worst in all criteria).

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[1, 2], [3, 4], [2, 1]])
    >>> types = [1, -1]  # Maximize first criterion, minimize second criterion
    >>> matrix_validator(matrix, types) # No output, as validation passes.

    >>> dominant_matrix = np.array([[5, 10], [1, 2], [3, 4]])
    >>> types = [1, 1]
    >>> matrix_validator(dominant_matrix, types)
    Traceback (most recent call last):
        ...
    ValueError: Alternatives with indices [0] are dominant. Consider removing them,
    as such alternatives can cause numerical errors in some methods.

    >>> dominated_matrix = np.array([[1, 2], [5, 10], [3, 4]])
    >>> matrix_validator(dominated_matrix, types)
    Traceback (most recent call last):
        ...
    ValueError: Alternatives with indices [0] are dominated. Consider removing them,
    as such alternatives can cause numerical errors in some methods.
    """
    array_dimension_validator(matrix, 2, 'Matrix')

    max_alt = np.max(matrix, axis=0)
    min_alt = np.min(matrix, axis=0)

    dominant = [max_alt[i] if types[i] == 1 else min_alt[i]
                for i in range(matrix.shape[1])]
    dominated = [max_alt[i] if types[i] == -1 else min_alt[i]
                 for i in range(matrix.shape[1])]

    dominant_alts, = np.where([np.all(dominant == alt) for alt in matrix])
    if dominant_alts.size > 0:
        raise ValueError(f'Alternatives with indices {list(dominant_alts)} are dominant. Consider removing them,'
                         'as such alternatives can cause numerical errors in some methods.')

    dominated_alts, = np.where([np.all(dominated == alt) for alt in matrix])
    if dominated_alts.size > 0:
        raise ValueError(f'Alternatives with indices {list(dominated_alts)} are dominated. Consider removing them,'
                         'as such alternatives can cause numerical errors in some methods.')


def weights_validator(matrix: np.ndarray, weights: np.ndarray):
    """
    Validates the weights assigned to the criteria in a decision matrix.

    This function ensures the following:

    1. The `weights` array is one-dimensional.
    2. The number of weights matches the number of criteria (columns) in the decision matrix.
    3. All weights are positive, and their sum is approximately 1 (within a tolerance of 0.01).

    Parameters
    ----------
    matrix : np.ndarray
        A 2D array where each row represents an alternative and each column represents a criterion.
    weights : np.ndarray
        A 1D array where each element represents the weight assigned to a criterion.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `weights` is not one-dimensional.
        If the number of weights does not match the number of criteria in `matrix`.
        If any weight is non-positive.
        If the sum of weights deviates from 1 by more than 0.01.

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[1, 2, 3], [4, 5, 6]])
    >>> weights = np.array([0.2, 0.3, 0.5])
    >>> weights_validator(matrix, weights) # No output, as validation passes.

    >>> invalid_weights = np.array([0.2, 0.3, 0.4])
    >>> weights_validator(matrix, invalid_weights)
    Traceback (most recent call last):
        ...
    ValueError: Weights should be positive and its sum should be equal one. Now, sum of the weights is 0.9.
    """
    array_dimension_validator(weights, 1, 'Weights')

    if matrix.shape[1] != weights.shape[0]:
        raise ValueError('Number of criteria should be same as number of weights.')

    if abs(weights.sum() - 1) >= 0.01 or np.any(weights <= 0):
        raise ValueError('Weights should be positive and its sum should be equal one. Now, sum of the weights is '
                         f'{weights.sum()}.')


def types_validator(matrix: np.ndarray, types: np.ndarray):
    """
    Validates the types array used to define optimization directions for each criterion in a decision matrix.

    This function ensures the following:

    1. The `types` array is one-dimensional.
    2. The number of elements in `types` matches the number of criteria (columns) in the decision matrix.
    3. The `types` array contains only the values `1` (for maximization) and `-1` (for minimization).

    Parameters
    ----------
    matrix : numpy.ndarray
        A 2D array where each row represents an alternative and each column represents a criterion.
    types : numpy.ndarray
        A 1D array where each element represents the optimization direction for a criterion:
        - `1` for maximization (profit).
        - `-1` for minimization (cost).

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If `types` is not one-dimensional.
        If the number of elements in `types` does not match the number of criteria in `matrix`.
        If `types` contains values other than `1` or `-1`.

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[1, 2], [3, 4]])
    >>> types = np.array([1, -1])  # Maximize first criterion, minimize second criterion
    >>> types_validator(matrix, types) # No output, as validation passes.

    >>> invalid_types = np.array([1, 0])
    >>> types_validator(matrix, invalid_types)
    Traceback (most recent call last):
        ...
    ValueError: Types array should only contain values -1 or 1.
    """
    array_dimension_validator(types, 1, 'Types')

    if matrix.shape[1] != types.shape[0]:
        raise ValueError('Number of criteria should be same as number of criteria types.')

    if np.sum(np.abs(types)) != types.shape[0]:
        raise ValueError('Types array should only contains values -1 '
                         'or 1.')


def validate_decision_problem(matrix: np.ndarray, weights: np.ndarray, types: np.ndarray):
    """
    Validates the components of a decision problem, including the decision matrix, weights, and types.

    This function performs the following validations:

        1. Ensures the decision matrix is valid
           and does not contain dominant or dominated alternatives (`matrix_validator`).
        2. Validates the weights array to ensure positivity, correct dimensionality,
           and that the sum is approximately 1 (`weights_validator`).
        3. Validates the types array to ensure it is one-dimensional,
           matches the number of criteria, and contains only `1` or `-1` values (`types_validator`).

    Parameters
    ----------
    matrix : numpy.ndarray
        A 2D array where each row represents an alternative and each column represents a criterion.
    weights : numpy.ndarray
        A 1D array where each element represents the weight assigned to a criterion.
    types : numpy.ndarray
        A 1D array where each element represents the optimization direction for a criterion:
        - `1` for maximization (profit).
        - `-1` for minimization (cost).

    Returns
    -------
    None
        This function does not return a value. It raises an error if any of the validations fail.

    Raises
    ------
    ValueError
        If the decision matrix fails validation (`matrix_validator`).
        If the weights array fails validation (`weights_validator`).
        If the types array fails validation (`types_validator`).

    Examples
    --------
    >>> import numpy as np
    >>> matrix = np.array([[1, 2], [3, 4]])
    >>> weights = np.array([0.5, 0.5])
    >>> types = np.array([1, -1])  # Maximize first criterion, minimize second criterion
    >>> validate_decision_problem(matrix, weights, types)
    # No output, as validation passes.

    >>> invalid_weights = np.array([0.5, 0.4])
    >>> validate_decision_problem(matrix, invalid_weights, types)
    Traceback (most recent call last):
        ...
    ValueError: Weights should be positive and its sum should be equal one. Now, sum of the weights is 0.9.
    """
    matrix_validator(matrix, types)
    weights_validator(matrix, weights)
    types_validator(matrix, types)


def validate_scoring(scoring: list | tuple | np.ndarray):
    """
    Validates the scoring values to ensure they are positive, non-zero numerical values.

    This function checks that:

    1. All elements in the `scoring` iterable are scalar values.
    2. Each scalar value is greater than zero.

    Parameters
    ----------
    scoring : iterable
        An iterable (e.g., list, numpy array) of scoring or ranking values. Each value should be a positive, 
        non-zero numerical value.

    Returns
    -------
    None
        This function does not return a value. It raises an error if validation fails.

    Raises
    ------
    ValueError
        If any value in `scoring` is not a scalar or if any value is zero or negative.

    Examples
    --------
    >>> import numpy as np
    >>> scoring = [1, 2, 3]
    >>> validate_scoring(scoring) # No output, as validation passes.

    >>> invalid_scoring = [1, -2, 3]
    >>> validate_scoring(invalid_scoring)
    Traceback (most recent call last):
        ...
    ValueError: Ranking and scoring should contain only positive non-zero numerical values!
    """
    if not all(np.isscalar(r) and r > 0 for r in scoring):
        raise ValueError('Ranking and scoring should contain only positive non-zero numerical values!')


def validate_pairwise_matrix(matrix, valid_values, answer_mapper):
    """
    Validates a pairwise comparison matrix.

    This function checks the following:

    1. All elements in the `matrix` belong to the specified set of valid values.
    2. The `matrix` is a square matrix, i.e., its shape is `(n, n)`.
    3. The pairwise relationships in the matrix are consistent, as defined by the `answer_mapper`.

    Parameters
    ----------
    matrix : numpy.ndarray
        A 2D square array representing the pairwise comparisons. Each element of the matrix
        must be one of the valid values.
    valid_values : iterable
        A collection of acceptable values that can appear in the `matrix`.
    answer_mapper : callable
        A function that defines the reciprocal relationship between matrix elements.
        For example, if `matrix[i, j]` is `x`, then `matrix[j, i]` should be `answer_mapper(x)`.

    Returns
    -------
    None
        This function does not return a value. It raises an error if any validation fails.

    Raises
    ------
    ValueError
        If any element in `matrix` is not in `valid_values`.
        If the `matrix` is not square.
        If the reciprocal relationship defined by `answer_mapper` is not satisfied.
    """
    valid_values = {round(v, 2) for v in valid_values}
    if not all(round(v, 2) in valid_values for v in np.unique(matrix)):
        raise ValueError(f'Valid values in the matrix are: {valid_values}')

    if len(matrix.shape) != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f'Matrix should be two-dimensional array with (n, n) shape.')

    for i, j in combinations(range(matrix.shape[0]), 2):
        if abs(matrix[j, i] - answer_mapper(matrix[i, j])) > 0.01:
            raise ValueError(f'matrix[{j}, {i}] should be {answer_mapper(matrix[i, j])}, because '
                             f'matrix[{i}, {j}] is {matrix[i, j]}.')
