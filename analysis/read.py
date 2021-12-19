"""Finds and reads data and datasets from results."""

import os
from re import sub
from shutil import rmtree

import pandas as pd

from analysis import paths


def prep_dir(path: str):
    """Prepares the destination directory for output. Clears existing files and
    creates an empty directory.
    """

    if os.path.exists(path):
        rmtree(path)

    os.makedirs(path)


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

    raw_dir = paths.dataset_dir(date, None)

    try:

        table_txt_path = os.path.join(raw_dir, "table.txt")

        data = read_data(table_txt_path)
        data.to_csv(paths.data_path(date, None), sep='\t', index=False)

        # Removes original table.txt
        os.remove(table_txt_path)

    except FileNotFoundError:

        if os.path.isfile(os.path.join(raw_dir, "table.tsv")):
            print("Already converted to tsv.")
        else:
            print("Raw data not found.")
