from allz.libs.abstract_decompress import AbstractDecompress


class ZipProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = f"7z x {src_path} -o{dest_path} -aoa".split()
        else:
            cmd = f"7z x {src_path} -o{dest_path} -aos".split()
        
        return cmd if cmd else None

    def decompress_test(self):
        cmd = "7z --help"
        
        return cmd if cmd else None
