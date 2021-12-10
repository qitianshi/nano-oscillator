"""Reads and writes results from the results directory."""

import os
from re import sub
from shutil import rmtree
import pandas as pd

def prep_dir(path):
    """Prepares the destination directory for output files."""

    # If a previous output was already generated, it is deleted so that the new
    # output can overwrite it.
    if os.path.exists(path):
        rmtree(path)

    os.mkdir(path)

def find_result_dir(date: str = None) -> str:
    """Returns the path of the results folder from the requested simulation.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm"),
          which matches the name of the subdirectory. If not given, the
          latest result is returned.

    Returns:
        str: The path of the results folder.
    """

    results_path = os.path.join(os.path.dirname(__file__), os.pardir, 'results')
    requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]

    return os.path.join(results_path, requested_result)

def find_raw(date: str = None) -> str:
    """Returns the path of the raw data for the requested simulation."""

    try:
        return os.path.join(find_result_dir(date), 'raw.out/table.tsv')

    # If table.tsv is not found, table.txt has likely not been converted yet.
    # Otherwise, convert_raw will raise FileNotFoundError as expected.
    except FileNotFoundError:
        convert_raw(date)
        return os.path.join(find_result_dir(date), 'raw.out/table.tsv')

def find_phi(phi: int, date: str = None) -> str:
    """Returns the path of the data for the requested value of phi."""

    return os.path.join(find_result_dir(date), 'split/by_phi/' + str(phi) + '.csv')

def read_table(path: str = find_raw()) -> pd.DataFrame:
    """Reads the raw table.txt output from mumax3 into a DataFrame."""

    with open(path, 'r', encoding="utf-8") as file:

        names = file.readline().strip('#').split('\t')
        names = [sub(r"[\(].*?[\)]", "", i) for i in names]    # Removes units in brackets.
        names = [i.strip() for i in names]

        return pd.read_csv(path, sep='\t', skiprows=1, names=names)

def convert_raw(date: str = None):
    """Converts raw table.txt output from mumax3 to tsv format."""

    table_dir = find_raw(date)
    result_dir = find_result_dir(date)

    results = read_table(table_dir)
    results.to_csv(os.path.join(result_dir, "raw.out", "table.tsv"), sep='\t', index=False)

    # Removes original table.txt
    os.remove(table_dir)
