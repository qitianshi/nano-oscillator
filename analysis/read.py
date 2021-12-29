"""Finds and reads data and datasets from results."""

import os
from dataclasses import dataclass
from re import sub
from shutil import rmtree

import pandas as pd
import numpy as np

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


def read_dataset(path: str) -> dict[str, pd.DataFrame]:
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

        table_txt_path = os.path.join(paths.dataset_dir(date), "table.txt")

        data = read_data(table_txt_path)
        data.to_csv(paths.data_path(date, None), sep='\t', index=False)

        # Removes original table.txt
        os.remove(table_txt_path)

    except FileNotFoundError:

        if os.path.isfile(paths.data_path(date)):
            print("Already converted to tsv.")
        else:
            print("Raw data not found.")


def convert_npy(date: str = None):
    """Converts all .npy files to .tsv files."""

    date = date if date is not None else paths.latest_date()
    mag_vars = ["mz", "my", "mx"]

    for file in os.listdir(paths.raw_geom_dir()):

        fields = {}

        if file.endswith(".npy"):

            #TODO raise FileNotFoundError

            filename = os.path.splitext(file)[0]
            if not os.path.isdir(paths.geom_dir(filename, date)):
                os.mkdir(paths.geom_dir(filename, date))

            fields[filename] = np.load(os.path.join(paths.raw_geom_dir(), file))

            for component in range(len(fields[filename])):
                mag_var = mag_vars[component]
                for slices in range(len(fields[filename][component])):
                    pd.DataFrame(fields[filename][component][slices]) \
                        .to_csv(paths.spatial_path(slices, filename, mag_var, date), sep="\t", index=False)


def get_header(date: str = None) -> str:

    with open(paths.geom_ovf_path(0, date), 'r', encoding='utf-8') as file:

        line = file.readline()
        while not line.startswith("# Segment count"):
            line = file.readline()

        seg_count = int(line.split(":")[-1])

        if seg_count > 1:
            raise NotImplementedError("Segment count is more than 1 🤡")

        ovf_headers = []
        line = file.readline()
        while not line.startswith("# End: Header"):
            line = file.readline()
            ovf_headers.append(line.strip("#").strip())

        ovf_headers = ovf_headers[
            (ovf_headers.index("Begin: Header") + 1)
            :(ovf_headers.index("End: Header"))
        ]

    return '\n'.join(ovf_headers)