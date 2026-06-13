"""Domain 1: Plural/Singular Noun inflection logic and data tables."""

from __future__ import annotations

import contextlib
import functools
import itertools
import re
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    cast,
)

from more_itertools import windowed_complete

from .utils import (
    BadGenderError,
    Words,
    bysize,
    enclose,
    joinstem,
    make_pl_si_lists,
    pl_count_one,
    pl_count_zero,
)


# 1. PLURALS

pl_sb_irregular_s = {
    "corpus": "corpuses|corpora",
    "opus": "opuses|opera",
    "genus": "genera",
    "mythos": "mythoi",
    "penis": "penises|penes",
    "testis": "testes",
    "atlas": "atlases|atlantes",
    "yes": "yeses",
}

pl_sb_irregular = {
    "child": "children",
    "chili": "chilis|chilies",
    "brother": "brothers|brethren",
    "infinity": "infinities|infinity",
    "loaf": "loaves",
    "lore": "lores|lore",
    "hoof": "hoofs|hooves",
    "beef": "beefs|beeves",
    "thief": "thiefs|thieves",
    "money": "monies",
    "mongoose": "mongooses",
    "ox": "oxen",
    "cow": "cows|kine",
    "graffito": "graffiti",
    "octopus": "octopuses|octopodes",
    "genie": "genies|genii",
    "ganglion": "ganglions|ganglia",
    "trilby": "trilbys",
    "turf": "turfs|turves",
    "numen": "numina",
    "atman": "atmas",
    "occiput": "occiputs|occipita",
    "sabretooth": "sabretooths",
    "sabertooth": "sabertooths",
    "lowlife": "lowlifes",
    "flatfoot": "flatfoots",
    "tenderfoot": "tenderfoots",
    "romany": "romanies",
    "jerry": "jerries",
    "mary": "maries",
    "talouse": "talouses",
    "rom": "roma",
    "carmen": "carmina",
}

pl_sb_irregular.update(pl_sb_irregular_s)
# pl_sb_irregular_keys = enclose('|'.join(pl_sb_irregular.keys()))

pl_sb_irregular_caps = {
    "Romany": "Romanies",
    "Jerry": "Jerrys",
    "Mary": "Marys",
    "Rom": "Roma",
}

pl_sb_irregular_compound = {"prima donna": "prima donnas|prime donne"}

si_sb_irregular = {v: k for (k, v) in pl_sb_irregular.items()}
for k in list(si_sb_irregular):
    if "|" in k:
        k1, k2 = k.split("|")
        si_sb_irregular[k1] = si_sb_irregular[k2] = si_sb_irregular[k]
        del si_sb_irregular[k]
si_sb_irregular_caps = {v: k for (k, v) in pl_sb_irregular_caps.items()}
si_sb_irregular_compound = {v: k for (k, v) in pl_sb_irregular_compound.items()}
for k in list(si_sb_irregular_compound):
    if "|" in k:
        k1, k2 = k.split("|")
        si_sb_irregular_compound[k1] = si_sb_irregular_compound[k2] = (
            si_sb_irregular_compound[k]
        )
        del si_sb_irregular_compound[k]

# si_sb_irregular_keys = enclose('|'.join(si_sb_irregular.keys()))

# Z's that don't double

pl_sb_z_zes_list = ("quartz", "topaz")
pl_sb_z_zes_bysize = bysize(pl_sb_z_zes_list)

pl_sb_ze_zes_list = ("snooze",)
pl_sb_ze_zes_bysize = bysize(pl_sb_ze_zes_list)


# CLASSICAL "..is" -> "..ides"

pl_sb_C_is_ides_complete = [
    # GENERAL WORDS...
    "ephemeris",
    "iris",
    "clitoris",
    "chrysalis",
    "epididymis",
]

pl_sb_C_is_ides_endings = [
    # INFLAMATIONS...
    "itis"
]

pl_sb_C_is_ides = joinstem(
    -2, pl_sb_C_is_ides_complete + [f".*{w}" for w in pl_sb_C_is_ides_endings]
)

pl_sb_C_is_ides_list = pl_sb_C_is_ides_complete + pl_sb_C_is_ides_endings

(
    si_sb_C_is_ides_list,
    si_sb_C_is_ides_bysize,
    pl_sb_C_is_ides_bysize,
) = make_pl_si_lists(pl_sb_C_is_ides_list, "ides", 2, dojoinstem=False)


# CLASSICAL "..a" -> "..ata"

pl_sb_C_a_ata_list = (
    "anathema",
    "bema",
    "carcinoma",
    "charisma",
    "diploma",
    "dogma",
    "drama",
    "edema",
    "enema",
    "enigma",
    "lemma",
    "lymphoma",
    "magma",
    "melisma",
    "miasma",
    "oedema",
    "sarcoma",
    "schema",
    "soma",
    "stigma",
    "stoma",
    "trauma",
    "gumma",
    "pragma",
)

(
    si_sb_C_a_ata_list,
    si_sb_C_a_ata_bysize,
    pl_sb_C_a_ata_bysize,
    pl_sb_C_a_ata,
) = make_pl_si_lists(pl_sb_C_a_ata_list, "ata", 1)

# UNCONDITIONAL "..a" -> "..ae"

pl_sb_U_a_ae_list = (
    "alumna",
    "alga",
    "vertebra",
    "persona",
    "vita",
)
(
    si_sb_U_a_ae_list,
    si_sb_U_a_ae_bysize,
    pl_sb_U_a_ae_bysize,
    pl_sb_U_a_ae,
) = make_pl_si_lists(pl_sb_U_a_ae_list, "e", None)

# CLASSICAL "..a" -> "..ae"

pl_sb_C_a_ae_list = (
    "amoeba",
    "antenna",
    "formula",
    "hyperbola",
    "medusa",
    "nebula",
    "parabola",
    "abscissa",
    "hydra",
    "nova",
    "lacuna",
    "aurora",
    "umbra",
    "flora",
    "fauna",
)
(
    si_sb_C_a_ae_list,
    si_sb_C_a_ae_bysize,
    pl_sb_C_a_ae_bysize,
    pl_sb_C_a_ae,
) = make_pl_si_lists(pl_sb_C_a_ae_list, "e", None)


# CLASSICAL "..en" -> "..ina"

pl_sb_C_en_ina_list = ("stamen", "foramen", "lumen")

(
    si_sb_C_en_ina_list,
    si_sb_C_en_ina_bysize,
    pl_sb_C_en_ina_bysize,
    pl_sb_C_en_ina,
) = make_pl_si_lists(pl_sb_C_en_ina_list, "ina", 2)


# UNCONDITIONAL "..um" -> "..a"

pl_sb_U_um_a_list = (
    "bacterium",
    "agendum",
    "desideratum",
    "erratum",
    "stratum",
    "datum",
    "ovum",
    "extremum",
    "candelabrum",
)
(
    si_sb_U_um_a_list,
    si_sb_U_um_a_bysize,
    pl_sb_U_um_a_bysize,
    pl_sb_U_um_a,
) = make_pl_si_lists(pl_sb_U_um_a_list, "a", 2)

# CLASSICAL "..um" -> "..a"

