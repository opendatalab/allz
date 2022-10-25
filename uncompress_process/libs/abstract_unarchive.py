from abc import ABC, abstractmethod
from libs.argparser import arg_parser
import libs.common as common
import time


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
            self.handle(src_path, dest_path)
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
