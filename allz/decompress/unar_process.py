from allz.libs.abstract_decompress import AbstractDecompress


class UnarProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = f"unar -q -D -f -o {dest_path} {src_path}".split()
        else:
            cmd = f"unar -q -D -o {dest_path} {src_path}".split()

        return cmd if cmd else None
    
    def decompress_test(self):
        cmd = "unar --help"
        
        return cmd if cmd else None
