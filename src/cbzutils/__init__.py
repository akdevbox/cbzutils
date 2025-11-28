# SPDX-License-Identifier: LGPL-3.0-only
#
# Copyright (c) 2025 Amaan
# Licensed under LGPL v3.0 (See LICENSE.txt)

from pathlib import Path
from typing import Any, Callable

import tqdm

from . import coverpage, sort_keys, source, writer


def merge_cbz(
    output: Path,
    files: list[Path],
    sort_key: Callable[[str], Any] = sort_keys.key_default,
    add_cover: bool = True,
    title: str = None,
    subtitle: str = None,
):
    """
    Merges as bunch of input cbz files into an output cbz file.

    the sort_key is a function that is passed as the key argument
    to the list.sort method.
    """

    files = [Path(x) for x in files]  # Just to make sure

    cbzwriter = writer.CbzWriter(Path(output))
    files.sort(key=lambda x: sort_key(x.name))

    if title is None:
        title = output.name.removesuffix(".cbz")
    if subtitle is None:
        subtitle = ""

    sources = [source.CbzSource(x) for x in files]
    if sources:
        if len(sources[0]):
            cover_background = sources[0][0]
        else:
            cover_background = None
    else:
        cover_background = None

    if add_cover:
        cover = coverpage.CoverPage(title, subtitle, cover_background)
        cbzwriter.append_source(cover)

    for x in tqdm.tqdm(sources, "Merging files"):
        cbzwriter.append_source(x)

    cbzwriter.close()
