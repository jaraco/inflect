"""
Pronoun tables: nominative, accusative, possessive forms and preposition lists.
"""

from __future__ import annotations

from typing import Dict, Union, cast

from .._shared import bysize, enclose


singular_pronoun_genders = {
    "neuter",
    "feminine",
    "masculine",
    "gender-neutral",
    "feminine or masculine",
    "masculine or feminine",
}

pl_pron_nom = {
    # NOMINATIVE    REFLEXIVE
    "i": "we",
    "myself": "ourselves",
    "you": "you",
    "yourself": "yourselves",
    "she": "they",
    "herself": "themselves",
    "he": "they",
    "himself": "themselves",
    "it": "they",
    "itself": "themselves",
    "they": "they",
    "themself": "themselves",
    #   POSSESSIVE
    "mine": "ours",
    "yours": "yours",
    "hers": "theirs",
    "his": "theirs",
    "its": "theirs",
    "theirs": "theirs",
}

si_pron: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
    "nom": {v: k for (k, v) in pl_pron_nom.items()}
}
si_pron["nom"]["we"] = "I"


pl_pron_acc = {
    # ACCUSATIVE    REFLEXIVE
    "me": "us",
    "myself": "ourselves",
    "you": "you",
    "yourself": "yourselves",
    "her": "them",
    "herself": "themselves",
    "him": "them",
    "himself": "themselves",
    "it": "them",
    "itself": "themselves",
    "them": "them",
    "themself": "themselves",
}

pl_pron_acc_keys = enclose("|".join(pl_pron_acc))
pl_pron_acc_keys_bysize = bysize(pl_pron_acc)

si_pron["acc"] = {v: k for (k, v) in pl_pron_acc.items()}

for _thecase, _plur, _gend_sing in (
    (
        "nom",
        "they",
        {
            "neuter": "it",
            "feminine": "she",
            "masculine": "he",
            "gender-neutral": "they",
            "feminine or masculine": "she or he",
            "masculine or feminine": "he or she",
        },
    ),
    (
        "nom",
        "themselves",
        {
            "neuter": "itself",
            "feminine": "herself",
            "masculine": "himself",
            "gender-neutral": "themself",
            "feminine or masculine": "herself or himself",
            "masculine or feminine": "himself or herself",
        },
    ),
    (
        "nom",
        "theirs",
        {
            "neuter": "its",
            "feminine": "hers",
            "masculine": "his",
            "gender-neutral": "theirs",
            "feminine or masculine": "hers or his",
            "masculine or feminine": "his or hers",
        },
    ),
    (
        "acc",
        "them",
        {
            "neuter": "it",
            "feminine": "her",
            "masculine": "him",
            "gender-neutral": "them",
            "feminine or masculine": "her or him",
            "masculine or feminine": "him or her",
        },
    ),
    (
        "acc",
        "themselves",
        {
            "neuter": "itself",
            "feminine": "herself",
            "masculine": "himself",
            "gender-neutral": "themself",
            "feminine or masculine": "herself or himself",
            "masculine or feminine": "himself or herself",
        },
    ),
):
    si_pron[_thecase][_plur] = _gend_sing


si_pron_acc_keys = enclose("|".join(si_pron["acc"]))
si_pron_acc_keys_bysize = bysize(si_pron["acc"])


def get_si_pron(thecase, word, gender) -> str:
    try:
        sing = si_pron[thecase][word]
    except KeyError:
        raise  # not a pronoun
    try:
        return sing[gender]  # has several types due to gender
    except TypeError:
        return cast(str, sing)  # answer independent of gender


# PREPOSITIONS

pl_prep_list = """
    about above across after among around at athwart before behind
    below beneath beside besides between betwixt beyond but by
    during except for from in into near of off on onto out over
    since till to under until unto upon with""".split()

pl_prep_list_da = pl_prep_list + ["de", "du", "da"]

pl_prep_bysize = bysize(pl_prep_list_da)

pl_prep = enclose("|".join(pl_prep_list_da))

pl_sb_prep_dual_compound = rf"(.*?)((?:-|\s+)(?:{pl_prep})(?:-|\s+))a(?:-|\s+)(.*)"
