from shlex import join

from allz.libs.abstract_decompress import AbstractDecompress


class ZipProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = join(["7z", "x", src_path, f"-o{dest_path}", "-aoa"])
        else:
            cmd = join(["7z", "x", src_path, f"-o{dest_path}", "-aos"])

        return cmd or None

    def decompress_test(self):
        cmd = "7z --help"

        return cmd or None

    def split_decompress(self, split_fiels, dest_path):
        pass
