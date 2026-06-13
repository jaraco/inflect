"""
Number-to-words methods: number_to_words, enword, millfn, unitfn,
tenfn, hundfn, group*sub, hundsub, tensub, unitsub, _sub_ord,
_chunk_num, _remove_last_blank, _get_sign, _render.
"""

from __future__ import annotations

import re
from numbers import Number
from typing import Any, Dict, List, Match, Optional, Union

from typeguard import typechecked

from .._shared import BadChunkingOptionError, Falsish, NumOutOfRangeError, Word
from ..data.numbers import mill, nth, nth_suff, ordinal, ordinal_suff, teen, ten, unit

# Pre-compiled regex patterns
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


class NumberWordsMixin:
    def millfn(self, ind: int = 0) -> str:
        if ind > len(mill) - 1:
            raise NumOutOfRangeError
        return mill[ind]

    def unitfn(self, units: int, mindex: int = 0) -> str:
        return f"{unit[units]}{self.millfn(mindex)}"

    def tenfn(self, tens, units, mindex=0) -> str:
        if tens != 1:
            tens_part = ten[tens]
            if tens and units:
                hyphen = "-"
            else:
                hyphen = ""
            unit_part = unit[units]
            mill_part = self.millfn(mindex)
            return f"{tens_part}{hyphen}{unit_part}{mill_part}"
        return f"{teen[units]}{mill[mindex]}"

    def hundfn(self, hundreds: int, tens: int, units: int, mindex: int) -> str:
        if hundreds:
            andword = f" {self._number_args['andword']} " if tens or units else ""
            # use unit not unitfn as simpler
            return (
                f"{unit[hundreds]} hundred{andword}"
                f"{self.tenfn(tens, units)}{self.millfn(mindex)}, "
            )
        if tens or units:
            return f"{self.tenfn(tens, units)}{self.millfn(mindex)}, "
        return ""

    def group1sub(self, mo: Match) -> str:
        units = int(mo.group(1))
        if units == 1:
            return f" {self._number_args['one']}, "
        elif units:
            return f"{unit[units]}, "
        else:
            return f" {self._number_args['zero']}, "

    def group1bsub(self, mo: Match) -> str:
        units = int(mo.group(1))
        if units:
            return f"{unit[units]}, "
        else:
            return f" {self._number_args['zero']}, "

    def group2sub(self, mo: Match) -> str:
        tens = int(mo.group(1))
        units = int(mo.group(2))
        if tens:
            return f"{self.tenfn(tens, units)}, "
        if units:
            return f" {self._number_args['zero']} {unit[units]}, "
        return f" {self._number_args['zero']} {self._number_args['zero']}, "

    def group3sub(self, mo: Match) -> str:
        hundreds = int(mo.group(1))
        tens = int(mo.group(2))
        units = int(mo.group(3))
        if hundreds == 1:
            hunword = f" {self._number_args['one']}"
        elif hundreds:
            hunword = str(unit[hundreds])
        else:
            hunword = f" {self._number_args['zero']}"
        if tens:
            tenword = self.tenfn(tens, units)
        elif units:
            tenword = f" {self._number_args['zero']} {unit[units]}"
        else:
            tenword = f" {self._number_args['zero']} {self._number_args['zero']}"
        return f"{hunword} {tenword}, "

    def hundsub(self, mo: Match) -> str:
        ret = self.hundfn(
            int(mo.group(1)), int(mo.group(2)), int(mo.group(3)), self.mill_count
        )
        self.mill_count += 1
        return ret

    def tensub(self, mo: Match) -> str:
        return f"{self.tenfn(int(mo.group(1)), int(mo.group(2)), self.mill_count)}, "

    def unitsub(self, mo: Match) -> str:
        return f"{self.unitfn(int(mo.group(1)), self.mill_count)}, "

    def enword(self, num: str, group: int) -> str:
        # import pdb
        # pdb.set_trace()

        if group == 1:
            num = DIGIT_GROUP.sub(self.group1sub, num)
        elif group == 2:
            num = TWO_DIGITS.sub(self.group2sub, num)
            num = DIGIT_GROUP.sub(self.group1bsub, num, 1)
        elif group == 3:
            num = THREE_DIGITS.sub(self.group3sub, num)
            num = TWO_DIGITS.sub(self.group2sub, num, 1)
            num = DIGIT_GROUP.sub(self.group1sub, num, 1)
        elif int(num) == 0:
            num = self._number_args["zero"]
        elif int(num) == 1:
            num = self._number_args["one"]
        else:
            num = num.lstrip().lstrip("0")
            self.mill_count = 0
            # surely there's a better way to do the next bit
            mo = THREE_DIGITS_WORD.search(num)
            while mo:
                num = THREE_DIGITS_WORD.sub(self.hundsub, num, 1)
                mo = THREE_DIGITS_WORD.search(num)
            num = TWO_DIGITS_WORD.sub(self.tensub, num, 1)
            num = ONE_DIGIT_WORD.sub(self.unitsub, num, 1)
        return num

    @classmethod
    def _chunk_num(cls, num, decimal, group):
        if decimal:
            max_split = -1 if group != 0 else 1
            chunks = num.split(".", max_split)
        else:
            chunks = [num]
        return cls._remove_last_blank(chunks)

    @staticmethod
    def _remove_last_blank(chunks):
        """
        Remove the last item from chunks if it's a blank string.

        Return the resultant chunks and whether the last item was removed.
        """
        removed = chunks[-1] == ""
        result = chunks[:-1] if removed else chunks
        return result, removed

    @staticmethod
    def _get_sign(num):
        return {'+': 'plus', '-': 'minus'}.get(num.lstrip()[0], '')

    @typechecked
    def number_to_words(  # noqa: C901
        self,
        num: Union[Number, Word],
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
        self._number_args = {"andword": andword, "zero": zero, "one": one}
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

        sign = self._get_sign(num)

        if num in nth_suff:
            num = zero

        myord = num[-2:] in nth_suff
        if myord:
            num = num[:-2]

        chunks, finalpoint = self._chunk_num(num, decimal, group)

        loopstart = chunks[0] == ""
        first: bool | None = not loopstart

        def _handle_chunk(chunk):
            nonlocal first

            # remove all non numeric \D
            chunk = NON_DIGIT.sub("", chunk)
            if chunk == "":
                chunk = "0"

            if group == 0 and not first:
                chunk = self.enword(chunk, 1)
            else:
                chunk = self.enword(chunk, group)

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
            numchunks[-1] = self._sub_ord(numchunks[-1])

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
            else ''.join(self._render(numchunks, decimal, comma))
        )
        return signout + valout

    @staticmethod
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
