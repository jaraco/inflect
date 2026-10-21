"""Uncountable (mass) nouns should not be pluralized.

Regression test for https://github.com/jaraco/inflect/issues/239 where
``plural_noun("equipment")`` returned ``"equipments"``.
"""

import inflect

# Unambiguous mass nouns added to ``pl_sb_uninflected_endings``. These have no
# ordinary plural form and should be returned unchanged.
MASS_NOUNS = [
    "equipment",
    "luggage",
    "baggage",
    "jewelry",
    "machinery",
    "cutlery",
    "livestock",
    # pre-existing entries, guarded here too
    "furniture",
    "information",
]

# Countable nouns that must keep pluralizing normally, guarding against the
# suffix-matching used for the uncountable list accidentally swallowing them.
COUNTABLE_NOUNS = {
    "document": "documents",
    "moment": "moments",
    "element": "elements",
    "instrument": "instruments",
    "package": "packages",
    "message": "messages",
    "machine": "machines",
    "stock": "stocks",
    "block": "blocks",
    "cutter": "cutters",
    "cat": "cats",
    "box": "boxes",
}


def test_mass_nouns_are_uninflected():
    p = inflect.engine()
    for noun in MASS_NOUNS:
        assert p.plural_noun(noun) == noun


def test_countable_nouns_still_pluralize():
    p = inflect.engine()
    for singular, plural in COUNTABLE_NOUNS.items():
        assert p.plural_noun(singular) == plural
