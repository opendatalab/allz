import allz.libs.common as common
from allz.libs.abstract_unarchive import AbstractUnarchive
# from allz.libs.argparser import arg_parser


class TarBzProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()
        # self.args = arg_parser()
        # self.src_path = self.args.src_path
        # self.dest_path = self.args.dest_path
        # self.log = common.get_logger("TarBzProcess")

    def handle(self, src_path, dest_path):
        cmd = f"tar xjf {src_path} -C {dest_path}".split()

        return cmd if cmd else None


if __name__ == '__main__':
    mylogger = common.get_logger(name="unar")
    prog = TarBzProcess()
    src_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz2"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz2#"
    prog.main(src_path, dest_path)

    exit(0)
