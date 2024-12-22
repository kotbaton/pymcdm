# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List, Callable

import numpy as np
import pandas as pd

from ..io import TableDesc


class Table:
    """
    Represents a table containing data for Multi-Criteria Decision Analysis (MCDA) processes, supporting LaTeX
    export and formatted row and column labeling.

    Parameters
    ----------
    data : np.ndarray | list | tuple
        The data for the table, either a 1D or 2D array, representing different data.
        This data is automatically converted to a NumPy array.
    desc : TableDesc
        Metadata for the table, provided as a `TableDesc` instance, including caption, label, and symbol
        information used in LaTeX representations.

    Raises
    ------
    ValueError
        If the shape of `data` is not supported (only 1D or 2D arrays are allowed).

    Attributes
    ----------
    data : np.ndarray
        The primary data of the table, stored as a NumPy array.
    desc : TableDesc
        The metadata description of the table, including caption and label information.
    row_labels : List[str] or Callable
        List of labels for the table's rows. Can be Callable with signature foo(n: int) -> List[str].
        Size of the returned list should be same as number of rows in the Table (`n`).
    col_labels : List[str] or Callable
        List of labels for the table's columns. Can be Callable with signature foo(n: int) -> List[str].
        Size of the returned list should be same as number of columns in the Table (`n`).
    row_labels_name : str
        The name or title of the row labels column in the table.
    caption : str
        Caption of the table. Caption with symbol from TableDesc will be used or
        only caption if no symbol is provided. Symbol will be added only if table
        is 2d.
    df : pd.DataFrame
        A pandas DataFrame representation of the table, including row and column labels as well as data.
    """

    def __init__(self,
                 data: np.ndarray | list | tuple,
                 desc: TableDesc):
        self.data = np.asarray(data)
        self.desc = desc

        if len(self.data.shape) > 2:
            raise ValueError(f'Data shape {self.data.shape} is not supported.')

        self.row_labels = self.generate_row_labels()
        self.col_labels = self.generate_col_labels()
        self.row_labels_name = self.generate_row_labels_name()

        if len(self.data.shape) == 2:
            self.df = pd.DataFrame(data=self.data, columns=self.col_labels)
            self.df.insert(0, self.row_labels_name, self.row_labels)
        else:
            self.df = pd.DataFrame(data=[self.data], columns=self.row_labels)
            self.df.insert(0, '', [self.desc.symbol])

        if self.desc.symbol is not None and len(self.data.shape) == 2:
            self.caption = f'{self.desc.caption} ({self.desc.symbol})'
        else:
            self.caption = self.desc.caption

    def fix_integers(self):
        """
        Converts columns in the table's DataFrame to integer type if all values in the column are integers.
        """
        for col in self.df.columns:
            try:
                if all(self.df[col].apply(float.is_integer)):
                    self.df[col] = self.df[col].astype(int)
            except TypeError:
                continue

    def to_latex(self, float_fmt: str or None = '%0.4f', label_prefix=''):
        """
        Exports the table as a LaTeX-formatted string, with optional floating-point formatting.

        This method generates a LaTeX tabular representation of the table's DataFrame, including metadata
        such as a caption and label for referencing. The float format can be specified to control the
        precision of numeric values in the output.

        Parameters
        ----------
        float_fmt : str or None, optional
            A formatting string that specifies the precision of floating-point numbers in the table.
            Defaults to '%0.4f' for four decimal places.
        label_prefix : str, optional
            Add prefix to the label, for example if label_prefix='topsis' label will be 'tab:topsis_matrix'
            instead of 'tab:matrix'. If used with MCDA_results class, name of the method will be used
            as the prefix.

        Returns
        -------
        str
            A string containing the table in LaTeX tabular format, ready for use in LaTeX documents.
        """
        return self.df.to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label=f'tab:{self.desc.label}' if not label_prefix else f'tab:{label_prefix}_{self.desc.label}',
            caption=self.caption,
        )

    def to_string(self, float_fmt: str or None = '%0.4f', label_prefix=''):
        """
        Returns a string representation of the table with an optional floating-point format.

        This method generates a plain-text string representation of the table's DataFrame, including
        the table's caption as a header. The float format can be specified to control the precision
        of numeric values in the output.

        Parameters
        ----------
        float_fmt : str or None, optional
            A formatting string specifying the precision of floating-point numbers in the table.
            Defaults to '%0.4f', showing four decimal places.
        label_prefix : str, optional
            Unused in this method.

        Returns
        -------
        str
            A string representation of the table with the caption followed by the table data.
        """
        s = self.df.to_string(
            index=False,
            float_format=float_fmt,
        )
        return f'{self.caption}\n{s}'

    def __str__(self):
        return self.to_string()

    def generate_row_labels(self):
        """
        Generates or validates row labels for the table based on the provided labels in metadata.

        Returns
        -------
        list of str
            A list of row labels, either validated custom labels or automatically generated labels
            based on the table's data shape.

        Raises
        ------
        ValueError
            If `rows` is provided as sequence but does not match the number of rows in the data.
            If provided value's type is wrong.
        """
        n = self.data.shape[0]
        rows = self.desc.rows
        # If rows are Callable then we try to use it and then verify output
        if callable(rows):
            rows = rows(n)

        if isinstance(rows, (list, tuple, np.ndarray)):
            if len(rows) != n:
                raise ValueError('rows should have same number of elements as number'
                                 f' of rows in data ({n}).')
            return rows
        elif isinstance(rows, str):
            return [f'${rows}_{{{i}}}$' for i in range(1, n + 1)]
        else:
            raise ValueError('rows should be List[str] or Callable which returns List[str] of the proper length.')

    def generate_col_labels(self):
        """
        Generates or validates column labels for the table based on the provided labels in metadata.

        Returns
        -------
        list of str
            A list of column labels, either validated custom labels or automatically generated labels
            based on the table's data shape.

        Raises
        ------
        ValueError
            If `cols` is provided but does not match the number of columns in the data.
            If provided value's type is wrong.
        """
        cols = self.desc.cols
        if len(self.data.shape) == 1:
            if isinstance(cols, str):
                return [cols]
            else:
                return cols

        n = self.data.shape[1]
        if callable(cols):
            cols = cols(n)

        if isinstance(cols, (list, tuple, np.ndarray)):
            if len(cols) != n:
                raise ValueError('cols should have same number of elements as number'
                                 f' of columns in data ({n}).')
            return cols
        elif isinstance(cols, str):
            return [f'${cols}_{{{i}}}$' for i in range(1, n + 1)]
        else:
            raise ValueError('cols should be List[str] or Callable which returns List[str] of the proper length.')

    def generate_row_labels_name(self):
        """
        Generates or returns a row label name based on provided metadata.

        Returns
        -------
        str
            The row labels name.
        """
        rows = self.desc.rows
        if len(self.data.shape) == 2 and isinstance(rows, str):
            return f'${rows}_{{j}}$' if rows == "C" else f'${rows}_{{i}}$'
        else:
            return ''

    @staticmethod
    def from_group(group: List):
        """
        Creates a new `Table` instance by combining data from a group of existing `Table` objects.

        This method aggregates the `data` attributes of multiple `Table` instances into a single table,
        where each original table contributes a column in the new table. Metadata for the new table,
        including a combined caption and label, is generated based on the metadata of the individual
        `Table` objects in the group. Aggregated tables should contain only 1d data.

        Parameters
        ----------
        group : list of Table
            A list of `Table` instances to be combined. Each table in the group should share compatible
            dimensions and metadata.

        Returns
        -------
        Table
            A new `Table` instance containing the combined data and generated metadata.

        Raises
        ------
        ValueError
            If the `group` if the tables have incompatible data shapes.
        """
        if any(len(t.data.shape) != 1 for t in group):
            raise ValueError('All tables in group should be 1d.')

        data = np.array([t.data for t in group]).T
        col_labels = [t.desc.symbol for t in group]
        desc = TableDesc(
            caption=', '.join(t.desc.caption for t in group),
            label='_'.join(t.desc.label for t in group),
            symbol=None,
            rows=group[0].desc.rows,
            cols=col_labels
        )
        return Table(data=data, desc=desc)
