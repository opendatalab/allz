from allz.libs.abstract_decompress import AbstractDecompress


class UnarProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path):
        cmd = f"unar -q -D -o {dest_path} {src_path}".split()

        return cmd if cmd else None
    
    def decompress_test(self):
        cmd = "unar --help"
        
        return cmd if cmd else None

    def split_decompress(self, split_fiels, dest_path):
        pass