pl_sb_C_um_a_list = (
    "maximum",
    "minimum",
    "momentum",
    "optimum",
    "quantum",
    "cranium",
    "curriculum",
    "dictum",
    "phylum",
    "aquarium",
    "compendium",
    "emporium",
    "encomium",
    "gymnasium",
    "honorarium",
    "interregnum",
    "lustrum",
    "memorandum",
    "millennium",
    "rostrum",
    "spectrum",
    "speculum",
    "stadium",
    "trapezium",
    "ultimatum",
    "medium",
    "vacuum",
    "velum",
    "consortium",
    "arboretum",
)

(
    si_sb_C_um_a_list,
    si_sb_C_um_a_bysize,
    pl_sb_C_um_a_bysize,
    pl_sb_C_um_a,
) = make_pl_si_lists(pl_sb_C_um_a_list, "a", 2)


# UNCONDITIONAL "..us" -> "i"

pl_sb_U_us_i_list = (
    "alumnus",
    "alveolus",
    "bacillus",
    "bronchus",
    "locus",
    "nucleus",
    "stimulus",
    "meniscus",
    "sarcophagus",
)
(
    si_sb_U_us_i_list,
    si_sb_U_us_i_bysize,
    pl_sb_U_us_i_bysize,
    pl_sb_U_us_i,
) = make_pl_si_lists(pl_sb_U_us_i_list, "i", 2)

# CLASSICAL "..us" -> "..i"

pl_sb_C_us_i_list = (
    "focus",
    "radius",
    "genius",
    "incubus",
    "succubus",
    "nimbus",
    "fungus",
    "nucleolus",
    "stylus",
    "torus",
    "umbilicus",
    "uterus",
    "hippopotamus",
    "cactus",
)

(
    si_sb_C_us_i_list,
    si_sb_C_us_i_bysize,
    pl_sb_C_us_i_bysize,
    pl_sb_C_us_i,
) = make_pl_si_lists(pl_sb_C_us_i_list, "i", 2)


# CLASSICAL "..us" -> "..us"  (ASSIMILATED 4TH DECLENSION LATIN NOUNS)

pl_sb_C_us_us = (
    "status",
    "apparatus",
    "prospectus",
    "sinus",
    "hiatus",
    "impetus",
    "plexus",
)
pl_sb_C_us_us_bysize = bysize(pl_sb_C_us_us)

# UNCONDITIONAL "..on" -> "a"

pl_sb_U_on_a_list = (
    "criterion",
    "perihelion",
    "aphelion",
    "phenomenon",
    "prolegomenon",
    "noumenon",
    "organon",
    "asyndeton",
    "hyperbaton",
)
(
    si_sb_U_on_a_list,
    si_sb_U_on_a_bysize,
    pl_sb_U_on_a_bysize,
    pl_sb_U_on_a,
) = make_pl_si_lists(pl_sb_U_on_a_list, "a", 2)

# CLASSICAL "..on" -> "..a"

pl_sb_C_on_a_list = ("oxymoron",)

(
    si_sb_C_on_a_list,
    si_sb_C_on_a_bysize,
    pl_sb_C_on_a_bysize,
    pl_sb_C_on_a,
) = make_pl_si_lists(pl_sb_C_on_a_list, "a", 2)


# CLASSICAL "..o" -> "..i"  (BUT NORMALLY -> "..os")

pl_sb_C_o_i = [
    "solo",
    "soprano",
    "basso",
    "alto",
    "contralto",
    "tempo",
    "piano",
    "virtuoso",
]  # list not tuple so can concat for pl_sb_U_o_os

pl_sb_C_o_i_bysize = bysize(pl_sb_C_o_i)
si_sb_C_o_i_bysize = bysize([f"{w[:-1]}i" for w in pl_sb_C_o_i])

pl_sb_C_o_i_stems = joinstem(-1, pl_sb_C_o_i)

# ALWAYS "..o" -> "..os"

pl_sb_U_o_os_complete = {"ado", "ISO", "NATO", "NCO", "NGO", "oto"}
si_sb_U_o_os_complete = {f"{w}s" for w in pl_sb_U_o_os_complete}


pl_sb_U_o_os_endings = [
    "aficionado",
    "aggro",
    "albino",
    "allegro",
    "ammo",
    "Antananarivo",
    "archipelago",
    "armadillo",
    "auto",
    "avocado",
    "Bamako",
    "Barquisimeto",
    "bimbo",
    "bingo",
    "Biro",
    "bolero",
    "Bolzano",
    "bongo",
    "Boto",
    "burro",
    "Cairo",
    "canto",
    "cappuccino",
    "casino",
    "cello",
    "Chicago",
    "Chimango",
    "cilantro",
    "cochito",
    "coco",
    "Colombo",
    "Colorado",
    "commando",
    "concertino",
    "contango",
    "credo",
    "crescendo",
    "cyano",
    "demo",
    "ditto",
    "Draco",
    "dynamo",
    "embryo",
    "Esperanto",
    "espresso",
    "euro",
    "falsetto",
    "Faro",
    "fiasco",
    "Filipino",
    "flamenco",
    "furioso",
    "generalissimo",
    "Gestapo",
    "ghetto",
    "gigolo",
    "gizmo",
    "Greensboro",
    "gringo",
    "Guaiabero",
    "guano",
    "gumbo",
    "gyro",
    "hairdo",
    "hippo",
    "Idaho",
    "impetigo",
    "inferno",
    "info",
    "intermezzo",
    "intertrigo",
    "Iquico",
    "jumbo",
    "junto",
    "Kakapo",
    "kilo",
    "Kinkimavo",
    "Kokako",
    "Kosovo",
    "Lesotho",
    "libero",
    "libido",
    "libretto",
    "lido",
    "Lilo",
    "limbo",
    "limo",
    "lineno",
    "lingo",
    "lino",
    "livedo",
    "loco",
    "logo",
    "lumbago",
    "macho",
    "macro",
    "mafioso",
    "magneto",
    "magnifico",
    "Majuro",
    "Malabo",
    "manifesto",
    "Maputo",
    "Maracaibo",
    "medico",
    "memo",
    "metro",
    "Mexico",
    "micro",
    "Milano",
    "Monaco",
    "mono",
    "Montenegro",
    "Morocco",
    "Muqdisho",
    "myo",
    "neutrino",
    "Ningbo",
    "octavo",
    "oregano",
    "Orinoco",
    "Orlando",
    "Oslo",
    "panto",
    "Paramaribo",
    "Pardusco",
    "pedalo",
    "photo",
    "pimento",
    "pinto",
    "pleco",
    "Pluto",
    "pogo",
    "polo",
    "poncho",
    "Porto-Novo",
    "Porto",
    "pro",
    "psycho",
    "pueblo",
    "quarto",
    "Quito",
    "repo",
    "rhino",
    "risotto",
    "rococo",
    "rondo",
    "Sacramento",
    "saddo",
    "sago",
    "salvo",
    "Santiago",
    "Sapporo",
    "Sarajevo",
    "scherzando",
    "scherzo",
    "silo",
    "sirocco",
    "sombrero",
    "staccato",
    "sterno",
    "stucco",
    "stylo",
    "sumo",
    "Taiko",
    "techno",
    "terrazzo",
    "testudo",
    "timpano",
    "tiro",
    "tobacco",
    "Togo",
    "Tokyo",
    "torero",
    "Torino",
    "Toronto",
    "torso",
    "tremolo",
    "typo",
    "tyro",
    "ufo",
    "UNESCO",
    "vaquero",
    "vermicello",
    "verso",
    "vibrato",
    "violoncello",
    "Virgo",
    "weirdo",
    "WHO",
    "WTO",
    "Yamoussoukro",
    "yo-yo",
    "zero",
    "Zibo",
] + pl_sb_C_o_i

