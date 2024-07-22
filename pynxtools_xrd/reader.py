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

from typing import Tuple, Any
import json
import os

import pint

from fairmat_readers_xrd import read_file
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.json_map.reader import (
    fill_undocumented,
    fill_documented,
)


# pylint: disable=too-few-public-methods
class XRDReader(BaseReader):
    """Reader for XRD."""

    supported_nxdls = ["NXxrd_pan"]
    supported_formats = [".rasx", ".xrdml", ".brml"]

    def __init__(self):
        """Initializes the reader and sets up the supported mapping."""
        with open(
            os.path.dirname(os.path.realpath(__file__)) + os.sep + "xrd.mapping.json"
        ) as mapping_file:
            self.mapping = json.load(mapping_file)

    def convert_quantity_to_value_units(self, data_dict):
        """
        In a dict, recursively convert every pint.Quantity into value and @units for template

        Args:
            data_dict (dict): A nested dictionary containing pint.Quantity and other data.
        """
        for k, v in list(data_dict.items()):
            if isinstance(v, pint.Quantity):
                data_dict[k] = v.magnitude
                data_dict[f"{k}@units"] = format(v.units, "~")
            if isinstance(v, dict):
                data_dict[k] = self.convert_quantity_to_value_units(v)
        return data_dict

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ):
        """Read method that returns a filled in pynxtools dataconverter template."""
        try:
            xrd_file_path = list(
                filter(
                    lambda paths: any(
                        format in paths for format in self.supported_formats
                    ),
                    file_paths,
                )
            )[0]
            xrd_data = self.convert_quantity_to_value_units(read_file(xrd_file_path))
        except IndexError:
            if objects[0] is not None and isinstance(objects[0], dict):
                xrd_data = self.convert_quantity_to_value_units(objects[0])
            else:
                raise ValueError(
                    "You need to provide one of the following file formats as --input-file to the converter: "
                    + str(self.supported_formats)
                )
        print(" #### : xrd_data", xrd_data)
        print(" #### : template", template)
        try:
            fill_documented(template, dict(self.mapping), template, xrd_data)
            fill_undocumented(dict(self.mapping), template, xrd_data)
        except KeyError as e:
            print(f"Skipping key, {e}, from intermediate dict.")

        return template


READER = XRDReader
