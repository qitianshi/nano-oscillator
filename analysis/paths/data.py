"""Data and datasets."""

import os
import warnings

from analysis.paths import top


def raw(date: str = None, datum: str = None) -> str:
    """Returns the path of data in the raw directory.
     Args:
        datum (str): The name of the file in the raw directory. If not given,
          returns the root of the raw directory.
     """

    if datum is None:
        return os.path.join(top.result_dir(date), "raw")
    else:
        return os.path.join(raw(date, datum=None), datum)


def dataset_dir(date: str = None, vals: dict[str, str] = None) -> tuple[str, tuple[str]]:
    """Returns the path of the dataset split by the requested variables.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm").
        If not given, the latest result is searched.
        vals (dict[str, str]): An ordered dict of variable names and their
        values, in order of how the data was split. If not given, the path
        of the unsplit data is returned. The path that is returned stops at
        the first item whose value is `None`.

    Returns:
        str: The path of the requested dataset. The path stops at the first
        item in `vals` whose value is `None`.
    """

    if vals is None:

        warnings.warn(
            "Using `dataset_dir` to return the path of the raw data directory is deprecated and"
            + " will be removed in the future. Use `paths.top.raw` instead.",
            DeprecationWarning
        )

        return raw(date, datum=None)

    else:
        return os.path.join(
            top.result_dir(date),
            "split",
            ", ".join(vals.keys()),
            *[i for i in list(vals.values())[:-1] if i is not None]
        )


def data_path(date: str = None, vals: dict[str, str] = None) -> str:
    """Returns the path of the data split by the requested variables and
    values.
    """

    if vals is None:
        return os.path.join(dataset_dir(date, vals), "table.tsv")
    else:
        return os.path.join(dataset_dir(date, vals), ", ".join(vals.values()) + ".tsv")
