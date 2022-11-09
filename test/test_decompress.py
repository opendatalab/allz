"""Tests for the decompress module."""
# Standard library imports
import os
import pathlib
from pathlib import Path

from allz.decompress import Decompress
from allz.decompress.bz2_split_process import Bz2SplitProcess
from allz.decompress.gz_split_process import GzSplitProcess
from allz.libs.file_type_tester import FileTypeTester
from allz.decompress.zip_process import ZipProcess

CURRENT_DIR = pathlib.Path(__file__).resolve().parent


def test_zip_process():
    """test unarchive command"""
    print(CURRENT_DIR)
    src_path = Path.joinpath(CURRENT_DIR, "data/source/MNIST.zip")
    dest_path = Path.joinpath(CURRENT_DIR, "data/dest")
    print(src_path, dest_path)

    process = ZipProcess()
    process.main(src_path, dest_path)
    assert Path.exists(dest_path) is True


def test_all_compress_type():
    dest_path_lst = []
    dest_file_name = '000000000001.jpg'
    archive_dir = Path.joinpath(CURRENT_DIR, "data/source")
    dest_dir = Path.joinpath(CURRENT_DIR, "data/dest") 
    for archive_file in os.listdir(archive_dir):
        is_file = os.path.isfile(Path.joinpath(archive_dir, archive_file))
        if is_file:
            src_path = "/".join([str(archive_dir), archive_file])
            dest_path = "/".join([str(dest_dir), archive_file + "#"])
            dest_path_lst.append(dest_path)
            Decompress(src_path, dest_path)

    for dest_path in dest_path_lst:
        assert os.path.exists(dest_path) is True
        type_suffix = ".".join(dest_path.split(".")[1:])
        if type_suffix in ["jpg.bz2#", "jpg.gz#", "jpg.lzma#", "jpg.xz#"]:
            assert os.path.exists(dest_path + os.sep + dest_file_name) is True
        else:
            assert os.path.exists(dest_path + "/MNIST/media/" + dest_file_name) is True


def test_tar_bz_split_process():
    """test unarchive command"""
    src_path = "/home/work/srccode/github/allz/test/data/split_src/MNIST.tar.gz.0000"
    dest_path = "/home/work/srccode/github/allz/test/data/split_dest"
    # src_path = Path.joinpath(CURRENT_DIR, "data/split_src/MNIST.tar.bz.0000")
    # dest_path = Path.joinpath(CURRENT_DIR, "data/dest")
    print(src_path, dest_path)

    # file_tester = FileTypeTester()
    # split_files = file_tester.get_split_volume_archives(src_path)
    process = GzSplitProcess()
    process.main(src_path, dest_path, is_split_file=True)
    assert Path.exists(Path(dest_path)) is True


if __name__ == '__main__':
    # test_zip_process()
    # test_all_compress_type()
    test_tar_bz_split_process()
