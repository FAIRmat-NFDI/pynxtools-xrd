"""XRD reader."""
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
from typing import Any, Tuple

import pint
from fairmat_readers_xrd import read_file
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader


def convert_to_hdf_file_path(nexus_path):
    """Converts a nexus path to a hdf file path"""
    pattern = r"\[(.*?)]"
    path_chain = nexus_path.split("/")
    hdf_path_component = []
    for path in path_chain:
        re_match = re.search(pattern, path)
        if re_match:
            hdf_path_component.append(re_match.group(1))
        else:
            hdf_path_component.append(path)
    return "/".join(hdf_path_component)


def _get_nested(path: str, data: dict) -> Any:
    """Traverse a slash-separated path into a nested dict."""
    keys = path.split("/")
    current = data
    for key in keys:
        current = current[key]
    return current


def _mapping_to_config(mapping: dict) -> dict:
    """Convert /data/path values to @data:data/path for fill_from_config."""
    result = {}
    for k, v in mapping.items():
        if isinstance(v, str) and v.startswith("/"):
            result[k] = f"@data:{v[1:]}"
        else:
            result[k] = v
    return result


class XRDReader(MultiFormatReader):
    """Reader for XRD."""

    supported_nxdls = ["NXxrd_pan"]
    supported_formats = [".rasx", ".xrdml", ".brml"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: dict = {}
        with open(
            os.path.dirname(os.path.realpath(__file__)) + os.sep + "xrd.mapping.json"
        ) as mapping_file:
            self._base_mapping = json.load(mapping_file)
        self.extensions = {
            ext: self._handle_xrd_file for ext in self.supported_formats
        }

    def convert_quantity_to_value_units(self, data_dict):
        """
        In a dict, recursively convert every pint.Quantity into value and @units for template.
        """
        for k, v in list(data_dict.items()):
            if isinstance(v, pint.Quantity):
                data_dict[k] = v.magnitude
                data_dict[f"{k}@units"] = format(v.units, "~")
            if isinstance(v, dict):
                data_dict[k] = self.convert_quantity_to_value_units(v)
        return data_dict

    def _handle_xrd_file(self, file_path: str) -> dict[str, Any]:
        self.data = self.convert_quantity_to_value_units(read_file(file_path))
        return {}

    def handle_objects(self, objects: tuple[Any]) -> dict[str, Any]:
        if objects and objects[0] is not None and isinstance(objects[0], dict):
            self.data = self.convert_quantity_to_value_units(objects[0])
        elif not self.data:
            raise ValueError(
                "You need to provide one of the following file formats as "
                "--input-file to the converter: " + str(self.supported_formats)
            )
        return {}

    def get_data(self, key: str, path: str) -> Any:
        """Resolve ``@data:path`` tokens by traversal into ``self.data``."""
        try:
            return _get_nested(path, self.data)
        except (KeyError, TypeError):
            return None

    def post_process(self) -> dict[str, Any] | None:
        """Build the config dict from the mapping file, filtering unavailable paths."""
        mapping = dict(self._base_mapping)
        self._clean_mapping(mapping)
        self.config_dict = _mapping_to_config(mapping)
        return None

    def _clean_mapping(self, mapping: dict) -> None:
        """Remove entries whose data path doesn't exist or whose value is empty."""
        for key in list(mapping.keys()):
            value = mapping[key]
            if isinstance(value, dict) and "link" in value:
                link_path = value["link"]
                if not mapping.get(link_path):
                    del mapping[key]
                else:
                    value["link"] = convert_to_hdf_file_path(link_path)
            elif not value:
                del mapping[key]

    def setup_template(self) -> dict[str, Any]:
        return {
            "//ENTRY[entry]/@default": "experiment_result",
            "/ENTRY[entry]/experiment_result/@signal": "intensity",
            "/ENTRY[entry]/experiment_result/@axes": "two_theta",
        }


READER = XRDReader
