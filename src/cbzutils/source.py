import abc
import copy
import io
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Self


class Source(abc.ABC):
    """
    Source abstract class

    Any class implementing Source should have the following behaviour
    * `object[index]` returns a pathlib.Path object that points to a image file.
    * `del object` automatically should cleanup any temporary files created by it.
    * `len(object)` should return the total number of pages in the source.
    * an IndexError is raised when index is out of range of the source.
    """

    @abc.abstractmethod
    def __len__(self) -> int: ...

    @abc.abstractmethod
    def __getitem__(self, idx: int) -> Path:
        """
        Should return a path to an image file.
        """
        ...


class CbzSource(Source):
    """
    A source object that can read cbz files one by one.
    This does not extract the cbz file immidiately but rather does it on demand.

    Upon deletion, automatically deletes any created temp files.
    Hence, tempfile paths returned by this object are only valid as long as the object is alive.
    """

    def __init__(self, fname: Path) -> None:
        self._fname = fname
        self._fhandle = zipfile.ZipFile(fname)

        self._internal_fnames = self._fhandle.namelist()
        self._internal_fnames.sort()

        # Create a list either containing None or containing the tempfile path to the
        # respective page/index in the cbz file. the tempfile is created if not found
        # inside __getitem__ method.
        self._extracted_tempfiles: list[str] = [
            None for x in range(len(self._internal_fnames))
        ]

    def __len__(self) -> int:
        return len(self._internal_fnames)

    def __getitem__(self, idx: int) -> Path:
        return Path(self._create_ifnotexists(idx))

    def _create_ifnotexists(self, idx: int) -> str:
        """
        Extracts the image from the zip file and saves it in a temporary file if the corresponding
        temporary file hasn't already been created. returns the string path to the temporary file.
        """
        if self._extracted_tempfiles[idx] is None:  # The item hasn't been extracted yet
            corresponding_internal_fname = self._internal_fnames[idx]

            # Preserve the file extension in the temporary file and create a temp file
            ext = Path(corresponding_internal_fname).suffix
            tfile = tempfile.NamedTemporaryFile(suffix=ext, delete=False)

            # Extract the image and write to the temporary file
            efile = self._fhandle.open(corresponding_internal_fname, "r")
            shutil.copyfileobj(efile, tfile)

            self._extracted_tempfiles[idx] = tfile.name

            tfile.close()
            efile.close()

        return self._extracted_tempfiles[idx]

    def __del__(self) -> None:
        self._fhandle.close()

        # Cleanup all temporary files that have been created
        for x in self._extracted_tempfiles:
            if x is not None:
                Path(x).unlink(missing_ok=True)


class CombinedSource(Source):
    """
    Combines the given sources to act like one. Essentially a merger without having marged
    yet.
    """

    def __init__(self, sources: list[Source]):
        self._sources = sources
        self._lens = [len(x) for x in self._sources]
        self._len = sum(self._lens)

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, idx: int) -> Path:
        for i, ln in enumerate(self._lens):
            if idx - ln < 0:
                return self._sources[i][idx]

        raise IndexError("Index not in range of the combined sources")


class SourceSlice(Source):
    """
    Creates a slice out of the original source
    """

    def __init__(self, source: Source, start_idx: int, end_idx: int):
        self._start = start_idx
        self._end = end_idx
        self.source = source

        assert (
            self._end >= self._start
        ), "The slice end_idx must be greated than start_idx"

    def __len__(self) -> int:
        return self._end - self._start

    def __getitem__(self, idx: int) -> Path:
        if idx >= len(self) or idx < 0:
            raise IndexError(f"index larger than slice length of: {len(self)}")

        return self.source[self._start + idx]
