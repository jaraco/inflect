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

* Moved hosting to `jazzband <https://github.com/jazzband/inflect>`_.

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

* fix a/an for dishonor, Honolulu, mpeg, onetime, Ugandan, Ukranian,
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

* replace short named methods with longer methods. shorted method now print a message and rasie DecrecationWarning
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
