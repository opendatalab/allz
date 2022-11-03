import subprocess
import time
from abc import ABC, abstractmethod
from pathlib import Path

import allz.libs.common as common
from allz.defs import LOG_MODE_NORMAL, LOG_MODE_QUIET


class AbstractUnarchive(ABC):
    def __init__(self):
        super().__init__()
        self.log = common.get_logger(self.__class__.__name__)

    @abstractmethod
    def handle(self, src_path, dest_path):
        pass

    def _handle(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        start_time = time.time()
        res_status = True
        stdout = ""
        stderr = ""

        if log_mode == LOG_MODE_QUIET or is_cli:
            self.log = common.get_logger(self.__class__.__name__, log_mode=LOG_MODE_QUIET)

        try:
            cmd = f"unar -q -D -o {dest_path} {src_path}".split()

            if not Path.exists(Path(dest_path)):
                Path(dest_path).mkdir(parents=True)

            handle_cmd = self.handle(src_path, dest_path)
            if handle_cmd:
                cmd = handle_cmd

            unar_res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout = unar_res.stdout

            if unar_res.returncode != 0:
                self.log.exception(unar_res.stderr)
                res_status = False
                stderr = unar_res.stderr

            unar_res.check_returncode()
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000) / 1000.0
            self.log.error(f"The compressed file {src_path} was processed with an error: {e}, elapsed time: {elapsed} 秒")
            self.log.exception(e)
            self.failed(src_path, dest_path, log_mode, is_cli)
            res_status = False
            return res_status, stderr, stdout

        stdout += "The decompress command is: " + ' '.join(cmd) + "\n"
        elapsed = int((time.time() - start_time) * 1000) / 1000.0
        stdout += f"The compressed file {src_path} was processed successfully, elapsed time: {elapsed} 秒" + "\n"

        self.succeed(src_path, dest_path, log_mode, is_cli)

        return res_status, stderr, stdout

    @abstractmethod
    def decompress_test(self):
        pass
    
    def _decompress_test(self):
        decompress_cmd = self.decompress_test()
        if not decompress_cmd:
            return False

        try:
            decompress_res = subprocess.run(decompress_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if decompress_res.returncode != 0:
                self.log.exception(decompress_res.stderr.decode('utf-8'))

            decompress_res.check_returncode()
        except Exception as e:
            self.log.exception(e)
            return False
        
        return True

    def failed(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        if is_cli:
            log_mode = LOG_MODE_QUIET
        common.on_failure(src_path, dest_path, log_mode)

    def succeed(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        if is_cli:
            log_mode = LOG_MODE_QUIET
        common.on_success(src_path, dest_path, log_mode)

    def main(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        res_status, stderr, stdout = self._handle(src_path, dest_path, log_mode, is_cli)
        return res_status, stderr, stdout
