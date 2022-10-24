import os
import re
from subprocess import DEVNULL, PIPE, Popen

from loguru import logger


class ArchiveTypeTester():
    """
    判断文件是否为压缩文件
    """
    def __init__(self):
        self.archive_file_type: str = ".7z .tar .tar.bz2 .tar.gz .tar.lzma .tar.xz .rar .tgz .bz2 .gz .lzma .xz .zip"
        self._init_ext_regex()
        self.split_volume_archive = "\\d{2,3}$"

    def _init_ext_regex(self):
        if len(self.archive_file_type) == 0:
            raise Exception("archive_file_type is not configured")
        exts = []
        for ext in self.archive_file_type:
            exts.append(ext.strip(".\r\n").replace(".", "\\."))
        self.ext_regex = re.compile(".+\\.(" + "|".join(exts) + ")$")

    def is_archive(self, file_path):
        return self.ext_regex.match(file_path) is not None

    def is_split_volume_archive(self, file_path):
        matches = re.search(self.split_volume_archive, file_path)
        if matches:
            return True, matches.group()
        else:
            return False, None
    
    def _get_archive_type(self, file_path):
        path_splits = str(file_path).strip().split(".")
        suffix_last_two = "." + path_splits[-1]
        suffix_last_one = "." + ".".join(path_splits[-2: len(path_splits)])

        return suffix_last_two, suffix_last_one
    
    def is_support_archive_type(self, file_path):
        suffix_last_two, suffix_last_one = self._get_archive_type(file_path)
        print(suffix_last_two, suffix_last_one)
        if suffix_last_two in self.archive_file_type:
            return True, suffix_last_two
        elif suffix_last_one in self.archive_file_type:
            return True, suffix_last_one

        return False, None

    def get_split_volume_archives(self, file_path):
        is_archive, suffix_str = self.is_split_volume_archive(file_path)
        similar_archive_list = []
        if is_archive and suffix_str:
            prefix_path = str(file_path).strip("/").split("/")[-1][:-len(suffix_str)]
            current_dir = "/".join(str(file_path).split("/")[:-1])
            current_file_list = [ar_file for ar_file in os.listdir(current_dir) if os.path.isfile(current_dir + "/" + ar_file)]
            for file in current_file_list:
                if self.is_split_volume_archive(current_dir + "/" + file)[0] and (str(file)[:-len(suffix_str)] == prefix_path):
                    similar_archive_list.append(file)

        return similar_archive_list


class UncompressArchive():
    def __init__(self):
        super().__init__()
        # self.node_name = self.args.node_name
        # self.disk_temp_dir = self.args.disk_temp_dir.rstrip("/")
        # self.unarchive_thread_cnt = self.args.unarchive_thread_cnt
        # self.unarchive_succ_delay = self.args.unarchive_succ_delay
        self.archive_file_type = ".7z .tar .tar.bz2 .tar.gz .tar.lzma .tar.xz .rar .tgz .bz2 .gz .lzma .xz .zip"

    def unzip(self, dest_path, src_path):
        cmd = ["unar", "-q", "-D", "-o", dest_path, src_path]
        logger.info(f"开始执行解压命令：{cmd}  解压到本地的目录dest_path: {dest_path}   zip文件路径src_path: {src_path}")
        p = Popen(cmd, stdout=DEVNULL, stderr=PIPE, encoding="utf-8")
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception(f"解压程序失败, cmd={cmd}, err=[{stderr}]")
    
    def get_archive_type(self, file_path):
        cmd = ["file", file_path]
        p = Popen(cmd, stdout=DEVNULL, stderr=PIPE, encoding="utf-8")
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception(f"压缩文件类型异常, cmd={cmd}, err=[{stderr}]")
        
        output_str = str(stdout).lower()
        output_splits = output_str.split(" ")
        if len(output_splits) >= 2:
            archive_type = output_splits[1]

        if "empty" in output_str:
            return False
        elif "tar" in output_str:
            # 纯tar打包文件
            pass
        elif "compress" in output_str:
            # 使用tar打包后压缩
            pass
        else:
            pass


def main():
    uncompress = UncompressArchive()
    dest_path = "/home/work/srccode/allz/data"
    src_path = "/home/work/srccode/allz/data/RapidEEx64.zip"
    uncompress.unzip(dest_path, src_path)

    # 1.获取输入的文件，判断是否是压缩文件，判断是否是分片文件
    # 2.判断压缩文件类型，使用对应的解压工具进行解压. 文件类型有1个点结尾和2个点结尾的，2个点结尾的都是使用tar包方式打包再压缩的
    # 3.如果是tar文件，定义解压方式


if __name__ == "__main__":
    # main()
    file_path = "/mnt/unarchive_dataset_tmp/A3D/7z_test/jumpcutter-master.tar.7z.001"
    test = ArchiveTypeTester()
    # is_split, path = test.is_split_volume_archive(file_path)
    # print(is_split, path)

    lst = test.get_split_volume_archives(file_path)
    for file in lst:
        print(file)
