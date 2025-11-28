import string
from functools import cmp_to_key
from typing import Union


def key_default(x: str) -> str:
    """
    Default key does not perform any conversions on the input type
    and returns the value as is so that it can be compared on default basis
    as defined by the python interpreter
    """
    return x


def _split_into_str_num_components(x: str) -> list[Union[float, str]]:
    """
    Returns the given element split into its string and numeric components

    For example: "abs213" -> ["abs", 213]

    what this results in is an alternating pattern of string and numbers, it is guarenteed
    that the first element is a str even if its empty, ie all even indexes
    are strings while all odd indexes are int
    """
    mode = "s"
    buffer = ""
    result = []
    encounter_float = False

    for letter in x:
        if mode == "s":  # String mode, if its string keep appending to buffer
            if letter in string.digits:  # Letter is a number, this is a mode change
                result.append(buffer)
                buffer = letter
                mode = "i"
            else:
                buffer += letter
        elif mode == "i":
            if letter in string.digits or (letter == "." and not encounter_float):
                if letter == ".":
                    encounter_float = True
                buffer += letter
            else:
                result.append(float(buffer))
                buffer = letter
                mode = "s"
                encounter_float = False

    # For if there is content remaining in the buffer
    if buffer:
        if mode == "s":
            result.append(buffer)
        elif mode == "i":
            result.append(float(buffer))
    return result


def _cmp_namenum(x1: str, x2: str) -> int:
    """
    returns 1 for x1 > x2 and -1 for x1 < x2 and 0 for x1 == x2.
    the logical definition of >, <, == is defined by the name num ordering.
    """
    # See docs for key_namenum

    # Strip cbz extension if present
    if x1.endswith(".cbz"):
        x1 = x1.removesuffix(".cbz")
    if x2.endswith(".cbz"):
        x2 = x2.removesuffix(".cbz")

    # First split into respective components of str and int so we can compare them one by one
    x1 = _split_into_str_num_components(x1)
    x2 = _split_into_str_num_components(x2)

    min_len = min(len(x1), len(x2))

    for idx in range(min_len):
        if x1[idx] < x2[idx]:
            return -1
        elif x1[idx] > x2[idx]:
            return 1

    if len(x1) < len(x2):
        return -1
    elif len(x1) > len(x2):
        return 1
    else:
        return 0


"""
A key to compare on the basis of name number ordering.
this is the best ordering to use for most logical comparisions

ie, in a normal string comparision 10 would loose against 9 which would make it
sort 10 before 9. but this one preserves the numeric and logical ordering of the elements.

First they are checked on the basis of their string and numeric parts separated
and if all that comes to equal. then the one with lesser parts is deemed lesser.

if all that still comes to equal, the strings are returned as equal
"""
key_namenum = cmp_to_key(_cmp_namenum)


KEY_DICT = {
    "default": key_default,
    "namenum": key_namenum,
}
