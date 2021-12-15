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
          of the raw data is returned.

    Returns:
        str: The path of the requested dataset.
    """

    if vals is None:
        return os.path.join(result_dir(date), "raw.out")
    else:
        return os.path.join(
            result_dir(date),
            "split",
            ", ".join(vals.keys()),
            *list(vals.values())[:-1]
        )


def data_path(date: str = None, vals: dict[str, str] = None) -> str:
    """Returns the path of the data split by the requested variables and
    values.
    """

    if vals is None:
        return os.path.join(dataset_dir(date, vals), "table.tsv")
    else:
        return os.path.join(dataset_dir(date, vals), ", ".join(vals.values()) + ".tsv")

def amplitude_path(date : str = None, phi : str = None):
    amplitude_dir = os.path.join(result_dir(date), "amplitudes")
    return os.path.join(amplitude_dir, f"{phi}deg.tsv")

def read_data(path: str) -> pd.DataFrame:
    """Reads a data file into a Pandas DataFrame."""

    with open(path, 'r', encoding="utf-8") as file:

        names = file.readline().strip('#').split('\t')
        names = [sub(r"[\(].*?[\)]", "", i) for i in names]    # Removes units in brackets.
        names = [i.strip() for i in names]

        return pd.read_csv(path, sep='\t', skiprows=1, names=names)


def convert_raw_txt(date: str = None):
    """Converts raw table.txt output from mumax3 to tsv format."""

    raw_dir = dataset_dir(date, None)
    table_txt_path = os.path.join(raw_dir, "table.txt")

    data = read_data(table_txt_path)
    data.to_csv(data_path(date, None), sep='\t', index=False)

    # Removes original table.txt
    os.remove(table_txt_path)
