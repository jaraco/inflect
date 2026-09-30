import pytest
from typeguard import TypeCheckError

from inflect import _runtime_typechecked


def test_runtime_typechecked_validates_arguments_and_returns():
    @_runtime_typechecked
    def identity(value: int) -> int:
        return value

    @_runtime_typechecked
    def invalid_return() -> int:
        return "not an integer"

    assert identity(1) == 1
    with pytest.raises(TypeCheckError):
        identity("not an integer")
    with pytest.raises(TypeCheckError):
        invalid_return()
