import pytest
import inflect


@pytest.mark.parametrize("word", ['grass', 'glass', 'underpass', 'boss', 'loss', 'moss', 'cross', 'dress', 'stress'])
def test_singular_noun_ss_words(word):
    """Words ending in -ss are already singular and should not be singularized further."""
    p = inflect.engine()
    assert p.singular_noun(word) is False


@pytest.mark.parametrize("plural,singular", [
    ('grasses', 'grass'),
    ('glasses', 'glass'),
    ('bosses', 'boss'),
    ('losses', 'loss'),
    ('mosses', 'moss'),
    ('crosses', 'cross'),
    ('dresses', 'dress'),
])
def test_singular_noun_sses_plurals(plural, singular):
    """Plurals ending in -sses should still singularize correctly."""
    p = inflect.engine()
    assert p.singular_noun(plural) == singular
