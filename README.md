[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/pytest.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools-xrd/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/pynxtools-xrd)
![](https://img.shields.io/pypi/l/pynxtools-xrd)
![](https://img.shields.io/pypi/v/pynxtools-xrd)
![](https://coveralls.io/repos/github/FAIRmat-NFDI/pynxtools_xrd/badge.svg?branch=master)
[![DOI](https://zenodo.org/badge/759916501.svg)](https://doi.org/10.5281/zenodo.16606402)

# A reader for XRD data

## Installation

It is recommended to use python 3.12 with a dedicated virtual environment for this package.
Learn how to manage [python versions](https://github.com/pyenv/pyenv) and
[virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

This package is a reader plugin for [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools) and thus should be installed together with `pynxtools`:


```shell
pip install pynxtools[xrd]
```

for the latest development version.

## Purpose
This reader plugin for [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools) is used to read X-ray diffraction experiment data and metadata and convert these into a NeXus file (HDF5 file with extension .nxs)
according to the [NeXus](https://github.com/FAIRmat-NFDI/nexus_definitions) application definition [NXxrd_pan](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXxrd_pan.nxdl.xml). 
Specifically, the plugin maps data and metadata from `.xrdml` files that were obtained with PANalytical X'Pert PRO version 1.5 (instruments).

## Status quo
This reader is considered in development.

## Contact person in FAIRmat for this reader
Rubel Mozumder
Markus Kühbach

## How to cite this work
Mozumder, R., Shabih, S., Kühbach, M., Pielsticker, L. & Brockhauser, S. (2025). pynxtools-xrd: A pynxtools reader plugin for X-ray diffraction data. Zenodo. https://doi.org/10.5281/zenodo.16606403
