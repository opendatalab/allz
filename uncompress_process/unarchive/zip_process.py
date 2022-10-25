
import os
import subprocess

import uncompress_process.libs.common as common
from uncompress_process.defs import UNARCHIVE_TYPE_COMMAND
from uncompress_process.libs.abstract_unarchive import AbstractUnarchive
from uncompress_process.libs.argparser import arg_parser


class ZipProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()
        self.args = arg_parser()
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

        unar_prefix_cmd = UNARCHIVE_TYPE_COMMAND['zip_process']['comm_unar_prefix_cmd']
        unar_suffix_cmd = UNARCHIVE_TYPE_COMMAND['zip_process']['comm_unar_suffix_cmd']
        cmd = f"{unar_prefix_cmd} {src_path} {unar_suffix_cmd}{dest_path}".split()
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
    prog = ZipProcess()
    src_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.zip"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/"
    prog.main(src_path, dest_path)

    # prog.handle(src_path, dest_path)
    exit(0)
