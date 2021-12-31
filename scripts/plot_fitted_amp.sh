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
import sys
from time import time
import analysis as anl

try:
    DATE = argv[1]
except IndexError:
    DATE = anl.paths.Top.latest_date()
    print(f"No 'date' parameter provided. Using latest result: {DATE}")

MAG_VARS = ("mx", "my", "mz")
t_init = time()

print("Plotting curve-fitted amp against f_RF...")
for mag in MAG_VARS:
    anl.plot.plot_function(
        data=anl.read.read_data(anl.paths.CalcVals.fitted_amp_path(mag)),
        func=anl.fit.cauchy,
        params=["x_0", "gamma", "I"],
        domain=[3.5e9, 6.0e9],
        xlabel="f_RF (Hz)",
        ylabel=f"fitted amp_{mag}",
        save_to=join(
            anl.paths.Plots.plot_dir(DATE, ["aggregate"]),
            f"fitted amp_{mag} against f_RF.pdf"
        )
    )

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