pl_sb_U_o_os_bysize = bysize(pl_sb_U_o_os_endings)
si_sb_U_o_os_bysize = bysize([f"{w}s" for w in pl_sb_U_o_os_endings])


# UNCONDITIONAL "..ch" -> "..chs"

pl_sb_U_ch_chs_list = ("czech", "eunuch", "stomach")

(
    si_sb_U_ch_chs_list,
    si_sb_U_ch_chs_bysize,
    pl_sb_U_ch_chs_bysize,
    pl_sb_U_ch_chs,
) = make_pl_si_lists(pl_sb_U_ch_chs_list, "s", None)


# UNCONDITIONAL "..[ei]x" -> "..ices"

pl_sb_U_ex_ices_list = ("codex", "murex", "silex")
(
    si_sb_U_ex_ices_list,
    si_sb_U_ex_ices_bysize,
    pl_sb_U_ex_ices_bysize,
    pl_sb_U_ex_ices,
) = make_pl_si_lists(pl_sb_U_ex_ices_list, "ices", 2)

pl_sb_U_ix_ices_list = ("radix", "helix")
(
    si_sb_U_ix_ices_list,
    si_sb_U_ix_ices_bysize,
    pl_sb_U_ix_ices_bysize,
    pl_sb_U_ix_ices,
) = make_pl_si_lists(pl_sb_U_ix_ices_list, "ices", 2)

# CLASSICAL "..[ei]x" -> "..ices"

pl_sb_C_ex_ices_list = (
    "vortex",
    "vertex",
    "cortex",
    "latex",
    "pontifex",
    "apex",
    "index",
    "simplex",
)

(
    si_sb_C_ex_ices_list,
    si_sb_C_ex_ices_bysize,
    pl_sb_C_ex_ices_bysize,
    pl_sb_C_ex_ices,
) = make_pl_si_lists(pl_sb_C_ex_ices_list, "ices", 2)


pl_sb_C_ix_ices_list = ("appendix",)

(
    si_sb_C_ix_ices_list,
    si_sb_C_ix_ices_bysize,
    pl_sb_C_ix_ices_bysize,
    pl_sb_C_ix_ices,
) = make_pl_si_lists(pl_sb_C_ix_ices_list, "ices", 2)


# ARABIC: ".." -> "..i"

pl_sb_C_i_list = ("afrit", "afreet", "efreet")

(si_sb_C_i_list, si_sb_C_i_bysize, pl_sb_C_i_bysize, pl_sb_C_i) = make_pl_si_lists(
    pl_sb_C_i_list, "i", None
)


# HEBREW: ".." -> "..im"

pl_sb_C_im_list = ("goy", "seraph", "cherub")

(si_sb_C_im_list, si_sb_C_im_bysize, pl_sb_C_im_bysize, pl_sb_C_im) = make_pl_si_lists(
    pl_sb_C_im_list, "im", None
)


# UNCONDITIONAL "..man" -> "..mans"

pl_sb_U_man_mans_list = """
    ataman caiman cayman ceriman
    desman dolman farman harman hetman
    human leman ottoman shaman talisman
""".split()
pl_sb_U_man_mans_caps_list = """
    Alabaman Bahaman Burman German
    Hiroshiman Liman Nakayaman Norman Oklahoman
    Panaman Roman Selman Sonaman Tacoman Yakiman
    Yokohaman Yuman
""".split()

(
    si_sb_U_man_mans_list,
    si_sb_U_man_mans_bysize,
    pl_sb_U_man_mans_bysize,
) = make_pl_si_lists(pl_sb_U_man_mans_list, "s", None, dojoinstem=False)
(
    si_sb_U_man_mans_caps_list,
    si_sb_U_man_mans_caps_bysize,
    pl_sb_U_man_mans_caps_bysize,
) = make_pl_si_lists(pl_sb_U_man_mans_caps_list, "s", None, dojoinstem=False)

# UNCONDITIONAL "..louse" -> "..lice"
pl_sb_U_louse_lice_list = ("booklouse", "grapelouse", "louse", "woodlouse")

(
    si_sb_U_louse_lice_list,
    si_sb_U_louse_lice_bysize,
    pl_sb_U_louse_lice_bysize,
) = make_pl_si_lists(pl_sb_U_louse_lice_list, "lice", 5, dojoinstem=False)

pl_sb_uninflected_s_complete = [
    # PAIRS OR GROUPS SUBSUMED TO A SINGULAR...
    "breeches",
    "britches",
    "pajamas",
    "pyjamas",
    "clippers",
    "gallows",
    "hijinks",
    "headquarters",
    "pliers",
    "scissors",
    "testes",
    "herpes",
    "pincers",
    "shears",
    "proceedings",
    "trousers",
    # UNASSIMILATED LATIN 4th DECLENSION
    "cantus",
    "coitus",
    "nexus",
    # RECENT IMPORTS...
    "contretemps",
    "corps",
    "debris",
    "siemens",
    # DISEASES
    "mumps",
    # MISCELLANEOUS OTHERS...
    "diabetes",
    "jackanapes",
    "series",
    "species",
    "subspecies",
    "rabies",
    "chassis",
    "innings",
    "news",
    "mews",
    "haggis",
]

pl_sb_uninflected_s_endings = [
    # RECENT IMPORTS...
    "ois",
    # DISEASES
    "measles",
]

pl_sb_uninflected_s = pl_sb_uninflected_s_complete + [
    f".*{w}" for w in pl_sb_uninflected_s_endings
]

pl_sb_uninflected_herd = (
    # DON'T INFLECT IN CLASSICAL MODE, OTHERWISE NORMAL INFLECTION
    "wildebeest",
    "swine",
    "eland",
    "bison",
    "buffalo",
    "cattle",
    "elk",
    "rhinoceros",
    "zucchini",
    "caribou",
    "dace",
    "grouse",
    "guinea fowl",
    "guinea-fowl",
    "haddock",
    "hake",
    "halibut",
    "herring",
    "mackerel",
    "pickerel",
    "pike",
    "roe",
    "seed",
    "shad",
    "snipe",
    "teal",
    "turbot",
    "water fowl",
    "water-fowl",
)

pl_sb_uninflected_complete = [
    # SOME FISH AND HERD ANIMALS
    "tuna",
    "salmon",
    "mackerel",
    "trout",
    "bream",
    "sea-bass",
    "sea bass",
    "carp",
    "cod",
    "flounder",
    "whiting",
    "moose",
    # OTHER ODDITIES
    "graffiti",
    "djinn",
    "samuri",
    "offspring",
    "pence",
    "quid",
    "hertz",
] + pl_sb_uninflected_s_complete
# SOME WORDS ENDING IN ...s (OFTEN PAIRS TAKEN AS A WHOLE)

