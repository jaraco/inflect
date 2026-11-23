import pytest

import inflect


@pytest.mark.parametrize("method", ["compare", "compare_adjs"])
@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("dresses's", "dresses'"),
        ("dogs's", "dogs'"),
        ("boys's", "boys'"),
        ("classes's", "classes'"),
    ],
)
def test_alternative_plural_possessives(method, left, right):
    engine = inflect.engine()
    assert getattr(engine, method)(left, right) == "p:p"
    assert getattr(engine, method)(right, left) == "p:p"


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("dress's", "dress'", False),
        ("Jess's", "Jess'", False),
        ("cats'", "dogs'", False),
        ("dogs", "dogs'", False),
        ("dogs'", "dogs'", "eq"),
        ("dog's", "dogs'", "s:p"),
        ("indexes'", "indices'", "p:p"),
    ],
)
def test_possessive_comparison_boundaries(left, right, expected):
    assert inflect.engine().compare_adjs(left, right) == expected
