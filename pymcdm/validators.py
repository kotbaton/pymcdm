# Copyright (c) 2024 Andrii Shekhovtsov
# Copyright (c) 2024 Bartłomiej Kizielewicz

from typing import Iterable

import numpy as np


def param_validator(param, name):
    if 0 <= param <= 1:
        return True
    else:
        raise ValueError(f'{name} should be in range [0, 1], but it\'s value is {param}.')


def array_dimension_validator(array: np.ndarray, ndim: int, name: str) -> None:
    if len(array.shape) != ndim:
        raise ValueError(f'{name} should be {ndim}d array, but it has shape {array.shape}.')


def matrix_ref_point_validator(matrix: np.ndarray, ref_point: np.ndarray) -> None:
    array_dimension_validator(ref_point, 1, 'ref_point')

    if ref_point.shape[0] != matrix.shape[1]:
        raise ValueError(
            f'Len of the ref_point {ref_point.shape[0]} should be the same as number of the criteria {matrix.shape[1]}.')


def matrix_cvalues_validator(matrix, cvalues):
    if matrix.shape[1] != len(cvalues):
        ValueError(f'Number of criteria in matrix ({matrix.shape[1]}) is different from number of criteria in '
                   f'the characteristic values ({len(cvalues)}), but those values should be the same.')

    for i, alt in enumerate(matrix):
        if any(a < cv[0] or cv[-1] < a for a, cv in zip(alt, cvalues)):
            ValueError(f'Some criteria values in alternative with index {i} are not in problem\'s domain, '
                       'i.e. there are values that are bigger or smaller then bounds defined in cvalues.')


def ref_ideal_bounds_validator(ref_ideal, bounds):
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
    if not np.all(np.logical_and(min_ <= ref_min, ref_max <= max_)) or ref_min >= ref_max:
        raise ValueError('ref_ideal values should be in range of min and max values (bounds) for each criterion.'
                         'ref_ideal values should be ordered in [min, max] order.')


def matrix_bounds_validator(matrix, bounds):
    min_, max_ = bounds[:, 0], bounds[:, 1]

    for i, alt in enumerate(matrix):
        if not np.all(np.logical_and(min_ <= alt, alt <= max_)):
            raise ValueError('Every alternative values should be in range of min and max values (bounds) '
                             f'for each criterion. Some values of alternative with index {i} is out of range.')


def cvalues_validator(cvalues):
    for i, cv in enumerate(cvalues):
        if not isinstance(cv, Iterable):
            raise ValueError(
                'Characteristic values should be represented with nested lists or other iterables.'
                f'However "{cv}" is not iterable.'
            )

        if len(cv) < 2:
            raise ValueError(
                f'You should provide minimum 2 characteristic value for each criterion. Check criterion with index '
                f'{i}.'
            )

        if any(cv[i] >= cv[i + 1] for i in range(len(cv) - 1)):
            raise ValueError(
                f'Characteristic values must be sorted in ascending order and does not contain repeated elements. '
                f'Check criterion with index {i}. '
            )


def bounds_validator(bounds):
    array_dimension_validator(bounds, 2, 'bounds')

    min_, max_ = bounds[:, 0], bounds[:, 1]

    if np.any(min_ >= max_):
        raise ValueError('Bounds should contain min and max values for each criterion, '
                         'in order [min, max] in each row.')


def esp_bounds_validator(esp, bounds):
    array_dimension_validator(esp, 1, 'esp')

    min_, max_ = bounds[:, 0], bounds[:, 1]

    if not np.all(np.logical_and(min_ <= esp, esp <= max_)):
        raise ValueError('ESP values should be in range of min and max values (bounds) for each criterion.')


def matrix_validator(matrix, types):
    array_dimension_validator(matrix, 2, 'Matrix')

    max_alt = np.max(matrix, axis=0)
    min_alt = np.min(matrix, axis=0)

    dominant = [max_alt[i] if types[i] == 1 else min_alt[i]
                for i in range(matrix.shape[1])]
    dominated = [max_alt[i] if types[i] == -1 else min_alt[i]
                 for i in range(matrix.shape[1])]

    dominant_alts, = np.where([np.all(dominant == alt) for alt in matrix])
    if dominant_alts:
        raise ValueError(f'Alternatives with indices {list(dominant_alts)} are dominant. Consider removing them,'
                         'as such alternatives can cause numerical errors in some methods.')

    dominated_alts, = np.where([np.all(dominated == alt) for alt in matrix])
    if dominated_alts:
        raise ValueError(f'Alternatives with indices {list(dominated_alts)} are dominated. Consider removing them,'
                         'as such alternatives can cause numerical errors in some methods.')


def weights_validator(matrix, weights):
    array_dimension_validator(weights, 1, 'Weights')

    if matrix.shape[1] != weights.shape[0]:
        raise ValueError('Number of criteria should be same as number of weights.')

    if abs(weights.sum() - 1) >= 0.01 or np.any(weights <= 0):
        raise ValueError('Weights should be positive and its sum should be equal one. Now, sum of the weights is '
                         f'{weights.sum()}.')


def types_validator(matrix, types):
    array_dimension_validator(types, 1, 'Types')

    if matrix.shape[1] != types.shape[0]:
        raise ValueError('Number of criteria should be same as number of criteria types.')

    if np.sum(np.abs(types)) != types.shape[0]:
        raise ValueError('Types array should only contains values -1 '
                         'or 1.')


def validate_decision_problem(matrix, weights, types):
    matrix_validator(matrix, types)
    weights_validator(matrix, weights)
    types_validator(matrix, types)
