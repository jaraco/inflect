from nose.tools import eq_

import inflect


def test_an():
    p = inflect.engine()

    eq_(p.an('cat'), 'a cat', msg='a cat')
    eq_(p.an('ant'), 'an ant', msg='an ant')
    eq_(p.an('a'), 'an a', msg='an a')
    eq_(p.an('b'), 'a b', msg='a b')
    eq_(p.an('honest cat'), 'an honest cat', msg='an honest')
    eq_(p.an('dishonest cat'), 'a dishonest cat', msg='a dishonest')
    eq_(p.an('Honolulu sunset'), 'a Honolulu sunset', msg='a Honolulu')
    eq_(p.an('mpeg'), 'an mpeg', msg='an mpeg')
    eq_(p.an('onetime holiday'), 'a onetime holiday', msg='a onetime')
    eq_(p.an('Ugandan person'), 'a Ugandan person', msg='a Ugandan')
    eq_(p.an('Ukranian person'), 'a Ukranian person', msg='a Ukranian')
    eq_(p.an('Unabomber'), 'a Unabomber', msg='a Unabomber')
    eq_(p.an('unanimous decision'), 'a unanimous decision', msg='a unanimous')
    eq_(p.an('US farmer'), 'a US farmer', msg='a US')
