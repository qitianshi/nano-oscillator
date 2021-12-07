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




