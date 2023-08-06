# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from pymcdm.methods import COMET, TOPSIS
from pymcdm.methods.comet_tools import CompromiseExpert

cvalues = [
        [0, 500, 1000],
        [1, 5],
        [1, 3, 10],
        ]

types = np.ones(3)

topsis = TOPSIS()

evaluation_function = [
        lambda co: topsis(co, np.array([0.2, 0.3, 0.5]), types),
        lambda co: topsis(co, np.array([0.3, 0.4, 0.3]), types),
        lambda co: topsis(co, np.array([0.1, 0.5, 0.4]), types),
        ]

expert_function = CompromiseExpert(evaluation_function)

comet = COMET(cvalues, expert_function)

print(comet.p)
