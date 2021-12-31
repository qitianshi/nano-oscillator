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

print("Plotting MaxAmp against phi...")
anl.plot.plot_xy(
    attr_data=anl.read.AttributedData(
        data=anl.read.read_data(anl.paths.CalcVals.maxamp_path(DATE)),
        x_var="phi",
        y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"]
    ),
    xlabel="phi (deg)",
    ylabel="MaxAmp",
    xstep=45,
    save_to=join(anl.paths.Plots.plot_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
