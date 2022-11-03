from allz.libs.abstract_unarchive import AbstractUnarchive


class TarBzProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path):
        cmd = f"tar xjf {src_path} -C {dest_path}".split()

        return cmd if cmd else None

    def decompress_test(self):
        cmd = "tar --help"

        return cmd if cmd else None
