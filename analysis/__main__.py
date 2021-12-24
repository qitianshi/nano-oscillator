"""Runs all data analyses, including splitting, calculations, and plotting."""

from os.path import join
from sys import argv
from time import time

import analysis as anl


#region Command line

try:
    DATE = argv[1]
except IndexError:
    DATE = anl.paths.latest_date()
    print(f"No 'date' parameter provided. Using latest result: {DATE}")

#endregion

t0 = time()

#region Splitting and calculations

print("Converting raw.txt to raw.tsv...")
anl.read.convert_raw_txt(DATE)

print("Splitting raw data...")
anl.split.split_phi(DATE)
anl.split.split_phi_fRF(DATE)

# Calculates amplitude data
print("Calculating amplitude data...")
anl.amplitude.amp_phi_fRF(DATE)
anl.amplitude.max_amp_phi(DATE)

# Calculates curve-fitting parameters for amplitude
print("Calculating curve-fit for amplitudes...")
for mag_var in ["mx", "my", "mz"]:
    anl.fit.fit_cauchy(mag_var=mag_var, xlim=[3.5e9, 6.0e9], date=DATE)

#endregion

#region Plotting

RAW_DATA = anl.read.read_data(anl.paths.data_path(DATE))

# Plots mx, my, mz against t
print("Plotting mx, my, mz against t from raw data...")
anl.plot.plot_xy(
    attr_data=anl.plot.AttributedData(
        data=RAW_DATA,
        x_var="t",
        y_vars=["mx", "my", "mz"]
    ),
    xlabel="t (s)",
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
)

# Plots MaxAngle against t
print("Plotting MaxAngle against t from raw data...")
anl.plot.plot_xy(
    attr_data=anl.plot.AttributedData(
        data=RAW_DATA,
        x_var="t",
        y_vars=["MaxAngle"]
    ),
    xlabel="t (s)",
    ylabel="MaxAngle (rad)",
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAngle against t.pdf")
)

# Plots mag against t, split by phi
print("Plotting mx, my, mz against t from data split by phi...")
anl.plot.plot_dataset_xy(
    data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    ylim=(-1.0, 1.0),
    save_to_root=anl.paths.plots_dir(DATE, ["phi"])
)

# Plots mag against t, split by phi, f_RF
print("Plotting mx, my, mz against t from data split by phi, f_RF...")
anl.plot.plot_dataset_xy(
    data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None, "f_RF": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    ylim=(-1.0, 1.0),
    save_to_root=anl.paths.plots_dir(DATE, ["phi, f_RF"])
)

# Plots amp against f_RF
print("Plotting amp against f_RF...")
for mag_var in ["mx", "my", "mz"]:
    AMP_DATA = anl.read.read_data(anl.paths.amp_path(mag_var, DATE))
    anl.plot.plot_xy(
        attr_data=anl.plot.AttributedData(
            data=AMP_DATA,
            x_var="f_RF",
            y_vars=AMP_DATA.columns[1:]
        ),
        xlabel="f_RF (Hz)",
        ylabel=f"amp_{mag_var}",
        save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), f"amp_{mag_var} against f_RF.pdf")
    )

# Plots MaxAmp against phi
print("Plotting MaxAmp against phi...")
anl.plot.plot_xy(
    attr_data=anl.plot.AttributedData(
        data=anl.read.read_data(anl.paths.maxamp_path(DATE)),
        x_var="phi",
        y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"]
    ),
    xlabel="phi (deg)",
    ylabel="MaxAmp",
    xstep=45,
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
)

# Plots curve-fitted amp against f_RF
print("Plotting curve-fitted amp against f_RF...")
for mag_var in ["mx", "my", "mz"]:
    anl.plot.plot_function(
        data=anl.read.read_data(anl.paths.fitted_amp_path(mag_var)),
        func=anl.fit.cauchy,
        params=["x_0", "gamma", "I"],
        domain=[3.5e9, 6.0e9],
        xlabel="f_RF (Hz)",
        ylabel=f"fitted amp_{mag_var}",
        save_to=join(
            anl.paths.plots_dir(DATE, ["aggregate"]),
            f"fitted amp_{mag_var} against f_RF.pdf"
        )
    )

#endregion

t1 = time()

print(f"Finished analyses in {t1 - t0:.1f}s.")