pl_sb_uninflected_caps = [
    # ALL NATIONALS ENDING IN -ese
    "Portuguese",
    "Amoyese",
    "Borghese",
    "Congoese",
    "Faroese",
    "Foochowese",
    "Genevese",
    "Genoese",
    "Gilbertese",
    "Hottentotese",
    "Kiplingese",
    "Kongoese",
    "Lucchese",
    "Maltese",
    "Nankingese",
    "Niasese",
    "Pekingese",
    "Piedmontese",
    "Pistoiese",
    "Sarawakese",
    "Shavese",
    "Vermontese",
    "Wenchowese",
    "Yengeese",
]


pl_sb_uninflected_endings = [
    # UNCOUNTABLE NOUNS
    "butter",
    "cash",
    "furniture",
    "information",
    # SOME FISH AND HERD ANIMALS
    "fish",
    "deer",
    "sheep",
    # ALL NATIONALS ENDING IN -ese
    "nese",
    "rese",
    "lese",
    "mese",
    # DISEASES
    "pox",
    # OTHER ODDITIES
    "craft",
] + pl_sb_uninflected_s_endings
# SOME WORDS ENDING IN ...s (OFTEN PAIRS TAKEN AS A WHOLE)


pl_sb_uninflected_bysize = bysize(pl_sb_uninflected_endings)


# SINGULAR WORDS ENDING IN ...s (ALL INFLECT WITH ...es)

pl_sb_singular_s_complete = [
    "acropolis",
    "aegis",
    "alias",
    "asbestos",
    "bathos",
    "bias",
    "bronchitis",
    "bursitis",
    "caddis",
    "cannabis",
    "canvas",
    "chaos",
    "cosmos",
    "dais",
    "digitalis",
    "epidermis",
    "ethos",
    "eyas",
    "gas",
    "glottis",
    "hubris",
    "ibis",
    "lens",
    "mantis",
    "marquis",
    "metropolis",
    "pathos",
    "pelvis",
    "polis",
    "rhinoceros",
    "sassafras",
    "trellis",
] + pl_sb_C_is_ides_complete


pl_sb_singular_s_endings = ["ss", "us"] + pl_sb_C_is_ides_endings

pl_sb_singular_s_bysize = bysize(pl_sb_singular_s_endings)

si_sb_singular_s_complete = [f"{w}es" for w in pl_sb_singular_s_complete]
si_sb_singular_s_endings = [f"{w}es" for w in pl_sb_singular_s_endings]
si_sb_singular_s_bysize = bysize(si_sb_singular_s_endings)

pl_sb_singular_s_es = ["[A-Z].*es"]

pl_sb_singular_s = enclose(
    "|".join(
        pl_sb_singular_s_complete
        + [f".*{w}" for w in pl_sb_singular_s_endings]
        + pl_sb_singular_s_es
    )
)


# PLURALS ENDING IN uses -> use


si_sb_ois_oi_case = ("Bolshois", "Hanois")

si_sb_uses_use_case = ("Betelgeuses", "Duses", "Meuses", "Syracuses", "Toulouses")

si_sb_uses_use = (
    "abuses",
    "applauses",
    "blouses",
    "carouses",
    "causes",
    "chartreuses",
    "clauses",
    "contuses",
    "douses",
    "excuses",
    "fuses",
    "grouses",
    "hypotenuses",
    "masseuses",
    "menopauses",
    "misuses",
    "muses",
    "overuses",
    "pauses",
    "peruses",
    "profuses",
    "recluses",
    "reuses",
    "ruses",
    "souses",
    "spouses",
    "suffuses",
    "transfuses",
    "uses",
)

si_sb_ies_ie_case = (
    "Addies",
    "Aggies",
    "Allies",
    "Amies",
    "Angies",
    "Annies",
    "Annmaries",
    "Archies",
    "Arties",
    "Aussies",
    "Barbies",
    "Barries",
    "Basies",
    "Bennies",
    "Bernies",
    "Berties",
    "Bessies",
    "Betties",
    "Billies",
    "Blondies",
    "Bobbies",
    "Bonnies",
    "Bowies",
    "Brandies",
    "Bries",
    "Brownies",
    "Callies",
    "Carnegies",
    "Carries",
    "Cassies",
    "Charlies",
    "Cheries",
    "Christies",
    "Connies",
    "Curies",
    "Dannies",
    "Debbies",
    "Dixies",
    "Dollies",
    "Donnies",
    "Drambuies",
    "Eddies",
    "Effies",
    "Ellies",
    "Elsies",
    "Eries",
    "Ernies",
    "Essies",
    "Eugenies",
    "Fannies",
    "Flossies",
    "Frankies",
    "Freddies",
    "Gillespies",
    "Goldies",
    "Gracies",
    "Guthries",
    "Hallies",
    "Hatties",
    "Hetties",
    "Hollies",
    "Jackies",
    "Jamies",
    "Janies",
    "Jannies",
    "Jeanies",
    "Jeannies",
    "Jennies",
    "Jessies",
    "Jimmies",
    "Jodies",
    "Johnies",
    "Johnnies",
    "Josies",
    "Julies",
    "Kalgoorlies",
    "Kathies",
    "Katies",
    "Kellies",
    "Kewpies",
    "Kristies",
    "Laramies",
    "Lassies",
    "Lauries",
    "Leslies",
    "Lessies",
    "Lillies",
    "Lizzies",
    "Lonnies",
    "Lories",
    "Lorries",
    "Lotties",
    "Louies",
    "Mackenzies",
    "Maggies",
    "Maisies",
    "Mamies",
    "Marcies",
    "Margies",
    "Maries",
    "Marjories",
    "Matties",
    "McKenzies",
    "Melanies",
    "Mickies",
    "Millies",
    "Minnies",
    "Mollies",
    "Mounties",
    "Nannies",
    "Natalies",
    "Nellies",
    "Netties",
    "Ollies",
    "Ozzies",
    "Pearlies",
    "Pottawatomies",
    "Reggies",
    "Richies",
    "Rickies",
    "Robbies",
    "Ronnies",
    "Rosalies",
    "Rosemaries",
    "Rosies",
    "Roxies",
    "Rushdies",
    "Ruthies",
    "Sadies",
    "Sallies",
    "Sammies",
    "Scotties",
    "Selassies",
    "Sherries",
    "Sophies",
    "Stacies",
    "Stefanies",
    "Stephanies",
    "Stevies",
    "Susies",
    "Sylvies",
    "Tammies",
    "Terries",
    "Tessies",
    "Tommies",
    "Tracies",
    "Trekkies",
    "Valaries",
    "Valeries",
    "Valkyries",
    "Vickies",
    "Virgies",
    "Willies",
    "Winnies",
    "Wylies",
    "Yorkies",
)

si_sb_ies_ie = (
    "aeries",
    "baggies",
    "belies",
    "biggies",
    "birdies",
    "bogies",
    "bonnies",
    "boogies",
    "bookies",
    "bourgeoisies",
    "brownies",
    "budgies",
    "caddies",
    "calories",
    "camaraderies",
    "cockamamies",
    "collies",
    "cookies",
    "coolies",
    "cooties",
    "coteries",
    "crappies",
    "curies",
    "cutesies",
    "dogies",
    "eyries",
    "floozies",
    "footsies",
    "freebies",
    "genies",
    "goalies",
    "groupies",
    "hies",
    "jalousies",
    "junkies",
    "kiddies",
    "laddies",
    "lassies",
    "lies",
    "lingeries",
    "magpies",
    "menageries",
    "mommies",
    "movies",
    "neckties",
    "newbies",
    "nighties",
    "oldies",
    "organdies",
    "overlies",
    "pies",
    "pinkies",
    "pixies",
    "potpies",
    "prairies",
    "quickies",
    "reveries",
    "rookies",
    "rotisseries",
    "softies",
    "sorties",
    "species",
    "stymies",
    "sweeties",
    "ties",
    "underlies",
    "unties",
    "veggies",
    "vies",
    "yuppies",
    "zombies",
)


