
from nose.tools import eq_, assert_not_equal

from .. import inflect

def test_an():
    
    p = inflect.engine()

    eq_(p.an('cat'), 'a cat' ,msg='cat')
    eq_(p.an('ant'), 'an ant' ,msg='ant')
    eq_(p.an('a'), 'an a' ,msg='a')
    eq_(p.an('b'), 'a b' ,msg='b')
    eq_(p.an('honest cat'), 'an honest cat' ,msg='honest')
    eq_(p.an('dishonest cat'), 'a dishonest cat' ,msg='dishonest')
    
