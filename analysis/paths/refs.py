"""References."""

import os

from analysis.paths import top


def ref_path(date: str = None):
    """Returns the path of the ref file."""
    return os.path.join(top.result_dir(date), "raw-ref.txt")


def raw_zip_path(date: str = None):
    """Returns the path of the zipped raw date file."""
    return os.path.join(top.result_dir(date), "raw.zip")
