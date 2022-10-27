# -*- coding: UTF-8 -*-

import click
from allz.__version__ import __version__
from allz.defs import LOG_MODE
from allz.unarchive.unarchive_main import Unarchive, decompress_cmd_test


@click.group(context_settings={"help_option_names": ("-h", "--help"), "ignore_unknown_options": True})
@click.version_option(__version__)
def cli():
    pass


@cli.command()
# @click.pass_context
@click.option('-output-directory', '-o', default="./", help="The directory to write the contents of the archive. Defaults to the current directory.", required=False)
@click.argument('unkown_args', nargs=-1, type=click.UNPROCESSED)
# @click.argument('src_path', nargs=-1, type=click.UNPROCESSED)
# @click.argument('src_path')
def d(output_directory, unkown_args):
    src_path = ""
    log_mode = LOG_MODE

    for arg in unkown_args:
        if arg == "q":
            log_mode = "quiet"

        if not arg.startswith(("-", "--")) and arg not in ["d", "q"]:
            src_path = arg
            break

    Unarchive(src_path, output_directory, log_mode)
    

@cli.command()
def test():
    can, cannot = decompress_cmd_test()
    click.echo("The decompression types that are supported are: " + str(", ".join(can)))
    click.echo("The decompression types that are not supported are: " + str(", ".join(cannot)))


cli.add_command(d)
# cli.add_command(q)
cli.add_command(test)


if __name__ == "__main__":
    cli()
