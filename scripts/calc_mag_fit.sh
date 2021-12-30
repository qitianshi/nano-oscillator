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

print("Calculating curve-fit for amplitudes...")
for mag_var in ["mx", "my", "mz"]:
    anl.fit.fit_cauchy(mag_var=mag_var, xlim=[3.5e9, 6.0e9], date=DATE)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
