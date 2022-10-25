import argparse

from allz.defs import LOG_LEVEL


class ArgParser(object):
    """
    参数解析
    """
    def __init__(self, ):
        parser = argparse.ArgumentParser(description='压缩包解压参数解析')
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
