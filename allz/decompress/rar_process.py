from allz.libs.abstract_decompress import AbstractDecompress


class RarProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = f"rar x {src_path} {dest_path} -o+".split()
        else:
            cmd = f"rar x {src_path} {dest_path} -o-".split()

        return cmd if cmd else None

    def decompress_test(self):
        cmd = "rar"

        return cmd if cmd else None
