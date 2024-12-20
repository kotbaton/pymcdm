# Copyright (c) 2024 Andrii Shekhovtsov
from typing import List, TypeVar

import numpy as np

from . import Table, TableDesc

MCDA_method = TypeVar('MCDA_method')

class MCDA_results:
    """
    Represents the results of a Multi-Criteria Decision Analysis (MCDA) method,
    including the decision matrix, processed results tables, and optional ranking.

    Parameters
    ----------
    method : MCDA_method
        The MCDA method used for analysis.
    matrix : np.ndarray | list | tuple
        The decision matrix used as input for the analysis.
    results : list of Table
        A list of `Table` objects representing the analysis results.

    Attributes
    ----------
    method : MCDA_method
        The MCDA method used to generate the results.
    method_name : str
        The name of the MCDA method class.
    matrix : np.ndarray | list | tuple
        The decision matrix used as input for the MCDA method.
    results : list of Table
        A list of `Table` objects representing the analysis results.
    """

    def __init__(self,
                 method: MCDA_method,
                 matrix: np.ndarray | list | tuple,
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
        if ranking and self.method_name == 'PROMETHEE_I':
            raise ValueError("Can't generate ranking for PROMETHEE I as it returns partial ranking.")

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
            Additional keyword arguments passed to `prepare_output()`.

        Returns
        -------
        str
            LaTeX-formatted string of the MCDA results.
        """
        s = self.prepare_output(output_function=lambda t, ff, lp: t.to_latex(ff, lp), **kwargs)
        return s.replace('\\caption', '\\centering\n\\caption')

    def to_string(self, **kwargs):
        """
        Returns the MCDA results formatted as a plain text string.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments passed to `prepare_output()`.

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