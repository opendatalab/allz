# -*- coding: UTF-8 -*-

import io
import sys

import click

from allz.decompress.decompress_main import DecompressMain
from allz.defs import LOG_MODE_NORMAL, LOG_MODE_QUIET
from allz.libs.file_type_tester import FileTypeTester


@click.group(context_settings={"help_option_names": ("-h", "--help"), "ignore_unknown_options": True})
@click.version_option()
def cli():
    pass


@cli.command("-d", help="To decompress file.")
@click.option('--output-directory', '-o', default="./", help="The directory to write the contents of the archive. Defaults to the current directory.", required=False)
@click.option("-q", is_flag=True, required=False, help="Run in quiet mode.")
@click.option("-f", is_flag=True, required=False, help="Always overwrite files when a file to be unpacked already exists on disk. By default, the program will skips the file.")
@click.argument("input", type=click.File("rb"), nargs=-1)
def decompress(output_directory, input, q, f):
    log_mode = LOG_MODE_NORMAL
    if q:
        log_mode = LOG_MODE_QUIET

    force_mode = bool(f)
    src_path = io.BufferedReader(input[0]).name if len(input) > 0 else ""
    try:
        de_main = DecompressMain()
        rtn_code, stderr, stdout = de_main.Decompress(src_path, output_directory, log_mode=log_mode, is_cli=True, is_force_mode=force_mode)
        sys.stderr.write(stderr)

        if not q:
            sys.stderr.write(stdout)

        sys.exit(rtn_code)
    except Exception:
        click.echo("allz decompress error, please check your command, you can wiew usage through the allz -d command")
        sys.exit(-1)


@cli.command("check", help="Test which compressed files are supported.")
def check_file_type():
    de_main = DecompressMain()
    can, cannot = de_main.decompress_cmd_test(is_cli=True)
    click.echo("The decompression types that are supported are: " + ", ".join(can))
    click.echo("The decompression types that are not supported are: " + ", ".join(cannot))


@cli.command("-p", help="Stdout normal and split volumn compressed file regex match pattern.")
@click.option("--only-normal", is_flag=True, required=False, help="Only stdout normal compressed files regex match pattern.")
@click.option("--only-split", is_flag=True, required=False, help="Only stdout split volumn compressed files regex match pattern.")
def compressed_file_regex_pattern(only_normal, only_split):
    tester = FileTypeTester()
    if only_normal:
        sys.stdout.write(f"{tester.ext_regex.pattern}\n")
    elif only_split:
        sys.stdout.write(f"{tester.split_volume_match_regex.pattern}\n")
    else:
        sys.stdout.write(f"{tester.ext_regex.pattern}\n{tester.split_volume_match_regex.pattern}\n")


cli.add_command(decompress)
cli.add_command(check_file_type)
cli.add_command(compressed_file_regex_pattern)


if __name__ == "__main__":
    cli()
