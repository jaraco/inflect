"""
inflect: english language inflection
 - correctly generate plurals, ordinals, indefinite articles
 - convert numbers to words

Copyright (C) 2010 Paul Dyson

Based upon the Perl module
`Lingua::EN::Inflect <https://metacpan.org/pod/Lingua::EN::Inflect>`_.

methods:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun no num a an
    compare compare_nouns compare_verbs compare_adjs
    present_participle
    ordinal
    number_to_words
    join
    defnoun defverb defadj defa defan

INFLECTIONS:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun no num a an
    present_participle

PLURALS:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun no num
    compare compare_nouns compare_verbs compare_adjs

COMPARISONS:
    classical
    compare compare_nouns compare_verbs compare_adjs

ARTICLES:
    classical inflect num a an

NUMERICAL:
    ordinal number_to_words

USER_DEFINED:
    defnoun defverb defadj defa defan

Exceptions:
 UnknownClassicalModeError
 BadNumValueError
 BadChunkingOptionError
 NumOutOfRangeError
 BadUserDefinedPatternError
 BadRcFileError
 BadGenderError

"""

from __future__ import annotations

import re
from numbers import Number
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Match,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from typeguard import typechecked

# Re-export all public names from domain modules
from .utils import (
    UnknownClassicalModeError,
    BadNumValueError,
    BadChunkingOptionError,
    NumOutOfRangeError,
    BadUserDefinedPatternError,
    BadRcFileError,
    BadGenderError,
    enclose,
    joinstem,
    bysize,
    make_pl_si_lists,
    Words,
    Word,
    Falsish,
    string_to_constant,
    def_classical,
    all_classical,
    no_classical,
    pl_count_zero,
    pl_count_one,
)

