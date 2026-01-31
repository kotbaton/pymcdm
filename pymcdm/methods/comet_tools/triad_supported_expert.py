# Copyright (c) 2023-2026 Andrii Shekhovtsov

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
        support of the consistent triads and pre-defined criteria types.

        Parameters
        ----------
            criteria_names : list[str]
                Criteria names which would be used during the procedure of the
                MEJ identification.

            criteria_types : list[str]
                Criteria types which would be used during the procedure of the
                MEJ identification. Supported types are 1 (profit) and -1 (cost).
                More useful if COMET class created with 'gray_code' CO ordering.

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
    def __init__(self, criteria_names, criteria_types=None, show_MEJ=False,
                 tablefmt='simple_grid', filename='mej.csv',
                 force_file_use=False):
        super().__init__(criteria_names, show_MEJ, tablefmt, filename, force_file_use)
        self.criteria_types = criteria_types
        if self.criteria_types is not None:
            if len(self.criteria_types) != len(self.criteria_names):
                raise ValueError('Length of criteria_types must be equal to '
                                 'length of criteria_names.')
            for t in self.criteria_types:
                if t not in (1, -1):
                    raise ValueError('Supported criteria types are 1 (profit) '
                                     'and -1 (cost).')

        # Made some counters for statistics
        self.user_q = 0
        self.triads_q = 0
        self.rules_q = 0

    def _query_helper(self, i, j):
        """
        Query helper will solve pairwise comparison question with the provided types
        or fallback to manual/user questioning if types are not provided or CO differ
        with more than 1 criterion.

        Parameters
        ----------
        i : int
            Index of the first characteristic object.
        j : int
            Index of the second characteristic object.

        Returns
        -------
            float
            Result of the pairwise comparison: 1, 0.5 or 0.
        """
        self._show_separator()

        co_i_name = self.co_names[i]
        co_j_name = self.co_names[j]

        co_i = self.characteristic_objects[i]
        co_j = self.characteristic_objects[j]

        # Try to solve comparison if criteria types are provided
        # This work only if CO differ with only one criterion
        mask = (co_i != co_j)
        if self.criteria_types is not None and mask.sum() == 1:
            self.rules_q += 1
            idx = np.where(mask)[0][0]
            t = self.criteria_types[idx]
            v_co_i = co_i[idx]
            v_co_j = co_j[idx]
            result = None
            if (v_co_i - v_co_j) * t > 0:
                result = 1
            elif v_co_i == v_co_j:
                result = 0.5
            else:
                result =  0
            print(f'\nComparison {co_i_name} vs {co_j_name} was completed using criteria types:')
            print(f'Criterion: {self.criteria_names[idx]}'
                  f'({"Profit" if t == 1 else "Cost"})')
            print(f'Values: {v_co_i} vs {v_co_j}')
            sign = {1: 'better than', 0.5: 'equal to', 0: 'wotse than'}
            print(f'Result: {self.co_names[i]} is {sign[result]} {self.co_names[j]} '
                  f'(mej[{co_i_name}][{co_j_name}] = {result})')
            return result

        # Fallback to manual/user questioning
        print('\nEvaluate following characteristic objects:')
        self._show_co(self.characteristic_objects[[i, j]],
                      [self.co_names[i], self.co_names[j]])

        self.user_q += 1
        return self._query_user(self.co_names[i], self.co_names[j])

    def _identify_manually(self, characteristic_objects):
        n = len(characteristic_objects)
        mej = - np.ones((n, n)) + 1.5 * np.eye(n)

        self.q = 0
        self.max_q = (n * (n - 1)) // 2

        self.user_q = 0
        self.triads_q = 0
        self.rules_q = 0

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

        # Query helper will solve pairwise comparison question with the provided types
        # or fallback to manual/user questioning if types are not provided or CO differ
        # with more than 1 criterion.
        self.q += 1  # Top up the question counter
        mej[0, 1] = self._query_helper(0, 1)
        if self.show_MEJ:
            self._show_mej(mej)

        for diag in range(1, n - 1):
            # In this loop, we are trying to predict mej[i, k] values using triads,
            # by looking for such j that mej[i, j], mej[j, k] are known.
            for i in range(0, n - diag - 1):
                k = i + diag + 1
                for j in range(i + 1, k):
                    # If mej[j, k] is unknown, we need to ask the expert or use criteria types
                    if mej[j, k] == -1:
                        self.q += 1
                        mej[j, k] = self._query_helper(j, k)
                        if self.show_MEJ:
                            self._show_mej(mej)

                    # Now, if mej[i, k] is unknown, we can try to find it using the triad
                    if mej[i, k] == -1:
                        concl = _find_triad(mej[i, j], mej[j, k])
                        if concl is not None:
                            mej[i, k] = concl
                            self.q += 1
                            self._show_separator()
                            self._triad_support_message(mej, i, j, k)
                            self.triads_q += 1
                            break
                else:
                    # If we could not find any j to support mej[i, k], we need to ask the expert
                    # or use criteria types (if provided)
                    self._show_separator()
                    self.q += 1
                    mej[i, k] = self._query_helper(i, k)
                    if self.show_MEJ:
                        self._show_mej(mej)

        mej[np.tril_indices(n, -1)] = 1 - mej.T[np.tril_indices(n, -1)]

        print('\nResulted MEJ:')
        self._show_mej(mej)
        print('\n')

        print(f'Answered by the expert: {self.user_q}')
        print(f'Completed by the triads: {self.triads_q}')
        if self.criteria_types is not None:
            print(f'Completed by the rules: {self.rules_q}')

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
