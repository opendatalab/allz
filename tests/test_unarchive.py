"""Tests for the reader.feed module."""
# Standard library imports
import pathlib
import os

# Third party imports
import pytest

# tar_bz_process imports
from allz.unarchive.tar_bz_process import TarBzProcess

# Current directory
HERE = pathlib.Path(__file__).resolve().parent


def test_tar_bz_process():
    """test unarchive command"""
    src_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz#"

    process = TarBzProcess()
    process.main(src_path, dest_path)
    assert os.path.exists(str(dest_path) + "/jumpcutter-master") is True


if __name__ == '__main__':
    test_tar_bz_process()
