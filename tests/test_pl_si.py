import pathlib

import pytest

import inflect


FNAME = "tests/words.txt"


def suitable_for_pl_si(word):
    return word and not word.endswith("'s")


@pytest.fixture(params=[False, True], ids=['classical off', 'classical on'])
def classical(request):
    return request.param


def suitable_words():
    words = pathlib.Path(FNAME).read_text(encoding='utf-8').splitlines()
    return filter(suitable_for_pl_si, words)


@pytest.fixture(params=suitable_words())
def word(request):
    return request.param


def test_pl_si(classical, word):
    p = inflect.engine()
    p.classical(all=classical)
    assert p.singular_noun(p.plural_noun(word, 2), 1) == word
