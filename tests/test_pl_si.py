import pytest

import inflect


@pytest.fixture(params=[False, True], ids=['classical off', 'classical on'])
def classical(request):
    return request.param


@pytest.mark.parametrize("word", ['Times', 'Jones'])
def test_pl_si(classical, word):
    p = inflect.engine()
    p.classical(all=classical)
    assert p.singular_noun(p.plural_noun(word, 2), 1) == word


@pytest.mark.parametrize(
    ('singular', 'plural'),
    [('thief', 'thieves'), ('Thief', 'Thieves'), ('THIEF', 'THIEVES')],
)
def test_thief_plural(classical, singular, plural):
    p = inflect.engine()
    p.classical(all=classical)
    assert p.plural(singular) == plural
    assert p.plural_noun(singular) == plural
    assert p.plural_noun(singular, 1) == singular
    assert p.singular_noun(plural) == singular


def test_hoof_plural_alternatives(classical):
    p = inflect.engine()
    p.classical(all=classical)
    expected = 'hooves' if classical else 'hoofs'
    assert p.plural('hoof') == expected
    assert p.singular_noun(expected) == 'hoof'
