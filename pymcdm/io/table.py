# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List, TypeVar

import numpy as np
from numpy.typing import ArrayLike
import pandas as pd

from ..io import TableDesc

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
        self.data = np.asarray(data)
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

    def to_latex(self, float_fmt: str or None = '%0.4f'):
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

        Returns
        -------
        str
            A string containing the table in LaTeX tabular format, ready for use in LaTeX documents.
        """
        return self.df.to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label=f'tab:{self.desc.label}',
            caption=self.desc.caption,
        )

    def to_string(self, float_fmt: str or None = '%0.4f'):
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

        Returns
        -------
        str
            A string representation of the table with the caption followed by the table data.
        """
        s = self.df.to_string(
            index=False,
            float_format=float_fmt,
        )
        return f'{self.desc.caption}\n{s}'

    def __str__(self):
        return self.to_string()

    def generate_row_labels(self, row_labels: List[str] or None):
        """
        Generates or validates row labels for the table based on the provided labels or metadata.

        This method checks if custom row labels are provided. If so, it validates that the number
        of labels matches the number of rows in the table's data. If no labels are provided, it generates
        default row labels using the symbol defined in the table's `desc` metadata.

        Parameters
        ----------
        row_labels : list of str or None
            A list of custom row labels. If None, default labels are generated based on the symbol in
            `desc.rows`, typically representing criteria or alternatives.

        Returns
        -------
        list of str
            A list of row labels, either validated custom labels or automatically generated labels
            based on the table's data shape.

        Raises
        ------
        ValueError
            If `row_labels` is provided but does not match the number of rows in the data.
        """
        n = self.data.shape[0]
        if row_labels is not None:
            if len(row_labels) != n:
                raise ValueError('row_labels should have same number of elements as number'
                                 f' of rows in data ({n}).')
            return row_labels

        sym = self.desc.rows
        return [f'${sym}_{{{i}}}$' for i in range(1, n + 1)]

    def generate_col_labels(self, col_labels: List[str] or None):
        """
        Generates or validates column labels for the table based on the provided labels or metadata.

        This method checks if custom column labels are provided. If so, it validates that the number of
        labels matches the number of columns in the table's data. If no labels are provided, it generates
        default column labels using the symbol defined in the table's `desc` metadata.

        Parameters
        ----------
        col_labels : list of str or None
            A list of custom column labels. If None, default labels are generated based on the symbol
            in `desc.cols`, typically representing criteria or alternatives.

        Returns
        -------
        list of str
            A list of column labels, either validated custom labels or automatically generated labels
            based on the table's data shape.

        Raises
        ------
        ValueError
            If `col_labels` is provided but does not match the number of columns in the data.
        """
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

    def generate_row_labels_name(self, row_labels_name: str or None):
        """
        Generates or returns a row label name based on provided input or metadata.

        This method determines the name for the row labels column in the table. If a custom row label name
        is provided, it returns that name. Otherwise, it generates a default name based on the table's data
        dimensions and metadata from `desc`.

        Parameters
        ----------
        row_labels_name : str or None
            A custom name for the row labels column. If None, a default name is generated based on the
            table's shape and metadata.

        Returns
        -------
        str
            The row labels name, either the provided custom name or a generated default name.
        """
        if row_labels_name is not None:
            return row_labels_name

        if len(self.data.shape) == 1:
            return ''

        if len(self.data.shape) == 2:
            return f'${self.desc.rows}_{{i}}$'

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
        desc = TableDesc(
            caption=', '.join(t.desc.caption for t in group),
            label='_'.join(t.desc.label for t in group),
            symbol=None,
            rows=group[0].desc.rows,
            cols=None
        )
        col_labels = [t.desc.symbol for t in group]
        return Table(data=data, desc=desc, col_labels=col_labels)
