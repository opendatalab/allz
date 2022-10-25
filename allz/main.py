# import configparser
# import os.path
# from pathlib import Path
import importlib
import os

from allz.defs import (UNARCHIVE_TYPE_COMMAND, UNARCHIVE_TYPE_KEY_MAPPING)
# from uncompress_process.defs import DAEMON_PROCESS
from allz.libs.argparser import arg_parser
from allz.libs.common import get_logger
from allz.unarchive_tester import ArchiveTypeTester

# import click


# from loguru import logger


# @click.command()
# @click.option('--config-path', default="./uncompress_type.ini", help='配置文件路径')
def main(src_path, dest_path):
    mylogger.info("解压程序已启动")
    # 1.判断压缩类型
    archiveTester = ArchiveTypeTester()
    is_archive = archiveTester.is_archive(src_path)
    if is_archive:
        res, archive_type = archiveTester.is_support_archive_type(src_path)
        # 2.遍历配置的压缩类型找到对应的解压命令
        archive_type_cmd_key = "unar_process"
        for type_key, type_value in UNARCHIVE_TYPE_KEY_MAPPING.items():
            if archive_type in type_value:
                archive_type_cmd_key = type_key
                break
        
        archive_type_cmd_value = UNARCHIVE_TYPE_COMMAND[archive_type_cmd_key]
        process_module = archive_type_cmd_value['process_module']
        process_class = archive_type_cmd_value['process_class']

        # 3.动态调用解压脚本
        unar_module = importlib.import_module(process_module)
        unar_class = getattr(unar_module, process_class)
        unar_instance = unar_class()
        unar_instance.main(src_path, dest_path)


if __name__ == '__main__':
    mylogger = get_logger("main")
    # 0. 接收arg_parser输入参数
    # args = arg_parser()
    # main(args.src_path, args.dest_path)

    # 1.本地测试
    # src_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz2"
    # dest_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz2#"
    # main(src_path, dest_path)

    # 2.完整压缩包测试
    dest_path_lst = []
    dest_file_name = 'jumpcutter.py'
    archive_dir = "/mnt/unarchive_dataset_tmp/A3D/compress"
    for archive_file in os.listdir(archive_dir):
        is_file = os.path.isfile(archive_dir + os.sep + archive_file)
        if is_file:
            src_path = "/".join([archive_dir, archive_file])
            dest_path = "/".join([archive_dir, archive_file + "#"])
            dest_path_lst.append(dest_path)
            # print(archive_file, src_path, dest_path)
            main(src_path, dest_path)

    # 2.1 测试压缩包是否解压成功
    for dest_path in dest_path_lst:
        if os.path.exists(dest_path):
            if not os.path.exists(dest_path + "/jumpcutter-master/" + dest_file_name):
                print(str(dest_path) + f"路径下, 解压文件 {dest_file_name} 不存在")
        else:
            print(str(dest_path) + ", 路径不存在")
