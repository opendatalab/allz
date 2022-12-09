from allz.libs.abstract_decompress import AbstractDecompress


class RarProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = f"rar x {src_path} {dest_path} -o+"
        else:
            cmd = f"rar x {src_path} {dest_path} -o-"

        return cmd or None

    def decompress_test(self):
        cmd = "rar"

        return cmd or None
    
    def split_decompress(self, split_files, dest_path, is_force_mode=False):
        pass
