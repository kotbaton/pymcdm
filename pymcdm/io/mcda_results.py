# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List, TypeVar

from numpy.typing import ArrayLike
from . import Table, TableDesc

MCDA_method = TypeVar('MCDA_method')

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
        A list of `Table` objects representinghttps://www.reddit.com/r/Polska/comments/1gr0vdy/czym_myjecie_d%C5%82ugie_w%C5%82osy/ the analysis results.

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
                       label_prefix: bool = True,
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
        if label_prefix:  # Check if label_prefix is enabled and use appropriate value for it
            label_prefix = self.method_name.lower()
        else:
            label_prefix = ''

        output_strs = [f'Results for the {self.method_name} method.']
        if matrix:
            t = Table(data=self.matrix,
                      desc=TableDesc(caption='Decision matrix',
                                     label='matrix', symbol='$x_{ij}$', rows='A', cols='C'))
            if fix_integers:
                t.fix_integers()
            output_strs.append(output_function(t, float_fmt, label_prefix))

        grouped_tables = []
        last_group_spec = ()
        for t in self.results:
            if not group_tables:  # If grouping is not enabled just add the table to final output
                output_strs.append(output_function(t, float_fmt, label_prefix))
            elif len(t.data.shape) == 2:
                # Add 2d table to grouped_tables to preserve correct order of displaying
                grouped_tables.append(t)
                # Reset last_group_spec to force create new group if next table is 1d
                last_group_spec = ()
            else:  # Process 1d table for the grouping
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
                output_strs.append(output_function(ranking_table, float_fmt, label_prefix))

        if group_tables:
            for i, group in enumerate(grouped_tables):
                if isinstance(group, Table):  # Check if we deal with real group or 2d table
                    output_strs.append(output_function(group, float_fmt, label_prefix))
                    continue

                t = Table.from_group(group)

                # If this is last group we need to explicitly fix integers (in ranking)
                if fix_integers and ranking and i == len(grouped_tables) - 1:
                    t.fix_integers()

                output_strs.append(output_function(t, float_fmt, label_prefix))

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
        return self.prepare_output(output_function=lambda t, ff, lp: t.to_latex(ff, lp), **kwargs)

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
        return self.prepare_output(output_function=lambda t, ff, lp: t.to_string(ff, lp), **kwargs)

    def __str__(self):
        """
        Returns the string representation of the MCDA results, equivalent to `to_string()`.

        Returns
        -------
        str
            String representation of the MCDA results.
        """
        return self.to_string()

    def to_dict(self):
        """
        Returns a dictionary of the results with captions as keys and np.array objects as values.

        Returns
        -------
        dict
            Dictionary where keys are captions of the tables in `results` and values are the np.array objects.
        """
        return {t.desc.caption: t.data for t in self.results}