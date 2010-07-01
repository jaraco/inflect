
import unittest

from .. import inflect

class test(unittest.TestCase):

    def test_classical(self):

        p = inflect.engine()

        # DEFAULT...
        
        self.assertEqual(p.plnoun('error', 0)    , 'errors'           , msg="classical 'zero' not active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeests'      , msg="classical 'herd' not active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallys'           , msg="classical 'names' active")
        self.assertEqual(p.plnoun('brother')     , 'brothers'         , msg="classical others not active")
        self.assertEqual(p.plnoun('person')      , 'people'           , msg="classical 'persons' not active")
        self.assertEqual(p.plnoun('formula')     , 'formulas'         , msg="classical 'ancient' not active")
        
        # CLASSICAL PLURALS ACTIVATED...
        
        p.classical('all')
        self.assertEqual(p.plnoun('error', 0)    , 'error'           , msg="classical 'zero' active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeest'      , msg="classical 'herd' active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallys'          , msg="classical 'names' active")
        self.assertEqual(p.plnoun('brother')     , 'brethren'        , msg="classical others active")
        self.assertEqual(p.plnoun('person')      , 'persons'         , msg="classical 'persons' active")
        self.assertEqual(p.plnoun('formula')     , 'formulae'        , msg="classical 'ancient' active")
        
        
        # CLASSICAL PLURALS DEACTIVATED...
        
        p.classical(all=0)
        self.assertEqual(p.plnoun('error', 0)    , 'errors'           , msg="classical 'zero' not active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeests'      , msg="classical 'herd' not active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallies'          , msg="classical 'names' not active")
        self.assertEqual(p.plnoun('brother')     , 'brothers'         , msg="classical others not active")
        self.assertEqual(p.plnoun('person')      , 'people'           , msg="classical 'persons' not active")
        self.assertEqual(p.plnoun('formula')     , 'formulas'         , msg="classical 'ancient' not active")
        
        
        # CLASSICAL PLURALS REACTIVATED...
        
        p.classical(all=1)
        self.assertEqual(p.plnoun('error', 0)    , 'error'           , msg="classical 'zero' active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeest'      , msg="classical 'herd' active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallys'          , msg="classical 'names' active")
        self.assertEqual(p.plnoun('brother')     , 'brethren'        , msg="classical others active")
        self.assertEqual(p.plnoun('person')      , 'persons'         , msg="classical 'persons' active")
        self.assertEqual(p.plnoun('formula')     , 'formulae'        , msg="classical 'ancient' active")
        
        
        # CLASSICAL PLURALS REDEACTIVATED...
        
        p.classical(0)
        self.assertEqual(p.plnoun('error', 0)    , 'errors'           , msg="classical 'zero' not active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeests'      , msg="classical 'herd' not active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallies'          , msg="classical 'names' not active")
        self.assertEqual(p.plnoun('brother')     , 'brothers'         , msg="classical others not active")
        self.assertEqual(p.plnoun('person')      , 'people'           , msg="classical 'persons' not active")
        self.assertEqual(p.plnoun('formula')     , 'formulas'         , msg="classical 'ancient' not active")
        
        
        # CLASSICAL PLURALS REREACTIVATED...
        
        p.classical(1)
        self.assertEqual(p.plnoun('error', 0)    , 'error'           , msg="classical 'zero' active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeest'      , msg="classical 'herd' active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallys'          , msg="classical 'names' active")
        self.assertEqual(p.plnoun('brother')     , 'brethren'        , msg="classical others active")
        self.assertEqual(p.plnoun('person')      , 'persons'         , msg="classical 'persons' active")
        self.assertEqual(p.plnoun('formula')     , 'formulae'        , msg="classical 'ancient' active")
        
        
        # CLASSICAL PLURALS REREDEACTIVATED...
        
        p.classical(0)
        self.assertEqual(p.plnoun('error', 0)    , 'errors'           , msg="classical 'zero' not active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeests'      , msg="classical 'herd' not active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallies'          , msg="classical 'names' not active")
        self.assertEqual(p.plnoun('brother')     , 'brothers'         , msg="classical others not active")
        self.assertEqual(p.plnoun('person')      , 'people'           , msg="classical 'persons' not active")
        self.assertEqual(p.plnoun('formula')     , 'formulas'         , msg="classical 'ancient' not active")
        
        
        # CLASSICAL PLURALS REREREACTIVATED...
        
        p.classical()
        self.assertEqual(p.plnoun('error', 0)    , 'error'           , msg="classical 'zero' active")
        self.assertEqual(p.plnoun('wildebeest')  , 'wildebeest'      , msg="classical 'herd' active")
        self.assertEqual(p.plnoun('Sally')       , 'Sallys'          , msg="classical 'names' active")
        self.assertEqual(p.plnoun('brother')     , 'brethren'        , msg="classical others active")
        self.assertEqual(p.plnoun('person')      , 'persons'         , msg="classical 'persons' active")
        self.assertEqual(p.plnoun('formula')     , 'formulae'        , msg="classical 'ancient' active")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
    
