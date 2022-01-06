"""Top level of the results directory."""

import os
from pathlib import Path


def results_root() -> str:
    """Returns the root path of the results directory."""
    return os.path.join(Path(__file__).parents[2], 'results')


def latest_date() -> str:
    """Returns the date of the latest result."""
    return sorted(os.listdir(results_root()))[-1]


def result_dir(date: str = None) -> str:
    """Returns the path of the requested result.

    Args:
        date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm"). If
        not given, the most recent result is returned.

    Returns:
        str: The path of the result.
    """

    return os.path.join(results_root(), date if date is not None else latest_date())
