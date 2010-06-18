'''
    inflect.py: correctly generate plurals, ordinals, indefinite articles;
                convert numbers to words
    Copyright (C) 2010 Paul Dyson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


methods:
          classical inflect
          PL PL_N PL_V PL_ADJ NO NUM A AN
          PL_eq PL_N_eq PL_V_eq PL_ADJ_eq
          PART_PRES
          ORD
          NUMWORDS
          WORDLIST
          def_noun def_verb def_adj def_a def_an

    INFLECTIONS:    classical inflect
          PL PL_N PL_V PL_ADJ PL_eq
          NO NUM A AN PART_PRES

    PLURALS:   classical inflect
          PL PL_N PL_V PL_ADJ NO NUM
          PL_eq PL_N_eq PL_V_eq PL_ADJ_eq

    COMPARISONS:    classical 
          PL_eq PL_N_eq PL_V_eq PL_ADJ_eq

    ARTICLES:   classical inflect NUM A AN 

    NUMERICAL:      ORD NUMWORDS

    USER_DEFINED:   def_noun def_verb def_adj def_a def_an

Exceptions:
 UnknownClassicalModeError
 BadNumValueError
 BadChunkingOptionError
 NumOutOfRangeError

'''

from re import match, search, compile, subn, IGNORECASE, VERBOSE
from re import split as splitre
from re import error as reerror
from re import sub as resub
from os.path import dirname, isfile, expanduser
from os.path import join as pathjoin

class UnknownClassicalModeError(Exception): pass
class BadNumValueError(Exception): pass
class BadChunkingOptionError(Exception): pass
class NumOutOfRangeError(Exception): pass

STDOUT_ON = True

def print3(txt):
    if STDOUT_ON:
        print(txt)

def enclose(s):
    return "(?:%s)" % s

def joinstem(cutpoint=0, words=''):
    '''
    join stem of each word in words into a string for regex
    each word is truncated at cutpoint
    cutpoint is usually negative indicating the number of letters to remove
    from the end of each word

    e.g.
    joinstem(-2, ["ephemeris", "iris", ".*itis"]) returns
    (?:ephemer|ir|.*it
 
    '''
    return enclose('|'.join(w[:cutpoint] for w in words))

# 1. PLURALS

PL_sb_irregular_s = {
    "corpus"    : "corpuses|corpora",
    "opus"      : "opuses|opera",
    "genus"     : "genera",
    "mythos"    : "mythoi",
    "penis"     : "penises|penes",
    "testis"    : "testes",
    "atlas"     : "atlases|atlantes",
    "yes"       : "yeses",
}

PL_sb_irregular = {
    "child"       : "children",
    "brother"     : "brothers|brethren",
    "loaf"        : "loaves",
    "hoof"        : "hoofs|hooves",
    "beef"        : "beefs|beeves",
    "thief"       : "thiefs|thieves",
    "money"       : "monies",
    "mongoose"    : "mongooses",
    "ox"          : "oxen",
    "cow"         : "cows|kine",
    "graffito"    : "graffiti",
    "prima donna" : "prima donnas|prime donne",
    "octopus"     : "octopuses|octopodes",
    "genie"       : "genies|genii",
    "ganglion"    : "ganglions|ganglia",
    "trilby"      : "trilbys",
    "turf"        : "turfs|turves",
    "numen"       : "numina",
    "atman"       : "atmas",
    "occiput"     : "occiputs|occipita",
    'sabretooth'  : 'sabretooths',
    'sabertooth'  : 'sabertooths',
    'lowlife'     : 'lowlifes',
    'flatfoot'    : 'flatfoots',
    'tenderfoot'  : 'tenderfoots',
    'Romany'      : 'Romanies',
    'romany'      : 'romanies',
    'Jerry'       : 'Jerrys',
    'jerry'       : 'jerries',
    'Mary'        : 'Marys',
    'mary'        : 'maries',
    'talouse'     : 'talouses',
    'blouse'      : 'blouses',
    'Rom'         : 'Roma',
    'rom'         : 'roma',
}

PL_sb_irregular.update(PL_sb_irregular_s)

PL_sb_irregular_keys = enclose('|'.join(PL_sb_irregular.keys()))

# CLASSICAL "..is" -> "..ides"

PL_sb_C_is_ides = [
# GENERAL WORDS...

    "ephemeris", "iris", "clitoris",
    "chrysalis", "epididymis",

# INFLAMATIONS...

    ".*itis", 

]

PL_sb_C_is_ides_stems = joinstem(-2, PL_sb_C_is_ides)

# CLASSICAL "..a" -> "..ata"

PL_sb_C_a_ata = (
    "anathema", "bema", "carcinoma", "charisma", "diploma",
    "dogma", "drama", "edema", "enema", "enigma", "lemma",
    "lymphoma", "magma", "melisma", "miasma", "oedema",
    "sarcoma", "schema", "soma", "stigma", "stoma", "trauma",
    "gumma", "pragma",
)

PL_sb_C_a_ata_stems = joinstem(-1, PL_sb_C_a_ata)

# UNCONDITIONAL "..a" -> "..ae"

PL_sb_U_a_ae = enclose('|'.join ((
    "alumna", "alga", "vertebra", "persona"
)))

# CLASSICAL "..a" -> "..ae"

PL_sb_C_a_ae = enclose('|'.join ((
    "amoeba", "antenna", "formula", "hyperbola",
    "medusa", "nebula", "parabola", "abscissa",
    "hydra", "nova", "lacuna", "aurora", ".*umbra",
    "flora", "fauna",
)))

# CLASSICAL "..en" -> "..ina"

PL_sb_C_en_ina = joinstem(-2, ((
    "stamen", "foramen", "lumen", "carmen"
)))

# UNCONDITIONAL "..um" -> "..a"

PL_sb_U_um_a = joinstem(-2, ((
    "bacterium",    "agendum",  "desideratum",  "erratum",
    "stratum",  "datum",    "ovum",     "extremum",
    "candelabrum",
)))

# CLASSICAL "..um" -> "..a"

PL_sb_C_um_a = joinstem(-2, ((
    "maximum",  "minimum",    "momentum",   "optimum",
    "quantum",  "cranium",    "curriculum", "dictum",
    "phylum",   "aquarium",   "compendium", "emporium",
    "enconium", "gymnasium",  "honorarium", "interregnum",
    "lustrum",  "memorandum", "millennium", "rostrum", 
    "spectrum", "speculum",   "stadium",    "trapezium",
    "ultimatum",    "medium",   "vacuum",   "velum", 
    "consortium",
)))

# UNCONDITIONAL "..us" -> "i"

PL_sb_U_us_i = joinstem(-2, ((
    "alumnus",  "alveolus", "bacillus", "bronchus",
    "locus",    "nucleus",  "stimulus", "meniscus",
    "sarcophagus",
)))

# CLASSICAL "..us" -> "..i"

PL_sb_C_us_i = joinstem(-2, ((
    "focus",    "radius",   "genius",
    "incubus",  "succubus", "nimbus",
    "fungus",   "nucleolus",    "stylus",
    "torus",    "umbilicus",    "uterus",
    "hippopotamus", "cactus",
)))

# CLASSICAL "..us" -> "..us"  (ASSIMILATED 4TH DECLENSION LATIN NOUNS)

PL_sb_C_us_us = enclose('|'.join ((
    "status", "apparatus", "prospectus", "sinus",
    "hiatus", "impetus", "plexus",
)))

# UNCONDITIONAL "..on" -> "a"

PL_sb_U_on_a = joinstem(-2, ((
    "criterion",    "perihelion",   "aphelion",
    "phenomenon",   "prolegomenon", "noumenon",
    "organon",  "asyndeton",    "hyperbaton",
)))

# CLASSICAL "..on" -> "..a"

PL_sb_C_on_a = joinstem(-2, ((
    "oxymoron",
)))

# CLASSICAL "..o" -> "..i"  (BUT NORMALLY -> "..os")

PL_sb_C_o_i = [
    "solo",     "soprano",  "basso",    "alto",
    "contralto",    "tempo",    "piano",    "virtuoso",
] # list not tuple so can concat for PL_sb_U_o_os

