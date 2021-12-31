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

print("Plotting mx, my, mz against t from table data...")
anl.plot.plot_xy(
    attr_data=anl.read.AttributedData(
        data=anl.read.read_data(anl.paths.Data.data_path(DATE)),
        x_var="t",
        y_vars=["mx", "my", "mz"]
    ),
    xlabel="t (s)",
    save_to=join(anl.paths.Plots.plot_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
