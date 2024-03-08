# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from .triads_consistency import T_con_rules
from .manual_expert import ManualExpert

def _find_triad(a, b):
    for cond1, cond2, concl in T_con_rules:
        if a == cond1 and b == cond2:
            return concl
    return None

class TriadSupportExpert(ManualExpert):
    """ Create object of the TriadSupportExpert expert function which allows
        to manually identify Matrix of Expert Judgements (MEJ), but with the
        support of the consistent triads.

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
        >>> from pymcdm.methods.comet_tools import TriadSupportExpert
        >>> cvalues = [
        ...     [0, 500, 1000],
        ...     [1, 5]
        ...     ]
        >>> expert_function = TriadSupportExpert(
        ...     criteria_names=['Price [$]', 'Profit [grade]'],
        ...     show_MEJ=True
        ...     )
        >>> # You will prompted to evaluate some of the CO and
        >>> # other CO will be completed using consistent triads.
        >>> comet = COMET(cvalues, expert_function)
    """
    def _identify_manually(self, characteristic_objects):
        n = len(characteristic_objects)
        mej = - np.ones((n, n)) + 1.5 * np.eye(n)

        self.q = 0
        self.max_q = (n * (n - 1)) // 2

        user_q = 0
        triads_q = 0

        self.characteristic_objects = characteristic_objects
        self.co_names = [self._co_name(i) for i in range(1, n + 1)]

        print(f'You need to evaluate {n} characteristic objects.')
        print(f'It will require {self.max_q} pairwise comparisons.\n')

        print('Characteristic Objects to be evaluated:')
        self._show_co(characteristic_objects, self.co_names)

        print('\nATTENTION: This expert function use full triad support',
              'to speed up identification of the MEJ matrix by expert.',
              'Please, be aware that full triad support assumes that',
              'answers of the expert are always is consistent and in',
              'transition relation. Please review resulted MEJ in the end',
              'and correct it if needed.')

        mej[0, 1] = self._query_helper(0, 1)
        user_q += 1
        if self.show_MEJ:
            self._show_mej(mej)

        for diag in range(1, n - 1):
            for i in range(0, n - diag - 1):
                k = i + diag + 1
                for j in range(i + 1, k):
                    if mej[j, k] == -1:
                        mej[j, k] = self._query_helper(j, k)
                        user_q += 1
                        if self.show_MEJ:
                            self._show_mej(mej)

                    if mej[i, k] == -1:
                        concl = _find_triad(mej[i, j], mej[j, k])
                        if concl is not None:
                            mej[i, k] = concl
                            self._show_separator()
                            self._triad_support_message(mej, i, j, k)
                            self.q += 1
                            triads_q += 1
                            break
                else:
                    self._show_separator()
                    mej[i, k] = self._query_helper(i, k)
                    user_q += 1
                    if self.show_MEJ:
                        self._show_mej(mej)

        mej[np.tril_indices(n, -1)] = 1 - mej.T[np.tril_indices(n, -1)]

        print('\nResulted MEJ:')
        self._show_mej(mej)
        print('\n')

        print(f'Answered by the expert: {user_q}')
        print(f'Completed by the triads: {triads_q}')

        if self.filename is not None:
            np.savetxt(self.filename, mej,
                       fmt='%.1f', delimiter=',')
            print(f'Identified MEJ was written to "{self.filename}".')

        return mej.sum(axis=1), mej

    def _triad_support_message(self, mej, i, j, k):
        sign = {0.0: '<', 1.0: '>', 0.5: '='}
        print('\nTriad support:')
        print(f'{self.co_names[i]} {sign[mej[i, j]]} {self.co_names[j]} and ',
              f'{self.co_names[j]} {sign[mej[j, k]]} {self.co_names[k]}')
        print('Therefore:')
        print(f'{self.co_names[i]} {sign[mej[i, k]]} {self.co_names[k]}',
              f'i.e. mej[{self.co_names[i]}][{self.co_names[k]}]',
              f'= {mej[i, k]}')
