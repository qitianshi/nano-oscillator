#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
import sys
import analysis as anl

DATE = sys.argv[1]

print("Plotting amp against f_RF...")
for mag in ["mx", "my", "mz"]:
    AMP_DATA = anl.read.read_data(anl.paths.amp_path(mag, DATE))
    anl.plot.plot_xy(
        data=AMP_DATA,
        x_var="f_RF",
        y_vars=AMP_DATA.columns[1:],
        xlabel="f_RF (Hz)",
        ylabel=f"amp_{mag}",
        save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), f"amp_{mag} against f_RF.pdf")
    )

PYSCRIPT
