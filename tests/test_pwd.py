#!/usr/bin/python

import unittest
from re import error as reerror

from ..inflect import BadChunkingOptionError, NumOutOfRangeError, UnknownClassicalModeError
from ..inflect import UnknownClassicalModeError, BadNumValueError
from .. import inflect

class test(unittest.TestCase):

    def TODO(self, ans, answer_wanted, answer_gives_now="default_that_will_never_occur__can't_use_None_as_that_is_a_possible_valid_value"):
        '''
        make this test for future testing

        so can easily rename these to assertEqual when code ready        
        '''
        if ans == answer_wanted:
            print 'test unexpectedly passed!: %s == %s' % (ans, answer_wanted)
        if answer_gives_now != "default_that_will_never_occur__can't_use_None_as_that_is_a_possible_valid_value":
            self.assertEqual(ans, answer_gives_now)
        
    def test_enclose(self):
        # def enclose
        self.assertEqual(inflect.enclose("test"), "(?:test)")

    def test_joinstem(self):
        # def joinstem
        self.assertEqual (inflect.joinstem(-2, ["ephemeris", "iris", ".*itis"]),
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

        p.classical(0)
        self.assertEqual(p.classical_dict, inflect.no_classical)

        p.classical(1)
        self.assertEqual(p.classical_dict, inflect.all_classical)
        
        p.classical(all=0)
        self.assertEqual(p.classical_dict, inflect.no_classical)

        p.classical('names', 'zero')
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=1,zero=1))
        self.assertEqual(p.classical_dict, mydict)

        p.classical('all')
        self.assertEqual(p.classical_dict, inflect.all_classical)

        p.classical(0)
        p.classical(names=1, zero=1)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=1,zero=1))
        self.assertEqual(p.classical_dict, mydict)

        p.classical(0)
        p.classical('names', zero=1)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=1,zero=1))
        self.assertEqual(p.classical_dict, mydict)

        p.classical(0)
        p.classical('names', zero=0)
        mydict = inflect.def_classical.copy()
        mydict.update(dict(names=1,zero=0))
        self.assertEqual(p.classical_dict, mydict)

        self.assertRaises(UnknownClassicalModeError, p.classical, 'bogus', reallybogus=1)

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
            self.assertEqual(p.inflect(txt), ans, msg='p.inflect("%s") != "%s"' % (txt, ans))

        for txt, ans in (
        ("pl(rock)", "rocks"),
        ("pl(rock)  pl(child)", "rocks  children"),
        ("num(2) pl(rock)  pl(child)", "2 rocks  children"),

        ("pl(rock) plnoun(rock) plverb(rocks) pladj(big) a(ant)",
                 "rocks rocks rock big an ant"),

        ("an(rock) no(cat) ordinal(3) numwords(1234) prespart(runs)",
                 "a rock no cats 3rd one thousand, two hundred and thirty-four running"),

        ("a(cat,0) a(cat,1) a(cat,2) a(cat, 2)", "0 cat a cat 2 cat  2 cat"), # TODO: extra space when space before number. Is this desirable?
                        ):
            self.assertEqual(p.inflect(txt), ans, msg='p.inflect("%s") != "%s"' % (txt, ans))



    def test_user_input_fns(self):
        p = inflect.engine()

        self.assertEqual(p.pl_sb_user_defined, [])
        p.defnoun('VAX','VAXen')
        self.assertEqual(p.pl('VAX'),'VAXEN')
        self.assertEqual(p.pl_sb_user_defined, ['VAX','VAXen'])

        self.assertTrue(p.ud_match('word',p.pl_sb_user_defined)
                        is None)
        self.assertEqual(p.ud_match('VAX',p.pl_sb_user_defined),
                        'VAXen')
        self.assertTrue(p.ud_match('VVAX',p.pl_sb_user_defined)
                        is None)

        p.defnoun('cow','cows|kine')
        self.assertEqual(p.pl('cow'),'cows')
        p.classical()
        self.assertEqual(p.pl('cow'),'kine')
        
        self.assertEqual(p.ud_match('cow',p.pl_sb_user_defined),
                        'cows|kine')

        p.defnoun('(.+i)o',r'$1i')
        self.assertEqual(p.pl('studio'),'studii')
        self.assertEqual(p.ud_match('studio',p.pl_sb_user_defined),
                        'studii')

        p.defnoun('aviatrix','aviatrices')
        self.assertEqual(p.pl('aviatrix'),'aviatrices')
        self.assertEqual(p.ud_match('aviatrix',p.pl_sb_user_defined),
                        'aviatrices')
        p.defnoun('aviatrix','aviatrixes')
        self.assertEqual(p.pl('aviatrix'),'aviatrixes')
        self.assertEqual(p.ud_match('aviatrix',p.pl_sb_user_defined),
                        'aviatrixes')
        p.defnoun('aviatrix',None)
        self.assertEqual(p.pl('aviatrix'),'aviatrices')
        self.assertEqual(p.ud_match('aviatrix',p.pl_sb_user_defined),
                        None)

        p.defnoun('(cat)',r'$1s')
        self.assertEqual(p.pl('cat'),'cats')

        inflect.STDOUT_ON = False
        self.assertRaises(inflect.BadUserDefinedPatternError, p.defnoun, '(??', None)
        inflect.STDOUT_ON = True

        p.defnoun(None,'') # check None doesn't crash it


        
        #defverb
        p.defverb('will','shall',
                         'will','will',
                         'will','will')
        self.assertEqual(p.ud_match('will',p.pl_v_user_defined),
                         'will')
        self.assertEqual(p.pl('will'),'will')
        #TODO: will -> shall. Tests below fail
        self.TODO(p.plequal('will','shall'),'s:p')
        self.TODO(p.plverbequal('will','shall'),'s:p')


        #defadj
        p.defadj('hir','their')
        self.assertEqual(p.pl('hir'),'their')
        self.assertEqual(p.ud_match('hir',p.pl_adj_user_defined),
                        'their')

        #defa defan
        p.defa('h')
        self.assertEqual(p.a('h'),'a h')
        self.assertEqual(p.ud_match('h',p.A_a_user_defined),
                        'a')

        p.defan('horrendous.*')
        self.assertEqual(p.a('horrendously'),'an horrendously')
        self.assertEqual(p.ud_match('horrendously',p.A_a_user_defined),
                        'an')


    def test_postprocess(self):
        p = inflect.engine()
        for orig, infl, txt in (
                    ('cow','cows','cows'),
                    ('I','we','we'),
                    ('COW','cows','COWS'),
                    ('Cow','cows','Cows'),
                    ('cow','cows|kine','cows'),
                                ):
            self.assertEqual(p.postprocess(orig, infl), txt)
            
        p.classical()
        self.assertEqual(p.postprocess('cow','cows|kine'),'kine')

    def test_partition_word(self):
        p = inflect.engine()
        for txt, part in (
                (' cow ',(' ', 'cow', ' ')),
                ('cow',('', 'cow', '')),
                ('   cow',('   ', 'cow', '')),
                ('cow   ',('', 'cow', '   ')),
                ('  cow   ',('  ', 'cow', '   ')),
                ('',('', '', '')),
                ('bottle of beer',('', 'bottle of beer', '')),
                #spaces give weird results
                #(' '),('', ' ', '')),
                #('  '),(' ', ' ', '')),
                #('   '),('  ', ' ', '')),
                        ):
            self.assertEqual(p.partition_word(txt),part)

    def test_pl(self):
        p = inflect.engine()
        for fn, sing, plur in (
                            (p.pl, '', ''),
                            (p.pl, 'cow', 'cows'),
                            (p.pl, 'thought', 'thoughts'),
                            (p.pl, 'mouse', 'mice'),
                            (p.pl, 'knife', 'knives'),
                            (p.pl, 'knifes', 'knife'),
                            (p.pl, ' cat  ', ' cats  '),
                            (p.pl, 'court martial', 'courts martial'),
                            (p.pl, 'a', 'some'),
                            (p.pl, 'carmen', 'carmina'),
                            (p.pl, 'quartz', 'quartzes'),
                            (p.pl, 'care', 'cares'),
                            (p.plnoun, '',''),
                            (p.plnoun, 'cow','cows'),
                            (p.plnoun, 'thought','thoughts'),
                            (p.plverb, '', ''),
                            (p.plverb, 'runs', 'run'),
                            (p.plverb, 'thought', 'thought'),
                            (p.plverb, 'eyes', 'eye'),
                            (p.pladj, '', ''),
                            (p.pladj, 'a', 'some'),
                            (p.pladj, 'this', 'these'),
                            (p.pladj, 'that', 'those'),
                            (p.pladj, 'my', 'our'),
                            (p.pladj, "cat's", "cats'"),
                            (p.pladj, "child's", "children's"),
                            ):
            self.assertEqual(fn(sing), plur,
                             msg='%s("%s") == "%s" != "%s"' % (
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
            self.assertEqual(p.pl(sing, num), plur)

        p.classical('zero')
        self.assertEqual(p.pl('cow', 0), 'cow')
        self.assertEqual(p.pl('cow', 'zero'), 'cow')
        self.assertEqual(p.pl('runs', 0), 'runs')
        self.assertEqual(p.pl('am', 0), 'am')
        self.assertEqual(p.plverb('runs', 1), 'runs')

        self.assertEqual(p.pl('die'),'dice')
        self.assertEqual(p.plnoun('die'),'dice')

    def test_sinoun(self):
        p = inflect.engine()
        for sing, plur in (
            ('cat', 'cats'),
            ('die', 'dice'),
            ):
            self.assertEqual(p.sinoun(plur), sing)
            self.assertEqual(p.inflect('sinoun(%s)' % plur), sing)

        

    def test_plequal(self):
        p = inflect.engine()
        for fn, sing, plur, res in (
                    (p.plequal, 'index','index','eq'),
                    (p.plequal, 'index','indexes','s:p'),
                    (p.plequal, 'index','indices','s:p'),
                    (p.plequal, 'indexes','index','p:s'),
                    (p.plequal, 'indices','index','p:s'),
                    (p.plequal, 'indices','indexes','p:p'),
                    (p.plequal, 'indexes','indices','p:p'),
                    (p.plequal, 'indices','indices','eq'),
                    (p.plequal, 'opuses','opera','p:p'),
                    (p.plequal, 'opera','opuses','p:p'),
                    (p.plequal, 'brothers','brethren','p:p'),                  
                    (p.plequal, 'cats','cats','eq'),
                    (p.plequal, 'base', 'basis', False),
                    (p.plequal, 'syrinx', 'syringe', False),
                    (p.plequal, 'she', 'he', False),
                    (p.plequal, 'opus', 'operas', False),
                    (p.plequal, 'taxi', 'taxes', False),
                    (p.plequal, 'time', 'Times', False),
                    (p.plequal, 'time'.lower(), 'Times'.lower(), 's:p'),
                    (p.plequal, 'courts martial', 'court martial', 'p:s'),
                    (p.plequal, 'my','my','eq'),
                    (p.plequal, 'my','our','s:p'),
                    (p.plequal, 'our','our','eq'),
                    (p.plnounequal, 'index','index','eq'),
                    (p.plnounequal, 'index','indexes','s:p'),
                    (p.plnounequal, 'index','indices','s:p'),
                    (p.plnounequal, 'indexes','index','p:s'),
                    (p.plnounequal, 'indices','index','p:s'),
                    (p.plnounequal, 'indices','indexes','p:p'),
                    (p.plnounequal, 'indexes','indices','p:p'),
                    (p.plnounequal, 'indices','indices','eq'),
                    (p.plverbequal, 'runs','runs','eq'),
                    (p.plverbequal, 'runs','run','s:p'),
                    (p.plverbequal, 'run','run','eq'),
                    (p.pladjequal, 'my','my','eq'),
                    (p.pladjequal, 'my','our','s:p'),
                    (p.pladjequal, 'our','our','eq'),
                        ):
            self.assertEqual(fn(sing, plur), res)

        for fn, sing, plur, res, badres in (
                    (p.plequal, "dresses's","dresses'", 'p:p', 'p:s'), # TODO: should return p:p 
                    (p.pladjequal, "dresses's","dresses'", 'p:p', False), # TODO: should return p:p

                    # TODO: future: support different singulars one day.
                    (p.plequal, "dress's","dress'",'s:s', 'p:s'),
                    (p.pladjequal, "dress's","dress'",'s:s', False),
                    (p.plequal, "Jess's","Jess'",'s:s', 'p:s'),
                    (p.pladjequal, "Jess's","Jess'",'s:s', False),
                        ):
            self.TODO(fn(sing, plur), res, badres)


        #TODO: pass upstream. multiple adjective plurals not supported
        self.assertEqual(p.plequal('your', 'our'), False)
        p.defadj('my', 'our|your') # what's ours is yours
        self.TODO(p.plequal('your', 'our'), 'p:p')

    def test__pl_reg_plurals(self):
        p = inflect.engine()
        for pair, stems, end1, end2, ans in (
                ('indexes|indices', 'dummy|ind', 'exes', 'ices', True),
                ('indexes|robots', 'dummy|ind', 'exes', 'ices', False),
                ('beaus|beaux', '.*eau', 's', 'x', True),
                                ):
            self.assertEqual(p._pl_reg_plurals(pair, stems, end1, end2),
                             ans)
            


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
                             msg = 'p._plnoun("%s") == %s != "%s"' % (
                                 sing, p._plnoun(sing), plur))

            self.assertEqual(p._sinoun(plur), sing,
                             msg = 'p._sinoun("%s") != "%s"' % (plur, sing))

        # words where forming singular is ambiguious or not attempted
        for sing, plur in (
                ('son of a gun', 'sons of guns'),
                ('son-of-a-gun', 'sons-of-guns'),
                ('basis', 'bases'),
                ('Jess', 'Jesses'),
                ):
            self.assertEqual(p._plnoun(sing), plur,
                             msg = 'p._plnoun("%s") != "%s"' % (sing, plur))


        for sing, plur in (
                #TODO: does not keep case
                ('about ME', 'about US'),
                #TODO: does not keep case
                ('YOU', 'YOU'),
                ):
            self.TODO(p._plnoun(sing), plur)


        p.num(1)
        self.assertEqual(p._plnoun('cat'), 'cat')
        p.num(3)


        p.classical('herd')
        self.assertEqual(p._plnoun('swine'), 'swine')
        p.classical(herd=0)
        self.assertEqual(p._plnoun('swine'), 'swines')
        p.classical(persons=1)
        self.assertEqual(p._plnoun('chairperson'), 'chairpersons')
        p.classical(persons=0)
        self.assertEqual(p._plnoun('chairperson'), 'chairpeople')
        p.classical(ancient=1)
        self.assertEqual(p._plnoun('formula'), 'formulae')
        p.classical(ancient=0)
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

        #p.classical(0)
        #p.classical('names')
        # clasical now back to the default mode


    def test_classical_pl(self):
        p = inflect.engine()
        p.classical()
        for sing, plur in ( ('brother', 'brethren'),
                            ('dogma', 'dogmata'),
                            ):
            self.assertEqual(p.pl(sing), plur)


    def test__pl_special_verb(self):
        p = inflect.engine()
        self.assertEqual(p._pl_special_verb(''), False)
        self.assertEqual(p._pl_special_verb('am'), 'are')
        self.assertEqual(p._pl_special_verb('am',0), 'are')
        self.assertEqual(p._pl_special_verb('runs',0), 'run')
        p.classical('zero')
        self.assertEqual(p._pl_special_verb('am',0), False)
        self.assertEqual(p._pl_special_verb('am',1), 'am')
        self.assertEqual(p._pl_special_verb('am',2), 'are')
        self.assertEqual(p._pl_special_verb('runs',0), False)
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
        self.assertEqual(p._pl_special_verb('zzzoes'), 'zzzo') # TODO: what's a real word to test this case?
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
                ('a','an a'),
                ('an','an an'),
                ('an ant','an ant'),
                ('a cat','a cat'),
                ('an cat','a cat'),
                ('a ant','an ant'),
                    ):
            self.assertEqual(p.a(sing), plur)

        self.assertEqual(p.a('cat',1), 'a cat')
        self.assertEqual(p.a('cat',2), '2 cat')
        
        self.assertEqual(p.a, p.an)

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
            self.assertEqual(p.prespart(sing), plur)
            
        self.assertEqual(p.prespart('hoes'), 'hoeing')
        self.assertEqual(p.prespart('alibis'), 'alibiing')
        self.assertEqual(p.prespart('is'), 'being')
        self.assertEqual(p.prespart('are'), 'being')
        self.assertEqual(p.prespart('had'), 'having')
        self.assertEqual(p.prespart('has'), 'having')
        

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
                    ('n', 'nth'), #bonus!
                ):
            self.assertEqual(p.ordinal(num), numord)

    def test_millfn(self):
        p = inflect.engine()
        millfn = p.millfn
        self.assertEqual(millfn(1), ' thousand')
        self.assertEqual(millfn(2), ' million')
        self.assertEqual(millfn(3), ' billion')
        self.assertEqual(millfn(0), '')
        self.assertEqual(millfn(11), ' decillion')
        inflect.STDOUT_ON = False
        self.assertRaises(NumOutOfRangeError, millfn, 12)
        inflect.STDOUT_ON = True
        
    def test_unitfn(self):
        p = inflect.engine()
        unitfn = p.unitfn
        self.assertEqual(unitfn(1,2), 'one million')
        self.assertEqual(unitfn(1,3), 'one billion')
        self.assertEqual(unitfn(5,3), 'five billion')
        self.assertEqual(unitfn(5,0), 'five')
        self.assertEqual(unitfn(0,0), '')

    def test_tenfn(self):
        p = inflect.engine()
        tenfn = p.tenfn
        self.assertEqual(tenfn(3,1,2), 'thirty-one million')
        self.assertEqual(tenfn(3,0,2), 'thirty million')
        self.assertEqual(tenfn(0,1,2), 'one million')
        self.assertEqual(tenfn(1,1,2), 'eleven million')
        self.assertEqual(tenfn(1,0,2), 'ten million')
        self.assertEqual(tenfn(1,0,0), 'ten')
        self.assertEqual(tenfn(0,0,0), '')

    def test_hundfn(self):
        p = inflect.engine()
        hundfn = p.hundfn
        p.number_args = dict(andword='and')
        self.assertEqual(hundfn(4,3,1,2), 'four hundred and thirty-one million, ')
        self.assertEqual(hundfn(4,0,0,2), 'four hundred million, ')
        self.assertEqual(hundfn(4,0,5,2), 'four hundred and five million, ')
        self.assertEqual(hundfn(0,3,1,2), 'thirty-one million, ')
        self.assertEqual(hundfn(0,0,7,2), 'seven million, ')

    def test_enword(self):
        p = inflect.engine()
        enword = p.enword
        self.assertEqual(enword('5',1),
                         'five, ')
        p.number_args = dict(zero='zero', one='one', andword='and')
        self.assertEqual(enword('0',1),
                         ' zero, ')
        self.assertEqual(enword('1',1),
                         ' one, ')
        self.assertEqual(enword('347',1),
                         'three, four, seven, ')
        
        self.assertEqual(enword('34',2),
                         'thirty-four, ')
        self.assertEqual(enword('347',2),
                         'thirty-four, seven, ')
        self.assertEqual(enword('34768',2),
                         'thirty-four, seventy-six, eight, ')
        self.assertEqual(enword('1',2),
                         'one, ')
        p.number_args['one'] = 'single'
        self.TODO(enword('1',2),
                         'single, ', 'one, ') #TODO: doesn't use default word for 'one' here

        p.number_args['one'] = 'one'

        self.assertEqual(enword('134',3),
                         ' one thirty-four, ')


        self.assertEqual(enword('0',-1),
                         'zero')
        self.assertEqual(enword('1',-1),
                         'one')


        self.assertEqual(enword('3',-1),
                         'three, ')
        self.assertEqual(enword('12',-1),
                         'twelve, ')
        self.assertEqual(enword('123',-1),
                         'one hundred and twenty-three, ')
        self.assertEqual(enword('1234',-1),
                         'one thousand, two hundred and thirty-four, ')
        self.assertEqual(enword('12345',-1),
                         'twelve thousand, three hundred and forty-five, ')
        self.assertEqual(enword('123456',-1),
                         'one hundred and twenty-three thousand, four hundred and fifty-six, ')
        self.assertEqual(enword('1234567',-1),
                         'one million, two hundred and thirty-four thousand, five hundred and sixty-seven, ')

    def test_numwords(self):
        p = inflect.engine()
        numwords = p.numwords

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
            ('10.','ten point zero'),
            ('.10', 'point one zero'),
            ):
            self.assertEqual(numwords(n), word)

        for n, word, wrongword in (
            #TODO: should be one point two three
            ('1.23', 'one point two three', 'one point twenty-three'), 
            ):
            self.TODO(numwords(n), word, wrongword)
            
        for n, txt in (
            (3, 'three bottles of beer on the wall'),
            (2, 'two bottles of beer on the wall'),
            (1, 'a solitary bottle of beer on the wall'),
            (0, 'no more bottles of beer on the wall'),
            ):
            self.assertEqual("%s%s" % (
                numwords(n, one='a solitary', zero='no more'),
                p.pl(" bottle of beer on the wall", n)),
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
                         'twelve million, three hundred and forty-five thousand, six hundred and seventy-eight')
        
    def test_numwords_group(self):
        p = inflect.engine()
        numwords = p.numwords
        self.assertEqual(numwords('12345', group=2),
                         'twelve, thirty-four, five')
        #TODO: 'hundred and' missing
        self.TODO(numwords('12345', group=3),
                         'one hundred and twenty-three',
                         'one twenty-three, forty-five')
        #TODO: answer wrong!
        self.TODO(numwords('123456', group=3),
                         'one twenty-three, four fifty-six',
                         'one twenty-three, six fifty-six')
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
        wordlist = p.wordlist
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
                         'apple & banana') # TODO: want spaces here. Done, report upstream
        self.assertEqual(wordlist(('apple', 'banana'), conj="&", conj_spaced=False),
                         'apple&banana')
        self.assertEqual(wordlist(('apple', 'banana'), conj="& ", conj_spaced=False),
                         'apple& banana')


        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj=" or "),
                         'apple, banana,  or  carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="+"),
                         'apple, banana, + carrot')
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="&"),
                         'apple, banana, & carrot') # TODO: want space here. Done, report updtream
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj="&", conj_spaced=False),
                         'apple, banana,&carrot') # TODO: want space here. Done, report updtream
        self.assertEqual(wordlist(('apple', 'banana', 'carrot'), conj=" &", conj_spaced=False),
                         'apple, banana, &carrot') # TODO: want space here. Done, report updtream



    def test_print(self):
        inflect.STDOUT_ON = True
        inflect.print3('') # make sure it doesn't crash
        inflect.STDOUT_ON = False
        
    def test_doc_examples(self):
        p = inflect.engine()
        self.assertEqual(p.plnoun('I'), 'we')
        self.assertEqual(p.plverb('saw'), 'saw')
        self.assertEqual(p.pladj('my'), 'our')
        self.assertEqual(p.plnoun('saw'), 'saws')
        self.assertEqual(p.pl('was'), 'were')
        self.assertEqual(p.pl('was',1), 'was')
        self.assertEqual(p.plverb('was',2), 'were')
        self.assertEqual(p.plverb('was'), 'were')
        self.assertEqual(p.plverb('was',1), 'was')

        for errors, txt in ( (0, 'There were no errors'),
                             (1, 'There was 1 error'),
                             (2, 'There were 2 errors'),
                             ):
            self.assertEqual("There %s%s" % (p.plverb('was',errors), p.no(" error", errors)),
                                         txt)

            self.assertEqual(p.inflect("There plverb(was,%d) no(error,%d)" % (errors, errors)),
                                         txt)



        for num1, num2, txt in (
                            (1, 2, 'I saw 2 saws'),
                            (2, 1, 'we saw 1 saw'),
                                ):
            self.assertEqual("%s%s%s %s%s" % (
                            p.num(num1,""),
                            p.pl("I"),
                            p.plverb(" saw"),
                            p.num(num2),
                            p.plnoun(" saw")
                            ),
                            txt)
            
            self.assertEqual(p.inflect(
                'num(%d,)pl(I) plverb(saw) num(%d) plnoun(saw)' % (num1, num2)
                            ),
                            txt)

        self.assertEqual(p.a('a cat'), 'a cat')


        for word, txt in (
            ('cat', 'a cat'),
            ('aardvark', 'an aardvark'),
            ('ewe', 'a ewe'),
            ('hour', 'an hour'),
            ):
            self.assertEqual(p.a('%s %s' % (p.numwords(1, one='a'),word)), txt)

        p.num(2)

#TODO: test .inflectrc file code        

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass

