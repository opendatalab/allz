import os
import pathlib
import re

from allz.defs import COMPRESS_FILE_TYPES, SPLIT_COMPRESS_FILE_TYPES

CURRENT_DIR = pathlib.Path(__file__).resolve().parent


class FileTypeTester():
    """
    压缩文件判断器
    """
    def __init__(self):
        super().__init__()
        self.archive_file_type = COMPRESS_FILE_TYPES
        self.split_archive_file_type = SPLIT_COMPRESS_FILE_TYPES
        self._init_ext_regex()
        # self.split_volume_match_regex = r".*\d{3,4}$"
        self.split_volume_search_regex = r"\d{2,4}$"
        self.rar_split_volumn_match_regex = r".*.part\d{1,4}.rar$"
        self.rar_split_volumn_search_regex = r".part\d{1,4}.rar$"

    def _init_ext_regex(self):
        if len(self.archive_file_type) == 0:
            raise Exception("archive_file_type is not configured")
        exts = [ext.strip(".\r\n").replace(".", "\\.") for ext in self.archive_file_type]
        split_exts = [ext.strip(".\r\n").replace(".", "\\.") for ext in self.split_archive_file_type]

        self.ext_regex = re.compile(".+\\.(" + "|".join(exts) + ")$")
        self.split_volume_match_regex = re.compile("(.+\\.(" + "|".join(split_exts) + ")\\..*\\d{2,4}$)|(.+\\.part\\d{1,4}\\.rar$)")

    def is_normal_compressed_file(self, file_path):
        if self._is_rar_split_volume_compressed_file(file_path):
            return False
        else:
            return self.ext_regex.match(file_path) is not None

    def is_split_volume_compressed_file(self, file_path):
        to_replace = ""
        if self._is_rar_split_volume_compressed_file(file_path):
            matches = re.search(self.rar_split_volumn_search_regex, file_path)
            to_replace = ".part"
        else:
            matches = re.search(self.split_volume_search_regex, file_path)
        
        if matches:
            return True, matches.group().replace(to_replace, "")
        else:
            return False, None
    
    def is_split_volume_compressed_file_regex(self, file_path):
        return re.compile(self.split_volume_match_regex).match(file_path) is not None

    def find_split_volume_compressed_file_list(self, file_path, file_lst):
        is_archive, suffix_str = self.is_split_volume_compressed_file(file_path)
        similar_archive_list = []
        if is_archive and suffix_str:
            prefix_path = str(file_path).rstrip("/").split("/")[-1][:-len(suffix_str)]
            similar_archive_list.extend(file for file in file_lst if str(file)[: -len(suffix_str)] == prefix_path)

        return similar_archive_list
    
    def _get_normal_compressed_type_suffix(self, file_path):
        path_splits = str(file_path).rstrip(".").split(".")
        suffix_last_one = f".{path_splits[-1]}"
        suffix_last_two = "." + ".".join(path_splits[-2:])

        return suffix_last_two, suffix_last_one
    
    def is_support_normal_compressed_type(self, file_path):
        suffix_last_two, suffix_last_one = self._get_normal_compressed_type_suffix(file_path)
        if suffix_last_two in self.archive_file_type:
            return True, suffix_last_two
        elif suffix_last_one in self.archive_file_type:
            return True, suffix_last_one

        return False, None
    
    def get_split_volume_compressed_file_path_list(self, file_path):
        is_archive, suffix_str = self.is_split_volume_compressed_file(file_path)
        similar_archive_list = []
        if is_archive and suffix_str:
            prefix_path = str(file_path).rstrip("/").split("/")[-1][:-len(suffix_str)]
            current_dir = "/".join(str(file_path).split("/")[:-1])
            if "/" not in file_path:
                current_dir = "./"
            current_file_list = [ar_file for ar_file in os.listdir(current_dir) if os.path.isfile(current_dir + "/" + ar_file)]
            for file in current_file_list:
                if self.is_split_volume_compressed_file(current_dir + "/" + file)[0] and (str(file)[:-len(suffix_str)] == prefix_path):
                    similar_archive_list.append("/".join([current_dir, file]))

        return similar_archive_list

    def get_all_compressed_file_path_list(self, file_path):
        rtn_file_path_lst = []
        if self.is_normal_compressed_file(file_path):
            rtn_file_path_lst.append(file_path)
        elif self.is_split_volume_compressed_file(file_path)[0]:
            rtn_file_path_lst.extend(self.get_split_volume_compressed_file_path_list(file_path))
        
        return rtn_file_path_lst

    def _is_rar_split_volume_compressed_file(self, file_path):
        return re.compile(self.rar_split_volumn_match_regex).match(file_path) is not None

    def get_compressed_files_classify_lst(self, file_lst):
        base_path = ""
        if len(file_lst) < 1:
            return [[]]

        result_lst = []
        raw_file_lst = []
        tmp_file_lst = []
        for file in file_lst:
            if "/" not in file:
                raw_file_lst = file_lst
                break
            if base_path == "":
                base_path = os.path.split(file)[0]
            raw_file_lst.append(os.path.split(file)[1])

        for file_name in raw_file_lst:
            if file_name in sum(tmp_file_lst, []):
                continue
            if self.is_normal_compressed_file(file_name):
                compressed_file_lst = ["/".join([base_path, file_name])]
                result_lst.append(compressed_file_lst)
                tmp_file_lst.append(compressed_file_lst)
            elif self.is_split_volume_compressed_file_regex(file_name):
                left_lst = list(set(raw_file_lst) - set(sum(tmp_file_lst, [])))
                match_lst = self.find_split_volume_compressed_file_list(file_name, left_lst)
                result_lst.append(["/".join([base_path, item]) for item in match_lst])
                tmp_file_lst.append(match_lst)

        return result_lst
