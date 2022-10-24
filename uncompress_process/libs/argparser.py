import argparse

from uncompress_process.defs import LOG_LEVEL


class ArgParser(object):
    """
    参数解析
    """
    def __init__(self, ):
        parser = argparse.ArgumentParser(description='压缩包解压参数解析')
        parser.add_argument("--archive-file-type", nargs="*", default='.tar .gz .tar.bz2 .tar.bz .zip .7z .tar.lz .tar.lzma .tar.lzo .tar.z .xz'.split(), type=list, help="系统可以解压的压缩文件后缀，例如zip,tgz,tar,tar.gz")
        parser.add_argument("--archive-type", nargs="?", default='unar', type=str, help="默认的压缩包类型，统一使用unar进行解压")
        parser.add_argument("--unar-cmd", nargs="?", default='unar -q -D -o', type=str, help="压缩包解压命令，从指定的src_path解压到dest_path目录")
        parser.add_argument("--src-path", nargs="?", default='/mnt/unarchive_dataset_tmp', type=str, help="压缩包的源路径，路径含压缩包的文件名称")
        parser.add_argument("--dest-path", nargs="?", default='/mnt/unarchive_dataset_tmp', type=str, help="压缩包的目标路径，路径是目录名称")

        parsed, unknown = parser.parse_known_args()
        for arg in unknown:  # 动态加入defs.py里子进程自定义的参数
            if arg.startswith(("-", "--")):
                parser.add_argument(arg.split("=")[0], nargs="?")

        self.args = parser.parse_args()
        # print(self.args)


def arg_parser():
    """
    函数用法
    :return:
    """
    parser = ArgParser()
    return parser.args


if __name__ == '__main__':
    # p = arg_parser()
    # print(p.archive_file_type)

    print(LOG_LEVEL)
