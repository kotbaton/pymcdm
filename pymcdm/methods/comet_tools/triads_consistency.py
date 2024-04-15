# Copyright (c) 2023 Andrii Shekhovtsov

from itertools import combinations
from math import factorial

from ..comet import COMET

import numpy as np

T_con_rules = (
    (1.0, 1.0, 1.0),
    (1.0, 0.5, 1.0),
    (0.5, 1.0, 1.0),
    (0.5, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (0.0, 0.5, 0.0),
    (0.5, 0.5, 0.5)
)

T_unk_rules = (
    (1.0, 0.0, 0.0),
    (1.0, 0.0, 0.5),
    (1.0, 0.0, 1.0),
    (0.0, 1.0, 0.0),
    (0.0, 1.0, 0.5),
    (0.0, 1.0, 1.0)
)

T_weak_inc_rules = (
    (1.0, 1.0, 0.5),
    (1.0, 0.5, 0.5),
    (0.5, 1.0, 0.5),
    (0.5, 0.5, 1.0),
    (0.5, 0.5, 0.0),
    (0.5, 0.0, 0.5),
    (0.0, 0.5, 0.5),
    (0.0, 0.0, 0.5)
    )

T_strong_inc_rules = (
    (1.0, 1.0, 0.0),
    (1.0, 0.5, 0.0),
    (0.5, 1.0, 0.0),
    (0.5, 0.0, 1.0),
    (0.0, 0.5, 1.0),
    (0.0, 0.0, 1.0),
    )

def triads_consistency(comet_or_mej):
    """ MEJ consistency coefficient based on inconsistence triads [#triads1]_.

        Parameters
        ----------
            comet_or_mej : COMET or np.array
                Either identified COMET method object or MEJ matrix from it.

        Returns
        -------
            Consistency coefficient value. See reference for details.

        References
        ----------
        .. [#triads1] Sałabun, W., Shekhovtsov, A., & Kizielewicz, B. (2021, June). A new consistency coefficient in the multi-criteria decision analysis domain. In Computational Science–ICCS 2021: 21st International Conference, Krakow, Poland, June 16–18, 2021, Proceedings, Part I (pp. 715-727). Cham: Springer International Publishing.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods.comet_tools import triads_consistency
        >>> mej = np.array([
        ...     [0.5, 0.0, 0.0, 1.0, 0.0, 1.0],
        ...     [1.0, 0.5, 0.0, 0.0, 0.0, 0.0],
        ...     [1.0, 1.0, 0.5, 0.0, 0.0, 0.0],
        ...     [0.0, 1.0, 1.0, 0.5, 0.0, 0.0],
        ...     [1.0, 1.0, 1.0, 1.0, 0.5, 0.0],
        ...     [0.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        ... ])
        >>> triads_consistency(mej)
        0.75
    """
    if isinstance(comet_or_mej, COMET):
        mej = comet_or_mej.get_MEJ()
    else:
        mej = comet_or_mej

    n = mej.shape[0]
    if n < 3:
        return 1

    T = factorial(n) / (factorial(n - 3) * factorial(3))
    T_inc = 0
    for i, j, k in combinations(range(n), 3):
        for cond1, cond2, concl in T_weak_inc_rules + T_strong_inc_rules:
            if mej[i, j] == cond1 and mej[j, k] == cond2 and mej[i, k] == concl:
                T_inc += 1

    return 1 - (T_inc / T)
