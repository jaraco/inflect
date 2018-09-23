
# use nosetest to run these tests

from nose.tools import eq_

import inflect

FNAME = 'tests/words.txt'
# FNAME = 'tests/list-of-nouns.txt'
# FNAME = '/usr/share/dict/british-english'
# FNAME = 'tricky.txt'


def getwords():
    words = open(FNAME).readlines()
    words = [w.strip() for w in words]
    return words


def test_pl_si():
    p = inflect.engine()
    words = getwords()
    for word in words:
        if word == '':
            continue
        if word[-2:] == "'s":
            continue
#        if word[-1] == 's':
#            continue
        p.classical(all=False)
        yield check_pl_si, p, word
        p.classical(all=True)
        yield check_pl_si, p, word


def check_pl_si(p, word):
    if p.singular_noun(p.plural_noun(word, 2), 1) != word:
        f = open('badsi.txt', 'a')
        f.write('{} {} {}\n'.format(word, p.plural_noun(word, 2),
                                    p.singular_noun(p.plural_noun(word, 2), 1)))
        f.close()
        eq_(p.singular_noun(p.plural_noun(word, 2), 1), word,
            msg='''word==%s
plnoun(%s)==%s
sinoun(%s)==%s''' % (word,
            word, p.plural_noun(word, 2),
            p.plural_noun(word, 2), p.singular_noun(p.plural_noun(word, 2), 1)))
