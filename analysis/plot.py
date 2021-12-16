"""Plots data."""

import os

import matplotlib.pyplot as plt
import pandas as pd

import readresults


def plot_xy(
    data: pd.DataFrame,
    x_var: str,
    y_vars: list[str],
    xlabel: str = None,
    ylabel: str = None,
    xlim: list[float, float] = None,
    ylim: list[float, float] = None,
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
        xlim (list[float, float]): x-axis limits, passed to
          `matplotlib.axes.Axes.set_xlim`.
        ylim (list[float, float]): y-axis limits, passed to
          `matplotlib.axes.Axes.set_ylim`.
        title (str): The title of the graph. If not given, defaults to
          "`ylabel` against `xlabel`".
        save_to (str): The full path to which the resultant graph shall be
          saved. Specify format using the extension; see matplotlib docs for a
          list of compatible formats. If not given, the graph will not be
          saved, and will be shown instead.
        show_plot (bool): Whether to show (`matplotlib.pyplot.show`) the graph.
    """

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    colors = plt.get_cmap('gist_rainbow')
    for i, var in enumerate(y_vars):
        ax.plot(data[x_var], data[var], label=var, c=colors(i / len(y_vars)))

    xlabel = xlabel if xlabel is not None else x_var
    ylabel = ylabel if ylabel is not None else ', '.join(y_vars)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title if title is not None else f"{ylabel} against {xlabel}")

    if len(y_vars) > 15:
        ax.legend(ncol=5, fontsize='xx-small')
    elif len(y_vars) > 1:
        ax.legend()

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    if save_to is not None:
        _, save_type = os.path.splitext(save_to)
        fig.savefig(save_to, format=save_type.strip('.'))

    if save_to is None or show_plot:
        plt.show()

    plt.close()


def plot_dataset_xy(
    data: dict[str, pd.DataFrame],
    x_var: str,
    y_vars: list[str],
    xlabel: str = None,
    ylabel: str = None,
    xlim: list[float, float] = None,
    ylim: list[float, float] = None,
    title: str = None,
    save_to_root: str = None,
    plot_format: str = "pdf"
):
    """Plots a dataset into multiple plots.

    Args:
        data (dict[str, pd.DataFrame]): A dictionary of data. See documentation
          at readresults.read_dataset.
        save_to_root (str): The root directory to which the resultant graphs
          shall be saved. Files will be named following the convention defined
          in readresults.dataset_dir and readresults.data_path.
        plot_format (str): The format of the resultant graph. See matplotlib
          docs for a list of compatible formats.
        (See plot_xy docs for other parameters.)
    """

    readresults.prep_dir(save_to_root)

    for key, val in data.items():

        save_to = save_to_root
        split_keys = key.split(", ")

        if len(split_keys) == 1:
            save_to = os.path.join(save_to, key + '.' + plot_format)

        elif len(split_keys) > 1:

            if not os.path.exists(os.path.join(save_to_root, *split_keys[:-1])):
                os.makedirs(os.path.join(save_to_root, *split_keys[:-1]))

            save_to = os.path.join(save_to, *split_keys[:-1], key + '.' + plot_format)

        plot_xy(val, x_var, y_vars, xlabel, ylabel, xlim, ylim, title, save_to)
