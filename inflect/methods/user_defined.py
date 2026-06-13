"""
User-defined pattern methods: defnoun, defverb, defadj, defa, defan,
checkpat, checkpatplural, ud_match.
"""

from __future__ import annotations

import re
from typing import Optional, Sequence, cast

from typeguard import typechecked

from .._shared import (
    BadUserDefinedPatternError,
    Word,
)

# Pre-compiled regex
DOLLAR_DIGITS = re.compile(r"\$(\d+)")


class UserDefinedMixin:
    @typechecked
    def defnoun(self, singular: Optional[Word], plural: Optional[Word]) -> int:
        """
        Set the noun plural of singular to plural.

        """
        self.checkpat(singular)
        self.checkpatplural(plural)
        self.pl_sb_user_defined.extend((singular, plural))
        self.si_sb_user_defined.extend((plural, singular))
        return 1

    @typechecked
    def defverb(
        self,
        s1: Optional[Word],
        p1: Optional[Word],
        s2: Optional[Word],
        p2: Optional[Word],
        s3: Optional[Word],
        p3: Optional[Word],
    ) -> int:
        """
        Set the verb plurals for s1, s2 and s3 to p1, p2 and p3 respectively.

        Where 1, 2 and 3 represent the 1st, 2nd and 3rd person forms of the verb.

        """
        self.checkpat(s1)
        self.checkpat(s2)
        self.checkpat(s3)
        self.checkpatplural(p1)
        self.checkpatplural(p2)
        self.checkpatplural(p3)
        self.pl_v_user_defined.extend((s1, p1, s2, p2, s3, p3))
        return 1

    @typechecked
    def defadj(self, singular: Optional[Word], plural: Optional[Word]) -> int:
        """
        Set the adjective plural of singular to plural.

        """
        self.checkpat(singular)
        self.checkpatplural(plural)
        self.pl_adj_user_defined.extend((singular, plural))
        return 1

    @typechecked
    def defa(self, pattern: Optional[Word]) -> int:
        """
        Define the indefinite article as 'a' for words matching pattern.

        """
        self.checkpat(pattern)
        self.A_a_user_defined.extend((pattern, "a"))
        return 1

    @typechecked
    def defan(self, pattern: Optional[Word]) -> int:
        """
        Define the indefinite article as 'an' for words matching pattern.

        """
        self.checkpat(pattern)
        self.A_a_user_defined.extend((pattern, "an"))
        return 1

    def checkpat(self, pattern: Optional[Word]) -> None:
        """
        check for errors in a regex pattern
        """
        if pattern is None:
            return
        try:
            re.match(pattern, "")
        except re.error as err:
            raise BadUserDefinedPatternError(pattern) from err

    def checkpatplural(self, pattern: Optional[Word]) -> None:
        """
        check for errors in a regex replace pattern
        """
        return

    @typechecked
    def ud_match(self, word: Word, wordlist: Sequence[Optional[Word]]) -> Optional[str]:
        for i in range(len(wordlist) - 2, -2, -2):  # backwards through even elements
            mo = re.search(rf"^{wordlist[i]}$", word, re.IGNORECASE)
            if mo:
                if wordlist[i + 1] is None:
                    return None
                pl = DOLLAR_DIGITS.sub(
                    r"\\1", cast(Word, wordlist[i + 1])
                )  # change $n to \n for expand
                return mo.expand(pl)
        return None
