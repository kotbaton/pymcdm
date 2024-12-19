# Copyright (c) 2023 Andrii Shekhovtsov

class MethodExpert:
    """ Create an object which will rate characteristic objects with any MCDA method.

        Parameters
        ----------
            method : MCDA_Method
                Any object of the MCDA method inherited from MCDA_Method.

            weights : ndarray
                Criteria weights. Sum of the weights should be 1. (e.g. sum(weights) == 1)

            types : ndarray
                Array with definitions of criteria types:
                1 if criteria is profit and -1 if criteria is cost for each criteria in `matrix`.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import COMET, TOPSIS
        >>> from pymcdm.methods.comet_tools import MethodExpert
        >>> cvalues = [
        ...     [0, 500, 1000],
        ...     [1, 5]
        ...     ]
        >>> weights = np.array([0.5, 0.5])
        >>> types = np.array([-1, 1])
        >>> expert_function = MethodExpert(TOPSIS(), weights, types)
        >>> comet = COMET(cvalues, expert_function)
    """
    def __init__(self, method, weights, types):
        self.method = method
        self.weights = weights
        self.types = types

    def __call__(self, co):
        """ Evaluate characteristic objects using provided MCDA method.

            Parameters
            ----------
            co : np.array
                Characteristic objects which should be compared.

            Returns
            -------
                sj : np.array
                    SJ vector (see the COMET procedure for more info).

                mej : None
                    Because of how this method works MEJ matrix is not
                    generated.
        """
        p = self.method(co, self.weights, self.types, validation=False)
        r = self.method.rank(p)
        return r.shape[0] - r, None
