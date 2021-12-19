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
import analysis as anl

DATE = sys.argv[1]

RAW_DATA = anl.read.read_data(anl.paths.data_path(DATE))

print("Plotting mx, my, mz against t from raw data...")
anl.plot.plot_xy(
    data=RAW_DATA,
    x_var="t",
    y_vars=["mx", "my", "mz"],
    xlabel="t (s)",
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "mx, my, mz against t.pdf")
)

PYSCRIPT
