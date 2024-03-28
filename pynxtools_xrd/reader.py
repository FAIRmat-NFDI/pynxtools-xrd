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

import yaml

from pynxtools.dataconverter.helpers import (
    validate_data_dict,
)
from pynxtools.dataconverter.convert import logger
from pynxtools.dataconverter.template import Template
from pynxtools_xrd.xrd_parser import parse_and_fill_template
from pynxtools.dataconverter.readers.utils import flatten_and_replace, FlattenSettings
from pynxtools.dataconverter.readers.base.reader import BaseReader

CONVERT_DICT: Dict[str, str] = {
    "unit": "@units",
    "Instrument": "INSTRUMENT[instrument]",
    "Source": "SOURCE[source]",
    "Detector": "DETECTOR[detector]",
    "Collection": "COLLECTION[collection]",
    "Sample": "SAMPLE[sample]",
    "version": "@version",
    "User": "USER[user]",
}


# Global var to collect the root from get_template_from_nxdl_name()
# and use it in the the the varidate_data_dict()
ROOT: ET.Element = None
REPLACE_NESTED: Dict[str, Any] = {}
XRD_FILE_EXTENSIONS = [".xrdml", "xrdml", ".udf", ".raw", ".xye"]


def get_template_from_xrd_reader(nxdl_name, file_paths):
    """Get filled template from reader.

    Parameters
    ----------
    nxdl_name : str
        Name of nxdl definition
    file_paths : Tuple[str]
        Tuple of path of files.

    Returns
    -------
    Template
        Template which is a map from NeXus concept path to value.
    """

    # template = get_template_from_nxdl_name(nxdl_name)

    data = XRDReader().read(template=template, file_paths=file_paths)
    validate_data_dict(template=template, data=data, nxdl_root=ROOT)
    return data


# pylint: disable=too-few-public-methods
class XRDReader(BaseReader):
    """Reader for XRD."""

    supported_nxdls = ["NXxrd_pan"]

    def read(
        self,
        template: Union[dict, 'Template'] = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ):
        """General read menthod to prepare the template."""

        if not isinstance(file_paths, tuple) and not isinstance(file_paths, list):
            file_paths = (file_paths,)
        filled_template: Union[Dict, None] = None
        eln_dict: Union[Dict[str, Any], None] = None
        xrd_file: str = ""
        xrd_file_ext: str = ""
        for file in file_paths:
            ext = "".join(Path(file).suffixes)
            # Read ELN file
            if ext in [".yaml", ".yml"]:
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(fl_obj), CONVERT_DICT, REPLACE_NESTED
                        )
                    )
            # Read XRD file
            elif ext in XRD_FILE_EXTENSIONS:
                xrd_file_ext = ext
                xrd_file = file
        if xrd_file:
            filled_template = parse_and_fill_template(template, xrd_file, eln_dict, xrd_file_ext, logger)
        else:
            raise ValueError(
                f"Allowed XRD experimental with extenstion from"
                f" {XRD_FILE_EXTENSIONS} found {xrd_file_ext}"
            )

        return filled_template


READER = XRDReader
