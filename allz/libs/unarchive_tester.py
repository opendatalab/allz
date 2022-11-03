import os
import re

from allz.defs import UNARCHIVE_FILE_TYPES


class ArchiveTypeTester():
    """
    压缩文件判断器
    """
    def __init__(self):
        super().__init__()
        self.archive_file_type = UNARCHIVE_FILE_TYPES
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
