v7.5.0
======

Features
--------

- Updated `ast` classes for Python 3.14 compatibility. (#225)


v7.4.0
======

Features
--------

- Handle a single apostrophe more gracefully. (#218)


v7.3.1
======

Bugfixes
--------

- Set minimum version of more-itertools to 8.5 (#215)


v7.3.0
======

Features
--------

- Restricted typing_extensions to Python 3.8. (#211)


v7.2.1
======

Bugfixes
--------

- Refactored number_to_words toward reduced complexity.


v7.2.0
======

Features
--------

- Replace pydantic with typeguard (#195)


v7.1.0
======

Features
--------

- Now handle 'pair of x' in pl_sb_uninflected_complete (#188)


v7.0.0
======

Features
--------

- Refine type hint for ``singular_noun`` to indicate a literal return type for ``False``. (#186)


Deprecations and Removals
-------------------------

- Removed methods renamed in 0.2.0.


v6.2.0
======

Features
--------

- Project now supports Pydantic 2 while retaining support for Pydantic 1. (#187)


Bugfixes
--------

- Added validation of user-defined words and amended the type declarations to match, allowing for null values but not empty strings. (#187)


v6.1.1
======

Bugfixes
--------

- ``ordinal`` now handles float types correctly without first coercing them to strings. (#178)


v6.1.0
======

Features
--------

- Require Python 3.8 or later.


v6.0.5
======

* #187: Pin to Pydantic 1 to avoid breaking in Pydantic 2.

v6.0.4
======

* Internal cleanup.

v6.0.3
======

* #136: A/an support now more correctly honors leading
  capitalized words and abbreviations.

* #178: Improve support for ordinals for floats.

v6.0.2
======

* #169: Require pydantic 1.9.1 to avoid ``ValueError``.

v6.0.1
======

* Minor tweaks and packaging refresh.

v6.0.0
======

* #157: ``compare`` methods now validate their inputs
  and will raise a more meaningful exception if an
  empty string or None is passed. This expectation is now
  documented.

* Many public methods now perform validation on arguments.
  An empty string is no longer allowed for words or text.
  Callers are expected to pass non-empty text or trap
  the validation errors that are raised. The exceptions
  raised are ``pydantic.error_wrappers.ValidationError``,
  which are currently a subclass of ``ValueError``, but since
  that
  `may change <https://pydantic-docs.helpmanual.io/usage/validation_decorator/#validation-exception>`_,
  tests check for a generic ``Exception``.

v5.6.2
======

* #15: Fixes to plural edge case handling.

v5.6.1
======

* Packaging refresh and docs update.

v5.6.0
======

* #153: Internal refactor to simplify and unify
  ``_plnoun`` and ``_sinoun``.

v5.5.2
======

* Fixed badges.

v5.5.1
======

* #150: Rewrite to satisfy type checkers.

v5.5.0
======

* #147: Enhanced type annotations.

v5.4.0
======

* #133: Add a ``py.typed`` file so mypy recognizes type annotations.
* Misc fixes in #128, #134, #135, #137, #138, #139, #140, #142,
  #143, #144.
* Require Python 3.7 or later.

v5.3.0
======

* #108: Add support for pluralizing open compound nouns.

v5.2.0
======

* #121: Modernized the codebase. Added a lot of type annotations.

v5.1.0
======

* #113: Add support for uncountable nouns.

v5.0.3
======

* Refreshed package metadata.

v5.0.2
======

* #102: Inflect withdraws from `Jazzband <https://jazzband.co>`_
  in order to continue to participate in sustained maintenance
  and enterprise support through `Tidelift <https://tidelift.com>`_.
  The project continues to honor the guidelines and principles
  behind Jazzband and welcomes contributors openly.

v5.0.1
======

* Identical release validating release process.

v5.0.0
======

* Module no longer exposes a ``__version__`` attribute. Instead
  to query the version installed, use
  `importlib.metadata <https://docs.python.org/3/library/importlib.metadata.html>`_
  or `its backport <https://pypi.org/project/importlib_metadata>`_
  to query::

    importlib.metadata.version('inflect')

v4.1.1
======

* Refreshed package metadata.

v4.1.0
======

* #95: Certain operations now allow ignore arbitrary leading words.

v4.0.0
======

* Require Python 3.6 or later.

v3.0.2
======

* #88: Distribution no longer includes root ``tests`` package.

v3.0.1
======

* Project now builds on jaraco/skeleton for shared package
  management.

v3.0.0
======

* #75: Drop support for Python 3.4.

v2.1.0
======

* #29: Relicensed under the more permissive MIT License.

v2.0.1
======

* #57: Fix pluralization of taco.

v2.0.0
======

* #37: fix inconsistencies with the inflect method

  We now build and parse AST to extract function arguments instead of relying
  on regular expressions. This also adds support for keyword arguments and
  built-in constants when calling functions in the string.
  Unfortunately, this is not backwards compatible in some cases:
* Strings should now be wrapped in single or double quotes
  p.inflect("singular_noun(to them)") should now be p.inflect("singular_noun('to them')")
* Empty second argument to a function will now be parsed as None instead of ''.
  p.inflect("num(%d,) eggs" % 2) now prints "2 eggs" instead of " eggs"
  Since None, True and False are now supported, they can be passed explicitly:
  p.inflect("num(%d, False) eggs" % 2) will print " eggs"
  p.inflect("num(%d, True) eggs" % 2) will print "2 eggs"

v1.0.2
======

* #53: Improved unicode handling.
* #5 and #40 via #55: Fix capitalization issues in processes where
  more than one word is involved.
* #56: Handle correctly units containing 'degree' and 'per'.

v1.0.1
======

* #31: fix extraneous close parentheses.

v1.0.0
======

* Dropped support for Python 3.3.

v0.3.1
======

* Fixed badges in readme.

v0.3.0
======

* Moved hosting to the `jazzband project on GitHub <https://github.com/jazzband/inflect>`_.

v0.2.5
======

* Fixed TypeError while parsing compounds (by yavarhusain)
* Fixed encoding issue in setup.py on Python 3


v0.2.4
======

* new maintainer (Alex Grönholm)
* added Python 3 compatibility (by Thorben Krüger)


v0.2.3
======

* fix a/an for dishonor, Honolulu, mpeg, onetime, Ugandan, Ukrainian,
  Unabomber, unanimous, US
* merge in 'subspecies' fix by UltraNurd
* add arboretum to classical plurals
* prevent crash with singular_noun('ys')


v0.2.2
======

* change numwords to number_to_words in strings
* improve some docstrings
* comment out imports for unused .inflectrc
* remove unused exception class


v0.2.1
======

* remove incorrect gnome_sudoku import


v0.2.0
======

* add gender() to select the gender of singular pronouns
* replace short named methods with longer methods. shorted method now print a message and raise DecrecationWarning

  pl -> plural

  plnoun -> plural_noun

  plverb -> plural_verb

  pladj -> plural_adjective

  sinoun -> singular_noun

  prespart -> present_participle

  numwords -> number_to_words

  plequal -> compare

  plnounequal -> compare_nouns

  plverbequal -> compare_verbs

  pladjequal -> compare_adjs

  wordlist -> join
* change classical() to only accept keyword args: only one way to do it
* fix bug in numwords where hundreds was giving the wrong number when group=3


v0.1.8
======

* add line to setup showing that this provides 'inflect' so that
  inflect_dj can require it
* add the rest of the tests from the Perl version


v0.1.7
======

* replace most of the regular expressions in _plnoun and _sinoun. They run several times faster now.


v0.1.6
======

* add method sinoun() to generate the singular of a plural noun. Phew!
* add changes from new Perl version: 1.892
* start adding tests from Perl version
* add test to check sinoun(plnoun(word)) == word
  Can now use word lists to check these methods without needing to have
  a list of plurals. ;-)
* fix die -> dice
