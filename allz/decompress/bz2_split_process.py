from allz.libs.abstract_decompress import AbstractDecompress


class Bz2SplitProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def split_decompress(self, split_files, dest_path, is_force_mode=False):
        cmd = ""
        if len(split_files) > 0:
            src_path = ".".join(str(split_files[0]).split(".")[:-1]) + ".*"
            cmd = f"cat {src_path} | tar jx -C {dest_path}"

        return cmd if cmd else None
    
    def handle(self, src_path, dest_path, is_force_mode=False):
        pass

    def decompress_test(self):
        pass
