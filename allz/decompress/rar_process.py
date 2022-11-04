from allz.libs.abstract_decompress import AbstractDecompress


class RarProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path):
        cmd = f"rar x {src_path} {dest_path}".split()

        return cmd if cmd else None

    def decompress_test(self):
        cmd = "rar"

        return cmd if cmd else None
