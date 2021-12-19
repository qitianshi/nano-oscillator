#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
import sys
import analysis as anl

DATE = sys.argv[1]

print("Plotting mx, my, mz against t from data split by phi...")
anl.plot.plot_dataset_xy(
    data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    save_to_root=anl.paths.plots_dir(DATE, ["phi"])
)

PYSCRIPT
