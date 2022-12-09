"""Tests for the decompress module."""
# Standard library imports
import os
import pathlib
from pathlib import Path

from allz.decompress.decompress_main import DecompressMain
from allz.decompress.gz_split_process import GzSplitProcess
# from allz.decompress.tar_7z_split_process import Tar7zSplitProcess
from allz.decompress.rar_split_process import RarSplitProcess
from allz.decompress.zip_process import ZipProcess
from allz.libs.file_type_tester import FileTypeTester

CURRENT_DIR = pathlib.Path(__file__).resolve().parent


def test_singel_file_normal_process():
    """Normal single compressed file test"""
    print(CURRENT_DIR)
    src_path = Path.joinpath(CURRENT_DIR, "data/source/MNIST.zip")
    dest_path = Path.joinpath(CURRENT_DIR, "data/dest")

    process = ZipProcess()
    process.main(src_path, dest_path)
    assert Path.exists(dest_path) is True


def test_single_file_recursive_path_process():
    """Normal single compressed file
    decompress file to recursively path, like 11/22/33
    """
    print(CURRENT_DIR)
    src_path = Path.joinpath(CURRENT_DIR, "data/source/MNIST.zip")
    dest_path = Path.joinpath(CURRENT_DIR, "data/dest/11/22/33")

    process = ZipProcess()
    process.main(src_path, dest_path)
    assert Path.exists(dest_path) is True


def test_all_files_normal_files():
    """
    Normal decompress function test
    it will decompress all compressed files in directory data/source to data/dest
    """
    dest_path_lst = []
    dest_file_name = '000000000001.jpg'
    archive_dir = Path.joinpath(CURRENT_DIR, "data/source")
    dest_dir = Path.joinpath(CURRENT_DIR, "data/dest")
    for archive_file in os.listdir(archive_dir):
        if os.path.isfile(Path.joinpath(archive_dir, archive_file)):
            src_path = "/".join([str(archive_dir), archive_file])
            dest_path = "/".join([str(dest_dir), f"{archive_file}#"])
            dest_path_lst.append(dest_path)
            de_main = DecompressMain()
            de_main.Decompress(src_path, dest_path)

    for dest_path in dest_path_lst:
        assert os.path.exists(dest_path) is True
        type_suffix = ".".join(dest_path.split(".")[1:])
        if type_suffix in {"jpg.bz2#", "jpg.gz#", "jpg.lzma#", "jpg.xz#", "jpg.gzip#"}:
            assert os.path.exists(dest_path + os.sep + dest_file_name) is True
        else:
            assert os.path.exists(f"{dest_path}/MNIST/media/{dest_file_name}") is True


def test_absolute_path_split_process():
    """
    Split single compressed file test
    src_path and dest_path use the absolute path
    """
    src_path = str(Path.joinpath(CURRENT_DIR, "data/split_src/MNIST.part1.rar"))
    dest_path = str(Path.joinpath(CURRENT_DIR, "data/split_dest"))
    print(src_path, dest_path)

    file_tester = FileTypeTester()
    split_files = file_tester.get_split_volume_compressed_file_path_list(src_path)
    assert len(split_files) == 4

    process = RarSplitProcess()
    process.main(src_path, dest_path, is_split_file=True)
    assert Path.exists(Path(dest_path + os.sep + "MNIST")) is True


def test_relative_path_split_process():
    """
    Split single compressed file test
    src_path and dest_path use the relative path
    """
    src_path = "MNIST.tar.gz.0000"
    dest_path = "../split_dest"
    target_path = Path.joinpath(CURRENT_DIR, "data/split_src")
    os.chdir(target_path)

    file_tester = FileTypeTester()
    split_files = file_tester.get_split_volume_compressed_file_path_list(src_path)
    assert len(split_files) == 2

    process = GzSplitProcess()
    process.main(src_path, dest_path, is_split_file=True)
    assert Path.exists(Path(dest_path + os.sep + "MNIST")) is True


