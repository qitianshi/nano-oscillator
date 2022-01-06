"""Analysis, plotting, read/write, parsing, and data check functions for
results from mumax3.

To use this package: run `python3 -m analysis` on macOS and Linux, or
`python -m analysis` on Windows. Use the `-h` flag for usage.

Nomenclature used in this package:
* data: A single `*.tsv` file containing either mumax3 output or calculated
  data.
* dataset: A folder, in any location, containing zero, one, or more data files,
  or zero, one, or more subdirectories containing the same.
* raw: Full mumax3 output, including tables, spatial data, and other output.
  Some modifications may be present, such as converting table.txt to table.tsv,
  or .ovf output to .npy.
* result: A folder at the top level of the `results` directory. Its name
  follows the convention "YYYY-MM-DD_hhmm".
* split: Breaking table data into several smaller data files, which are then
  saved to disk in the appropriate result folder.
* table: Table output from mumax3, either in its original `table.txt` form or
  in the converted `table.tsv` form.
* variable: A variable from the mumax3 simulation. Used to identify columns
  in data.

Requires Python 3.10 or later.
"""

from analysis import amplitude, fetch, fit, geom, paths, plot, read, split, write
