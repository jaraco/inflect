"""Domain 5: Number-to-Words / Ordinals logic and data tables."""

from __future__ import annotations

import re
from numbers import Number
from typing import List, Optional, Union

from .utils import (
    BadChunkingOptionError,
    NumOutOfRangeError,
    Falsish,
    Word,
)


# NUMERICAL INFLECTIONS

nth = {
    0: "th",
    1: "st",
    2: "nd",
    3: "rd",
    4: "th",
    5: "th",
    6: "th",
    7: "th",
    8: "th",
    9: "th",
    11: "th",
    12: "th",
    13: "th",
}
nth_suff = set(nth.values())

ordinal = dict(
    ty="tieth",
    one="first",
    two="second",
    three="third",
    five="fifth",
    eight="eighth",
    nine="ninth",
    twelve="twelfth",
)

ordinal_suff = re.compile(rf"({'|'.join(ordinal)})\Z")


# NUMBERS

unit = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
teen = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
ten = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]
mill = [
    " ",
    " thousand",
    " million",
    " billion",
    " trillion",
    " quadrillion",
    " quintillion",
    " sextillion",
    " septillion",
    " octillion",
    " nonillion",
    " decillion",
]


# Pre-compiled regex patterns for numbers domain

DIGIT = re.compile(r"\d")

DIGIT_GROUP = re.compile(r"(\d)")
TWO_DIGITS = re.compile(r"(\d)(\d)")
THREE_DIGITS = re.compile(r"(\d)(\d)(\d)")
THREE_DIGITS_WORD = re.compile(r"(\d)(\d)(\d)(?=\D*\Z)")
TWO_DIGITS_WORD = re.compile(r"(\d)(\d)(?=\D*\Z)")
ONE_DIGIT_WORD = re.compile(r"(\d)(?=\D*\Z)")

FOUR_DIGIT_COMMA = re.compile(r"(\d)(\d{3}(?:,|\Z))")
NON_DIGIT = re.compile(r"\D")
WHITESPACES_COMMA = re.compile(r"\s+,")
COMMA_WORD = re.compile(r", (\S+)\s+\Z")
WHITESPACES = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def ordinal_fn(engine, num):  # noqa: F811 - 'ordinal' is also a data table name
    """
    Return the ordinal of num.

    >>> p = __import__('inflect').engine()
    >>> p.ordinal(1)
    '1st'
    >>> p.ordinal('one')
    'first'
    """
    if DIGIT.match(str(num)):
        if isinstance(num, (float, int)) and int(num) == num:
            n = int(num)
        else:
            if "." in str(num):
                try:
                    # numbers after decimal,
                    # so only need last one for ordinal
                    n = int(str(num)[-1])

                except ValueError:
                    # ends with '.', so need to use whole string
                    n = int(str(num)[:-1])
            else:
                n = int(num)  # type: ignore[arg-type]
        try:
            post = nth[n % 100]
        except KeyError:
            post = nth[n % 10]
        return f"{num}{post}"
    else:
        return _sub_ord(num)


def millfn(engine, ind: int = 0) -> str:
    if ind > len(mill) - 1:
        raise NumOutOfRangeError
    return mill[ind]


def unitfn(engine, units: int, mindex: int = 0) -> str:
    return f"{unit[units]}{millfn(engine, mindex)}"


def tenfn(engine, tens, units, mindex=0) -> str:
    if tens != 1:
        tens_part = ten[tens]
        if tens and units:
            hyphen = "-"
        else:
            hyphen = ""
        unit_part = unit[units]
        mill_part = millfn(engine, mindex)
        return f"{tens_part}{hyphen}{unit_part}{mill_part}"
    return f"{teen[units]}{mill[mindex]}"


