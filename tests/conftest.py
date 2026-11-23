"""Make the ``inflect`` package importable without an install.

Tries, in order: this workdir's ``inflect-src`` checkout and the repo
root layout (the layout the PR targets). Tests use a fresh engine per
test because classical mode, gender and user definitions are engine
state.
"""

import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = (
    os.path.join(_HERE, "..", "inflect-src"),
    os.path.join(_HERE, "..", ".."),
)
for _candidate in _CANDIDATES:
    if os.path.isdir(os.path.join(_candidate, "inflect")):
        sys.path.insert(0, os.path.normpath(_candidate))

import inflect  # noqa: E402


@pytest.fixture()
def engine():
    return inflect.engine()
