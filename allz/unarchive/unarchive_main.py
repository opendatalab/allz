import importlib

from allz.defs import (LOG_MODE, UNARCHIVE_TYPE_COMMAND, UNARCHIVE_TYPE_KEY_MAPPING)
from allz.libs.common import get_logger
from allz.libs.unarchive_tester import ArchiveTypeTester


def Unarchive(src_path, dest_path, log_mode=LOG_MODE):
    base_package_path = "allz.unarchive."

    # 1.判断压缩类型
    archiveTester = ArchiveTypeTester()
    is_archive = archiveTester.is_archive(src_path)
    if not is_archive:
        return "input compress file type test error"

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
    stderr = unar_instance.main(src_path, dest_path, log_mode)

    return str(stderr).strip()
        

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
            

if __name__ == '__main__':
    mylogger = get_logger("main")
    # 0. 接收arg_parser输入参数
    # args = arg_parser()
    # main(args.src_path, args.dest_path)

    # 1.本地测试
    src_path = "/mnt/unarchive_dataset_tmp/A3D/compress/temp/jumpcutter-master.tar.bz"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/compress/temp/jumpcutter-master.tar.bz#"
    status = Unarchive(src_path, dest_path)
    print(status)

    # 2.完整压缩包测试
    # dest_path_lst = []
    # dest_file_name = 'jumpcutter.py'
    # archive_dir = "/mnt/unarchive_dataset_tmp/A3D/compress"
    # for archive_file in os.listdir(archive_dir):
    #     is_file = os.path.isfile(archive_dir + os.sep + archive_file)
    #     if is_file:
    #         src_path = "/".join([archive_dir, archive_file])
    #         dest_path = "/".join([archive_dir, archive_file + "#"])
    #         dest_path_lst.append(dest_path)
    #         # print(archive_file, src_path, dest_path)
    #         Unarchive(src_path, dest_path)

    # # 2.1 测试压缩包是否解压成功
    # for dest_path in dest_path_lst:
    #     if os.path.exists(dest_path):
    #         if not os.path.exists(dest_path + "/jumpcutter-master/" + dest_file_name):
    #             print(str(dest_path) + f"路径下, 解压文件 {dest_file_name} 不存在")
    #     else:
    #         print(str(dest_path) + ", 路径不存在")

    # 3.压缩类型test
    # can, cannot = decompress_cmd_test()
    # print(can)
    # print(cannot)
