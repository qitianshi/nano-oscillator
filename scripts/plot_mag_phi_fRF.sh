#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
from os.path import join
import sys
from time import time
import analysis as anl

DATE = sys.argv[1]
t_init = time()

print("Plotting mx, my, mz against t from data split by phi, f_RF...")
anl.plot.plot_dataset_xy(
    attr_data=anl.read.read_dataset(anl.paths.dataset_dir(DATE, {"phi": None, "f_RF": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    save_to_root=anl.paths.plots_dir(DATE, ["phi, f_RF"])
)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
