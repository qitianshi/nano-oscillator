"""Plots data."""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis import read


def plot_xy(
    attr_data: list[read.AttributedData],
    xlabel: str = None,
    ylabel: str = None,
    xlim: list[float, float] = None,
    ylim: list[float, float] = None,
    xstep: float = None,
    title: str = None,
    save_to: str = None,
    show_plot: bool = False
):
    """Plots a number of dependent variables against an independent variable.

    Args:
        attr_data (list[AttributedData]): A list of data to plot. The item at
          index 0 will be treated as the primary data.
        xlabel (str): The label on the x-axis. If not given, defaults to
          `x-var` of the primary data.
        ylabel (str): The label on the y-axis. If not given, defaults to comma-
          separated list of `y-vars` of the primary data.
        xlim (list[float, float]): x-axis limits, passed to
          `matplotlib.axes.Axes.set_xlim`.
        ylim (list[float, float]): y-axis limits, passed to
          `matplotlib.axes.Axes.set_ylim`.
        xsteps (float): Tick steps for the x-axis.
        title (str): The title of the graph. If not given, defaults to
          "`ylabel` against `xlabel`" of the primary data.
        save_to (str): The full path to which the resultant graph shall be
          saved. Specify format using the extension; see matplotlib docs for a
          list of compatible formats. If not given, the graph will not be
          saved, and will be shown instead.
        show_plot (bool): Whether to show (`matplotlib.pyplot.show`) the graph.
    """

    attr_data = attr_data if isinstance(attr_data, list) else [attr_data]

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    colors = plt.get_cmap('gist_rainbow')
    for datum in attr_data:
        for i, var in enumerate(datum.y_vars):
            ax.plot(
                datum.data[datum.x_var],
                datum.data[var],
                datum.fmt,
                label=var,
                c=colors(i / len(datum.y_vars))
            )

    xlabel = xlabel if xlabel is not None else attr_data[0].x_var
    ylabel = ylabel if ylabel is not None else ', '.join(attr_data[0].y_vars)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title if title is not None else f"{ylabel} against {xlabel}")

    if len(attr_data[0].y_vars) > 15:
        ax.legend(ncol=5, fontsize='xx-small')
    elif len(attr_data[0].y_vars) > 1:
        ax.legend()

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    if xstep is not None:
        x_vals = attr_data[0].data[attr_data[0].x_var]
        ax.set_xticks(np.arange(min(x_vals), max(x_vals) + xstep, xstep))

    if save_to is not None:

        read.prep_dir(os.path.split(save_to)[0], clear=False)

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
    xstep: float = None,
    title: str = None,
    save_to_root: str = None,
    plot_format: str = "pdf"
):
    """Plots a dataset into multiple plots.

    Args:
        data (dict[str, pd.DataFrame]): A dictionary of data. See documentation
          at read.read_dataset.
        save_to_root (str): The root directory to which the resultant graphs
          shall be saved. Files will be named following the convention defined
          in read.dataset_dir and read.data_path.
        plot_format (str): The format of the resultant graph. See matplotlib
          docs for a list of compatible formats.
        (See plot_xy docs for other parameters.)
    """

    read.prep_dir(save_to_root)

    for key, val in data.items():

        save_to = save_to_root
        split_keys = key.split(", ")

        if len(split_keys) == 1:
            save_to = os.path.join(save_to, key + '.' + plot_format)

        elif len(split_keys) > 1:

            read.prep_dir(os.path.join(save_to_root, *split_keys[:-1]), clear=False)

            save_to = os.path.join(save_to, *split_keys[:-1], key + '.' + plot_format)

        plot_xy(read.AttributedData(val, x_var, y_vars),
            xlabel, ylabel, xlim, ylim, xstep, title, save_to)


def plot_function(
    data: pd.DataFrame,
    func,
    params: list[str],
    domain: list[float, float],
    rows: list = None,
    xlabel: str = None,
    ylabel: str = None,
    xlim: list[float, float] = None,
    ylim: list[float, float] = None,
    xstep: float = None,
    title: str = None,
    save_to: str = None,
    show_plot: bool = False
):
    """Plots a function over a given domain.

    Args:
        data (pandas.DataFrame): A DataFrame in which each row contains
          parameters for one line. The first column must be the independent
          variable, which will be plotted on the horizontal axis.
        func (callable): The mathematical function to plot. The first parameter
          must be the independent variable.
        params (list[str]): Ordered list of column names in `data` from which
          parameters for `func` will be read.
        domain (list[float, float]): The domain over which to plot. A length-2
          array, where the zeroth value is the lower bound and the first value
          is the upper bound.
        rows (list): A list of values. If set, only rows in `data` whose first
          value appears in `rows` will be plotted; otherwise all rows will be
          plotted.
        (See plot_xy docs for other parameters.)
    """

    steps = 100
    x_vals = np.linspace(*domain, steps)
    ind_var = data.columns[0]           # Independent variable

    result = np.zeros(shape=(steps, 0))
    result = np.append(result, np.reshape(x_vals, newshape=(-1, 1)), axis=1)

    for _, row in (data.iterrows() if rows is None else data.loc[data[ind_var].isin(rows)]):
        y_vals = func(x_vals, *[row[i] for i in params])
        result = np.append(result, np.reshape(y_vals, newshape=(-1, 1)), axis=1)

    df_result = pd.DataFrame(result, columns=("x_vals", *(data[ind_var])))

    plot_xy(read.AttributedData(df_result, "x_vals", data[ind_var]),
        xlabel, ylabel, xlim, ylim, xstep, title, save_to, show_plot)
