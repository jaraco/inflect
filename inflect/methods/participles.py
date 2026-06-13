"""
Present participle method.
"""

from __future__ import annotations

import re

from typeguard import typechecked

from .._shared import Word

# Pre-compiled regex
PRESENT_PARTICIPLE_REPLACEMENTS = (
    (re.compile(r"ie$"), r"y"),
    (
        re.compile(r"ue$"),
        r"u",
    ),  # TODO: isn't ue$ -> u encompassed in the following rule?
    (re.compile(r"([auy])e$"), r"\g<1>"),
    (re.compile(r"ski$"), r"ski"),
    (re.compile(r"[^b]i$"), r""),
    (re.compile(r"^(are|were)$"), r"be"),
    (re.compile(r"^(had)$"), r"hav"),
    (re.compile(r"^(hoe)$"), r"\g<1>"),
    (re.compile(r"([^e])e$"), r"\g<1>"),
    (re.compile(r"er$"), r"er"),
    (re.compile(r"([^aeiou][aeiouy]([bdgmnprst]))$"), r"\g<1>\g<2>"),
)


class ParticipleMixin:
    @typechecked
    def present_participle(self, word: Word) -> str:
        """
        Return the present participle for word.

        word is the 3rd person singular verb.

        """
        plv = self.plural_verb(word, 2)
        ans = plv

        for regexen, repl in PRESENT_PARTICIPLE_REPLACEMENTS:
            ans, num = regexen.subn(repl, plv)
            if num:
                return f"{ans}ing"
        return f"{ans}ing"
