"""Extended plural / singular coverage for inflect.

All expected forms below were probed against the shipped engine
before being written down. Quirks pinned as current behaviour:

* ``singular_noun("indices")`` is ``"indice"`` and
  ``singular_noun("matrices")`` is ``"matrice"`` -- the -es stripping
  does not restore the Latin -x form; ``singular_noun("octopi")``
  is ``False`` (no singular found).
* ``singular_noun`` on an already-singular word returns ``False``
  -- unless a plural persistent count is set (via ``num(2)``), in
  which case it returns the word unchanged.
* ``plural`` preserves the input's capitalisation (``"Cat"`` ->
  ``"Cats"``, ``"CAT"`` -> ``"CATS"``).
* ``plural("cat and dog")`` pluralises only the last word
  (``"cat and dogs"``).
"""

import pytest

import inflect


@pytest.mark.parametrize(
    "singular,plural",
    [
        ("cat", "cats"),
        ("dog", "dogs"),
        ("box", "boxes"),
        ("church", "churches"),
        ("city", "cities"),
        ("baby", "babies"),
        ("knife", "knives"),
        ("leaf", "leaves"),
        ("sheep", "sheep"),
        ("fish", "fish"),
        ("man", "men"),
        ("woman", "women"),
        ("child", "children"),
        ("person", "people"),
        ("octopus", "octopuses"),
        ("cactus", "cactuses"),
        ("analysis", "analyses"),
        ("thesis", "theses"),
        ("phenomenon", "phenomena"),
        ("datum", "data"),
        ("index", "indexes"),
        ("matrix", "matrixes"),
        ("mouse", "mice"),
        ("foot", "feet"),
        ("tooth", "teeth"),
        ("goose", "geese"),
    ],
)
def test_plural_forms(engine, singular, plural):
    assert engine.plural(singular) == plural


@pytest.mark.parametrize(
    "plural, singular",
    [
        ("cats", "cat"),
        ("boxes", "box"),
        ("cities", "city"),
        ("children", "child"),
        ("men", "man"),
        ("women", "woman"),
        ("people", "person"),
        ("sheep", "sheep"),
        ("analyses", "analysis"),
        ("data", "datum"),
        ("mice", "mouse"),
        ("feet", "foot"),
        ("teeth", "tooth"),
        ("geese", "goose"),
    ],
)
def test_singular_forms(engine, plural, singular):
    assert engine.singular_noun(plural) == singular


def test_singular_latin_x_forms_are_truncated(engine):
    assert engine.singular_noun("indices") == "indice"
    assert engine.singular_noun("matrices") == "matrice"


def test_singular_unknown_returns_false(engine):
    assert engine.singular_noun("octopi") is False


def test_singular_of_singular_word_is_false(engine):
    assert engine.singular_noun("cat") is False


def test_singular_of_singular_word_with_plural_count_is_unchanged(engine):
    engine.num(2)
    assert engine.singular_noun("cat") == "cat"


def test_plural_count_argument(engine):
    assert engine.plural("cat", 1) == "cat"
    assert engine.plural("cat", 2) == "cats"
    assert engine.plural("dog", 0) == "dogs"
    assert engine.plural("cat", "2") == "cats"


def test_plural_noun_alias_and_compound(engine):
    assert engine.plural_noun("cat") == "cats"
    assert engine.plural_noun("mother-in-law") == "mothers-in-law"


def test_plural_only_last_word_of_phrase(engine):
    assert engine.plural("cat and dog") == "cat and dogs"


def test_plural_preserves_capitalisation(engine):
    assert engine.plural("Cat") == "Cats"
    assert engine.plural("CAT") == "CATS"
    assert engine.singular_noun("Cats") == "Cat"


@pytest.mark.parametrize(
    "verb, count, expected",
    [
        ("runs", 1, "runs"),
        ("runs", 2, "run"),
        ("is", 2, "are"),
        ("was", 2, "were"),
        ("were", 1, "were"),
        ("has", 2, "have"),
    ],
)
def test_plural_verb(engine, verb, count, expected):
    assert engine.plural_verb(verb, count) == expected


def test_plural_verb_preserves_case(engine):
    assert engine.plural_verb("Runs", 2) == "Run"


def test_plural_adj_is_identity_for_plain_adjectives(engine):
    assert engine.plural_adj("big", 2) == "big"


def test_compare_nouns_and_verbs(engine):
    assert engine.compare_nouns("cat", "cats") == "s:p"
    assert engine.compare_nouns("cat", "cat") == "eq"
    assert engine.compare_verbs("runs", "run") == "s:p"


def test_compare_adjs(engine):
    assert engine.compare_adjs("big", "big") == "eq"
    # A comparative against its base is not a recognised pair.
    assert engine.compare_adjs("bigger", "big") is False


def test_classical_all_changes_latin_plurals(engine):
    engine.classical(all=True)
    assert engine.plural("octopus") == "octopodes"
    assert engine.plural("cactus") == "cacti"


def test_classical_all_off_restores_defaults(engine):
    engine.classical(all=True)
    engine.classical(all=False)
    assert engine.plural("octopus") == "octopuses"


def test_classical_no_args_turns_all_on(engine):
    engine.classical()
    assert engine.plural("octopus") == "octopodes"


def test_classical_unknown_mode_raises(engine):
    with pytest.raises(inflect.UnknownClassicalModeError):
        engine.classical(person=True)


def test_classical_herd_keeps_fish_singular(engine):
    engine.classical(herd=True)
    assert engine.plural("fish") == "fish"


def test_defnoun_and_defadj_and_defverb(engine):
    assert engine.defnoun("wug", "wugs") == 1
    assert engine.plural("wug") == "wugs"
    assert engine.defadj("wuggy", "wuggier") == 1
    assert engine.plural_adj("wuggy", 2) == "wuggier"
    assert engine.defverb("wugs", "wug", "wugged", "wugged", "wugged", "wugged") == 1
    assert engine.plural_verb("wugs", 2) == "wug"


def test_gender_changes_they_singular(engine):
    engine.gender("masculine")
    assert engine.singular_noun("they") == "he"
    engine.gender("feminine")
    assert engine.singular_noun("they") == "she"
    engine.gender("neuter")
    assert engine.singular_noun("they") == "it"


def test_gender_default_is_neuter(engine):
    assert engine.singular_noun("they") == "it"


def test_gender_bad_value_raises(engine):
    with pytest.raises(inflect.BadGenderError):
        engine.gender("wrong")
