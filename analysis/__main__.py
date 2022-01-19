"""Runs all data analyses, including splitting, calculations, and plotting."""

import argparse
import os
from enum import Enum, auto
from sys import exit
from time import time

import analysis as anl


#region Internals

class Commands(Enum):
    """CLI commands."""

    CROSSPLOT = auto()
    PREPARSE = auto()
    RESONANCE = auto()
    SPATIAL = auto()
    SPATIALLINE = auto()


def __resolve_dates(values: list[str]) -> list[str]:

    # Checks that simulation date exists.
    for val in values:
        if val != "..." and (not os.path.exists(anl.paths.top.result_dir(val))):
            exit(f"Error: no result was found for '{val}'.")

    if "..." in values:

        start_date, end_date = values[0], values[2]
        all_dates = sorted(os.listdir(anl.paths.top.results_root()))

        return all_dates[all_dates.index(start_date) : all_dates.index(end_date) + 1]

    else:
        return values


def __timed_run(anl_funcs: list):
    """Runs all analyses."""

    t_init = time()

    if not CLI_TEST:

        for func in anl_funcs:
            t_start = time()
            func()
            print(f"  Done in {time() - t_start:.1f}s.")

        print(f"Finished {len(anl_funcs)} {'analysis' if len(anl_funcs) == 1 else 'analyses'} in",
              f"{time() - t_init:.1f}s.\n")

    else:
        print(
            "CLI test mode is active.",
            f"Analysis functions: {[func.__name__ for func in anl_funcs]}\n"
        )

#endregion

#region Command line

def __validate_date(value: list[str], arg_obj):

    if "..." in value and (value.count("...") > 1 or value.index("...") != 1 or len(value) != 3):
        raise argparse.ArgumentError(
            arg_obj, "Ranged dates must be in the format 'DATE_1 ... DATE_2'")


def __validate_arg_list(value: list, arg_obj, accept_vals: list):

    if any(i not in accept_vals for i in value):

        rejected_mag_vars = list(set(value) - set(accept_vals))

        raise argparse.ArgumentError(
            arg_obj,
            f"{', '.join(rejected_mag_vars)}"
            + f" {'does not' if len(rejected_mag_vars) == 1 else 'do not'}"
            + f" match valid values: {', '.join(accept_vals)}"
        )


def __validate_arg_option(value, arg_obj, accept_vals: str):

    if value not in accept_vals:
        raise argparse.ArgumentError(
            arg_obj, f"'{value}' does not match valid_values: {', '.join(accept_vals)}")