from .plurals import (
    pl_sb_irregular_s,
    pl_sb_irregular,
    pl_sb_irregular_caps,
    pl_sb_irregular_compound,
    si_sb_irregular,
    si_sb_irregular_caps,
    si_sb_irregular_compound,
    pl_sb_z_zes_list,
    pl_sb_z_zes_bysize,
    pl_sb_ze_zes_list,
    pl_sb_ze_zes_bysize,
    pl_sb_C_is_ides_complete,
    pl_sb_C_is_ides_endings,
    pl_sb_C_is_ides,
    pl_sb_C_is_ides_list,
    si_sb_C_is_ides_list,
    si_sb_C_is_ides_bysize,
    pl_sb_C_is_ides_bysize,
    pl_sb_C_a_ata_list,
    si_sb_C_a_ata_list,
    si_sb_C_a_ata_bysize,
    pl_sb_C_a_ata_bysize,
    pl_sb_C_a_ata,
    pl_sb_U_a_ae_list,
    si_sb_U_a_ae_list,
    si_sb_U_a_ae_bysize,
    pl_sb_U_a_ae_bysize,
    pl_sb_U_a_ae,
    pl_sb_C_a_ae_list,
    si_sb_C_a_ae_list,
    si_sb_C_a_ae_bysize,
    pl_sb_C_a_ae_bysize,
    pl_sb_C_a_ae,
    pl_sb_C_en_ina_list,
    si_sb_C_en_ina_list,
    si_sb_C_en_ina_bysize,
    pl_sb_C_en_ina_bysize,
    pl_sb_C_en_ina,
    pl_sb_U_um_a_list,
    si_sb_U_um_a_list,
    si_sb_U_um_a_bysize,
    pl_sb_U_um_a_bysize,
    pl_sb_U_um_a,
    pl_sb_C_um_a_list,
    si_sb_C_um_a_list,
    si_sb_C_um_a_bysize,
    pl_sb_C_um_a_bysize,
    pl_sb_C_um_a,
    pl_sb_U_us_i_list,
    si_sb_U_us_i_list,
    si_sb_U_us_i_bysize,
    pl_sb_U_us_i_bysize,
    pl_sb_U_us_i,
    pl_sb_C_us_i_list,
    si_sb_C_us_i_list,
    si_sb_C_us_i_bysize,
    pl_sb_C_us_i_bysize,
    pl_sb_C_us_i,
    pl_sb_C_us_us,
    pl_sb_C_us_us_bysize,
    pl_sb_U_on_a_list,
    si_sb_U_on_a_list,
    si_sb_U_on_a_bysize,
    pl_sb_U_on_a_bysize,
    pl_sb_U_on_a,
    pl_sb_C_on_a_list,
    si_sb_C_on_a_list,
    si_sb_C_on_a_bysize,
    pl_sb_C_on_a_bysize,
    pl_sb_C_on_a,
    pl_sb_C_o_i,
    pl_sb_C_o_i_bysize,
    si_sb_C_o_i_bysize,
    pl_sb_C_o_i_stems,
    pl_sb_U_o_os_complete,
    si_sb_U_o_os_complete,
    pl_sb_U_o_os_endings,
    pl_sb_U_o_os_bysize,
    si_sb_U_o_os_bysize,
    pl_sb_U_ch_chs_list,
    si_sb_U_ch_chs_list,
    si_sb_U_ch_chs_bysize,
    pl_sb_U_ch_chs_bysize,
    pl_sb_U_ch_chs,
    pl_sb_U_ex_ices_list,
    si_sb_U_ex_ices_list,
    si_sb_U_ex_ices_bysize,
    pl_sb_U_ex_ices_bysize,
    pl_sb_U_ex_ices,
    pl_sb_U_ix_ices_list,
    si_sb_U_ix_ices_list,
    si_sb_U_ix_ices_bysize,
    pl_sb_U_ix_ices_bysize,
    pl_sb_U_ix_ices,
    pl_sb_C_ex_ices_list,
    si_sb_C_ex_ices_list,
    si_sb_C_ex_ices_bysize,
    pl_sb_C_ex_ices_bysize,
    pl_sb_C_ex_ices,
    pl_sb_C_ix_ices_list,
    si_sb_C_ix_ices_list,
    si_sb_C_ix_ices_bysize,
    pl_sb_C_ix_ices_bysize,
    pl_sb_C_ix_ices,
    pl_sb_C_i_list,
    si_sb_C_i_list,
    si_sb_C_i_bysize,
    pl_sb_C_i_bysize,
    pl_sb_C_i,
    pl_sb_C_im_list,
    si_sb_C_im_list,
    si_sb_C_im_bysize,
    pl_sb_C_im_bysize,
    pl_sb_C_im,
    pl_sb_U_man_mans_list,
    pl_sb_U_man_mans_caps_list,
    si_sb_U_man_mans_list,
    si_sb_U_man_mans_bysize,
    pl_sb_U_man_mans_bysize,
    si_sb_U_man_mans_caps_list,
    si_sb_U_man_mans_caps_bysize,
    pl_sb_U_man_mans_caps_bysize,
    pl_sb_U_louse_lice_list,
    si_sb_U_louse_lice_list,
    si_sb_U_louse_lice_bysize,
    pl_sb_U_louse_lice_bysize,
    pl_sb_uninflected_s_complete,
    pl_sb_uninflected_s_endings,
    pl_sb_uninflected_s,
    pl_sb_uninflected_herd,
    pl_sb_uninflected_complete,
    pl_sb_uninflected_caps,
    pl_sb_uninflected_endings,
    pl_sb_uninflected_bysize,
    pl_sb_singular_s_complete,
    pl_sb_singular_s_endings,
    pl_sb_singular_s_bysize,
    si_sb_singular_s_complete,
    si_sb_singular_s_endings,
    si_sb_singular_s_bysize,
    pl_sb_singular_s_es,
    pl_sb_singular_s,
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
    pl_sb_postfix_adj,
    pl_sb_postfix_adj_stems,
    si_sb_es_is,
    pl_prep_list,
    pl_prep_list_da,
    pl_prep_bysize,
    pl_prep,
    pl_sb_prep_dual_compound,
    singular_pronoun_genders,
    pl_pron_nom,
    si_pron,
    pl_pron_acc,
    pl_pron_acc_keys,
    pl_pron_acc_keys_bysize,
    si_pron_acc_keys,
    si_pron_acc_keys_bysize,
    get_si_pron,
    PL_SB_POSTFIX_ADJ_STEMS_RE,
    PL_SB_PREP_DUAL_COMPOUND_RE,
    DENOMINATOR,
    _plnoun as _plnoun_impl,
    _sinoun as _sinoun_impl,
    _handle_prepositional_phrase as _handle_prepositional_phrase_impl,
    _handle_long_compounds as _handle_long_compounds_impl,
    _find_pivot as _find_pivot_impl,
)

