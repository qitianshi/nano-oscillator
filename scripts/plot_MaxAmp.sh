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

print("Plotting MaxAmp against phi...")
anl.plot.plot_xy(
    attr_data=anl.read.AttributedData(
        data=anl.read.read_data(anl.paths.maxamp_path(DATE)),
        x_var="phi",
        y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"]
    ),
    xlabel="phi (deg)",
    ylabel="MaxAmp",
    xstep=45,
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
