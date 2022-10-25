import os
import subprocess
import time
from abc import ABC, abstractmethod

import allz.libs.common as common
from allz.defs import UNARCHIVE_TYPE_COMMAND
from allz.libs.argparser import arg_parser


class AbstractUnarchive(ABC):
    def __init__(self, thread_cnt=4):
        super().__init__()
        self.args = arg_parser()
        self.src_path = self.args.src_path
        self.dest_path = self.args.dest_path
        self.log = common.get_logger(name=self.src_path)

    @abstractmethod
    def handle(self, src_path, dest_path):
        pass

    def _handle(self, src_path, dest_path):
        start_time = time.time()
        self.log.info(f"开始处理压缩包: {src_path}")
        try:
            cmd = f"unar -q -D -o {dest_path} {src_path}".split()

            # dest_path不存在，则新建目录
            if not os.path.exists(dest_path):
                mkdir_cmd = f"mkdir -p {dest_path}".split()
                mk_res = subprocess.run(mkdir_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if mk_res.returncode != 0:
                    self.log.exception(mk_res.stderr.decode('utf-8'))

                mk_res.check_returncode()
                self.log.info("创建目录成功, " + ' '.join(mkdir_cmd))

            handle_cmd = self.handle(src_path, dest_path)
            if handle_cmd:
                cmd = handle_cmd

            unar_res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if unar_res.returncode != 0:
                self.log.exception(unar_res.stderr.decode('utf-8'))

            unar_res.check_returncode()
            self.log.info("解压命令: " + ' '.join(cmd))
            
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000) / 1000.0
            self.log.error(f"压缩包 {src_path} 处理出错: {e}, 处理时长: {elapsed} 秒")
            self.log.exception(e)
            self.failed(src_path, dest_path)
            return

        elapsed = int((time.time() - start_time) * 1000) / 1000.0
        self.log.info(f"压缩包 {src_path} 处理成功, 处理时长: {elapsed} 秒")
        self.succeed(src_path, dest_path)

    def failed(self, src_path, dest_path):
        common.on_failure(src_path, dest_path)

    def succeed(self, src_path, dest_path):
        common.on_success(src_path, dest_path)

    def main(self, src_path, dest_path):
        self._handle(src_path, dest_path)