si_sb_oes_oe_case = (
    "Chloes",
    "Crusoes",
    "Defoes",
    "Faeroes",
    "Ivanhoes",
    "Joes",
    "McEnroes",
    "Moes",
    "Monroes",
    "Noes",
    "Poes",
    "Roscoes",
    "Tahoes",
    "Tippecanoes",
    "Zoes",
)

si_sb_oes_oe = (
    "aloes",
    "backhoes",
    "canoes",
    "does",
    "floes",
    "foes",
    "hoes",
    "mistletoes",
    "oboes",
    "pekoes",
    "roes",
    "sloes",
    "throes",
    "tiptoes",
    "toes",
    "woes",
)

si_sb_z_zes = ("quartzes", "topazes")

si_sb_zzes_zz = ("buzzes", "fizzes", "frizzes", "razzes")

si_sb_ches_che_case = (
    "Andromaches",
    "Apaches",
    "Blanches",
    "Comanches",
    "Nietzsches",
    "Porsches",
    "Roches",
)

si_sb_ches_che = (
    "aches",
    "avalanches",
    "backaches",
    "bellyaches",
    "caches",
    "cloches",
    "creches",
    "douches",
    "earaches",
    "fiches",
    "headaches",
    "heartaches",
    "microfiches",
    "niches",
    "pastiches",
    "psyches",
    "quiches",
    "stomachaches",
    "toothaches",
    "tranches",
)

si_sb_xes_xe = ("annexes", "axes", "deluxes", "pickaxes")

si_sb_sses_sse_case = ("Hesses", "Jesses", "Larousses", "Matisses")
si_sb_sses_sse = (
    "bouillabaisses",
    "crevasses",
    "demitasses",
    "impasses",
    "mousses",
    "posses",
)

si_sb_ves_ve_case = (
    # *[nwl]ives -> [nwl]live
    "Clives",
    "Palmolives",
)
si_sb_ves_ve = (
    # *[^d]eaves -> eave
    "interweaves",
    "weaves",
    # *[nwl]ives -> [nwl]live
    "olives",
    # *[eoa]lves -> [eoa]lve
    "bivalves",
    "dissolves",
    "resolves",
    "salves",
    "twelves",
    "valves",
)


# Postfix adjective data
_pl_sb_postfix_adj_defn = (
    ("general", enclose(r"(?!major|lieutenant|brigadier|adjutant|.*star)\S+")),
    ("martial", enclose("court")),
    ("force", enclose("pound")),
)

pl_sb_postfix_adj: Iterable[str] = (
    enclose(val + f"(?=(?:-|\\s+){key})") for key, val in _pl_sb_postfix_adj_defn
)

pl_sb_postfix_adj_stems = f"({'|'.join(pl_sb_postfix_adj)})(.*)"


# PLURAL WORDS ENDING IS es GO TO SINGULAR is

si_sb_es_is = (
    "amanuenses",
    "amniocenteses",
    "analyses",
    "antitheses",
    "apotheoses",
    "arterioscleroses",
    "atheroscleroses",
    "axes",
    # 'bases', # bases -> basis
    "catalyses",
    "catharses",
    "chasses",
    "cirrhoses",
    "cocces",
    "crises",
    "diagnoses",
    "dialyses",
    "diereses",
    "electrolyses",
    "emphases",
    "exegeses",
    "geneses",
    "halitoses",
    "hydrolyses",
    "hypnoses",
    "hypotheses",
    "hystereses",
    "metamorphoses",
    "metastases",
    "misdiagnoses",
    "mitoses",
    "mononucleoses",
    "narcoses",
    "necroses",
    "nemeses",
    "neuroses",
    "oases",
    "osmoses",
    "osteoporoses",
    "paralyses",
    "parentheses",
    "parthenogeneses",
    "periphrases",
    "photosyntheses",
    "probosces",
    "prognoses",
    "prophylaxes",
    "prostheses",
    "preces",
    "psoriases",
    "psychoanalyses",
    "psychokineses",
    "psychoses",
    "scleroses",
    "scolioses",
    "sepses",
    "silicoses",
    "symbioses",
    "synopses",
    "syntheses",
    "taxes",
    "telekineses",
    "theses",
    "thromboses",
    "tuberculoses",
    "urinalyses",
)

pl_prep_list = """
    about above across after among around at athwart before behind
    below beneath beside besides between betwixt beyond but by
    during except for from in into near of off on onto out over
    since till to under until unto upon with""".split()

pl_prep_list_da = pl_prep_list + ["de", "du", "da"]

pl_prep_bysize = bysize(pl_prep_list_da)

pl_prep = enclose("|".join(pl_prep_list_da))

pl_sb_prep_dual_compound = rf"(.*?)((?:-|\s+)(?:{pl_prep})(?:-|\s+))a(?:-|\s+)(.*)"


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


# Pre-compiled regex patterns for plurals domain

PL_SB_POSTFIX_ADJ_STEMS_RE = re.compile(
    rf"^(?:{pl_sb_postfix_adj_stems})$", re.IGNORECASE
)
PL_SB_PREP_DUAL_COMPOUND_RE = re.compile(
    rf"^(?:{pl_sb_prep_dual_compound})$", re.IGNORECASE
)
DENOMINATOR = re.compile(r"(?P<denominator>.+)( (per|a) .+)")


# ---------------------------------------------------------------------------
# Domain logic functions (take engine instance as first param where needed)
# ---------------------------------------------------------------------------


def _find_pivot(words, candidates):
    """Find the pivot word in a list of words."""
    pivots = (
        index for index in range(1, len(words) - 1) if words[index] in candidates
    )
    try:
        return next(pivots)
    except StopIteration:
        raise ValueError("No pivot found") from None


def _handle_prepositional_phrase(phrase, transform, sep):
    """
    Given a word or phrase possibly separated by sep, parse out
    the prepositional phrase and apply the transform to the word
    preceding the prepositional phrase.

    Raise ValueError if the pivot is not found or if at least two
    separators are not found.

    >>> _handle_prepositional_phrase("man-of-war", str.upper, '-')
    'MAN-of-war'
    >>> _handle_prepositional_phrase("man of war", str.upper, ' ')
    'MAN of war'
    """
    parts = phrase.split(sep)
    if len(parts) < 3:
        raise ValueError("Cannot handle words with fewer than two separators")

    pivot = _find_pivot(parts, pl_prep_list_da)

    transformed = transform(parts[pivot - 1]) or parts[pivot - 1]
    return " ".join(
        parts[: pivot - 1] + [sep.join([transformed, parts[pivot], ''])]
    ) + " ".join(parts[(pivot + 1) :])


