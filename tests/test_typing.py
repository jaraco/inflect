from typing import get_type_hints

import pytest
from typeguard import TypeCheckError

import inflect


def test_word_annotation_keeps_runtime_validation():
    hints = get_type_hints(inflect.engine.plural_noun)

    assert hints["text"] is inflect.Word
    assert inflect.engine().plural_noun("cat") == "cats"
    with pytest.raises(TypeCheckError):
        inflect.engine().plural_noun("")
