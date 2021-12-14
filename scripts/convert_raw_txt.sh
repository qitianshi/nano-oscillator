#!/bin/sh

if  [[ $1 = "-h" ]]; then
    cat << HELP
usage: $0 [-h] <date>
HELP
    exit
fi

source scripts/activate_py.sh

python - $1 << PYSCRIPT
import sys
from analysis.readresults import convert_raw_txt
convert_raw_txt(sys.argv[1] if len(sys.argv) >= 2 else None)
PYSCRIPT