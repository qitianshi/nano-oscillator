"""Parses table.txt output from mumax3."""


import os

def get_result(date: str = None):

    """Retrieves the path of table.txt from the requested directory.

    Args:
        date (str): The date of the simulation, matching the name of the
            subdirectory.
    """

    results_path = os.path.join(os.path.dirname(__file__), os.pardir, 'results')
    requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]

    return open(os.path.join(results_path, requested_result, 'raw.out/table.txt'),
                "r", encoding="utf-8")
