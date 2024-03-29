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

            filename : str or None
                Path to the file in which identified save should be saved.
                If None, MEJ will be not saved. If file exists, MEJ will be
                loaded from this file. Default is 'mej.csv'.

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

    def __init__(self, criteria_names, show_MEJ=False,
                 tablefmt='simple_grid', filename='mej.csv',
                 force_file_use=False):
        self.criteria_names = criteria_names
        self.show_MEJ = show_MEJ
        self.tablefmt = tablefmt
        self.filename = filename
        self.co_names = None
        self.force_file_use = force_file_use

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
        if self.filename is None or not os.path.isfile(self.filename):
            return self._identify_manually(characteristic_objects)
        else:
            result = self._load_from_file(characteristic_objects)
            if result is None:
                return self._identify_manually(characteristic_objects)
            else:
                return result

    def _identify_manually(self, characteristic_objects):
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

        if self.filename is not None:
            np.savetxt(self.filename, mej,
                       fmt='%.1f', delimiter=',')
            print(f'Identified MEJ was written to "{self.filename}".')

        return mej.sum(axis=1), mej

    def _load_from_file(self, characteristic_objects):
        mej = np.loadtxt(self.filename, delimiter=',')
        n, m = mej.shape
        mej_uniq = np.unique(mej)
        if n != m:
            raise ValueError('MEJ loaded from file is not square matrix '
                             'and therefore is not valid MEJ!')
        elif np.any(mej[np.tril_indices(n, -1)] != 1 - mej.T[np.tril_indices(n, -1)]):
            raise ValueError('MEJ loaded from file is not valid! '
                             'Some values in upper and lower triangle sub-'
                             'matrices are wrong.')
        elif len(mej_uniq) != 3 or np.any(mej_uniq != np.array([0, 0.5, 1])):
            raise ValueError('MEJ loaded from file is not valid! '
                             'There are values other than [0, 0.5, 1].')
        elif len(np.unique(np.diag(mej))) != 1:
            raise ValueError('MEJ loaded from file is not valid! '
                             'There are different values on diagonal.')
        elif len(characteristic_objects) != n:
            raise ValueError('MEJ loaded from file is not valid! '
                             'Number of the characteristic objects in this'
                             'MEJ is different from the one provided in '
                             'arguments.')

        print(f'\nMEJ from the file ({self.filename}):')
        self.co_names = [self._co_name(i) for i in range(1, n + 1)]
        self._show_mej(mej)
        print('\n')

        if not self.force_file_use:
            print('Do you want to use this MEJ? [Y/n]')
            ans = input('>>> ').strip().lower()
            while ans not in ('', 'n', 'y'):
                ans = input('>>> ').strip().lower()
            print('\n')
        else:
            print('This MEJ will be used in the model.')
            ans = 'y'

        if ans == '' or ans == 'y':
            return mej.sum(axis=1), mej
        else:
            return None # Explicitely return None, matrix will be re-identified


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
