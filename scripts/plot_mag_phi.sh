#!/bin/sh

if  [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
from os.path import join
import sys

from analysis.plot import plot_dataset_xy
from analysis.readresults import read_dataset, dataset_dir, result_dir

plot_dataset_xy(
    data=read_dataset(dataset_dir(sys.argv[1], {"phi": None})),
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    ylim=[-1.0, 1.0],
    save_to_root=join(result_dir(sys.argv[1]), "plots", "phi")
)

PYSCRIPT