PL_sb_C_o_i_stems = joinstem(-1, PL_sb_C_o_i)

# ALWAYS "..o" -> "..os"

PL_sb_U_o_os = enclose('|'.join ([
    "^ado",          "aficionado",   "aggro",
    "albino",       "allegro",      "ammo",
    "Antananarivo", "archipelago",  "armadillo",
    "auto",         "avocado",      "Bamako",
    "Barquisimeto", "bimbo",        "bingo",
    "Biro",         "bolero",       "Bolzano",
    "bongo",        "Boto",         "burro",
    "Cairo",        "canto",        "cappuccino",
    "casino",       "cello",        "Chicago",
    "Chimango",     "cilantro",     "cochito",
    "coco",         "Colombo",      "Colorado",     
    "commando",     "concertino",   "contango",
    "credo",        "crescendo",    "cyano",
    "demo",         "ditto",        "Draco",
    "dynamo",       "embryo",       "Esperanto",
    "espresso",     "euro",         "falsetto",
    "Faro",         "fiasco",       "Filipino",
    "flamenco",     "furioso",      "generalissimo",
    "Gestapo",      "ghetto",       "gigolo",
    "gizmo",        "Greensboro",   "gringo",
    "Guaiabero",    "guano",        "gumbo",
    "gyro",         "hairdo",       "hippo",
    "Idaho",        "impetigo",     "inferno",
    "info",         "intermezzo",   "intertrigo",
    "Iquico",       "^ISO",          "jumbo",
    "junto",        "Kakapo",       "kilo",
    "Kinkimavo",    "Kokako",       "Kosovo",
    "Lesotho",      "libero",       "libido",
    "libretto",     "lido",         "Lilo", 
    "limbo",        "limo",         "lineno",
    "lingo",        "lino",         "livedo",
    "loco",         "logo",         "lumbago",
    "macho",        "macro",        "mafioso",
    "magneto",      "magnifico",    "Majuro",
    "Malabo",       "manifesto",    "Maputo",
    "Maracaibo",    "medico",       "memo",
    "metro",        "Mexico",       "micro",
    "Milano",       "Monaco",       "mono", 
    "Montenegro",   "Morocco",      "Muqdisho",
    "myo",          "^NATO",         "^NCO",
    "neutrino",     "^NGO",          "Ningbo",
    "octavo",       "oregano",      "Orinoco",
    "Orlando",      "Oslo",         "^oto",
    "panto",        "Paramaribo",   "Pardusco",
    "pedalo",       "photo",        "pimento",
    "pinto",        "pleco",        "Pluto",
    "pogo",         "polo",         "poncho",
    "Porto-Novo",   "Porto",        "pro",
    "psycho",       "pueblo",       "quarto",
    "Quito",        "rhino",        "risotto",
    "rococo",       "rondo",        "Sacramento",
    "saddo",        "sago",         "salvo",
    "Santiago",     "Sapporo",      "Sarajevo",
    "scherzando",   "scherzo",      "silo",
    "sirocco",      "sombrero",     "staccato",
    "sterno",       "stucco",       "stylo",
    "sumo",         "Taiko",        "techno",
    "terrazzo",     "testudo",      "timpano",
    "tiro",         "tobacco",      "Togo",
    "Tokyo",        "torero",       "Torino",
    "Toronto",      "torso",        "tremolo",
    "typo",         "tyro",         "ufo",
    "UNESCO",       "vaquero",      "vermicello",
    "verso",        "vibrato",      "violoncello",
    "Virgo",        "weirdo",       "WHO",  
    "WTO",          "Yamoussoukro", "yo-yo",        
    "zero",         "Zibo",         
    ] + PL_sb_C_o_i
))


# UNCONDITIONAL "..ch" -> "..chs"

PL_sb_U_ch_chs = joinstem(-2, ((
    "czech",  "eunuch",   "stomach"
)))

# UNCONDITIONAL "..[ei]x" -> "..ices"

PL_sb_U_ex_ices = joinstem(-2, ((
    "codex",    "murex",    "silex",
)))

PL_sb_U_ix_ices = joinstem(-2, ((
    "radix",    "helix",
)))

# CLASSICAL "..[ei]x" -> "..ices"

PL_sb_C_ex_ices = joinstem(-2, ((
    "vortex",   "vertex",   "cortex",   "latex",
    "pontifex", "apex",     "index",    "simplex",
)))

PL_sb_C_ix_ices = joinstem(-2, ((
    "appendix",
)))

# ARABIC: ".." -> "..i"

PL_sb_C_i = enclose('|'.join ((
    "afrit",    "afreet",   "efreet",
)))

# HEBREW: ".." -> "..im"

PL_sb_C_im = enclose('|'.join ((
    "goy",      "seraph",   "cherub",
)))

# UNCONDITIONAL "..man" -> "..mans"

PL_sb_U_man_mans = enclose('|'.join (
"""
    ataman caiman cayman ceriman
    desman dolman farman harman hetman
    human leman ottoman shaman talisman
    Alabaman Bahaman Burman German
    Hiroshiman Liman Nakayaman Norman Oklahoman 
    Panaman Roman Selman Sonaman Tacoman Yakiman
    Yokohaman Yuman
""".split()
))

PL_sb_uninflected_s = [
# PAIRS OR GROUPS SUBSUMED TO A SINGULAR...
    "breeches", "britches", "pajamas", "pyjamas", "clippers", "gallows",
    "hijinks", "headquarters", "pliers", "scissors", "testes", "herpes",
    "pincers", "shears", "proceedings", "trousers",

# UNASSIMILATED LATIN 4th DECLENSION

    "cantus", "coitus", "nexus",

# RECENT IMPORTS...
    "contretemps", "corps", "debris",
    ".*ois", "siemens",
    
# DISEASES
    ".*measles", "mumps",

# MISCELLANEOUS OTHERS...
    "diabetes", "jackanapes", "series", "species", "rabies",
    "chassis", "innings", "news", "mews", "haggis",
]

PL_sb_uninflected_herd = enclose('|'.join((
# DON'T INFLECT IN CLASSICAL MODE, OTHERWISE NORMAL INFLECTION
    "wildebeest", "swine", "eland", "bison", "buffalo",
    "elk", "rhinoceros", 'zucchini',
    'caribou', 'dace', 'grouse', 'guinea[- ]fowl',
    'haddock', 'hake', 'halibut', 'herring', 'mackerel',
    'pickerel', 'pike', 'roe', 'seed', 'shad',
    'snipe', 'teal', 'turbot', 'water[- ]fowl',
)))

PL_sb_uninflected = enclose('|'.join ([
# SOME FISH AND HERD ANIMALS
    ".*fish", "tuna", "salmon", "mackerel", "trout",
    "bream", "sea[- ]bass", "carp", "cod", "flounder", "whiting", 

    ".*deer", ".*sheep", "moose",

# ALL NATIONALS ENDING IN -ese
    "Portuguese", "Amoyese", "Borghese", "Congoese", "Faroese",
    "Foochowese", "Genevese", "Genoese", "Gilbertese", "Hottentotese",
    "Kiplingese", "Kongoese", "Lucchese", "Maltese", "Nankingese",
    "Niasese", "Pekingese", "Piedmontese", "Pistoiese", "Sarawakese",
    "Shavese", "Vermontese", "Wenchowese", "Yengeese",
    ".*[nrlm]ese",

# DISEASES
    ".*pox",


# OTHER ODDITIES
    "graffiti", "djinn", 'samuri',
    '.*craft$', 'offspring', 'pence', 'quid', 'hertz',
   ] + 

# SOME WORDS ENDING IN ...s (OFTEN PAIRS TAKEN AS A WHOLE)

    PL_sb_uninflected_s

))

# SINGULAR WORDS ENDING IN ...s (ALL INFLECT WITH ...es)

