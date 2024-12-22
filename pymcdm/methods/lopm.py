# Copyright (c) 2024 Andrii Shekhovtsov
from typing import Sequence

import numpy as np

from .mcda_method import MCDA_method
from ..io import TableDesc


class LoPM(MCDA_method):
    """ Limits on Property Method

        Limits on Property Method is a method primarily proposed for dealing with material selection problems.
        It operates on three types of criteria (in method's convention): lower-limit, upper-limit
        and target properties [#lopm]_.

        Read more in the User Guide.

        Parameters
        ----------
            property_limits : Sequence[float] or None
                Vector of lower-limit, upper-limit and target value properties. If None, then limits will be derived
                from matrix based on types on each call. Default is None.

            property_types : Sequence[str] or None
                Vector of property types: should be iterable with str values that define types of properties
                provided in `property_limits` argument. Letters can be either lowercase or upper case. Possible values:
                - 'l' or 'L' for lower-limit, treated as "no lower than", equivalent to profit criteria.
                - 'u' or 'U' for upper-limit, treated as "no bigger than", equivalent to cost criteria.
                - 't' or 'T' for target properties, equivalent of Expected Solution Point.
                If None, then `types` argument will be used to determine limits' types. Default is None.

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
        >>> lopm = LoPM([10_000, 14, 0.0015, 3.5, 2.3, 9.0], 'LLUUTU')
        >>> print(lopm(matrix, weights, None).round(2))
        [0.77 1.08 0.81 0.66 0.78 0.68]
    """
    reverse_ranking = False
    _tables = [
        # TODO add table desc
    ]

    def __init__(self,
                 property_limits: Sequence[float] or None = None,
                 property_types: Sequence[str] or None = None):
        # TODO add validation pl and pt should be same length
        # TODO Can be not provided, then will be derived from data in _method
        self.property_limits = np.array(property_limits)
        self.property_types = np.array([c.lower() for c in property_types])

    def _method(self, matrix, weights, types):
        limits = self.property_limits
        types = self.property_types

        upper_mask = (types == 'u')
        lower_mask = (types == 'l')
        target_mask = (types == 't')

        lower = np.sum(weights[lower_mask] * (limits[lower_mask] / matrix[:, lower_mask]), axis=1)
        upper = np.sum(weights[upper_mask] * (matrix[:, upper_mask] / limits[upper_mask]), axis=1)
        target = np.sum(weights[target_mask] * np.abs((matrix[:, target_mask] / limits[target_mask]) - 1), axis=1)

        # TODO return all according to _tables
        # TODO make proper test for the method
        # TODO user guide description
        return lower + upper + target

    def _additional_validation(self, matrix, weights, types):
        # TODO validate if matrix has good number of criteria as in property_limits and property_types
        pass
