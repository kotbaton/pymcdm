# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np

from .mcda_method import MCDA_method
from ..io import TableDesc
from ..validators import array_dimension_validator, matrix_validator, weights_validator, types_validator


class LoPM(MCDA_method):
    """ Limits on Property Method

        Limits on Property Method is a method primarily proposed for dealing with material selection problems.
        It operates on three types of criteria (in method's convention): lower-limit, upper-limit
        and target properties [#lopm]_.

        Read more in the User Guide.

        Parameters
        ----------
            property_limits : np.ndarray or None
                Vector of lower-limit, upper-limit and target value properties. If None, then limits will be derived
                from matrix based on types on each call. Default is None.

            property_types : np.ndarray or None
                Vector of property types: should be iterable with int values that define types of properties
                provided in `property_limits` argument. Possible values:
                -  1 for lower-limit, treated as "no lower than", equivalent to profit criteria.
                - -1 for upper-limit, treated as "no bigger than", equivalent to cost criteria.
                -  0 for target properties, equivalent of Expected Solution Point.
                If None, then `types` argument will be used to determine limits' types.
                Note, that if the
                Default is None.

        References
        ----------
        .. [#lopm] Farag, M. M. (2020). Materials and process selection for engineering design. CRC press.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import LoPM
        >>> matrix = np.array([
        ...     [14_820, 18, 0.0002, 2.1,  9.5, 4.5],
        ...     [21_450, 18, 0.0012, 2.7, 14.4, 9.0],
        ...     [78_000, 16, 0.0006, 2.6,  9.0, 8.5],
        ...     [20_475, 17, 0.0006, 2.6,  6.5, 2.6],
        ...     [16_575, 14, 0.0010, 3.1,  5.6, 3.5],
        ...     [21_450, 16, 0.0005, 2.2,  8.6, 1.0]
        ... ])
        >>> weights = np.array([0.20, 0.33, 0.13, 0.07, 0.07, 0.20])
        >>> lopm = LoPM([10_000, 14, 0.0015, 3.5, 2.3, 9.0], [1, 1, -1, -1, 0, -1])
        >>> print(lopm(matrix, weights, None).round(2))
        [0.77 1.08 0.81 0.66 0.78 0.68]
    """
    reverse_ranking = False
    _tables = [
        TableDesc(caption='Lower property score',
                  label='lower_profit', symbol='', rows='A', cols=None),
        TableDesc(caption='Upper property score',
                  label='upper_cost', symbol='', rows='A', cols=None),
        TableDesc(caption='Target property score',
                  label='target', symbol='', rows='A', cols=None),
        TableDesc(caption='Merit/Preference value',
                  label='pref', symbol='$P_i$', rows='A', cols=None),
    ]

    def __init__(self,
                 property_limits: np.ndarray or None = None,
                 property_types: np.ndarray or None = None):
        if (property_limits is None and property_types is not None) \
                or (property_limits is not None and property_types is None):
            raise ValueError('Both property_limits and property_types should be provided and have same length.'
                             'Alternatively, none of the arguments should be provided.')

        if property_limits is not None and property_types is not None:
            self.property_limits = np.asarray(property_limits)
            self.property_types = np.asarray(property_types)
            array_dimension_validator(self.property_limits, 1, 'property_limits')
            array_dimension_validator(self.property_types, 1, 'property_types')

            valid_property_types = (-1, 0, 1)
            if not all(v in valid_property_types for v in self.property_types):
                raise ValueError('Valid property_types are: {-1, 0 1}, but different value was provided.')

            if len(self.property_limits) != len(self.property_types):
                raise ValueError('property_limits and property_types should have same length.')
        else:
            self.property_limits = None
            self.property_types = None


    def __call__(self,
                 matrix: np.ndarray | list | tuple,
                 weights: np.ndarray | list | tuple,
                 types: np.ndarray | list | tuple = None,
                 validation: bool = True,
                 verbose: bool = False):
        """ Rank alternatives from decision matrix `matrix`, with criteria
            weights `weights` and criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : ndarray
                    Criteria weights. Sum of the weights should be 1. (e.g.
                    sum(weights) == 1)

                types : ndarray or None
                    Array with definitions of criteria types:
                    1 if criteria is profit and -1 if criteria is cost for
                    each criteria in `matrix`. Can be omitted if property_limits
                    and property_types were provided in the constructor.
                    Note, that if both types and property_types are provided,
                    property_types are preferred and will be used.

                validation : bool
                    Enable or disable validation of the all input data. True - validation is enabled,
                    False - validation is disabled. Default is True.

                verbose : bool
                    Explain the MCDA, i.e. provide matrices and vectors from
                    all the steps of the method, instead of return just the
                    preference vector. Default is False.
        """
        matrix = np.asarray(matrix, dtype='float')
        weights = np.asarray(weights, dtype='float')

        if validation:
            if types is not None:
                types = np.asarray(types)
                matrix_validator(matrix, types)
                types_validator(matrix, types)
            elif self.property_types is None:
                raise ValueError('Either types (in call) or property_types (in init) should be provided.')
            weights_validator(matrix, weights)
            self._additional_validation(matrix, weights, types)

        if verbose:
            return self._method_explained(matrix, weights, types)
        else:
            return self._method(matrix, weights, types)[-1]

    def _method(self, matrix, weights, types):
        if self.property_limits is not None:
            limits = self.property_limits
            types = self.property_types
        else:
            limits = np.array([np.min(matrix[:, i]) if types[i] == -1 else np.max(matrix[:, i])
                               for i in range(matrix.shape[1])])

        upper_mask = (types == -1)
        lower_mask = (types == 1)
        target_mask = (types == 0)

        lower = np.sum(weights[lower_mask] * (limits[lower_mask] / matrix[:, lower_mask]), axis=1)
        upper = np.sum(weights[upper_mask] * (matrix[:, upper_mask] / limits[upper_mask]), axis=1)
        target = np.sum(weights[target_mask] * np.abs((matrix[:, target_mask] / limits[target_mask]) - 1), axis=1)

        # TODO make proper test for the method
        # TODO user guide description
        m = lower + upper + target
        return lower, upper, target, m

    def _additional_validation(self, matrix, weights, types):
        if self.property_limits is not None and self.property_limits.shape[0] != matrix.shape[1]:
            raise ValueError(f'Property limits are provided for {self.property_limits.shape[0]} criteria, but '
                             f'matrix has {matrix.shape[1]} criteria.')
