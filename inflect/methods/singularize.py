"""
Singularize methods: _sinoun, singular_noun.
"""

from __future__ import annotations

import contextlib
import functools
import re
from typing import Any, Literal, Optional, Union

from typeguard import typechecked

from .._shared import BadGenderError, Words
from ..data.plurals import (
    pl_sb_irregular_caps,
    pl_sb_irregular_compound,
    pl_sb_uninflected_complete,
    pl_sb_uninflected_caps,
    pl_sb_uninflected_bysize,
    pl_sb_uninflected_herd,
    pl_sb_C_us_us,
    pl_sb_C_us_us_bysize,
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
    pl_sb_C_a_ae_bysize,
    pl_sb_C_a_ata_bysize,
    pl_sb_C_is_ides_bysize,
    pl_sb_C_o_i_bysize,
    pl_sb_C_on_a_bysize,
    pl_sb_C_i_bysize,
    pl_sb_C_im_bysize,
    pl_sb_U_man_mans_bysize,
    pl_sb_U_man_mans_caps_bysize,
    pl_sb_U_louse_lice_bysize,
    pl_sb_U_o_os_complete,
    pl_sb_U_o_os_bysize,
    pl_sb_singular_s_complete,
    PL_SB_POSTFIX_ADJ_STEMS_RE,
    si_sb_ois_oi_case,
    si_sb_uses_use_case,
    si_sb_uses_use,
    si_sb_ies_ie_case,
    si_sb_ies_ie,
    si_sb_oes_oe_case,
    si_sb_oes_oe,
    si_sb_z_zes,
    si_sb_zzes_zz,
    si_sb_ches_che_case,
    si_sb_ches_che,
    si_sb_xes_xe,
    si_sb_sses_sse_case,
    si_sb_sses_sse,
    si_sb_ves_ve_case,
    si_sb_ves_ve,
    si_sb_es_is,
    si_sb_singular_s_complete,
    si_sb_singular_s_bysize,
    si_sb_C_en_ina_bysize,
    si_sb_C_ex_ices_bysize,
    si_sb_C_ix_ices_bysize,
    si_sb_C_um_a_bysize,
    si_sb_C_us_i_bysize,
    si_sb_C_a_ae_bysize,
    si_sb_C_a_ata_bysize,
    si_sb_C_is_ides_bysize,
    si_sb_C_o_i_bysize,
    si_sb_C_on_a_bysize,
    si_sb_C_im_bysize,
    si_sb_C_i_bysize,
    si_sb_U_ch_chs_bysize,
    si_sb_U_ex_ices_bysize,
    si_sb_U_ix_ices_bysize,
    si_sb_U_um_a_bysize,
    si_sb_U_us_i_bysize,
    si_sb_U_on_a_bysize,
    si_sb_U_a_ae_bysize,
    si_sb_U_louse_lice_bysize,
    si_sb_U_man_mans_bysize,
    si_sb_U_man_mans_caps_bysize,
    si_sb_U_o_os_complete,
    si_sb_U_o_os_bysize,
)
from ..data.singulars import si_sb_irregular, si_sb_irregular_caps, si_sb_irregular_compound
from ..data.pronouns import (
    si_pron_acc_keys_bysize,
    pl_prep_bysize,
    get_si_pron,
)


