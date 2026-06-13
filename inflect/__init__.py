"""
inflect: english language inflection
 - correctly generate plurals, ordinals, indefinite articles
 - convert numbers to words

Copyright (C) 2010 Paul Dyson

Based upon the Perl module
`Lingua::EN::Inflect <https://metacpan.org/pod/Lingua::EN::Inflect>`_.

methods:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun no num a an
    compare compare_nouns compare_verbs compare_adjs
    present_participle
    ordinal
    number_to_words
    join
    defnoun defverb defadj defa defan

INFLECTIONS:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun compare
    no num a an present_participle

PLURALS:
    classical inflect
    plural plural_noun plural_verb plural_adj singular_noun no num
    compare compare_nouns compare_verbs compare_adjs

COMPARISONS:
    classical
    compare compare_nouns compare_verbs compare_adjs

ARTICLES:
    classical inflect num a an

NUMERICAL:
    ordinal number_to_words

USER_DEFINED:
    defnoun defverb defadj defa defan

Exceptions:
 UnknownClassicalModeError
 BadNumValueError
 BadChunkingOptionError
 NumOutOfRangeError
 BadUserDefinedPatternError
 BadRcFileError
 BadGenderError

"""

# Re-export the engine class as the main public API
from .engine import engine  # noqa: F401

# Re-export exception classes
from ._shared import (  # noqa: F401
    UnknownClassicalModeError,
    BadNumValueError,
    BadChunkingOptionError,
    NumOutOfRangeError,
    BadUserDefinedPatternError,
    BadRcFileError,
    BadGenderError,
)

# Re-export module-level helper functions, classes, and data
from ._shared import (  # noqa: F401
    enclose,
    joinstem,
    bysize,
    make_pl_si_lists,
    Words,
    Word,
    all_classical,
    def_classical,
    no_classical,
)

# Re-export data that was previously module-level
from .data.numbers import nth_suff  # noqa: F401
