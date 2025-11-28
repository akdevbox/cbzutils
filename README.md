This project is licensed under the GNU Lesser General Public License version 3.0 (LGPL-3.0).
See LICENSE.txt for the full license text.
Also check out licenses of vendored items inside the licenses folder.


# CBZ Utilities

This is both a library and a command line tool to deal with CBZ files. It can
perform different functions in relation to it. Its mostly a hobby project that
was born out of need.

## Features
* Merging CBZ files
* Auto generating a basic cover
* Automatic Logical Ordering of input files

## Install
To install the latest stable release, simply run the following

```
pip install cbzutils
```

or if you have pipx

```
pipx install cbzutils
```

then you can access it via the command line as `cbzutils` if its added to your PATH during install properly.

To clone and run this project

```
uv sync
uv tool install .
```

To provide contributions and install the project in editable mode

```
uv sync
uv tool install . -e
```

## How to use

```
usage: cbzutils merge [-h] [-o FILE] [-s {default,namenum}] [-d] [--no-cover] [-t TITLE] [-T SUBTITLE] files [files ...]

positional arguments:
  files                 Path to all cbz files

options:
  -h, --help            show this help message and exit
  -o, --out FILE        Output file
  -s, --sort-key {default,namenum}
                        Sort key to sort names, by default uses a smart name num sort
  -d, --dry-run         Doesn't actually does the compression and instead prints the list of chapters in the order they shall be put according to the provided sort key
  --no-cover            Don't add automatically generated cover. Useful for chapters or volumes which already have a cover
  -t, --title TITLE     The title of the file for the cover, defaults to output file name
  -T, --subtitle SUBTITLE
                        The subtitle of the file for the cover, defaults to empty string
```

Here are a few examples. Suppose you have the following files in a folder

```
Chap 1.cbz
Chap 2.cbz
Chap 3.cbz
Chap 3.5.cbz
Chap 4.cbz
```

first cd into that folder 

```
cd path/to/the/folder
```

and then you can run the following command

```
cbzutils merge Chap* -d
```

This will print a list of chapters and the order in which they shall be merged, be sure to check it. Please report any bugs
to the github repository so the ordering can be fixed in special cases. But if the ordering is messed up, in the meanwhile, try
renaming the files in a consistent manner like presented above. (Cbzutils itself is designed to work out of the box with all sorts of inconsistent file naming schemes).

Then to actually merge, run the following

```
cbzutils merge Chap* -o MyComic.cbz --title "MyComic" --subtitle "Ch 1-4"
```

This will produce an output cbz file named MyComic.cbz, you can now conver this file into other desired formats using
[Callibre](https://calibre-ebook.com), a free books management software.

## Contribution Guidelines

* Please format your code using `black` and `isort` before opening a PR.
* All PRs introducing major
changes should be accompanies by an Issue. Please discuss inside the Issue before going ahead
and making changes.
* Small changes regarding documentation and such can be made directly without an associated Issue

Thank you!