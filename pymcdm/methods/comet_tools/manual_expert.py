# Copyright (c) 2023 Andrii Shekhovtsov

import os
import numpy as np
from tabulate import tabulate

class ManualExpert:
    """ Create object of the ManualExpert expert function which allows to 
        manually identify Matrix of Expert Judgements (MEJ).

        Parameters
        ----------
            criteria_names : list[str]
                Criteria names which would be used during the procedure of the
                MEJ identification.

            show_MEJ : bool
                If MEJ should be shown after each question answered.
                Default is False.

            tablefmt : str
                tablefmt argument for the tablulate function. See tabulate
                documentation for more info.
                Default is 'simple_grid'.

        Examples
        --------
        >>> import numpy as np
        >>> from pymcdm.methods import COMET
        >>> from pymcdm.methods.comet_tools import ManualExpert
        >>> cvalues = [
        ...     [0, 500, 1000],
        ...     [1, 5]
        ...     ]
        >>> expert_function = ManualExpert(
        ...     criteria_names=['Price [$]', 'Profit [grade]'],
        ...     show_MEJ=True
        ...     )
        >>> # You will prompted to evaluate all CO
        >>> comet = COMET(cvalues, expert_function)
    """

    def __init__(self, criteria_names, show_MEJ=False, tablefmt='simple_grid'):
        self.criteria_names = criteria_names
        self.show_MEJ = show_MEJ
        self.tablefmt = tablefmt
        self.co_names = None

        self.q = None
        self.max_q = None
        self.characteristic_objects = None

    def __call__(self, characteristic_objects):
        """ Evaluate characteristic objects by asking pairwise comparison
            questions.

            Parameters
            ----------
            characteristic_objects : np.array
                Characteristic objects which should be compared.

            Returns
            -------
                sj : np.array
                    SJ vector (see the COMET procedure for more info).

                mej : np.array
                    MEJ matrix created by comparisons
                    (see the COMET procedure for more info).
        """
        n = len(characteristic_objects)
        mej = -np.ones((n, n)) + 1.5 * np.eye(n)

        self.q = 0
        self.max_q = (n * (n - 1)) // 2

        self.characteristic_objects = characteristic_objects
        self.co_names = [self._co_name(i) for i in range(1, n + 1)]
        print(f'You need to evaluate {n} characteristic objects.')
        print(f'It will require {self.max_q} pairwise comparisons.\n')

        print('Characteristic Objects to be evaluated:')
        self._show_co(characteristic_objects, self.co_names)

        for diag in range(0, n - 1):
            for i in range(0, n - diag - 1):
                j = i + diag + 1

                mej[i, j] = self._query_helper(i, j)
                if self.show_MEJ:
                    self._show_mej(mej)

        mej[np.tril_indices(n, -1)] = 1 - mej.T[np.tril_indices(n, -1)]

        print('\nResulted MEJ:')
        self._show_mej(mej)
        print('\n')

        return mej.sum(axis=1), mej

    def _query_helper(self, i, j):
        self.q += 1
        self._show_separator()
        print('\nEvaluate following characteristic objects:')
        self._show_co(self.characteristic_objects[[i, j]],
                      [self.co_names[i], self.co_names[j]])
        return self._query_user(self.co_names[i], self.co_names[j])

    def _query_user(self, coi, coj):
        print(f'\nInput "{coi}" if {coi} is better.',
              f'Input "{coj}" if {coj} is better',
              f'Leave empty for the tie.', sep='\n')
        ans = None
        options = {coi: 1, coj: 0, '': 0.5}
        while ans not in options:
            ans = input('>>> ').strip()

        return options[ans]

    def _co_name(self, i):
        letters = []
        while i > 0:
            letters.append(chr(ord('A') - 1 + i % 26))
            i //= 26
        return ''.join(letters[::-1])

    def _show_mej(self, mej):
        mapper = {-1: '', 0.5: '1/2', 1.0: 1, 0.0: 0}
        table = [[self.co_names[i]] + [mapper[v] for v in mej[i]]
                  for i in range(mej.shape[0])]
        table = tabulate(table, headers=[' '] + self.co_names, tablefmt=self.tablefmt)
        print(table)

    def _show_co(self, characteristic_objects, co_names):
        table = tabulate(
                [
                    [n, *co]
                    for n, co in zip(co_names, characteristic_objects)
                    ],
                headers=[' '] + self.criteria_names,
                tablefmt=self.tablefmt,
                numalign='center',
                stralign='center'
                )
        print(table)

    def _show_separator(self):
        q_info = f' {self.q} / {self.max_q} '
        try:
            cols = os.get_terminal_size().columns
        except OSError:
            cols = 80
        first = (cols - len(q_info) - 2) // 2
        print(f'\n{"="*first}{q_info}{"="*(cols - first - len(q_info))}')