def hundfn(engine, hundreds: int, tens: int, units: int, mindex: int) -> str:
    if hundreds:
        andword = f" {engine._number_args['andword']} " if tens or units else ""
        # use unit not unitfn as simpler
        return (
            f"{unit[hundreds]} hundred{andword}"
            f"{tenfn(engine, tens, units)}{millfn(engine, mindex)}, "
        )
    if tens or units:
        return f"{tenfn(engine, tens, units)}{millfn(engine, mindex)}, "
    return ""


def group1sub(engine, mo) -> str:
    units = int(mo.group(1))
    if units == 1:
        return f" {engine._number_args['one']}, "
    elif units:
        return f"{unit[units]}, "
    else:
        return f" {engine._number_args['zero']}, "


def group1bsub(engine, mo) -> str:
    units = int(mo.group(1))
    if units:
        return f"{unit[units]}, "
    else:
        return f" {engine._number_args['zero']}, "


def group2sub(engine, mo) -> str:
    tens = int(mo.group(1))
    units = int(mo.group(2))
    if tens:
        return f"{tenfn(engine, tens, units)}, "
    if units:
        return f" {engine._number_args['zero']} {unit[units]}, "
    return f" {engine._number_args['zero']} {engine._number_args['zero']}, "


def group3sub(engine, mo) -> str:
    hundreds = int(mo.group(1))
    tens = int(mo.group(2))
    units = int(mo.group(3))
    if hundreds == 1:
        hunword = f" {engine._number_args['one']}"
    elif hundreds:
        hunword = str(unit[hundreds])
    else:
        hunword = f" {engine._number_args['zero']}"
    if tens:
        tenword = tenfn(engine, tens, units)
    elif units:
        tenword = f" {engine._number_args['zero']} {unit[units]}"
    else:
        tenword = f" {engine._number_args['zero']} {engine._number_args['zero']}"
    return f"{hunword} {tenword}, "


def hundsub(engine, mo) -> str:
    ret = hundfn(
        engine, int(mo.group(1)), int(mo.group(2)), int(mo.group(3)), engine.mill_count
    )
    engine.mill_count += 1
    return ret


def tensub(engine, mo) -> str:
    return f"{tenfn(engine, int(mo.group(1)), int(mo.group(2)), engine.mill_count)}, "


def unitsub(engine, mo) -> str:
    return f"{unitfn(engine, int(mo.group(1)), engine.mill_count)}, "


def enword(engine, num: str, group: int) -> str:
    if group == 1:
        num = DIGIT_GROUP.sub(lambda mo: group1sub(engine, mo), num)
    elif group == 2:
        num = TWO_DIGITS.sub(lambda mo: group2sub(engine, mo), num)
        num = DIGIT_GROUP.sub(lambda mo: group1bsub(engine, mo), num, 1)
    elif group == 3:
        num = THREE_DIGITS.sub(lambda mo: group3sub(engine, mo), num)
        num = TWO_DIGITS.sub(lambda mo: group2sub(engine, mo), num, 1)
        num = DIGIT_GROUP.sub(lambda mo: group1sub(engine, mo), num, 1)
    elif int(num) == 0:
        num = engine._number_args["zero"]
    elif int(num) == 1:
        num = engine._number_args["one"]
    else:
        num = num.lstrip().lstrip("0")
        engine.mill_count = 0
        # surely there's a better way to do the next bit
        mo = THREE_DIGITS_WORD.search(num)
        while mo:
            num = THREE_DIGITS_WORD.sub(lambda m: hundsub(engine, m), num, 1)
            mo = THREE_DIGITS_WORD.search(num)
        num = TWO_DIGITS_WORD.sub(lambda m: tensub(engine, m), num, 1)
        num = ONE_DIGIT_WORD.sub(lambda m: unitsub(engine, m), num, 1)
    return num


def _sub_ord(val):
    new = ordinal_suff.sub(lambda match: ordinal[match.group(1)], val)
    return new + "th" * (new == val)


def _chunk_num(engine, num, decimal, group):
    if decimal:
        max_split = -1 if group != 0 else 1
        chunks = num.split(".", max_split)
    else:
        chunks = [num]
    return _remove_last_blank(chunks)


