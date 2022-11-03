# -*- coding: UTF-8 -*-

import logging
import sys

import click

from allz.defs import LOG_MODE_QUIET, __version__
from allz.unarchive.unarchive_main import Unarchive, decompress_cmd_test

stderr_handler = logging.StreamHandler(stream=sys.stderr)


@click.group(context_settings={"help_option_names": ("-h", "--help"), "ignore_unknown_options": True})
@click.version_option(__version__)
def cli():
    pass


@cli.command("-d", help="To decompress file")
@click.option('--output-directory', '-o', default="./", help="The directory to write the contents of the archive. Defaults to the current directory.", required=False)
@click.option("-q", is_flag=True, required=False)
@click.argument('unkown_args', nargs=-1, type=click.UNPROCESSED)
def decompress(output_directory, unkown_args, q):
    src_path = ""

    for arg in unkown_args:
        if not arg.startswith(("-", "--")):
            src_path = arg
            break

    res_status, stderr, stdout = Unarchive(src_path, output_directory, log_mode=LOG_MODE_QUIET, is_cli=True)
    sys.stderr.write(stderr)
    if not q:
        sys.stderr.write(stdout)

    if not res_status:
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command("check", help="Test which compressed files are supported")
def check_file_type():
    can, cannot = decompress_cmd_test()
    click.echo("The decompression types that are supported are: " + str(", ".join(can)))
    click.echo("The decompression types that are not supported are: " + str(", ".join(cannot)))


cli.add_command(decompress)
cli.add_command(check_file_type)


if __name__ == "__main__":
    cli()
