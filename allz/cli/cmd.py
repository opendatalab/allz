# -*- coding: UTF-8 -*-

import click
from allz.__version__ import __version__
from allz.defs import LOG_MODE
from allz.unarchive.unarchive_main import Unarchive, decompress_cmd_test


@click.group(chain=True, invoke_without_command=True, context_settings={"help_option_names": ("-h", "--help"), "ignore_unknown_options": True})
@click.version_option(__version__)
def cli():
    pass


@cli.command("-d", help="To decompress file")
@click.option('-output-directory', '-o', default="./", help="The directory to write the contents of the archive. Defaults to the current directory.", required=False)
@click.argument('unkown_args', nargs=-1, type=click.UNPROCESSED)
# @click.pass_context
def decompress(output_directory, unkown_args):
    src_path = ""
    log_mode = LOG_MODE

    for arg in unkown_args:
        if arg == "-q":
            log_mode = "quiet"

        if not arg.startswith(("-", "--")):
            src_path = arg
            break

    Unarchive(src_path, output_directory, log_mode)


@cli.command("-q", help="Keep quiet, don't print output logs.")
# @click.option('-q', '--quiet', is_flag=True)
def set_quiet_mode():
    click.echo("quiet")
    

@cli.command("check", help="Test which compressed files are supported")
def check_file_type():
    can, cannot = decompress_cmd_test()
    click.echo("The decompression types that are supported are: " + str(", ".join(can)))
    click.echo("The decompression types that are not supported are: " + str(", ".join(cannot)))


cli.add_command(decompress)
cli.add_command(set_quiet_mode)
cli.add_command(check_file_type)


if __name__ == "__main__":
    cli()
