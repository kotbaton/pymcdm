# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List, TypeVar, Sequence

import numpy as np
from numpy.typing import ArrayLike
import pandas as pd

from .validators import (validate_decision_problem,
                         esp_bounds_validator,
                         bounds_validator,
                         matrix_bounds_validator,
                         cvalues_validator,
                         matrix_cvalues_validator,
                         ref_ideal_bounds_validator,
                         matrix_ref_point_validator)

MCDA_method = TypeVar('MCDA_method')


class MCDA_problem:
    """
    Represents a Multi-Criteria Decision Analysis (MCDA) problem by aggregating elements 
    of the decision problem and presenting them in a tabular format as text or LaTeX code. 
    The `matrix` argument is used solely for validating the consistency of other parameters.

    Attributes
    ----------
    df : pandas.DataFrame
        A DataFrame containing the criteria description, including weights, types, names, units, 
        cvalues, bounds, expected values, and reference ideals.
    columns_order : list of str
        The default order of columns for display in the DataFrame.
    """
    def __init__(self,
                 matrix: ArrayLike,
                 weights: ArrayLike,
                 types: Sequence[{1, -1}],
                 criteria_names: Sequence[str] = None,
                 criteria_units: Sequence[str] = None,
                 cvalues: ArrayLike = None,
                 bounds: ArrayLike = None,
                 esp: Sequence[float or int] = None,
                 ref_ideal: ArrayLike = None):
        """
        Initializes an MCDA_problem instance, validating the consistency of weights, types,
        and other optional parameters with the decision matrix.

        Parameters
        ----------
        matrix : ArrayLike
            Decision matrix for validating dimensions and consistency of the problem.
            It will not be stored or outputted by to_latex() and to_string() methods.
        weights : ArrayLike
            Array of weights assigned to each criterion.
        types : Sequence[{1, -1}]
            Sequence indicating the optimization direction for each criterion
            (1 for maximization/profit, -1 for minimization/cost).
        criteria_names : Sequence[str], optional
            List of names for each criterion, by default None.
        criteria_units : Sequence[str], optional
            List of units for each criterion, by default None.
        cvalues : ArrayLike, optional
            Array of characteristic values associated with each criterion, by default None.
            Normally used in the COMET method.
        bounds : ArrayLike, optional
            Array of bounds for each criterion, by default None.
            Normally used in such methods as SPOTIS and RIM.
        esp : Sequence[float or int], optional
            Expected values for each criterion, by default None.
            Normally used in the ESPExpert class.
        ref_ideal : ArrayLike, optional
            Reference ideal values for each criterion, by default None.
            Normally used in the RIM method.

        Raises
        ------
        ValueError
            If `matrix` or `types` size does not match `weights`.
            If `criteria_names` or `criteria_units` length does not match `weights`.
            If `esp`, or `ref_ideal` are provided without `bounds` for validation.
            If the shape of `cvalues` is not supported.
        """
        matrix = np.asarray(matrix)
        weights = np.asarray(weights)
        types = np.asarray(types)
        validate_decision_problem(matrix, weights, types)  # Validate dimensions of the basic parts of the problem
        data = {
            'Weight': weights,
            'Type': ['Max' if t == 1 else 'Min' for t in types],
            '$C_i$': [f'$C_{{{i}}}$' for i in range(1, len(weights) + 1)]
        }

        if criteria_names is not None:
            if len(criteria_names) != len(weights):
                raise ValueError('Criteria_names should have same length as weights.')
            data['Criterion Name'] = criteria_names

        if criteria_units is not None:
            if len(criteria_units) != len(weights):
                raise ValueError('Criteria_units should have same length as weights.')
            data['Unit'] = criteria_units

        if cvalues is not None:
            cvalues = np.asarray(cvalues)
            cvalues_validator(cvalues)
            matrix_cvalues_validator(matrix, cvalues)
            if cvalues.shape[1] == 3:
                data['$CV_1$'] = cvalues[:, 0]
                data['$CV_3$'] = cvalues[:, -1]
                data['$CV_2$'] = cvalues[:, 1]
            else:
                print('Other then 3 cvalues is not supported.')

        if bounds is not None:
            bounds = np.asarray(bounds)
            bounds_validator(bounds)
            matrix_bounds_validator(matrix, bounds)
            data['Min'] = bounds[:, 0]
            data['Max'] = bounds[:, 1]
        elif cvalues is not None:  # Derive bounds variable from cvalues if not provided
            bounds = cvalues[:, [0, -1]]
        elif esp is not None or ref_ideal is not None:
            raise ValueError('If you want to use esp or/and ref_ideal you need to provide bounds for validation.')

        if esp is not None:
            esp = np.asarray(esp)
            esp_bounds_validator(esp, bounds)
            data['Expected value'] = esp

        if ref_ideal is not None:
            ref_ideal = np.asarray(ref_ideal)
            ref_ideal_bounds_validator(ref_ideal, bounds)
            matrix_ref_point_validator(matrix, ref_ideal)
            data['Ref. ideal Min'] = ref_ideal[:, 0]
            data['Ref. ideal Max'] = ref_ideal[:, 1]

        self.df = pd.DataFrame(data)
        self.columns_order = ['$C_i$', 'Criterion Name', 'Unit', 'Weight',
                              'Type', 'Min', 'Max', '$CV_1$', '$CV_2$', '$CV_3$',
                              'Expected value', 'Ref. ideal Min', 'Ref. ideal Max']

    def to_latex(self, float_fmt: str or None = '%0.4f'):
        """
        Returns a LaTeX-formatted table of the criteria description.

        Parameters
        ----------
        float_fmt : str or None, optional
            Format for floating-point numbers, by default '%0.4f'.

        Returns
        -------
        str
            LaTeX-formatted string of the criteria description table.
        """
        used_columns = [c for c in self.columns_order if c in self.df.columns]
        s = self.df[used_columns].to_latex(
            index=False,
            float_format=float_fmt,
            position='h',
            label='crit_desc',
            caption='Criteria description.',
        )
        return s

    def to_string(self, float_fmt: str or None = '%0.4f'):
        """
        Returns a plain text table of the criteria description.

        Parameters
        ----------
        float_fmt : str or None, optional
            Format for floating-point numbers, by default '%0.4f'.

        Returns
        -------
        str
            Plain text representation of the criteria description table.
        """
        used_columns = [c for c in self.columns_order if c in self.df.columns]
        s = self.df[used_columns].to_string(
            index=False,
            float_format=float_fmt,
        )
        return f'Criteria description.\n{s}'

    def __str__(self):
        """
        Returns a string representation of the criteria description, equivalent to `to_string()`.

        Returns
        -------
        str
            String representation of the criteria description.
        """
        return self.to_string()


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
    def validate_option(opt: str or None):
        """
        Validates the option provided for row or column designation in the table.

        This method checks if the specified option for rows or columns is valid. Accepted values
        are "C" for criteria, "A" for alternatives, or None. If the input is invalid, a ValueError
        is raised.

        Parameters
        ----------
        opt : str or None
            The option to validate, which should be either "C" (for criteria), "A" (for alternatives),
            or None.

        Returns
        -------
        str or None
            The validated option, returned unchanged if it is valid.

        Raises
        ------
        ValueError
            If `opt` is not one of {"C", "A", None}.
        """
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


