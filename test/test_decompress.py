"""Tests for the decompress module."""
# Standard library imports
import os
import pathlib
from pathlib import Path

from allz.decompress.decompress_main import DecompressMain
from allz.decompress.gz_split_process import GzSplitProcess
from allz.decompress.zip_process import ZipProcess
from allz.libs.file_type_tester import FileTypeTester

CURRENT_DIR = pathlib.Path(__file__).resolve().parent


def test_single_zip_process():
    """Normal single compressed file test"""
    print(CURRENT_DIR)
    src_path = Path.joinpath(CURRENT_DIR, "data/source/MNIST.zip")
    dest_path = Path.joinpath(CURRENT_DIR, "data/dest")

    process = ZipProcess()
    process.main(src_path, dest_path)
    assert Path.exists(dest_path) is True


def test_all_normal_compress_type():
    """
    Normal decompress function test
    it will decompress all compressed files in directory data/source to data/dest
    """
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
            de_main = DecompressMain()
            de_main.Decompress(src_path, dest_path)

    for dest_path in dest_path_lst:
        assert os.path.exists(dest_path) is True
        type_suffix = ".".join(dest_path.split(".")[1:])
        if type_suffix in ["jpg.bz2#", "jpg.gz#", "jpg.lzma#", "jpg.xz#"]:
            assert os.path.exists(dest_path + os.sep + dest_file_name) is True
        else:
            assert os.path.exists(dest_path + "/MNIST/media/" + dest_file_name) is True


def test_absolute_path_split_process():
    """
    Split single compressed file test
    src_path and dest_path use the absolute path
    """
    src_path = "/home/work/srccode/github/allz/test/data/split_src/MNIST.tar.gz.0000"
    dest_path = "/home/work/srccode/github/allz/test/data/split_dest/"
    # src_path = Path.joinpath(CURRENT_DIR, "data/split_src/MNIST.tar.bz.0000")
    # dest_path = Path.joinpath(CURRENT_DIR, "data/dest")
    print(src_path, dest_path)

    file_tester = FileTypeTester()
    split_files = file_tester.get_split_volume_archives(src_path)
    assert len(split_files) == 2

    process = GzSplitProcess()
    process.main(src_path, dest_path, is_split_file=True)
    assert Path.exists(Path(dest_path + os.sep + "MNIST")) is True


def test_relative_path_split_process():
    """
    Split single compressed file test
    src_path and dest_path use the relative path
    """
    src_path = "MNIST.tar.gz.0000"
    dest_path = "../split_dest"
    target_path = Path("/home/work/srccode/github/allz/test/data/split_src/")
    os.chdir(target_path)

    file_tester = FileTypeTester()
    split_files = file_tester.get_split_volume_archives(src_path)
    assert len(split_files) == 2

    process = GzSplitProcess()
    process.main(src_path, dest_path, is_split_file=True)
    assert Path.exists(Path(dest_path + os.sep + "MNIST")) is True


if __name__ == '__main__':
    # test_single_zip_process()
    # test_all_normal_compress_type()
    # test_absolute_path_split_process()
    test_relative_path_split_process()
