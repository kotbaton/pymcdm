# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from pymcdm.methods import COMET
from pymcdm.comet_tools import ManualExpert

cvalues = [
        [0, 500, 1000],
        [1, 5]
        ]

expert_function = ManualExpert(
        criteria_names=['Price [$]', 'Profit [grade]'],
        show_MEJ=True
        )

comet = COMET(cvalues, expert_function)
