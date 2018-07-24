import unittest

import inflect


class test(unittest.TestCase):
    def test_classical(self):
        p = inflect.engine()

        # DEFAULT...

        self.assertEqual(p.plural_noun('error', 0), 'errors',
                         msg="classical 'zero' not active")
        self.assertEqual(p.plural_noun('wildebeest'), 'wildebeests',
                         msg="classical 'herd' not active")
        self.assertEqual(p.plural_noun('Sally'), 'Sallys',
                         msg="classical 'names' active")
        self.assertEqual(p.plural_noun('brother'), 'brothers',
                         msg="classical others not active")
        self.assertEqual(p.plural_noun('person'), 'people',
                         msg="classical 'persons' not active")
        self.assertEqual(p.plural_noun('formula'), 'formulas',
                         msg="classical 'ancient' not active")

        # CLASSICAL PLURALS ACTIVATED...

        p.classical(all=True)
        self.assertEqual(p.plural_noun('error', 0), 'error',
                         msg="classical 'zero' active")
        self.assertEqual(p.plural_noun('wildebeest'), 'wildebeest',
                         msg="classical 'herd' active")
        self.assertEqual(p.plural_noun('Sally'), 'Sallys',
                         msg="classical 'names' active")
        self.assertEqual(p.plural_noun('brother'), 'brethren',
                         msg="classical others active")
        self.assertEqual(p.plural_noun('person'), 'persons',
                         msg="classical 'persons' active")
        self.assertEqual(p.plural_noun('formula'), 'formulae',
                         msg="classical 'ancient' active")

        # CLASSICAL PLURALS DEACTIVATED...

        p.classical(all=False)
        self.assertEqual(p.plural_noun('error', 0), 'errors',
                         msg="classical 'zero' not active")
        self.assertEqual(p.plural_noun('wildebeest'), 'wildebeests',
                         msg="classical 'herd' not active")
        self.assertEqual(p.plural_noun('Sally'), 'Sallies',
                         msg="classical 'names' not active")
        self.assertEqual(p.plural_noun('brother'), 'brothers',
                         msg="classical others not active")
        self.assertEqual(p.plural_noun('person'), 'people',
                         msg="classical 'persons' not active")
        self.assertEqual(p.plural_noun('formula'), 'formulas',
                         msg="classical 'ancient' not active")

        # CLASSICAL PLURALS REREREACTIVATED...

        p.classical()
        self.assertEqual(p.plural_noun('error', 0), 'error',
                         msg="classical 'zero' active")
        self.assertEqual(p.plural_noun('wildebeest'), 'wildebeest',
                         msg="classical 'herd' active")
        self.assertEqual(p.plural_noun('Sally'), 'Sallys',
                         msg="classical 'names' active")
        self.assertEqual(p.plural_noun('brother'), 'brethren',
                         msg="classical others active")
        self.assertEqual(p.plural_noun('person'), 'persons',
                         msg="classical 'persons' active")
        self.assertEqual(p.plural_noun('formula'), 'formulae',
                         msg="classical 'ancient' active")


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
