# -*- coding: UTF-8 -*-

from functools import partial
from pathlib import Path

import click
from allz.__version__ import __version__
from allz.unarchive.unarchive_main import Unarchive, decompress_cmd_test


@click.group(context_settings={"help_option_names": ("-h", "--help"), "ignore_unknown_options": True})
@click.version_option(__version__)
# @click.pass_context
def cli():
    pass


@click.command()
@click.option('-output-directory', '-o', default="./", help="The directory to write the contents of the archive to. Defaults to the current directory.", required=False)
@click.argument('unkown_args', nargs=-1, type=click.UNPROCESSED)
def unarchive(output_directory, unkown_args):
    src_path = ""
    current_dir = Path.cwd()

    for arg in unkown_args:
        if not arg.startswith(("-", "--")):
            src_path = arg
            break

    if not Path.exists(Path(src_path)):
        if Path.exists(Path.joinpath(current_dir, src_path)):
            src_path = Path.joinpath(current_dir, src_path)
            Unarchive(src_path, output_directory)
        else:
            click.echo("input archive file is not exists.")
            exit(1)


@click.command()
@click.option('-test', is_flag=True, expose_value=False, is_eager=True, help="Test the decompressed file types supported by the current environment. ", required=False)
def test():
    can, cannot = decompress_cmd_test()
    click.echo("The decompression types that are supported are: " + str(",".join(can)))
    click.echo("The decompression types that are not supported are: " + str(",".join(cannot)))


cli.add_command(unarchive)
cli.add_command(test)


if __name__ == "__main__":
    cli()
