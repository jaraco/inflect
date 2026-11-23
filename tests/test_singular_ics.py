import pytest

import inflect

# Mass nouns ending in -ics are already singular and uninflected.
ICS_MASS_NOUNS = [
    "aerobics",
    "biomechanics",
    "calisthenics",
    "economics",
    "genetics",
    "genomics",
    "gymnastics",
    "informatics",
    "kinematics",
    "linguistics",
    "logistics",
    "mathematics",
    "metaphysics",
    "physics",
    "politics",
    "proteomics",
    "semantics",
    "thermodynamics",
]

# True plurals of countable -ic nouns must still singularize.
ICS_PLURALS = [
    ("acoustics", "acoustic"),
    ("aesthetics", "aesthetic"),
    ("comics", "comic"),
    ("critics", "critic"),
    ("dynamics", "dynamic"),
    ("ethics", "ethic"),
    ("graphics", "graphic"),
    ("mechanics", "mechanic"),
    ("optics", "optic"),
    ("statistics", "statistic"),
    ("tactics", "tactic"),
    ("topics", "topic"),
]


@pytest.mark.parametrize("word", ICS_MASS_NOUNS)
def test_singular_noun_ics_mass_nouns(word):
    """Mass nouns ending in -ics are already singular (like 'news')."""
    p = inflect.engine()
    assert p.singular_noun(word) == word


@pytest.mark.parametrize("word", ICS_MASS_NOUNS)
def test_plural_ics_mass_nouns_unchanged(word):
    """Mass nouns ending in -ics do not change in the plural."""
    p = inflect.engine()
    assert p.plural(word) == word
    assert p.plural_noun(word) == word


@pytest.mark.parametrize("plural,singular", ICS_PLURALS)
def test_singular_noun_ics_true_plurals(plural, singular):
    """Plurals of countable -ic nouns still singularize correctly."""
    p = inflect.engine()
    assert p.singular_noun(plural) == singular
