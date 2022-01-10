"""Plots."""

import os

from analysis.paths import top


def plot_dir(date: str = None, subs: list[str] = None) -> str:
    """Returns the path of aggregate plots."""

    if isinstance(subs, str):
        raise TypeError(
            f"'str' is an invalid argument type for `subs`. Perhaps you meant ['{subs}']?")

    return os.path.join(top.result_dir(date), "plots", *(subs if subs is not None else []))


def spatial_dir(filename: str, component=str, date: str = None) -> str:
    """Returns the path of the spatial plots"""
    return os.path.join(
        plot_dir(date),
        "spatial_distribution",
        f"{filename}",
        f"{filename}_{component}.pdf"
    )


def spatial_line(filename: str, component=str, index=str, date: str = None) -> str:
    """Returns the path of the spatial line plots."""
    return os.path.join(
        plot_dir(date),
        "spatial_line",
        f"{filename}", f"{filename}_{component} against {index}.pdf"
    )
