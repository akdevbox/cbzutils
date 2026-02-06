# SPDX-License-Identifier: LGPL-3.0-only
#
# Copyright (c) 2025 Amaan
# Licensed under LGPL v3.0 (See LICENSE.txt)
from pathlib import Path
from typing import Any, Callable

import tqdm

from cbzutils.options import CommonOptions

from . import coverpage, sort_keys, source, writer


def merge_cbz(
    output: Path,
    files: list[Path],
    options: CommonOptions | None = None,
):
    """
    Merges as bunch of input cbz files into an output cbz file.

    the sort_key is a function that is passed as the key argument
    to the list.sort method.
    """

    if options is None:
        options = CommonOptions()

    options.with_fn(output)

    files = [Path(x) for x in files]  # Just to make sure

    cbzwriter = writer.CbzWriter(Path(output))
    files.sort(key=lambda x: options.sort_key(x.name))

    sources = [source.CbzSource(x) for x in files]
    cover_background: str | None
    if sources:
        if len(sources[0]):
            cover_background = str(sources[0][0])
        else:
            cover_background = None
    else:
        cover_background = None

    if options.add_cover:
        cover = coverpage.CoverPage(options.title, options.subtitle, cover_background)
        cbzwriter.append_source(cover)

    for x in tqdm.tqdm(sources, "Merging files"):
        cbzwriter.append_source(x)

    cbzwriter.close()