from .verbs import (
    plverb_irregular_pres,
    plverb_ambiguous_pres,
    plverb_irregular_non_pres,
    plverb_ambiguous_non_pres,
    plverb_ambiguous_pres_keys,
    pl_v_oes_oe,
    pl_v_oes_oe_endings_size4,
    pl_v_oes_oe_endings_size5,
    plverb_special_s,
    PLVERB_SPECIAL_S_RE,
    WHITESPACE,
    ENDS_WITH_S,
    _pl_special_verb as _pl_special_verb_impl,
    _pl_general_verb as _pl_general_verb_impl,
)

from .adjectives import (
    pl_adj_special,
    pl_adj_special_keys,
    pl_adj_poss,
    pl_adj_poss_keys,
    ENDS_WITH_APOSTROPHE_S,
    _pl_special_adjective as _pl_special_adjective_impl,
)

from .articles import (
    A_abbrev,
    A_y_cons,
    A_explicit_a,
    A_explicit_an,
    A_ordinal_an,
    A_ordinal_a,
    INDEFINITE_ARTICLE_TEST,
    SPECIAL_AN,
    SPECIAL_A,
    SPECIAL_ABBREV_AN,
    SPECIAL_ABBREV_A,
    CONSONANTS,
    ARTICLE_SPECIAL_EU,
    ARTICLE_SPECIAL_ONCE,
    ARTICLE_SPECIAL_ONETIME,
    ARTICLE_SPECIAL_UNIT,
    ARTICLE_SPECIAL_UBA,
    ARTICLE_SPECIAL_UKR,
    SPECIAL_CAPITALS,
    VOWELS,
    _indef_article as _indef_article_impl,
    _indef_article_cases,
)

from .numbers import (
    nth,
    nth_suff,
    ordinal,
    ordinal_suff,
    unit,
    teen,
    ten,
    mill,
    DIGIT,
    DIGIT_GROUP,
    TWO_DIGITS,
    THREE_DIGITS,
    THREE_DIGITS_WORD,
    TWO_DIGITS_WORD,
    ONE_DIGIT_WORD,
    FOUR_DIGIT_COMMA,
    NON_DIGIT,
    WHITESPACES_COMMA,
    COMMA_WORD,
    WHITESPACES as NUMBERS_WHITESPACES,
    ordinal_fn as _ordinal_impl,
    millfn as _millfn_impl,
    unitfn as _unitfn_impl,
    tenfn as _tenfn_impl,
    hundfn as _hundfn_impl,
    group1sub as _group1sub_impl,
    group1bsub as _group1bsub_impl,
    group2sub as _group2sub_impl,
    group3sub as _group3sub_impl,
    hundsub as _hundsub_impl,
    tensub as _tensub_impl,
    unitsub as _unitsub_impl,
    enword as _enword_impl,
    _sub_ord,
    _chunk_num as _chunk_num_impl,
    _remove_last_blank,
    _get_sign,
    number_to_words as _number_to_words_impl,
    _render,
)

from .comparisons import (
    _pl_reg_plurals,
    _pl_check_plurals_N as _pl_check_plurals_N_impl,
    _pl_check_plurals_adj as _pl_check_plurals_adj_impl,
    _plequal as _plequal_impl,
)

from .template import (
    DOLLAR_DIGITS,
    FUNCTION_CALL,
    PARTITION_WORD,
    PRESENT_PARTICIPLE_REPLACEMENTS,
    _get_value_from_ast as _get_value_from_ast_impl,
    _string_to_substitute as _string_to_substitute_impl,
    inflect as _inflect_impl,
    postprocess as _postprocess_impl,
    partition_word as _partition_word_impl,
    plural as _plural_impl,
    plural_noun_fn as _plural_noun_impl,
    plural_verb_fn as _plural_verb_impl,
    plural_adj_fn as _plural_adj_impl,
    singular_noun_fn as _singular_noun_impl,
    a_fn as _a_impl,
    no_fn as _no_impl,
    present_participle_fn as _present_participle_impl,
    get_count as _get_count_impl,
    classical_fn as _classical_impl,
    num_fn as _num_impl,
    gender_fn as _gender_impl,
    defnoun_fn as _defnoun_impl,
    defverb_fn as _defverb_impl,
    defadj_fn as _defadj_impl,
    defa_fn as _defa_impl,
    defan_fn as _defan_impl,
    checkpat_fn,
    checkpatplural_fn,
    ud_match_fn as _ud_match_impl,
    join_fn as _join_impl,
)


