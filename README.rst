.. image:: https://img.shields.io/pypi/v/inflect.svg
   :target: https://pypi.org/project/inflect

.. image:: https://img.shields.io/pypi/pyversions/inflect.svg

.. image:: https://github.com/jaraco/inflect/actions/workflows/main.yml/badge.svg
   :target: https://github.com/jaraco/inflect/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://readthedocs.org/projects/inflect/badge/?version=latest
   :target: https://inflect.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2025-informational
   :target: https://blog.jaraco.com/skeleton

.. image:: https://tidelift.com/badges/package/pypi/inflect
   :target: https://tidelift.com/subscription/pkg/pypi-inflect?utm_source=pypi-inflect&utm_medium=readme

NAME
====

inflect.py - Accurately generate plurals, singular nouns, ordinals, indefinite articles, and word-based representations of numbers. This functionality is limited to English.

SYNOPSIS
========

.. code-block:: python
    
    >>> import inflect
    >>> p = inflect.engine()

Simple example with pluralization and word-representation of numbers:

.. code-block:: python
    
    >>> count=1
    >>> print('There', p.plural_verb('was', count), p.number_to_words(count), p.plural_noun('person', count), 'by the door.')
    There was one person by the door.

When ``count=243``, the same code will generate:

.. code-block:: python
    
    There were two hundred and forty-three people by the door.


Methods
=======

- ``plural``, ``plural_noun``, ``plural_verb``, ``plural_adj``, ``singular_noun``, ``no``, ``num``
- ``compare``, ``compare_nouns``, ``compare_nouns``, ``compare_adjs``
- ``a``, ``an``
- ``present_participle``
- ``ordinal``, ``number_to_words``
- ``join``
- ``inflect``, ``classical``, ``gender``
- ``defnoun``, ``defverb``, ``defadj``, ``defa``, ``defan``

Plurality/Singularity
---------------------
Unconditionally Form the Plural
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> "the plural of person is " + p.plural("person")
    'the plural of person is people'

Conditionally Form the Plural
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> "the plural of 1 person is " + p.plural("person", 1)
    'the plural of 1 person is person'

Form Plurals for Specific Parts of Speech
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.plural_noun("I", 2)
    'we'
    >>> p.plural_verb("saw", 1)
    'saw'
    >>> p.plural_adj("my", 2)
    'our'
    >>> p.plural_noun("saw", 2)
    'saws'

Form the Singular of Plural Nouns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> "The singular of people is " + p.singular_noun("people")
    'The singular of people is person'

Select the Gender of Singular Pronouns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.singular_noun("they")
    'it'
    >>> p.gender("feminine")
    >>> p.singular_noun("they")
    'she'

Deal with "0/1/N" -> "no/1/N" Translation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> errors = 1
    >>> "There ", p.plural_verb("was", errors), p.no(" error", errors)
    ('There ', 'was', ' 1 error')
    >>> errors = 2
    >>> "There ", p.plural_verb("was", errors), p.no(" error", errors)
    ('There ', 'were', ' 2 errors')

Use Default Counts
^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.num(1, "")
    ''
    >>> p.plural("I")
    'I'
    >>> p.plural_verb(" saw")
    ' saw'
    >>> p.num(2)
    '2'
    >>> p.plural_noun(" saw")
    ' saws'
    >>> "There ", p.num(errors, ""), p.plural_verb("was"), p.no(" error")
    ('There ', '', 'were', ' 2 errors')

Compare Two Words Number-Intensitively
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.compare('person', 'person')
    'eq'
    >>> p.compare('person', 'people')
    's:p'
    >>> p.compare_nouns('person', 'people')
    's:p'
    >>> p.compare_verbs('run', 'ran')
    False
    >>> p.compare_verbs('run', 'running')
    False
    >>> p.compare_verbs('run', 'run')
    'eq'
    >>> p.compare_adjs('my', 'mine')
    False
    >>> p.compare_adjs('my', 'our')
    's:p'

Add Correct *a* or *an* for a Given Word
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> "Did you want ", p.a('thing'), " or ", p.a('idea')
    ('Did you want ', 'a thing', ' or ', 'an idea')

Convert Numerals into Ordinals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> "It was", p.ordinal(1), " from the left"
    ('It was', '1st', ' from the left')
    >>> "It was", p.ordinal(2), " from the left"
    ('It was', '2nd', ' from the left')
    >>> "It was", p.ordinal(3), " from the left"
    ('It was', '3rd', ' from the left')
    >>> "It was", p.ordinal(347), " from the left"
    ('It was', '347th', ' from the left')

