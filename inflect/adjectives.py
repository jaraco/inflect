"""Domain 3: Plural Adjective inflection logic and data tables."""

from __future__ import annotations

import re
from typing import Optional, Union

from .utils import (
    enclose,
)


pl_adj_special = {"a": "some", "an": "some", "this": "these", "that": "those"}

pl_adj_special_keys = re.compile(
    rf"^({enclose('|'.join(pl_adj_special))})$", re.IGNORECASE
)

pl_adj_poss = {
    "my": "our",
    "your": "your",
    "its": "their",
    "her": "their",
    "his": "their",
    "their": "their",
}

pl_adj_poss_keys = re.compile(rf"^({enclose('|'.join(pl_adj_poss))})$", re.IGNORECASE)


# Pre-compiled regex patterns for adjectives domain
ENDS_WITH_APOSTROPHE_S = re.compile(r"^(.+)'s?$")


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def _pl_special_adjective(engine, word: str, count=None):
    count = engine.get_count(count)

    if count == 1:
        return word

    # HANDLE USER-DEFINED ADJECTIVES

    value = engine.ud_match(word, engine.pl_adj_user_defined)
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
        pl = engine.plural_noun(mo.group(1))
        trailing_s = "" if pl[-1] == "s" else "s"
        return f"{pl}'{trailing_s}"

    # OTHERWISE, NO IDEA

    return False
