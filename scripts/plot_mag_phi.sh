#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] [<date>]
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
from os.path import join
from sys import argv
from time import time
import analysis as anl

try:
    DATE = argv[1]
except IndexError:
    DATE = anl.paths.Top.latest_date()
    print(f"No 'date' parameter provided. Using latest result: {DATE}")

MAG_VARS = ("mx", "my", "mz")
t_init = time()

print("Plotting mx, my, mz against t from data split by phi...")
anl.plot.plot_dataset_xy(
    attr_data=anl.read.read_dataset(anl.paths.Data.dataset_dir(DATE, {"phi": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    ylim=(-1.0, 1.0),
    save_to_root=anl.paths.Plots.plot_dir(DATE, ["phi"])
)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
