"""Plots data."""

import os
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis import read, paths, write


def plot_xy(
    attr_data: list[read.AttributedData],
    xlabel: str = None,
    ylabel: str = None,
    xlim: list[float, float] = None,
    ylim: list[float, float] = None,
    xstep: float = None,
    cmap_name: str = "gist_rainbow",
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
        cmap_name (str): the name of the colomap_instance
        title (str): The title of the graph. If not given, defaults to
          "`ylabel` against `xlabel`" of the primary data.
        save_to (str): The full path to which the resultant graph shall be
          saved. Specify format using the extension; see matplotlib docs for a
          list of compatible formats. If not given, the graph will not be
          saved, and will be shown instead.
        show_plot (bool): Whether to show (`matplotlib.pyplot.show`) the graph.
    """

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    colors = plt.get_cmap(cmap_name)
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

        write.prep_dir(os.path.split(save_to)[0], clear=False)

        _, save_type = os.path.splitext(save_to)
        fig.savefig(save_to, format=save_type.strip('.'))

    if save_to is None or show_plot:
        plt.show()

    plt.close()


def plot_dataset_xy(
    attr_data: list[read.AttributedData],
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
        data (list[analysis.read.AttributedData]): A list of data generated by
          `analysis.read.read_dataset`. See `read_dataset` docs for details.
        save_to_root (str): The root directory to which the resultant graphs
          shall be saved. Files will be named following the convention defined
          in `paths`.
        plot_format (str): The format of the resultant graph. See matplotlib
          docs for a list of compatible formats.
        (See plot_xy docs for other parameters.)
    """

    write.prep_dir(save_to_root)

    for datum in attr_data:

        save_to = save_to_root
        split_keys = datum.title.split(", ")

        if len(split_keys) == 1:
            save_to = os.path.join(save_to, datum.title + '.' + plot_format)

        elif len(split_keys) > 1:
            write.prep_dir(os.path.join(save_to_root, *split_keys[:-1]), clear=False)
            save_to = os.path.join(save_to, *split_keys[:-1], datum.title + '.' + plot_format)

        plot_xy(read.AttributedData(datum.data, x_var=x_var, y_vars=y_vars),
            xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim, xstep=xstep, title=title,
            save_to=save_to)


def plot_function(
    data: pd.DataFrame,
    func,
    params: list[str],
    domain: list[float, float],
    overlay: list[read.AttributedData] = None,
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
        overlay (list[read.AttributedData]): Other plots which will be
          overlayed on the functions. Useful for plotting data points with
          curve fits.
        (See plot_xy docs for other parameters.)
    """

    if isinstance(params, str):
        raise TypeError(
            f"'str' is an invalid argument type for `params`. Perhaps you meant ['{params}']?")

    steps = 100
    x_vals = np.linspace(*domain, steps)
    ind_var = data.columns[0]           # Independent variable

    result = np.zeros(shape=(steps, 0))
    result = np.append(result, np.reshape(x_vals, newshape=(-1, 1)), axis=1)

    for _, row in data.iterrows():
        y_vals = func(x_vals, *[row[i] for i in params])
        result = np.append(result, np.reshape(y_vals, newshape=(-1, 1)), axis=1)

    df_result = pd.DataFrame(
        result, columns=("x_vals", *data[ind_var]))

    plot_xy(
        [
            read.AttributedData(
                data=df_result,
                x_var="x_vals",
                y_vars=data[ind_var]
            ),
            *(overlay if overlay is not None else [])
        ],
        xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim, xstep=xstep, title=title,
        save_to=save_to, show_plot=show_plot
    )


def plot_spatial_line(
    date: str,
    x_index: int = None,
    y_index: int = None,
    component: str = "z",
    filename: str = None,
    save_to: str = None,
    show_plot: bool = False,
    slices: int = None
):
    """Plots the graphs of spatial data against the x or y index of the cells.

    Args:
        xindex: the column index of data (starts at 0), equivalent to drawing a line of x=... on
            the table of values
        yindex: the row index of data (starts at 0), equivalent to drawing a line of y=... on
            the table of values
    """

    #TODO: Replace `filename` with `save_to` of full path with extension.

    # Creates a Pandas dataframe with the B_ext data as a column
    if y_index is None:
        # Vertical line
        line_index_name = "y"
        line_index = x_index
        plot_data = read.read_data(
                paths.spatial.spatial_path(filename, component, slices, date)
        ).iloc[:, x_index].to_frame(str(x_index))

    elif x_index is None:
        # Horizontal line
        line_index_name = "x"
        line_index = y_index
        plot_data = read.read_data(
                paths.spatial.spatial_path(filename, component, slices, date)
        ).iloc[y_index, :].to_frame(str(y_index))

    else:
        raise ValueError("`xindex` and `yindex` cannot both be `None`.")

    # Create the list of x coordinates and puts it in the Pandas dataframe
    with open(paths.spatial.header_path(date), 'r', encoding='utf-8') as file:
        headers = json.load(file)

        xvar = np.arange(
            float(headers[f"{line_index_name}min"]),
            float(headers[f"{line_index_name}max"]),
            float(headers[f"{line_index_name}stepsize"])
        )

        xlabel = f"{line_index_name} (" + headers["meshunit"] + ")"
        ylabel = f"{filename} (T)"
        #TODO: make the y axis units an option

        plot_data.insert(0, line_index_name, xvar)

    plot_xy(
        [read.AttributedData(plot_data, x_var=line_index_name, y_vars=[str(line_index)])],
        xlabel,
        ylabel,
        xstep=0.2e-06,
        save_to=save_to,
        show_plot=show_plot
    )


def plot_image(
    data: pd.DataFrame,
    xlabel: str,
    ylabel: str,
    title: str,
    save_to: str,
    xindexes: list[int] = None, #index starts at 0
    yindexes: list[int] = None, #index starts at 0
    xstep: float = 100e-09,
    ystep: float = 100e-09,
    cmap_name: str = "winter",
    show_plot: bool = False,
    date: str = None,
):
    """Plots an image from a given dataset

    Args:
        data (pandas.DataFrame): 2D scalar data, usually taking the form of a
          2D array.
        (See plot_xy docs for other paramters.)
    """
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    if xindexes is None:
        xindexes = [0, 511]
    if yindexes is None:
        yindexes = [0, 511]

    with open(paths.spatial.header_path(date), 'r', encoding='utf-8') as file:
        headers = json.load(file)

        xaxis_max = (float(headers["xmax"]) - float(headers["xmin"])) / 2
        all_cells_x = np.arange(-abs(xaxis_max), xaxis_max, float(headers["xstepsize"]))
        xticks = np.arange(
            all_cells_x[xindexes[0]] + xstep - all_cells_x[xindexes[0]] % xstep,
            all_cells_x[xindexes[1]] + xstep - all_cells_x[xindexes[1]] % xstep,
            xstep
        )
        ax.set_xticks(xticks, xticks)

        yaxis_max = (float(headers["ymax"]) - float(headers["ymin"])) / 2
        all_cells_y = np.arange(-abs(yaxis_max), yaxis_max, float(headers["ystepsize"]))
        yticks = np.arange(
            all_cells_y[yindexes[0]] + ystep - all_cells_y[yindexes[0]] % ystep,
            all_cells_y[yindexes[1]] + ystep - all_cells_y[yindexes[1]] % ystep,
            ystep
        )
        ax.set_yticks(yticks, yticks)

    data = data.iloc[yindexes[0] : yindexes[1] + 1, xindexes[0] : xindexes[1] + 1]

    plot = plt.imshow(data, cmap=cmap_name,
        extent=[xticks.min(), xticks.max(), yticks.min(), yticks.max()]
    )
    plt.colorbar(plot).set_label(title)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title if title is not None else f"{ylabel} against {xlabel}")

    if save_to is not None:

        write.prep_dir(os.path.split(save_to)[0], clear=False)

        _, save_type = os.path.splitext(save_to)
        fig.savefig(save_to, format=save_type.strip('.'))

    if save_to is None or show_plot:
        plt.show()

    plt.close()
