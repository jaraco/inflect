import os
import io

import six

from nose.tools import eq_, assert_not_equal

import inflect


def is_eq(p, a, b):
    return (p.compare(a, b) or
            p.plnounequal(a, b) or
            p.plverbequal(a, b) or
            p.pladjequal(a, b))


def test_many():
    p = inflect.engine()

    data = get_data()

    for line in data:
        if 'TODO:' in line:
            continue
        try:
            singular, rest = line.split('->', 1)
        except ValueError:
            continue
        singular = singular.strip()
        rest = rest.strip()
        try:
            plural, comment = rest.split('#', 1)
        except ValueError:
            plural = rest.strip()
            comment = ''
        try:
            mod_plural, class_plural = plural.split("|", 1)
            mod_plural = mod_plural.strip()
            class_plural = class_plural.strip()
        except ValueError:
            mod_plural = class_plural = plural.strip()
        if 'verb' in comment.lower():
            is_nv = '_V'
        elif 'noun' in comment.lower():
            is_nv = '_N'
        else:
            is_nv = ''

        p.classical(all=0, names=0)
        mod_PL_V = p.plural_verb(singular)
        mod_PL_N = p.plural_noun(singular)
        mod_PL = p.plural(singular)
        if is_nv == '_V':
            mod_PL_val = mod_PL_V
        elif is_nv == '_N':
            mod_PL_val = mod_PL_N
        else:
            mod_PL_val = mod_PL

        p.classical(all=1)
        class_PL_V = p.plural_verb(singular)
        class_PL_N = p.plural_noun(singular)
        class_PL = p.plural(singular)
        if is_nv == '_V':
            class_PL_val = class_PL_V
        elif is_nv == '_N':
            class_PL_val = class_PL_N
        else:
            class_PL_val = class_PL

        yield check_all, p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural


def check_all(p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural):
    eq_(mod_plural, mod_PL_val)
    eq_(class_plural, class_PL_val)
    eq_(is_eq(p, singular, mod_plural) in ('s:p', 'p:s', 'eq'), True,
        msg='is_eq({},{}) == {} != {}'.format(
            singular,
            mod_plural,
            is_eq(p, singular, mod_plural),
            's:p, p:s or eq'))
    eq_(is_eq(p, mod_plural, singular) in ('p:s', 's:p', 'eq'), True,
        msg='is_eq({},{}) == {} != {}'.format(
            mod_plural,
            singular,
            is_eq(p, mod_plural, singular),
            's:p, p:s or eq'))
    eq_(is_eq(p, singular, class_plural) in ('s:p', 'p:s', 'eq'), True)
    eq_(is_eq(p, class_plural, singular) in ('p:s', 's:p', 'eq'), True)
    assert_not_equal(singular, '')
    eq_(mod_PL_val, mod_PL_val if class_PL_val else '%s|%s' (mod_PL_val, class_PL_val))

    if is_nv != '_V':
        eq_(p.singular_noun(mod_plural, 1), singular,
            msg="p.singular_noun({}) == {} != {}".format(
                mod_plural, p.singular_noun(mod_plural, 1), singular))

        eq_(p.singular_noun(class_plural, 1), singular,
            msg="p.singular_noun({}) == {} != {}".format(
                class_plural, p.singular_noun(class_plural, 1), singular))


def test_def():
    p = inflect.engine()

    p.defnoun("kin", "kine")
    p.defnoun('(.*)x', '$1xen')

    p.defverb('foobar',  'feebar',
              'foobar',  'feebar',
              'foobars', 'feebar')

    p.defadj('red', 'red|gules')

    eq_(p.no("kin", 0), "no kine", msg="kin -> kine (user defined)...")
    eq_(p.no("kin", 1), "1 kin")
    eq_(p.no("kin", 2), "2 kine")

    eq_(p.no("regex", 0), "no regexen", msg="regex -> regexen (user defined)")

    eq_(p.plural("foobar", 2), "feebar", msg="foobar -> feebar (user defined)...")
    eq_(p.plural("foobars", 2), "feebar")

    eq_(p.plural("red", 0), "red", msg="red -> red...")
    eq_(p.plural("red", 1), "red")
    eq_(p.plural("red", 2), "red")
    p.classical(all=True)
    eq_(p.plural("red", 0), "red", msg="red -> gules...")
    eq_(p.plural("red", 1), "red")
    eq_(p.plural("red", 2), "gules")


