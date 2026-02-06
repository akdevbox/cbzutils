"""
Provides a dataclass for common options
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import cbzutils.sort_keys


@dataclass
class CommonOptions:
    add_cover: bool = True
    title: str = ""
    subtitle: str = ""
    sort_key: Callable[[str], Any] = cbzutils.sort_keys.key_default

    def with_fn(self, fn: str | Path):
        """
        forms the title from file name if title is empty
        """
        if not self.title:
            self.title = Path(fn).stem
