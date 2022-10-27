import allz.libs.common as common
from allz.libs.abstract_unarchive import AbstractUnarchive


class UnarProcess(AbstractUnarchive):
    def __init__(self):
        super().__init__()

    def handle(self, src_path, dest_path):
        cmd = f"unar -q -D -o {dest_path} {src_path}".split()

        return cmd if cmd else None