def __parse_cli_input() -> tuple:
    """Parses and validates the command line interface.

    Returns:
        list: A list of length 3. The 0th item is the subcommand. The 1st item
          is a tuple of arguments for the subcommand. The 2nd item is a tuple
          of top-level arguments.
    """

    parser = argparse.ArgumentParser(prog="analysis", description="Runs analyses of mumax3 data.")
    subparser = parser.add_subparsers(dest="command", required=True)

    comm_crossplot = subparser.add_parser(
        "crossplot",
        description="Plots quantities across multiple results."
    )

    comm_preparse = subparser.add_parser(
        "preparse",
        description="Readies mumax3 output before being uploaded."
    )

    comm_resonance = subparser.add_parser(
        "resonance",
        description=(
            "Analyses for characterizing resonance characteristics of the nano-constriction.")
    )

    comm_spatial = subparser.add_parser(
        "spatial",
        description="Analyses of spatial magnetization data."
    )

    comm_spatialline = subparser.add_parser(
        "spatialline",
        description="Plots a line of values in spatial data."
    )

    # Top-level args

    parser.add_argument(
        "--cli-test",
        dest="cli_test",
        action="store_true",
        help="activates CLI test mode; analysis functions will be printed but not run."
    )

    # preparse args

    argobj_preparse_dates = comm_preparse.add_argument(
        "date",
        type=str,
        nargs='*',
        default=[anl.paths.top.latest_date()],
        help="the list of dates to analyze (YYYY-MM-DD_hhmm), defaults to latest"
    )

    argobj_result_type = comm_preparse.add_argument(
        "--type",
        dest="result_type",
        type=str,
        required=True,
        help="the type of simulaton to preparse, e.g. resonance, spatial"
    )

    # resonance args

    argobj_resonance_dates = comm_resonance.add_argument(
        "date",
        type=str,
        nargs='*',
        default=[anl.paths.top.latest_date()],
        help="the list of dates to analyze (YYYY-MM-DD_hhmm), defaults to latest"
    )

    argobj_mag_vars = comm_resonance.add_argument(
        "--mag-vars",
        dest="mag_vars",
        type=str,
        nargs='+',
        required=False,
        default=["mx", "my", "mz"],
        help="magnetization components to plot and analyze, any of: mx my mz, defaults to all"
    )

    comm_resonance.add_argument(
        "--plot-depth",
        dest="plot_depth",
        type=int,
        required=False,
        default=1,
        help="the number of split levels to plot, defaults to 1"
    )

    # spatial args

    argobj_spatial_dates = comm_spatial.add_argument(
        "date",
        type=str,
        nargs='*',
        default=[anl.paths.top.latest_date()],
        help="the list of dates to analyze (YYYY-MM-DD_hhmm), defaults to latest"
    )

    argobj_spatial_components = comm_spatial.add_argument(
        "--components",
        dest="components",
        type=str,
        nargs='+',
        required=False,
        default=["x", "y", "z"],
        help="components to plot and analyze, any of: x y z, defaults to all"
    )

    comm_spatial.add_argument(
        "--quantities",
        dest="quantities",
        type=str,
        nargs='+',
        required=False,
        default=None,
        help="quantities to plot, defaults to all"
    )

    # spatialline args

    argobj_spatialline_dates = comm_spatialline.add_argument(
        "date",
        type=str,
        nargs='*',
        default=[anl.paths.top.latest_date()],
        help="the list of dates to analyze (YYYY-MM-DD_hhmm), defaults to latest"
    )

    comm_spatialline.add_argument(
        "--quantity",
        type=str,
        required=True,
        help="the quantity to be plotted"
    )

    argobj_spatialline_components = comm_spatialline.add_argument(
        "--components",
        dest="components",
        type=str,
        nargs='+',
        required=False,
        default=["x", "y", "z"],
        help="magnetization components to plot and analyze, any of: x y z, defaults to all"
    )

    comm_spatialline.add_argument(
        "--show",
        action="store_true",
        default=False,
        help="whether to show the plot in a new window, defaults to False"
    )

    comm_spatialline.add_argument(
        "--save",
        action="store_true",
        default=True,
        help="whether to save the plot, defaults to True"
    )

    spatialline_axis_grp = comm_spatialline.add_mutually_exclusive_group(required=True)

    spatialline_axis_grp.add_argument(
        "-x",
        dest="x_val",
        type=int,
        help="plots a vertical line of values with the given x-value"
    )

    spatialline_axis_grp.add_argument(
        "-y",
        dest="y_val",
        type=int,
        help="plots a horizontal line of values with the given y-value"
    )

    # Parsing

    args = parser.parse_args()

    if args.command == "preparse":

        __validate_date(args.date, argobj_preparse_dates)
        __validate_arg_option(args.result_type, argobj_result_type, ("resonance", "spatial"))

        return (Commands.PREPARSE, (args.date, args.result_type), (args.cli_test,))

    if args.command == "resonance":

        __validate_date(args.date, argobj_resonance_dates)
        __validate_arg_list(args.mag_vars, argobj_mag_vars, ("mx", "my", "mz"))

        return (Commands.RESONANCE, (args.date, args.mag_vars, args.plot_depth), (args.cli_test,))

    if args.command == "spatial":

        __validate_date(args.date, argobj_spatial_dates)
        __validate_arg_list(args.components, argobj_spatial_components, ("x", "y", "z"))

        return (Commands.SPATIAL, (args.date, args.components, args.quantities), (args.cli_test,))

    if args.command == "spatialline":

        __validate_date(args.date, argobj_spatialline_dates)
        __validate_arg_list(args.components, argobj_spatialline_components, ("x", "y", "z"))

        comm_args = [args.date, args.quantity, args.components, args.show, args.save]

        if args.x_val is not None:
            comm_args.extend(("x", args.x_val))
        elif args.y_val is not None:
            comm_args.extend(("y", args.y_val))

        return (Commands.SPATIALLINE, list(comm_args), (args.cli_test,))

#endregion

#region Refs

def __fetch_raw():
    print("Fetching raw data from Google Drive...")
    anl.fetch.fetch_raw(DATE)

#endregion

#region Resonance

#region Splits and calculations

def __split_phi():
    print("Splitting by phi...")
    anl.split.split_phi(DATE)


def __split_phi_fRF():
    print("Splitting by phi, f_RF...")
    anl.split.split_phi_fRF(DATE)


def __calc_amp():
    print("Calculating amplitude data...")
    anl.amplitude.amp_phi_fRF(DATE)
    anl.amplitude.max_amp_phi(DATE)


def __calc_mag_fit():
    print("Calculating curve-fit for amplitudes...")
    for mag in MAG_VARS:
        anl.fit.fit_cauchy(mag_var=mag, xlim=[3.5e9, 6.0e9], date=DATE)

#endregion

#region Plots

def __plot_mag():
    print("Plotting mx, my, mz against t from table data...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.data.data_path(DATE)),
            x_var="t",
            y_vars=["mx", "my", "mz"]
        ),
        xlabel="t (s)",
        save_to=os.path.join(
            anl.paths.plots.plot_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
    )


def __plot_MaxAngle():                                                #pylint: disable=invalid-name
    print("Plotting MaxAngle against t from table data...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.data.data_path(DATE)),
            x_var="t",
            y_vars=["MaxAngle"]
        ),
        xlabel="t (s)",
        ylabel="MaxAngle (rad)",
        save_to=os.path.join(
            anl.paths.plots.plot_dir(DATE, ["aggregate"]), "MaxAngle against t.pdf")
    )


def __plot_mag_phi():
    print("Plotting mx, my, mz against t from data split by phi...")
    anl.plot.plot_dataset_xy(
        attr_data=anl.read.read_dataset(anl.paths.data.dataset_dir(DATE, {"phi": None})),
        x_var="t",
        y_vars=["mx", "my", "mz"],
        xlabel="t (s)",
        ylim=(-1.0, 1.0),
        save_to_root=anl.paths.plots.plot_dir(DATE, ["phi"])
    )


def __plot_mag_phi_fRF():
    print("Plotting mx, my, mz against t from data split by phi, f_RF...")

    if PLOT_DEPTH >= 2:
        anl.plot.plot_dataset_xy(
            attr_data=anl.read.read_dataset(
                anl.paths.data.dataset_dir(DATE, {"phi": None, "f_RF": None})
            ),
            x_var="t",
            y_vars=["mx", "my", "mz"],
            xlabel="t (s)",
            save_to_root=anl.paths.plots.plot_dir(DATE, ["phi, f_RF"])
        )

    else:
        print("Skipped.")


def __plot_amp():
    print("Plotting amp against f_RF...")
    for mag in MAG_VARS:
        amp_data = anl.read.read_data(anl.paths.calcvals.amp_path(mag, DATE))
        anl.plot.plot_xy(
            attr_data=anl.read.AttributedData(
                data=amp_data,
                x_var="f_RF",
                y_vars=amp_data.columns[1:]
            ),
            xlabel="f_RF (Hz)",
            ylabel=f"amp_{mag}",
            save_to=os.path.join(
                anl.paths.plots.plot_dir(DATE, ["aggregate"]), f"amp_{mag} against f_RF.pdf")
        )


def __plot_MaxAmp():                                                  #pylint: disable=invalid-name
    print("Plotting MaxAmp against phi...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.calcvals.maxamp_path(DATE)),
            x_var="phi",
            y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"]
        ),
        xlabel="phi (deg)",
        ylabel="MaxAmp",
        xstep=45,
        save_to=os.path.join(
            anl.paths.plots.plot_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
    )


def __plot_fitted_amp():
    print("Plotting curve-fitted amp against f_RF...")
    for mag in MAG_VARS:
        anl.plot.plot_function(
            data=anl.read.read_data(anl.paths.calcvals.fitted_amp_path(mag, DATE)),
            func=anl.fit.cauchy,
            params=["x_0", "gamma", "I"],
            domain=[3.5e9, 6.0e9],
            xlabel="f_RF (Hz)",
            ylabel=f"fitted amp_{mag}",
            save_to=os.path.join(
                anl.paths.plots.plot_dir(DATE, ["aggregate"]),
                f"fitted amp_{mag} against f_RF.pdf"
            )
        )


#endregion

#region Calibration checks

def __plotcheck_fitted_amp():
    print("Checks: Plotting curve fit with data points for amp against f_RF...")
    for var in MAG_VARS:

        curve_data = anl.read.read_data(anl.paths.calcvals.fitted_amp_path(var, DATE))
        amp_data = anl.read.read_data(anl.paths.calcvals.amp_path(var, DATE))
        rows = curve_data["phi"][::(len(curve_data["phi"]) // 4)]     # Extracts a few sample rows.
        domain = (3.5e9, 6.0e9)

        anl.plot.plot_function(
            data=curve_data[curve_data["phi"].isin(rows)],
            func=anl.fit.cauchy,
            params=["x_0", "gamma", "I"],
            domain=domain,
            overlay=[anl.read.AttributedData(
                amp_data[(amp_data["f_RF"] >= domain[0]) & (amp_data["f_RF"] <= domain[1])],
                x_var="f_RF",
                y_vars=rows,
                fmt='x'
            )],
            xlabel="f_RF (Hz)",
            ylabel=f"fitted amp_{var}",
            title=f"Curve-fit check for amp_{var}",
            save_to=os.path.join(
                anl.paths.plots.plot_dir(DATE, ["checks"]),
                f"check amp_{var} against f_RF.pdf"
            )
        )


#endregion

#endregion Resonance

#region Spatial

#region Conversions

def __convert_npy():
    print("Converting all .npy files to .tsv files")
    anl.geom.convert_npy(DATE)

#endregion

#region Plots

def __plot_spatial():
    print("Plotting all spatial distribution data...")

    plot_files = []
    if QUANTITIES is None:
        plot_files = [f for f in os.listdir(anl.paths.spatial.root(DATE))
            if not f.endswith("json")]
    else:
        plot_files = [f for f in os.listdir(anl.paths.spatial.root(DATE))
            if not f.endswith("json") and f in QUANTITIES]

    # Checks if plot_files is empty.
    if not plot_files:
        print("No data matches the requested patterns.")

    for filename in plot_files:
        for component in COMPONENTS:

            try:
                anl.plot.plot_image(
                    anl.read.read_data(
                        anl.paths.spatial.spatial_path(
                            filename, component, None, DATE)
                    ),
                    xlabel="x (m)",
                    ylabel="y (m)",
                    title=filename + " (T)",
                    save_to=anl.paths.plots.spatial_dir(
                        filename, component, DATE
                    ),
                    xindexes=None,
                    yindexes=None,
                    show_plot=False,
                    date=DATE
                )

            except FileNotFoundError:

                print(f"{component} not found for {filename}. Component skipped.")

                #TODO: Check that it's only the singular component that is not found.
                #      Otherwise the error should still be raised.

#endregion

#endregion Spatial

#region Spatial line

def __plot_spatial_line():

    print("Plotting spatial line...")

    for component in COMPONENTS:

        anl.plot.plot_spatial_line(
            date=DATE,
            x_index=AXIS_VAL if AXIS == 'x' else None,
            y_index=AXIS_VAL if AXIS == 'y' else None,
            component=component,
            filename=QUANTITY,
            save_to = anl.paths.plots.spatial_line(
                filename=QUANTITY,
                component=component,
                xaxis_name=('y' if AXIS == 'x' else 'x'),
                line_index_name=AXIS,
                line_index = AXIS_VAL,
                date=date
            ) if SAVE else None,
            show_plot=SHOW,
        )

#endregion

#region Preparse

def __convert_table_txt():
    print("Converting table.txt to table.tsv...")
    anl.read.convert_table_txt(DATE)

def __create_json():
    print("Creating the json file...")
    anl.write.write_json(DATE)

#endregion

#region Run

COMMAND, COMM_ARGS, TOP_ARGS = __parse_cli_input()

if COMMAND is Commands.PREPARSE:
    date_arg, RESULT_TYPE = COMM_ARGS                                        #pylint: disable=W0632
elif COMMAND is Commands.RESONANCE:
    date_arg, MAG_VARS, PLOT_DEPTH = COMM_ARGS                               #pylint: disable=W0632
elif COMMAND is Commands.SPATIAL:
    date_arg, COMPONENTS, QUANTITIES = COMM_ARGS                             #pylint: disable=W0632
elif COMMAND is Commands.SPATIALLINE:
    date_arg, QUANTITY, COMPONENTS, SHOW, SAVE, AXIS, AXIS_VAL = COMM_ARGS   #pylint: disable=W0632

DATES = __resolve_dates(date_arg)
CLI_TEST = TOP_ARGS[0]

if len(DATES) > 1:
    print(f"Running analysis for {len(DATES)} results: {DATES}. \n")

if COMMAND is Commands.PREPARSE:

    for date in DATES:

        DATE = date

        print(
            "Running analysis (preparse) with parameters:",
            f"date: {DATE.__repr__()}",
            f"result_type: {RESULT_TYPE.__repr__()}",
            sep='\n  ',
            end='\n\n'
        )

        if RESULT_TYPE == "resonance":
            __timed_run([__convert_table_txt])
        elif RESULT_TYPE == "spatial":
            __timed_run([__create_json])

elif COMMAND is Commands.RESONANCE:

    #TODO: Modifying DATE directly is very hacky.

    for date in DATES:

        DATE = date

        print(
            "Running analysis (resonance) with parameters:",
            f"date: {DATE.__repr__()}",
            f"mag-vars: {MAG_VARS.__repr__()}",
            f"plot-depth: {PLOT_DEPTH.__repr__()}",
            sep='\n  ',
            end='\n\n'
        )

        __timed_run([
            __fetch_raw,
            __convert_table_txt,
            __split_phi,
            __split_phi_fRF,
            __calc_amp,
            __calc_mag_fit,
            __plot_mag,
            __plot_MaxAngle,
            __plot_mag_phi,
            __plot_mag_phi_fRF,
            __plot_amp,
            __plot_MaxAmp,
            __plot_fitted_amp,
            __plotcheck_fitted_amp
        ])

elif COMMAND is Commands.SPATIAL:

    for date in DATES:

        DATE = date

        print(
            "Running analysis (spatial) with parameters:",
            f"date: {DATE.__repr__()}",
            f"components: {COMPONENTS.__repr__()}",
            sep='\n  ',
            end='\n\n'
        )

        __timed_run([
            __fetch_raw,
            __convert_npy,
            __plot_spatial
        ])

elif COMMAND is Commands.SPATIALLINE:

    for date in DATES:

        DATE = date

        print(
            "Running analysis (spatialline) with parameters:",
            f"date: {DATE.__repr__()}",
            f"quantity: {QUANTITY.__repr__()}",
            f"components: {COMPONENTS.__repr__()}",
            f"show: {SHOW.__repr__()}",
            f"save: {SAVE.__repr__()}",
            f"axis: {AXIS.__repr__()}",
            f"axis_val: {AXIS_VAL.__repr__()}",
            sep='\n  ',
            end='\n\n'
        )

        __timed_run([
            __fetch_raw,
            __convert_npy,
            __plot_spatial_line
        ])

#endregion
