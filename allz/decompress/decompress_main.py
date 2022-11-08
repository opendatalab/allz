import importlib

from allz.defs import (LOG_MODE_NORMAL, COMPRESS_TYPE_COMMAND, COMPRESS_TYPE_KEY_MAPPING)
from allz.libs.file_type_tester import FileTypeTester


def Decompress(src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False, is_force_mode=False):
    base_package_path = "allz.decompress."

    # 1.判断压缩类型
    fileTester = FileTypeTester()
    is_archive = fileTester.is_archive(src_path)
    if not is_archive:
        return False, "input compress file type test error, or compress type not supported \n", ""

    res, archive_type = fileTester.is_support_archive_type(src_path)
    # 2.遍历配置的压缩类型找到对应的解压命令
    archive_type_cmd_init = "unar_process"
    for type_key, type_value in COMPRESS_TYPE_KEY_MAPPING.items():
        if archive_type in type_value:
            archive_type_cmd_init = type_key
            break
    
    archive_type_cmd_key = COMPRESS_TYPE_COMMAND[archive_type_cmd_init]
    process_module = archive_type_cmd_key['process_module']
    process_class = archive_type_cmd_key['process_class']

    # 3.动态调用解压脚本
    unar_module = importlib.import_module(base_package_path + process_module)
    unar_class = getattr(unar_module, process_class)
    unar_instance = unar_class()
    res_status, stderr, stdout = unar_instance.main(src_path, dest_path, log_mode, is_cli, is_force_mode)

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
