"""
Basic example based test for the stm reader
"""

import os

import pytest
from pynxtools.testing.nexus_conversion import ReaderTest

# e.g. module_dir = /pynxtools-foo/tests
module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        ("NXxrd_pan", "xrd", f"{module_dir}/../tests/data/xrdml_918-16_10"),
    ],
)
def test_xrd_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    """Test for the XRD reader plugin.

    Parameters
    ----------
    nxdl : str
        Name of the NXDL application definition that is to be tested by
        this reader plugin without the file ending .nxdl.xml.
    reader_name : str
        Name of the class of the reader )
    files_or_dir : class
        Name of the class of the reader.
    tmp_path : pytest.fixture
        Pytest fixture variable, used to create temporary file and clean up the generated files
        after test.
    caplog : pytest.fixture
        Pytest fixture variable, used to capture the log messages during the test.
    """
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    # Use `ignore_undocumented` to skip undocumented fields
    # test.convert_to_nexus(ignore_undocumented=True)
    test.check_reproducibility_of_nexus()
