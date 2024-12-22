from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike

from pymcdm.methods.mcda_method import MCDA_method


class LoPM(MCDA_method):
    """ Limits on Property Method

        Limits on Property Method is a method primarily proposed for dealing with material selection problems.
        It operates on three types of criteria (in method's convention): lower-limit, upper-limit
        and target properties [#lopm]_.

        Read more in the User Guide.

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

    def __init__(self,
                 property_limits: Iterable[float] or None = None,
                 property_types: Iterable[str] or None = None):
        """ Create Limits on Property Method object.

        Limits on Property Method is a method primarily proposed for dealing with material selection problems. It
        operates on three types of criteria (in method's convention): lower-limit, upper-limit and target properties.

        Parameters
        ----------
            property_limits : Iterable[float] or None
                Vector of lower-limit, upper-limit and target value properties. If None, then limits will be derived
                from matrix based on types on each call. Default is None.

            property_types : Iterable[str] or None
                Vector of property types: should be iterable with str values that define types of properties
                provided in `property_limits` argument. Letters can be either lowercase or upper case. Possible values:
                - 'l' or 'L' for lower-limit, treated as "no lower than", equivalent to profit criteria.
                - 'u' or 'U' for upper-limit, treated as "no bigger than", equivalent to cost criteria.
                - 't' or 'T' for target properties, equivalent of Expected Solution Point.
                If None, then `types` argument will be used to determine limits' types. Default is None.
        """
        self.property_limits = np.array(property_limits)
        self.property_types = np.array([c.lower() for c in property_types])

    def __call__(self, matrix, weights, types, *args, **kwargs):
        """Rank alternatives from decision matrix `matrix`, with criteria weights `weights` and criteria types `types`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : ndarray
                    Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

                types : ndarray
                    Array with definitions of criteria types:
                    1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

                *args: is necessary for methods which reqiure some additional data.

                **kwargs: is necessary for methods which reqiure some additional data.

            Returns
            -------
                ndarray
                    Preference values for alternatives. Better alternatives have smaller values.
        """
        LoPM._validate_input_data(matrix, weights, types)

        return self._method(matrix, weights)

    def _method(self, matrix: ArrayLike, weights: ArrayLike):
        limits = self.property_limits
        types = self.property_types

        upper_mask = (types == 'u')
        lower_mask = (types == 'l')
        target_mask = (types == 't')

        lower = np.sum(weights[lower_mask] * (limits[lower_mask] / matrix[:, lower_mask]), axis=1)
        upper = np.sum(weights[upper_mask] * (matrix[:, upper_mask] / limits[upper_mask]), axis=1)
        target = np.sum(weights[target_mask] * np.abs((matrix[:, target_mask] / limits[target_mask]) - 1), axis=1)

        return lower + upper + target
