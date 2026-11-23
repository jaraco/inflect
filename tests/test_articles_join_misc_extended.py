"""Extended articles / join / participle / template coverage.

Probed behaviours pinned here:

* ``a(word, 0)`` returns ``"0 word"`` and ``a(word, 2)`` returns
  ``"2 word"`` -- a non-1 count replaces the article with the count
  itself, it does not produce ``"no word"``.
* ``a`` uses the *sound* of the word: ``"hour"``/``"honest"`` take
  ``"an"``, ``"university"``/``"one"``/``"herb"`` take ``"a"``.
* ``inflect()`` template calls need quoted string arguments:
  ``plural('cat')`` works, bare ``plural(cat)`` raises ``NameError``.
* ``join`` with a comma inside a word switches the separator to
  ``";"`` automatically.
* ``present_participle`` doubles a final consonant after a short
  vowel (``"stop"`` -> ``"stopping"``) and drops a silent ``"e"``.
"""

import pytest

import inflect


@pytest.mark.parametrize(
    "word, expected",
    [
        ("cat", "a cat"),
        ("dog", "a dog"),
        ("apple", "an apple"),
        ("hour", "an hour"),
        ("honest", "an honest"),
        ("university", "a university"),
        ("one", "a one"),
        ("banana", "a banana"),
        ("herb", "a herb"),
    ],
)
def test_indefinite_article(engine, word, expected):
    assert engine.a(word) == expected


def test_indefinite_article_preserves_case(engine):
    assert engine.a("Apple") == "an Apple"


def test_indefinite_article_with_count(engine):
    assert engine.a("cat", 0) == "0 cat"
    assert engine.a("hour", 2) == "2 hour"


def test_a_with_empty_string_raises_type_error(engine):
    # The engine's Word type rejects an empty string at the gate.
    with pytest.raises(Exception):
        engine.a("")


@pytest.mark.parametrize(
    "word, count, expected",
    [
        ("cat", 0, "no cats"),
        ("cat", 1, "1 cat"),
        ("cat", 5, "5 cats"),
        ("dog", 3, "3 dogs"),
    ],
)
def test_no(engine, word, count, expected):
    assert engine.no(word, count) == expected


def test_no_default_count_is_plural_no(engine):
    assert engine.no("cat") == "no cats"


def test_no_with_persistent_num(engine):
    assert engine.no("cat", engine.num(0)) == "no cats"


@pytest.mark.parametrize(
    "word, expected",
    [
        ("run", "running"),
        ("swim", "swimming"),
        ("make", "making"),
        ("dance", "dancing"),
        ("die", "dying"),
        ("lie", "lying"),
        ("stop", "stopping"),
    ],
)
def test_present_participle(engine, word, expected):
    assert engine.present_participle(word) == expected


def test_join_defaults(engine):
    assert engine.join([]) == ""
    assert engine.join(["a"]) == "a"
    assert engine.join(["a", "b"]) == "a and b"
    assert engine.join(["a", "b", "c"]) == "a, b, and c"


def test_join_conjunction_and_separators(engine):
    assert engine.join(["a", "b", "c"], conj="or") == "a, b, or c"
    assert engine.join(["a", "b"], conj="or") == "a or b"
    assert engine.join(["a", "b", "c"], sep=";") == "a; b; and c"
    assert engine.join(["a", "b", "c"], sep=",", sep_spaced=False) == "a,b, and c"


def test_join_comma_in_word_switches_separator(engine):
    assert engine.join(["a, x", "b", "c"]) == "a, x; b; and c"


def test_inflect_template_with_quoted_args(engine):
    assert engine.inflect("The plural of cat is plural('cat')") == "The plural of cat is cats"
    assert engine.inflect("I saw no('cat', 0)") == "I saw no cats"
    assert engine.inflect("I saw a('cat')") == "I saw a cat"
    assert engine.inflect("They plural_verb('runs', 2)") == "They run"
    assert engine.inflect("She is present_participle('run')") == "She is running"
    assert engine.inflect("This is ordinal(21)") == "This is 21st"
    assert engine.inflect("number_to_words(42)") == "forty-two"


def test_inflect_template_bare_name_raises(engine):
    with pytest.raises(NameError):
        engine.inflect("plural(cat)")


def test_partition_word_plain_word(engine):
    assert engine.partition_word("cats") == ("", "cats", "")


def test_module_helpers_enclose_and_bysize(engine):
    assert inflect.enclose("x") == "(?:x)"
    grouped = inflect.bysize(["a", "bb", "ccc", "dd"])
    assert grouped[1] == {"a"}
    assert grouped[2] == {"bb", "dd"}
    assert grouped[3] == {"ccc"}
