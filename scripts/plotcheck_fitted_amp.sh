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

print("Checks: Plotting curve fit with data points for amp against f_RF...")
for var in MAG_VARS:

    curve_data = anl.read.read_data(anl.paths.CalcVals.fitted_amp_path(var))
    amp_data = anl.read.read_data(anl.paths.CalcVals.amp_path(var, DATE))
    rows = curve_data["phi"][::(len(curve_data["phi"]) // 4)]     # Extracts a few sample rows.
    domain = (3.5e9, 6.0e9)

    anl.plot.plot_function(
        data=curve_data[curve_data["phi"].isin(rows)],
        func=anl.fit.cauchy,
        params=["x_0", "gamma", "I"],
        domain=domain,
        overlay=[anl.read.AttributedData(
            amp_data[(amp_data["f_RF"] >= domain[0]) & (amp_data["f_RF"] <= domain[1])],
            x_var="f_RF",
            y_vars=rows,
            fmt='x'
        )],
        xlabel="f_RF (Hz)",
        ylabel=f"fitted amp_{var}",
        title=f"Curve-fit check for amp_{var}",
        save_to=join(
            anl.paths.Plots.plot_dir(DATE, ["checks"]),
            f"check amp_{var} against f_RF.pdf"
        )
    )

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