class MCDA_results:
    """
    Represents the results of a Multi-Criteria Decision Analysis (MCDA) method,
    including the decision matrix, processed results tables, and optional ranking.

    Attributes
    ----------
    method : MCDA_method
        The MCDA method used to generate the results.
    method_name : str
        The name of the MCDA method class.
    matrix : ArrayLike
        The decision matrix used as input for the MCDA method.
    results : list of Table
        A list of `Table` objects representing the analysis results.

    Methods
    -------
    prepare_output(group_tables=True, ranking=True, matrix=True, label_prefix=True,
                   float_fmt='%0.4f', fix_integers=True, output_function=None)
        Prepares the formatted output string for the results, supporting options for
        table grouping, rankings, matrix display, and formatting options.

    to_latex(**kwargs)
        Returns the results formatted as a LaTeX string, using the `prepare_output` method.

    to_string(**kwargs)
        Returns the results formatted as a plain text string, using the `prepare_output` method.

    __str__()
        Returns the results formatted as a string, equivalent to `to_string()`.

    __dict__()
        Returns a dictionary where the keys are the captions of the tables in `results`
        and the values are the corresponding `Table` objects.
    """

    def __init__(self,
                 method: MCDA_method,
                 matrix: ArrayLike,
                 results: List[Table]):
        """
        Initializes an MCDA_results instance.

        Parameters
        ----------
        method : MCDA_method
            The MCDA method used for analysis.
        matrix : ArrayLike
            The decision matrix used as input for the analysis.
        results : list of Table
            A list of `Table` objects representing the analysis results.
        """
        self.method = method
        self.method_name = method.__class__.__name__
        self.matrix = matrix
        self.results = results

    def prepare_output(self,
                       group_tables: bool = True,
                       ranking: bool = True,
                       matrix: bool = True,
                       label_prefix: bool = True,  # TODO implement it
                       float_fmt: str or None = '%0.4f',
                       fix_integers=True,
                       output_function=None):
        """
        Prepares the formatted output string for the MCDA results, with options for
        grouping tables, including rankings, and displaying the decision matrix.
        Not meant for explicit usage.

        Parameters
        ----------
        group_tables : bool, optional
            Whether to group tables with similar structure, by default True.
        ranking : bool, optional
            Whether to include the ranking table in the output, by default True.
        matrix : bool, optional
            Whether to include the decision matrix in the output, by default True.
        label_prefix : bool, optional
            Whether to use label prefixes in the output, by default True.
        float_fmt : str or None, optional
            Format for floating-point numbers, by default '%0.4f'.
        fix_integers : bool, optional
            Whether to round integer values in tables, by default True.
            Applied only to decision matrix and ranking. Work only if all column is integer.
        output_function : callable, optional
            Function to format each table, passed as a function argument.

        Returns
        -------
        str
            The formatted output as a string, with grouped tables, rankings,
            and decision matrix if specified.
        """
        output_strs = [f'Results for the {self.method_name} method.']
        if matrix:
            t = Table(data=self.matrix,
                      desc=TableDesc(caption='Decision matrix',
                                     label='matrix', symbol='$x_{ij}$', rows='A', cols='C'))
            if fix_integers:
                t.fix_integers()
            output_strs.append(output_function(t, float_fmt))

        # TODO rewrite here so the order of grouped and not grouped tables will be preserved (same as in method)
        # TODO now the order is wrong in for example EDAS (AV is in the middle but should be first), ERVD
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
            if fix_integers:
                ranking_table.fix_integers()
            if group_tables and last_group_spec == ('A', None):  # If grouping is enabled and ranking fits last group
                grouped_tables[-1].append(ranking_table)
            else:  # If not, just add as another table
                output_strs.append(output_function(ranking_table, float_fmt))

        if group_tables:
            for i, group in enumerate(grouped_tables):
                t = Table.from_group(group)

                # If this is last group we need to explicitly fix integers (in ranking)
                if fix_integers and ranking and i == len(grouped_tables) - 1:
                    t.fix_integers()

                output_strs.append(output_function(t, float_fmt))

        output_strs.append(f'Total {len(output_strs) - 1} tables.\n')

        return '\n\n'.join(output_strs)

    def to_latex(self, **kwargs):
        """
        Returns the MCDA results formatted as a LaTeX string.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments passed to `prepare_output`.

        Returns
        -------
        str
            LaTeX-formatted string of the MCDA results.
        """
        return self.prepare_output(output_function=lambda t, ff: t.to_latex(ff), **kwargs)

    def to_string(self, **kwargs):
        """
        Returns the MCDA results formatted as a plain text string.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments passed to `prepare_output`.

        Returns
        -------
        str
            Plain text string of the MCDA results.
        """
        return self.prepare_output(output_function=lambda t, ff: t.to_string(ff), **kwargs)

    def __str__(self):
        """
        Returns the string representation of the MCDA results, equivalent to `to_string()`.

        Returns
        -------
        str
            String representation of the MCDA results.
        """
        return self.to_string()

    def __dict__(self):
        """
        Returns a dictionary of the results with captions as keys and np.array objects as values.

        Returns
        -------
        dict
            Dictionary where keys are captions of the tables in `results` and values are the np.array objects.
        """
        return {t.desc.caption: t.data for t in self.results}