Convert Numerals to Words
^^^^^^^^^^^^^^^^^^^^^^^^^
Note: This returns a single string.

.. code-block:: python
    
    >>> p.number_to_words(1)
    'one'
    >>> p.number_to_words(38)
    'thirty-eight'
    >>> p.number_to_words(1234)
    'one thousand, two hundred and thirty-four'
    >>> p.number_to_words(p.ordinal(1234))
    'one thousand, two hundred and thirty-fourth'

Retrieve Words as List of Parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.number_to_words(1234, wantlist=True)
    ['one thousand', 'two hundred and thirty-four']

Grouping Options
^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.number_to_words(12345, group=1)
    'one, two, three, four, five'
    >>> p.number_to_words(12345, group=2)
    'twelve, thirty-four, five'
    >>> p.number_to_words(12345, group=3)
    'one twenty-three, forty-five'
    >>> p.number_to_words(1234, andword="")
    'one thousand, two hundred thirty-four'
    >>> p.number_to_words(1234, andword=", plus")
    'one thousand, two hundred, plus thirty-four'
    >>> p.number_to_words(555_1202, group=1, zero="oh")
    'five, five, five, one, two, oh, two'
    >>> p.number_to_words(555_1202, group=1, one="unity")
    'five, five, five, unity, two, zero, two'
    >>> p.number_to_words(123.456, group=1, decimal="mark")
    'one, two, three, mark, four, five, six'

Apply Threshold for Word-Representation of Numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Above provided threshold, numberals will remain numerals

.. code-block:: python
    
    >>> p.number_to_words(9, threshold=10)
    'nine'
    >>> p.number_to_words(10, threshold=10)
    'ten'
    >>> p.number_to_words(11, threshold=10)
    '11'
    >>> p.number_to_words(1000, threshold=10)
    '1,000'

Join Words into a List
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    >>> p.join(("apple", "banana", "carrot"))
    'apple, banana, and carrot'
    >>> p.join(("apple", "banana"))
    'apple and banana'
    >>> p.join(("apple", "banana", "carrot"), final_sep="")
    'apple, banana and carrot'
    >>> p.join(('apples', 'bananas', 'carrots'), conj='and even')
    'apples, bananas, and even carrots'
    >>> p.join(('apple', 'banana', 'carrot'), sep='/', sep_spaced=False, conj='', conj_spaced=False)
    'apple/banana/carrot'
    
Require Classical Plurals
^^^^^^^^^^^^^^^^^^^^^^^^^
Adhere to conventions from Classical Latin and Classical Greek

.. code-block:: python
        
    >>> p.classical()
    >>> p.plural_noun("focus", 2)
    'foci'
    >>> p.plural_noun("cherubim", 2)
    'cherubims'
    >>> p.plural_noun("cherub", 2)
    'cherubim'

Other options for classical plurals:

.. code-block:: python
    
    p.classical(all=True)  # USE ALL CLASSICAL PLURALS
    p.classical(all=False)  # SWITCH OFF CLASSICAL MODE
    
    p.classical(zero=True)  #  "no error" INSTEAD OF "no errors"
    p.classical(zero=False)  #  "no errors" INSTEAD OF "no error"
    
    p.classical(herd=True)  #  "2 buffalo" INSTEAD OF "2 buffalos"
    p.classical(herd=False)  #  "2 buffalos" INSTEAD OF "2 buffalo"
    
    p.classical(persons=True)  # "2 chairpersons" INSTEAD OF "2 chairpeople"
    p.classical(persons=False)  # "2 chairpeople" INSTEAD OF "2 chairpersons"
    
    p.classical(ancient=True)  # "2 formulae" INSTEAD OF "2 formulas"
    p.classical(ancient=False)  # "2 formulas" INSTEAD OF "2 formulae"


Support for interpolation
^^^^^^^^^^^^^^^^^^^^^^^^^
Supports string interpolation with the following functions: ``plural()``, ``plural_noun()``, ``plural_verb()``, ``plural_adj()``, ``singular_noun()``, ``a()``, ``an()``, ``num()`` and ``ordinal()``.

