# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List

import numpy as np
from numpy.typing import ArrayLike
import pandas as pd


class MCDA_method:
    pass


# TODO rewrite as a class, add more output options (at least latex and str)
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


class TableDesc:
    """
    Represents metadata for a table used in the decision process, describing various attributes of the table 
    including its caption, label, symbol, and orientation of rows and columns. Mostly for internal use.

    Parameters
    ----------
    caption : str
        A descriptive caption for the table, used as the main title or explanation in text or LaTeX representation.
    label : str
        A short reference label for the table, primarily used in LaTeX for referencing purposes.
    symbol : str or None, optional
        A mathematical symbol representing the data in the table as in the referenced paper. Defaults to None
        if no symbol is specified.
    rows : {'C', 'A'}, optional
        Defines the type of data stored in the rows of the table. Use 'C' to indicate criteria, or 'A' to 
        indicate alternatives. Defaults to None if unspecified.
    cols : {'C', 'A'}, optional
        Defines the type of data stored in the columns of the table. Use 'C' to indicate criteria, or 'A' 
        to indicate alternatives. Defaults to None if unspecified.

    Attributes
    ----------
    caption : str
        The description or caption of the table.
    label : str
        The short reference label for the table in LaTeX or other references.
    symbol : str or None
        Mathematical symbol associated with the table data.
    rows : str or None
        Specifies whether criteria ('C') or alternatives ('A') are represented in the rows, if applicable.
    cols : str or None
        Specifies whether criteria ('C') or alternatives ('A') are represented in the columns, if applicable.
    """

    def __init__(self,
                 caption: str,
                 label: str,
                 symbol: str or None = None,
                 rows: str or None = None,
                 cols: str or None = None):
        self.caption = caption
        self.label = label
        self.symbol = symbol
        self.rows = self.validate_option(rows)
        self.cols = self.validate_option(cols)

    def create_table(self, data: ArrayLike):
        return Table(data, self)

    @staticmethod
    def validate_option(opt):
        if opt not in ('C', 'A', None):
            raise ValueError('Valid option for rows and cols are {"C", "A"} or None.')
        return opt


class Table:
    """
    Represents a table containing data for Multi-Criteria Decision Analysis (MCDA) processes, supporting LaTeX
    export and formatted row and column labeling.

    Parameters
    ----------
    data : ArrayLike
        The data for the table, either a 1D or 2D array, representing different data.
        This data is automatically converted to a NumPy array.
    desc : TableDesc
        Metadata for the table, provided as a `TableDesc` instance, including caption, label, and symbol
        information used in LaTeX representations.
    row_labels : List[str] or None, optional
        Labels for each row in the table. If None, row labels will be generated based on TableDesc.
        If provided, then row labels info from TableDesc will be overridden.
    col_labels : List[str] or None, optional
        Labels for each column in the table. If None, columns labels will be generated based on TableDesc.
        If provided, then column labels info from TableDesc will be overridden.
    row_labels_name : str or None, optional
        Name to display for the row labels, useful for creating a title for the first column in the table.
        If None, a default based on the table type is used.

    Attributes
    ----------
    data : np.ndarray
        The primary data of the table, stored as a NumPy array.
    desc : TableDesc
        The metadata description of the table, including caption and label information.
    row_labels : List[str]
        List of labels for the table's rows.
    col_labels : List[str]
        List of labels for the table's columns.
    row_labels_name : str
        The name or title of the row labels column in the table.
    df : pd.DataFrame
        A pandas DataFrame representation of the table, including row and column labels as well as data.

    Raises
    ------
    ValueError
        If the shape of `data` is not supported (only 1D or 2D arrays are allowed).
    """

    def __init__(self,
                 data: ArrayLike,
                 desc: TableDesc,
                 row_labels: List[str] or None = None,
                 col_labels: List[str] or None = None,
                 row_labels_name: str or None = None):
        self.data = np.array(data)
        self.desc = desc

        if len(self.data.shape) > 2:
            raise ValueError(f'Data shape {self.data.shape} is not supported.')

        self.row_labels = self.generate_row_labels(row_labels)
        self.col_labels = self.generate_col_labels(col_labels)
        self.row_labels_name = self.generate_row_labels_name(row_labels_name)

        if len(self.data.shape) == 2:
            self.df = pd.DataFrame(data=self.data, columns=self.col_labels)
            self.df.insert(0, self.row_labels_name, self.row_labels)
        else:
            self.df = pd.DataFrame(data=[self.data], columns=self.row_labels)
            self.df.insert(0, '', [self.desc.symbol])

    def to_latex(self, float_fmt=None):
        return self.df.to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label=f'tab:{self.desc.label}',
            caption=self.desc.caption,
        )

    def to_string(self, float_fmt='0.4f'):
        s = self.df.to_string(
            index=False,
            float_format=float_fmt,
        )
        return f'{self.desc.caption}\n{s}'

    def __str__(self):
        return self.to_string()

    def generate_row_labels(self, row_labels):
        n = self.data.shape[0]
        if row_labels is not None:
            if len(row_labels) != n:
                raise ValueError('row_labels should have same number of elements as number'
                                 f' of rows in data ({n}).')
            return row_labels

        sym = self.desc.rows
        return [f'${sym}_{{{i}}}$' for i in range(1, n + 1)]

    def generate_col_labels(self, col_labels):
        if len(self.data.shape) == 1:
            return [self.desc.symbol]

        n = self.data.shape[1]
        if col_labels is not None:
            if len(col_labels) != n:
                raise ValueError('col_labels should have same number of elements as number'
                                 f' of columns in data ({n}).')
            return col_labels

        sym = self.desc.cols
        return [f'${sym}_{{{i}}}$' for i in range(1, n + 1)]

    def generate_row_labels_name(self, row_labels_name):
        if row_labels_name is not None:
            return row_labels_name

        if len(self.data.shape) == 1:
            return ''

        if len(self.data.shape) == 2:
            return f'${self.desc.rows}_{{i}}$'

    @staticmethod
    def from_group(group: List):
        data = np.array([t.data for t in group]).T
        desc = TableDesc(
            caption=', '.join(t.desc.caption for t in group),
            label='_'.join(t.desc.label for t in group),
            symbol=None,
            rows=group[0].desc.rows,
            cols=None
        )
        col_labels = [t.desc.symbol for t in group]
        return Table(data=data, desc=desc, col_labels=col_labels)


