
# use nosetest to run these tests

from nose.tools import eq_

from .. import inflect

FNAME = 'tests/words.txt'
#FNAME = 'tests/list-of-nouns.txt'
#FNAME = '/usr/share/dict/british-english'
#FNAME = 'tricky.txt'

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
        p.classical(False)
        yield check_pl_si, p, word
        p.classical(True)
        yield check_pl_si, p, word


def check_pl_si(p, word):

 	if p.sinoun(p.plnoun(word, 2), 1) != word:
            f = open('badsi.txt','a')
            f.write('%s %s %s\n' % ( word, p.plnoun(word, 2),
                                   p.sinoun(p.plnoun(word, 2), 1))) 
            f.close()
        eq_(p.sinoun(p.plnoun(word, 2), 1), word,
                             msg='''word==%s
plnoun(%s)==%s
sinoun(%s)==%s''' % (word,
       word, p.plnoun(word, 2),
       p.plnoun(word, 2), p.sinoun(p.plnoun(word, 2), 1),
                             ))


