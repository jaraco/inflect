"""Domain 4: Indefinite Article logic and data tables."""

from __future__ import annotations

import re
from typing import Union


# THIS PATTERN MATCHES STRINGS OF CAPITALS STARTING WITH A "VOWEL-SOUND"
# CONSONANT FOLLOWED BY ANOTHER CONSONANT, AND WHICH ARE NOT LIKELY
# TO BE REAL WORDS (OH, ALL RIGHT THEN, IT'S JUST MAGIC!)

A_abbrev = re.compile(
    r"""
^(?! FJO | [HLMNS]Y.  | RY[EO] | SQU
  | ( F[LR]? | [HL] | MN? | N | RH? | S[CHKLMNPTVW]? | X(YL)?) [AEIOU])
[FHLMNRSX][A-Z]
""",
    re.VERBOSE,
)

# THIS PATTERN CODES THE BEGINNINGS OF ALL ENGLISH WORDS BEGINING WITH A
# 'y' FOLLOWED BY A CONSONANT. ANY OTHER Y-CONSONANT PREFIX THEREFORE
# IMPLIES AN ABBREVIATION.

A_y_cons = re.compile(r"^(y(b[lor]|cl[ea]|fere|gg|p[ios]|rou|tt))", re.IGNORECASE)

# EXCEPTIONS TO EXCEPTIONS

A_explicit_a = re.compile(r"^((?:unabomber|unanimous|US))", re.IGNORECASE)

A_explicit_an = re.compile(
    r"^((?:euler|hour(?!i)|heir|honest|hono[ur]|mpeg))", re.IGNORECASE
)

A_ordinal_an = re.compile(r"^([aefhilmnorsx]-?th)", re.IGNORECASE)

A_ordinal_a = re.compile(r"^([bcdgjkpqtuvwyz]-?th)", re.IGNORECASE)


# Pre-compiled regex patterns for articles domain

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


# Indefinite article matching cases
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


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def _indef_article(engine, word: str, count) -> str:
    mycount = engine.get_count(count)

    if mycount != 1:
        return f"{count} {word}"

    # HANDLE USER-DEFINED VARIANTS

    value = engine.ud_match(word, engine.A_a_user_defined)
    if value is not None:
        return f"{value} {word}"

    matches = (
        f'{article} {word}'
        for regexen, article in _indef_article_cases
        if regexen.search(word)
    )

    # OTHERWISE, GUESS "a"
    fallback = f'a {word}'
    return next(matches, fallback)