.. code-block:: python
    
    >>> p.inflect("The plural of {0} is plural('{0}')".format('car'))
    'The plural of car is cars'
    >>> p.inflect("The singular of {0} is singular_noun('{0}')".format('car'))
    'The singular of car is car'
    >>> p.inflect("I saw {0} plural('cat',{0})".format(3))
    'I saw 3 cats'
    >>> p.inflect(
    ...     "plural('I',{0}) "
    ...     "plural_verb('saw',{0}) "
    ...     "plural('a',{1}) "
    ...     "plural_noun('saw',{1})".format(1, 2)
    ... )
    'I saw some saws'
    >>> p.inflect(
    ...     "num({0}, False)plural('I') "
    ...     "plural_verb('saw') "
    ...     "num({1}, False)plural('a') "
    ...     "plural_noun('saw')".format(N1, 1)
    ... )
    'I saw a saw'
    >>> p.inflect(
    ...     "num({0}, False)plural('I') "
    ...     "plural_verb('saw') "
    ...     "num({1}, False)plural('a') "
    ...     "plural_noun('saw')".format(2, 2)
    ... )
    'we saw some saws'
    >>> p.inflect("I saw num({0}) plural('cat')\nnum()".format(cat_count))
    'I saw 3 cats\n'
    >>> p.inflect("There plural_verb('was',{0}) no('error',{0})".format(errors))
    'There were 2 errors'
    >>> p.inflect("There num({0}, False)plural_verb('was') no('error')".format(errors))
    'There were 2 errors'
    >>> p.inflect("Did you want a('{0}') or an('{1}')".format(thing, idea))
    'Did you want a thing or an idea'
    >>> p.inflect("It was ordinal('{0}') from the left".format(2))
    'It was 2nd from the left'

Add User-Defined Inflections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Allows for overriding default rules.

Override noun defaults:

.. code-block:: python
        
    p.defnoun("VAX", "VAXen")  # SINGULAR => PLURAL

Override Verb defaults:

.. code-block:: python
    
    p.defverb(
        "will",  # 1ST PERSON SINGULAR
        "shall",  # 1ST PERSON PLURAL
        "will",  # 2ND PERSON SINGULAR
        "will",  # 2ND PERSON PLURAL
        "will",  # 3RD PERSON SINGULAR
        "will",  # 3RD PERSON PLURAL
    )

Override adjective defaults:

.. code-block:: python
    
    >>> p.defadj('hir', 'their')
    1
    >>> p.plural_adj('hir', 2)
    'their'

Override the words that use the indefinite articles "a" or "an":

.. code-block:: python
    
    >>> p.a('ape', 1)
    'an ape'
    >>> p.defa('a')
    1
    >>> p.a('ape', 1)
    'an ape'
    >>> p.defa('ape')
    1
    >>> p.a('ape', 1)
    'a ape'
    >>> p.defan('horrendous.*')
    1
    >>> p.a('horrendous affectation', 1)
    'an horrendous affectation'
    >>> 


DESCRIPTION
===========

The methods of the class ``engine`` in module ``inflect.py`` provide plural
inflections, singular noun inflections, "a"/"an" selection for English words,
and manipulation of numbers as words.

Plural forms of all nouns, most verbs, and some adjectives are
provided. Where appropriate, "classical" variants (for example: "brother" ->
"brethren", "dogma" -> "dogmata", etc.) are also provided.

Single forms of nouns are also provided. The gender of singular pronouns
can be chosen (for example "they" -> "it" or "she" or "he" or "they").

Pronunciation-based "a"/"an" selection is provided for all English
words, and most initialisms.

It is also possible to inflect numerals (1,2,3) to ordinals (1st, 2nd, 3rd)
or to English words ("one", "two", "three").

In generating these inflections, ``inflect.py`` follows the Oxford
English Dictionary and the guidelines in Fowler's Modern English
Usage, preferring the former where the two disagree.

The module is built around standard British spelling, but is designed
to cope with common American variants as well. Slang, jargon, and
other English dialects are *not* explicitly catered for.

Where two or more inflected forms exist for a single word (typically a
"classical" form and a "modern" form), ``inflect.py`` prefers the
more common form (typically the "modern" one), unless "classical"
processing has been specified
(see `MODERN VS CLASSICAL INFLECTIONS`).

FORMING PLURALS AND SINGULARS
=============================

Inflecting Plurals and Singulars
--------------------------------

All of the ``plural...`` plural inflection methods take the word to be
inflected as their first argument and return the corresponding inflection.
Note that all such methods expect the *singular* form of the word. The
results of passing a plural form are undefined (and unlikely to be correct).
Similarly, the ``si...`` singular inflection method expects the *plural*
form of the word.

The ``plural...`` methods also take an optional second argument,
which indicates the grammatical "number" of the word (or of another word
with which the word being inflected must agree). If the "number" argument is
supplied and is not ``1`` (or ``"one"`` or ``"a"``, or some other adjective that
implies the singular), the plural form of the word is returned. If the
"number" argument *does* indicate singularity, the (uninflected) word
itself is returned. If the number argument is omitted, the plural form
is returned unconditionally.

