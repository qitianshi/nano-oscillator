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

print("Checks: Plotting curve fit with data points for amp against f_RF...")
for mag_var in ["mx", "my", "mz"]:

    curve_data = anl.read.read_data(anl.paths.fitted_amp_path(mag_var))
    raw_data = anl.read.read_data(anl.paths.amp_path(mag_var, DATE))
    rows = curve_data["phi"][::(len(curve_data["phi"]) // 4)]     # Extracts a few sample rows.
    domain = (3.5e9, 6.0e9)

    anl.plot.plot_function(
        data=curve_data[curve_data["phi"].isin(rows)],
        func=anl.fit.cauchy,
        params=["x_0", "gamma", "I"],
        domain=domain,
        overlay=[anl.read.AttributedData(
            raw_data[(raw_data["f_RF"] >= domain[0]) & (raw_data["f_RF"] <= domain[1])],
            x_var="f_RF",
            y_vars=rows,
            fmt='x'
        )],
        xlabel="f_RF (Hz)",
        ylabel=f"fitted amp_{mag_var}",
        title=f"Curve-fit check for amp_{mag_var}",
        save_to=join(
            anl.paths.plots_dir(DATE, ["checks"]),
            f"check amp_{mag_var} against f_RF.pdf"
        )
    )

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
