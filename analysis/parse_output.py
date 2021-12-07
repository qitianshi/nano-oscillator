"""Parses table.txt output from mumax3."""

import pandas as pd
import os

def get_folder_dir(date: str = None):

    """Retrieves the path of table.txt from the requested directory.

    Args:
        date (str): The date of the simulation, matching the name of the
            subdirectory.
    """

    results_path = os.path.join(os.path.dirname(__file__), os.pardir, 'results')
    requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]


    return os.path.join(results_path, requested_result)

def get_result():
    folder_dir = get_folder_dir()
    return os.path.join(folder_dir, 'raw.out/table.txt')

def split_data_angle():
    filepath = get_result()
    folder_dir = get_folder_dir()
    start_angle = 0
    end_angle = 360
    angle_step = 30

    data = pd.read_csv(filepath, sep="\t")

    for i in range(start_angle, end_angle + 30, angle_step):

        split_name = str(i) + '.csv'
        split_path = os.path.join(folder_dir,'split/by_angle/', split_name)

        filtered = data[data["phi (degree)"] == i]
        filtered.to_csv(split_path, sep=",")


split_data_angle()


