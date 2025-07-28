[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/pytest.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/pynxtools-xrd)
![](https://img.shields.io/pypi/l/pynxtools-xrd)
![](https://img.shields.io/pypi/v/pynxtools-xrd)
![](https://coveralls.io/repos/github/FAIRmat-NFDI/pynxtools_xrd/badge.svg?branch=master)

# XRD Reader
With the XRD reader, data from X-ray diffraction experiment can be read and written into a NeXus file (h5 type file with extension .nxs) according to NXxrd_pan application definition in [NeXus](https://github.com/FAIRmat-NFDI/nexus_definitions). There are a few different methods of measuring XRD: 1. θ:2θ instruments (e.g. Rigaku H3R), and 2. θ:θ instrument (e.g. PANalytical X’Pert Pro). The goal with this reader is to support both of these methods.

**NOTE: This reader is still under development. As of now, the reader can only handle files with the extension `.xrdml` , obtained with PANalytical X’Pert Pro version 1.5 (method 2 described above). Currently we are wtoking to include more file types and file versions.**

# Installation

It is recommended to use python 3.11 with a dedicated virtual environment for this package.
Learn how to manage [python versions](https://github.com/pyenv/pyenv) and
[virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

This package is a reader plugin for [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools) and thus should be installed together with `pynxtools`:


```shell
pip install pynxtools[xrd]
```

for the latest development version.

## Parsers
Though, in computer science, parser is a process that reads code into smaller parts (called tocken) with relations among tockens in a tree diagram. The process helps compiler to understand the tocken relationship of the source code.

The XRD reader calls a program or class (called parser) that reads the experimenal input file and re-organises the different physical/experiment concepts or properties in a certain structure which is defined by developer.

### class pynxtools.dataconverter.readers.xrd.xrd_parser.XRDMLParser

    **inputs:**
        file_path: Full path of the input file.

    **Important method:**
        get_slash_separated_xrd_dict() -> dict

        This method can be used to check if all the data from the input file have been read or not, it returns the slash separated dict as described.

### How To
The reader can be run from Jupyter-notebook or Jupyter-lab with the following command:

```sh
 ! dataconverter \
--reader xrd \
--nxdl NXxrd_pan \
$<xrd-file location> \
$<eln-file location> \
--output <output-file location>.nxs
```

An example file can be found here in GitLab in [nomad-remote-tools-hub](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/xrd) feel free to vist and try out the reader.

# Contributing

## Development install

Install the package with its dependencies:

```shell
git clone https://github.com/FAIRmat-NFDI/pynxtools-xrd.git \\
    --branch main \\
    --recursive pynxtools_xrd
cd pynxtools_xrd
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e ".[dev]"
```

There is also a [pre-commit hook](https://pre-commit.com/#intro) available
which formats the code and checks the linting before actually commiting.
It can be installed with
```shell
pre-commit install
```
from the root of this repository.

## Contact person in FAIRmat
In principle, you can reach out to any member of Area B of the FAIRmat consortium, but Rubel Mozumder could be more reasonable for the early response.
