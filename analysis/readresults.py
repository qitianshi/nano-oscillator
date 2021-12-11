"""Finds and reads data and datasets from results."""

import os
from re import sub
from shutil import rmtree
import pandas as pd


def prep_dir(path: str):
    """Prepares the destination directory for output. Clears existing files and
    creates an empty directory.
    """

    if os.path.exists(path):
        rmtree(path)

    os.mkdir(path)


def find_result(date: str = None) -> str:
    """Returns the path of the requested result.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm"). If
          not given, the most recent result is returned.

    Returns:
        str: The path of the result.
    """

    results_path = os.path.join(os.path.dirname(__file__), os.pardir, 'results')
    requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]

    return os.path.join(results_path, requested_result)


def find_dataset(date: str = None, var: list[str] = None) -> tuple[str, tuple[str]]:
    """Returns the path of the dataset split by the requested variables.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm").
          If not given, the latest result is searched.
        var (list[str]): An ordered list of variables, in order of how the data
          was split. If not given, the path of the raw dataset is returned.

    Returns:
        str: The path of the requested dataset.
    """


def find_data(date: str = None, vals: dict[str, str] = None) -> str:
    """Returns the path of the data split by the requested variables and
    values.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm").
          If not given, the latest result is searched.
        vals (dict[str, str]): An ordered dict of variable names and their
          values, in order of how the data was split. If not given, the path
          of the raw data is returned.

    Returns:
        str: The path of the requested dataset.
    """

    if vals is None:
        return os.path.join(find_result(date), "raw.out", "table.tsv")
    else:
        return os.path.join(
            find_result(date),
            "split",
            ", ".join(vals.keys()),
            *list(vals.values())[:-1],
            ", ".join(vals.values()) + ".tsv"
        )


def read_data(path: str) -> pd.DataFrame:
    """Reads a data file into a Pandas DataFrame."""

    with open(path, 'r', encoding="utf-8") as file:

        names = file.readline().strip('#').split('\t')
        names = [sub(r"[\(].*?[\)]", "", i) for i in names]    # Removes units in brackets.
        names = [i.strip() for i in names]

        return pd.read_csv(path, sep='\t', skiprows=1, names=names)
