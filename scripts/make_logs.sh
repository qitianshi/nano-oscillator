#!/bin/bash

# Generates a day-by-day changelog from Git history.

# Adapted from an answer by user:takeshin and another by user:kristianlm on Stack Overflow:
# https://stackoverflow.com/a/2979587 and https://stackoverflow.com/a/4712213.
# Licensed under CC-BY-SA 4.0.


NEXT=$(date +%F)

echo "CHANGELOG"
echo ----------------------

git log --no-merges --format="%cd" --date=short | sort -u -r | while read DATE ; do
    echo
    echo [$DATE]
    GIT_PAGER=cat git log --no-merges --format=" * %s" --since="$DATE 00:00:00" --until="$DATE 24:00:00"
    NEXT=$DATE
done
