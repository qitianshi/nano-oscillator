"""Analysis, plotting, read/write, parsing, and data check functions for
results from mumax3.

Terminology used in this package:
* data: A single `*.tsv` file containing either mumax3 output or calculated
  data.
* dataset: A folder, in any location, containing zero, one, or more data files,
  or zero, one, or more subdirectories containing the same.
* raw: Raw output from mumax3, either in its original `table.txt` form or in
  the converted `table.tsv` form.
* result: A folder at the top level of the `results` directory. Its name
  follows the convention "YYYY-MM-DD_hhmm".
* split: Breaking raw data into several smaller data files, which are then
  saved to disk in the appropriate result folder.
* variable: A variable from the mumax3 simulation. Used to identify columns
  in data.

The package requires Python 3.9 or later.
"""

from analysis import amplitude, fit, geom, paths, plot, read, refs, split, write
