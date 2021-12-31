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

print("Plotting amp against f_RF...")
for mag in MAG_VARS:
    amp_data = anl.read.read_data(anl.paths.CalcVals.amp_path(mag, DATE))
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=amp_data,
            x_var="f_RF",
            y_vars=amp_data.columns[1:]
        ),
        xlabel="f_RF (Hz)",
        ylabel=f"amp_{mag}",
        save_to=join(
            anl.paths.Plots.plot_dir(DATE, ["aggregate"]), f"amp_{mag} against f_RF.pdf")
    )

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