def test_ordinal():
    p = inflect.engine()
    eq_(p.ordinal(0), "0th", msg="0 -> 0th...")
    eq_(p.ordinal(1), "1st")
    eq_(p.ordinal(2), "2nd")
    eq_(p.ordinal(3), "3rd")
    eq_(p.ordinal(4), "4th")
    eq_(p.ordinal(5), "5th")
    eq_(p.ordinal(6), "6th")
    eq_(p.ordinal(7), "7th")
    eq_(p.ordinal(8), "8th")
    eq_(p.ordinal(9), "9th")
    eq_(p.ordinal(10), "10th")
    eq_(p.ordinal(11), "11th")
    eq_(p.ordinal(12), "12th")
    eq_(p.ordinal(13), "13th")
    eq_(p.ordinal(14), "14th")
    eq_(p.ordinal(15), "15th")
    eq_(p.ordinal(16), "16th")
    eq_(p.ordinal(17), "17th")
    eq_(p.ordinal(18), "18th")
    eq_(p.ordinal(19), "19th")
    eq_(p.ordinal(20), "20th")
    eq_(p.ordinal(21), "21st")
    eq_(p.ordinal(22), "22nd")
    eq_(p.ordinal(23), "23rd")
    eq_(p.ordinal(24), "24th")
    eq_(p.ordinal(100), "100th")
    eq_(p.ordinal(101), "101st")
    eq_(p.ordinal(102), "102nd")
    eq_(p.ordinal(103), "103rd")
    eq_(p.ordinal(104), "104th")

    eq_(p.ordinal('zero'), "zeroth", msg="zero -> zeroth...")
    eq_(p.ordinal('one'), "first")
    eq_(p.ordinal('two'), "second")
    eq_(p.ordinal('three'), "third")
    eq_(p.ordinal('four'), "fourth")
    eq_(p.ordinal('five'), "fifth")
    eq_(p.ordinal('six'), "sixth")
    eq_(p.ordinal('seven'), "seventh")
    eq_(p.ordinal('eight'), "eighth")
    eq_(p.ordinal('nine'), "ninth")
    eq_(p.ordinal('ten'), "tenth")
    eq_(p.ordinal('eleven'), "eleventh")
    eq_(p.ordinal('twelve'), "twelfth")
    eq_(p.ordinal('thirteen'), "thirteenth")
    eq_(p.ordinal('fourteen'), "fourteenth")
    eq_(p.ordinal('fifteen'), "fifteenth")
    eq_(p.ordinal('sixteen'), "sixteenth")
    eq_(p.ordinal('seventeen'), "seventeenth")
    eq_(p.ordinal('eighteen'), "eighteenth")
    eq_(p.ordinal('nineteen'), "nineteenth")
    eq_(p.ordinal('twenty'), "twentieth")
    eq_(p.ordinal('twenty-one'), "twenty-first")
    eq_(p.ordinal('twenty-two'), "twenty-second")
    eq_(p.ordinal('twenty-three'), "twenty-third")
    eq_(p.ordinal('twenty-four'), "twenty-fourth")
    eq_(p.ordinal('one hundred'), "one hundredth")
    eq_(p.ordinal('one hundred and one'), "one hundred and first")
    eq_(p.ordinal('one hundred and two'), "one hundred and second")
    eq_(p.ordinal('one hundred and three'), "one hundred and third")
    eq_(p.ordinal('one hundred and four'), "one hundred and fourth")


def test_prespart():
    p = inflect.engine()
    eq_(p.present_participle("sees"), "seeing", msg="sees -> seeing...")
    eq_(p.present_participle("eats"), "eating")
    eq_(p.present_participle("bats"), "batting")
    eq_(p.present_participle("hates"), "hating")
    eq_(p.present_participle("spies"), "spying")
    eq_(p.present_participle("skis"), "skiing")


def test_inflect_on_tuples():
    p = inflect.engine()
    eq_(p.inflect("plural(egg, ('a', 'b', 'c')"), "eggs")
    eq_(p.inflect("plural_noun(egg, ('a', 'b', 'c'))"), "eggs")
    eq_(p.inflect("plural_adj(a, ('a', 'b', 'c'))"), "some")
    eq_(p.inflect("plural_verb(was, ('a', 'b', 'c'))"), "were")
    eq_(p.inflect("singular_noun(eggs, ('a', 'b', 'c'))"), "eggs")
    eq_(p.inflect("an(error, ('a', 'b', 'c'))"), " ('a', 'b', 'c') error")
    eq_(p.inflect("number_to_words((10, 20))"), 'one thousand and twenty')


def get_data():
    filename = os.path.join(os.path.dirname(__file__), 'inflections.txt')
    with io.open(filename) as strm:
        return list(map(six.text_type.strip, strm))
