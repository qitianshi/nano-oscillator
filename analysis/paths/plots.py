"""Plots."""

import os

from analysis.paths import top


def plot_dir(date: str = None, subs: list[str] = None) -> str:
    """Returns the path of aggregate plots."""
    return os.path.join(top.result_dir(date), "plots", *(subs if subs is not None else []))


def spatial_dir(filename: str, component=str, date: str = None) -> str:
    """Returns the path of the spatial plots"""
    return os.path.join(
        plot_dir(date),
        "spatial_distribution",
        f"{filename}",
        f"{filename}_{component}.pdf"
    )


def linearspace_dir(filename: str, component=str, index=str, date: str = None) -> str:
    """Returns the path of the linearspace plots"""
    return os.path.join(
        plot_dir(date),
        "line_distribution",
        f"{filename}", f"{filename}_{component} against {index}.pdf"
    )