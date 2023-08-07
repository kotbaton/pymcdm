# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

class FunctionExpert:
    """ Create an object which will rate characteristic objects using expert function.

        Parameters
        ----------
            expert_function : Callable
                Function with a signature (co_i, co_j) -> float.
                If co_i < co_j this function should return 0.0.
                If co_i == co_j this function should return 0.5.
                If co_i > co_j this function should return 1.0.
    """
    def __init__(self, expert_function):
        self.expert_function = expert_function

    def __call__(self, co):
        """ Evaluate characteristic objects using provided expert function.

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
        expert_function = self.expert_function
        mej = np.diag(np.ones(co.shape[0]) * 0.5)
        for i in range(mej.shape[0]):
            for j in range(i + 1, mej.shape[0]):
                v = expert_function(co[i], co[j])
                mej[i, j] = v
                mej[j, i] = 1 - v

        return mej.sum(axis=1), mej
