"""
The engine class: the main public API for the inflect library.

Composes all method mixins and provides core state management
(classical_dict, persistent_count, gender, etc.).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Union, cast

from typeguard import typechecked

from ._shared import (
    BadGenderError,
    BadNumValueError,
    UnknownClassicalModeError,
    Word,
    all_classical,
    def_classical,
    no_classical,
)
from .data.pronouns import singular_pronoun_genders
from .data.plurals import pl_count_zero, pl_count_one
from ._shared import PARTITION_WORD

from .methods.pluralize import PluralizeMixin
from .methods.singularize import SingularizeMixin
from .methods.articles import ArticleMixin
from .methods.compare import CompareMixin
from .methods.ordinals import OrdinalMixin
from .methods.number_words import NumberWordsMixin
from .methods.participles import ParticipleMixin
from .methods.inflection import InflectionMixin
from .methods.user_defined import UserDefinedMixin


class engine(
    UserDefinedMixin,
    InflectionMixin,
    PluralizeMixin,
    SingularizeMixin,
    ArticleMixin,
    CompareMixin,
    OrdinalMixin,
    NumberWordsMixin,
    ParticipleMixin,
):
    def __init__(self) -> None:
        self.classical_dict = def_classical.copy()
        self.persistent_count: Optional[int] = None
        self.mill_count = 0
        self.pl_sb_user_defined: List[Optional[Word]] = []
        self.pl_v_user_defined: List[Optional[Word]] = []
        self.pl_adj_user_defined: List[Optional[Word]] = []
        self.si_sb_user_defined: List[Optional[Word]] = []
        self.A_a_user_defined: List[Optional[Word]] = []
        self.thegender = "neuter"
        self.__number_args: Optional[Dict[str, str]] = None

    @property
    def _number_args(self):
        return cast(Dict[str, str], self.__number_args)

    @_number_args.setter
    def _number_args(self, val):
        self.__number_args = val

    def classical(self, **kwargs) -> None:
        """
        turn classical mode on and off for various categories

        turn on all classical modes:
        classical()
        classical(all=True)

        turn on or off specific claassical modes:
        e.g.
        classical(herd=True)
        classical(names=False)

        By default all classical modes are off except names.

        unknown value in args or key in kwargs raises
        exception: UnknownClasicalModeError

        """
        if not kwargs:
            self.classical_dict = all_classical.copy()
            return
        if "all" in kwargs:
            if kwargs["all"]:
                self.classical_dict = all_classical.copy()
            else:
                self.classical_dict = no_classical.copy()

        for k, v in kwargs.items():
            if k in def_classical:
                self.classical_dict[k] = v
            else:
                raise UnknownClassicalModeError

    def num(
        self, count: Optional[int] = None, show: Optional[int] = None
    ) -> str:  # (;$count,$show)
        """
        Set the number to be used in other method calls.

        Returns count.

        Set show to False to return '' instead.

        """
        if count is not None:
            try:
                self.persistent_count = int(count)
            except ValueError as err:
                raise BadNumValueError from err
            if (show is None) or show:
                return str(count)
        else:
            self.persistent_count = None
        return ""

    def gender(self, gender: str) -> None:
        """
        set the gender for the singular of plural pronouns

        can be one of:
        'neuter'                ('they' -> 'it')
        'feminine'              ('they' -> 'she')
        'masculine'             ('they' -> 'he')
        'gender-neutral'        ('they' -> 'they')
        'feminine or masculine' ('they' -> 'she or he')
        'masculine or feminine' ('they' -> 'he or she')
        """
        if gender in singular_pronoun_genders:
            self.thegender = gender
        else:
            raise BadGenderError

    # 2. TRANSLATE ZERO-QUANTIFIED $word TO "no plural($word)"

    @typechecked
    def no(self, text: Word, count: Optional[Union[int, str]] = None) -> str:
        """
        If count is 0, no, zero or nil, return 'no' followed by the plural
        of text.

        If count is one of:
            1, a, an, one, each, every, this, that
            return count followed by text.

        Otherwise return count follow by the plural of text.

        In the return value count is always followed by a space.

        Whitespace at the start and end is preserved.

        """
        if count is None and self.persistent_count is not None:
            count = self.persistent_count

        if count is None:
            count = 0
        mo = PARTITION_WORD.search(text)
        if mo:
            pre = mo.group(1)
            word = mo.group(2)
            post = mo.group(3)
        else:
            pre = ""
            word = ""
            post = ""

        if str(count).lower() in pl_count_zero:
            count = 'no'
        return f"{pre}{count} {self.plural(word, count)}{post}"

    @typechecked
    def join(
        self,
        words: Optional[Sequence[Word]],
        sep: Optional[str] = None,
        sep_spaced: bool = True,
        final_sep: Optional[str] = None,
        conj: str = "and",
        conj_spaced: bool = True,
    ) -> str:
        """
        Join words into a list.

        e.g. join(['ant', 'bee', 'fly']) returns 'ant, bee, and fly'

        options:
        conj: replacement for 'and'
        sep: separator. default ',', unless ',' is in the list then ';'
        final_sep: final separator. default ',', unless ',' is in the list then ';'
        conj_spaced: boolean. Should conj have spaces around it

        """
        if not words:
            return ""
        if len(words) == 1:
            return words[0]

        if conj_spaced:
            if conj == "":
                conj = " "
            else:
                conj = f" {conj} "

        if len(words) == 2:
            return f"{words[0]}{conj}{words[1]}"

        if sep is None:
            if "," in "".join(words):
                sep = ";"
            else:
                sep = ","
        if final_sep is None:
            final_sep = sep

        final_sep = f"{final_sep}{conj}"

        if sep_spaced:
            sep += " "

        return f"{sep.join(words[0:-1])}{final_sep}{words[-1]}"
