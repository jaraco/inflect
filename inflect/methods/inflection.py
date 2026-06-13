"""
Inflection methods: inflect, postprocess, partition_word.
"""

from __future__ import annotations

import ast
import re
from typing import Callable, Dict, Match

from typeguard import typechecked

from .._shared import PARTITION_WORD, Word

# Pre-compiled regex
FUNCTION_CALL = re.compile(r"((\w+)\([^)]*\)*)", re.IGNORECASE)


class InflectionMixin:
    def _get_value_from_ast(self, obj):
        """
        Return the value of the ast object.
        """
        if isinstance(obj, ast.Constant):
            return obj.value
        elif isinstance(obj, ast.List):
            return [self._get_value_from_ast(e) for e in obj.elts]
        elif isinstance(obj, ast.Tuple):
            return tuple([self._get_value_from_ast(e) for e in obj.elts])

        # Probably passed a variable name.
        # Or passed a single word without wrapping it in quotes as an argument
        # ex: p.inflect("I plural(see)") instead of p.inflect("I plural('see')")
        raise NameError(f"name '{obj.id}' is not defined")

    def _string_to_substitute(
        self, mo: Match, methods_dict: Dict[str, Callable]
    ) -> str:
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
            self._get_value_from_ast(a)
            for a in a_tree.body[0].value.args  # type: ignore[attr-defined]
        ]
        kwargs_list = {
            kw.arg: self._get_value_from_ast(kw.value)
            for kw in a_tree.body[0].value.keywords  # type: ignore[attr-defined]
        }

        # Call the corresponding function
        return methods_dict[f_name](*args_list, **kwargs_list)

    # 0. PERFORM GENERAL INFLECTIONS IN A STRING

    @typechecked
    def inflect(self, text: Word) -> str:
        """
        Perform inflections in a string.

        e.g. inflect('The plural of cat is plural(cat)') returns
        'The plural of cat is cats'

        can use plural, plural_noun, plural_verb, plural_adj,
        singular_noun, a, an, no, ordinal, number_to_words,
        and prespart

        """
        save_persistent_count = self.persistent_count

        # Dictionary of allowed methods
        methods_dict: Dict[str, Callable] = {
            "plural": self.plural,
            "plural_adj": self.plural_adj,
            "plural_noun": self.plural_noun,
            "plural_verb": self.plural_verb,
            "singular_noun": self.singular_noun,
            "a": self.a,
            "an": self.a,
            "no": self.no,
            "ordinal": self.ordinal,
            "number_to_words": self.number_to_words,
            "present_participle": self.present_participle,
            "num": self.num,
        }

        # Regular expression to find Python's function call syntax
        output = FUNCTION_CALL.sub(
            lambda mo: self._string_to_substitute(mo, methods_dict), text
        )
        self.persistent_count = save_persistent_count
        return output

    # ## PLURAL SUBROUTINES

    def postprocess(self, orig: str, inflected) -> str:
        inflected = str(inflected)
        if "|" in inflected:
            word_options = inflected.split("|")
            # When two parts of a noun need to be pluralized
            if len(word_options[0].split(" ")) == len(word_options[1].split(" ")):
                result = inflected.split("|")[self.classical_dict["all"]].split(" ")
            # When only the last part of the noun needs to be pluralized
            else:
                result = inflected.split(" ")
                for index, word in enumerate(result):
                    if "|" in word:
                        result[index] = word.split("|")[self.classical_dict["all"]]
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

    def partition_word(self, text: str):
        mo = PARTITION_WORD.search(text)
        if mo:
            return mo.group(1), mo.group(2), mo.group(3)
        else:
            return "", "", ""
