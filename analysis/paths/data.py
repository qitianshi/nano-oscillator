"""Data and datasets."""

import os

from analysis.paths import top


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
        return os.path.join(top.result_dir(date), "raw")
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
