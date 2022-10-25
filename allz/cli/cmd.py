# -*- coding: UTF-8 -*-

import os
import platform

import click
from allz.unarchive.unarchive_main import Unarchive

HERE = os.path.dirname(os.path.abspath(__file__))
OS_TYPE = platform.platform().split('-')[0]


@click.command()
@click.option('--src_path', '-src', help="Specify the source path.", required=False)
@click.option('--dest_path', '-dest', help="Specify the destination.", required=False)
def main(src_path, dest_path):
    """
    """
    Unarchive(src_path, dest_path)
