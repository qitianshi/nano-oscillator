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

print("Converting raw.txt to raw.tsv...")
anl.read.convert_raw_txt(DATE)

PYSCRIPT
