import allz.libs.common as common
from allz.defs import UNARCHIVE_TYPE_COMMAND
from allz.libs.abstract_unarchive import AbstractUnarchive
from allz.libs.argparser import arg_parser


class UnarProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()
        self.args = arg_parser()
        self.src_path = self.args.src_path
        self.dest_path = self.args.dest_path
        self.log = common.get_logger(name=self.src_path)

    def handle(self, src_path, dest_path):
        cmd = f"unar -q -D -o {dest_path} {src_path}".split()

        return cmd if cmd else None


if __name__ == '__main__':
    mylogger = common.get_logger(name="unar")
    prog = UnarProcess()
    src_path = "/mnt/unarchive_dataset_tmp/A3D/compresss/jumpcutter-master.tar.lz"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/compress/jumpcutter-master.tar.lz#"
    prog.main(src_path, dest_path)

    # prog.handle(src_path, dest_path)
    exit(0)
