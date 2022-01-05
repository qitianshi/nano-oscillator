"""Provides paths to datasets and directories."""

import os


class Top:
    """Top level of the results directory."""

    @staticmethod
    def latest_date() -> str:
        """Returns the date of the latest result."""
        return sorted(
            os.listdir(os.path.join(os.path.dirname(__file__), os.pardir, 'results')))[-1]

    @staticmethod
    def result_dir(date: str = None) -> str:
        """Returns the path of the requested result.

        Args:
            date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm"). If
            not given, the most recent result is returned.

        Returns:
            str: The path of the result.
        """

        results_path = os.path.join(os.path.dirname(__file__), os.pardir, 'results')
        requested_result = date if date is not None else sorted(os.listdir(results_path))[-1]

        return os.path.join(results_path, requested_result)


class Refs:
    """References."""

    @staticmethod
    def ref_path(date: str = None):
        """Returns the path of the ref file."""
        return os.path.join(Top.result_dir(date), "raw-ref.txt")

    @staticmethod
    def raw_zip_path(date: str = None):
        """Returns the path of the zipped raw date file."""
        return os.path.join(Top.result_dir(date), "raw.zip")


class Tables:
    """Tables in the raw directory."""

    @staticmethod
    def ref_path(date: str = None):
        """Returns the path of the table-ref.txt file."""
        return os.path.join(Data.dataset_dir(date, vals=None), "table-ref.txt")

    @staticmethod
    def txt_path(date: str = None):
        """Returns the path of the table.txt file."""
        return os.path.join(Data.dataset_dir(date, vals=None), "table.txt")


class Data:
    """Data and datasets."""

    @staticmethod
    def dataset_dir(date: str = None, vals: dict[str, str] = None) -> tuple[str, tuple[str]]:
        """Returns the path of the dataset split by the requested variables.

        Args:
            date (str): The date and time of the simulation ("YYYY-MM-DD_hhmm").
            If not given, the latest result is searched.
            vals (dict[str, str]): An ordered dict of variable names and their
            values, in order of how the data was split. If not given, the path
            of the unsplit data is returned. The path that is returned stops at
            the first item whose value is `None`.

        Returns:
            str: The path of the requested dataset. The path stops at the first
            item in `vals` whose value is `None`.
        """

        if vals is None:
            return os.path.join(Top.result_dir(date), "raw")
        else:
            return os.path.join(
                Top.result_dir(date),
                "split",
                ", ".join(vals.keys()),
                *[i for i in list(vals.values())[:-1] if i is not None]
            )

    @staticmethod
    def data_path(date: str = None, vals: dict[str, str] = None) -> str:
        """Returns the path of the data split by the requested variables and
        values.
        """

        if vals is None:
            return os.path.join(Data.dataset_dir(date, vals), "table.tsv")
        else:
            return os.path.join(Data.dataset_dir(date, vals), ", ".join(vals.values()) + ".tsv")


class Plots:
    """Plots."""

    @staticmethod
    def plot_dir(date: str = None, subs: list[str] = None) -> str:
        """Returns the path of aggregate plots."""
        return os.path.join(Top.result_dir(date), "plots", *(subs if subs is not None else []))

    @staticmethod
    def spatial_dir(filename: str, component=str, date: str = None) -> str:
        """Returns the path of the spatial plots"""
        return os.path.join(
            Plots.plot_dir(date),
            "spatial_distribution",
            f"{filename}",
            f"{filename}_{component}.pdf"
        )

    @staticmethod
    def linearspace_dir(filename: str, component=str, index=str, date: str = None) -> str:
        """Returns the path of the linearspace plots"""
        return os.path.join(
            Plots.plot_dir(date),
            "line_distribution",
            f"{filename}", f"{filename}_{component} against {index}.pdf"
        )

class Spatial:
    """Spatial data."""

    @staticmethod
    def root(date: str = None) -> str:
        """Returns the path of the directory with spatial data"""
        return os.path.join(Top.result_dir(date), "spatial_data")

    @staticmethod
    def geom_dir(filename: str, date: str = None) -> str:
        """Returns the path of the geom directory under spatial_data"""
        return os.path.join(Spatial.root(date), f"{filename}")

    @staticmethod
    def header_path(date: str = None) -> str:
        """Returns the path of the YAML file"""
        return os.path.join(Spatial.root(date), "headers.json")

    @staticmethod
    def spatial_path(filename: str, mag_var: str, slices: int, date: str = None):
        """Returns the path of the spatial data .tsv files"""
        slices = str(slices) if slices is not None else str(0)
        return os.path.join(
            Spatial.geom_dir(filename, date),
            f"{filename}_{mag_var}_slice_{slices}.tsv"
        )

    @staticmethod
    def geom_ovf_path(filename: int, date: str = None) -> str:
        """Returns the path of the ovf file"""
        return os.path.join(Data.dataset_dir(date), f"{filename}.ovf")


class CalcVals:
    """Calculated values."""

    @staticmethod
    def root(date: str = None):
        """Returns the path of the calculated_values dataset."""
        return os.path.join(Top.result_dir(date), "calculated_values")

    @staticmethod
    def amp_path(mag_var: str, date: str = None) -> str:
        """Returns the path of the amplitude data."""
        return os.path.join(CalcVals.root(date), f"amp_{mag_var}.tsv")

    @staticmethod
    def maxamp_path(date: str = None) -> str:
        """Returns the path of the MaxAmp data."""
        return os.path.join(CalcVals.root(date), "MaxAmp.tsv")

    @staticmethod
    def fitted_amp_path(mag_var: str, date: str = None) -> str:
        """Returns the path of the curve-fitted amplitude data."""
        return os.path.join(CalcVals.root(date), f"fitted amp_{mag_var}.tsv")