def test_all_files_split_process():
    """
    Split decompress function test
    it will decompress all split compressed files in directory data/split_src to data/split_dest
    """
    dest_path_lst = []
    dest_file_name = '000000000001.jpg'
    split_src_dir = Path.joinpath(CURRENT_DIR, "data/split_src")
    split_dest_dir = Path.joinpath(CURRENT_DIR, "data/split_dest") 

    for archive_file in os.listdir(split_src_dir):
        if os.path.isfile(Path.joinpath(split_src_dir, archive_file)):
            if ".tar.7z." in archive_file and not str(archive_file).endswith(".001"):
                continue

            src_path = "/".join([str(split_src_dir), archive_file])
            dest_path = "/".join([str(split_dest_dir), f"{archive_file}#"])
            dest_path_lst.append(dest_path)
            de_main = DecompressMain()
            de_main.Decompress(src_path, dest_path)
    for dest_path in dest_path_lst:
        assert os.path.exists(dest_path) is True

        assert os.path.exists(f"{dest_path}/MNIST/media/{dest_file_name}") is True


def test_split_volumn_return_path():
    """
    Split decompress function test.
    It will return the list of split volumn files path that match the input src_path file.
    """
    src_path = "./MNIST.tar.0001"
    # src_path = "./MNIST.tar.gz.0000"
    target_path = Path.joinpath(CURRENT_DIR, "data/split_src")
    os.chdir(target_path)
    file_tester = FileTypeTester()
    res_lst = file_tester.get_split_volume_compressed_file_path_list(src_path)
    
    assert len(res_lst) == 8


def test_all_return_path():
    """
    Split decompress function test.
    If the input src_path is a normal compressed file, it will return the src_path, 
    else if it is a split volumn file, it will return the list of split volumn files path that match the input src_path file.
    """
    src_path = "./MNIST.tar.0001"
    target_path = Path.joinpath(CURRENT_DIR, "data/split_src")
    os.chdir(target_path)
    file_tester = FileTypeTester()
    res_lst = file_tester.get_all_compressed_file_path_list(src_path)
    
    assert len(res_lst) > 0


def test_split_regex_match():
    file_lst = ["MNIST.tar.0000", "MNIST.tar.0001", "MNIST.tar.0002", "MNIST.tar.0003", "MNIST.tar.0004", "MNIST.tar.7z.001", "MNIST.tar.7z.002", 
                "MNIST.part1.rar", "MNIST.part2.rar", "MNIST.part3.rar", "MNIST.part4.rar", "MNIST.7z.001", "MNIST.7z.002", "123.rar", "abc.zip", 
                "abc", "000", "0000.tar", "02287.txt", "NLST_CT.tar.gz.part0000", "NLST_CT.tar.gz.part0001", "NLST_CT.tar.gz.part0002"]

    tester = FileTypeTester() 
    res_lst = tester.get_compressed_files_classify_lst(file_lst)

    assert len(res_lst) == 8


def test_with_path_split_regex_match():
    file_lst = ["/home/work/srccode/github/allz/allz/libs/MNIST.tar.0000", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.0001", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.0002",
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.0003",
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.0004",
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.7z.001",
                "/home/work/srccode/github/allz/allz/libs/MNIST.tar.7z.002", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.part1.rar", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.part2.rar", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.part3.rar", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.part4.rar", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.7z.001", 
                "/home/work/srccode/github/allz/allz/libs/MNIST.7z.002",
                "/home/work/srccode/github/allz/allz/libs/NLST_CT.tar.gz.part0000",
                "/home/work/srccode/github/allz/allz/libs/NLST_CT.tar.gz.part0001",
                "/home/work/srccode/github/allz/allz/libs/NLST_CT.tar.gz.part0002",
                "/home/work/srccode/github/allz/allz/libs/NLST_CT.tar.gz.part0003",
                "/home/work/srccode/github/allz/allz/libs/123.rar",
                "/home/work/srccode/github/allz/allz/libs/acb",
                "/home/work/srccode/github/allz/allz/libs/0000",
                "/home/work/srccode/github/allz/allz/libs/02287.txt",
                "/home/work/srccode/github/allz/allz/libs/000.tar",
                "/home/work/srccode/github/allz/allz/libs/123.jpg"]

    tester = FileTypeTester() 
    res_lst = tester.get_compressed_files_classify_lst(file_lst)

    assert len(res_lst) == 7


if __name__ == '__main__':
    # test_singel_file_normal_process()
    # test_single_file_recursive_path_process()
    # test_all_files_normal_files()

    # test_absolute_path_split_process()
    # test_relative_path_split_process()
    # test_all_files_split_process()

    test_split_volumn_return_path()
    # test_all_return_path()

    # test_split_regex_match()
    # test_with_path_split_regex_match()
