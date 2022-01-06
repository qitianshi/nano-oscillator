"""Calculated values."""

import os

from analysis.paths import top


def root(date: str = None):
    """Returns the path of the calculated_values dataset."""
    return os.path.join(top.result_dir(date), "calculated_values")


def amp_path(mag_var: str, date: str = None) -> str:
    """Returns the path of the amplitude data."""
    return os.path.join(root(date), f"amp_{mag_var}.tsv")


def maxamp_path(date: str = None) -> str:
    """Returns the path of the MaxAmp data."""
    return os.path.join(root(date), "MaxAmp.tsv")


def fitted_amp_path(mag_var: str, date: str = None) -> str:
    """Returns the path of the curve-fitted amplitude data."""
    return os.path.join(root(date), f"fitted amp_{mag_var}.tsv")