PL_sb_singular_s = enclose('|'.join ([
    ".*ss",
    "acropolis", "aegis", "alias", "asbestos", "bathos", "bias",
    "bronchitis", "bursitis", "caddis", "cannabis",
    "canvas", "chaos", "cosmos", "dais", "digitalis",
    "epidermis", "ethos", "eyas", "gas", "glottis", 
    "hubris", "ibis", "lens", "mantis", "marquis", "metropolis",
    "pathos", "pelvis", "polis", "rhinoceros",
    "sassafras", "trellis", ".*us", "[A-Z].*es",
   ] + PL_sb_C_is_ides
))


PL_v_special_s = enclose('|'.join (
    [PL_sb_singular_s] +
    PL_sb_uninflected_s +
    PL_sb_irregular_s.keys() + [
    '(.*[csx])is',
    '(.*)ceps',
    '[A-Z].*s',
]))

PL_sb_postfix_adj = {
    'general' : ['(?!major|lieutenant|brigadier|adjutant)\S+'],
    'martial' : "court".split(),
}

for k in PL_sb_postfix_adj.keys():
    PL_sb_postfix_adj[k] = enclose(
                   enclose('|'.join(PL_sb_postfix_adj[k]))
                   + "(?=(?:-|\\s+)%s)" % k)

PL_sb_postfix_adj_stems = '(' + '|'.join(PL_sb_postfix_adj.values()) + ')(.*)'

#TODO: file upstream bug: next two are never used. Should comment out.
PL_sb_military = 'major|lieutenant|brigadier|adjutant|quartermaster'
PL_sb_general = '((?!'+PL_sb_military+r').*?)((-|\s+)general)'

PL_prep = enclose('|'.join( """
    about above across after among around at athwart before behind
    below beneath beside besides between betwixt beyond but by
    during except for from in into near of off on onto out over
    since till to under until unto upon with""".split()
))

PL_sb_prep_dual_compound = r'(.*?)((?:-|\s+)(?:'+PL_prep+r'|d[eua])(?:-|\s+))a(?:-|\s+)(.*)'


PL_sb_prep_compound = r'(.*?)((-|\s+)('+PL_prep+r'|d[eua])((-|\s+)(.*))?)'


PL_pron_nom = {
#   NOMINATIVE      REFLEXIVE

"i" : "we",    "myself"   :   "ourselves",
"you"   : "you",   "yourself" :   "yourselves",
"she"   : "they",  "herself"  :   "themselves",
"he"    : "they",  "himself"  :   "themselves",
"it"    : "they",  "itself"   :   "themselves",
"they"  : "they",  "themself" :   "themselves",

#   POSSESSIVE

"mine"   : "ours",
"yours"  : "yours",
"hers"   : "theirs",
"his"    : "theirs",
"its"    : "theirs",
"theirs" : "theirs",
}

PL_pron_acc = {
#   ACCUSATIVE      REFLEXIVE

"me"    : "us",    "myself"   :   "ourselves",
"you"   : "you",   "yourself" :   "yourselves",
"her"   : "them",  "herself"  :   "themselves",
"him"   : "them",  "himself"  :   "themselves",
"it"    : "them",  "itself"   :   "themselves",
"them"  : "them",  "themself" :   "themselves",
}

PL_pron_acc_keys = enclose('|'.join(PL_pron_acc.keys()))

PL_v_irregular_pres = {
#   1st PERS. SING.     2ND PERS. SING.     3RD PERS. SINGULAR
#               3RD PERS. (INDET.)  

"am"    : "are",   "are"   : "are",   "is"     : "are",
"was"   : "were",  "were"  : "were",  "was"    : "were",
"have"  : "have",  "have"  : "have",  "has"    : "have",
"do"    : "do",    "do"    : "do",    "does"   : "do",
}

PL_v_irregular_pres_keys = enclose('|'.join(PL_v_irregular_pres.keys()))

PL_v_ambiguous_pres = {
#   1st PERS. SING.     2ND PERS. SING.     3RD PERS. SINGULAR
#               3RD PERS. (INDET.)  

"act"   : "act",   "act"   : "act",   "acts"    : "act",
"blame" : "blame", "blame" : "blame", "blames"  : "blame",
"can"   : "can",   "can"   : "can",   "can"     : "can",
"must"  : "must",  "must"  : "must",  "must"    : "must",
"fly"   : "fly",   "fly"   : "fly",   "flies"   : "fly",
"copy"  : "copy",  "copy"  : "copy",  "copies"  : "copy",
"drink" : "drink", "drink" : "drink", "drinks"  : "drink",
"fight" : "fight", "fight" : "fight", "fights"  : "fight",
"fire"  : "fire",  "fire"  : "fire",  "fires"   : "fire",
"like"  : "like",  "like"  : "like",  "likes"   : "like",
"look"  : "look",  "look"  : "look",  "looks"   : "look",
"make"  : "make",  "make"  : "make",  "makes"   : "make",
"reach" : "reach", "reach" : "reach", "reaches" : "reach",
"run"   : "run",   "run"   : "run",   "runs"    : "run",
"sink"  : "sink",  "sink"  : "sink",  "sinks"   : "sink",
"sleep" : "sleep", "sleep" : "sleep", "sleeps"  : "sleep",
"view"  : "view",  "view"  : "view",  "views"   : "view",
}

PL_v_ambiguous_pres_keys = enclose('|'.join(PL_v_ambiguous_pres.keys()));


PL_v_irregular_non_pres = enclose('|'.join ((
"did", "had", "ate", "made", "put", 
"spent", "fought", "sank", "gave", "sought",
"shall", "could", "ought", "should",
)))

PL_v_ambiguous_non_pres = enclose('|'.join ((
"thought", "saw", "bent", "will", "might", "cut",
)))

# "..oes" -> "..oe" (the rest are "..oes" -> "o")

PL_v_oes_oe = enclose('|'.join ( """
    .*shoes  .*hoes  .*toes
    canoes   floes   oboes  roes  throes  woes
    """.split()
))

PL_count_zero = (
"0", "no", "zero", "nil"
)


PL_count_one = (
"1", "a", "an", "one", "each", "every", "this", "that",
)

PL_adj_special = {
"a"    : "some",   "an"   :  "some",
"this" : "these",  "that" : "those",
}

PL_adj_special_keys = enclose('|'.join(PL_adj_special.keys()))

PL_adj_poss = {
"my"    : "our",
"your"  : "your",
"its"   : "their",
"her"   : "their",
"his"   : "their",
"their" : "their",
}

PL_adj_poss_keys = enclose('|'.join(PL_adj_poss.keys()))


# 2. INDEFINITE ARTICLES

# THIS PATTERN MATCHES STRINGS OF CAPITALS STARTING WITH A "VOWEL-SOUND"
# CONSONANT FOLLOWED BY ANOTHER CONSONANT, AND WHICH ARE NOT LIKELY
# TO BE REAL WORDS (OH, ALL RIGHT THEN, IT'S JUST MAGIC!)

A_abbrev = r"""
(?! FJO | [HLMNS]Y.  | RY[EO] | SQU
  | ( F[LR]? | [HL] | MN? | N | RH? | S[CHKLMNPTVW]? | X(YL)?) [AEIOU])
[FHLMNRSX][A-Z]
"""

# THIS PATTERN CODES THE BEGINNINGS OF ALL ENGLISH WORDS BEGINING WITH A
# 'y' FOLLOWED BY A CONSONANT. ANY OTHER Y-CONSONANT PREFIX THEREFORE
# IMPLIES AN ABBREVIATION.

A_y_cons = 'y(b[lor]|cl[ea]|fere|gg|p[ios]|rou|tt)'

# EXCEPTIONS TO EXCEPTIONS

A_explicit_an = enclose('|'.join((
    "euler",
    "hour(?!i)", "heir", "honest", "hono",
    "[fhlmnx]-?th",
    )))


# NUMERICAL INFLECTIONS

nth = {
     0: 'th',
     1: 'st',
     2: 'nd',
     3: 'rd',
     4: 'th',
     5: 'th',
     6: 'th',
     7: 'th',
     8: 'th',
     9: 'th',
     11: 'th',
     12: 'th',
     13: 'th',
}

