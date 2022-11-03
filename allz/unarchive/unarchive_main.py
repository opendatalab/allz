import importlib

from allz.defs import (LOG_MODE_NORMAL, UNARCHIVE_TYPE_COMMAND, UNARCHIVE_TYPE_KEY_MAPPING)
from allz.libs.unarchive_tester import ArchiveTypeTester


def Unarchive(src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
    base_package_path = "allz.unarchive."

    # 1.判断压缩类型
    archiveTester = ArchiveTypeTester()
    is_archive = archiveTester.is_archive(src_path)
    if not is_archive:
        return False, "input compress file type test error, or compress type not supported", ""

    res, archive_type = archiveTester.is_support_archive_type(src_path)
    # 2.遍历配置的压缩类型找到对应的解压命令
    archive_type_cmd_init = "unar_process"
    for type_key, type_value in UNARCHIVE_TYPE_KEY_MAPPING.items():
        if archive_type in type_value:
            archive_type_cmd_init = type_key
            break
    
    archive_type_cmd_key = UNARCHIVE_TYPE_COMMAND[archive_type_cmd_init]
    process_module = archive_type_cmd_key['process_module']
    process_class = archive_type_cmd_key['process_class']

    # 3.动态调用解压脚本
    unar_module = importlib.import_module(base_package_path + process_module)
    unar_class = getattr(unar_module, process_class)
    unar_instance = unar_class()
    res_status, stderr, stdout = unar_instance.main(src_path, dest_path, log_mode, is_cli)

    return res_status, stderr, stdout
        

def decompress_cmd_test():
    base_package_path = "allz.unarchive."
    can_process_type = []
    cannot_process_type = []

    for cmd_key, cmd_value in UNARCHIVE_TYPE_COMMAND.items():
        archive_type_cmd_key = UNARCHIVE_TYPE_COMMAND[cmd_key]
        process_module = archive_type_cmd_key['process_module']
        process_class = archive_type_cmd_key['process_class']

        unar_module = importlib.import_module(base_package_path + process_module)
        unar_class = getattr(unar_module, process_class)
        unar_instance = unar_class()
        res = unar_instance._decompress_test()
        
        if res:
            can_process_type.extend(UNARCHIVE_TYPE_KEY_MAPPING[cmd_key])
        else:
            cannot_process_type.extend(UNARCHIVE_TYPE_KEY_MAPPING[cmd_key])

    return list(set(can_process_type)), list(set(cannot_process_type))
