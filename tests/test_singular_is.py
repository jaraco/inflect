import pytest

import inflect

# Singular nouns ending in -is (mostly Greek, plural -es) are already singular.
IS_SINGULARS = [
    "analysis",
    "axis",
    "basis",
    "catharsis",
    "crisis",
    "diagnosis",
    "emphasis",
    "genesis",
    "hypothesis",
    "metamorphosis",
    "metropolis",
    "nemesis",
    "neurosis",
    "oasis",
    "paralysis",
    "parenthesis",
    "prognosis",
    "psychosis",
    "symbiosis",
    "synthesis",
    "thesis",
]

# Known singular nouns ending in -s from pl_sb_singular_s_complete.
SINGULAR_S_WORDS = [
    "alias",
    "bias",
    "canvas",
    "chaos",
]

# Plural to singular direction must keep working.
IS_PLURAL_PAIRS = [
    ("analyses", "analysis"),
    ("crises", "crisis"),
    ("diagnoses", "diagnosis"),
    ("emphases", "emphasis"),
    ("geneses", "genesis"),
    ("oases", "oasis"),
    ("theses", "thesis"),
]

# Pluralization of the singular -is words must be unchanged.
IS_PLURALIZATION = [
    ("analysis", "analyses"),
    ("axis", "axes"),
    ("basis", "bases"),
    ("crisis", "crises"),
    ("metropolis", "metropolises"),
]


@pytest.mark.parametrize("word", IS_SINGULARS + SINGULAR_S_WORDS)
def test_singular_noun_already_singular(word):
    """Singular nouns ending in -s are not pluralized words (like 'mass')."""
    p = inflect.engine()
    assert p.singular_noun(word) is False


@pytest.mark.parametrize("plural,singular", IS_PLURAL_PAIRS)
def test_singular_noun_is_plurals(plural, singular):
    """Plurals ending in -es still singularize to their -is forms."""
    p = inflect.engine()
    assert p.singular_noun(plural) == singular


@pytest.mark.parametrize("singular,plural", IS_PLURALIZATION)
def test_plural_of_is_singulars_unchanged(singular, plural):
    """The -is singulars keep their existing -es plurals."""
    p = inflect.engine()
    assert p.plural(singular) == plural
