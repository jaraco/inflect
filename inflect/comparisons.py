"""Domain 6: Comparison logic for inflect."""

from __future__ import annotations

from typing import Union

from .utils import (
    Words,
    Word,
    all_classical,
    no_classical,
)
from .plurals import (
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
    pl_sb_irregular_s,
    pl_sb_irregular,
    pl_sb_irregular_caps,
)


def _pl_reg_plurals(pair: str, stems: str, end1: str, end2: str) -> bool:
    import re
    pattern = rf"({stems})({end1}\|\1{end2}|{end2}\|\1{end1})"
    return bool(re.search(pattern, pair))


def _pl_check_plurals_N(word1: str, word2: str) -> bool:
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
            _pl_reg_plurals(pair, stems, end1, end2)
            for stems, end1, end2 in stem_endings
        )
    )


def _pl_check_plurals_adj(word1: str, word2: str) -> bool:
    word1a = word1[: word1.rfind("'")] if word1.endswith(("'s", "'")) else ""
    word2a = word2[: word2.rfind("'")] if word2.endswith(("'s", "'")) else ""

    return (
        bool(word1a)
        and bool(word2a)
        and (
            _pl_check_plurals_N(word1a, word2a)
            or _pl_check_plurals_N(word2a, word1a)
        )
    )


def _plequal(engine, word1: str, word2: str, pl) -> Union[str, bool]:
    classval = engine.classical_dict.copy()
    for dictionary in (all_classical, no_classical):
        engine.classical_dict = dictionary.copy()
        if word1 == word2:
            return "eq"
        if word1 == pl(word2):
            return "p:s"
        if pl(word1) == word2:
            return "s:p"
    engine.classical_dict = classval.copy()

    if pl == engine.plural or pl == engine.plural_noun:
        if _pl_check_plurals_N(word1, word2):
            return "p:p"
        if _pl_check_plurals_N(word2, word1):
            return "p:p"
    if pl == engine.plural or pl == engine.plural_adj:
        if _pl_check_plurals_adj(word1, word2):
            return "p:p"
    return False
