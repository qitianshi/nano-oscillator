"""Finds and reads data and datasets from results."""

import os
from dataclasses import dataclass
from re import sub
from shutil import rmtree

import pandas as pd

from analysis import paths


@dataclass
class AttributedData:
    """A set of data with attributes to be plotted.

    Plotting properties (for `analysis.plot` methods) are also included, but
    not required.

    Attributes:
        data (pandas.DataFrame): The data.
        title (str): The title of the data.
        x_var (str): The name of the independent variable (on the x-axis).
          Should correspond to a variable in the data file.
        y-vars (list[str]): The names of the dependent variables (on the
          y-axis). Should correspond to a variable in the data file.
        fmt (str): The format string for the plot. See matplotlib docs for
          syntax. Defaults to solid line of default color.
    """

    # Data properties
    data: pd.DataFrame
    title: str = None

    # Plot properties
    x_var: str = None
    y_vars: list[str] = None
    fmt: str = '-'


def prep_dir(path: str, clear: str = True):
    """Prepares the destination directory for output. Optionally clears
    existing files and creates an empty directory.
    """

    if clear and os.path.exists(path):
        rmtree(path)

    os.makedirs(path, exist_ok=True)


def read_data(path: str) -> pd.DataFrame:
    """Reads a data file into a Pandas DataFrame."""

    with open(path, 'r', encoding="utf-8") as file:

        names = file.readline().strip('#').split('\t')
        names = [sub(r"[\(].*?[\)]", "", i) for i in names]    # Removes units in brackets.
        names = [i.strip() for i in names]

        return pd.read_csv(path, sep='\t', skiprows=1, names=names)


def read_dataset(path: str) -> list[pd.DataFrame]:
    """Reads a dataset into a list of `AttributedData`."""

    dataset_data = []

    for root, _, files in os.walk(path):
        for file in files:
            name, ext = os.path.splitext(file)
            #TODO: raise FileNotFound error
            if ext.endswith("tsv"):
                dataset_data.append(
                    AttributedData(
                        data=read_data(os.path.join(root, file)),
                        title=name
                    )
                )

    return dataset_data


def convert_raw_txt(date: str = None):
    """Converts raw table.txt output from mumax3 to tsv format."""

    try:

        table_txt_path = os.path.join(paths.Data.dataset_dir(date), "table.txt")

        data = read_data(table_txt_path)
        data.to_csv(paths.Data.data_path(date, None), sep='\t', index=False)

        # Removes original table.txt
        os.remove(table_txt_path)

    except FileNotFoundError:

        if os.path.isfile(paths.Data.data_path(date)):
            print("Already converted to tsv.")
        else:
            print("Raw data not found.")
