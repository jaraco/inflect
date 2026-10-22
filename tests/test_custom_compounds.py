import pytest

import inflect


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("jeans", "jeans"),
        ("blue jeans", "blue jeans"),
        ("dark blue jeans", "dark blue jeans"),
        ("Blue Jeans", "Blue Jeans"),
        ("BLUE JEANS", "BLUE JEANS"),
        ("  blue jeans  ", "  blue jeans  "),
    ],
)
def test_custom_noun_in_phrase(phrase, expected):
    engine = inflect.engine()
    engine.defnoun("jeans", "jeans")
    assert engine.plural_noun(phrase, 2) == expected
    assert engine.plural_noun(phrase, 1) == phrase


def test_full_phrase_custom_rule_takes_precedence():
    engine = inflect.engine()
    engine.defnoun("jeans", "jeans")
    engine.defnoun("blue jeans", "denim trousers")
    assert engine.plural_noun("blue jeans") == "denim trousers"


def test_custom_noun_regex_in_phrase():
    engine = inflect.engine()
    engine.defnoun("(.+i)o", r"$1i")
    assert engine.plural_noun("large studio") == "large studii"


def test_custom_noun_rule_is_engine_local():
    engine = inflect.engine()
    engine.defnoun("mouse", "mouses")
    assert engine.plural_noun("small mouse") == "small mouses"
    assert inflect.engine().plural_noun("small mouse") == "small mice"


def test_custom_noun_does_not_override_special_compound_head():
    engine = inflect.engine()
    engine.defnoun("law", "customlaws")
    engine.defnoun("general", "customgenerals")
    assert engine.plural_noun("mother-in-law") == "mothers-in-law"
    assert engine.plural_noun("governor general") == "governors general"


def test_unmatched_custom_noun_retains_regular_phrase_rules():
    engine = inflect.engine()
    engine.defnoun("mouse", "mouses")
    assert engine.plural_noun("small dog") == "small dogs"
    assert engine.plural_noun("small child") == "small children"


def test_later_custom_noun_definition_wins_in_phrase():
    engine = inflect.engine()
    engine.defnoun("mouse", "mouses")
    engine.defnoun("mouse", "mice")
    assert engine.plural_noun("small mouse") == "small mice"
