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

from typing import Tuple, Any, Dict, Union
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import re

import pint


from pynxtools.dataconverter.helpers import (
    generate_template_from_nxdl,
    validate_data_dict,
)
from pynxtools.dataconverter.template import Template
from pynxtools_xrd.read_file_formats import read_file, formats, ureg
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.json_map.reader import (
    fill_undocumented,
    fill_documented,
)


# pylint: disable=too-few-public-methods
class XRDReader(BaseReader):
    """Reader for XRD."""

    supported_nxdls = ["NXxrd_pan"]
    supported_formats = formats

    mapping = {
        "/ENTRY[entry]/definition": "NXxrd_pan",  # Any JSON data gets copied over.
        "/ENTRY[entry]/method": "X-Ray Diffraction (XRD)",
        "/ENTRY[entry]/2theta_plot/intensity": "/intensity",  # /path like strings are the hierarchy in the dict returned by read_file_formats.py:read_file
        "/ENTRY[entry]/2theta_plot/two_theta": "/2Theta",
        "/ENTRY[entry]/2theta_plot/two_theta/@units": "/2Theta@units",  # Units are added in convert_quantity_to_value_units in the dict returned by read_file_formats.py:read_file
        "/ENTRY[entry]/2theta_plot/omega": "/Omega",
        "/ENTRY[entry]/2theta_plot/omega/@units": "/Omega@units",
        "/ENTRY[entry]/2theta_plot/chi": "/Chi",
        "/ENTRY[entry]/2theta_plot/phi": "/Phi",
        "/ENTRY[entry]/2theta_plot/phi/@units": "/Phi@units",
        "/ENTRY[entry]/COLLECTION[collection]/count_time": "/countTime",
        "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/scan_axis": "/metadata/scan_axis",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_material": "/metadata/source/anode_material",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_one": "/metadata/source/kAlpha1",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_one/@units": "/metadata/source/kAlpha1@units",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_two": "/metadata/source/kAlpha2",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/k_alpha_two/@units": "/metadata/source/kAlpha2@units",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/ratio_k_alphatwo_k_alphaone": "/metadata/source/ratioKAlpha2KAlpha1",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/ratio_k_alphatwo_k_alphaone/@units": "/metadata/source/ratioKAlpha2KAlpha1@units",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/kbeta": "/metadata/source/kBeta",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_voltage": "/metadata/source/voltage",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_voltage/@units": "/metadata/source/voltage@units",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_current": "/metadata/source/current",
        "/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[source]/xray_tube_current/@units": "/metadata/source/current@units",
        "/ENTRY[entry]/SAMPLE[sample]/sample_id": "/metadata/sample_id",
        "/ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]/scan_mode": "/metadata/scan_type",
    }

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

        try:
            fill_documented(template, dict(self.mapping), template, xrd_data)
            fill_undocumented(dict(self.mapping), template, xrd_data)
        except KeyError as e:
            print(f"Skipping key, {e}, from intermediate dict.")

        return template


READER = XRDReader
