"""Runs all data analyses, including splitting, calculations, and plotting."""

import os

from sys import argv
from time import time

import analysis as anl


#region Setup

try:
    DATE = argv[1]
except IndexError:
    DATE = anl.paths.latest_date()
    print(f"No 'date' parameter provided. Using latest result: {DATE}")

MAG_VARS = ("mx", "my", "mz")

#endregion

#region Splitting and calculations

def __convert_raw_txt():
    print("Converting raw.txt to raw.tsv...")
    anl.read.convert_raw_txt(DATE)


def __split_raw():
    print("Splitting raw data...")
    anl.split.split_phi(DATE)
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
    anl.geom.convert_npy(DATE)


def __create_json():
    print("Creating the json file...")
    anl.write.write_json(DATE)


#endregion

#region Plotting

def __plot_mag():
    print("Plotting mx, my, mz against t from raw data...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.data_path(DATE)),
            x_var="t",
            y_vars=["mx", "my", "mz"]
        ),
        xlabel="t (s)",
        save_to=os.path.join(anl.paths.plots_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
    )


def __plot_MaxAngle():                                                #pylint: disable=invalid-name
    print("Plotting MaxAngle against t from raw data...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.data_path(DATE)),
            x_var="t",
            y_vars=["MaxAngle"]
        ),
        xlabel="t (s)",
        ylabel="MaxAngle (rad)",
        save_to=os.path.join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAngle against t.pdf")
    )


def __plot_mag_phi():
    print("Plotting mx, my, mz against t from data split by phi...")
    anl.plot.plot_dataset_xy(
        attr_data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None})),
        x_var="t",
        y_vars=["mx", "my", "mz"],
        xlabel="t (s)",
        ylim=(-1.0, 1.0),
        save_to_root=anl.paths.plots_dir(DATE, ["phi"])
    )


def __plot_mag_phi_fRF():
    print("Plotting mx, my, mz against t from data split by phi, f_RF...")
    anl.plot.plot_dataset_xy(
        attr_data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None, "f_RF": None})),
        x_var="t",
        y_vars=["mx", "my", "mz"],
        xlabel="t (s)",
        save_to_root=anl.paths.plots_dir(DATE, ["phi, f_RF"])
    )


def __plot_amp():
    print("Plotting amp against f_RF...")
    for mag in MAG_VARS:
        amp_data = anl.read.read_data(anl.paths.amp_path(mag, DATE))
        anl.plot.plot_xy(
            attr_data=anl.read.AttributedData(
                data=amp_data,
                x_var="f_RF",
                y_vars=amp_data.columns[1:]
            ),
            xlabel="f_RF (Hz)",
            ylabel=f"amp_{mag}",
            save_to=os.path.join(
                anl.paths.plots_dir(DATE, ["aggregate"]), f"amp_{mag} against f_RF.pdf")
        )


def __plot_MaxAmp():                                                  #pylint: disable=invalid-name
    print("Plotting MaxAmp against phi...")
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=anl.read.read_data(anl.paths.maxamp_path(DATE)),
            x_var="phi",
            y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"]
        ),
        xlabel="phi (deg)",
        ylabel="MaxAmp",
        xstep=45,
        save_to=os.path.join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
    )


def __plot_fitted_amp():
    print("Plotting curve-fitted amp against f_RF...")
    for mag in MAG_VARS:
        anl.plot.plot_function(
            data=anl.read.read_data(anl.paths.fitted_amp_path(mag)),
            func=anl.fit.cauchy,
            params=["x_0", "gamma", "I"],
            domain=[3.5e9, 6.0e9],
            xlabel="f_RF (Hz)",
            ylabel=f"fitted amp_{mag}",
            save_to=os.path.join(
                anl.paths.plots_dir(DATE, ["aggregate"]),
                f"fitted amp_{mag} against f_RF.pdf"
            )
        )


def __plot_spatial():
    print("Plotting all spatial distribution data...")
    for filename in os.listdir(anl.paths.spatial_dir()):
        if not filename.endswith("json"):
            for mag_var in ["mx", "my", "mz"]:
                try:
                    anl.plot.plot_image(
                        anl.read.read_data(anl.paths.spatial_path(filename, mag_var, date=DATE)),
                        xlabel="x (m)",
                        ylabel="y (m)",
                        title = filename + " (T)",
                        save_to=anl.paths.plots_spatial_dir(filename, mag_var, date=DATE),
                        show_plot=False
                    )
                except FileNotFoundError as e:
                    if os.path.isdir(os.path.join(anl.paths.spatial_dir(DATE), filename)):
                        print(f"{mag_var} component not found for {filename}. Component skipped.")
                    else:
                        raise e


#endregion

#region Calibration checks

def __plotcheck_fitted_amp():
    print("Checks: Plotting curve fit with data points for amp against f_RF...")
    for var in MAG_VARS:

        curve_data = anl.read.read_data(anl.paths.fitted_amp_path(var))
        raw_data = anl.read.read_data(anl.paths.amp_path(var, DATE))
        rows = curve_data["phi"][::(len(curve_data["phi"]) // 4)]     # Extracts a few sample rows.
        domain = (3.5e9, 6.0e9)

        anl.plot.plot_function(
            data=curve_data[curve_data["phi"].isin(rows)],
            func=anl.fit.cauchy,
            params=["x_0", "gamma", "I"],
            domain=domain,
            overlay=[anl.read.AttributedData(
                raw_data[(raw_data["f_RF"] >= domain[0]) & (raw_data["f_RF"] <= domain[1])],
                x_var="f_RF",
                y_vars=rows,
                fmt='x'
            )],
            xlabel="f_RF (Hz)",
            ylabel=f"fitted amp_{var}",
            title=f"Curve-fit check for amp_{var}",
            save_to=os.path.join(
                anl.paths.plots_dir(DATE, ["checks"]),
                f"check amp_{var} against f_RF.pdf"
            )
        )


#endregion

#region Run analyses

def timed_run():
    """Runs all analyses."""

    anl_funcs = [
        __convert_raw_txt,
        __split_raw,
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

    print(f"Finished all analyses in {time() - t_init:.1f}s.")

timed_run()

#endregion
