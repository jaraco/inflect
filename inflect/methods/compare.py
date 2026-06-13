"""
Compare methods: compare, compare_nouns, compare_verbs, compare_adjs,
_plequal, _pl_reg_plurals, _pl_check_plurals_N, _pl_check_plurals_adj.
"""

from __future__ import annotations

import re
from typing import Union

from typeguard import typechecked

from .._shared import Word, Words
from ..data.plurals import (
    pl_sb_irregular_s,
    pl_sb_irregular,
    pl_sb_irregular_caps,
    pl_sb_C_a_ata,
    pl_sb_C_is_ides,
    pl_sb_C_a_ae,
    pl_sb_C_en_ina,
    pl_sb_C_um_a,
    pl_sb_C_us_i,
    pl_sb_C_on_a,
    pl_sb_C_o_i_stems,
    pl_sb_C_ex_ices,
    pl_sb_C_ix_ices,
    pl_sb_C_i,
    pl_sb_C_im,
)
from .._shared import all_classical, no_classical


class CompareMixin:
    @typechecked
    def compare(self, word1: Word, word2: Word) -> Union[str, bool]:
        """
        compare word1 and word2 for equality regardless of plurality

        return values:
        eq - the strings are equal
        p:s - word1 is the plural of word2
        s:p - word2 is the plural of word1
        p:p - word1 and word2 are two different plural forms of the one word
        False - otherwise

        >>> compare = engine().compare
        >>> compare("egg", "eggs")
        's:p'
        >>> compare('egg', 'egg')
        'eq'

        Words should not be empty.

        >>> compare('egg', '')
        Traceback (most recent call last):
        ...
        typeguard.TypeCheckError:...is not an instance of inflect.Word
        """
        norms = self.plural_noun, self.plural_verb, self.plural_adj
        results = (self._plequal(word1, word2, norm) for norm in norms)
        return next(filter(None, results), False)

    @typechecked
    def compare_nouns(self, word1: Word, word2: Word) -> Union[str, bool]:
        """
        compare word1 and word2 for equality regardless of plurality
        word1 and word2 are to be treated as nouns

        return values:
        eq - the strings are equal
        p:s - word1 is the plural of word2
        s:p - word2 is the plural of word1
        p:p - word1 and word2 are two different plural forms of the one word
        False - otherwise

        """
        return self._plequal(word1, word2, self.plural_noun)

    @typechecked
    def compare_verbs(self, word1: Word, word2: Word) -> Union[str, bool]:
        """
        compare word1 and word2 for equality regardless of plurality
        word1 and word2 are to be treated as verbs

        return values:
        eq - the strings are equal
        p:s - word1 is the plural of word2
        s:p - word2 is the plural of word1
        p:p - word1 and word2 are two different plural forms of the one word
        False - otherwise

        """
        return self._plequal(word1, word2, self.plural_verb)

    @typechecked
    def compare_adjs(self, word1: Word, word2: Word) -> Union[str, bool]:
        """
        compare word1 and word2 for equality regardless of plurality
        word1 and word2 are to be treated as adjectives

        return values:
        eq - the strings are equal
        p:s - word1 is the plural of word2
        s:p - word2 is the plural of word1
        p:p - word1 and word2 are two different plural forms of the one word
        False - otherwise

        """
        return self._plequal(word1, word2, self.plural_adj)

    def _plequal(self, word1: str, word2: str, pl) -> Union[str, bool]:
        classval = self.classical_dict.copy()
        for dictionary in (all_classical, no_classical):
            self.classical_dict = dictionary.copy()
            if word1 == word2:
                return "eq"
            if word1 == pl(word2):
                return "p:s"
            if pl(word1) == word2:
                return "s:p"
        self.classical_dict = classval.copy()

        if pl == self.plural or pl == self.plural_noun:
            if self._pl_check_plurals_N(word1, word2):
                return "p:p"
            if self._pl_check_plurals_N(word2, word1):
                return "p:p"
        if pl == self.plural or pl == self.plural_adj:
            if self._pl_check_plurals_adj(word1, word2):
                return "p:p"
        return False

    def _pl_reg_plurals(self, pair: str, stems: str, end1: str, end2: str) -> bool:
        pattern = rf"({stems})({end1}\|\1{end2}|{end2}\|\1{end1})"
        return bool(re.search(pattern, pair))

    def _pl_check_plurals_N(self, word1: str, word2: str) -> bool:
        stem_endings = (
            (pl_sb_C_a_ata, "as", "ata"),
            (pl_sb_C_is_ides, "is", "ides"),
            (pl_sb_C_a_ae, "s", "e"),
            (pl_sb_C_en_ina, "ens", "ina"),
            (pl_sb_C_um_a, "ums", "a"),
            (pl_sb_C_us_i, "uses", "i"),
            (pl_sb_C_on_a, "ons", "a"),
            (pl_sb_C_o_i_stems, "os", "i"),
            (pl_sb_C_ex_ices, "exes", "ices"),
            (pl_sb_C_ix_ices, "ixes", "ices"),
            (pl_sb_C_i, "s", "i"),
            (pl_sb_C_im, "s", "im"),
            (".*eau", "s", "x"),
            (".*ieu", "s", "x"),
            (".*tri", "xes", "ces"),
            (".{2,}[yia]n", "xes", "ges"),
        )

        words = map(Words, (word1, word2))
        pair = "|".join(word.last for word in words)

        return (
            pair in pl_sb_irregular_s.values()
            or pair in pl_sb_irregular.values()
            or pair in pl_sb_irregular_caps.values()
            or any(
                self._pl_reg_plurals(pair, stems, end1, end2)
                for stems, end1, end2 in stem_endings
            )
        )

    def _pl_check_plurals_adj(self, word1: str, word2: str) -> bool:
        word1a = word1[: word1.rfind("'")] if word1.endswith(("'s", "'")) else ""
        word2a = word2[: word2.rfind("'")] if word2.endswith(("'s", "'")) else ""

        return (
            bool(word1a)
            and bool(word2a)
            and (
                self._pl_check_plurals_N(word1a, word2a)
                or self._pl_check_plurals_N(word2a, word1a)
            )
        )
