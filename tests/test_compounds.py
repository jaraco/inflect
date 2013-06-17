from nose.tools import eq_

import inflect


class TestCompounds(object):
    def setup(self):
        self.p = inflect.engine()

    def test_compound_1(self):
        eq_(self.p.singular_noun('hello-out-there'), 'hello-out-there')

    def test_compound_2(self):
        eq_(self.p.singular_noun('hello out there'), 'hello out there')

    def test_compound_3(self):
        eq_(self.p.singular_noun('continue-to-operate'), 'continue-to-operate')

    def test_compound_4(self):
        eq_(self.p.singular_noun('case of diapers'), 'case of diapers')
