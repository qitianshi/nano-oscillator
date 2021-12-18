#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date> <reset_t>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 $2 << PYSCRIPT
import sys
from analysis.split import split_phi

split_phi(sys.argv[1], sys.argv[2])

PYSCRIPT
