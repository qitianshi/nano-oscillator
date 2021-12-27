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

print("Plotting amp against f_RF...")
for mag_var in ["mx", "my", "mz"]:
    amp_data = anl.read.read_data(anl.paths.amp_path(mag_var, DATE))
    anl.plot.plot_xy(
        attr_data=anl.read.AttributedData(
            data=amp_data,
            x_var="f_RF",
            y_vars=amp_data.columns[1:]
        ),
        xlabel="f_RF (Hz)",
        ylabel=f"amp_{mag_var}",
        save_to=join(
            anl.paths.plots_dir(DATE, ["aggregate"]), f"amp_{mag_var} against f_RF.pdf")
    )

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
