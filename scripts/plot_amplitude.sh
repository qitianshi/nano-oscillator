#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date> <mag_var>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 $2 << PYSCRIPT
import sys
from os.path import join
from analysis import readresults, plot

data = readresults.read_data(readresults.amplitude_path(sys.argv[2], sys.argv[1]))
plot.plot_xy(
    data=data,
    x_var="f_RF",
    y_vars=data.columns[1:],
    xlabel="frequency (Hz)",
    ylabel=f"amplitude {sys.argv[2]}",
    save_to=join(readresults.result_dir(sys.argv[1]), "plots", "aggregate", f"amplitude {sys.argv[2]} against f_RF.pdf")
)

PYSCRIPT