The ``si...`` method takes a second argument in a similar fashion. If it is
some form of the number ``1``, or is omitted, the singular form is returned.
Otherwise the plural is returned unaltered.


The various methods of ``inflect.engine`` are:



``plural_noun(word, count=None)``

 The method ``plural_noun()`` takes a *singular* English noun or
 pronoun and returns its plural. Pronouns in the nominative ("I" ->
 "we") and accusative ("me" -> "us") cases are handled, as are
 possessive pronouns ("mine" -> "ours").


``plural_verb(word, count=None)``

 The method ``plural_verb()`` takes the *singular* form of a
 conjugated verb (that is, one which is already in the correct "person"
 and "mood") and returns the corresponding plural conjugation.


``plural_adj(word, count=None)``

 The method ``plural_adj()`` takes the *singular* form of
 certain types of adjectives and returns the corresponding plural form.
 Adjectives that are correctly handled include: "numerical" adjectives
 ("a" -> "some"), demonstrative adjectives ("this" -> "these", "that" ->
 "those"), and possessives ("my" -> "our", "cat's" -> "cats'", "child's"
 -> "childrens'", etc.)


``plural(word, count=None)``

 The method ``plural()`` takes a *singular* English noun,
 pronoun, verb, or adjective and returns its plural form. Where a word
 has more than one inflection depending on its part of speech (for
 example, the noun "thought" inflects to "thoughts", the verb "thought"
 to "thought"), the (singular) noun sense is preferred to the (singular)
 verb sense.

 Hence ``plural("knife")`` will return "knives" ("knife" having been treated
 as a singular noun), whereas ``plural("knifes")`` will return "knife"
 ("knifes" having been treated as a 3rd person singular verb).

 The inherent ambiguity of such cases suggests that,
 where the part of speech is known, ``plural_noun``, ``plural_verb``, and
 ``plural_adj`` should be used in preference to ``plural``.


``singular_noun(word, count=None)``

 The method ``singular_noun()`` takes a *plural* English noun or
 pronoun and returns its singular. Pronouns in the nominative ("we" ->
 "I") and accusative ("us" -> "me") cases are handled, as are
 possessive pronouns ("ours" -> "mine"). When third person
 singular pronouns are returned they take the neuter gender by default
 ("they" -> "it"), not ("they"-> "she") nor ("they" -> "he"). This can be
 changed with ``gender()``.

Note that all these methods ignore any whitespace surrounding the
word being inflected, but preserve that whitespace when the result is
returned. For example, ``plural(" cat  ")`` returns " cats  ".


``gender(genderletter)``

 The third person plural pronoun takes the same form for the female, male and
 neuter (e.g. "they"). The singular however, depends upon gender (e.g. "she",
 "he", "it" and "they" -- "they" being the gender neutral form.) By default
 ``singular_noun`` returns the neuter form, however, the gender can be selected with
 the ``gender`` method. Pass the first letter of the gender to
 ``gender`` to return the f(eminine), m(asculine), n(euter) or t(hey)
 form of the singular. e.g.
 gender('f') followed by singular_noun('themselves') returns 'herself'.

Numbered plurals
----------------

The ``plural...`` methods return only the inflected word, not the count that
was used to inflect it. Thus, in order to produce "I saw 3 ducks", it
is necessary to use:

.. code-block:: python

    print("I saw", N, p.plural_noun(animal, N))

Since the usual purpose of producing a plural is to make it agree with
a preceding count, inflect.py provides a method
(``no(word, count)``) which, given a word and a(n optional) count, returns the
count followed by the correctly inflected word. Hence the previous
example can be rewritten:

.. code-block:: python

    print("I saw ", p.no(animal, N))

In addition, if the count is zero (or some other term which implies
zero, such as ``"zero"``, ``"nil"``, etc.) the count is replaced by the
word "no". Hence, if ``N`` had the value zero, the previous example
would print (the somewhat more elegant)::

    I saw no animals

rather than::

    I saw 0 animals

Note that the name of the method is a pun: the method
returns either a number (a *No.*) or a ``"no"``, in front of the
inflected word.


Reducing the number of counts required
--------------------------------------

In some contexts, the need to supply an explicit count to the various
``plural...`` methods makes for tiresome repetition. For example:

.. code-block:: python

    print(
        plural_adj("This", errors),
        plural_noun(" error", errors),
        plural_verb(" was", errors),
        " fatal.",
    )

