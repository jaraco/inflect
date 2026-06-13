"""
Pluralize methods: _plnoun, _pl_special_verb, _pl_general_verb,
_pl_special_adjective, _handle_prepositional_phrase, _handle_long_compounds,
_find_pivot, get_count, and the public plural/plural_noun/plural_verb/plural_adj.
"""

from __future__ import annotations

import contextlib
import functools
import itertools
import re
from typing import Any, Optional, Union
from numbers import Number

from typeguard import typechecked
from more_itertools import windowed_complete

from .._shared import Word, Words, Falsish
from ..data.plurals import (
    pl_sb_irregular,
    pl_sb_irregular_caps,
    pl_sb_irregular_compound,
    pl_sb_U_man_mans_bysize,
    pl_sb_U_man_mans_caps_bysize,
    pl_sb_U_louse_lice_bysize,
    pl_sb_uninflected_complete,
    pl_sb_uninflected_caps,
    pl_sb_uninflected_bysize,
    pl_sb_uninflected_herd,
    pl_sb_U_ch_chs_bysize,
    pl_sb_U_ex_ices_bysize,
    pl_sb_U_ix_ices_bysize,
    pl_sb_U_um_a_bysize,
    pl_sb_U_us_i_bysize,
    pl_sb_U_on_a_bysize,
    pl_sb_U_a_ae_bysize,
    pl_sb_C_en_ina_bysize,
    pl_sb_C_ex_ices_bysize,
    pl_sb_C_ix_ices_bysize,
    pl_sb_C_um_a_bysize,
    pl_sb_C_us_i_bysize,
    pl_sb_C_us_us_bysize,
    pl_sb_C_a_ae_bysize,
    pl_sb_C_a_ata_bysize,
    pl_sb_C_is_ides_bysize,
    pl_sb_C_o_i_bysize,
    pl_sb_C_on_a_bysize,
    pl_sb_C_i_bysize,
    pl_sb_C_im_bysize,
    pl_sb_C_o_i_stems,
    pl_sb_singular_s_complete,
    pl_sb_singular_s_bysize,
    pl_sb_z_zes_bysize,
    pl_sb_ze_zes_bysize,
    pl_sb_U_o_os_complete,
    pl_sb_U_o_os_bysize,
    plverb_irregular_pres,
    plverb_irregular_non_pres,
    plverb_ambiguous_pres,
    plverb_ambiguous_pres_keys,
    plverb_ambiguous_non_pres,
    pl_v_oes_oe,
    pl_v_oes_oe_endings_size4,
    pl_v_oes_oe_endings_size5,
    pl_count_zero,
    pl_count_one,
    pl_adj_special,
    pl_adj_special_keys,
    pl_adj_poss,
    pl_adj_poss_keys,
    PL_SB_POSTFIX_ADJ_STEMS_RE,
    PLVERB_SPECIAL_S_RE,
)
from ..data.pronouns import (
    pl_pron_nom,
    pl_pron_acc,
    pl_pron_acc_keys_bysize,
    pl_prep_bysize,
    pl_prep_list_da,
    pl_sb_prep_dual_compound,
)

# Pre-compiled regex patterns
PL_SB_PREP_DUAL_COMPOUND_RE = re.compile(
    rf"^(?:{pl_sb_prep_dual_compound})$", re.IGNORECASE
)
DENOMINATOR = re.compile(r"(?P<denominator>.+)( (per|a) .+)")
WHITESPACE = re.compile(r"\s")
ENDS_WITH_S = re.compile(r"^(.*[^s])s$", re.IGNORECASE)
ENDS_WITH_APOSTROPHE_S = re.compile(r"^(.+)'s?$")