class MCDA_results:
    def __init__(self,
                 method: MCDA_method,
                 matrix: ArrayLike,
                 results: List[Table]):
        self.method = method
        self.method_name = method.__class__.__name__
        self.matrix = matrix
        self.results = results

    def prepare_output(self,
                       group_tables: bool = True,
                       ranking: bool = True,
                       matrix: bool = True,
                       label_prefix: bool = True,
                       float_fmt: str or List[str] or None = '%0.4f',
                       output_function=None):
        output_strs = [f'Results of the {self.method_name}.']
        if matrix:
            t = Table(data=self.matrix,
                      desc=TableDesc(caption='Decision matrix',
                                     label='matrix', symbol='$x_{ij}$', rows='A', cols='C'))
            output_strs.append(output_function(t, float_fmt))

        grouped_tables = []
        last_group_spec = ()
        for t in self.results:
            if len(t.data.shape) == 2:  # Can't group 2d tables
                output_strs.append(output_function(t, float_fmt))
            elif not group_tables:  # If grouping is not enabled just add the table to final output
                output_strs.append(output_function(t, float_fmt))
            else:  # Process table for the grouping
                t_spec = (t.desc.rows, t.desc.cols)
                if last_group_spec == t_spec:  # Table fits last group
                    grouped_tables[-1].append(t)
                else:  # Create new group which will include current table and update last_group_spec
                    last_group_spec = t_spec
                    grouped_tables.append([t])

        if ranking:
            ranking_table = Table(data=self.method.rank(self.results[-1].data),
                                  desc=TableDesc(caption='Final ranking',
                                                 label='ranking', symbol='$R_{i}$', rows='A', cols=None))
            if group_tables and last_group_spec == ('A', None):  # If grouping is enabled and ranking fits last group
                grouped_tables[-1].append(ranking_table)
            else:  # If not, just add as another table
                output_strs.append(output_function(ranking_table, float_fmt))

        if group_tables:
            for group in grouped_tables:
                output_strs.append(output_function(Table.from_group(group), float_fmt))

        output_strs.append(f'Total {len(output_strs) - 1} tables.')

        return '\n\n'.join(output_strs)

    def to_latex(self, **kwargs):
        return self.prepare_output(output_function=lambda t, ff: t.to_latex(ff), **kwargs)

    def to_string(self, **kwargs):
        return self.prepare_output(output_function=lambda t, ff: t.to_string(ff), **kwargs)


    def __str__(self):
        return 'Not implemented yet'

    def __dict__(self):
        pass
