# -*- coding: UTF-8 -*-

from pathlib import Path

import click
from allz.unarchive.unarchive_main import Unarchive


@click.command(context_settings=dict(ignore_unknown_options=True, help_option_names=("-h", "--help")))
@click.option('-output-directory', '-o', default="./", help="The directory to write the contents of the archive to. Defaults to the current directory.", required=False)
@click.argument('unkown_args', nargs=-1, type=click.UNPROCESSED)
def cli(output_directory, unkown_args):
    """
    """
    src_path = ""
    current_dir = Path.cwd()

    for arg in unkown_args:
        if not arg.startswith(("-", "--")):
            src_path = arg
            break

    if not Path.exists(Path(src_path)):
        if Path.exists(Path.joinpath(current_dir, src_path)):
            src_path = Path.joinpath(current_dir, src_path)
        else:
            click.echo("input archive file is not exists.")
            exit(1)

    Unarchive(src_path, output_directory)
