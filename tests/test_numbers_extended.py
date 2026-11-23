"""Extended number coverage for inflect.

Probed behaviours pinned here:

* ``number_to_words`` on an unparseable string returns ``"zero"``
  rather than raising.
* ``ordinal`` works on word input too (``"three"`` -> ``"third"``)
  and on 0 / negatives (``"0th"``, ``"-1st"``).
* ``number_to_currency`` always renders ``"<words> and NN/100"``;
  the ``andword`` argument does *not* replace that ``"and"`` in the
  probed build (``number_to_currency(5, andword="dollars")`` still
  gives ``"five and 00/100"``).
"""

import pytest

import inflect


@pytest.mark.parametrize(
    "num, words",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (10, "ten"),
        (11, "eleven"),
        (19, "nineteen"),
        (20, "twenty"),
        (21, "twenty-one"),
        (99, "ninety-nine"),
        (100, "one hundred"),
        (101, "one hundred and one"),
        (1000, "one thousand"),
        (1234, "one thousand, two hundred and thirty-four"),
        (1000000, "one million"),
        (10**12, "one trillion"),
        (-5, "minus five"),
        (3.14, "three point one four"),
        (0.5, "zero point five"),
    ],
)
def test_number_to_words(engine, num, words):
    assert engine.number_to_words(num) == words


def test_number_to_words_string_input(engine):
    assert engine.number_to_words("42") == "forty-two"


def test_number_to_words_unparseable_is_zero(engine):
    assert engine.number_to_words("abc") == "zero"


def test_number_to_words_custom_andword(engine):
    assert engine.number_to_words(101, andword="") == "one hundred one"


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (111, "111th"),
        (0, "0th"),
        (-1, "-1st"),
    ],
)
def test_ordinal(engine, num, expected):
    assert engine.ordinal(num) == expected


def test_ordinal_string_and_word_input(engine):
    assert engine.ordinal("21") == "21st"
    assert engine.ordinal("three") == "third"


@pytest.mark.parametrize(
    "num, expected",
    [
        (1, "one and 00/100"),
        (2, "two and 00/100"),
        (100, "one hundred and 00/100"),
        (1234.56, "one thousand, two hundred and thirty-four and 56/100"),
    ],
)
def test_number_to_currency(engine, num, expected):
    assert engine.number_to_currency(num) == expected


def test_number_to_currency_andword_does_not_replace_and(engine):
    assert engine.number_to_currency(5, andword="dollars") == "five and 00/100"


def test_num_returns_and_resets(engine):
    assert engine.num(5) == "5"
    assert engine.num(5, show=False) == ""
    assert engine.num() == ""


def test_num_bad_value_raises(engine):
    with pytest.raises(inflect.BadNumValueError):
        engine.num("cat")


def test_get_count(engine):
    # With no persistent count set, get_count() is "".
    assert engine.get_count() == ""
    assert engine.get_count(0) == 2
    assert engine.get_count(1) == 1
    assert engine.get_count(2) == 2
    engine.num(2)
    assert engine.get_count() == 2
