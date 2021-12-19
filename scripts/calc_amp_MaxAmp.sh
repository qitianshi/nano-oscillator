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

print("Calculating amplitude data...")
anl.amplitude.amp_phi_fRF(DATE)
anl.amplitude.max_amp_phi(DATE)

PYSCRIPT
