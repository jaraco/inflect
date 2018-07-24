#!/usr/bin/python

import unittest

from inflect import (BadChunkingOptionError, NumOutOfRangeError, BadNumValueError, BadGenderError,
                     UnknownClassicalModeError)
import inflect


class test(unittest.TestCase):
    def TODO(self, ans, answer_wanted,
             answer_gives_now="default_that_will_never_occur__can't_use_None"
                              "_as_that_is_a_possible_valid_value"):
        '''
        make this test for future testing

        so can easily rename these to assertEqual when code ready
        '''
        if ans == answer_wanted:
            print('test unexpectedly passed!: {} == {}'.format(ans, answer_wanted))
        if answer_gives_now != ("default_that_will_never_occur__can't_use_None"
                                "_as_that_is_a_possible_valid_value"):
            self.assertEqual(ans, answer_gives_now)

    def test_enclose(self):
        # def enclose
        self.assertEqual(inflect.enclose("test"), "(?:test)")

    def test_joinstem(self):
        # def joinstem
        self.assertEqual(inflect.joinstem(-2, ["ephemeris", "iris", ".*itis"]),
                         '(?:ephemer|ir|.*it)')

    def test_classical(self):
        # classical dicts
        self.assertEqual(set(inflect.def_classical.keys()), set(inflect.all_classical.keys()))
        self.assertEqual(set(inflect.def_classical.keys()), set(inflect.no_classical.keys()))

        # def classical
        p = inflect.engine()
        self.assertEqual(p.classical_dict, inflect.def_classical)

        p.classical()
        self.assertEqual(p.classical_dict, inflect.all_classical)

        self.assertRaises(TypeError, p.classical, 0)
        self.assertRaises(TypeError, p.classical, 1)
        self.assertRaises(TypeError, p.classical, 'names')
        self.assertRaises(TypeError, p.classical, 'names', 'zero')
        self.assertRaises(TypeError, p.classical, 'all')

        p.classical(all=False)
        self.assertEqual(p.classical_dict, inflect.no_classical)

        p.classical(names=True, zero=True)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=1, zero=1))
        self.assertEqual(p.classical_dict, mydict)

        p.classical(all=True)
        self.assertEqual(p.classical_dict, inflect.all_classical)

        p.classical(all=False)
        p.classical(names=True, zero=True)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=True, zero=True))
        self.assertEqual(p.classical_dict, mydict)

        p.classical(all=False)
        p.classical(names=True, zero=False)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=True, zero=False))
        self.assertEqual(p.classical_dict, mydict)

        self.assertRaises(UnknownClassicalModeError, p.classical, bogus=True)

    def test_num(self):
        # def num
        p = inflect.engine()
        self.assertTrue(p.persistent_count is None)

        p.num()
        self.assertTrue(p.persistent_count is None)

        ret = p.num(3)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.num()
        ret = p.num("3")
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.num()
        ret = p.num(count=3, show=1)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.num()
        ret = p.num(count=3, show=0)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '')

        self.assertRaises(BadNumValueError, p.num, 'text')

    def test_inflect(self):
        p = inflect.engine()
        for txt, ans in (
            ("num(1)", "1"),
            ("num(1,0)", "1"),
            ("num(1,1)", "1"),
            ("num(1)   ", "1   "),
            ("   num(1)   ", "   1   "),
            ("num(3) num(1)", "3 1"),
        ):
            self.assertEqual(p.inflect(txt), ans, msg='p.inflect("{}") != "{}"'.format(txt, ans))

        for txt, ans in (
            ("plural(rock)", "rocks"),
            ("plural(rock)  plural(child)", "rocks  children"),
            ("num(2) plural(rock)  plural(child)", "2 rocks  children"),

            ("plural(rock) plural_noun(rock) plural_verb(rocks) plural_adj(big) a(ant)",
             "rocks rocks rock big an ant"),

            ("an(rock) no(cat) ordinal(3) number_to_words(1234) present_participle(runs)",
             "a rock no cats 3rd one thousand, two hundred and thirty-four running"),

            # TODO: extra space when space before number. Is this desirable?
            ("a(cat,0) a(cat,1) a(cat,2) a(cat, 2)", "0 cat a cat 2 cat  2 cat"),
        ):
            self.assertEqual(p.inflect(txt), ans, msg='p.inflect("{}") != "{}"'.format(txt, ans))

    def test_user_input_fns(self):
        p = inflect.engine()

        self.assertEqual(p.pl_sb_user_defined, [])
        p.defnoun('VAX', 'VAXen')
        self.assertEqual(p.plural('VAX'), 'VAXEN')
        self.assertEqual(p.pl_sb_user_defined, ['VAX', 'VAXen'])

        self.assertTrue(p.ud_match('word', p.pl_sb_user_defined)
                        is None)
        self.assertEqual(p.ud_match('VAX', p.pl_sb_user_defined),
                         'VAXen')
        self.assertTrue(p.ud_match('VVAX', p.pl_sb_user_defined)
                        is None)

        p.defnoun('cow', 'cows|kine')
        self.assertEqual(p.plural('cow'), 'cows')
        p.classical()
        self.assertEqual(p.plural('cow'), 'kine')

        self.assertEqual(p.ud_match('cow', p.pl_sb_user_defined),
                         'cows|kine')

        p.defnoun('(.+i)o', r'$1i')
        self.assertEqual(p.plural('studio'), 'studii')
        self.assertEqual(p.ud_match('studio', p.pl_sb_user_defined),
                         'studii')

        p.defnoun('aviatrix', 'aviatrices')
        self.assertEqual(p.plural('aviatrix'), 'aviatrices')
        self.assertEqual(p.ud_match('aviatrix', p.pl_sb_user_defined),
                         'aviatrices')
        p.defnoun('aviatrix', 'aviatrixes')
        self.assertEqual(p.plural('aviatrix'), 'aviatrixes')
        self.assertEqual(p.ud_match('aviatrix', p.pl_sb_user_defined),
                         'aviatrixes')
        p.defnoun('aviatrix', None)
        self.assertEqual(p.plural('aviatrix'), 'aviatrices')
        self.assertEqual(p.ud_match('aviatrix', p.pl_sb_user_defined),
                         None)

        p.defnoun('(cat)', r'$1s')
        self.assertEqual(p.plural('cat'), 'cats')

        inflect.STDOUT_ON = False
        self.assertRaises(inflect.BadUserDefinedPatternError, p.defnoun, '(??', None)
        inflect.STDOUT_ON = True

        p.defnoun(None, '')  # check None doesn't crash it

        # defverb
        p.defverb('will', 'shall',
                  'will', 'will',
                  'will', 'will')
        self.assertEqual(p.ud_match('will', p.pl_v_user_defined),
                         'will')
        self.assertEqual(p.plural('will'), 'will')
        # TODO: will -> shall. Tests below fail
        self.TODO(p.compare('will', 'shall'), 's:p')
        self.TODO(p.compare_verbs('will', 'shall'), 's:p')

        # defadj
        p.defadj('hir', 'their')
        self.assertEqual(p.plural('hir'), 'their')
        self.assertEqual(p.ud_match('hir', p.pl_adj_user_defined), 'their')

        # defa defan
        p.defa('h')
        self.assertEqual(p.a('h'), 'a h')
        self.assertEqual(p.ud_match('h', p.A_a_user_defined), 'a')

        p.defan('horrendous.*')
        self.assertEqual(p.a('horrendously'), 'an horrendously')
        self.assertEqual(p.ud_match('horrendously', p.A_a_user_defined), 'an')

    def test_postprocess(self):
        p = inflect.engine()
        for orig, infl, txt in (
            ('cow', 'cows', 'cows'),
            ('I', 'we', 'we'),
            ('COW', 'cows', 'COWS'),
            ('Cow', 'cows', 'Cows'),
            ('cow', 'cows|kine', 'cows'),
        ):
            self.assertEqual(p.postprocess(orig, infl), txt)

        p.classical()
        self.assertEqual(p.postprocess('cow', 'cows|kine'), 'kine')

    def test_partition_word(self):
        p = inflect.engine()
        for txt, part in (
            (' cow ', (' ', 'cow', ' ')),
            ('cow', ('', 'cow', '')),
            ('   cow', ('   ', 'cow', '')),
            ('cow   ', ('', 'cow', '   ')),
            ('  cow   ', ('  ', 'cow', '   ')),
            ('', ('', '', '')),
            ('bottle of beer', ('', 'bottle of beer', '')),
            # spaces give weird results
            # (' '),('', ' ', '')),
            # ('  '),(' ', ' ', '')),
            # ('   '),('  ', ' ', '')),
        ):
            self.assertEqual(p.partition_word(txt), part)

    def test_pl(self):
        p = inflect.engine()
        for fn, sing, plur in (
            (p.plural, '', ''),
            (p.plural, 'cow', 'cows'),
            (p.plural, 'thought', 'thoughts'),
            (p.plural, 'mouse', 'mice'),
            (p.plural, 'knife', 'knives'),
            (p.plural, 'knifes', 'knife'),
            (p.plural, ' cat  ', ' cats  '),
            (p.plural, 'court martial', 'courts martial'),
            (p.plural, 'a', 'some'),
            (p.plural, 'carmen', 'carmina'),
            (p.plural, 'quartz', 'quartzes'),
            (p.plural, 'care', 'cares'),
            (p.plural_noun, '', ''),
            (p.plural_noun, 'cow', 'cows'),
            (p.plural_noun, 'thought', 'thoughts'),
            (p.plural_noun, 'snooze', 'snoozes'),
            (p.plural_verb, '', ''),
            (p.plural_verb, 'runs', 'run'),
            (p.plural_verb, 'thought', 'thought'),
            (p.plural_verb, 'eyes', 'eye'),
            (p.plural_adj, '', ''),
            (p.plural_adj, 'a', 'some'),
            (p.plural_adj, 'this', 'these'),
            (p.plural_adj, 'that', 'those'),
            (p.plural_adj, 'my', 'our'),
            (p.plural_adj, "cat's", "cats'"),
            (p.plural_adj, "child's", "children's"),
        ):
            self.assertEqual(fn(sing), plur,
                             msg='{}("{}") == "{}" != "{}"'.format(
                                 fn.__name__, sing, fn(sing), plur))

        for sing, num, plur in (
            ('cow', 1, 'cow'),
            ('cow', 2, 'cows'),
            ('cow', 'one', 'cow'),
            ('cow', 'each', 'cow'),
            ('cow', 'two', 'cows'),
            ('cow', 0, 'cows'),
            ('cow', 'zero', 'cows'),
            ('runs', 0, 'run'),
            ('runs', 1, 'runs'),
            ('am', 0, 'are'),
        ):
            self.assertEqual(p.plural(sing, num), plur)

        p.classical(zero=True)
        self.assertEqual(p.plural('cow', 0), 'cow')
        self.assertEqual(p.plural('cow', 'zero'), 'cow')
        self.assertEqual(p.plural('runs', 0), 'runs')
        self.assertEqual(p.plural('am', 0), 'am')
        self.assertEqual(p.plural_verb('runs', 1), 'runs')

        self.assertEqual(p.plural('die'), 'dice')
        self.assertEqual(p.plural_noun('die'), 'dice')

    def test_sinoun(self):
        p = inflect.engine()
        for sing, plur in (
            ('cat', 'cats'),
            ('die', 'dice'),
            ('status', 'status'),
            ('hiatus', 'hiatus'),
            ('goose', 'geese'),
        ):
            self.assertEqual(p.singular_noun(plur), sing)
            self.assertEqual(p.inflect('singular_noun(%s)' % plur), sing)

        self.assertEqual(p.singular_noun('cats', count=2), 'cats')

        self.assertEqual(p.singular_noun('zombies'), 'zombie')

        self.assertEqual(p.singular_noun('shoes'), 'shoe')

        self.assertEqual(p.singular_noun('Matisses'), 'Matisse')
        self.assertEqual(p.singular_noun('bouillabaisses'), 'bouillabaisse')

        self.assertEqual(p.singular_noun('quartzes'), 'quartz')

        self.assertEqual(p.singular_noun('Nietzsches'), 'Nietzsche')
        self.assertEqual(p.singular_noun('aches'), 'ache')

        self.assertEqual(p.singular_noun('Clives'), 'Clive')
        self.assertEqual(p.singular_noun('weaves'), 'weave')

    def test_gender(self):
        p = inflect.engine()
        p.gender('feminine')
        for sing, plur in (
            ('she', 'they'),
            ('herself', 'themselves'),
            ('hers', 'theirs'),
            ('to her', 'to them'),
            ('to herself', 'to themselves'),
        ):
            self.assertEqual(p.singular_noun(plur), sing,
                             "singular_noun({}) == {} != {}".format(
                                plur,
                                p.singular_noun(plur),
                                sing))
            self.assertEqual(p.inflect('singular_noun(%s)' % plur), sing)

        p.gender('masculine')
        for sing, plur in (
            ('he', 'they'),
            ('himself', 'themselves'),
            ('his', 'theirs'),
            ('to him', 'to them'),
            ('to himself', 'to themselves'),
        ):
            self.assertEqual(p.singular_noun(plur), sing,
                             "singular_noun({}) == {} != {}".format(
                                plur,
                                p.singular_noun(plur),
                                sing))
            self.assertEqual(p.inflect('singular_noun(%s)' % plur), sing)

        p.gender('gender-neutral')
        for sing, plur in (
            ('they', 'they'),
            ('themself', 'themselves'),
            ('theirs', 'theirs'),
            ('to them', 'to them'),
            ('to themself', 'to themselves'),
        ):
            self.assertEqual(p.singular_noun(plur), sing,
                             "singular_noun({}) == {} != {}".format(
                                plur,
                                p.singular_noun(plur),
                                sing))
            self.assertEqual(p.inflect('singular_noun(%s)' % plur), sing)

        p.gender('neuter')
        for sing, plur in (
            ('it', 'they'),
            ('itself', 'themselves'),
            ('its', 'theirs'),
            ('to it', 'to them'),
            ('to itself', 'to themselves'),
        ):
            self.assertEqual(p.singular_noun(plur), sing,
                             "singular_noun({}) == {} != {}".format(
                                plur,
                                p.singular_noun(plur),
                                sing))
            self.assertEqual(p.inflect('singular_noun(%s)' % plur), sing)

        self.assertRaises(BadGenderError, p.gender, 'male')

        for sing, plur, gen in (
            ('it', 'they', 'neuter'),
            ('she', 'they', 'feminine'),
            ('he', 'they', 'masculine'),
            ('they', 'they', 'gender-neutral'),
            ('she or he', 'they', 'feminine or masculine'),
            ('he or she', 'they', 'masculine or feminine'),
        ):
            self.assertEqual(p.singular_noun(plur, gender=gen), sing)

        with self.assertRaises(BadGenderError):
            p.singular_noun('cats', gender='unknown gender')

    def test_plequal(self):
        p = inflect.engine()
        for fn, sing, plur, res in (
            (p.compare, 'index', 'index', 'eq'),
            (p.compare, 'index', 'indexes', 's:p'),
            (p.compare, 'index', 'indices', 's:p'),
            (p.compare, 'indexes', 'index', 'p:s'),
            (p.compare, 'indices', 'index', 'p:s'),
            (p.compare, 'indices', 'indexes', 'p:p'),
            (p.compare, 'indexes', 'indices', 'p:p'),
            (p.compare, 'indices', 'indices', 'eq'),
            (p.compare, 'opuses', 'opera', 'p:p'),
            (p.compare, 'opera', 'opuses', 'p:p'),
            (p.compare, 'brothers', 'brethren', 'p:p'),
            (p.compare, 'cats', 'cats', 'eq'),
            (p.compare, 'base', 'basis', False),
            (p.compare, 'syrinx', 'syringe', False),
            (p.compare, 'she', 'he', False),
            (p.compare, 'opus', 'operas', False),
            (p.compare, 'taxi', 'taxes', False),
            (p.compare, 'time', 'Times', False),
            (p.compare, 'time'.lower(), 'Times'.lower(), 's:p'),
            (p.compare, 'courts martial', 'court martial', 'p:s'),
            (p.compare, 'my', 'my', 'eq'),
            (p.compare, 'my', 'our', 's:p'),
            (p.compare, 'our', 'our', 'eq'),
            (p.compare_nouns, 'index', 'index', 'eq'),
            (p.compare_nouns, 'index', 'indexes', 's:p'),
            (p.compare_nouns, 'index', 'indices', 's:p'),
            (p.compare_nouns, 'indexes', 'index', 'p:s'),
            (p.compare_nouns, 'indices', 'index', 'p:s'),
            (p.compare_nouns, 'indices', 'indexes', 'p:p'),
            (p.compare_nouns, 'indexes', 'indices', 'p:p'),
            (p.compare_nouns, 'indices', 'indices', 'eq'),
            (p.compare_verbs, 'runs', 'runs', 'eq'),
            (p.compare_verbs, 'runs', 'run', 's:p'),
            (p.compare_verbs, 'run', 'run', 'eq'),
            (p.compare_adjs, 'my', 'my', 'eq'),
            (p.compare_adjs, 'my', 'our', 's:p'),
            (p.compare_adjs, 'our', 'our', 'eq'),
        ):
            self.assertEqual(fn(sing, plur), res)

        for fn, sing, plur, res, badres in (
            (p.compare, "dresses's", "dresses'", 'p:p', 'p:s'),  # TODO: should return p:p
            (p.compare_adjs, "dresses's", "dresses'", 'p:p', False),  # TODO: should return p:p

            # TODO: future: support different singulars one day.
            (p.compare, "dress's", "dress'", 's:s', 'p:s'),
            (p.compare_adjs, "dress's", "dress'", 's:s', False),
            (p.compare, "Jess's", "Jess'", 's:s', 'p:s'),
            (p.compare_adjs, "Jess's", "Jess'", 's:s', False),
        ):
            self.TODO(fn(sing, plur), res, badres)

        # TODO: pass upstream. multiple adjective plurals not supported
        self.assertEqual(p.compare('your', 'our'), False)
        p.defadj('my', 'our|your')  # what's ours is yours
        self.TODO(p.compare('your', 'our'), 'p:p')

    def test__pl_reg_plurals(self):
        p = inflect.engine()
        for pair, stems, end1, end2, ans in (
            ('indexes|indices', 'dummy|ind', 'exes', 'ices', True),
            ('indexes|robots', 'dummy|ind', 'exes', 'ices', False),
            ('beaus|beaux', '.*eau', 's', 'x', True),
        ):
            self.assertEqual(p._pl_reg_plurals(pair, stems, end1, end2), ans)

    def test__pl_check_plurals_N(self):
        p = inflect.engine()
        self.assertEqual(p._pl_check_plurals_N('index', 'indices'), False)
        self.assertEqual(p._pl_check_plurals_N('indexes', 'indices'), True)
        self.assertEqual(p._pl_check_plurals_N('indices', 'indexes'), True)
        self.assertEqual(p._pl_check_plurals_N('stigmata', 'stigmas'), True)
        self.assertEqual(p._pl_check_plurals_N('phalanxes', 'phalanges'), True)

    def test__pl_check_plurals_adj(self):
        p = inflect.engine()
        self.assertEqual(p._pl_check_plurals_adj("indexes's", "indices's"), True)
        self.assertEqual(p._pl_check_plurals_adj("indices's", "indexes's"), True)
        self.assertEqual(p._pl_check_plurals_adj("indexes'", "indices's"), True)
        self.assertEqual(p._pl_check_plurals_adj("indexes's", "indices'"), True)
        self.assertEqual(p._pl_check_plurals_adj("indexes's", "indexes's"), False)
        self.assertEqual(p._pl_check_plurals_adj("dogmas's", "dogmata's"), True)
        self.assertEqual(p._pl_check_plurals_adj("dogmas'", "dogmata'"), True)
        self.assertEqual(p._pl_check_plurals_adj("indexes'", "indices'"), True)

    def test_count(self):
        p = inflect.engine()
        for txt, num in (
            (1, 1),
            (2, 2),
            (0, 2),
            (87, 2),
            (-7, 2),
            ('1', 1),
            ('2', 2),
            ('0', 2),
            ('no', 2),
            ('zero', 2),
            ('nil', 2),
            ('a', 1),
            ('an', 1),
            ('one', 1),
            ('each', 1),
            ('every', 1),
            ('this', 1),
            ('that', 1),
            ('dummy', 2),
        ):
            self.assertEqual(p.get_count(txt), num)

        self.assertEqual(p.get_count(), '')
        p.num(3)
        self.assertEqual(p.get_count(), 2)

    def test__plnoun(self):
        p = inflect.engine()
        for sing, plur in (
            ('', ''),
            ('tuna', 'tuna'),
            ('TUNA', 'TUNA'),
            ('swordfish', 'swordfish'),
            ('Governor General', 'Governors General'),
            ('Governor-General', 'Governors-General'),
            ('Major General', 'Major Generals'),
            ('Major-General', 'Major-Generals'),
            ('mother in law', 'mothers in law'),
            ('mother-in-law', 'mothers-in-law'),
            ('about me', 'about us'),
            ('to it', 'to them'),
            ('from it', 'from them'),
            ('with it', 'with them'),
            ('I', 'we'),
            ('you', 'you'),
            ('me', 'us'),
            ('mine', 'ours'),
            ('child', 'children'),
            ('brainchild', 'brainchilds'),
            ('human', 'humans'),
            ('soliloquy', 'soliloquies'),

            ('chairwoman', 'chairwomen'),
            ('goose', 'geese'),
            ('tooth', 'teeth'),
            ('foot', 'feet'),
            ('forceps', 'forceps'),
            ('protozoon', 'protozoa'),
            ('czech', 'czechs'),
            ('codex', 'codices'),
            ('radix', 'radices'),
            ('bacterium', 'bacteria'),
            ('alumnus', 'alumni'),
            ('criterion', 'criteria'),
            ('alumna', 'alumnae'),

            ('bias', 'biases'),
            ('quiz', 'quizzes'),
            ('fox', 'foxes'),

            ('shelf', 'shelves'),
            ('leaf', 'leaves'),
            ('midwife', 'midwives'),
            ('scarf', 'scarves'),

            ('key', 'keys'),
            ('Sally', 'Sallys'),
            ('sally', 'sallies'),

            ('ado', 'ados'),
            ('auto', 'autos'),
            ('alto', 'altos'),
            ('zoo', 'zoos'),
            ('tomato', 'tomatoes'),
        ):
            self.assertEqual(p._plnoun(sing), plur,
                             msg='p._plnoun("{}") == {} != "{}"'.format(
                                 sing, p._plnoun(sing), plur))

            self.assertEqual(p._sinoun(plur), sing,
                             msg='p._sinoun("{}") != "{}"'.format(plur, sing))

        # words where forming singular is ambiguious or not attempted
        for sing, plur in (
            ('son of a gun', 'sons of guns'),
            ('son-of-a-gun', 'sons-of-guns'),
            ('basis', 'bases'),
            ('Jess', 'Jesses'),
        ):
            self.assertEqual(p._plnoun(sing), plur,
                             msg='p._plnoun("{}") != "{}"'.format(sing, plur))

        for sing, plur in (
            # TODO: does not keep case
            ('about ME', 'about US'),
            # TODO: does not keep case
            ('YOU', 'YOU'),
        ):
            self.TODO(p._plnoun(sing), plur)

        p.num(1)
        self.assertEqual(p._plnoun('cat'), 'cat')
        p.num(3)

        p.classical(herd=True)
        self.assertEqual(p._plnoun('swine'), 'swine')
        p.classical(herd=False)
        self.assertEqual(p._plnoun('swine'), 'swines')
        p.classical(persons=True)
        self.assertEqual(p._plnoun('chairperson'), 'chairpersons')
        p.classical(persons=False)
        self.assertEqual(p._plnoun('chairperson'), 'chairpeople')
        p.classical(ancient=True)
        self.assertEqual(p._plnoun('formula'), 'formulae')
        p.classical(ancient=False)
        self.assertEqual(p._plnoun('formula'), 'formulas')

        p.classical()
        for sing, plur in (
            ('matrix', 'matrices'),
            ('gateau', 'gateaux'),
            ('millieu', 'millieux'),
            ('syrinx', 'syringes'),

            ('stamen', 'stamina'),
            ('apex', 'apices'),
            ('appendix', 'appendices'),
            ('maximum', 'maxima'),
            ('focus', 'foci'),
            ('status', 'status'),
            ('aurora', 'aurorae'),
            ('soma', 'somata'),
            ('iris', 'irides'),
            ('solo', 'soli'),
            ('oxymoron', 'oxymora'),
            ('goy', 'goyim'),
            ('afrit', 'afriti'),
        ):
            self.assertEqual(p._plnoun(sing), plur)

        # p.classical(0)
        # p.classical('names')
        # clasical now back to the default mode

    def test_classical_pl(self):
        p = inflect.engine()
        p.classical()
        for sing, plur in (
            ('brother', 'brethren'),
            ('dogma', 'dogmata'),
        ):
            self.assertEqual(p.plural(sing), plur)

    def test__pl_special_verb(self):
        p = inflect.engine()
        self.assertEqual(p._pl_special_verb(''), False)
        self.assertEqual(p._pl_special_verb('am'), 'are')
        self.assertEqual(p._pl_special_verb('am', 0), 'are')
        self.assertEqual(p._pl_special_verb('runs', 0), 'run')
        p.classical(zero=True)
        self.assertEqual(p._pl_special_verb('am', 0), False)
        self.assertEqual(p._pl_special_verb('am', 1), 'am')
        self.assertEqual(p._pl_special_verb('am', 2), 'are')
        self.assertEqual(p._pl_special_verb('runs', 0), False)
        self.assertEqual(p._pl_special_verb('am going to'), 'are going to')
        self.assertEqual(p._pl_special_verb('did'), 'did')
        self.assertEqual(p._pl_special_verb("wasn't"), "weren't")
        self.assertEqual(p._pl_special_verb("shouldn't"), "shouldn't")
        self.assertEqual(p._pl_special_verb('bias'), False)
        self.assertEqual(p._pl_special_verb('news'), False)
        self.assertEqual(p._pl_special_verb('Jess'), False)
        self.assertEqual(p._pl_special_verb(' '), False)
        self.assertEqual(p._pl_special_verb('brushes'), 'brush')
        self.assertEqual(p._pl_special_verb('fixes'), 'fix')
        self.assertEqual(p._pl_special_verb('quizzes'), 'quiz')
        self.assertEqual(p._pl_special_verb('fizzes'), 'fizz')
        self.assertEqual(p._pl_special_verb('dresses'), 'dress')
        self.assertEqual(p._pl_special_verb('flies'), 'fly')
        self.assertEqual(p._pl_special_verb('canoes'), 'canoe')
        self.assertEqual(p._pl_special_verb('horseshoes'), 'horseshoe')
        self.assertEqual(p._pl_special_verb('does'), 'do')
        # TODO: what's a real word to test this case?
        self.assertEqual(p._pl_special_verb('zzzoes'), 'zzzo')
        self.assertEqual(p._pl_special_verb('runs'), 'run')

    def test__pl_general_verb(self):
        p = inflect.engine()
        self.assertEqual(p._pl_general_verb('acts'), 'act')
        self.assertEqual(p._pl_general_verb('act'), 'act')
        self.assertEqual(p._pl_general_verb('saw'), 'saw')
        self.assertEqual(p._pl_general_verb('runs', 1), 'runs')

    def test__pl_special_adjective(self):
        p = inflect.engine()
        self.assertEqual(p._pl_special_adjective('a'), 'some')
        self.assertEqual(p._pl_special_adjective('my'), 'our')
        self.assertEqual(p._pl_special_adjective("John's"), "Johns'")
        # TODO: original can't handle this. should we handle it?
        self.TODO(p._pl_special_adjective("JOHN's"), "JOHNS'")
        # TODO: can't handle capitals
        self.TODO(p._pl_special_adjective("JOHN'S"), "JOHNS'")
        self.TODO(p._pl_special_adjective("TUNA'S"), "TUNA'S")
        self.assertEqual(p._pl_special_adjective("tuna's"), "tuna's")
        self.assertEqual(p._pl_special_adjective("TUNA's"), "TUNA's")
        self.assertEqual(p._pl_special_adjective("bad"), False)

    def test_a(self):
        p = inflect.engine()
        for sing, plur in (
            ('cat', 'a cat'),
            ('euphemism', 'a euphemism'),
            ('Euler number', 'an Euler number'),
            ('hour', 'an hour'),
            ('houri', 'a houri'),
            ('nth', 'an nth'),
            ('rth', 'an rth'),
            ('sth', 'an sth'),
            ('xth', 'an xth'),
            ('ant', 'an ant'),
            ('book', 'a book'),
            ('RSPCA', 'an RSPCA'),
            ('SONAR', 'a SONAR'),
            ('FJO', 'a FJO'),
            ('FJ', 'an FJ'),
            ('NASA', 'a NASA'),
            ('UN', 'a UN'),
            ('yak', 'a yak'),
            ('yttrium', 'an yttrium'),
            ('a elephant', 'an elephant'),
            ('a giraffe', 'a giraffe'),
            ('an ewe', 'a ewe'),
            ('a orangutan', 'an orangutan'),
            ('R.I.P.', 'an R.I.P.'),
            ('C.O.D.', 'a C.O.D.'),
            ('e-mail', 'an e-mail'),
            ('X-ray', 'an X-ray'),
            ('T-square', 'a T-square'),
            ('LCD', 'an LCD'),
            ('XML', 'an XML'),
            ('YWCA', 'a YWCA'),
            ('LED', 'a LED'),
            ('OPEC', 'an OPEC'),
            ('FAQ', 'a FAQ'),
            ('UNESCO', 'a UNESCO'),
            ('a', 'an a'),
            ('an', 'an an'),
            ('an ant', 'an ant'),
            ('a cat', 'a cat'),
            ('an cat', 'a cat'),
            ('a ant', 'an ant'),
        ):
            self.assertEqual(p.a(sing), plur)

        self.assertEqual(p.a('cat', 1), 'a cat')
        self.assertEqual(p.a('cat', 2), '2 cat')

        self.assertEqual(p.a, p.an)
        self.assertEqual(p.a(''), '')

    def test_no(self):
        p = inflect.engine()
        self.assertEqual(p.no('cat'), 'no cats')
        self.assertEqual(p.no('cat', count=3), '3 cats')
        self.assertEqual(p.no('cat', count='three'), 'three cats')
        self.assertEqual(p.no('cat', count=1), '1 cat')
        self.assertEqual(p.no('cat', count='one'), 'one cat')
        self.assertEqual(p.no('mouse'), 'no mice')
        p.num(3)
        self.assertEqual(p.no('cat'), '3 cats')

    def test_prespart(self):
        p = inflect.engine()
        for sing, plur in (
            ('runs', 'running'),
            ('dies', 'dying'),
            ('glues', 'gluing'),
            ('eyes', 'eying'),
            ('skis', 'skiing'),
            ('names', 'naming'),
            ('sees', 'seeing'),
            ('hammers', 'hammering'),
            ('bats', 'batting'),
            ('eats', 'eating'),
            ('loves', 'loving'),
            ('spies', 'spying'),
        ):
            self.assertEqual(p.present_participle(sing), plur)

        self.assertEqual(p.present_participle('hoes'), 'hoeing')
        self.assertEqual(p.present_participle('alibis'), 'alibiing')
        self.assertEqual(p.present_participle('is'), 'being')
        self.assertEqual(p.present_participle('are'), 'being')
        self.assertEqual(p.present_participle('had'), 'having')
        self.assertEqual(p.present_participle('has'), 'having')

    def test_ordinal(self):
        p = inflect.engine()
        for num, numord in (
            ('1', '1st'),
            ('2', '2nd'),
            ('3', '3rd'),
            ('4', '4th'),
            ('10', '10th'),
            ('28', '28th'),
            ('100', '100th'),
            ('101', '101st'),
            ('1000', '1000th'),
            ('1001', '1001st'),
            ('0', '0th'),
            ('one', 'first'),
            ('two', 'second'),
            ('four', 'fourth'),
            ('twenty', 'twentieth'),
            ('one hundered', 'one hunderedth'),
            ('one hundered and one', 'one hundered and first'),
            ('zero', 'zeroth'),
            ('n', 'nth'),  # bonus!
        ):
            self.assertEqual(p.ordinal(num), numord)

    def test_millfn(self):
        p = inflect.engine()
        millfn = p.millfn
        self.assertEqual(millfn(1), ' thousand')
        self.assertEqual(millfn(2), ' million')
        self.assertEqual(millfn(3), ' billion')
        self.assertEqual(millfn(0), ' ')
        self.assertEqual(millfn(11), ' decillion')
        inflect.STDOUT_ON = False
        self.assertRaises(NumOutOfRangeError, millfn, 12)
        inflect.STDOUT_ON = True

    def test_unitfn(self):
        p = inflect.engine()
        unitfn = p.unitfn
        self.assertEqual(unitfn(1, 2), 'one million')
        self.assertEqual(unitfn(1, 3), 'one billion')
        self.assertEqual(unitfn(5, 3), 'five billion')
        self.assertEqual(unitfn(5, 0), 'five ')
        self.assertEqual(unitfn(0, 0), ' ')

    def test_tenfn(self):
        p = inflect.engine()
        tenfn = p.tenfn
        self.assertEqual(tenfn(3, 1, 2), 'thirty-one million')
        self.assertEqual(tenfn(3, 0, 2), 'thirty million')
        self.assertEqual(tenfn(0, 1, 2), 'one million')
        self.assertEqual(tenfn(1, 1, 2), 'eleven million')
        self.assertEqual(tenfn(1, 0, 2), 'ten million')
        self.assertEqual(tenfn(1, 0, 0), 'ten ')
        self.assertEqual(tenfn(0, 0, 0), ' ')

    def test_hundfn(self):
        p = inflect.engine()
        hundfn = p.hundfn
        p.number_args = dict(andword='and')
        self.assertEqual(hundfn(4, 3, 1, 2), 'four hundred and thirty-one  million, ')
        self.assertEqual(hundfn(4, 0, 0, 2), 'four hundred  million, ')
        self.assertEqual(hundfn(4, 0, 5, 2), 'four hundred and five  million, ')
        self.assertEqual(hundfn(0, 3, 1, 2), 'thirty-one  million, ')
        self.assertEqual(hundfn(0, 0, 7, 2), 'seven  million, ')

    def test_enword(self):
        p = inflect.engine()
        enword = p.enword
        self.assertEqual(enword('5', 1),
                         'five, ')
        p.number_args = dict(zero='zero', one='one', andword='and')
        self.assertEqual(enword('0', 1),
                         ' zero, ')
        self.assertEqual(enword('1', 1),
                         ' one, ')
        self.assertEqual(enword('347', 1),
                         'three, four, seven, ')

        self.assertEqual(enword('34', 2),
                         'thirty-four , ')
        self.assertEqual(enword('347', 2),
                         'thirty-four , seven, ')
        self.assertEqual(enword('34768', 2),
                         'thirty-four , seventy-six , eight, ')
        self.assertEqual(enword('1', 2),
                         'one, ')
        p.number_args['one'] = 'single'
        self.TODO(enword('1', 2),
                  'single, ', 'one, ')  # TODO: doesn't use default word for 'one' here

        p.number_args['one'] = 'one'

        self.assertEqual(enword('134', 3),
                         ' one thirty-four , ')

        self.assertEqual(enword('0', -1),
                         'zero')
        self.assertEqual(enword('1', -1),
                         'one')

        self.assertEqual(enword('3', -1),
                         'three , ')
        self.assertEqual(enword('12', -1),
                         'twelve , ')
        self.assertEqual(enword('123', -1),
                         'one hundred and twenty-three  , ')
        self.assertEqual(enword('1234', -1),
                         'one thousand, two hundred and thirty-four  , ')
        self.assertEqual(enword('12345', -1),
                         'twelve thousand, three hundred and forty-five  , ')
        self.assertEqual(enword('123456', -1),
                         'one hundred and twenty-three  thousand, four hundred and fifty-six  , ')
        self.assertEqual(enword('1234567', -1),
                         'one million, two hundred and thirty-four  thousand, '
                         'five hundred and sixty-seven  , ')

    def test_numwords(self):
        p = inflect.engine()
        numwords = p.number_to_words

        for n, word in (
            ('1', 'one'),
            ('10', 'ten'),
            ('100', 'one hundred'),
            ('1000', 'one thousand'),
            ('10000', 'ten thousand'),
            ('100000', 'one hundred thousand'),
            ('1000000', 'one million'),
            ('10000000', 'ten million'),
            ('+10', 'plus ten'),
            ('-10', 'minus ten'),
            ('10.', 'ten point'),
            ('.10', 'point one zero'),
        ):
            self.assertEqual(numwords(n), word)

        for n, word, wrongword in (
            # TODO: should be one point two three
            ('1.23', 'one point two three', 'one point twenty-three'),
        ):
            self.assertEqual(numwords(n), word)

        for n, txt in (
            (3, 'three bottles of beer on the wall'),
            (2, 'two bottles of beer on the wall'),
            (1, 'a solitary bottle of beer on the wall'),
            (0, 'no more bottles of beer on the wall'),
        ):
            self.assertEqual("{}{}".format(
                numwords(n, one='a solitary', zero='no more'),
                p.plural(" bottle of beer on the wall", n)),
                txt)

        self.assertEqual(numwords(0, one='one', zero='zero'), 'zero')

        self.assertEqual(numwords('1234'),
                         'one thousand, two hundred and thirty-four')
        self.assertEqual(numwords('1234', wantlist=True),
                         ['one thousand', 'two hundred and thirty-four'])
        self.assertEqual(numwords('1234567', wantlist=True),
                         ['one million',
                          'two hundred and thirty-four thousand',
                          'five hundred and sixty-seven'])
        self.assertEqual(numwords('+10', wantlist=True),
                         ['plus', 'ten'])
        self.assertEqual(numwords('1234', andword=''),
                         'one thousand, two hundred thirty-four')
        self.assertEqual(numwords('1234', andword='plus'),
                         'one thousand, two hundred plus thirty-four')
        self.assertEqual(numwords(p.ordinal('21')),
                         'twenty-first')
        self.assertEqual(numwords('9', threshold=10),
                         'nine')
        self.assertEqual(numwords('10', threshold=10),
                         'ten')
        self.assertEqual(numwords('11', threshold=10),
                         '11')
        self.assertEqual(numwords('1000', threshold=10),
                         '1,000')
        self.assertEqual(numwords('123', threshold=10),
                         '123')
        self.assertEqual(numwords('1234', threshold=10),
                         '1,234')
        self.assertEqual(numwords('1234.5678', threshold=10),
                         '1,234.5678')
        self.assertEqual(numwords('1', decimal=None),
                         'one')
        self.assertEqual(numwords('1234.5678', decimal=None),
                         'twelve million, three hundred and forty-five '
                         'thousand, six hundred and seventy-eight')

    def test_numwords_group(self):
        p = inflect.engine()
        numwords = p.number_to_words
        self.assertEqual(numwords('12345', group=2),
                         'twelve, thirty-four, five')
        # TODO: 'hundred and' missing
        self.TODO(numwords('12345', group=3),
                  'one hundred and twenty-three',
                  'one twenty-three, forty-five')
        self.assertEqual(numwords('123456', group=3),
                         'one twenty-three, four fifty-six')
        self.assertEqual(numwords('12345', group=1),
                         'one, two, three, four, five')
        self.assertEqual(numwords('1234th', group=0, andword='and'),
                         'one thousand, two hundred and thirty-fourth')
        self.assertEqual(numwords(p.ordinal('1234'), group=0),
                         'one thousand, two hundred and thirty-fourth')
        self.assertEqual(numwords('120', group=2),
                         'twelve, zero')
        self.assertEqual(numwords('120', group=2, zero='oh', one='unity'),
                         'twelve, oh')
        # TODO: ignoring 'one' param with group=2
        self.TODO(numwords('101', group=2, zero='oh', one='unity'),
                  'ten, unity',
                  'ten, one')
        self.assertEqual(numwords('555_1202', group=1, zero='oh'),
                         'five, five, five, one, two, oh, two')
        self.assertEqual(numwords('555_1202', group=1, one='unity'),
                         'five, five, five, unity, two, zero, two')
        self.assertEqual(numwords('123.456', group=1, decimal='mark', one='one'),
                         'one, two, three, mark, four, five, six')

        inflect.STDOUT_ON = False
        self.assertRaises(BadChunkingOptionError,
                          numwords, '1234', group=4)
        inflect.STDOUT_ON = True

    def test_wordlist(self):
        p = inflect.engine()
        wordlist = p.join
        self.assertEqual(wordlist([]),
                         '')
        self.assertEqual(wordlist(('apple',)),
                         'apple')
        self.assertEqual(wordlist(('apple', 'banana')),
                         'apple and banana')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot')),
                         'apple, banana, and carrot')
        self.assertEqual(wordlist(('apple', '1,000', 'carrot')),
                         'apple; 1,000; and carrot')
        self.assertEqual(wordlist(('apple', '1,000', 'carrot'), sep=','),
                         'apple, 1,000, and carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), final_sep=""),
                         'apple, banana and carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), final_sep=";"),
                         'apple, banana; and carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="or"),
                         'apple, banana, or carrot')

        self.assertEqual(wordlist(('apple', 'banana'), conj=" or "),
                         'apple  or  banana')
        self.assertEqual(wordlist(('apple', 'banana'), conj="&"),
                         'apple & banana')  # TODO: want spaces here. Done, report upstream
        self.assertEqual(wordlist(('apple', 'banana'), conj="&", conj_spaced=False),
                         'apple&banana')
        self.assertEqual(wordlist(('apple', 'banana'), conj="& ", conj_spaced=False),
                         'apple& banana')

        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj=" or "),
                         'apple, banana,  or  carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="+"),
                         'apple, banana, + carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="&"),
                         'apple, banana, & carrot')  # TODO: want space here. Done, report updtream
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="&", conj_spaced=False),
                         'apple, banana,&carrot')  # TODO: want space here. Done, report updtream
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj=" &", conj_spaced=False),
                         'apple, banana, &carrot')  # TODO: want space here. Done, report updtream

    def test_print(self):
        inflect.STDOUT_ON = True
        inflect.print3('')  # make sure it doesn't crash
        inflect.STDOUT_ON = False

    def test_doc_examples(self):
        p = inflect.engine()
        self.assertEqual(p.plural_noun('I'), 'we')
        self.assertEqual(p.plural_verb('saw'), 'saw')
        self.assertEqual(p.plural_adj('my'), 'our')
        self.assertEqual(p.plural_noun('saw'), 'saws')
        self.assertEqual(p.plural('was'), 'were')
        self.assertEqual(p.plural('was', 1), 'was')
        self.assertEqual(p.plural_verb('was', 2), 'were')
        self.assertEqual(p.plural_verb('was'), 'were')
        self.assertEqual(p.plural_verb('was', 1), 'was')

        for errors, txt in (
            (0, 'There were no errors'),
            (1, 'There was 1 error'),
            (2, 'There were 2 errors'),
        ):
            self.assertEqual("There {}{}".format(p.plural_verb('was', errors),
                                                 p.no(" error", errors)),
                             txt)

            self.assertEqual(p.inflect(
                "There plural_verb(was,%d) no(error,%d)" % (errors, errors)),
                             txt)

        for num1, num2, txt in (
            (1, 2, 'I saw 2 saws'),
            (2, 1, 'we saw 1 saw'),
        ):
            self.assertEqual("{}{}{} {}{}".format(
                p.num(num1, ""),
                p.plural("I"),
                p.plural_verb(" saw"),
                p.num(num2),
                p.plural_noun(" saw")),
                txt)

            self.assertEqual(
                p.inflect(
                    'num(%d,)plural(I) plural_verb(saw) num(%d) plural_noun(saw)' % (num1, num2)
                ), txt)

        self.assertEqual(p.a('a cat'), 'a cat')

        for word, txt in (
            ('cat', 'a cat'),
            ('aardvark', 'an aardvark'),
            ('ewe', 'a ewe'),
            ('hour', 'an hour'),
        ):
            self.assertEqual(p.a('{} {}'.format(p.number_to_words(1, one='a'), word)), txt)

        p.num(2)

    def test_deprecation(self):
        p = inflect.engine()
        for meth in ('pl',
                     'plnoun',
                     'plverb',
                     'pladj',
                     'sinoun',
                     'prespart',
                     'numwords',
                     'plequal',
                     'plnounequal',
                     'plverbequal',
                     'pladjequal',
                     'wordlist',
                     ):
            self.assertRaises(DeprecationWarning, getattr, p, meth)

    def test_unknown_method(self):
        p = inflect.engine()
        with self.assertRaises(AttributeError):
            p.unknown_method


# TODO: test .inflectrc file code

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass
