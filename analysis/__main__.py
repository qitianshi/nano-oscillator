"""Runs all data analyses, including splitting, calculations, and plotting."""

import argparse
import os
from sys import exit
from time import time

import analysis as anl


#region Command line

def __parse_cli_input() -> tuple[str, list[str], int, bool]:

    cli_parser = argparse.ArgumentParser(prog="analysis", description="Runs all analyses.")

    cli_parser.add_argument(
        "date",
        type=str,
        nargs='?',
        default=anl.paths.top.latest_date(),
        help="the date of the simulation (YYYY-MM-DD_hhmm), defaults to latest"
    )

    cli_arg_mag_vars = cli_parser.add_argument(
        "--mag-vars",
        dest="mag_vars",
        type=str,
        nargs='+',
        required=False,
        default=["mx", "my", "mz"],
        help="magnetization components to plot and analyze, any of: mx my mz, defaults to all"
    )

    cli_parser.add_argument(
        "--plot-depth",
        dest="plot_depth",
        type=int,
        required=False,
        default=1,
        help="the number of split levels to plot, defaults to 1"
    )

    cli_parser.add_argument(
        "--skip-spatial",
        dest="skip_spatial",
        action="store_true",
        help="skips analysis of spatial data"
    )

    cli_args = cli_parser.parse_args()

    if not os.path.exists(anl.paths.top.result_dir(cli_args.date)):
        exit(f"Error: no result was found for '{cli_args.date}'.")

    acceptable_mag_vars = ("mx", "my", "mz")
    if any(i not in acceptable_mag_vars for i in cli_args.mag_vars):
        rejected_mag_vars = list(set(cli_args.mag_vars) - set(acceptable_mag_vars))
        raise argparse.ArgumentError(
            cli_arg_mag_vars,
            f"{', '.join(rejected_mag_vars)}"
            + f" {'does not' if len(rejected_mag_vars) == 1 else 'do not'}"
            + f" match valid values: {', '.join(acceptable_mag_vars)}"
        )

    return (cli_args.date, cli_args.mag_vars, cli_args.plot_depth, cli_args.skip_spatial)

DATE, MAG_VARS, PLOT_DEPTH, SKIP_SPATIAL = __parse_cli_input()

print(
    "Running analysis with parameters:",
    f"date: {DATE.__repr__()}",
    f"mag-vars: {MAG_VARS.__repr__()}",
    f"plot-depth: {PLOT_DEPTH.__repr__()}",
    f"skip-spatial: {SKIP_SPATIAL.__repr__()}",
    sep='\n  ',
    end='\n\n'
)

#endregion

#region Fetching refs

def __fetch_raw():
    print("Fetching raw data from Google Drive...")
    anl.fetch.fetch_raw(DATE)

#endregion

#region Splits and calculations

def __convert_table_txt():
    print("Converting table.txt to table.tsv...")
    anl.read.convert_table_txt(DATE)


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


def __convert_npy():
    print("Covnerting all .npy files to .tsv files")

    if not SKIP_SPATIAL:
        anl.geom.convert_npy(DATE)
    else:
        print("Skipped.")


def __create_json():
    print("Creating the json file...")

    if not SKIP_SPATIAL:
        anl.write.write_json(DATE)
    else:
        print("Skipped.")

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


def __plot_spatial():
    print("Plotting all spatial distribution data...")

    if not SKIP_SPATIAL:
        for filename in os.listdir(anl.paths.spatial.root(DATE)):
            if not filename.endswith("json"):
                for component in MAG_VARS:
                    component = component.strip("m")
                    try:
                        anl.plot.plot_image(
                            anl.read.read_data(
                                anl.paths.spatial.spatial_path(filename, component, None, DATE)
                            ),
                            xlabel="x (m)",
                            ylabel="y (m)",
                            title=filename + " (T)",
                            save_to=anl.paths.plots.spatial_dir(
                                filename, component, DATE
                            ),
                            show_plot=False,
                            date=DATE
                        )
                    except FileNotFoundError as err:
                        if len(
                            os.listdir(os.path.join(anl.paths.spatial.root(DATE), filename))
                        ) > 0:
                            #TODO: add in condition to look for x, y or z in the name
                            print(
                                f"{component} not found for {filename}. Component skipped.")
                        else:
                            raise err

    else:
        print("Skipped.")


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

#region Run

def timed_run():
    """Runs all analyses."""

    anl_funcs = [
        __fetch_raw,
        __convert_table_txt,
        __split_phi,
        __split_phi_fRF,
        __calc_amp,
        __calc_mag_fit,
        __convert_npy,
        __create_json,
        __plot_mag,
        __plot_MaxAngle,
        __plot_mag_phi,
        __plot_mag_phi_fRF,
        __plot_amp,
        __plot_MaxAmp,
        __plot_fitted_amp,
        __plot_spatial,
        __plotcheck_fitted_amp
    ]

    t_init = time()

    for func in anl_funcs:
        t_start = time()
        func()
        print(f"  Done in {time() - t_start:.1f}s.")

    print(f"Finished {len(anl_funcs)} {'analysis' if len(anl_funcs) == 1 else 'analyses'} in", \
        f"{time() - t_init:.1f}s.")

timed_run()

#endregion
