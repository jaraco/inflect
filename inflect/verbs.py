"""Domain 2: Plural Verb inflection logic and data tables."""

from __future__ import annotations

import re
from typing import Optional, Union

from .utils import (
    Words,
    enclose,
    pl_count_zero,
)
from .plurals import (
    pl_sb_irregular_s,
    pl_sb_singular_s,
    pl_sb_uninflected_s,
)


# These dictionaries group verbs by first, second and third person
# conjugations.

plverb_irregular_pres = {
    "am": "are",
    "are": "are",
    "is": "are",
    "was": "were",
    "were": "were",
    "have": "have",
    "has": "have",
    "do": "do",
    "does": "do",
}

plverb_ambiguous_pres = {
    "act": "act",
    "acts": "act",
    "blame": "blame",
    "blames": "blame",
    "can": "can",
    "must": "must",
    "fly": "fly",
    "flies": "fly",
    "copy": "copy",
    "copies": "copy",
    "drink": "drink",
    "drinks": "drink",
    "fight": "fight",
    "fights": "fight",
    "fire": "fire",
    "fires": "fire",
    "like": "like",
    "likes": "like",
    "look": "look",
    "looks": "look",
    "make": "make",
    "makes": "make",
    "reach": "reach",
    "reaches": "reach",
    "run": "run",
    "runs": "run",
    "sink": "sink",
    "sinks": "sink",
    "sleep": "sleep",
    "sleeps": "sleep",
    "view": "view",
    "views": "view",
}

plverb_ambiguous_pres_keys = re.compile(
    rf"^({enclose('|'.join(plverb_ambiguous_pres))})((\s.*)?)$", re.IGNORECASE
)


plverb_irregular_non_pres = (
    "did",
    "had",
    "ate",
    "made",
    "put",
    "spent",
    "fought",
    "sank",
    "gave",
    "sought",
    "shall",
    "could",
    "ought",
    "should",
)

plverb_ambiguous_non_pres = re.compile(
    r"^((?:thought|saw|bent|will|might|cut))((\s.*)?)$", re.IGNORECASE
)

# "..oes" -> "..oe" (the rest are "..oes" -> "o")

pl_v_oes_oe = ("canoes", "floes", "oboes", "roes", "throes", "woes")
pl_v_oes_oe_endings_size4 = ("hoes", "toes")
pl_v_oes_oe_endings_size5 = ("shoes",)


# plverb_special_s depends on plurals data
plverb_special_s = enclose(
    "|".join(
        [pl_sb_singular_s]
        + pl_sb_uninflected_s
        + list(pl_sb_irregular_s)
        + ["(.*[csx])is", "(.*)ceps", "[A-Z].*s"]
    )
)


# Pre-compiled regex patterns for verbs domain
PLVERB_SPECIAL_S_RE = re.compile(rf"^({plverb_special_s})$")
WHITESPACE = re.compile(r"\s")
ENDS_WITH_S = re.compile(r"^(.*[^s])s$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def _pl_special_verb(engine, word: str, count=None):  # noqa: C901
    if engine.classical_dict["zero"] and str(count).lower() in pl_count_zero:
        return False
    count = engine.get_count(count)

    if count == 1:
        return word

    # HANDLE USER-DEFINED VERBS

    value = engine.ud_match(word, engine.pl_v_user_defined)
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


def _pl_general_verb(engine, word: str, count=None) -> str:
    count = engine.get_count(count)

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
