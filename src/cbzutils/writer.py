import abc
import shutil
import zipfile
from pathlib import Path

from .source import Source


class Writer(abc.ABC):
    def append_source(self, src: Source) -> None:
        """
        Appends a source into the writer.
        """
        pass

    def close(self) -> None:
        """
        Performs all the necessary cleanup to close and complete
        the output file
        """


class CbzWriter(Writer):

    def __init__(self, fname: Path) -> None:
        self._fname = fname
        self._fhandle = zipfile.ZipFile(fname, "w")
        self._counter = 1

    def append_source(self, src: Source) -> None:
        """
        Takes the image files from the source one by one and append them
        to the cbz file. the files are renamed in correspondence to the internal counter
        """
        for x in range(len(src)):
            source_file_path = src[x]

            ext = source_file_path.suffix

            srcfile = open(source_file_path, "rb")
            destfile = self._fhandle.open(f"{self._counter:06d}{ext}", "w")
            shutil.copyfileobj(srcfile, destfile)

            srcfile.close()
            destfile.close()

            self._counter += 1

    def close(self) -> None:
        self._fhandle.close()

    def __del__(self) -> None:
        self.close()
