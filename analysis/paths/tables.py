"""Tables in the raw directory."""

import os

from analysis.paths import data


def ref_path(date: str = None):
    """Returns the path of the table-ref.txt file."""
    return os.path.join(data.raw(date), "table-ref.txt")


def txt_path(date: str = None):
    """Returns the path of the table.txt file."""
    return os.path.join(data.raw(date), "table.txt")
