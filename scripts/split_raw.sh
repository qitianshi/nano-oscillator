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

print("Splitting raw data...")
anl.split.split_phi(DATE)
anl.split.split_phi_fRF(DATE)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
