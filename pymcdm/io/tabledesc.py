# Copyright (c) 2024 Andrii Shekhovtsov
import numpy as np
from .. import io

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
    rows : str or list[str] or None
        Defines the labels of data stored in the rows of the table. Use 'C' to indicate criteria, or 'A' to
        indicate alternatives. Usage of custom symbol will result in labels like: $S_1$, $S_2$, etc.
        If list provided, then labels from the list will be used.
        Defaults to None if unspecified.
    cols : str or list[str] or None
        Defines the labels of data stored in the columns of the table. Use 'C' to indicate criteria, or 'A' to
        indicate alternatives. Usage of custom symbol will result in labels like: $S_1$, $S_2$, etc.
        If list provided, then labels from the list will be used.

    Attributes
    ----------
    caption : str
        The description or caption of the table.
    label : str
        The short reference label for the table in LaTeX or other references.
    symbol : str or None
        Mathematical symbol associated with the table data.
    rows : str or list[str] or None
        Defines the labels of data stored in the rows of the table. Use 'C' to indicate criteria, or 'A' to
        indicate alternatives. Usage of custom symbol will result in labels like: $S_1$, $S_2$, etc.
        If list provided, then labels from the list will be used.
        Defaults to None if unspecified.
    cols : str or list[str] or None
        Defines the labels of data stored in the columns of the table. Use 'C' to indicate criteria, or 'A' to
        indicate alternatives. Usage of custom symbol will result in labels like: $S_1$, $S_2$, etc.
        If list provided, then labels from the list will be used.
    """

    def __init__(self,
                 caption: str,
                 label: str,
                 symbol: str or None = None,
                 rows: str or list[str] or None = None,
                 cols: str or list[str] or None = None):
        self.caption = caption
        self.label = label
        self.symbol = symbol
        self.rows = self.validate_option(rows)
        self.cols = self.validate_option(cols)

    def create_table(self, data: np.ndarray | list | tuple):
        return io.Table(data, self)

    @staticmethod
    def validate_option(opt: str or list[str] or None):
        """
        Validates the provided option for row or column designation in a table.

        This method ensures that the input `opt` is valid for designating rows or columns in a table.
        The valid options are:
        - "C" for criteria
        - "A" for alternatives
        - Any other str which will be changed in the list of labels with lower index.
        - None if not used
        - A callable with a signature foo(n: int) -> list[str]
        - A list of strings, where each string represents a valid label.

        If the input does not meet these criteria, a `ValueError` is raised.

        Parameters
        ----------
        opt : str | list[str] | Callable | None
            The option to validate. This can be:

            - A string: "C" (criteria) or "A" (alternatives) or other string.
            - A callable object with signature foo(n: int) -> list[str].
            - A list of strings, where all elements are valid labels.
            - None

        Returns
        -------
        str | list[str] | Callable | None
            The validated option, returned unchanged if it is valid.

        Raises
        ------
        ValueError
            If `opt` is not one of the required types.
        """
        if opt is not None\
                and not isinstance(opt, str)\
                and not callable(opt)\
                and not all(isinstance(v, str) for v in opt):
            raise ValueError('Valid arguments for cols or rows are str, list[str] or None.')
        return opt