def _handle_long_compounds(engine, word, count):
    """
    Handles the plural and singular for compound `Words` that
    have three or more words, based on the given count.

    >>> p = __import__('inflect').engine()
    >>> _handle_long_compounds(p, Words("pair of scissors"), 2)
    'pairs of scissors'
    >>> _handle_long_compounds(p, Words("men beyond hills"), 1)
    'man beyond hills'
    """
    inflection = _sinoun if count == 1 else _plnoun
    solutions = (
        " ".join(
            itertools.chain(
                leader,
                [inflection(engine, cand, count), prep],
                trailer,
            )
        )
        for leader, (cand, prep), trailer in windowed_complete(word.split_, 2)
        if prep in pl_prep_list_da
    )
    return next(solutions, None)


def _plnoun(engine, word: str, count=None) -> str:  # noqa: C901
    count = engine.get_count(count)

    # DEFAULT TO PLURAL

    if count == 1:
        return word

    # HANDLE USER-DEFINED NOUNS

    value = engine.ud_match(word, engine.pl_sb_user_defined)
    if value is not None:
        return value

    # HANDLE EMPTY WORD, SINGULAR COUNT AND UNINFLECTED PLURALS

    if word == "":
        return word

    word = Words(word)

    if word.last.lower() in pl_sb_uninflected_complete:
        if len(word.split_) >= 3:
            return _handle_long_compounds(engine, word, count=2) or word
        return word

    if word in pl_sb_uninflected_caps:
        return word

    for k, v in pl_sb_uninflected_bysize.items():
        if word.lowered[-k:] in v:
            return word

    if engine.classical_dict["herd"] and word.last.lower() in pl_sb_uninflected_herd:
        return word

    # HANDLE COMPOUNDS ("Governor General", "mother-in-law", "aide-de-camp", ETC.)

    mo = PL_SB_POSTFIX_ADJ_STEMS_RE.search(word)
    if mo and mo.group(2) != "":
        return f"{_plnoun(engine, mo.group(1), 2)}{mo.group(2)}"

    if " a " in word.lowered or "-a-" in word.lowered:
        mo = PL_SB_PREP_DUAL_COMPOUND_RE.search(word)
        if mo and mo.group(2) != "" and mo.group(3) != "":
            return (
                f"{_plnoun(engine, mo.group(1), 2)}"
                f"{mo.group(2)}"
                f"{_plnoun(engine, mo.group(3))}"
            )

    if len(word.split_) >= 3:
        handled_words = _handle_long_compounds(engine, word, count=2)
        if handled_words is not None:
            return handled_words

    # only pluralize denominators in units
    mo = DENOMINATOR.search(word.lowered)
    if mo:
        index = len(mo.group("denominator"))
        return f"{_plnoun(engine, word[:index])}{word[index:]}"

    # handle units given in degrees (only accept if
    # there is no more than one word following)
    # degree Celsius => degrees Celsius but degree
    # fahrenheit hour => degree fahrenheit hours
    if len(word.split_) >= 2 and word.split_[-2] == "degree":
        return " ".join([_plnoun(engine, word.first)] + word.split_[1:])

    with contextlib.suppress(ValueError):
        return _handle_prepositional_phrase(
            word.lowered,
            functools.partial(_plnoun, engine, count=2),
            '-',
        )

    # HANDLE PRONOUNS

    for k, v in pl_pron_acc_keys_bysize.items():
        if word.lowered[-k:] in v:  # ends with accusative pronoun
            for pk, pv in pl_prep_bysize.items():
                if word.lowered[:pk] in pv:  # starts with a prep
                    if word.lowered.split() == [
                        word.lowered[:pk],
                        word.lowered[-k:],
                    ]:
                        # only whitespace in between
                        return word.lowered[:-k] + pl_pron_acc[word.lowered[-k:]]

    try:
        return pl_pron_nom[word.lowered]
    except KeyError:
        pass

    try:
        return pl_pron_acc[word.lowered]
    except KeyError:
        pass

    # HANDLE ISOLATED IRREGULAR PLURALS

    if word.last in pl_sb_irregular_caps:
        llen = len(word.last)
        return f"{word[:-llen]}{pl_sb_irregular_caps[word.last]}"

    lowered_last = word.last.lower()
    if lowered_last in pl_sb_irregular:
        llen = len(lowered_last)
        return f"{word[:-llen]}{pl_sb_irregular[lowered_last]}"

    dash_split = word.lowered.split('-')
    if (" ".join(dash_split[-2:])).lower() in pl_sb_irregular_compound:
        llen = len(
            " ".join(dash_split[-2:])
        )  # TODO: what if 2 spaces between these words?
        return (
            f"{word[:-llen]}"
            f"{pl_sb_irregular_compound[(' '.join(dash_split[-2:])).lower()]}"
        )

    if word.lowered[-3:] == "quy":
        return f"{word[:-1]}ies"

    if word.lowered[-6:] == "person":
        if engine.classical_dict["persons"]:
            return f"{word}s"
        else:
            return f"{word[:-4]}ople"

    # HANDLE FAMILIES OF IRREGULAR PLURALS

    if word.lowered[-3:] == "man":
        for k, v in pl_sb_U_man_mans_bysize.items():
            if word.lowered[-k:] in v:
                return f"{word}s"
        for k, v in pl_sb_U_man_mans_caps_bysize.items():
            if word[-k:] in v:
                return f"{word}s"
        return f"{word[:-3]}men"
    if word.lowered[-5:] == "mouse":
        return f"{word[:-5]}mice"
    if word.lowered[-5:] == "louse":
        v = pl_sb_U_louse_lice_bysize.get(len(word))
        if v and word.lowered in v:
            return f"{word[:-5]}lice"
        return f"{word}s"
    if word.lowered[-5:] == "goose":
        return f"{word[:-5]}geese"
    if word.lowered[-5:] == "tooth":
        return f"{word[:-5]}teeth"
    if word.lowered[-4:] == "foot":
        return f"{word[:-4]}feet"
    if word.lowered[-4:] == "taco":
        return f"{word[:-5]}tacos"

    if word.lowered == "die":
        return "dice"

    # HANDLE UNASSIMILATED IMPORTS

    if word.lowered[-4:] == "ceps":
        return word
    if word.lowered[-4:] == "zoon":
        return f"{word[:-2]}a"
    if word.lowered[-3:] in ("cis", "sis", "xis"):
        return f"{word[:-2]}es"

    for lastlet, d, numend, post in (
        ("h", pl_sb_U_ch_chs_bysize, None, "s"),
        ("x", pl_sb_U_ex_ices_bysize, -2, "ices"),
        ("x", pl_sb_U_ix_ices_bysize, -2, "ices"),
        ("m", pl_sb_U_um_a_bysize, -2, "a"),
        ("s", pl_sb_U_us_i_bysize, -2, "i"),
        ("n", pl_sb_U_on_a_bysize, -2, "a"),
        ("a", pl_sb_U_a_ae_bysize, None, "e"),
    ):
        if word.lowered[-1] == lastlet:  # this test to add speed
            for k, v in d.items():
                if word.lowered[-k:] in v:
                    return word[:numend] + post

    # HANDLE INCOMPLETELY ASSIMILATED IMPORTS

    if engine.classical_dict["ancient"]:
        if word.lowered[-4:] == "trix":
            return f"{word[:-1]}ces"
        if word.lowered[-3:] in ("eau", "ieu"):
            return f"{word}x"
        if word.lowered[-3:] in ("ynx", "inx", "anx") and len(word) > 4:
            return f"{word[:-1]}ges"

        for lastlet, d, numend, post in (
            ("n", pl_sb_C_en_ina_bysize, -2, "ina"),
            ("x", pl_sb_C_ex_ices_bysize, -2, "ices"),
            ("x", pl_sb_C_ix_ices_bysize, -2, "ices"),
            ("m", pl_sb_C_um_a_bysize, -2, "a"),
            ("s", pl_sb_C_us_i_bysize, -2, "i"),
            ("s", pl_sb_C_us_us_bysize, None, ""),
            ("a", pl_sb_C_a_ae_bysize, None, "e"),
            ("a", pl_sb_C_a_ata_bysize, None, "ta"),
            ("s", pl_sb_C_is_ides_bysize, -1, "des"),
            ("o", pl_sb_C_o_i_bysize, -1, "i"),
            ("n", pl_sb_C_on_a_bysize, -2, "a"),
        ):
            if word.lowered[-1] == lastlet:  # this test to add speed
                for k, v in d.items():
                    if word.lowered[-k:] in v:
                        return word[:numend] + post

        for d, numend, post in (
            (pl_sb_C_i_bysize, None, "i"),
            (pl_sb_C_im_bysize, None, "im"),
        ):
            for k, v in d.items():
                if word.lowered[-k:] in v:
                    return word[:numend] + post

    # HANDLE SINGULAR NOUNS ENDING IN ...s OR OTHER SILIBANTS

    if lowered_last in pl_sb_singular_s_complete:
        return f"{word}es"

    for k, v in pl_sb_singular_s_bysize.items():
        if word.lowered[-k:] in v:
            return f"{word}es"

    if word.lowered[-2:] == "es" and word[0] == word[0].upper():
        return f"{word}es"

    if word.lowered[-1] == "z":
        for k, v in pl_sb_z_zes_bysize.items():
            if word.lowered[-k:] in v:
                return f"{word}es"

        if word.lowered[-2:-1] != "z":
            return f"{word}zes"

    if word.lowered[-2:] == "ze":
        for k, v in pl_sb_ze_zes_bysize.items():
            if word.lowered[-k:] in v:
                return f"{word}s"

    if word.lowered[-2:] in ("ch", "sh", "zz", "ss") or word.lowered[-1] == "x":
        return f"{word}es"

    # HANDLE ...f -> ...ves

    if word.lowered[-3:] in ("elf", "alf", "olf"):
        return f"{word[:-1]}ves"
    if word.lowered[-3:] == "eaf" and word.lowered[-4:-3] != "d":
        return f"{word[:-1]}ves"
    if word.lowered[-4:] in ("nife", "life", "wife"):
        return f"{word[:-2]}ves"
    if word.lowered[-3:] == "arf":
        return f"{word[:-1]}ves"

    # HANDLE ...y

    if word.lowered[-1] == "y":
        if word.lowered[-2:-1] in "aeiou" or len(word) == 1:
            return f"{word}s"

        if engine.classical_dict["names"]:
            if word.lowered[-1] == "y" and word[0] == word[0].upper():
                return f"{word}s"

        return f"{word[:-1]}ies"

    # HANDLE ...o

    if lowered_last in pl_sb_U_o_os_complete:
        return f"{word}s"

    for k, v in pl_sb_U_o_os_bysize.items():
        if word.lowered[-k:] in v:
            return f"{word}s"

    if word.lowered[-2:] in ("ao", "eo", "io", "oo", "uo"):
        return f"{word}s"

    if word.lowered[-1] == "o":
        return f"{word}es"

    # OTHERWISE JUST ADD ...s

    return f"{word}s"


