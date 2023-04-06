import pathlib

import pytest

import inflect


FNAME = "tests/words.txt"


def suitable_for_pl_si(word):
    return word and not word.endswith("'s")


@pytest.fixture(params=[False, True], ids=['classical off', 'classical on'])
def classical(request):
    return request.param


def test_pl_si(classical):
    p = inflect.engine()
    p.classical(all=classical)
    words = pathlib.Path(FNAME).read_text(encoding='utf-8').splitlines()
    for word in filter(suitable_for_pl_si, words):
        check_pl_si(p, word)


def check_pl_si(p, word):
    if p.singular_noun(p.plural_noun(word, 2), 1) != word:
        f = open("badsi.txt", "a", encoding='utf-8')
        f.write(
            "{} {} {}\n".format(
                word, p.plural_noun(word, 2), p.singular_noun(p.plural_noun(word, 2), 1)
            )
        )
        f.close()
        assert p.singular_noun(p.plural_noun(word, 2), 1) == word
