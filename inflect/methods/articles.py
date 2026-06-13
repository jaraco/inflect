"""
Article methods: a, an, _indef_article.
"""

from __future__ import annotations

import re
from typing import Any, Optional, Union

from typeguard import typechecked

from .._shared import PARTITION_WORD, Word
from ..data.articles import (
    A_abbrev,
    A_explicit_a,
    A_explicit_an,
    A_ordinal_a,
    A_ordinal_an,
    A_y_cons,
)

# Pre-compiled regex patterns for article determination
INDEFINITE_ARTICLE_TEST = re.compile(r"\A(\s*)(?:an?\s+)?(.+?)(\s*)\Z", re.IGNORECASE)
SPECIAL_AN = re.compile(r"^[aefhilmnorsx]$", re.IGNORECASE)
SPECIAL_A = re.compile(r"^[bcdgjkpqtuvwyz]$", re.IGNORECASE)
SPECIAL_ABBREV_AN = re.compile(r"^[aefhilmnorsx][.-]", re.IGNORECASE)
SPECIAL_ABBREV_A = re.compile(r"^[a-z][.-]", re.IGNORECASE)
CONSONANTS = re.compile(r"^[^aeiouy]", re.IGNORECASE)
ARTICLE_SPECIAL_EU = re.compile(r"^e[uw]", re.IGNORECASE)
ARTICLE_SPECIAL_ONCE = re.compile(r"^onc?e\b", re.IGNORECASE)
ARTICLE_SPECIAL_ONETIME = re.compile(r"^onetime\b", re.IGNORECASE)
ARTICLE_SPECIAL_UNIT = re.compile(r"^uni([^nmd]|mo)", re.IGNORECASE)
ARTICLE_SPECIAL_UBA = re.compile(r"^u[bcfghjkqrst][aeiou]", re.IGNORECASE)
ARTICLE_SPECIAL_UKR = re.compile(r"^ukr", re.IGNORECASE)
SPECIAL_CAPITALS = re.compile(r"^U[NK][AIEO]?")
VOWELS = re.compile(r"^[aeiou]", re.IGNORECASE)


class ArticleMixin:
    @typechecked
    def a(self, text: Word, count: Optional[Union[int, str, Any]] = 1) -> str:
        """
        Return the appropriate indefinite article followed by text.

        The indefinite article is either 'a' or 'an'.

        If count is not one, then return count followed by text
        instead of 'a' or 'an'.

        Whitespace at the start and end is preserved.

        """
        mo = INDEFINITE_ARTICLE_TEST.search(text)
        if mo:
            word = mo.group(2)
            if not word:
                return text
            pre = mo.group(1)
            post = mo.group(3)
            result = self._indef_article(word, count)
            return f"{pre}{result}{post}"
        return ""

    an = a

    _indef_article_cases = (
        # HANDLE ORDINAL FORMS
        (A_ordinal_a, "a"),
        (A_ordinal_an, "an"),
        # HANDLE SPECIAL CASES
        (A_explicit_an, "an"),
        (SPECIAL_AN, "an"),
        (SPECIAL_A, "a"),
        # HANDLE ABBREVIATIONS
        (A_abbrev, "an"),
        (SPECIAL_ABBREV_AN, "an"),
        (SPECIAL_ABBREV_A, "a"),
        # HANDLE CONSONANTS
        (CONSONANTS, "a"),
        # HANDLE SPECIAL VOWEL-FORMS
        (ARTICLE_SPECIAL_EU, "a"),
        (ARTICLE_SPECIAL_ONCE, "a"),
        (ARTICLE_SPECIAL_ONETIME, "a"),
        (ARTICLE_SPECIAL_UNIT, "a"),
        (ARTICLE_SPECIAL_UBA, "a"),
        (ARTICLE_SPECIAL_UKR, "a"),
        (A_explicit_a, "a"),
        # HANDLE SPECIAL CAPITALS
        (SPECIAL_CAPITALS, "a"),
        # HANDLE VOWELS
        (VOWELS, "an"),
        # HANDLE y...
        # (BEFORE CERTAIN CONSONANTS IMPLIES (UNNATURALIZED) "i.." SOUND)
        (A_y_cons, "an"),
    )

    def _indef_article(self, word: str, count: Union[int, str, Any]) -> str:
        mycount = self.get_count(count)

        if mycount != 1:
            return f"{count} {word}"

        # HANDLE USER-DEFINED VARIANTS

        value = self.ud_match(word, self.A_a_user_defined)
        if value is not None:
            return f"{value} {word}"

        matches = (
            f'{article} {word}'
            for regexen, article in self._indef_article_cases
            if regexen.search(word)
        )

        # OTHERWISE, GUESS "a"
        fallback = f'a {word}'
        return next(matches, fallback)
