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

# Calculates amplitude data
print("Calculating amplitude data...")
anl.amplitude.amp_phi_fRF(DATE)
anl.amplitude.max_amp_phi(DATE)

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

# Plots amp against f_RF
print("Plotting amp against f_RF...")
for mag in ["mx", "my", "mz"]:
    AMP_DATA = anl.read.read_data(anl.paths.amp_path(mag, DATE))
    anl.plot.plot_xy(
        data=AMP_DATA,
        x_var="f_RF",
        y_vars=AMP_DATA.columns[1:],
        xlabel="f_RF (Hz)",
        ylabel=f"amp_{mag}",
        save_to=anl.paths.plots_dir(DATE, ["aggregate"])
    )

# Plots MaxAmp against phi
print("Plotting MaxAmp against phi...")
anl.plot.plot_xy(
    data=anl.read.read_data(anl.paths.maxamp_path(DATE)),
    x_var="phi",
    y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"],
    xlabel="phi (deg)",
    ylabel=["MaxAmp"],
    xstep=45,
    save_to=anl.paths.plots_dir(DATE, ["aggregate"])
)
