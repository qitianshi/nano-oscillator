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
from analysis.split import split_phi_fRF

split_phi_fRF(sys.argv[1])

PYSCRIPT
