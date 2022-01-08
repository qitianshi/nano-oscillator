"""Spatial data."""

import os

from analysis.paths import top, data


def root(date: str = None) -> str:
    """Returns the path of the directory with spatial data"""
    return os.path.join(top.result_dir(date), "spatial_data")


def geom_dir(filename: str, date: str = None) -> str:
    """Returns the path of the geom directory under spatial_data"""
    return os.path.join(root(date), f"{filename}")


def header_path(date: str = None) -> str:
    """Returns the path of the YAML file"""
    return os.path.join(data.raw(date), "headers.json")


def spatial_path(filename: str, mag_var: str, slices: int, date: str = None):
    """Returns the path of the spatial data .tsv files"""
    slices = str(slices) if slices is not None else str(0)
    return os.path.join(
        geom_dir(filename, date),
        f"{filename}_{mag_var}_slice_{slices}.tsv"
    )


def geom_ovf_path(filename: int, date: str = None) -> str:
    """Returns the path of the ovf file"""
    return os.path.join(data.raw(date), f"{filename}.ovf")
