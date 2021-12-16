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

    os.makedirs(path)


def result_dir(date: str = None) -> str:
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


def dataset_dir(date: str = None, vals: dict[str, str] = None) -> tuple[str, tuple[str]]:
    """Returns the path of the dataset split by the requested variables.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm").
          If not given, the latest result is searched.
        vals (dict[str, str]): An ordered dict of variable names and their
          values, in order of how the data was split. If not given, the path
          of the raw data is returned. The path that is returned stops at the
          first item whose value is `None`.

    Returns:
        str: The path of the requested dataset. The path stops at the first
          item in `vals` whose value is `None`.
    """

    if vals is None:
        return os.path.join(result_dir(date), "raw.out")
    else:
        return os.path.join(
            result_dir(date),
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


def amplitude_path(date: str = None, phi: str = None) -> str:

    """Returns the path of the amplitude data."""

    amplitude_dir = os.path.join(result_dir(date), "amplitudes")
    return os.path.join(amplitude_dir, f"{phi}deg.tsv")


def read_data(path: str) -> pd.DataFrame:
    """Reads a data file into a Pandas DataFrame."""

    with open(path, 'r', encoding="utf-8") as file:

        names = file.readline().strip('#').split('\t')
        names = [sub(r"[\(].*?[\)]", "", i) for i in names]    # Removes units in brackets.
        names = [i.strip() for i in names]

        return pd.read_csv(path, sep='\t', skiprows=1, names=names)


def read_dataset(path: str) -> dict[str, pd.DataFrame]:
    """Reads a dataset into a dict of Pandas DataFrames.

    Returns:
        dict[str, pd.DataFrame]: A dict, whose keys are the names of the data
          files, in the format returned from data_path.
    """

    data_paths = {}

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".tsv"):
                data_paths[file.removesuffix(".tsv")] = read_data(os.path.join(root, file))

    return data_paths


def convert_raw_txt(date: str = None):
    """Converts raw table.txt output from mumax3 to tsv format."""

    raw_dir = dataset_dir(date, None)
    table_txt_path = os.path.join(raw_dir, "table.txt")

    data = read_data(table_txt_path)
    data.to_csv(data_path(date, None), sep='\t', index=False)

    # Removes original table.txt
    os.remove(table_txt_path)
