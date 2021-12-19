#!/bin/sh

if [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <expressions>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
import analysis as anl

$1

PYSCRIPT
