
import os
import subprocess

import uncompress_process.libs.common as common
from uncompress_process.defs import UNARCHIVE_TYPE_COMMAND
from uncompress_process.libs.abstract_unarchive import AbstractUnarchive
from uncompress_process.libs.argparser import arg_parser


class UnarProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()
        self.args = arg_parser()
        self.unar_cmd = self.args.unar_cmd
        self.archive_type = self.args.archive_type
        self.src_path = self.args.src_path
        self.dest_path = self.args.dest_path
        self.log = common.get_logger(name=self.src_path)

    def handle(self, src_path, dest_path):
        if not os.path.exists(dest_path):
            mkdir_cmd = f"mkdir -p {dest_path}".split()
            try:
                mk_res = subprocess.run(mkdir_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if mk_res.returncode != 0:
                    self.log.exception(mk_res.stderr.decode('utf-8'))

                mk_res.check_returncode()
                self.log.info("创建目录成功, " + ' '.join(mkdir_cmd))
            except Exception:
                raise

        unar_cmd = UNARCHIVE_TYPE_COMMAND['unar_process']['comm_unar_prefix_cmd']
        cmd = f"{unar_cmd} {dest_path} {src_path}".split()
        try:
            unar_res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if unar_res.returncode != 0:
                self.log.exception(unar_res.stderr.decode('utf-8'))

            unar_res.check_returncode()
            self.log.info("解压命令: " + ' '.join(cmd))
        except Exception:
            raise


if __name__ == '__main__':
    mylogger = common.get_logger(name="unar")
    prog = UnarProcess()
    src_path = "/mnt/unarchive_dataset_tmp/A3D/compresss/jumpcutter-master.tar.lz"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/compress/jumpcutter-master.tar.lz#"
    prog.main(src_path, dest_path)

    # prog.handle(src_path, dest_path)
    exit(0)
