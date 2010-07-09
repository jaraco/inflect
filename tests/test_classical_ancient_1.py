
from nose.tools import eq_

from .. import inflect


def test_ancient_1():
    
    p = inflect.engine()

    # DEFAULT...
    
    eq_ (p.plnoun('formula')     , 'formulas'         , msg="classical 'ancient' not active")
    
    # "person" PLURALS ACTIVATED...
    
    p.classical(ancient=1)
    eq_ (p.plnoun('formula')     , 'formulae'         , msg="classical 'ancient' active")
    
    # OTHER CLASSICALS NOT ACTIVATED...
    
    eq_ (p.plnoun('wildebeest')  , 'wildebeests'      , msg="classical 'herd' not active")
    eq_ (p.plnoun('error', 0)    , 'errors'           , msg="classical 'zero' not active")
    eq_ (p.plnoun('Sally')       , 'Sallys'           , msg="classical 'names' active")
    eq_ (p.plnoun('brother')     , 'brothers'         , msg="classical 'all' not active")
    eq_ (p.plnoun('person')      , 'people'           , msg="classical 'persons' not active")