class engine:
    # Preserve class-level attributes for backward compatibility
    _indef_article_cases = _indef_article_cases

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

    @typechecked
    def defnoun(self, singular: Optional[Word], plural: Optional[Word]) -> int:
        return _defnoun_impl(self, singular, plural)

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
        return _defverb_impl(self, s1, p1, s2, p2, s3, p3)

    @typechecked
    def defadj(self, singular: Optional[Word], plural: Optional[Word]) -> int:
        return _defadj_impl(self, singular, plural)

    @typechecked
    def defa(self, pattern: Optional[Word]) -> int:
        return _defa_impl(self, pattern)

    @typechecked
    def defan(self, pattern: Optional[Word]) -> int:
        return _defan_impl(self, pattern)

    def checkpat(self, pattern: Optional[Word]) -> None:
        return checkpat_fn(pattern)

    def checkpatplural(self, pattern: Optional[Word]) -> None:
        return checkpatplural_fn(pattern)

    @typechecked
    def ud_match(self, word: Word, wordlist: Sequence[Optional[Word]]) -> Optional[str]:
        return _ud_match_impl(self, word, wordlist)

    def classical(self, **kwargs) -> None:
        return _classical_impl(self, **kwargs)

    def num(self, count: Optional[int] = None, show: Optional[int] = None) -> str:
        return _num_impl(self, count, show)

    def gender(self, gender: str) -> None:
        return _gender_impl(self, gender)

    def _get_value_from_ast(self, obj):
        return _get_value_from_ast_impl(self, obj)

    def _string_to_substitute(self, mo: Match, methods_dict: Dict[str, Callable]) -> str:
        return _string_to_substitute_impl(self, mo, methods_dict)

    @typechecked
    def inflect(self, text: Word) -> str:
        return _inflect_impl(self, text)

    def postprocess(self, orig: str, inflected) -> str:
        return _postprocess_impl(self, orig, inflected)

    def partition_word(self, text: str) -> Tuple[str, str, str]:
        return _partition_word_impl(self, text)

    @typechecked
    def plural(self, text: Word, count: Optional[Union[str, int, Any]] = None) -> str:
        return _plural_impl(self, text, count)

    @typechecked
    def plural_noun(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        return _plural_noun_impl(self, text, count)

    @typechecked
    def plural_verb(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        return _plural_verb_impl(self, text, count)

    @typechecked
    def plural_adj(
        self, text: Word, count: Optional[Union[str, int, Any]] = None
    ) -> str:
        return _plural_adj_impl(self, text, count)

    @typechecked
    def compare(self, word1: Word, word2: Word) -> Union[str, bool]:
        norms = self.plural_noun, self.plural_verb, self.plural_adj
        results = (_plequal_impl(self, word1, word2, norm) for norm in norms)
        return next(filter(None, results), False)

    @typechecked
    def compare_nouns(self, word1: Word, word2: Word) -> Union[str, bool]:
        return _plequal_impl(self, word1, word2, self.plural_noun)

    @typechecked
    def compare_verbs(self, word1: Word, word2: Word) -> Union[str, bool]:
        return _plequal_impl(self, word1, word2, self.plural_verb)

    @typechecked
    def compare_adjs(self, word1: Word, word2: Word) -> Union[str, bool]:
        return _plequal_impl(self, word1, word2, self.plural_adj)

    @typechecked
    def singular_noun(
        self,
        text: Word,
        count: Optional[Union[int, str, Any]] = None,
        gender: Optional[str] = None,
    ) -> Union[str, Literal[False]]:
        return _singular_noun_impl(self, text, count, gender)

    def _plequal(self, word1: str, word2: str, pl) -> Union[str, bool]:
        return _plequal_impl(self, word1, word2, pl)

    def _pl_reg_plurals(self, pair: str, stems: str, end1: str, end2: str) -> bool:
        return _pl_reg_plurals(pair, stems, end1, end2)

    def _pl_check_plurals_N(self, word1: str, word2: str) -> bool:
        return _pl_check_plurals_N_impl(word1, word2)

    def _pl_check_plurals_adj(self, word1: str, word2: str) -> bool:
        return _pl_check_plurals_adj_impl(word1, word2)

    def get_count(self, count: Optional[Union[str, int]] = None) -> Union[str, int]:
        return _get_count_impl(self, count)

    def _plnoun(self, word: str, count: Optional[Union[str, int]] = None) -> str:
        return _plnoun_impl(self, word, count)

    @classmethod
    def _handle_prepositional_phrase(cls, phrase, transform, sep):
        return _handle_prepositional_phrase_impl(phrase, transform, sep)

    def _handle_long_compounds(self, word: Words, count: int) -> Union[str, None]:
        return _handle_long_compounds_impl(self, word, count)

    @staticmethod
    def _find_pivot(words, candidates):
        return _find_pivot_impl(words, candidates)

    def _pl_special_verb(
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> Union[str, bool]:
        return _pl_special_verb_impl(self, word, count)

    def _pl_general_verb(
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> str:
        return _pl_general_verb_impl(self, word, count)

    def _pl_special_adjective(
        self, word: str, count: Optional[Union[str, int]] = None
    ) -> Union[str, bool]:
        return _pl_special_adjective_impl(self, word, count)

    def _sinoun(
        self,
        word: str,
        count: Optional[Union[str, int]] = None,
        gender: Optional[str] = None,
    ) -> Union[str, bool]:
        return _sinoun_impl(self, word, count, gender)

    @typechecked
    def a(self, text: Word, count: Optional[Union[int, str, Any]] = 1) -> str:
        return _a_impl(self, text, count)

    an = a

    def _indef_article(self, word: str, count: Union[int, str, Any]) -> str:
        return _indef_article_impl(self, word, count)

    @typechecked
    def no(self, text: Word, count: Optional[Union[int, str]] = None) -> str:
        return _no_impl(self, text, count)

    @typechecked
    def present_participle(self, word: Word) -> str:
        return _present_participle_impl(self, word)

    @typechecked
    def ordinal(self, num: Union[Number, Word]) -> str:
        return _ordinal_impl(self, num)

    def millfn(self, ind: int = 0) -> str:
        return _millfn_impl(self, ind)

    def unitfn(self, units: int, mindex: int = 0) -> str:
        return _unitfn_impl(self, units, mindex)

    def tenfn(self, tens, units, mindex=0) -> str:
        return _tenfn_impl(self, tens, units, mindex)

    def hundfn(self, hundreds: int, tens: int, units: int, mindex: int) -> str:
        return _hundfn_impl(self, hundreds, tens, units, mindex)

    def group1sub(self, mo: Match) -> str:
        return _group1sub_impl(self, mo)

    def group1bsub(self, mo: Match) -> str:
        return _group1bsub_impl(self, mo)

    def group2sub(self, mo: Match) -> str:
        return _group2sub_impl(self, mo)

    def group3sub(self, mo: Match) -> str:
        return _group3sub_impl(self, mo)

    def hundsub(self, mo: Match) -> str:
        return _hundsub_impl(self, mo)

    def tensub(self, mo: Match) -> str:
        return _tensub_impl(self, mo)

    def unitsub(self, mo: Match) -> str:
        return _unitsub_impl(self, mo)

    def enword(self, num: str, group: int) -> str:
        return _enword_impl(self, num, group)

    @staticmethod
    def _sub_ord(val):
        return _sub_ord(val)

    @classmethod
    def _chunk_num(cls, num, decimal, group):
        return _chunk_num_impl(cls, num, decimal, group)

    @staticmethod
    def _remove_last_blank(chunks):
        return _remove_last_blank(chunks)

    @staticmethod
    def _get_sign(num):
        return _get_sign(num)

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
        return _number_to_words_impl(
            self, num, wantlist, group, comma, andword, zero, one, decimal, threshold
        )

    @staticmethod
    def _render(chunks, decimal, comma):
        return _render(chunks, decimal, comma)

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
        return _join_impl(self, words, sep, sep_spaced, final_sep, conj, conj_spaced)
