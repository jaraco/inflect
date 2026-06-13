"""Domain 7: Template Engine / Infrastructure for inflect."""

from __future__ import annotations

import ast
import re
from typing import (
    Any,
    Callable,
    Dict,
    Match,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from typeguard import typechecked

from .utils import (
    BadGenderError,
    BadNumValueError,
    BadUserDefinedPatternError,
    UnknownClassicalModeError,
    Word,
    all_classical,
    def_classical,
    no_classical,
    pl_count_one,
    pl_count_zero,
    string_to_constant,
)
from .plurals import singular_pronoun_genders


# Pre-compiled regex patterns for template domain

DOLLAR_DIGITS = re.compile(r"\$(\d+)")
FUNCTION_CALL = re.compile(r"((\w+)\([^)]*\)*)", re.IGNORECASE)
PARTITION_WORD = re.compile(r"\A(\s*)(.+?)(\s*)\Z")

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


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def _get_value_from_ast(engine, obj):
    """
    Return the value of the ast object.
    """
    if isinstance(obj, ast.Constant):
        return obj.value
    elif isinstance(obj, ast.List):
        return [_get_value_from_ast(engine, e) for e in obj.elts]
    elif isinstance(obj, ast.Tuple):
        return tuple([_get_value_from_ast(engine, e) for e in obj.elts])

    # Probably passed a variable name.
    # Or passed a single word without wrapping it in quotes as an argument
    # ex: p.inflect("I plural(see)") instead of p.inflect("I plural('see')")
    raise NameError(f"name '{obj.id}' is not defined")


def _string_to_substitute(engine, mo: Match, methods_dict: Dict[str, Callable]) -> str:
    """
    Return the string to be substituted for the match.
    """
    matched_text, f_name = mo.groups()
    # matched_text is the complete match string. e.g. plural_noun(cat)
    # f_name is the function name. e.g. plural_noun

    # Return matched_text if function name is not in methods_dict
    if f_name not in methods_dict:
        return matched_text

    # Parse the matched text
    a_tree = ast.parse(matched_text)

    # get the args and kwargs from ast objects
    args_list = [
        _get_value_from_ast(engine, a)
        for a in a_tree.body[0].value.args  # type: ignore[attr-defined]
    ]
    kwargs_list = {
        kw.arg: _get_value_from_ast(engine, kw.value)
        for kw in a_tree.body[0].value.keywords  # type: ignore[attr-defined]
    }

    # Call the corresponding function
    return methods_dict[f_name](*args_list, **kwargs_list)


def inflect(engine, text: Word) -> str:
    """
    Perform inflections in a string.

    e.g. inflect('The plural of cat is plural(cat)') returns
    'The plural of cat is cats'

    can use plural, plural_noun, plural_verb, plural_adj,
    singular_noun, a, an, no, ordinal, number_to_words,
    and prespart

    """
    save_persistent_count = engine.persistent_count

    # Dictionary of allowed methods
    methods_dict: Dict[str, Callable] = {
        "plural": engine.plural,
        "plural_adj": engine.plural_adj,
        "plural_noun": engine.plural_noun,
        "plural_verb": engine.plural_verb,
        "singular_noun": engine.singular_noun,
        "a": engine.a,
        "an": engine.a,
        "no": engine.no,
        "ordinal": engine.ordinal,
        "number_to_words": engine.number_to_words,
        "present_participle": engine.present_participle,
        "num": engine.num,
    }

    # Regular expression to find Python's function call syntax
    output = FUNCTION_CALL.sub(
        lambda mo: _string_to_substitute(engine, mo, methods_dict), text
    )
    engine.persistent_count = save_persistent_count
    return output


def postprocess(engine, orig: str, inflected) -> str:
    inflected = str(inflected)
    if "|" in inflected:
        word_options = inflected.split("|")
        # When two parts of a noun need to be pluralized
        if len(word_options[0].split(" ")) == len(word_options[1].split(" ")):
            result = inflected.split("|")[engine.classical_dict["all"]].split(" ")
        # When only the last part of the noun needs to be pluralized
        else:
            result = inflected.split(" ")
            for index, word in enumerate(result):
                if "|" in word:
                    result[index] = word.split("|")[engine.classical_dict["all"]]
    else:
        result = inflected.split(" ")

    # Try to fix word wise capitalization
    for index, word in enumerate(orig.split(" ")):
        if word == "I":
            # Is this the only word for exceptions like this
            # Where the original is fully capitalized
            # without 'meaning' capitalization?
            # Also this fails to handle a capitalizaion in context
            continue
        if word.capitalize() == word:
            result[index] = result[index].capitalize()
        if word == word.upper():
            result[index] = result[index].upper()
    return " ".join(result)


def partition_word(engine, text: str) -> Tuple[str, str, str]:
    mo = PARTITION_WORD.search(text)
    if mo:
        return mo.group(1), mo.group(2), mo.group(3)
    else:
        return "", "", ""


def plural(engine, text: Word, count=None) -> str:
    """
    Return the plural of text.

    If count supplied, then return text if count is one of:
        1, a, an, one, each, every, this, that

    otherwise return the plural.

    Whitespace at the start and end is preserved.

    """
    pre, word, post = partition_word(engine, text)
    if not word:
        return text
    pl = postprocess(
        engine,
        word,
        engine._pl_special_adjective(word, count)
        or engine._pl_special_verb(word, count)
        or engine._plnoun(word, count),
    )
    return f"{pre}{pl}{post}"


def plural_noun_fn(engine, text: Word, count=None) -> str:
    """
    Return the plural of text, where text is a noun.

    If count supplied, then return text if count is one of:
        1, a, an, one, each, every, this, that

    otherwise return the plural.

    Whitespace at the start and end is preserved.

    """
    pre, word, post = partition_word(engine, text)
    if not word:
        return text
    pl = postprocess(engine, word, engine._plnoun(word, count))
    return f"{pre}{pl}{post}"


def plural_verb_fn(engine, text: Word, count=None) -> str:
    """
    Return the plural of text, where text is a verb.

    If count supplied, then return text if count is one of:
        1, a, an, one, each, every, this, that

    otherwise return the plural.

    Whitespace at the start and end is preserved.

    """
    pre, word, post = partition_word(engine, text)
    if not word:
        return text
    pl = postprocess(
        engine,
        word,
        engine._pl_special_verb(word, count) or engine._pl_general_verb(word, count),
    )
    return f"{pre}{pl}{post}"


def plural_adj_fn(engine, text: Word, count=None) -> str:
    """
    Return the plural of text, where text is an adjective.

    If count supplied, then return text if count is one of:
        1, a, an, one, each, every, this, that

    otherwise return the plural.

    Whitespace at the start and end is preserved.

    """
    pre, word, post = partition_word(engine, text)
    if not word:
        return text
    pl = postprocess(engine, word, engine._pl_special_adjective(word, count) or word)
    return f"{pre}{pl}{post}"


def singular_noun_fn(engine, text: Word, count=None, gender=None):
    """
    Return the singular of text, where text is a plural noun.

    If count supplied, then return the singular if count is one of:
        1, a, an, one, each, every, this, that or if count is None

    otherwise return text unchanged.

    Whitespace at the start and end is preserved.

    >>> p = __import__('inflect').engine()
    >>> p.singular_noun('horses')
    'horse'
    >>> p.singular_noun('knights')
    'knight'

    Returns False when a singular noun is passed.

    >>> p.singular_noun('horse')
    False
    >>> p.singular_noun('knight')
    False
    >>> p.singular_noun('soldier')
    False

    """
    pre, word, post = partition_word(engine, text)
    if not word:
        return text
    sing = engine._sinoun(word, count=count, gender=gender)
    if sing is not False:
        pl = postprocess(engine, word, sing)
        return f"{pre}{pl}{post}"
    return False


def a_fn(engine, text: Word, count=1) -> str:
    """
    Return the appropriate indefinite article followed by text.

    The indefinite article is either 'a' or 'an'.

    If count is not one, then return count followed by text
    instead of 'a' or 'an'.

    Whitespace at the start and end is preserved.

    """
    from .articles import INDEFINITE_ARTICLE_TEST
    mo = INDEFINITE_ARTICLE_TEST.search(text)
    if mo:
        word = mo.group(2)
        if not word:
            return text
        pre = mo.group(1)
        post = mo.group(3)
        result = engine._indef_article(word, count)
        return f"{pre}{result}{post}"
    return ""


def no_fn(engine, text: Word, count=None) -> str:
    """
    If count is 0, no, zero or nil, return 'no' followed by the plural
    of text.

    If count is one of:
        1, a, an, one, each, every, this, that
        return count followed by text.

    Otherwise return count follow by the plural of text.

    In the return value count is always followed by a space.

    Whitespace at the start and end is preserved.

    """
    if count is None and engine.persistent_count is not None:
        count = engine.persistent_count

    if count is None:
        count = 0
    mo = PARTITION_WORD.search(text)
    if mo:
        pre = mo.group(1)
        word = mo.group(2)
        post = mo.group(3)
    else:
        pre = ""
        word = ""
        post = ""

    if str(count).lower() in pl_count_zero:
        count = 'no'
    return f"{pre}{count} {engine.plural(word, count)}{post}"


def present_participle_fn(engine, word: Word) -> str:
    """
    Return the present participle for word.

    word is the 3rd person singular verb.

    """
    plv = engine.plural_verb(word, 2)
    ans = plv

    for regexen, repl in PRESENT_PARTICIPLE_REPLACEMENTS:
        ans, num = regexen.subn(repl, plv)
        if num:
            return f"{ans}ing"
    return f"{ans}ing"


def get_count(engine, count=None):
    if count is None and engine.persistent_count is not None:
        count = engine.persistent_count

    if count is not None:
        count = (
            1
            if (
                (str(count) in pl_count_one)
                or (
                    engine.classical_dict["zero"]
                    and str(count).lower() in pl_count_zero
                )
            )
            else 2
        )
    else:
        count = ""
    return count


def classical_fn(engine, **kwargs) -> None:
    """
    turn classical mode on and off for various categories

    turn on all classical modes:
    classical()
    classical(all=True)

    turn on or off specific claassical modes:
    e.g.
    classical(herd=True)
    classical(names=False)

    By default all classical modes are off except names.

    unknown value in args or key in kwargs raises
    exception: UnknownClasicalModeError

    """
    if not kwargs:
        engine.classical_dict = all_classical.copy()
        return
    if "all" in kwargs:
        if kwargs["all"]:
            engine.classical_dict = all_classical.copy()
        else:
            engine.classical_dict = no_classical.copy()

    for k, v in kwargs.items():
        if k in def_classical:
            engine.classical_dict[k] = v
        else:
            raise UnknownClassicalModeError


def num_fn(engine, count=None, show=None) -> str:
    """
    Set the number to be used in other method calls.

    Returns count.

    Set show to False to return '' instead.

    """
    if count is not None:
        try:
            engine.persistent_count = int(count)
        except ValueError as err:
            raise BadNumValueError from err
        if (show is None) or show:
            return str(count)
    else:
        engine.persistent_count = None
    return ""


def gender_fn(engine, gender: str) -> None:
    """
    set the gender for the singular of plural pronouns

    can be one of:
    'neuter'                ('they' -> 'it')
    'feminine'              ('they' -> 'she')
    'masculine'             ('they' -> 'he')
    'gender-neutral'        ('they' -> 'they')
    'feminine or masculine' ('they' -> 'she or he')
    'masculine or feminine' ('they' -> 'he or she')
    """
    if gender in singular_pronoun_genders:
        engine.thegender = gender
    else:
        raise BadGenderError


def defnoun_fn(engine, singular, plural) -> int:
    """
    Set the noun plural of singular to plural.

    """
    checkpat_fn(singular)
    checkpatplural_fn(plural)
    engine.pl_sb_user_defined.extend((singular, plural))
    engine.si_sb_user_defined.extend((plural, singular))
    return 1


def defverb_fn(engine, s1, p1, s2, p2, s3, p3) -> int:
    """
    Set the verb plurals for s1, s2 and s3 to p1, p2 and p3 respectively.

    Where 1, 2 and 3 represent the 1st, 2nd and 3rd person forms of the verb.

    """
    checkpat_fn(s1)
    checkpat_fn(s2)
    checkpat_fn(s3)
    checkpatplural_fn(p1)
    checkpatplural_fn(p2)
    checkpatplural_fn(p3)
    engine.pl_v_user_defined.extend((s1, p1, s2, p2, s3, p3))
    return 1


def defadj_fn(engine, singular, plural) -> int:
    """
    Set the adjective plural of singular to plural.

    """
    checkpat_fn(singular)
    checkpatplural_fn(plural)
    engine.pl_adj_user_defined.extend((singular, plural))
    return 1


def defa_fn(engine, pattern) -> int:
    """
    Define the indefinite article as 'a' for words matching pattern.

    """
    checkpat_fn(pattern)
    engine.A_a_user_defined.extend((pattern, "a"))
    return 1


def defan_fn(engine, pattern) -> int:
    """
    Define the indefinite article as 'an' for words matching pattern.

    """
    checkpat_fn(pattern)
    engine.A_a_user_defined.extend((pattern, "an"))
    return 1


def checkpat_fn(pattern) -> None:
    """
    check for errors in a regex pattern
    """
    if pattern is None:
        return
    try:
        re.match(pattern, "")
    except re.error as err:
        raise BadUserDefinedPatternError(pattern) from err


def checkpatplural_fn(pattern) -> None:
    """
    check for errors in a regex replace pattern
    """
    return


def ud_match_fn(engine, word, wordlist):
    for i in range(len(wordlist) - 2, -2, -2):  # backwards through even elements
        mo = re.search(rf"^{wordlist[i]}$", word, re.IGNORECASE)
        if mo:
            if wordlist[i + 1] is None:
                return None
            pl = DOLLAR_DIGITS.sub(
                r"\\1", cast(Word, wordlist[i + 1])
            )  # change $n to \n for expand
            return mo.expand(pl)
    return None


def join_fn(
    engine,
    words,
    sep=None,
    sep_spaced: bool = True,
    final_sep=None,
    conj: str = "and",
    conj_spaced: bool = True,
) -> str:
    """
    Join words into a list.

    e.g. join(['ant', 'bee', 'fly']) returns 'ant, bee, and fly'

    options:
    conj: replacement for 'and'
    sep: separator. default ',', unless ',' is in the list then ';'
    final_sep: final separator. default ',', unless ',' is in the list then ';'
    conj_spaced: boolean. Should conj have spaces around it

    """
    if not words:
        return ""
    if len(words) == 1:
        return words[0]

    if conj_spaced:
        if conj == "":
            conj = " "
        else:
            conj = f" {conj} "

    if len(words) == 2:
        return f"{words[0]}{conj}{words[1]}"

    if sep is None:
        if "," in "".join(words):
            sep = ";"
        else:
            sep = ","
    if final_sep is None:
        final_sep = sep

    final_sep = f"{final_sep}{conj}"

    if sep_spaced:
        sep += " "

    return f"{sep.join(words[0:-1])}{final_sep}{words[-1]}"
