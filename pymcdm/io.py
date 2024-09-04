# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List

import numpy as np
from numpy.typing import ArrayLike
import pandas as pd


class MCDA_method:
    pass

def latex_problem_definition(weights,
                             types=None,
                             criteria_names=None,
                             criteria_units=None,
                             cvalues=None,
                             bounds=None,
                             esp=None,
                             ref_ideal=None,
                             float_fmt=None,
                             caption='Criteria description',
                             label='crit_desc'):
    data = {
            'Weight': weights,
            '$C_i$': [f'$C_{{{i}}}$' for i in range(1, weights.shape[0] + 1)]
            }

    if types is not None:
        data['Type'] = ['Max' if t == 1 else 'Min'
                        for t in types]

    if criteria_names is not None:
        data['Criterion Name'] = criteria_names

    if criteria_units is not None:
        data['Unit'] = criteria_units

    if cvalues is not None:
        if cvalues.shape[1] == 3:
            data['Min'] = cvalues[:, 0]
            data['Max'] = cvalues[:, -1]
            data['Mean'] = cvalues[:, 1]
        else:
            print('Other then 3 cvalues is not supported.')

    if bounds is not None:
        data['Min'] = bounds[:, 0]
        data['Max'] = bounds[:, 1]

    if esp is not None:
        data['Expected value'] = esp

    if ref_ideal is not None:
        data['Ref. ideal Min'] = ref_ideal[:, 0]
        data['Ref. ideal Max'] = ref_ideal[:, 1]

    df = pd.DataFrame(data)

    columns_order = ['$C_i$', 'Criterion Name', 'Unit', 'Weight',
                     'Type', 'Min', 'Mean', 'Max', 'Expected value',
                     'Ref. ideal Min', 'Ref. ideal Max']
    used_columns = [c for c in columns_order if c in data]
    s = df[used_columns].to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label=label,
            caption=caption,
            )

    print('\n', s, sep='')

# def latex_ndarray(array,
#                   row_labels=None,
#                   rows_name='',
#                   column_labels=None,
#                   float_fmt=None,
#                   caption='',
#                   label=''):
#
#     n, m = array.shape
#     if row_labels is None or row_labels == 'alts':
#         row_labels = [f'$A_{{{i}}}$' for i in range(1, n + 1)]
#         rows_name = '$A_i$'
#     elif row_labels == 'crit':
#         row_labels = [f'$C_{{{i}}}$' for i in range(1, n + 1)]
#
#     if column_labels is None or column_labels == 'crit':
#         column_labels = [f'$C_{{{i}}}$' for i in range(1, m + 1)]
#     elif column_labels == 'alts':
#         column_labels = [f'$A_{{{i}}}$' for i in range(1, m + 1)]
#
#     df = pd.DataFrame([[n, *row] for n, row in zip(row_labels, array)],
#                       columns=[rows_name, *column_labels])
#
#     s = df.to_latex(
#             index=False,
#             float_format=float_fmt,
#             position='h',
#             label=label,
#             caption=caption,
#             )
#
#     print('\n', s, sep='')


class TableDesc:
    def __init__(self, caption: str, label: str, symbol: str or None=None):
        self.caption = caption
        self.label = label
        self.symbol = symbol

    def create_table(self, data: ArrayLike):
        return Table(data, self)


class Table:
    def __init__(self,
                 data: ArrayLike,
                 desc: TableDesc,
                 row_labels: List[str] or None=None,
                 col_labels: List[str] or None=None,
                 row_labels_name: str or None=None):
        self.data = data
        self.desc = desc

        if len(data.shape) == 2:
            if row_labels is None:
                self.row_labels = [f'$A_{{{i}}}$'
                                   for i in range(1, data.shape[0] + 1)]
            else:
                self.row_labels = row_labels

            if col_labels is None:
                self.col_labels = [f'$C_{{{i}}}$'
                                   for i in range(1, data.shape[1] + 1)]
            else:
                self.col_labels = col_labels

            if row_labels_name is None:
                self.row_labels_name = '$A_{i}$'
            else:
                self.row_labels_name = row_labels_name

            self.df = pd.DataFrame(data=self.data, columns=self.col_labels)
            self.df.insert(0, self.row_labels_name, self.row_labels)

        elif len(data.shape) == 1:
            if row_labels is None:
                self.row_labels = [desc.symbol]
            else:
                self.row_labels = row_labels

            if col_labels is None:
                self.col_labels = [f'$A_{{{i}}}$'
                                   for i in range(1, data.shape[0] + 1)]
            else:
                self.col_labels = col_labels

            if row_labels_name is None:
                self.row_labels_name = ''
            else:
                self.row_labels_name = row_labels_name

            self.df = pd.DataFrame(data=[self.data], columns=self.col_labels)
            self.df.insert(0, self.row_labels_name, self.row_labels)

        else:
            raise ValueError(f'Data shape {data.shape} is not supported.')

    def to_latex(self, float_fmt=None):
        return self.df.to_latex(
                index=False,
                float_format=float_fmt,
                position='h',
                label=f'tab:{self.desc.label}',
                caption=self.desc.caption,
                )


# TODO We supposely don't need it
# class GroupedTableDesc(TableDesc):
#     def __init__(self,
#                  table_slice: str,
#                  caption: str,
#                  label: str,
#                  symbol: str or None=None):
#         self.table_slice = table_slice # TODO check tables are only vectors, not matrices
#         super().__init__(caption, label, symbol)
#
#     def create_table(self, data: ArrayLike):
#         return


class MCDA_results: # TODO it should work as a list
    def __init__(self,
                 method: MCDA_method,
                 matrix: ArrayLike,
                 results: List[Table]):
        self.method = method
        self.method_name = method.__class__.__name__
        self.matrix = matrix
        self.results = results

    def to_latex(self,
                 group_tables: bool=True,
                 ranking: bool=True,
                 matrix: bool=True,
                 label_prefix: bool=True,
                 float_fmt: str or List[str] or None='%0.4f',
                 **kwargs): # TODO there will be many different parameters
        output_strs = [f'Results of the {self.method_name}.']
        if matrix:
            t = Table(data=self.matrix,
                      desc=TableDesc(caption='Decision matrix', label='matrix'))
            output_strs.append(t.to_latex(float_fmt))

        grouped_tables = []
        for t in self.results:
            if len(t.data.shape) == 2:
                output_strs.append(t.to_latex(float_fmt))
            elif group_tables:
                grouped_tables.append(t)
            else:
                output_strs.append(t.to_latex(float_fmt))

        if ranking:
            ranking_table = Table(data=self.method.rank(self.results[-1].data),
                                  desc=TableDesc(caption='Ranking',
                                                 label='ranking',
                                                 symbol='$R_{i}$'))
            if group_tables:
                grouped_tables.append(ranking_table)
            else:
                output_strs.append(ranking_table.to_latex(float_fmt))

        if group_tables:
            data = [t.data for t in grouped_tables]
            desc = TableDesc(
                    caption=f'Results of the {self.method_name} calculations.',
                    label='results'
                    )
            col_labels = [t.data for t in grouped_tables]
            t = Table(data=data, desc=desc, col_labels=col_labels)
            output_strs.append(t.to_latex(float_fmt))

        output_strs.append(f'Total {len(output_strs) - 1} tables.')

        return '\n\n'.join(output_strs)


    def __str__(self):
        return 'Not implemented yet'

    def __dict__(self):
        pass