class PluralizeMixin:
    def get_count(self, count: Optional[Union[str, int]] = None) -> Union[str, int]:
        if count is None and self.persistent_count is not None:
            count = self.persistent_count

        if count is not None:
            count = (
                1
                if (
                    (str(count) in pl_count_one)
                    or (
                        self.classical_dict["zero"]
                        and str(count).lower() in pl_count_zero
                    )
                )
                else 2
            )
        else:
            count = ""
        return count

    # @profile
    def _plnoun(  # noqa: C901
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> str:
        count = self.get_count(count)

        # DEFAULT TO PLURAL

        if count == 1:
            return word

        # HANDLE USER-DEFINED NOUNS

        value = self.ud_match(word, self.pl_sb_user_defined)
        if value is not None:
            return value

        # HANDLE EMPTY WORD, SINGULAR COUNT AND UNINFLECTED PLURALS

        if word == "":
            return word

        word = Words(word)

        if word.last.lower() in pl_sb_uninflected_complete:
            if len(word.split_) >= 3:
                return self._handle_long_compounds(word, count=2) or word
            return word

        if word in pl_sb_uninflected_caps:
            return word

        for k, v in pl_sb_uninflected_bysize.items():
            if word.lowered[-k:] in v:
                return word

        if self.classical_dict["herd"] and word.last.lower() in pl_sb_uninflected_herd:
            return word

        # HANDLE COMPOUNDS ("Governor General", "mother-in-law", "aide-de-camp", ETC.)

        mo = PL_SB_POSTFIX_ADJ_STEMS_RE.search(word)
        if mo and mo.group(2) != "":
            return f"{self._plnoun(mo.group(1), 2)}{mo.group(2)}"

        if " a " in word.lowered or "-a-" in word.lowered:
            mo = PL_SB_PREP_DUAL_COMPOUND_RE.search(word)
            if mo and mo.group(2) != "" and mo.group(3) != "":
                return (
                    f"{self._plnoun(mo.group(1), 2)}"
                    f"{mo.group(2)}"
                    f"{self._plnoun(mo.group(3))}"
                )

        if len(word.split_) >= 3:
            handled_words = self._handle_long_compounds(word, count=2)
            if handled_words is not None:
                return handled_words

        # only pluralize denominators in units
        mo = DENOMINATOR.search(word.lowered)
        if mo:
            index = len(mo.group("denominator"))
            return f"{self._plnoun(word[:index])}{word[index:]}"

        # handle units given in degrees (only accept if
        # there is no more than one word following)
        # degree Celsius => degrees Celsius but degree
        # fahrenheit hour => degree fahrenheit hours
        if len(word.split_) >= 2 and word.split_[-2] == "degree":
            return " ".join([self._plnoun(word.first)] + word.split_[1:])

        with contextlib.suppress(ValueError):
            return self._handle_prepositional_phrase(
                word.lowered,
                functools.partial(self._plnoun, count=2),
                '-',
            )

        # HANDLE PRONOUNS

        for k, v in pl_pron_acc_keys_bysize.items():
            if word.lowered[-k:] in v:  # ends with accusative pronoun
                for pk, pv in pl_prep_bysize.items():
                    if word.lowered[:pk] in pv:  # starts with a prep
                        if word.lowered.split() == [
                            word.lowered[:pk],
                            word.lowered[-k:],
                        ]:
                            # only whitespace in between
                            return word.lowered[:-k] + pl_pron_acc[word.lowered[-k:]]

        try:
            return pl_pron_nom[word.lowered]
        except KeyError:
            pass

        try:
            return pl_pron_acc[word.lowered]
        except KeyError:
            pass

        # HANDLE ISOLATED IRREGULAR PLURALS

        if word.last in pl_sb_irregular_caps:
            llen = len(word.last)
            return f"{word[:-llen]}{pl_sb_irregular_caps[word.last]}"

        lowered_last = word.last.lower()
        if lowered_last in pl_sb_irregular:
            llen = len(lowered_last)
            return f"{word[:-llen]}{pl_sb_irregular[lowered_last]}"

        dash_split = word.lowered.split('-')
        if (" ".join(dash_split[-2:])).lower() in pl_sb_irregular_compound:
            llen = len(
                " ".join(dash_split[-2:])
            )  # TODO: what if 2 spaces between these words?
            return (
                f"{word[:-llen]}"
                f"{pl_sb_irregular_compound[(' '.join(dash_split[-2:])).lower()]}"
            )

        if word.lowered[-3:] == "quy":
            return f"{word[:-1]}ies"

        if word.lowered[-6:] == "person":
            if self.classical_dict["persons"]:
                return f"{word}s"
            else:
                return f"{word[:-4]}ople"

        # HANDLE FAMILIES OF IRREGULAR PLURALS

        if word.lowered[-3:] == "man":
            for k, v in pl_sb_U_man_mans_bysize.items():
                if word.lowered[-k:] in v:
                    return f"{word}s"
            for k, v in pl_sb_U_man_mans_caps_bysize.items():
                if word[-k:] in v:
                    return f"{word}s"
            return f"{word[:-3]}men"
        if word.lowered[-5:] == "mouse":
            return f"{word[:-5]}mice"
        if word.lowered[-5:] == "louse":
            v = pl_sb_U_louse_lice_bysize.get(len(word))
            if v and word.lowered in v:
                return f"{word[:-5]}lice"
            return f"{word}s"
        if word.lowered[-5:] == "goose":
            return f"{word[:-5]}geese"
        if word.lowered[-5:] == "tooth":
            return f"{word[:-5]}teeth"
        if word.lowered[-4:] == "foot":
            return f"{word[:-4]}feet"
        if word.lowered[-4:] == "taco":
            return f"{word[:-5]}tacos"

        if word.lowered == "die":
            return "dice"

        # HANDLE UNASSIMILATED IMPORTS

        if word.lowered[-4:] == "ceps":
            return word
        if word.lowered[-4:] == "zoon":
            return f"{word[:-2]}a"
        if word.lowered[-3:] in ("cis", "sis", "xis"):
            return f"{word[:-2]}es"

        for lastlet, d, numend, post in (
            ("h", pl_sb_U_ch_chs_bysize, None, "s"),
            ("x", pl_sb_U_ex_ices_bysize, -2, "ices"),
            ("x", pl_sb_U_ix_ices_bysize, -2, "ices"),
            ("m", pl_sb_U_um_a_bysize, -2, "a"),
            ("s", pl_sb_U_us_i_bysize, -2, "i"),
            ("n", pl_sb_U_on_a_bysize, -2, "a"),
            ("a", pl_sb_U_a_ae_bysize, None, "e"),
        ):
            if word.lowered[-1] == lastlet:  # this test to add speed
                for k, v in d.items():
                    if word.lowered[-k:] in v:
                        return word[:numend] + post

        # HANDLE INCOMPLETELY ASSIMILATED IMPORTS

        if self.classical_dict["ancient"]:
            if word.lowered[-4:] == "trix":
                return f"{word[:-1]}ces"
            if word.lowered[-3:] in ("eau", "ieu"):
                return f"{word}x"
            if word.lowered[-3:] in ("ynx", "inx", "anx") and len(word) > 4:
                return f"{word[:-1]}ges"

            for lastlet, d, numend, post in (
                ("n", pl_sb_C_en_ina_bysize, -2, "ina"),
                ("x", pl_sb_C_ex_ices_bysize, -2, "ices"),
                ("x", pl_sb_C_ix_ices_bysize, -2, "ices"),
                ("m", pl_sb_C_um_a_bysize, -2, "a"),
                ("s", pl_sb_C_us_i_bysize, -2, "i"),
                ("s", pl_sb_C_us_us_bysize, None, ""),
                ("a", pl_sb_C_a_ae_bysize, None, "e"),
                ("a", pl_sb_C_a_ata_bysize, None, "ta"),
                ("s", pl_sb_C_is_ides_bysize, -1, "des"),
                ("o", pl_sb_C_o_i_bysize, -1, "i"),
                ("n", pl_sb_C_on_a_bysize, -2, "a"),
            ):
                if word.lowered[-1] == lastlet:  # this test to add speed
                    for k, v in d.items():
                        if word.lowered[-k:] in v:
                            return word[:numend] + post

            for d, numend, post in (
                (pl_sb_C_i_bysize, None, "i"),
                (pl_sb_C_im_bysize, None, "im"),
            ):
                for k, v in d.items():
                    if word.lowered[-k:] in v:
                        return word[:numend] + post

        # HANDLE SINGULAR NOUNS ENDING IN ...s OR OTHER SILIBANTS

        if lowered_last in pl_sb_singular_s_complete:
            return f"{word}es"

        for k, v in pl_sb_singular_s_bysize.items():
            if word.lowered[-k:] in v:
                return f"{word}es"

        if word.lowered[-2:] == "es" and word[0] == word[0].upper():
            return f"{word}es"

        if word.lowered[-1] == "z":
            for k, v in pl_sb_z_zes_bysize.items():
                if word.lowered[-k:] in v:
                    return f"{word}es"

            if word.lowered[-2:-1] != "z":
                return f"{word}zes"

        if word.lowered[-2:] == "ze":
            for k, v in pl_sb_ze_zes_bysize.items():
                if word.lowered[-k:] in v:
                    return f"{word}s"

        if word.lowered[-2:] in ("ch", "sh", "zz", "ss") or word.lowered[-1] == "x":
            return f"{word}es"

        # HANDLE ...f -> ...ves

        if word.lowered[-3:] in ("elf", "alf", "olf"):
            return f"{word[:-1]}ves"
        if word.lowered[-3:] == "eaf" and word.lowered[-4:-3] != "d":
            return f"{word[:-1]}ves"
        if word.lowered[-4:] in ("nife", "life", "wife"):
            return f"{word[:-2]}ves"
        if word.lowered[-3:] == "arf":
            return f"{word[:-1]}ves"

        # HANDLE ...y

        if word.lowered[-1] == "y":
            if word.lowered[-2:-1] in "aeiou" or len(word) == 1:
                return f"{word}s"

            if self.classical_dict["names"]:
                if word.lowered[-1] == "y" and word[0] == word[0].upper():
                    return f"{word}s"

            return f"{word[:-1]}ies"

        # HANDLE ...o

        if lowered_last in pl_sb_U_o_os_complete:
            return f"{word}s"

        for k, v in pl_sb_U_o_os_bysize.items():
            if word.lowered[-k:] in v:
                return f"{word}s"

        if word.lowered[-2:] in ("ao", "eo", "io", "oo", "uo"):
            return f"{word}s"

        if word.lowered[-1] == "o":
            return f"{word}es"

        # OTHERWISE JUST ADD ...s

        return f"{word}s"

    @classmethod
    def _handle_prepositional_phrase(cls, phrase, transform, sep):
        """
        Given a word or phrase possibly separated by sep, parse out
        the prepositional phrase and apply the transform to the word
        preceding the prepositional phrase.

        Raise ValueError if the pivot is not found or if at least two
        separators are not found.

        >>> engine._handle_prepositional_phrase("man-of-war", str.upper, '-')
        'MAN-of-war'
        >>> engine._handle_prepositional_phrase("man of war", str.upper, ' ')
        'MAN of war'
        """
        parts = phrase.split(sep)
        if len(parts) < 3:
            raise ValueError("Cannot handle words with fewer than two separators")

        pivot = cls._find_pivot(parts, pl_prep_list_da)

        transformed = transform(parts[pivot - 1]) or parts[pivot - 1]
        return " ".join(
            parts[: pivot - 1] + [sep.join([transformed, parts[pivot], ''])]
        ) + " ".join(parts[(pivot + 1) :])

    def _handle_long_compounds(self, word: Words, count: int):
        """
        Handles the plural and singular for compound `Words` that
        have three or more words, based on the given count.

        >>> engine()._handle_long_compounds(Words("pair of scissors"), 2)
        'pairs of scissors'
        >>> engine()._handle_long_compounds(Words("men beyond hills"), 1)
        'man beyond hills'
        """
        inflection = self._sinoun if count == 1 else self._plnoun
        solutions = (
            " ".join(
                itertools.chain(
                    leader,
                    [inflection(cand, count), prep],  # type: ignore[operator]
                    trailer,
                )
            )
            for leader, (cand, prep), trailer in windowed_complete(word.split_, 2)
            if prep in pl_prep_list_da
        )
        return next(solutions, None)

    @staticmethod
    def _find_pivot(words, candidates):
        pivots = (
            index for index in range(1, len(words) - 1) if words[index] in candidates
        )
        try:
            return next(pivots)
        except StopIteration:
            raise ValueError("No pivot found") from None

    def _pl_special_verb(  # noqa: C901
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> Union[str, bool]:
        if self.classical_dict["zero"] and str(count).lower() in pl_count_zero:
            return False
        count = self.get_count(count)

        if count == 1:
            return word

        # HANDLE USER-DEFINED VERBS

        value = self.ud_match(word, self.pl_v_user_defined)
        if value is not None:
            return value

        # HANDLE IRREGULAR PRESENT TENSE (SIMPLE AND COMPOUND)

        try:
            words = Words(word)
        except IndexError:
            return False  # word is ''

        if words.first in plverb_irregular_pres:
            return f"{plverb_irregular_pres[words.first]}{words[len(words.first) :]}"

        # HANDLE IRREGULAR FUTURE, PRETERITE AND PERFECT TENSES

        if words.first in plverb_irregular_non_pres:
            return word

        # HANDLE PRESENT NEGATIONS (SIMPLE AND COMPOUND)

        if words.first.endswith("n't") and words.first[:-3] in plverb_irregular_pres:
            return (
                f"{plverb_irregular_pres[words.first[:-3]]}n't"
                f"{words[len(words.first) :]}"
            )

        if words.first.endswith("n't"):
            return word

        # HANDLE SPECIAL CASES

        mo = PLVERB_SPECIAL_S_RE.search(word)
        if mo:
            return False
        if WHITESPACE.search(word):
            return False

        if words.lowered == "quizzes":
            return "quiz"

        # HANDLE STANDARD 3RD PERSON (CHOP THE ...(e)s OFF SINGLE WORDS)

        if (
            words.lowered[-4:] in ("ches", "shes", "zzes", "sses")
            or words.lowered[-3:] == "xes"
        ):
            return words[:-2]

        if words.lowered[-3:] == "ies" and len(words) > 3:
            return words.lowered[:-3] + "y"

        if (
            words.last.lower() in pl_v_oes_oe
            or words.lowered[-4:] in pl_v_oes_oe_endings_size4
            or words.lowered[-5:] in pl_v_oes_oe_endings_size5
        ):
            return words[:-1]

        if words.lowered.endswith("oes") and len(words) > 3:
            return words.lowered[:-2]

        mo = ENDS_WITH_S.search(words)
        if mo:
            return mo.group(1)

        # OTHERWISE, A REGULAR VERB (HANDLE ELSEWHERE)

        return False

    def _pl_general_verb(
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> str:
        count = self.get_count(count)

        if count == 1:
            return word

        # HANDLE AMBIGUOUS PRESENT TENSES  (SIMPLE AND COMPOUND)

        mo = plverb_ambiguous_pres_keys.search(word)
        if mo:
            return f"{plverb_ambiguous_pres[mo.group(1).lower()]}{mo.group(2)}"

        # HANDLE AMBIGUOUS PRETERITE AND PERFECT TENSES

        mo = plverb_ambiguous_non_pres.search(word)
        if mo:
            return word

        # OTHERWISE, 1st OR 2ND PERSON IS UNINFLECTED

        return word

    def _pl_special_adjective(
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> Union[str, bool]:
        count = self.get_count(count)

        if count == 1:
            return word

        # HANDLE USER-DEFINED ADJECTIVES

        value = self.ud_match(word, self.pl_adj_user_defined)
        if value is not None:
            return value

        # HANDLE KNOWN CASES

        mo = pl_adj_special_keys.search(word)
        if mo:
            return pl_adj_special[mo.group(1).lower()]

        # HANDLE POSSESSIVES

        mo = pl_adj_poss_keys.search(word)
        if mo:
            return pl_adj_poss[mo.group(1).lower()]

        mo = ENDS_WITH_APOSTROPHE_S.search(word)
        if mo:
            pl = self.plural_noun(mo.group(1))
            trailing_s = "" if pl[-1] == "s" else "s"
            return f"{pl}'{trailing_s}"

        # OTHERWISE, NO IDEA

        return False

    # PUBLIC API

    @typechecked
    def plural(self, text: Word, count: Optional[Union[str, int, Any]] = None) -> str:
        """
        Return the plural of text.

        If count supplied, then return text if count is one of:
            1, a, an, one, each, every, this, that

        otherwise return the plural.

        Whitespace at the start and end is preserved.

        """
        pre, word, post = self.partition_word(text)
        if not word:
            return text
        plural = self.postprocess(
            word,
            self._pl_special_adjective(word, count)
            or self._pl_special_verb(word, count)
            or self._plnoun(word, count),
        )
        return f"{pre}{plural}{post}"

    @typechecked
    def plural_noun(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        """
        Return the plural of text, where text is a noun.

        If count supplied, then return text if count is one of:
            1, a, an, one, each, every, this, that

        otherwise return the plural.

        Whitespace at the start and end is preserved.

        """
        pre, word, post = self.partition_word(text)
        if not word:
            return text
        plural = self.postprocess(word, self._plnoun(word, count))
        return f"{pre}{plural}{post}"

    @typechecked
    def plural_verb(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        """
        Return the plural of text, where text is a verb.

        If count supplied, then return text if count is one of:
            1, a, an, one, each, every, this, that

        otherwise return the plural.

        Whitespace at the start and end is preserved.

        """
        pre, word, post = self.partition_word(text)
        if not word:
            return text
        plural = self.postprocess(
            word,
            self._pl_special_verb(word, count) or self._pl_general_verb(word, count),
        )
        return f"{pre}{plural}{post}"

    @typechecked
    def plural_adj(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        """
        Return the plural of text, where text is an adjective.

        If count supplied, then return text if count is one of:
            1, a, an, one, each, every, this, that

        otherwise return the plural.

        Whitespace at the start and end is preserved.

        """
        pre, word, post = self.partition_word(text)
        if not word:
            return text
        plural = self.postprocess(word, self._pl_special_adjective(word, count) or word)
        return f"{pre}{plural}{post}"
