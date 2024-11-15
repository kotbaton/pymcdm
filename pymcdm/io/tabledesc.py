# Copyright (c) 2024 Andrii Shekhovtsov
from numpy.typing import ArrayLike
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

    def create_table(self, data: ArrayLike):
        return io.Table(data, self)

    @staticmethod
    def validate_option(opt: str or list[str] or None):
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
        if opt is not None\
                and not isinstance(opt, str)\
                and not all(isinstance(v, str) for v in opt):
            raise ValueError('Valid arguments for cols or rows are str, list[str] or None.')
        return opt