ordinal = dict(ty='tieth',
               one='first',
               two='second',
               three='third',
               five='fifth',
               eight='eighth',
               nine='ninth',
               twelve='twelfth',
              )

ordinal_suff = '|'.join(ordinal.keys())



# NUMBERS

default_args = {
    'group'   : 0,
    'comma'   : ',',
    'andword'   : 'and',
    'zero'    : 'zero',
    'one'     : 'one',
    'decimal' : 'point',
}


unit = ['', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine']
teen = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
        'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
ten  = ['','','twenty', 'thirty', 'forty',
        'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
mill = ['', ' thousand', ' million', ' billion', ' trillion', ' quadrillion',
        'quintillion', ' sextillion', ' septillion', ' octillion',
        ' nonillion', ' decillion']



# SUPPORT CLASSICAL PLURALIZATIONS

def_classical = dict(
    all      = 0,
    zero     = 0,
    herd     = 0,
    names    = 1,
    persons  = 0,
    ancient  = 0,
)

all_classical = dict((k,1) for k in def_classical.keys())
no_classical = dict((k,0) for k in def_classical.keys())


for rcfile in (pathjoin(dirname(__file__), '.inflectrc'),
               expanduser(pathjoin(('~'), '.inflectrc'))):
    if isfile(rcfile):
        try:
            execfile(rcfile)
        except:
            print3("\nBad .inflectrc file (%s):\n" % rcfile)
            raise



class engine:

    def __init__(self):

        self.classical_dict = def_classical.copy()
        self.persistent_count = None
        self.number_args = default_args.copy() # user can overwrite these in NUM
        self.mill_count = 0
        self.PL_sb_user_defined = []
        self.PL_v_user_defined  = []
        self.PL_adj_user_defined  = []
        self.A_a_user_defined   = []

    #TODO checkpat is not the correct routine for checking the plural (i.e. replace) strings
    def def_noun(self, singular, plural):
        self.checkpat(singular)
        #checkpat(plural)
        self.PL_sb_user_defined.extend((singular, plural))
        return 1

    # TODO does the eg in the docs work? will goes to both shall and will?
    # will it work for the test of what is the plurl of what

    def def_verb(self, s1, p1, s2, p2, s3, p3):
        self.checkpat(s1)
        self.checkpat(s2)
        self.checkpat(s3)
        #checkpat(p1)
        #checkpat(p2)
        #checkpat(p3)
        self.PL_v_user_defined.extend((s1, p1, s2, p2, s3, p3))
        return 1

    def def_adj(self, singular, plural):
        self.checkpat(singular)
        #checkpat(plural)
        self.PL_adj_user_defined.extend((singular, plural))
        return 1

    # BUG in perl code line 1270: if set a or an in .inflectrc it returns
    # 'a' or 'an'
    # instead of 'a word' or 'an word'
    # fixed in my version of inflect.pm

    def def_a(self, pattern):
        self.checkpat(pattern)
        self.A_a_user_defined.extend((pattern, 'a'))
        return 1

    def def_an(self, pattern):
        self.checkpat(pattern)
        self.A_a_user_defined.extend((pattern, 'an'))
        return 1

    def checkpat(self, pattern):
        '''
        check for errors in a regex pattern
        '''
        if pattern is None:
            return
        try:
            match(pattern, '')
        except reerror:
            print3("\nBad user-defined singular pattern:\n\t%s\n" % pattern)
            raise
       
    def ud_match(self, word, wordlist):
        for i in range(len(wordlist)-2, -2, -2): # backwards through even elements
            mo = search(r'^%s$' % wordlist[i], word, IGNORECASE)
            if mo:
                if wordlist[i+1] is None:
                    return None
                pl = resub(r'\$(\d+)',r'\\1',wordlist[i+1]) # change $n to \n for expand
                return mo.expand(pl)
        return None



    def classical(self, *args, **kwargs):
        """
        Set the classical mode by changing classical_dict

        no args: all_classical
        single args: all_classical if arg else no_classical
        if 'all' in args or all=<true value> then all_classical
        if all=<false value> then no_classical
        else set each that appears in args as long as it is a valid key
        and set each according to kwargs as long as a valid key

        unknown value in args or key in kwargs rasies exception: UnknownClasicalModeError

        """
        classical_mode = def_classical.keys()
        if not args and not kwargs:
            self.classical_dict = all_classical.copy()
            return
        if (not kwargs) and len(args) == 1 and args[0] not in classical_mode:
            self.classical_dict = all_classical.copy() if args[0] else no_classical.copy()
            return
        for arg in args:
            if arg in classical_mode:
                self.classical_dict[arg] = 1
            else:
                raise UnknownClassicalModeError
        for k, v in kwargs.items():
            if k in classical_mode:
                self.classical_dict[k] = v
        if 'all' in args or 'all' in kwargs:
            self.classical_dict = all_classical.copy() if self.classical_dict['all'] else no_classical.copy()


    def NUM(self, count=None, show=None):     # (;$count,$show)
        if count is not None:
            try:
                self.persistent_count = int(count)
            except ValueError:
                raise BadNumValueError
            if (show is None) or show:
                return str(count)
        else:
            self.persistent_count = None;
        return ''

    def NUMmo(self, matchobject):
        '''
        NUM but take a matchobject
        use groups 1 and 2 in matchobject
        '''
        return self.NUM(matchobject.group(1), matchobject.group(2))

    def PLmo(self, matchobject):
        '''
        PL but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.PL(matchobject.group(1), matchobject.group(3))

    def PL_Nmo(self, matchobject):
        '''
        PL_N but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.PL_N(matchobject.group(1), matchobject.group(3))

    def PL_Vmo(self, matchobject):
        '''
        PL_V but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.PL_V(matchobject.group(1), matchobject.group(3))

    def PL_ADJmo(self, matchobject):
        '''
        PL_ADJ but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.PL_ADJ(matchobject.group(1), matchobject.group(3))

    def Amo(self, matchobject):
        '''
        A but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.A(matchobject.group(1), matchobject.group(3))

    def NOmo(self, matchobject):
        '''
        NO but take a matchobject
        use groups 1 and 3 in matchobject
        '''
        return self.A(matchobject.group(1), matchobject.group(3))

    def ORDmo(self, matchobject):
        '''
        ORD but take a matchobject
        use group 1
        '''
        return self.ORD(matchobject.group(1))

    def NUMWORDSmo(self, matchobject):
        '''
        NUMWORDS but take a matchobject
        use group 1
        '''
        return self.NUMWORDS(matchobject.group(1))

    def PART_PRESmo(self, matchobject):
        '''
        PART_PRES but take a matchobject
        use group 1
        '''
        return self.PART_PRES(matchobject.group(1))


# 0. PERFORM GENERAL INFLECTIONS IN A STRING

    def inflect(self, text):

        save_persistent_count = self.persistent_count
        sections = splitre(r"(NUM\([^)]*\))", text)
        inflection = []

        for section in sections:
            (section, count) = subn(r"NUM\(\s*?(?:([^),]*)(?:,([^)]*))?)?\)", self.NUMmo, section)
            if not count:
                total = -1
                while total:
                    (section, total) = subn(
                        r"(?x)\bPL     \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.PLmo, section)
                    (section, count) = subn(
                        r"(?x)\bPL_N   \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.PL_Nmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bPL_V   \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.PL_Vmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bPL_ADJ \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.PL_ADJmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bAN?    \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.Amo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bNO    \( ([^),]*) (, ([^)]*) )? \)  ",
                        self.NOmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bORD        \( ([^)]*) \)            ",
                        self.ORDmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bNUMWORDS  \( ([^)]*) \)            ",
                        self.NUMWORDSmo, section)
                    total += count
                    (section, count) = subn(
                        r"(?x)\bPART_PRES \( ([^)]*) \)            ",
                        self.PART_PRESmo, section)
                    total += count

            inflection.append(section)

        self.persistent_count = save_persistent_count
        return "".join(inflection)

### PLURAL SUBROUTINES

    def postprocess(self, orig, inflected):
        """
        FIX PEDANTRY AND CAPITALIZATION :-)
        """
        if '|' in inflected:
            inflected = inflected.split('|')[self.classical_dict['all']]
        if orig == "I": return inflected
        if orig == orig.upper(): return inflected.upper()
        if orig[0] == orig[0].upper(): return '%s%s' % (inflected[0].upper(),
                                                      inflected[1:])
        return inflected

    def partition_word(self, mystr):
        mo = search(r'\A(\s*)(.+?)(\s*)\Z', mystr)
        try:
            return mo.group(1), mo.group(2), mo.group(3)
        except AttributeError: # empty string
            return '', '', ''

    def PL(self, mystr, count=None):
        pre, word, post = self.partition_word(mystr)
        if not word: return mystr
        plural = self.postprocess(word,
              self._PL_special_adjective(word, count)
              or self._PL_special_verb(word, count)
              or self._PL_noun(word, count))
        return "%s%s%s" % (pre, plural, post)

    def PL_N(self, mystr, count=None):
        pre, word, post = self.partition_word(mystr)
        if not word: return mystr
        plural = self.postprocess(word, self._PL_noun(word, count))
        return "%s%s%s" % (pre, plural, post)

    def PL_V(self, mystr, count=None):
        pre, word, post = self.partition_word(mystr)
        if not word: return mystr
        plural = self.postprocess(word, self._PL_special_verb(word, count)
              or self._PL_general_verb(word, count))
        return "%s%s%s" % (pre, plural, post)

    def PL_ADJ(self, mystr, count=None):
        pre, word, post = self.partition_word(mystr)
        if not word: return mystr
        plural = self.postprocess(word, self._PL_special_adjective(word, count)
              or word)
        return "%s%s%s" % (pre, plural, post)

# TODO: BUG to report upstream.
# PL_eq returns reference to PL_ADJ function instead of false
# it does not copare two adjectives
# fixed below

    def PL_eq(self, word1, word2):
        return (
          self._PL_eq(word1, word2, self.PL_N) or
          self._PL_eq(word1, word2, self.PL_V) or
          self._PL_eq(word1, word2, self.PL_ADJ))

    def PL_N_eq(self, word1, word2):
          return self._PL_eq(word1, word2, self.PL_N)

    def PL_V_eq(self, word1, word2):
          return self._PL_eq(word1, word2, self.PL_V)

    def PL_ADJ_eq(self, word1, word2):
          return self._PL_eq(word1, word2, self.PL_ADJ)

    def _PL_eq(self, word1, word2, PL):
        classval = self.classical_dict.copy()
        self.classical_dict = all_classical.copy()
        if word1 == word2: return "eq"
        if word1 == PL(word2): return "p:s"
        if PL(word1) == word2: return "s:p"
        self.classical_dict = no_classical.copy()
        if word1 == PL(word2): return "p:s"
        if PL(word1) == word2: return "s:p"
        self.classical_dict = classval.copy()

        if PL == self.PL or PL == self.PL_N:
            if self._PL_check_plurals_N(word1, word2): return "p:p"
            if self._PL_check_plurals_N(word2, word1): return "p:p"
        if PL == self.PL or PL == self.PL_ADJ:
            if self._PL_check_plurals_ADJ(word1, word2): return "p:p"
        return False

    def _PL_reg_plurals(self, pair, stems, end1, end2):
#TODO delete commented try block
      #try:
        if search(r"(%s)(%s\|\1%s|%s\|\1%s)" %
                                 (stems, end1, end2, end2, end1),
                                         pair):
            return True
      #except:
        #print r"(%s)(%s\|\1%s|%s\|\1%s)" % (stems, end1, end2, end2, end1), pair

        #raise
        return False

    def _PL_check_plurals_N(self, word1, word2):
        pair = "%s|%s" % (word1, word2)
        if pair in PL_sb_irregular_s.values(): return True
        if pair in PL_sb_irregular.values(): return True

        for (stems, end1, end2) in (
                   (PL_sb_C_a_ata_stems,   "as","ata"),
                   (PL_sb_C_is_ides_stems, "is","ides"),
                   (PL_sb_C_a_ae,    "s","e"),
                   (PL_sb_C_en_ina,  "ens","ina"),
                   (PL_sb_C_um_a,    "ums","a"),
                   (PL_sb_C_us_i,    "uses","i"),
                   (PL_sb_C_on_a,    "ons","a"),
                   (PL_sb_C_o_i_stems,     "os","i"),
                   (PL_sb_C_ex_ices, "exes","ices"),
                   (PL_sb_C_ix_ices, "ixes","ices"),
                   (PL_sb_C_i,       "s","i"),
                   (PL_sb_C_im,      "s","im"),
                   ('.*eau',       "s","x"),
                   ('.*ieu',       "s","x"),
                   ('.*tri',       "xes","ces"),
                   ('.{2,}[yia]n', "xes","ges"),
                                    ):
            if self._PL_reg_plurals(pair, stems, end1, end2):
                return True
        return False

    def _PL_check_plurals_ADJ(self, word1, word2):
#VERSION: tuple in endswith requires python 2.5
#TODO PL_ADJ_eq shouldn't return true from dogmata' . Check that it doesn't
        word1a = word1[:word1.rfind("'")] if word1.endswith(("'s","'")) else ''
        word2a = word2[:word2.rfind("'")] if word2.endswith(("'s","'")) else ''
        word1b = word1[:-2] if word1.endswith("s'") else ''
        word2b = word2[:-2] if word2.endswith("s'") else ''

        if word1a:
            if word2a and ( self._PL_check_plurals_N(word1a, word2a)
                            or self._PL_check_plurals_N(word2a, word1a) ):
                return True
            if word2b and ( self._PL_check_plurals_N(word1a, word2b)
                            or self._PL_check_plurals_N(word2b, word1a) ):
                return True

        if word1b:
            if word2a and ( self._PL_check_plurals_N(word1b, word2a)
                            or self._PL_check_plurals_N(word2a, word1b) ):
                return True
            if word2b and ( self._PL_check_plurals_N(word1b, word2b)
                            or self._PL_check_plurals_N(word2b, word1b) ):
                return True

        return False

    def get_count(self, count=None):
        if count is None and self.persistent_count is not None:
            count = self.persistent_count

        if count is not None:
            count = 1 if ((str(count) in PL_count_one) or
              (self.classical_dict['zero'] and
                                str(count).lower() in PL_count_zero)) else 2
        else:
            count = ''
        return count

    def _PL_noun(self, word, count=None):
        count = self.get_count(count)

# DEFAULT TO PLURAL

        if count==1: return word

# HANDLE USER-DEFINED NOUNS

        value = self.ud_match(word, self.PL_sb_user_defined)
        if value is not None: return value


# HANDLE EMPTY WORD, SINGULAR COUNT AND UNINFLECTED PLURALS

        if word == '': return word

        if search(r"^%s$" % PL_sb_uninflected, word, IGNORECASE): return word

        if (self.classical_dict['herd'] and
               search(r"^%s$" % PL_sb_uninflected_herd, word, IGNORECASE)):
            return word

# HANDLE COMPOUNDS ("Governor General", "mother-in-law", "aide-de-camp", ETC.)

        mo = search(r"^(?:%s)$" % PL_sb_postfix_adj_stems, word, IGNORECASE)
        if mo and mo.group(2) != '':
            return "%s%s" % (self._PL_noun(mo.group(1), 2), mo.group(2))

        mo = search(r"^(?:%s)$" % PL_sb_prep_dual_compound, word, IGNORECASE)
        if mo and mo.group(2) != '' and mo.group(3) != '':
            return "%s%s%s" % (self._PL_noun(mo.group(1), 2),
                               mo.group(2),
                               self._PL_noun(mo.group(3)))

        mo = search(r"^(?:%s)$" % PL_sb_prep_compound, word, IGNORECASE)
        if mo and mo.group(2) != '':
                return "%s%s" % (self._PL_noun(mo.group(1), 2), mo.group(2))

# HANDLE PRONOUNS
# BUG does not keep case: "about ME" -> "about us". bug not fixed here
        mo = search(r"^((?:%s)\s+)(%s)$" % (PL_prep, PL_pron_acc_keys), word,
                                                         IGNORECASE)
        if mo: return "%s%s" % (mo.group(1), PL_pron_acc[mo.group(2).lower()])
     
        try:
            return PL_pron_nom[word.lower()]
        except KeyError: pass

        try:
            return PL_pron_acc[word.lower()]
        except KeyError: pass

# HANDLE ISOLATED IRREGULAR PLURALS 

        mo = search(r"(.*)\b(%s)$" % PL_sb_irregular_keys, word, IGNORECASE)
        if mo: return "%s%s" % (mo.group(1),
                                PL_sb_irregular.get(mo.group(2),
                                    PL_sb_irregular[mo.group(2).lower()]))

        mo = search(r"(%s)$" % PL_sb_U_man_mans, word, IGNORECASE)
        if mo: return "%ss" % mo.group(1)

        mo = search(r"(\S*)quy$", word, IGNORECASE)
        if mo: return "%squies" % mo.group(1)

        mo = search(r"(\S*)(person)$", word, IGNORECASE)
        if mo:
             if self.classical_dict['persons']:
                 return "%spersons" % mo.group(1)
             else:
                 return "%speople" % mo.group(1)

# HANDLE FAMILIES OF IRREGULAR PLURALS 

        for a in (
                  (r"(.*)man$", "%smen"),
                  (r"(.*[ml])ouse$", "%sice"),
                  (r"(.*)goose$", "%sgeese"),
                  (r"(.*)tooth$", "%steeth"),
                  (r"(.*)foot$", "%sfeet"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return a[1] % mo.group(1)


# HANDLE UNASSIMILATED IMPORTS

        if search(r"(.*)ceps$", word, IGNORECASE): return word


        for a in (
                  (r"(.*)zoon$", "%szoa"),
                  (r"(.*[csx])is$", "%ses"),
                  (r"(%s)ch$" % PL_sb_U_ch_chs, "%schs"),
                  (r"(%s)ex$" % PL_sb_U_ex_ices, "%sices"),
                  (r"(%s)ix$" % PL_sb_U_ix_ices, "%sices"),
                  (r"(%s)um$" % PL_sb_U_um_a, "%sa"),
                  (r"(%s)us$" % PL_sb_U_us_i, "%si"),
                  (r"(%s)on$" % PL_sb_U_on_a, "%sa"),
                  (r"(%s)$" % PL_sb_U_a_ae, "%se"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return a[1] % mo.group(1)


# HANDLE INCOMPLETELY ASSIMILATED IMPORTS

        if (self.classical_dict['ancient']):

            for a in (
                  (r"(.*)trix$", "%strices"),
                  (r"(.*)eau$", "%seaux"),
                  (r"(.*)ieu$", "%sieux"),
                  (r"(.{2,}[yia])nx$", "%snges"),
                  (r"(%s)en$" % PL_sb_C_en_ina, "%sina"),
                  (r"(%s)ex$" % PL_sb_C_ex_ices, "%sices"),
                  (r"(%s)ix$" % PL_sb_C_ix_ices, "%sices"),
                  (r"(%s)um$" % PL_sb_C_um_a, "%sa"),
                  (r"(%s)us$" % PL_sb_C_us_i, "%si"),
                  (r"(%s)$" % PL_sb_C_us_us, "%s"),
                  (r"(%s)$" % PL_sb_C_a_ae, "%se"),
                  (r"(%s)a$" % PL_sb_C_a_ata_stems, "%sata"),
                  (r"(%s)is$" % PL_sb_C_is_ides_stems, "%sides"),
                  (r"(%s)o$" % PL_sb_C_o_i_stems, "%si"),
                  (r"(%s)on$" % PL_sb_C_on_a, "%sa"),
                  (r"(%s)$" % PL_sb_C_im, "%sim"),
                  (r"(%s)$" % PL_sb_C_i, "%si"),
                 ):
                mo = search(a[0], word, IGNORECASE)
                if mo: return a[1] % mo.group(1)


# HANDLE SINGULAR NOUNS ENDING IN ...s OR OTHER SILIBANTS
        mo = search(r"(%s)$" % PL_sb_singular_s, word, IGNORECASE)
        if mo: return "%ses" % mo.group(1)

# TODO: not sure if this makes a difference. Wouldn't special words
# ending with 's' always have been caught, regardless of them starting
# with a capitla letter (i.e. bieing names)
# It makes sense below to do this for words ending in 'y' so that
# Sally -> Sallys. But not sure it makes sense here. Where is the case
# of a word ending in s that is caught here and would otherwise have been
# caught below?
        if (self.classical_dict['names']):
            mo = search(r"([A-Z].*s)$", word)
            if mo: return "%ses" % mo.group(1)

        mo = search(r"^(.*[^z])(z)$", word, IGNORECASE)
        if mo: return "%szzes" % mo.group(1)

        for a in (
                  (r"^(.*)([cs]h|x|zz|ss)$",  "%s%ses"),
#                  (r"(.*)(us)$", "%s%ses"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return a[1] % (mo.group(1), mo.group(2))


# HANDLE ...f -> ...ves

        for a in (
                  (r"(.*[eao])lf$", "%slves"),
                  (r"(.*[^d])eaf$", "%seaves"),
                  (r"(.*[nlw])ife$", "%sives"),
                  (r"(.*)arf$", "%sarves"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return a[1] % mo.group(1)

# HANDLE ...y

        mo = search(r"(.*[aeiou])y$", word, IGNORECASE)
        if mo: return "%sys" % mo.group(1)

        if (self.classical_dict['names']):
            mo = search(r"([A-Z].*y)$", word)
            if mo: return "%ss" % mo.group(1)

        mo = search(r"(.*)y$", word, IGNORECASE)
        if mo: return "%sies" % mo.group(1)


# HANDLE ...o

        for a in (
                  (r"%s$" % PL_sb_U_o_os, "s"),
                  (r"[aeiou]o$", "s"),
                  (r"o$", "es"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return "%s%s" % (word, a[1])

# OTHERWISE JUST ADD ...s

        return "%ss" % word


    def _PL_special_verb(self, word, count=None):
        count = self.get_count(count)
# TODO: should zero make count 2 not return here: check Perl code
        if str(count).lower() in PL_count_zero: return False

        if count==1: return word

# HANDLE USER-DEFINED VERBS

        value = self.ud_match(word, self.PL_v_user_defined)
        if value is not None: return value

# HANDLE IRREGULAR PRESENT TENSE (SIMPLE AND COMPOUND)

        mo = search(r"^(%s)((\s.*)?)$" % PL_v_irregular_pres_keys,
                    word, IGNORECASE)
        if mo: return "%s%s" % (PL_v_irregular_pres[mo.group(1).lower()],
                                 mo.group(2))

# HANDLE IRREGULAR FUTURE, PRETERITE AND PERFECT TENSES 

        mo = search(r"^(%s)((\s.*)?)$" % PL_v_irregular_non_pres,
                    word, IGNORECASE)
        if mo: return word

# HANDLE PRESENT NEGATIONS (SIMPLE AND COMPOUND)

        mo = search(r"^(%s)(n't(\s.*)?)$" % PL_v_irregular_pres_keys,
                    word, IGNORECASE)
        if mo: return "%s%s" % (PL_v_irregular_pres[mo.group(1).lower()],
                                 mo.group(2))

        mo = search(r"^\S+n't\b",
                    word, IGNORECASE)
        if mo: return word

# HANDLE SPECIAL CASES

        mo = search(r"^(%s)$" % PL_v_special_s, word)
        if mo: return False
        if search(r"\s", word): return False


# HANDLE STANDARD 3RD PERSON (CHOP THE ...(e)s OFF SINGLE WORDS)

        mo = search(r"^(.*)([cs]h|[x]|zz|ss)es$",
                    word, IGNORECASE)
        if mo: return "%s%s" % (mo.group(1), mo.group(2))

        mo = search(r"^(..+)ies$",
                    word, IGNORECASE)
        if mo: return "%sy" % mo.group(1)

        mo = search(r"(%s)$" % PL_v_oes_oe,
                    word, IGNORECASE)
        if mo: return word[:-1]

        mo = search(r"(.+)oes$",
                    word, IGNORECASE)
        if mo: return word[:-2]

        mo = search(r"^(.*[^s])s$",
                    word, IGNORECASE)
        if mo: return mo.group(1)

# OTHERWISE, A REGULAR VERB (HANDLE ELSEWHERE)

        return False

    def _PL_general_verb(self, word, count=None):
        count = self.get_count(count)

        if count==1: return word

# HANDLE AMBIGUOUS PRESENT TENSES  (SIMPLE AND COMPOUND)

        mo = search(r"^(%s)((\s.*)?)$" % PL_v_ambiguous_pres_keys,
                    word, IGNORECASE)
        if mo: return "%s%s" % (PL_v_ambiguous_pres[mo.group(1).lower()],
                                 mo.group(2))

# HANDLE AMBIGUOUS PRETERITE AND PERFECT TENSES 

        mo = search(r"^(%s)((\s.*)?)$" % PL_v_ambiguous_non_pres,
                    word, IGNORECASE)
        if mo: return word

# OTHERWISE, 1st OR 2ND PERSON IS UNINFLECTED

        return word


    def _PL_special_adjective(self, word, count=None):
        count = self.get_count(count)

        if count==1: return word

# HANDLE USER-DEFINED ADJECTIVES

        value = self.ud_match(word, self.PL_adj_user_defined)
        if value is not None: return value

# HANDLE KNOWN CASES

        mo = search(r"^(%s)$" % PL_adj_special_keys,
                    word, IGNORECASE)
        if mo: return "%s" % (PL_adj_special[mo.group(1).lower()])

# HANDLE POSSESSIVES

        mo = search(r"^(%s)$" % PL_adj_poss_keys,
                    word, IGNORECASE)
        if mo: return "%s" % (PL_adj_poss[mo.group(1).lower()])

        mo = search(r"^(.*)'s?$",
                    word)
        if mo:
            pl = self.PL_N(mo.group(1))
            trailing_s = "" if pl[-1] == 's' else "s" 
            return "%s'%s" % (pl, trailing_s)

# OTHERWISE, NO IDEA

        return False


# ADJECTIVES

    def A(self, mystr, count=1):
        mo = search(r"\A(\s*)(?:an?\s+)?(.+?)(\s*)\Z",
                    mystr, IGNORECASE)
        if mo:
            word = mo.group(2)
            if not word: return mystr
            pre = mo.group(1)
            post = mo.group(3)
            result = self._indef_article(word, count)
            return "%s%s%s" % (pre, result, post)
        return '' #TODO: is this what should be returned on no match?

    AN = A


    def _indef_article(self, word, count):
        mycount = self.get_count(count)

        if mycount!=1: return "%s %s" % (count, word)


# HANDLE USER-DEFINED VARIANTS

        value = self.ud_match(word, self.A_a_user_defined)
        if value is not None: return "%s %s" % (value, word)


# HANDLE SPECIAL CASES

        for a in (
                  (r"(%s)" % A_explicit_an, "an"),
                  (r"^[aefhilmnorsx]$", "an"),
                  (r"^[bcdgjkpqtuvwyz]$", "a"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return "%s %s" % (a[1], word)


# HANDLE ABBREVIATIONS

        for a in (
                  (r"(%s)" % A_abbrev, "an", VERBOSE),
                  (r"^[aefhilmnorsx][.-]", "an", IGNORECASE),
                  (r"^[a-z][.-]", "a", IGNORECASE),
                 ):
            mo = search(a[0], word, a[2])
            if mo: return "%s %s" % (a[1], word)

# HANDLE CONSONANTS

        mo = search(r"^[^aeiouy]", word, IGNORECASE)
        if mo: return "a %s" % word

# HANDLE SPECIAL VOWEL-FORMS

        for a in (
                  (r"^e[uw]", "a"),
                  (r"^onc?e\b", "a"),
                  (r"^uni([^nmd]|mo)", "a"),
                  (r"^u[bcfhjkqrst][aeiou]", "a"),
                 ):
            mo = search(a[0], word, IGNORECASE)
            if mo: return "%s %s" % (a[1], word)

# HANDLE SPECIAL CAPITALS

        mo = search(r"^U[NK][AIEO]?", word)
        if mo: return "a %s" % word

# HANDLE VOWELS

        mo = search(r"^[aeiou]", word, IGNORECASE)
        if mo: return "an %s" % word

# HANDLE y... (BEFORE CERTAIN CONSONANTS IMPLIES (UNNATURALIZED) "i.." SOUND)

        mo = search(r"^(%s)" % A_y_cons, word, IGNORECASE)
        if mo: return "an %s" % word

# OTHERWISE, GUESS "a"
        return "a %s" % word


# 2. TRANSLATE ZERO-QUANTIFIED $word TO "no PL($word)"

    def NO(self, mystr, count=None):
        if count is None and self.persistent_count is not None:
            count = self.persistent_count

        if count is None:
            count = 0
        mo = search(r"\A(\s*)(.+?)(\s*)\Z", mystr)
        pre = mo.group(1)
        word = mo.group(2)
        post = mo.group(3)

        if str(count).lower() in PL_count_zero:
            return "%sno %s%s" % (pre, self.PL(word, 0), post)
        else:
            return "%s%s %s%s" % (pre, count, self.PL(word, count), post)


# PARTICIPLES

    def PART_PRES(self, word):
        plv = self.PL_V(word, 2)

        for pat, repl in (
                          (r"ie$", r"y"),
                          (r"ue$", r"u"),
                          (r"([auy])e$", r"\g<1>"),
                          (r"ski$", r"ski"),
                          (r"i$", r""),
                          (r"([^e])e$", r"\g<1>"),
                          (r"er$", r"er"),
                          (r"([^aeiou][aeiouy]([bdgmnprst]))$", "\g<1>\g<2>"),
                         ):
            (ans, num) = subn(pat, repl, plv)
            if num:
                return "%sing" % ans
        return "%sing" % ans
            
    #TODO: isn't ue$ -> u encompassed in the following rule?
    #TODO: bug: hoe should go to hoeing not hoing
    #TODO: bug: alibi should go to alibiing not alibing


# NUMERICAL INFLECTIONS

    def ORD(self, num):
        if match(r"\d", num):
            n = int(num)
            try:
                post = nth[n%100]
            except KeyError:
                post = nth[n%10]
            return "%s%s" % (n, post)
        else:
            mo = search(r"(%s)\Z" % ordinal_suff, num)
            try:
                post = ordinal[mo.group(1)]
                return resub(r"(%s)\Z" % ordinal_suff, post, num)
            except AttributeError:
                return "%sth" % num

    
    def millfn(self, ind=0):
        if ind > len(mill)-1:
            print3("Number out of range")
            raise NumOutOfRangeError
    
        return mill[ind] if ind < len(mill) else ' ???illion' #TODO: never returns ???illion as this is caught above
    
    
    def unitfn(self, units, mindex=0):
        return "%s%s" % (unit[units], self.millfn(mindex))
    
    def tenfn(self, tens, units, mindex=0):
        if tens != 1:
            return "%s%s%s%s" % (ten[tens],
                                 '-' if tens and units else '',
                                 unit[units],
                                 self.millfn(mindex))
        return "%s%s" % (teen[units],
                         mill[mindex])
    
    def hundfn(self, hundreds, tens, units, mindex):
        if hundreds:
            return "%s hundred%s%s%s, " % (unit[hundreds], #use unit not unitfn as simpler
                                           " %s " % self.number_args['andword'] if tens or units else '',
                                           self.tenfn(tens,units),
                                           self.millfn(mindex))
        if tens or units:
            return "%s%s, " % (self.tenfn(tens,units), self.millfn(mindex))
        return ''
    
    
    def group1sub(self, mo):
        units = int(mo.group(1))
        if units == 1: return " %s, " % self.number_args['one']
        elif units: return "%s, " % unit[units] #TODO: bug one and zero are padded with a space but other numbers aren't. check this in perl
        else: return " %s, " % self.number_args['zero']
    
    def group1bsub(self, mo):
        units = int(mo.group(1))
        if units: return "%s, " % unit[units] #TODO: bug one and zero are padded with a space but other numbers aren't. check this in perl
        else: return " %s, " % self.number_args['zero']
    
    def group2sub(self, mo):
        tens = int(mo.group(1))
        units = int(mo.group(2))
        if tens: return "%s, " % self.tenfn(tens, units)
        if units: return " %s %s, " % (self.number_args['zero'],unit[units])
        return " %s %s, " % (self.number_args['zero'], self.number_args['zero'])
    
    def group3sub(self, mo):
        hundreds = int(mo.group(1))
        tens = int(mo.group(2))
        units = int(mo.group(3))
        if hundreds==1: hunword = " %s" % self.number_args['one']
        elif hundreds: hunword = "%s" % unit[units] #TODO: bug one and zero are padded with a space but other numbers aren't. check this in perl
        else: hunword = " %s" % self.number_args['zero']
        if tens: tenword = self.tenfn(tens, units)
        elif units: tenword = " %s %s" % (self.number_args['zero'], unit[units])
        else: tenword = " %s %s" % (self.number_args['zero'], self.number_args['zero'])
        return "%s %s, " % (hunword, tenword)
    
    def hundsub(self, mo):
        ret = self.hundfn(int(mo.group(1)),
                     int(mo.group(2)),
                     int(mo.group(3)),
                     self.mill_count)
        self.mill_count += 1
        return ret
    
    def tensub(self, mo):
        return "%s, " % self.tenfn(int(mo.group(1)),
                              int(mo.group(2)),
                              self.mill_count)
    
    def unitsub(self, mo):
        return "%s, " % self.unitfn(int(mo.group(1)),
                              self.mill_count)
    
    def enword(self, num, group):
    
        if group==1:
            num = resub(r"(\d)", self.group1sub, num)
        elif group==2:
            num = resub(r"(\d)(\d)", self.group2sub, num)
            num = resub(r"(\d)", self.group1bsub, num, 1) #group1bsub same as group1sub except it doesn't use the default word for one. Is this required? i.e. is the default word only for the single number 1 and not for 1 in otehr cases???
        elif group==3:
            num = resub(r"(\d)(\d)(\d)", self.group3sub, num)
            num = resub(r"(\d)(\d)", self.group2sub, num, 1)
            num = resub(r"(\d)", self.group1sub, num, 1)
        elif int(num) == 0:
            num = self.number_args['zero']
        elif int(num) == 1:
            num = self.number_args['one']
        else:
            num = num.lstrip().lstrip('0')
            self.mill_count = 0
            num = resub(r"(\d)(\d)(\d)(?=\D*\Z)", self.hundsub, num)
            num = resub(r"(\d)(\d)(?=\D*\Z)", self.tensub, num, 1)
            num = resub(r"(\d)(?=\D*\Z)", self.unitsub, num, 1)
        return num
    
    def blankfn(self, mo):
        ''' do a global blank replace
        TODO: surely this can be done with an option to resub
              rather than this fn
        '''
        return ''
    
    def commafn(self, mo):
        ''' do a global ',' replace
        TODO: surely this can be done with an option to resub
              rather than this fn
        '''
        return ','

    def spacefn(self, mo):
        ''' do a global ' ' replace
        TODO: surely this can be done with an option to resub
              rather than this fn
        '''
        return ' '

    def NUMWORDS(self, num, wantarray=False, **kwds):
        self.number_args.update(kwds) 
        group = int(self.number_args['group'])
    
        # Handle "stylistic" conversions (up to a given threshold)...
        if ('threshold' in self.number_args and
             float(num) > self.number_args['threshold']):
            spnum = num.split('.',1)
            while (self.number_args['comma']):
                    (spnum[0], n) = subn(r"(\d)(\d{3}(?:,|\Z))",r"\1,\2", spnum[0])
                    if n==0: break
            try:
                return "%s.%s" % (spnum[0], spnum[1])
            except IndexError:
                return "%s" % spnum[0]
            
        if group < 0 or group > 3:
            raise BadChunkingOptionError 
        nowhite = num.lstrip()
        if nowhite[0] == '+':
            sign = "+"
        elif nowhite[0] == '-':
            sign = "-"
        else:
            sign = ""
        comma = self.number_args['comma']
        andword = self.number_args['andword'] #can't use 'and' keyword in **kwds
    
        myord =  (num[-2:] in ('st', 'nd', 'rd', 'th'))
        if myord: num = num[:-2]
        if self.number_args['decimal']:
            if group != 0:
                chunks = num.split('.')
            else:
                chunks = num.split('.',1)
        else:
            chunks = [num]


        first = 1
        loopstart = 0

        if chunks[0] == '':
            first = 0
            if len(chunks) > 1: loopstart = 1

        for i in range(loopstart, len(chunks)): 
            chunk = chunks[i]
            #remove all non numeric \D
            chunk = resub(r"\D", self.blankfn, chunk)
            if chunk == "": chunk = "0"

            if group != 0 and first != 0:
                chunk = self.enword(chunk, 1)
            else:
                chunk = self.enword(chunk, group)

            if chunk[-2:] == ', ': chunk = chunk[:-2]
            chunk = resub(r"\s+,", self.commafn, chunk)
            if group != 0 and first:
                chunk = resub(r", (\S+)\s+\Z", "%s \1" % andword, chunk)
            chunk = resub(r"\s+", self.spacefn, chunk)
            #chunk = resub(r"(\A\s|\s\Z)", self.blankfn, chunk)
            chunk = chunk.strip()
            if first: first = ''
            chunks[i] = chunk

        numchunks = []
        if first != 0:
            numchunks = chunks[0].split("%s " % comma)

        if myord and numchunks:
            #TODO: can this be just one re as it is in perl?
            mo = search(r"(%s)\Z" % ordinal_suff, numchunks[-1])
            if mo:
                numchunks[-1] = resub(r"(%s)\Z" % ordinal_suff , ordinal[mo.group(1)],
                                      numchunks[-1])
            else:
                numchunks[-1] += 'th'

        for chunk in chunks[1:]:
            numchunks.append(self.number_args['decimal'])
            numchunks.extend(chunk.split("%s " % comma))

        #wantarray: Perl list context. can explictly specify in Python
        if wantarray:
            if sign:
                return [sign].append(numchunks)
            return numchunks
        elif group:
            signout = "%s " % sign if sign else ''
            return "%s%s" % (signout, ", ".join(numchunks))
        else:
            signout = "%s " % sign if sign else ''
            num = "%s%s" % (signout, numchunks.pop(0))
            first = not num.endswith(self.number_args['decimal'])
            for nc in numchunks:
                if nc == self.number_args['decimal']:
                    num += " %s" % nc
                    first = 0
                elif first:
                    num += "%s %s" % (comma, nc)
                else:
                    num += " %s" % nc
            return num

# Join words with commas and a trailing 'and' (when appropriate)...

    def WORDLIST(self, *words, **opt):
        if not words: return ""
        if len(words) == 1: return words[0] 
 
        conj = opt.get('conj', 'and')
        if len(words) == 2:
            conj = resub(r"^(?=[^\W\d_])|(?<=[^\W\d_])$", self.spacefn, conj)
            return "%s%s%s" % (words[0], conj, words[1])
 
        try:
            sep = opt['sep']
        except KeyError:
            if ',' in ''.join(words):
                sep = '; '
            else:
                sep = ', '
    
        if 'final_sep' not in opt:
            final_sep = "%s %s" % (sep, conj)
        else:
            if len(opt['final_sep']) == 0:
                final_sep = conj
            else:
                final_sep = "%s %s" % (opt['final_sep'], conj)

        final_sep = resub(r"\s+", self.spacefn ,final_sep)
        final_sep = resub(r"^(?=[^\W\d_])|(?<=[^\W\d_])$", self.spacefn, final_sep)
    
        return "%s%s%s" %(sep.join(words[0:-1]), final_sep, words[-1])

