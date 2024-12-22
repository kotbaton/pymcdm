# Copyright (c) 2024 Andrii Shekhovtsov
from typing import Sequence

import numpy as np
import pandas as pd

from ..validators import (validate_decision_problem,
                          esp_bounds_validator,
                          bounds_validator,
                          matrix_bounds_validator,
                          cvalues_validator,
                          matrix_cvalues_validator,
                          ref_ideal_bounds_validator,
                          matrix_ref_point_validator)


class MCDA_problem:
    """
    Represents a Multi-Criteria Decision Analysis (MCDA) problem by aggregating elements
    of the decision problem and presenting them in a tabular format as text or LaTeX code.
    The `matrix` argument is used solely for validating the consistency of other parameters.

    Parameters
    ----------
        matrix : np.ndarray | list | tuple
            Decision matrix for validating dimensions and consistency of the problem.
            It will not be stored or outputted by to_latex() and to_string() methods.
        weights : np.ndarray | list | tuple
            Array of weights assigned to each criterion.
        types : Sequence[{1, -1}]
            Sequence indicating the optimization direction for each criterion
            (1 for maximization/profit, -1 for minimization/cost).
        criteria_names : Sequence[str], optional
            List of names for each criterion, by default None.
        criteria_units : Sequence[str], optional
            List of units for each criterion, by default None.
        cvalues : np.ndarray | list | tuple, optional
            Array of characteristic values associated with each criterion, by default None.
            Normally used in the COMET method.
        bounds : np.ndarray | list | tuple, optional
            Array of bounds for each criterion, by default None.
            Normally used in such methods as SPOTIS and RIM.
        esp : Sequence[float or int], optional
            Expected values for each criterion, by default None.
            Normally used in the ESPExpert class.
        ref_ideal : np.ndarray | list | tuple, optional
            Reference ideal values for each criterion, by default None.
            Normally used in the RIM method.

    Raises
    ------
    ValueError
        If `matrix` or `types` size does not match `weights`.
        If `criteria_names` or `criteria_units` length does not match `weights`.
        If `esp`, or `ref_ideal` are provided without `bounds` for validation.
        If the shape of `cvalues` is not supported.

    Attributes
    ----------
    df : pandas.DataFrame
        A DataFrame containing the criteria description, including weights, types, names, units,
        cvalues, bounds, expected values, and reference ideals.
    columns_order : list of str
        The default order of columns for display in the DataFrame.
    """
    def __init__(self,
                 matrix: np.ndarray | list | tuple,
                 weights: np.ndarray | list | tuple,
                 types: Sequence[{1, -1}],
                 criteria_names: Sequence[str] = None,
                 criteria_units: Sequence[str] = None,
                 cvalues: np.ndarray | list | tuple = None,
                 bounds: np.ndarray | list | tuple = None,
                 esp: Sequence[float or int] = None,
                 ref_ideal: np.ndarray | list | tuple = None):
        matrix = np.asarray(matrix)
        weights = np.asarray(weights)
        types = np.asarray(types)
        validate_decision_problem(matrix, weights, types)  # Validate dimensions of the basic parts of the problem
        data = {
            'Weight': weights,
            'Type': ['Max' if t == 1 else 'Min' for t in types],
            '$C_i$': [f'$C_{{{i}}}$' for i in range(1, len(weights) + 1)]
        }

        if criteria_names is not None:
            if len(criteria_names) != len(weights):
                raise ValueError('Criteria_names should have same length as weights.')
            data['Criterion Name'] = criteria_names

        if criteria_units is not None:
            if len(criteria_units) != len(weights):
                raise ValueError('Criteria_units should have same length as weights.')
            data['Unit'] = criteria_units

        if cvalues is not None:
            cvalues = np.asarray(cvalues)
            cvalues_validator(cvalues)
            matrix_cvalues_validator(matrix, cvalues)
            if cvalues.shape[1] == 3:
                data['$CV_1$'] = cvalues[:, 0]
                data['$CV_3$'] = cvalues[:, -1]
                data['$CV_2$'] = cvalues[:, 1]
            else:
                print('Other then 3 cvalues is not supported.')

        if bounds is not None:
            bounds = np.asarray(bounds)
            bounds_validator(bounds)
            matrix_bounds_validator(matrix, bounds)
            data['Min'] = bounds[:, 0]
            data['Max'] = bounds[:, 1]
        elif cvalues is not None:  # Derive bounds variable from cvalues if not provided
            bounds = cvalues[:, [0, -1]]
        elif esp is not None or ref_ideal is not None:
            raise ValueError('If you want to use esp or/and ref_ideal you need to provide bounds for validation.')

        if esp is not None:
            esp = np.asarray(esp)
            esp_bounds_validator(esp, bounds)
            data['Expected value'] = esp

        if ref_ideal is not None:
            ref_ideal = np.asarray(ref_ideal)
            ref_ideal_bounds_validator(ref_ideal, bounds)
            matrix_ref_point_validator(matrix, ref_ideal)
            data['Ref. ideal Min'] = ref_ideal[:, 0]
            data['Ref. ideal Max'] = ref_ideal[:, 1]

        self.df = pd.DataFrame(data)
        self.columns_order = ['$C_i$', 'Criterion Name', 'Unit', 'Weight',
                              'Type', 'Min', 'Max', '$CV_1$', '$CV_2$', '$CV_3$',
                              'Expected value', 'Ref. ideal Min', 'Ref. ideal Max']

    def to_latex(self, float_fmt: str or None = '%0.4f'):
        """
        Returns a LaTeX-formatted table of the criteria description.

        Parameters
        ----------
        float_fmt : str or None, optional
            Format for floating-point numbers, by default '%0.4f'.

        Returns
        -------
        str
            LaTeX-formatted string of the criteria description table.
        """
        used_columns = [c for c in self.columns_order if c in self.df.columns]
        s = self.df[used_columns].to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label='crit_desc',
            caption='Criteria description.',
        )
        return s

    def to_string(self, float_fmt: str or None = '%0.4f'):
        """
        Returns a plain text table of the criteria description.

        Parameters
        ----------
        float_fmt : str or None, optional
            Format for floating-point numbers, by default '%0.4f'.

        Returns
        -------
        str
            Plain text representation of the criteria description table.
        """
        used_columns = [c for c in self.columns_order if c in self.df.columns]
        s = self.df[used_columns].to_string(
            index=False,
            float_format=float_fmt,
        )
        return f'Criteria description.\n{s}'

    def __str__(self):
        """
        Returns a string representation of the criteria description, equivalent to `to_string()`.

        Returns
        -------
        str
            String representation of the criteria description.
        """
        return self.to_string()
