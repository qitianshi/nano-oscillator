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

print("Plotting curve-fitted amp against f_RF...")
for mag_var in ["mx", "my", "mz"]:
    anl.plot.plot_function(
        data=anl.read.read_data(anl.paths.fitted_amp_path(mag_var)),
        func=anl.fit.cauchy,
        params=["x_0", "gamma", "I"],
        domain=[3.5e9, 6.0e9],
        xlabel="f_RF (Hz)",
        ylabel="fitted amp_mz",
        save_to=join(
            anl.paths.plots_dir(DATE, ["aggregate"]),
            f"fitted amp_{mag_var} against f_RF.pdf"
        )
    )

PYSCRIPT
