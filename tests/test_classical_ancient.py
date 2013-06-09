from nose.tools import eq_

import inflect


def test_ancient_1():
    p = inflect.engine()

    # DEFAULT...

    eq_(p.plural_noun('formula'),    'formulas',    msg="classical 'ancient' not active")

    # "person" PLURALS ACTIVATED...

    p.classical(ancient=True)
    eq_(p.plural_noun('formula'),    'formulae',    msg="classical 'ancient' active")

    # OTHER CLASSICALS NOT ACTIVATED...

    eq_(p.plural_noun('wildebeest'), 'wildebeests', msg="classical 'herd' not active")
    eq_(p.plural_noun('error', 0),   'errors',      msg="classical 'zero' not active")
    eq_(p.plural_noun('Sally'),      'Sallys',      msg="classical 'names' active")
    eq_(p.plural_noun('brother'),    'brothers',    msg="classical 'all' not active")
    eq_(p.plural_noun('person'),     'people',      msg="classical 'persons' not active")
