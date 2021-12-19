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

print("Plotting MaxAmp against phi...")
anl.plot.plot_xy(
    data=anl.read.read_data(anl.paths.maxamp_path(DATE)),
    x_var="phi",
    y_vars=["MaxAmp_mx", "MaxAmp_my", "MaxAmp_mz"],
    xlabel="phi (deg)",
    ylabel="MaxAmp",
    xstep=45,
    save_to=join(anl.paths.plots_dir(DATE, ["aggregate"]), "MaxAmp against phi.pdf")
)

PYSCRIPT