def _remove_last_blank(chunks):
    """
    Remove the last item from chunks if it's a blank string.

    Return the resultant chunks and whether the last item was removed.
    """
    removed = chunks[-1] == ""
    result = chunks[:-1] if removed else chunks
    return result, removed


def _get_sign(num):
    return {'+': 'plus', '-': 'minus'}.get(num.lstrip()[0], '')


def number_to_words(  # noqa: C901
    engine,
    num,
    wantlist: bool = False,
    group: int = 0,
    comma: Union[Falsish, str] = ",",
    andword: str = "and",
    zero: str = "zero",
    one: str = "one",
    decimal: Union[Falsish, str] = "point",
    threshold: Optional[int] = None,
) -> Union[str, List[str]]:
    """
    Return a number in words.

    group = 1, 2 or 3 to group numbers before turning into words
    comma: define comma

    andword:
        word for 'and'. Can be set to ''.
        e.g. "one hundred and one" vs "one hundred one"

    zero: word for '0'
    one: word for '1'
    decimal: word for decimal point
    threshold: numbers above threshold not turned into words

    parameters not remembered from last call. Departure from Perl version.
    """
    engine._number_args = {"andword": andword, "zero": zero, "one": one}
    num = str(num)

    # Handle "stylistic" conversions (up to a given threshold)...
    if threshold is not None and float(num) > threshold:
        spnum = num.split(".", 1)
        while comma:
            (spnum[0], n) = FOUR_DIGIT_COMMA.subn(r"\1,\2", spnum[0])
            if n == 0:
                break
        try:
            return f"{spnum[0]}.{spnum[1]}"
        except IndexError:
            return str(spnum[0])

    if group < 0 or group > 3:
        raise BadChunkingOptionError

    sign = _get_sign(num)

    if num in nth_suff:
        num = zero

    myord = num[-2:] in nth_suff
    if myord:
        num = num[:-2]

    chunks, finalpoint = _chunk_num(engine, num, decimal, group)

    loopstart = chunks[0] == ""
    first: bool | None = not loopstart

    def _handle_chunk(chunk):
        nonlocal first

        # remove all non numeric \D
        chunk = NON_DIGIT.sub("", chunk)
        if chunk == "":
            chunk = "0"

        if group == 0 and not first:
            chunk = enword(engine, chunk, 1)
        else:
            chunk = enword(engine, chunk, group)

        if chunk[-2:] == ", ":
            chunk = chunk[:-2]
        chunk = WHITESPACES_COMMA.sub(",", chunk)

        if group == 0 and first:
            chunk = COMMA_WORD.sub(f" {andword} \\1", chunk)
        chunk = WHITESPACES.sub(" ", chunk)
        # chunk = re.sub(r"(\A\s|\s\Z)", self.blankfn, chunk)
        chunk = chunk.strip()
        if first:
            first = None
        return chunk

    chunks[loopstart:] = map(_handle_chunk, chunks[loopstart:])

    numchunks = []
    if first != 0:
        numchunks = chunks[0].split(f"{comma} ")

    if myord and numchunks:
        numchunks[-1] = _sub_ord(numchunks[-1])

    for chunk in chunks[1:]:
        numchunks.append(decimal)
        numchunks.extend(chunk.split(f"{comma} "))

    if finalpoint:
        numchunks.append(decimal)

    if wantlist:
        return [sign] * bool(sign) + numchunks

    signout = f"{sign} " if sign else ""
    valout = (
        ', '.join(numchunks)
        if group
        else ''.join(_render(numchunks, decimal, comma))
    )
    return signout + valout


def _render(chunks, decimal, comma):
    first_item = chunks.pop(0)
    yield first_item
    first = decimal is None or not first_item.endswith(decimal)
    for nc in chunks:
        if nc == decimal:
            first = False
        elif first:
            yield comma
        yield f" {nc}"
