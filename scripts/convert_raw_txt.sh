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

print("Converting raw.txt to raw.tsv...")
anl.read.convert_raw_txt(DATE)

print(f"Done in {time() - t_init:.1f}s.")

PYSCRIPT
