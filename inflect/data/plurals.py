"""
Plural-related word lists, verb conjugation data, adjective data,
and pre-compiled regex patterns derived from these lists.

This module contains:
- pl_sb_* (plural noun) word lists and bysize tables
- si_sb_* (singular noun) data derived via make_pl_si_lists
- plverb_* (verb conjugation) data
- pl_count_* (count word) data
- pl_adj_* (adjective) data
- pl_sb_postfix_adj* (postfix adjective) data
- Pre-compiled regex patterns that reference this data
"""

from __future__ import annotations

import re

from .._shared import bysize, enclose, joinstem, make_pl_si_lists


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


# VERB CONJUGATION DATA

plverb_special_s = enclose(
    "|".join(
        [pl_sb_singular_s]
        + pl_sb_uninflected_s
        + list(pl_sb_irregular_s)
        + ["(.*[csx])is", "(.*)ceps", "[A-Z].*s"]
    )
)

# Postfix adjective definitions
_pl_sb_postfix_adj_defn = (
    ("general", enclose(r"(?!major|lieutenant|brigadier|adjutant|.*star)\S+")),
    ("martial", enclose("court")),
    ("force", enclose("pound")),
)

from typing import Iterable as _Iterable

pl_sb_postfix_adj: _Iterable[str] = (
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


# These dictionaries group verbs by first, second and third person
# conjugations.

plverb_irregular_pres = {
    "am": "are",
    "are": "are",
    "is": "are",
    "was": "were",
    "were": "were",
    "have": "have",
    "has": "have",
    "do": "do",
    "does": "do",
}

plverb_ambiguous_pres = {
    "act": "act",
    "acts": "act",
    "blame": "blame",
    "blames": "blame",
    "can": "can",
    "must": "must",
    "fly": "fly",
    "flies": "fly",
    "copy": "copy",
    "copies": "copy",
    "drink": "drink",
    "drinks": "drink",
    "fight": "fight",
    "fights": "fight",
    "fire": "fire",
    "fires": "fire",
    "like": "like",
    "likes": "like",
    "look": "look",
    "looks": "look",
    "make": "make",
    "makes": "make",
    "reach": "reach",
    "reaches": "reach",
    "run": "run",
    "runs": "run",
    "sink": "sink",
    "sinks": "sink",
    "sleep": "sleep",
    "sleeps": "sleep",
    "view": "view",
    "views": "view",
}

plverb_ambiguous_pres_keys = re.compile(
    rf"^({enclose('|'.join(plverb_ambiguous_pres))})((\s.*)?)$", re.IGNORECASE
)


plverb_irregular_non_pres = (
    "did",
    "had",
    "ate",
    "made",
    "put",
    "spent",
    "fought",
    "sank",
    "gave",
    "sought",
    "shall",
    "could",
    "ought",
    "should",
)

plverb_ambiguous_non_pres = re.compile(
    r"^((?:thought|saw|bent|will|might|cut))((\s.*)?)$", re.IGNORECASE
)

# "..oes" -> "..oe" (the rest are "..oes" -> "o")

pl_v_oes_oe = ("canoes", "floes", "oboes", "roes", "throes", "woes")
pl_v_oes_oe_endings_size4 = ("hoes", "toes")
pl_v_oes_oe_endings_size5 = ("shoes",)


# COUNT WORDS

pl_count_zero = ("0", "no", "zero", "nil")

pl_count_one = ("1", "a", "an", "one", "each", "every", "this", "that")

# ADJECTIVE DATA

pl_adj_special = {"a": "some", "an": "some", "this": "these", "that": "those"}

pl_adj_special_keys = re.compile(
    rf"^({enclose('|'.join(pl_adj_special))})$", re.IGNORECASE
)

pl_adj_poss = {
    "my": "our",
    "your": "your",
    "its": "their",
    "her": "their",
    "his": "their",
    "their": "their",
}

pl_adj_poss_keys = re.compile(rf"^({enclose('|'.join(pl_adj_poss))})$", re.IGNORECASE)


# ── Pre-compiled regex patterns derived from this data ──────────────

PL_SB_POSTFIX_ADJ_STEMS_RE = re.compile(
    rf"^(?:{pl_sb_postfix_adj_stems})$", re.IGNORECASE
)

PLVERB_SPECIAL_S_RE = re.compile(rf"^({plverb_special_s})$")
