"""All .ovf file related functions"""

import os
import re

import pandas as pd
import numpy as np

from analysis import paths


def convert_npy(date: str = None):
    """Converts all .npy files to .tsv files."""

    date = date if date is not None else paths.latest_date()
    mag_vars = ["mz", "my", "mx"]

    for file in os.listdir(paths.dataset_dir()):

        fields = {}

        if file.endswith(".npy"):

            #TODO raise FileNotFoundError, use prep_dir()

            filename = os.path.splitext(file)[0]
            if not os.path.isdir(paths.geom_dir(filename, date)):
                os.mkdir(paths.geom_dir(filename, date))

            fields[filename] = np.load(os.path.join(paths.dataset_dir(), file))

            for component in range(len(fields[filename])):
                mag_var = mag_vars[component]
                for slices in range(len(fields[filename][component])):
                    pd.DataFrame(fields[filename][component][slices]) \
                        .to_csv(paths.spatial_path(
                            filename, mag_var, slices, date), sep="\t", index=False
                        )


def preparse_yml(header: list):
    """Parses the header data as yaml."""

    for i, line in enumerate(header):
        #removes double whitespaces
        line = re.sub(r"\s\s+" , " ", line)

        #split based on multiple colons in the same line
        if line.count(":") > 1:
            new_val = line.split(":", 1)
            new_val[0] = new_val[0] + ": "
            new_val[1] = " " + new_val[1]
            header.pop(i)
            header = header[:i] + new_val + header[i:]

    offset = 0
    for i, _ in enumerate(header):
        #split based on spaces that do not follow a colon
        i += offset
        if " " in header[i][header[i].index(": ") + 2:]:

            indentation = "" + "- "
            if header[i].split(":")[0].startswith("  "):
                indentation = "  " + indentation

            new_list = (
                [header[i].split(":")[0] + ":"] +
                [indentation + string for string in
                    header[i][header[i].index(": ") + 2:].split(" ")
                ]
            )
            header.pop(i)
            header = header[:i] + new_list + header[i:]
            offset += len(new_list) - 1

    return "\n".join(header)


def get_header(date: str = None) -> list[str]:
    """Returns the list of headers from any .ovf file"""

    for file in os.listdir(paths.dataset_dir(date)):
        if file.endswith(".ovf"):
            data = paths.geom_ovf_path(file.strip(".ovf"), date)

    with open(data, 'r', encoding='utf-8', errors="surrogateescape") as file:

        line = file.readline()
        while not line.startswith("# Segment count"):
            line = file.readline()

        seg_count = int(line.split(":")[-1])

        if seg_count > 1:
            raise NotImplementedError("Segment count is more than 1 🤡")

        ovf_headers = []
        line = file.readline()
        while not line.startswith("# End: Header"):
            line = file.readline()
            ovf_headers.append(line.strip("#").strip())

        ovf_headers = ovf_headers[
            (ovf_headers.index("Begin: Header") + 1)
            :(ovf_headers.index("End: Header"))
        ]

    return ovf_headers
