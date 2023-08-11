# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

class CompromiseExpert:
    """ Create an object which will rate characteristic objects (CO) using
        compromise of several preferences. If the CO is better in most of the
        preferences, than it is bigger in the final MEJ.

        Parameters
        ----------
            evaluation_functions : list[Callable]
                List of functions which will evaluate preferences of the
                characteristic objets. If you want to use MCDA methods, please
                use lambda or partial to provide weights and types to them.

            vote_limit : float
                Vote limit decides the limit for the voting. If number of votes
                CO_i > CO_j are bigger then vote_limit, then in the final MEJ
                matrix CO_i > CO_j, otherwise CO_i < CO_j.

        Examples
        --------
        >>> # Compromise solution for 3 different weights vectors
        >>> import numpy as np
        >>> from pymcdm.methods import COMET, TOPSIS
        >>> from pymcdm.methods.comet_tools import CompromiseExpert
        >>> cvalues = [
        ...         [0, 500, 1000],
        ...         [1, 5],
        ...         [1, 3, 10],
        ...         ]
        >>> types = np.ones(3)
        >>> topsis = TOPSIS()
        >>> evaluation_function = [
        ...         lambda co: topsis(co, np.array([0.2, 0.3, 0.5]), types),
        ...         lambda co: topsis(co, np.array([0.3, 0.4, 0.3]), types),
        ...         lambda co: topsis(co, np.array([0.1, 0.5, 0.4]), types),
        ...         ]
        >>> expert_function = CompromiseExpert(evaluation_function)
        >>> comet = COMET(cvalues, expert_function)
    """
    def __init__(self, evaluation_functions, vote_limit=None):
        self.evaluation_functions = evaluation_functions

        if vote_limit is None:
            vote_limit = len(evaluation_functions) / 2

        self.vote_limit = vote_limit


    def __call__(self, co):
        prefs = np.array([func(co)
                          for func in self.evaluation_functions]).T
        vote_limit = self.vote_limit

        n = len(co)

        mej = np.diag(np.ones(n))
        for i in range(n):
            for j in range(i + 1, n):
                votes = sum([iv > jv for iv, jv in zip(prefs[i], prefs[j])])

                if votes > vote_limit:
                    mej[i, j] = 1.0
                    mej[j, i] = 0.0
                elif votes == vote_limit:
                    mej[i, j] = 0.5
                    mej[j, i] = 0.5
                else:
                    mej[i, j] = 0.0
                    mej[j, i] = 1.0

        return mej.sum(axis=1), mej
