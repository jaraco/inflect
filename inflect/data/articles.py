"""
Article rules: regex patterns for determining 'a' vs 'an'.
"""

from __future__ import annotations

import re


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
