# Convert X-ray powder diffraction data and metadata to NeXus

## Who is this tutorial for?

This document is for X-ray diffraction scientists who want to standardize their research data by converting these into a NeXus standardized format.

## What should you know before this tutorial?

- You should have a basic understanding of [NeXus and FAIRmat's contribution to NeXus](https://github.com/FAIRmat-NFDI/nexus_definitions) and [`pynxtools`](https://github.com/FAIRmat/pynxtools)

## What you will know at the end of this tutorial?

You will have a basic understanding how to use pynxtools-xrd for converting XRD data to a NeXus/HDF5 file.

## Steps

### Installation

See [the installation tutorial](installation.md) for how to install pynxtools together with the XRD reader plugin.

### Running the reader from the command line

An example script to run the XRD reader in `pynxtools`:

```console
user@box:~$ dataconverter $<xrd-file path> $<eln-file path> --reader xrd --nxdl NXxrd_pan --output <output-file path>.nxs
```

You can find an example `.xrdml` file in `tests/data/xrdml_918-16_10`.

**Congrats! You now have a NeXus file!**

