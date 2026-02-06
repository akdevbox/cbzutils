# SPDX-License-Identifier: LGPL-3.0-only
#
# Copyright (c) 2025 Amaan
# Licensed under LGPL v3.0 (See LICENSE.txt)
import argparse
import glob
import sys
from pathlib import Path

import cbzutils
from cbzutils.options import CommonOptions


def run_app(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="CBZ Utils provides you the abilities to work with cbz files to merge them or perform other operations on them"
    )

    subparsers = parser.add_subparsers(dest="_cmd")

    merge_opts = subparsers.add_parser(
        "merge", help="To merge multiple cbz files into one"
    )
    merge_opts.add_argument("files", nargs="+", help="Path to all cbz files")
    merge_opts.add_argument(
        "-o", "--out", metavar="FILE", help="Output file", default="output.cbz"
    )
    merge_opts.add_argument(
        "-s",
        "--sort-key",
        help="Sort key to sort names, by default uses a smart name num sort",
        choices=cbzutils.sort_keys.KEY_DICT.keys(),
        default="namenum",
    )
    merge_opts.add_argument(
        "-d",
        "--dry-run",
        help="Doesn't actually does the compression and instead prints the list of chapters in the order they shall be put according to the provided sort key",
        action="store_true",
    )
    merge_opts.add_argument(
        "--no-cover",
        help="Don't add automatically generated cover. Useful for chapters or volumes which already have a cover",
        action="store_true",
    )
    merge_opts.add_argument(
        "-t",
        "--title",
        help="The title of the file for the cover, defaults to output file name",
        default="",
    )
    merge_opts.add_argument(
        "-T",
        "--subtitle",
        help="The subtitle of the file for the cover, defaults to empty string",
        default="",
    )

    args_parsed = parser.parse_args(args=args)

    if args_parsed._cmd == "merge":
        cmd_merge(args_parsed)


def cmd_merge(args: argparse.Namespace):
    outfile = args.out
    infiles = args.files
    sort_key = args.sort_key

    sort_key_fn = cbzutils.sort_keys.KEY_DICT[sort_key]

    infiles_expanded = []
    for x in infiles:
        infiles_expanded.extend(glob.glob(x))

    if args.dry_run:
        for i, x in enumerate(sorted(infiles_expanded, key=sort_key_fn)):
            print(f"({i+1}/{len(infiles_expanded)}) {Path(x).name}")
    else:
        options = CommonOptions(
            not args.no_cover, args.title, args.subtitle, sort_key_fn
        )
        cbzutils.merge_cbz(outfile, infiles_expanded, options)
