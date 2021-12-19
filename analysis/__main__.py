"""Runs all data analyses, including splitting, calculations, and plotting."""

from os.path import join
import sys

import analysis as anl


DATE = sys.argv[1]

print("Converting raw.txt to raw.tsv...")
anl.read.convert_raw_txt(DATE)

print("Splitting raw data...")
anl.split.split_phi(DATE)
anl.split.split_phi_fRF(DATE)

#TODO: Calculate amplitudes
# print("Calculating amplitude data...")

RAW_DATA = anl.read.read_data(anl.paths.data_path(DATE))

# Plots mx, my, mz against t
print("Plotting mx, my, mz against t from raw data...")
anl.plot.plot_xy(
    data=RAW_DATA,
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
)

# Plots MaxAngle against t
print("Plotting MaxAngle against t from raw data...")
anl.plot.plot_xy(
    data=RAW_DATA,
    x_var="t",
    y_vars=["MaxAngle"],
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
    save_to_root=anl.paths.plots_dir(DATE, ["phi"])
)

# Plots mag against t, split by phi, f_RF
print("Plotting mx, my, mz against t from data split by phi, f_RF...")
anl.plot.plot_dataset_xy(
    data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None, "f_RF": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    save_to_root=anl.paths.plots_dir(DATE, ["phi, f_RF"])
)

#TODO: Plot amp against f_RF
# print("Plotting amp against f_RF...")

#TODO: Plot MaxAmp against phi
# print("Plotting MaxAmp against phi...")