inflect.py therefore provides a method
(``num(count=None, show=None)``) which may be used to set a persistent "default number"
value. If such a value is set, it is subsequently used whenever an
optional second "number" argument is omitted. The default value thus set
can subsequently be removed by calling ``num()`` with no arguments.
Hence we could rewrite the previous example:

.. code-block:: python

    p.num(errors)
    print(p.plural_adj("This"), p.plural_noun(" error"), p.plural_verb(" was"), "fatal.")
    p.num()

Normally, ``num()`` returns its first argument, so that it may also
be "inlined" in contexts like:

.. code-block:: python

    print(p.num(errors), p.plural_noun(" error"), p.plural_verb(" was"), " detected.")
    if severity > 1:
        print(
            p.plural_adj("This"), p.plural_noun(" error"), p.plural_verb(" was"), "fatal."
        )

However, in certain contexts (see `INTERPOLATING INFLECTIONS IN STRINGS`)
it is preferable that ``num()`` return an empty string. Hence ``num()``
provides an optional second argument. If that argument is supplied (that is, if
it is defined) and evaluates to false, ``num`` returns an empty string
instead of its first argument. For example:

.. code-block:: python

    print(p.num(errors, 0), p.no("error"), p.plural_verb(" was"), " detected.")
    if severity > 1:
        print(
            p.plural_adj("This"), p.plural_noun(" error"), p.plural_verb(" was"), "fatal."
        )



Number-insensitive equality
---------------------------

inflect.py also provides a solution to the problem
of comparing words of differing plurality through the methods
``compare(word1, word2)``, ``compare_nouns(word1, word2)``,
``compare_verbs(word1, word2)``, and ``compare_adjs(word1, word2)``.
Each  of these methods takes two strings, and  compares them
using the corresponding plural-inflection method (``plural()``, ``plural_noun()``,
``plural_verb()``, and ``plural_adj()`` respectively).

The comparison returns true if:

- the strings are equal, or
- one string is equal to a plural form of the other, or
- the strings are two different plural forms of the one word.


Hence all of the following return true:

.. code-block:: python

    p.compare("index", "index")  # RETURNS "eq"
    p.compare("index", "indexes")  # RETURNS "s:p"
    p.compare("index", "indices")  # RETURNS "s:p"
    p.compare("indexes", "index")  # RETURNS "p:s"
    p.compare("indices", "index")  # RETURNS "p:s"
    p.compare("indices", "indexes")  # RETURNS "p:p"
    p.compare("indexes", "indices")  # RETURNS "p:p"
    p.compare("indices", "indices")  # RETURNS "eq"

As indicated by the comments in the previous example, the actual value
returned by the various ``compare`` methods encodes which of the
three equality rules succeeded: "eq" is returned if the strings were
identical, "s:p" if the strings were singular and plural respectively,
"p:s" for plural and singular, and "p:p" for two distinct plurals.
Inequality is indicated by returning an empty string.

It should be noted that two distinct singular words which happen to take
the same plural form are *not* considered equal, nor are cases where
one (singular) word's plural is the other (plural) word's singular.
Hence all of the following return false:

.. code-block:: python

    p.compare("base", "basis")  # ALTHOUGH BOTH -> "bases"
    p.compare("syrinx", "syringe")  # ALTHOUGH BOTH -> "syringes"
    p.compare("she", "he")  # ALTHOUGH BOTH -> "they"

    p.compare("opus", "operas")  # ALTHOUGH "opus" -> "opera" -> "operas"
    p.compare("taxi", "taxes")  # ALTHOUGH "taxi" -> "taxis" -> "taxes"

Note too that, although the comparison is "number-insensitive" it is *not*
case-insensitive (that is, ``plural("time","Times")`` returns false. To obtain
both number and case insensitivity, use the ``lower()`` method on both strings
(that is, ``plural("time".lower(), "Times".lower())`` returns true).

Related Functionality
=====================

Shout out to these libraries that provide related functionality:

* `WordSet <https://jaracotext.readthedocs.io/en/latest/#jaraco.text.WordSet>`_
  parses identifiers like variable names into sets of words suitable for re-assembling
  in another form.

* `word2number <https://pypi.org/project/word2number/>`_ converts words to
  a number.


For Enterprise
==============

Available as part of the Tidelift Subscription.

This project and the maintainers of thousands of other packages are working with Tidelift to deliver one enterprise subscription that covers all of the open source you use.

`Learn more <https://tidelift.com/subscription/pkg/pypi-PROJECT?utm_source=pypi-PROJECT&utm_medium=referral&utm_campaign=github>`_.
