import subprocess
import time
from abc import ABC, abstractmethod
from pathlib import Path

from allz.libs.file_type_tester import FileTypeTester

import allz.libs.common as common
from allz.defs import LOG_MODE_NORMAL, LOG_MODE_QUIET


class AbstractDecompress(ABC):
    def __init__(self):
        super().__init__()
        self.log = common.get_logger(self.__class__.__name__)
        self.file_type_tester = FileTypeTester()

    @abstractmethod
    def handle(self, src_path, dest_path, is_force_mode=False):
        pass

    def _handle(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False, is_force_mode=False, is_split_file=False):
        start_time = time.time()
        rtn_code = 0
        stdout = ""
        stderr = ""
        cmd = f"unar -q -D -o {dest_path} {src_path}"
        handle_cmd = ""

        if log_mode == LOG_MODE_QUIET or is_cli:
            self.log = common.set_log_mode(self.__class__.__name__, log_mode=LOG_MODE_QUIET)

        try:
            if not is_split_file:
                handle_cmd = self.handle(src_path, dest_path, is_force_mode)
            elif is_split_file:
                split_files_path = self.file_type_tester.get_split_volume_compressed_file_path_list(src_path)
                handle_cmd = self.split_decompress(split_files_path, dest_path, is_force_mode)
            
            cmd = f"unar -q -D -o {dest_path} {src_path}"

            if not Path.exists(Path(dest_path)):
                Path.mkdir(Path(str(dest_path).replace("\\ ", " ")), exist_ok=True, parents=True)

            if handle_cmd:
                cmd = handle_cmd

            unar_res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            rtn_code = unar_res.returncode
            stdout = unar_res.stdout

            if unar_res.returncode != 0:
                self.log.exception(unar_res.stderr)
                stderr = unar_res.stderr

            unar_res.check_returncode()
        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000) / 1000.0
            self.log.error(f"The compressed file {src_path} was processed with an error: {e}, elapsed time: {elapsed} 秒")
            self.log.exception(e)
            self.failed(src_path, dest_path, log_mode, is_cli)

            return rtn_code, stderr, stdout

        stdout += f"The decompress command is: {cmd} \n"
        elapsed = int((time.time() - start_time) * 1000) / 1000.0
        stdout += f"The compressed file {src_path} was processed successfully, elapsed time: {elapsed} 秒" + "\n"

        self.succeed(src_path, dest_path, log_mode, is_cli)

        return rtn_code, stderr, stdout

    @abstractmethod
    def decompress_test(self):
        pass
    
    def _decompress_test(self, is_cli=False):
        if is_cli:
            self.log = common.get_logger(self.__class__.__name__, log_mode=LOG_MODE_QUIET)

        try:
            decompress_cmd = self.decompress_test()
            if not decompress_cmd:
                return False

            decompress_res = subprocess.run(decompress_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if decompress_res.returncode != 0:
                self.log.exception(decompress_res.stderr.decode('utf-8'))

            decompress_res.check_returncode()
        except Exception as e:
            self.log.exception(e)
            return False
        
        return True
    
    @abstractmethod
    def split_decompress(self, split_fiels, dest_path, is_force_mode=False):
        pass

    def failed(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        if is_cli:
            log_mode = LOG_MODE_QUIET
        common.on_failure(src_path, dest_path, log_mode)

    def succeed(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False):
        if is_cli:
            log_mode = LOG_MODE_QUIET
        common.on_success(src_path, dest_path, log_mode)

    def main(self, src_path, dest_path, log_mode=LOG_MODE_NORMAL, is_cli=False, is_force_mode=False, is_split_file=False):
        rtn_code, stderr, stdout = self._handle(src_path, dest_path, log_mode, is_cli, is_force_mode, is_split_file)
        return rtn_code, stderr, stdout