def _sinoun(engine, word: str, count=None, gender=None):  # noqa: C901
    count = engine.get_count(count)

    # DEFAULT TO PLURAL

    if count == 2:
        return word

    # SET THE GENDER

    try:
        if gender is None:
            gender = engine.thegender
        elif gender not in singular_pronoun_genders:
            raise BadGenderError
    except (TypeError, IndexError) as err:
        raise BadGenderError from err

    # HANDLE USER-DEFINED NOUNS

    value = engine.ud_match(word, engine.si_sb_user_defined)
    if value is not None:
        return value

    # HANDLE EMPTY WORD, SINGULAR COUNT AND UNINFLECTED PLURALS

    if word == "":
        return word

    if word in si_sb_ois_oi_case:
        return word[:-1]

    words = Words(word)

    if words.last.lower() in pl_sb_uninflected_complete:
        if len(words.split_) >= 3:
            return _handle_long_compounds(engine, words, count=1) or word
        return word

    if word in pl_sb_uninflected_caps:
        return word

    for k, v in pl_sb_uninflected_bysize.items():
        if words.lowered[-k:] in v:
            return word

    if engine.classical_dict["herd"] and words.last.lower() in pl_sb_uninflected_herd:
        return word

    if words.last.lower() in pl_sb_C_us_us:
        return word if engine.classical_dict["ancient"] else False

    # HANDLE COMPOUNDS ("Governor General", "mother-in-law", "aide-de-camp", ETC.)

    mo = PL_SB_POSTFIX_ADJ_STEMS_RE.search(word)
    if mo and mo.group(2) != "":
        return f"{_sinoun(engine, mo.group(1), 1, gender=gender)}{mo.group(2)}"

    with contextlib.suppress(ValueError):
        return _handle_prepositional_phrase(
            words.lowered,
            functools.partial(_sinoun, engine, count=1, gender=gender),
            ' ',
        )

    with contextlib.suppress(ValueError):
        return _handle_prepositional_phrase(
            words.lowered,
            functools.partial(_sinoun, engine, count=1, gender=gender),
            '-',
        )

    # HANDLE PRONOUNS

    for k, v in si_pron_acc_keys_bysize.items():
        if words.lowered[-k:] in v:  # ends with accusative pronoun
            for pk, pv in pl_prep_bysize.items():
                if words.lowered[:pk] in pv:  # starts with a prep
                    if words.lowered.split() == [
                        words.lowered[:pk],
                        words.lowered[-k:],
                    ]:
                        # only whitespace in between
                        return words.lowered[:-k] + get_si_pron(
                            "acc", words.lowered[-k:], gender
                        )

    try:
        return get_si_pron("nom", words.lowered, gender)
    except KeyError:
        pass

    try:
        return get_si_pron("acc", words.lowered, gender)
    except KeyError:
        pass

    # HANDLE ISOLATED IRREGULAR PLURALS

    if words.last in si_sb_irregular_caps:
        llen = len(words.last)
        return f"{word[:-llen]}{si_sb_irregular_caps[words.last]}"

    if words.last.lower() in si_sb_irregular:
        llen = len(words.last.lower())
        return f"{word[:-llen]}{si_sb_irregular[words.last.lower()]}"

    dash_split = words.lowered.split("-")
    if (" ".join(dash_split[-2:])).lower() in si_sb_irregular_compound:
        llen = len(
            " ".join(dash_split[-2:])
        )  # TODO: what if 2 spaces between these words?
        return "{}{}".format(
            word[:-llen],
            si_sb_irregular_compound[(" ".join(dash_split[-2:])).lower()],
        )

    if words.lowered[-5:] == "quies":
        return word[:-3] + "y"

    if words.lowered[-7:] == "persons":
        return word[:-1]
    if words.lowered[-6:] == "people":
        return word[:-4] + "rson"

    # HANDLE FAMILIES OF IRREGULAR PLURALS

    if words.lowered[-4:] == "mans":
        for k, v in si_sb_U_man_mans_bysize.items():
            if words.lowered[-k:] in v:
                return word[:-1]
        for k, v in si_sb_U_man_mans_caps_bysize.items():
            if word[-k:] in v:
                return word[:-1]
    if words.lowered[-3:] == "men":
        return word[:-3] + "man"
    if words.lowered[-4:] == "mice":
        return word[:-4] + "mouse"
    if words.lowered[-4:] == "lice":
        v = si_sb_U_louse_lice_bysize.get(len(word))
        if v and words.lowered in v:
            return word[:-4] + "louse"
    if words.lowered[-5:] == "geese":
        return word[:-5] + "goose"
    if words.lowered[-5:] == "teeth":
        return word[:-5] + "tooth"
    if words.lowered[-4:] == "feet":
        return word[:-4] + "foot"

    if words.lowered == "dice":
        return "die"

    # HANDLE UNASSIMILATED IMPORTS

    if words.lowered[-4:] == "ceps":
        return word
    if words.lowered[-3:] == "zoa":
        return word[:-1] + "on"

    for lastlet, d, unass_numend, post in (
        ("s", si_sb_U_ch_chs_bysize, -1, ""),
        ("s", si_sb_U_ex_ices_bysize, -4, "ex"),
        ("s", si_sb_U_ix_ices_bysize, -4, "ix"),
        ("a", si_sb_U_um_a_bysize, -1, "um"),
        ("i", si_sb_U_us_i_bysize, -1, "us"),
        ("a", si_sb_U_on_a_bysize, -1, "on"),
        ("e", si_sb_U_a_ae_bysize, -1, ""),
    ):
        if words.lowered[-1] == lastlet:  # this test to add speed
            for k, v in d.items():
                if words.lowered[-k:] in v:
                    return word[:unass_numend] + post

    # HANDLE INCOMPLETELY ASSIMILATED IMPORTS

    if engine.classical_dict["ancient"]:
        if words.lowered[-6:] == "trices":
            return word[:-3] + "x"
        if words.lowered[-4:] in ("eaux", "ieux"):
            return word[:-1]
        if words.lowered[-5:] in ("ynges", "inges", "anges") and len(word) > 6:
            return word[:-3] + "x"

        for lastlet, d, class_numend, post in (
            ("a", si_sb_C_en_ina_bysize, -3, "en"),
            ("s", si_sb_C_ex_ices_bysize, -4, "ex"),
            ("s", si_sb_C_ix_ices_bysize, -4, "ix"),
            ("a", si_sb_C_um_a_bysize, -1, "um"),
            ("i", si_sb_C_us_i_bysize, -1, "us"),
            ("s", pl_sb_C_us_us_bysize, None, ""),
            ("e", si_sb_C_a_ae_bysize, -1, ""),
            ("a", si_sb_C_a_ata_bysize, -2, ""),
            ("s", si_sb_C_is_ides_bysize, -3, "s"),
            ("i", si_sb_C_o_i_bysize, -1, "o"),
            ("a", si_sb_C_on_a_bysize, -1, "on"),
            ("m", si_sb_C_im_bysize, -2, ""),
            ("i", si_sb_C_i_bysize, -1, ""),
        ):
            if words.lowered[-1] == lastlet:  # this test to add speed
                for k, v in d.items():
                    if words.lowered[-k:] in v:
                        return word[:class_numend] + post

    # HANDLE PLURLS ENDING IN uses -> use

    if (
        words.lowered[-6:] == "houses"
        or word in si_sb_uses_use_case
        or words.last.lower() in si_sb_uses_use
    ):
        return word[:-1]

    # HANDLE PLURLS ENDING IN ies -> ie

    if word in si_sb_ies_ie_case or words.last.lower() in si_sb_ies_ie:
        return word[:-1]

    # HANDLE PLURLS ENDING IN oes -> oe

    if (
        words.lowered[-5:] == "shoes"
        or word in si_sb_oes_oe_case
        or words.last.lower() in si_sb_oes_oe
    ):
        return word[:-1]

    # HANDLE SINGULAR NOUNS ENDING IN ...s OR OTHER SILIBANTS

    if word in si_sb_sses_sse_case or words.last.lower() in si_sb_sses_sse:
        return word[:-1]

    if words.last.lower() in si_sb_singular_s_complete:
        return word[:-2]

    for k, v in si_sb_singular_s_bysize.items():
        if words.lowered[-k:] in v:
            return word[:-2]

    if words.lowered[-4:] == "eses" and word[0] == word[0].upper():
        return word[:-2]

    if words.last.lower() in si_sb_z_zes:
        return word[:-2]

    if words.last.lower() in si_sb_zzes_zz:
        return word[:-2]

    if words.lowered[-4:] == "zzes":
        return word[:-3]

    if word in si_sb_ches_che_case or words.last.lower() in si_sb_ches_che:
        return word[:-1]

    if words.lowered[-4:] in ("ches", "shes"):
        return word[:-2]

    if words.last.lower() in si_sb_xes_xe:
        return word[:-1]

    if words.lowered[-3:] == "xes":
        return word[:-2]

    # HANDLE ...f -> ...ves

    if word in si_sb_ves_ve_case or words.last.lower() in si_sb_ves_ve:
        return word[:-1]

    if words.lowered[-3:] == "ves":
        if words.lowered[-5:-3] in ("el", "al", "ol"):
            return word[:-3] + "f"
        if words.lowered[-5:-3] == "ea" and word[-6:-5] != "d":
            return word[:-3] + "f"
        if words.lowered[-5:-3] in ("ni", "li", "wi"):
            return word[:-3] + "fe"
        if words.lowered[-5:-3] == "ar":
            return word[:-3] + "f"

    # HANDLE ...y

    if words.lowered[-2:] == "ys":
        if len(words.lowered) > 2 and words.lowered[-3] in "aeiou":
            return word[:-1]

        if engine.classical_dict["names"]:
            if words.lowered[-2:] == "ys" and word[0] == word[0].upper():
                return word[:-1]

    if words.lowered[-3:] == "ies":
        return word[:-3] + "y"

    # HANDLE ...o

    if words.lowered[-2:] == "os":
        if words.last.lower() in si_sb_U_o_os_complete:
            return word[:-1]

        for k, v in si_sb_U_o_os_bysize.items():
            if words.lowered[-k:] in v:
                return word[:-1]

        if words.lowered[-3:] in ("aos", "eos", "ios", "oos", "uos"):
            return word[:-1]

    if words.lowered[-3:] == "oes":
        return word[:-2]

    # UNASSIMILATED IMPORTS FINAL RULE

    if word in si_sb_es_is:
        return word[:-2] + "is"

    # OTHERWISE JUST REMOVE ...s

    if words.lowered[-1] == "s":
        return word[:-1]

    # COULD NOT FIND SINGULAR

    return False
