"""Top level of the results directory."""

import os


def latest_date() -> str:
    """Returns the date of the latest result."""
    return sorted(
        os.listdir(os.path.join(os.path.dirname(__file__), os.pardir, 'results')))[-1]


def result_dir(date: str = None) -> str:
    """Returns the path of the requested result.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm"). If
        not given, the most recent result is returned.

    Returns:
        str: The path of the result.
    """

    results_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'results')
    requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]

    return os.path.join(results_path, requested_result)
