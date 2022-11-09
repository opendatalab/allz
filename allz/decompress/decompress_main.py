import importlib

from allz.defs import (LOG_MODE_NORMAL, COMPRESS_TYPE_COMMAND, COMPRESS_TYPE_KEY_MAPPING, SPLIT_COMPRESS_TYPE_KEY_MAPPING, SPLIT_COMPRESS_TYPE_COMMAND)
from allz.libs.file_type_tester import FileTypeTester


def Decompress(src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False, is_force_mode=False):
    base_package_path = "allz.decompress."
    archive_type_cmd_init = "unar_process"
    archive_type = ""
    archive_type_cmd_key = {}
    is_split_file = False

    # 1.判断压缩类型
    fileTester = FileTypeTester()
    if fileTester.is_archive(src_path):
        # return False, "input compress file type test error, or compress type not supported \n", ""
        res, archive_type = fileTester.is_support_archive_type(src_path)
        # 2-1.遍历配置的压缩类型找到对应的解压命令
        for type_key, type_value in COMPRESS_TYPE_KEY_MAPPING.items():
            if archive_type in type_value:
                archive_type_cmd_init = type_key
                break
        archive_type_cmd_key = COMPRESS_TYPE_COMMAND[archive_type_cmd_init]
    elif fileTester.is_split_volume_archive(src_path)[0]:
        prefix_path = ".".join(str(src_path).split(".")[:-1])
        res, archive_type = fileTester.is_support_archive_type(prefix_path)
        # 2-2.遍历配置的分片压缩类型找到对应的解压命令
        for type_key, type_value in SPLIT_COMPRESS_TYPE_KEY_MAPPING.items():
            if archive_type in type_value:
                archive_type_cmd_init = type_key
                break
        archive_type_cmd_key = SPLIT_COMPRESS_TYPE_COMMAND[archive_type_cmd_init]
        is_split_file = True
    
    process_module = archive_type_cmd_key['process_module']
    process_class = archive_type_cmd_key['process_class']

    # 3.动态调用解压脚本
    unar_module = importlib.import_module(base_package_path + process_module)
    unar_class = getattr(unar_module, process_class)
    unar_instance = unar_class()
    res_status, stderr, stdout = unar_instance.main(src_path, dest_path, log_mode, is_cli, is_force_mode, is_split_file)

    return res_status, stderr, stdout
        

def decompress_cmd_test():
    base_package_path = "allz.decompress."
    can_process_type = []
    cannot_process_type = []

    for cmd_key, cmd_value in COMPRESS_TYPE_COMMAND.items():
        archive_type_cmd_key = COMPRESS_TYPE_COMMAND[cmd_key]
        process_module = archive_type_cmd_key['process_module']
        process_class = archive_type_cmd_key['process_class']

        unar_module = importlib.import_module(base_package_path + process_module)
        unar_class = getattr(unar_module, process_class)
        unar_instance = unar_class()
        res = unar_instance._decompress_test()
        
        if res:
            can_process_type.extend(COMPRESS_TYPE_KEY_MAPPING[cmd_key])
        else:
            cannot_process_type.extend(COMPRESS_TYPE_KEY_MAPPING[cmd_key])

    return list(set(can_process_type)), list(set(cannot_process_type))


if __name__ == '__main__':
    src_path = "MNIST.tar.gz.0000"
    # src_path = "/home/work/srccode/github/allz/test/data/split_src/MNIST.tar.gz.0000"
    dest_path = "/home/work/srccode/github/allz/test/data/split_dest"
    decom = Decompress(src_path, dest_path)
