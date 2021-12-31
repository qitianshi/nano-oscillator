"""Manipulates and writes data to files"""

import json
import os
from shutil import rmtree

import yaml

from analysis import geom, paths


def write_json(date: str = None):
    """Uses yaml to parse the data and writes it into a json file titled "headers.json"."""

    yaml_data = yaml.safe_load(geom.preparse_yml(geom.get_header(date)))

    with open(paths.header_path(date), 'w', encoding='utf-8') as file:
        json.dump(yaml_data, file, indent=4)
        file.write("\n")


def prep_dir(path: str, clear: str = True):
    """Prepares the destination directory for output. Optionally clears
    existing files and creates an empty directory.
    """

    if clear and os.path.exists(path):
        rmtree(path)

    os.makedirs(path, exist_ok=True)
    