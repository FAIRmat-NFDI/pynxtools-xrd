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
"""XRD reader built on MultiFormatReader."""

import json
import numpy as np
import os
import re
import flatdict
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


def _clean_mapping(mapping: dict[str, Any]) -> dict[str, Any]:
    """Return a mapping without entries whose data path doesn't exist or whose value is empty."""
    result: dict[str, Any] = {}

    for key, value in mapping.items():
        if value.startswith("@link:"):
            link_path = value.split("@link:", 1)[-1]
            if mapping.get(link_path):
                value = value.copy()
                value["link"] = convert_to_hdf_file_path(link_path)
                result[key] = value
        elif value:
            result[key] = value

    return result


def _mapping_to_config(mapping: dict[str, Any]) -> dict[str, Any]:
    """Convert /data/path values to @attr:data/path for fill_from_config."""
    return {
        k: f"@attr:{v[1:]}" if isinstance(v, str) and v.startswith("/") else v
        for k, v in mapping.items()
    }


def _get_minimal_step(lst: list[float] | np.ndarray) -> float:
    """
    Return the minimal difference between two consecutive values
    in a list. Used for extracting minimal difference in a
    list with (potentially) non-uniform spacing.

    Args:
        lst (list): List of data points.

    Returns:
        step (float): Non-zero, minimal distance between consecutive data
        points in lst.

    """
    lst1 = np.roll(lst, -1)
    diff = np.abs(np.subtract(lst, lst1))
    step = round(np.min(diff[diff != 0]), 2)

    return step


def _extract_experiment_config(data: dict[str, Any]) -> dict[str, Any]:
    """Extract experimental scan parameters from measured axes."""
    axes = ("2Theta", "Omega")
    config: dict[str, Any] = {}

    for axis in axes:
        values = data.get(axis)
        if values is None:
            continue

        config[f"{axis}_start"] = values[0]
        config[f"{axis}_end"] = values[-1]
        config[f"{axis}_step"] = _get_minimal_step(values)

    return config


def _normalize_units(data: dict[str, Any]) -> None:
    """Normalize unit labels."""
    unit_map = {"Å": "angstrom"}

    for key, value in data.items():
        if key.endswith("@units"):
            data[key] = unit_map.get(value, value)


class XRDReader(MultiFormatReader):
    """Reader for XRD."""

    supported_nxdls = ["NXxrd_pan"]
    supported_formats = [".rasx", ".xrdml", ".brml"]
    suppress_warnings = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data: dict = {}

        self.extensions = {ext: self._handle_xrd_file for ext in self.supported_formats}

        with open(
            os.path.dirname(os.path.realpath(__file__)) + os.sep + "xrd.config.json"
        ) as config_file:
            self.config_dict = json.load(config_file)
        self.config_dict = _clean_mapping(self.config_dict)
        self.config_dict = _mapping_to_config(self.config_dict)

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
        data = dict(
            flatdict.FlatDict(
                self.convert_quantity_to_value_units(read_file(file_path)),
                delimiter="/",
            )
        )
        # Post process to get the experiment_config and normalize units
        data.update(_extract_experiment_config(data))
        _normalize_units(data)

        self.data = dict(data)

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

    def get_attr(self, key: str, path: str) -> Any:
        """Resolve ``@attr:path`` tokens by traversal into ``self.data``."""
        try:
            return self.data.get(path)
        except (KeyError, TypeError):
            return None

    def setup_template(self) -> dict[str, Any]:
        return {
            "/@default": "entry",
        }

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] | None = None,
        **kwargs,
    ) -> dict:
        return super().read(template, file_paths, objects, suppress_warning=True)


READER = XRDReader
