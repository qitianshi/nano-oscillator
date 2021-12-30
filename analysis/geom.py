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

            #TODO raise FileNotFoundError

            filename = os.path.splitext(file)[0]
            if not os.path.isdir(paths.geom_dir(filename, date)):
                os.mkdir(paths.geom_dir(filename, date))

            fields[filename] = np.load(os.path.join(paths.dataset_dir(), file))

            for component in range(len(fields[filename])):
                mag_var = mag_vars[component]
                for slices in range(len(fields[filename][component])):
                    pd.DataFrame(fields[filename][component][slices]) \
                        .to_csv(paths.spatial_path(
                            slices, filename, mag_var, date), sep="\t", index=False
                        )


def preparse_yml(header: list):
    """Parses the header data as yaml."""

    for line_index, line in enumerate(header):
        #removes double whitespaces
        line = re.sub("\s\s+" , " ", line)

        #split based on multiple colons in the same line
        if line.count(":") > 1:
            new_val = line.split(":", 1)
            new_val[0] = new_val[0] + ": "
            new_val[1] = " " + new_val[1]
            header.pop(line_index)
            header = header[:line_index] + new_val + header[line_index:]

    offset = 0
    for line_index in range(len(header)):
        #split based on spaces that do not follow a colon
        line_index += offset
        if " " in header[line_index][header[line_index].index(": ") + 2:]:

            indentation = "" + "- "
            if header[line_index].split(":")[0].startswith("  "):
                indentation = "  " + indentation

            new_list = (
                [header[line_index].split(":")[0] + ":"] +
                [indentation + string for string in
                    header[line_index][header[line_index].index(": ") + 2:].split(" ")
                ]
            )
            header.pop(line_index)
            header = header[:line_index] + new_list + header[line_index:]
            offset += len(new_list) - 1

    return "\n".join(header)


def get_header(date: str = None) -> list[str]:

    with open(paths.geom_ovf_path(0, date), 'r', encoding='utf-8') as file:

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