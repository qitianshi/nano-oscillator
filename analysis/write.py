"""Manipulates and writes data to files"""

import json
import yaml

from analysis import geom, paths


def write_json(date: str = None):
    """Uses yaml to parse the data and writes it into a json file named "headers.json"."""

    yaml_data = yaml.safe_load(geom.preparse_yml(geom.get_header(date)))

    with open(paths.Spatial.header_path(date), 'w', encoding='utf-8') as file:
        json.dump(yaml_data, file, indent=4)
        file.write("\n")