class SingularizeMixin:
    # @profile
    def _sinoun(  # noqa: C901
        self,
        word: str,
        count: Optional[Union[str, int]] = None,
        gender: Optional[str] = None,
    ) -> Union[str, bool]:
        count = self.get_count(count)

        # DEFAULT TO PLURAL

        if count == 2:
            return word

        # SET THE GENDER

        try:
            if gender is None:
                gender = self.thegender
            elif gender not in (
                "neuter",
                "feminine",
                "masculine",
                "gender-neutral",
                "feminine or masculine",
                "masculine or feminine",
            ):
                raise BadGenderError
        except (TypeError, IndexError) as err:
            raise BadGenderError from err

        # HANDLE USER-DEFINED NOUNS

        value = self.ud_match(word, self.si_sb_user_defined)
        if value is not None:
            return value

        # HANDLE EMPTY WORD, SINGULAR COUNT AND UNINFLECTED PLURALS

        if word == "":
            return word

        if word in si_sb_ois_oi_case:
            return word[:-1]

        words = Words(word)

        if words.last.lower() in pl_sb_uninflected_complete:
            if len(words.split_) >= 3:
                return self._handle_long_compounds(words, count=1) or word
            return word

        if word in pl_sb_uninflected_caps:
            return word

        for k, v in pl_sb_uninflected_bysize.items():
            if words.lowered[-k:] in v:
                return word

        if self.classical_dict["herd"] and words.last.lower() in pl_sb_uninflected_herd:
            return word

        if words.last.lower() in pl_sb_C_us_us:
            return word if self.classical_dict["ancient"] else False

        # HANDLE COMPOUNDS ("Governor General", "mother-in-law", "aide-de-camp", ETC.)

        mo = PL_SB_POSTFIX_ADJ_STEMS_RE.search(word)
        if mo and mo.group(2) != "":
            return f"{self._sinoun(mo.group(1), 1, gender=gender)}{mo.group(2)}"

        with contextlib.suppress(ValueError):
            return self._handle_prepositional_phrase(
                words.lowered,
                functools.partial(self._sinoun, count=1, gender=gender),
                ' ',
            )

        with contextlib.suppress(ValueError):
            return self._handle_prepositional_phrase(
                words.lowered,
                functools.partial(self._sinoun, count=1, gender=gender),
                '-',
            )

        # HANDLE PRONOUNS

        for k, v in si_pron_acc_keys_bysize.items():
            if words.lowered[-k:] in v:  # ends with accusative pronoun
                for pk, pv in pl_prep_bysize.items():
                    if words.lowered[:pk] in pv:  # starts with a prep
                        if words.lowered.split() == [
                            words.lowered[:pk],
                            words.lowered[-k:],
                        ]:
                            # only whitespace in between
                            return words.lowered[:-k] + get_si_pron(
                                "acc", words.lowered[-k:], gender
                            )

        try:
            return get_si_pron("nom", words.lowered, gender)
        except KeyError:
            pass

        try:
            return get_si_pron("acc", words.lowered, gender)
        except KeyError:
            pass

        # HANDLE ISOLATED IRREGULAR PLURALS

        if words.last in si_sb_irregular_caps:
            llen = len(words.last)
            return f"{word[:-llen]}{si_sb_irregular_caps[words.last]}"

        if words.last.lower() in si_sb_irregular:
            llen = len(words.last.lower())
            return f"{word[:-llen]}{si_sb_irregular[words.last.lower()]}"

        dash_split = words.lowered.split("-")
        if (" ".join(dash_split[-2:])).lower() in si_sb_irregular_compound:
            llen = len(
                " ".join(dash_split[-2:])
            )  # TODO: what if 2 spaces between these words?
            return "{}{}".format(
                word[:-llen],
                si_sb_irregular_compound[(" ".join(dash_split[-2:])).lower()],
            )

        if words.lowered[-5:] == "quies":
            return word[:-3] + "y"

        if words.lowered[-7:] == "persons":
            return word[:-1]
        if words.lowered[-6:] == "people":
            return word[:-4] + "rson"

        # HANDLE FAMILIES OF IRREGULAR PLURALS

        if words.lowered[-4:] == "mans":
            for k, v in si_sb_U_man_mans_bysize.items():
                if words.lowered[-k:] in v:
                    return word[:-1]
            for k, v in si_sb_U_man_mans_caps_bysize.items():
                if word[-k:] in v:
                    return word[:-1]
        if words.lowered[-3:] == "men":
            return word[:-3] + "man"
        if words.lowered[-4:] == "mice":
            return word[:-4] + "mouse"
        if words.lowered[-4:] == "lice":
            v = si_sb_U_louse_lice_bysize.get(len(word))
            if v and words.lowered in v:
                return word[:-4] + "louse"
        if words.lowered[-5:] == "geese":
            return word[:-5] + "goose"
        if words.lowered[-5:] == "teeth":
            return word[:-5] + "tooth"
        if words.lowered[-4:] == "feet":
            return word[:-4] + "foot"

        if words.lowered == "dice":
            return "die"

        # HANDLE UNASSIMILATED IMPORTS

        if words.lowered[-4:] == "ceps":
            return word
        if words.lowered[-3:] == "zoa":
            return word[:-1] + "on"

        for lastlet, d, unass_numend, post in (
            ("s", si_sb_U_ch_chs_bysize, -1, ""),
            ("s", si_sb_U_ex_ices_bysize, -4, "ex"),
            ("s", si_sb_U_ix_ices_bysize, -4, "ix"),
            ("a", si_sb_U_um_a_bysize, -1, "um"),
            ("i", si_sb_U_us_i_bysize, -1, "us"),
            ("a", si_sb_U_on_a_bysize, -1, "on"),
            ("e", si_sb_U_a_ae_bysize, -1, ""),
        ):
            if words.lowered[-1] == lastlet:  # this test to add speed
                for k, v in d.items():
                    if words.lowered[-k:] in v:
                        return word[:unass_numend] + post

        # HANDLE INCOMPLETELY ASSIMILATED IMPORTS

        if self.classical_dict["ancient"]:
            if words.lowered[-6:] == "trices":
                return word[:-3] + "x"
            if words.lowered[-4:] in ("eaux", "ieux"):
                return word[:-1]
            if words.lowered[-5:] in ("ynges", "inges", "anges") and len(word) > 6:
                return word[:-3] + "x"

            for lastlet, d, class_numend, post in (
                ("a", si_sb_C_en_ina_bysize, -3, "en"),
                ("s", si_sb_C_ex_ices_bysize, -4, "ex"),
                ("s", si_sb_C_ix_ices_bysize, -4, "ix"),
                ("a", si_sb_C_um_a_bysize, -1, "um"),
                ("i", si_sb_C_us_i_bysize, -1, "us"),
                ("s", pl_sb_C_us_us_bysize, None, ""),
                ("e", si_sb_C_a_ae_bysize, -1, ""),
                ("a", si_sb_C_a_ata_bysize, -2, ""),
                ("s", si_sb_C_is_ides_bysize, -3, "s"),
                ("i", si_sb_C_o_i_bysize, -1, "o"),
                ("a", si_sb_C_on_a_bysize, -1, "on"),
                ("m", si_sb_C_im_bysize, -2, ""),
                ("i", si_sb_C_i_bysize, -1, ""),
            ):
                if words.lowered[-1] == lastlet:  # this test to add speed
                    for k, v in d.items():
                        if words.lowered[-k:] in v:
                            return word[:class_numend] + post

        # HANDLE PLURLS ENDING IN uses -> use

        if (
            words.lowered[-6:] == "houses"
            or word in si_sb_uses_use_case
            or words.last.lower() in si_sb_uses_use
        ):
            return word[:-1]

        # HANDLE PLURLS ENDING IN ies -> ie

        if word in si_sb_ies_ie_case or words.last.lower() in si_sb_ies_ie:
            return word[:-1]

        # HANDLE PLURLS ENDING IN oes -> oe

        if (
            words.lowered[-5:] == "shoes"
            or word in si_sb_oes_oe_case
            or words.last.lower() in si_sb_oes_oe
        ):
            return word[:-1]

        # HANDLE SINGULAR NOUNS ENDING IN ...s OR OTHER SILIBANTS

        if word in si_sb_sses_sse_case or words.last.lower() in si_sb_sses_sse:
            return word[:-1]

        if words.last.lower() in si_sb_singular_s_complete:
            return word[:-2]

        for k, v in si_sb_singular_s_bysize.items():
            if words.lowered[-k:] in v:
                return word[:-2]

        if words.lowered[-4:] == "eses" and word[0] == word[0].upper():
            return word[:-2]

        if words.last.lower() in si_sb_z_zes:
            return word[:-2]

        if words.last.lower() in si_sb_zzes_zz:
            return word[:-2]

        if words.lowered[-4:] == "zzes":
            return word[:-3]

        if word in si_sb_ches_che_case or words.last.lower() in si_sb_ches_che:
            return word[:-1]

        if words.lowered[-4:] in ("ches", "shes"):
            return word[:-2]

        if words.last.lower() in si_sb_xes_xe:
            return word[:-1]

        if words.lowered[-3:] == "xes":
            return word[:-2]

        # HANDLE ...f -> ...ves

        if word in si_sb_ves_ve_case or words.last.lower() in si_sb_ves_ve:
            return word[:-1]

        if words.lowered[-3:] == "ves":
            if words.lowered[-5:-3] in ("el", "al", "ol"):
                return word[:-3] + "f"
            if words.lowered[-5:-3] == "ea" and word[-6:-5] != "d":
                return word[:-3] + "f"
            if words.lowered[-5:-3] in ("ni", "li", "wi"):
                return word[:-3] + "fe"
            if words.lowered[-5:-3] == "ar":
                return word[:-3] + "f"

        # HANDLE ...y

        if words.lowered[-2:] == "ys":
            if len(words.lowered) > 2 and words.lowered[-3] in "aeiou":
                return word[:-1]

            if self.classical_dict["names"]:
                if words.lowered[-2:] == "ys" and word[0] == word[0].upper():
                    return word[:-1]

        if words.lowered[-3:] == "ies":
            return word[:-3] + "y"

        # HANDLE ...o

        if words.lowered[-2:] == "os":
            if words.last.lower() in si_sb_U_o_os_complete:
                return word[:-1]

            for k, v in si_sb_U_o_os_bysize.items():
                if words.lowered[-k:] in v:
                    return word[:-1]

            if words.lowered[-3:] in ("aos", "eos", "ios", "oos", "uos"):
                return word[:-1]

        if words.lowered[-3:] == "oes":
            return word[:-2]

        # UNASSIMILATED IMPORTS FINAL RULE

        if word in si_sb_es_is:
            return word[:-2] + "is"

        # OTHERWISE JUST REMOVE ...s

        if words.lowered[-1] == "s":
            return word[:-1]

        # COULD NOT FIND SINGULAR

        return False

    @typechecked
    def singular_noun(
        self,
        text,
        count: Optional[Union[int, str, Any]] = None,
        gender: Optional[str] = None,
    ) -> Union[str, Literal[False]]:
        """
        Return the singular of text, where text is a plural noun.

        If count supplied, then return the singular if count is one of:
            1, a, an, one, each, every, this, that or if count is None

        otherwise return text unchanged.

        Whitespace at the start and end is preserved.

        >>> p = engine()
        >>> p.singular_noun('horses')
        'horse'
        >>> p.singular_noun('knights')
        'knight'

        Returns False when a singular noun is passed.

        >>> p.singular_noun('horse')
        False
        >>> p.singular_noun('knight')
        False
        >>> p.singular_noun('soldier')
        False

        """
        pre, word, post = self.partition_word(text)
        if not word:
            return text
        sing = self._sinoun(word, count=count, gender=gender)
        if sing is not False:
            plural = self.postprocess(word, sing)
            return f"{pre}{plural}{post}"
        return False
