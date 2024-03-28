"""
XRD file parser collection.
"""

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

from typing import Dict, Any
import copy

def feed_eln_data_to_template(template, eln_dict):  
    """Feed ELN data to template.

    Parameters
    ----------
    template : Template[dict]
        Template gnenerated from nxdl definition.
    eln_dict : Dict
        Plain and '/' separated dictionary from yaml for ELN.
    """
    for key, value in copy.deepcopy(template).items():
        if eln_dict.get(key, "") and not value:
            template[key] = value


# Handle Panalytical XRDml files
def read_panalytical_xrdml(file_path: str, logger) -> Dict[str, Any]:
    return {"data": "data"}

# Handle Rigaku RASX files
def read_rigaku_rasx(file_path: str, logger) -> Dict[str, Any]:
    return {"data": "data"}
    
# Handle Bruker BRML files
def read_bruker_brml(file_path: str, logger) -> Dict[str, Any]:
    return {"data": "data"}

def fill_template(template, xrd_data, logger):
    """Fill the template with data from xrd file.

    Parameters
    ----------
    template : Template[dict]
        Template gnenerated from nxdl definition.
    xrd_data : Dict
        Dictionary from xrd file.
    config_dict : Dict
        Dictionary from config.json or similar file.
    """
    pass

def parse_and_fill_template(template, xrd_file, ext, eln_dict, logger):
    """Parse xrd file and fill the template with data from that file.

    Parameters
    ----------
    template : Template[dict]
        Template gnenerated from nxdl definition.
    xrd_file : str
        Name of the xrd file with extension
    config_dict : Dict
        Dictionary from config.json or similar file.
    eln_dict : Dict
        Plain and '/' separated dictionary from yaml for ELN.
    """

    # Paser xrd file
    if ext == '.rasx':
        xrd_data = read_rigaku_rasx(xrd_file, logger)
    elif ext == '.xrdml':
        xrd_data = read_panalytical_xrdml(xrd_file, logger)
    elif ext == '.brml':
        xrd_data = read_bruker_brml(xrd_file, logger)

    # TODO fill template here
    fill_template(template, xrd_data, logger)
    if eln_dict:
        feed_eln_data_to_template(template, eln_dict. logger)

    return template
