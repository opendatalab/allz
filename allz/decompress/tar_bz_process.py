from allz.libs.abstract_decompress import AbstractDecompress


class TarBzProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path, is_force_mode=False):
        if is_force_mode:
            cmd = f"tar xjf {src_path} -C {dest_path} --overwrite "
        else:
            cmd = f"tar xjf {src_path} -C {dest_path} --skip-old-files"

        return cmd or None

    def decompress_test(self):
        cmd = "tar --help"

        return cmd or None

    def split_decompress(self, split_fiels, dest_path):
        pass
