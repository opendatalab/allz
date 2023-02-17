from shlex import join

from allz.libs.abstract_decompress import AbstractDecompress

and_symbol = "&&"


class Tar7zSplitProcess(AbstractDecompress):
    def __init__(self):
        super().__init__()

    def split_decompress(self, split_files, dest_path, is_force_mode=False):
        cmd = ""
        if len(split_files) > 0:
            split_first_path = sorted(split_files)[0]
            split_tar_path = "/".join([dest_path, str(split_first_path).split("/")[-1].rstrip(".7z.001")])

            if is_force_mode:
                cmd = join(['7z', 'x', '-aoa', split_first_path, f"-o{dest_path}"]) + ' && ' + join(['tar', '-xvf', split_tar_path, '-C', dest_path, '--overwrite']) + ' && ' + join(['rm', split_tar_path])
            else:
                cmd = join(['7z', 'x', '-aos', split_first_path, f"-o{dest_path}"]) + ' && ' + join(['tar', '-xvf', split_tar_path, '-C', dest_path, '--skip-old-files']) + ' && ' + join(['rm', split_tar_path])

        return cmd or None
    
    def handle(self, src_path, dest_path, is_force_mode=False):
        pass

    def decompress_test(self):
        pass
