"""
Ordinal methods: ordinal, _sub_ord.
"""

from __future__ import annotations

import re
from numbers import Number
from typing import Union

from typeguard import typechecked

from .._shared import Word
from ..data.numbers import nth, ordinal, ordinal_suff

# Pre-compiled regex
DIGIT = re.compile(r"\d")


class OrdinalMixin:
    @typechecked
    def ordinal(self, num: Union[Number, Word]) -> str:
        """
        Return the ordinal of num.

        >>> ordinal = engine().ordinal
        >>> ordinal(1)
        '1st'
        >>> ordinal('one')
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
            return self._sub_ord(num)

    @staticmethod
    def _sub_ord(val):
        new = ordinal_suff.sub(lambda match: ordinal[match.group(1)], val)
        return new + "th" * (new == val)
