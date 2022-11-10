import os

from allz.libs.abstract_decompress import AbstractDecompress


class Z7SplitProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def split_decompress(self, split_files, dest_path, is_force_mode=False):
        cmd = ""
        if len(split_files) > 0:
            split_first_path = sorted(split_files)[0]
            split_tar_path = str(dest_path).strip("/") + os.sep + str(split_first_path).split("/")[-1].strip(".7z.001")
            cmd = f"7z x -aoa {split_first_path} -o{dest_path} && tar -xvf {split_tar_path} -C {dest_path} && rm {split_tar_path}"

        return cmd if cmd else None
    
    def handle(self, src_path, dest_path, is_force_mode=False):
        pass

    def decompress_test(self):
        pass
