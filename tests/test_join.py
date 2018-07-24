
from nose.tools import eq_

import inflect


def test_join():
    p = inflect.engine()

    # Three words...
    words = "apple banana carrot".split()

    eq_(p.join(words),
        "apple, banana, and carrot", msg='plain 3 words')

    eq_(p.join(words, final_sep=''),
        "apple, banana and carrot", msg='3 words, no final sep')

    eq_(p.join(words, final_sep='...'),
        "apple, banana... and carrot", msg='3 words, different final sep')

    eq_(p.join(words, final_sep='...', conj=''),
        "apple, banana... carrot",
        msg='-->{} != {}<--   3 words, different final sep, no conjunction'.format(
        p.join(words, final_sep='...', conj=''), "apple, banana... carrot"))

    eq_(p.join(words, conj='or'),
        "apple, banana, or carrot",
        msg='{} != {}    3 words, different conjunction'.format(
            p.join(words, conj='or'),
            "apple, banana, or carrot"))

    # Three words with semicolons...
    words = ('apple,fuji', 'banana', 'carrot')

    eq_(p.join(words),
        "apple,fuji; banana; and carrot",
        msg='{} != {}<-- comma-inclusive 3 words'.format(
            p.join(words), "apple,fuji, banana; and carrot"))

    eq_(p.join(words, final_sep=''),
        "apple,fuji; banana and carrot",
        msg='join({}) == "{}" != "{}"'.format(
            words,
            p.join(words, final_sep=''),
            "apple,fuji) banana and carrot"))

    eq_(p.join(words, final_sep='...'),
        "apple,fuji; banana... and carrot", msg='comma-inclusive 3 words, different final sep')

    eq_(p.join(words, final_sep='...', conj=''),
        "apple,fuji; banana... carrot",
        msg='comma-inclusive 3 words, different final sep, no conjunction')

    eq_(p.join(words, conj='or'),
        "apple,fuji; banana; or carrot", msg='comma-inclusive 3 words, different conjunction')

    # Two words...
    words = ('apple', 'carrot')

    eq_(p.join(words),
        "apple and carrot", msg='plain 2 words')

    eq_(p.join(words, final_sep=''),
        "apple and carrot", msg='2 words, no final sep')

    eq_(p.join(words, final_sep='...'),
        "apple and carrot", msg='2 words, different final sep')

    eq_(p.join(words, final_sep='...', conj=''),
        "apple carrot", msg="join({}, final_sep='...', conj='') == {} != {}".format(
            words, p.join(words, final_sep='...', conj=''), 'apple carrot'))

    eq_(p.join(words, final_sep='...', conj='', conj_spaced=False),
        "applecarrot", msg="join({}, final_sep='...', conj='') == {} != {}".format(
            words, p.join(words, final_sep='...', conj=''), 'applecarrot'))

    eq_(p.join(words, conj='or'),
        "apple or carrot", msg='2 words, different conjunction')

    # One word...
    words = ['carrot']

    eq_(p.join(words),
        "carrot", msg='plain 1 word')

    eq_(p.join(words, final_sep=''),
        "carrot", msg='1 word, no final sep')

    eq_(p.join(words, final_sep='...'),
        "carrot", msg='1 word, different final sep')

    eq_(p.join(words, final_sep='...', conj=''),
        "carrot", msg='1 word, different final sep, no conjunction')

    eq_(p.join(words, conj='or'),
        "carrot", msg='1 word, different conjunction')
