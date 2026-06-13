"""Utility functions, exception classes, and shared types for inflect."""

from __future__ import annotations

import collections
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
)

from .compat.py38 import Annotated


class UnknownClassicalModeError(Exception):
    pass


class BadNumValueError(Exception):
    pass


class BadChunkingOptionError(Exception):
    pass


class NumOutOfRangeError(Exception):
    pass


class BadUserDefinedPatternError(Exception):
    pass


class BadRcFileError(Exception):
    pass


class BadGenderError(Exception):
    pass


def enclose(s: str) -> str:
    return f"(?:{s})"


def joinstem(cutpoint: Optional[int] = 0, words: Optional[Iterable[str]] = None) -> str:
    """
    Join stem of each word in words into a string for regex.

    Each word is truncated at cutpoint.

    Cutpoint is usually negative indicating the number of letters to remove
    from the end of each word.

    >>> joinstem(-2, ["ephemeris", "iris", ".*itis"])
    '(?:ephemer|ir|.*it)'

    >>> joinstem(None, ["ephemeris"])
    '(?:ephemeris)'

    >>> joinstem(5, None)
    '(?:)'
    """
    return enclose("|".join(w[:cutpoint] for w in words or []))


def bysize(words: Iterable[str]) -> Dict[int, set]:
    """
    From a list of words, return a dict of sets sorted by word length.

    >>> words = ['ant', 'cat', 'dog', 'pig', 'frog', 'goat', 'horse', 'elephant']
    >>> ret = bysize(words)
    >>> sorted(ret[3])
    ['ant', 'cat', 'dog', 'pig']
    >>> ret[5]
    {'horse'}
    """
    res: Dict[int, set] = collections.defaultdict(set)
    for w in words:
        res[len(w)].add(w)
    return res


def make_pl_si_lists(
    lst: Iterable[str],
    plending: str,
    siendingsize: Optional[int],
    dojoinstem: bool = True,
):
    """
    given a list of singular words: lst

    an ending to append to make the plural: plending

    the number of characters to remove from the singular
    before appending plending: siendingsize

    a flag whether to create a joinstem: dojoinstem

    return:
    a list of pluralised words: si_list (called si because this is what you need to
    look for to make the singular)

    the pluralised words as a dict of sets sorted by word length: si_bysize
    the singular words as a dict of sets sorted by word length: pl_bysize
    if dojoinstem is True: a regular expression that matches any of the stems: stem
    """
    if siendingsize is not None:
        siendingsize = -siendingsize
    si_list = [w[:siendingsize] + plending for w in lst]
    pl_bysize = bysize(lst)
    si_bysize = bysize(si_list)
    if dojoinstem:
        stem = joinstem(siendingsize, lst)
        return si_list, si_bysize, pl_bysize, stem
    else:
        return si_list, si_bysize, pl_bysize


class Words(str):
    lowered: str
    split_: List[str]
    first: str
    last: str

    def __init__(self, orig) -> None:
        self.lowered = self.lower()
        self.split_ = self.split()
        self.first = self.split_[0]
        self.last = self.split_[-1]


Falsish = Any  # ideally, falsish would only validate on bool(value) is False


_STATIC_TYPE_CHECKING = TYPE_CHECKING
# ^-- Workaround for typeguard AST manipulation:
#     https://github.com/agronholm/typeguard/issues/353#issuecomment-1556306554

if _STATIC_TYPE_CHECKING:  # pragma: no cover
    Word = Annotated[str, "String with at least 1 character"]
else:

    class _WordMeta(type):  # Too dynamic to be supported by mypy...
        def __instancecheck__(self, instance: Any) -> bool:
            return isinstance(instance, str) and len(instance) >= 1

    class Word(metaclass=_WordMeta):  # type: ignore[no-redef]
        """String with at least 1 character"""


# Maps strings to built-in constant types
string_to_constant = {"True": True, "False": False, "None": None}


# SUPPORT CLASSICAL PLURALIZATIONS

def_classical = dict(
    all=False, zero=False, herd=False, names=True, persons=False, ancient=False
)

all_classical = {k: True for k in def_classical}
no_classical = {k: False for k in def_classical}


# Count constants used across domains
pl_count_zero = ("0", "no", "zero", "nil")
pl_count_one = ("1", "a", "an", "one", "each", "every", "this", "that")
