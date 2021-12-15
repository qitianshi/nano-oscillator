"""Plots data."""

import matplotlib.pyplot as plt
import pandas as pd


def plot_xy(
    data: pd.DataFrame,
    x_var: str,
    y_vars: list[str],
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    save_to: str = None,
    show_plot: bool = False
):
    """Plots a number of dependent variables against an independent variable.

    Args:
        data (pandas.DataFrame): The data to be plotted.
        x_var (str): The name of the independent variable (on the x-axis).
          Should correspond to a variable in the data file.
        y-vars (list[str]): The names of the dependent variables (on the
          y-axis). Should correspond to a variable in the data file.
        xlabel (str): The label on the x-axis. If not given, defaults to
          `x-var`.
        ylabel (str): The label on the y-axis. If not given, defaults to comma-
          separated list of `y-vars`.
        title (str): The title of the graph. If not given, defaults to
          "`ylabel` against `xlabel`".
        save_to (str): The full path to which the resultant graph shall be
          saved. The default format is pdf; provide a different extension to
          save as a different format. See matplotlib documentation for a list
          of compatible formats. If not given, the graph will not be saved, and
          will be shown instead.
        show_plot (bool): Whether to show (`matplotlib.pyplot.show`) the graph.
    """

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    for var in y_vars:
        ax.plot(data[x_var], data[var], label=var)

    xlabel = xlabel if xlabel is not None else x_var
    ylabel = ylabel if ylabel is not None else ', '.join(y_vars)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title if title is not None else f"{ylabel} against {xlabel}")
    if len(y_vars) > 1:
        ax.legend()

    if save_to is not None:
        fig.savefig(save_to, format='pdf')

    if save_to is None or show_plot:
        plt.show()


def plot_dataset_xy(
    data: dict[str, pd.DataFrame],
    x_var: str,
    y_vars: list[str],
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    save_to: str = None,
    show_plot: bool = False
):
    """Plots a dataset into multiple plots.

    Args:
        data (dict[str, pd.DataFrame]): A dictionary of data. See documentation
          at readresults.read_dataset.
    """
