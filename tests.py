#!/usr/bin/python

import unittest
from re import error as reerror

import inflect

reload(inflect)
from inflect import BadChunkingOptionError, NumOutOfRangeError

class test(unittest.TestCase):
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



    def test_num(self):
        # def NUM
        p = inflect.engine()
        self.assertTrue(p.persistent_count is None)

        p.NUM()
        self.assertTrue(p.persistent_count is None)

        ret = p.NUM(3)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.NUM()
        ret = p.NUM("3")
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.NUM()
        ret = p.NUM(count=3, show=1)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '3')

        p.NUM()
        ret = p.NUM(count=3, show=0)
        self.assertEqual(p.persistent_count, 3)
        self.assertEqual(ret, '')


    def test_inflect(self):
        p = inflect.engine()
        for txt, ans in (
                    ("NUM(1)", "1"),
                    ("NUM(1,0)", "1"),
                    ("NUM(1,1)", "1"),
                    ("NUM(1)   ", "1   "),
                    ("   NUM(1)   ", "   1   "),
                    ("NUM(3) NUM(1)", "3 1"),
                        ):
            self.assertEqual(p.inflect(txt), ans)

        p.PLmo = lambda mo: "mockPL"
        p.PL_Nmo = lambda mo: "mockPL_N"
        p.PL_Vmo = lambda mo: "mockPL_V"
        p.PL_ADJmo = lambda mo: "mockPL_ADJ"
        p.Amo = lambda mo: "mockA"
        p.NOmo = lambda mo: "mockNO"
        p.ORDmo = lambda mo: "mockORD"
        p.NUMWORDSmo = lambda mo: "mockNUMWORDS"
        p.PART_PRESmo = lambda mo: "mockPART_PRES"

        for txt, ans in (
        ("PL(rock)", "mockPL"),
        ("PL(rock)  PL(child)", "mockPL  mockPL"),
        ("NUM(2) PL(rock)  PL(child)", "2 mockPL  mockPL"),

        ("PL(rock) PL_N(rock) PL_V(rocks) PL_ADJ(big) A(ant)",
                 "mockPL mockPL_N mockPL_V mockPL_ADJ mockA"),

        ("AN(rock) NO(0) ORD(3) NUMWORDS(1234) PART_PRES(runs)",
                 "mockA mockNO mockORD mockNUMWORDS mockPART_PRES"),
                        ):
            self.assertEqual(p.inflect(txt), ans)



    def test_user_input_fns(self):
        p = inflect.engine()

        self.assertEqual(p.PL_sb_user_defined, [])
        p.def_noun('VAX','VAXen')
        self.assertEqual(p.PL('VAX'),'VAXEN')
        self.assertEqual(p.PL_sb_user_defined, ['VAX','VAXen'])

        self.assertTrue(p.ud_match('word',p.PL_sb_user_defined)
                        is None)
        self.assertEqual(p.ud_match('VAX',p.PL_sb_user_defined),
                        'VAXen')
        self.assertTrue(p.ud_match('VVAX',p.PL_sb_user_defined)
                        is None)

        p.def_noun('cow','cows|kine')
        self.assertEqual(p.PL('cow'),'cows')
        p.classical()
        self.assertEqual(p.PL('cow'),'kine')
        
        self.assertEqual(p.ud_match('cow',p.PL_sb_user_defined),
                        'cows|kine')

        p.def_noun('(.+i)o',r'$1i')
        self.assertEqual(p.PL('studio'),'studii')
        self.assertEqual(p.ud_match('studio',p.PL_sb_user_defined),
                        'studii')

        p.def_noun('aviatrix','aviatrices')
        self.assertEqual(p.PL('aviatrix'),'aviatrices')
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        'aviatrices')
        p.def_noun('aviatrix','aviatrixes')
        self.assertEqual(p.PL('aviatrix'),'aviatrixes')
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        'aviatrixes')
        p.def_noun('aviatrix',None)
        self.assertEqual(p.PL('aviatrix'),'aviatrices')
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        None)

        p.def_noun('(cat)',r'$1s')
        self.assertEqual(p.PL('cat'),'cats')

        inflect.STDOUT_ON = False
        self.assertRaises(inflect.BadUserDefinedPatternError, p.def_noun, '(??', None)
        inflect.STDOUT_ON = True

        #def_verb
        p.def_verb('will','shall',
                         'will','will',
                         'will','will')
        self.assertEqual(p.ud_match('will',p.PL_v_user_defined),
                         'will')


        #def_adj
        p.def_adj('hir','their')
        self.assertEqual(p.PL('hir'),'their')
        self.assertEqual(p.ud_match('hir',p.PL_adj_user_defined),
                        'their')

        #def_a def_an
        p.def_a('h')
        self.assertEqual(p.A('h'),'a h')
        self.assertEqual(p.ud_match('h',p.A_a_user_defined),
                        'a')

        p.def_an('horrendous.*')
        self.assertEqual(p.A('horrendously'),'an horrendously')
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

    def test_PL(self):
        p = inflect.engine()
        for fn, sing, plur in (
                            (p.PL, '', ''),
                            (p.PL, 'cow', 'cows'),
                            (p.PL, 'thought', 'thoughts'),
                            (p.PL, 'mouse', 'mice'),
                            (p.PL, 'knife', 'knives'),
                            (p.PL, 'knifes', 'knife'),
                            (p.PL, ' cat  ', ' cats  '),
                            (p.PL, 'court martial', 'courts martial'),
                            (p.PL_N, '',''),
                            (p.PL_N, 'cow','cows'),
                            (p.PL_N, 'thought','thoughts'),
                            (p.PL_V, '', ''),
                            (p.PL_V, 'runs', 'run'),
                            (p.PL_V, 'thought', 'thought'),
                            (p.PL_V, 'eyes', 'eye'),
                            (p.PL_ADJ, '', ''),
                            (p.PL_ADJ, 'a', 'some'),
                            (p.PL_ADJ, 'this', 'these'),
                            (p.PL_ADJ, 'that', 'those'),
                            (p.PL_ADJ, 'my', 'our'),
                            (p.PL_ADJ, "cat's", "cats'"),
                            (p.PL_ADJ, "child's", "children's"),
                            ):
            self.assertEqual(fn(sing), plur)

    def test_PL_eq(self):
        p = inflect.engine()
        for fn, sing, plur, res in (
                    (p.PL_eq, 'index','index','eq'),
                    (p.PL_eq, 'index','indexes','s:p'),
                    (p.PL_eq, 'index','indices','s:p'),
                    (p.PL_eq, 'indexes','index','p:s'),
                    (p.PL_eq, 'indices','index','p:s'),
                    (p.PL_eq, 'indices','indexes','p:p'),
                    (p.PL_eq, 'indexes','indices','p:p'),
                    (p.PL_eq, 'indices','indices','eq'),
                    (p.PL_eq, 'cats','cats','eq'),
                    (p.PL_eq, 'base', 'basis', False),
                    (p.PL_eq, 'syrinx', 'syringe', False),
                    (p.PL_eq, 'she', 'he', False),
                    (p.PL_eq, 'opus', 'operas', False),
                    (p.PL_eq, 'taxi', 'taxes', False),
                    (p.PL_eq, 'time', 'Times', False),
                    (p.PL_eq, 'time'.lower(), 'Times'.lower(), 's:p'),
                    (p.PL_eq, 'courts martial', 'court martial', 'p:s'),
                    (p.PL_N_eq, 'index','index','eq'),
                    (p.PL_N_eq, 'index','indexes','s:p'),
                    (p.PL_N_eq, 'index','indices','s:p'),
                    (p.PL_N_eq, 'indexes','index','p:s'),
                    (p.PL_N_eq, 'indices','index','p:s'),
                    (p.PL_N_eq, 'indices','indexes','p:p'),
                    (p.PL_N_eq, 'indexes','indices','p:p'),
                    (p.PL_N_eq, 'indices','indices','eq'),
                    (p.PL_V_eq, 'runs','runs','eq'),
                    (p.PL_V_eq, 'runs','run','s:p'),
                    (p.PL_V_eq, 'run','run','eq'),
                    (p.PL_ADJ_eq, 'my','my','eq'),
                    (p.PL_ADJ_eq, 'my','our','s:p'),
                    (p.PL_ADJ_eq, 'our','our','eq'),
                        ):
            self.assertEqual(fn(sing, plur), res)


    def test__PL_reg_plurals(self):
        p = inflect.engine()
        for pair, stems, end1, end2, ans in (
                ('indexes|indices', 'dummy|ind', 'exes', 'ices', True),
                ('indexes|robots', 'dummy|ind', 'exes', 'ices', False),
                ('beaus|beaux', '.*eau', 's', 'x', True),
                                ):
            self.assertEqual(p._PL_reg_plurals(pair, stems, end1, end2),
                             ans)
            


    def test__PL_check_plurals_N(self):
        p = inflect.engine()
        self.assertEqual(p._PL_check_plurals_N('index', 'indices'), False)
        self.assertEqual(p._PL_check_plurals_N('indexes', 'indices'), True)
        self.assertEqual(p._PL_check_plurals_N('indices', 'indexes'), True)
        self.assertEqual(p._PL_check_plurals_N('stigmata', 'stigmas'), True)
        self.assertEqual(p._PL_check_plurals_N('phalanxes', 'phalanges'), True)

    def test__PL_check_plurals_ADJ(self):
        p = inflect.engine()
        self.assertEqual(p._PL_check_plurals_ADJ("indexes's", "indices's"), True)
        self.assertEqual(p._PL_check_plurals_ADJ("indices's", "indexes's"), True)
        self.assertEqual(p._PL_check_plurals_ADJ("indexes'", "indices's"), True)
        self.assertEqual(p._PL_check_plurals_ADJ("indexes's", "indices'"), True)
        self.assertEqual(p._PL_check_plurals_ADJ("indexes's", "indexes's"), False)
        self.assertEqual(p._PL_check_plurals_ADJ("dogmas's", "dogmata's"), True)
        self.assertEqual(p._PL_check_plurals_ADJ("dogmas'", "dogmata'"), True)

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
        p.NUM(3)
        self.assertEqual(p.get_count(), 2)


    def test__PL_noun(self):
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
                ('son of a gun', 'sons of guns'),
                ('son-of-a-gun', 'sons-of-guns'),
                ('mother in law', 'mothers in law'),
                ('mother-in-law', 'mothers-in-law'),
                ('about me', 'about us'),
                #('about ME', 'about US'),
                ('to it', 'to them'),
                ('from it', 'from them'),
                ('with it', 'with them'),
                ('I', 'we'),
                ('you', 'you'),
                #('YOU', 'YOU'),
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
                ('basis', 'bases'),
                ('czech', 'czechs'),
                ('codex', 'codices'),
                ('radix', 'radices'),
                ('bacterium', 'bacteria'),
                ('alumnus', 'alumni'),
                ('criterion', 'criteria'),
                ('alumna', 'alumnae'),

                ('bias', 'biases'),
                ('Jess', 'Jesses'),
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
            self.assertEqual(p._PL_noun(sing), plur)

        p.NUM(1)
        self.assertEqual(p._PL_noun('cat'), 'cat')
        p.NUM(3)


        p.classical('herd')
        self.assertEqual(p._PL_noun('swine'), 'swine')
        p.classical(herd=0)
        self.assertEqual(p._PL_noun('swine'), 'swines')
        p.classical(persons=1)
        self.assertEqual(p._PL_noun('chairperson'), 'chairpersons')
        p.classical(persons=0)
        self.assertEqual(p._PL_noun('chairperson'), 'chairpeople')
        p.classical(ancient=1)
        self.assertEqual(p._PL_noun('formula'), 'formulae')
        p.classical(ancient=0)
        self.assertEqual(p._PL_noun('formula'), 'formulas')


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
            self.assertEqual(p._PL_noun(sing), plur)

        #p.classical(0)
        #p.classical('names')
        # clasical now back to the default mode


    def test_classical_PL(self):
        p = inflect.engine()
        p.classical()
        for sing, plur in ( ('brother', 'brethren'),
                            ('dogma', 'dogmata'),
                            ):
            self.assertEqual(p.PL(sing), plur)


    def test__PL_special_verb(self):
        p = inflect.engine()
        self.assertEqual(p._PL_special_verb(''), False)
        self.assertEqual(p._PL_special_verb('am'), 'are')
        self.assertEqual(p._PL_special_verb('am going to'), 'are going to')
        self.assertEqual(p._PL_special_verb('did'), 'did')
        self.assertEqual(p._PL_special_verb("wasn't"), "weren't")
        self.assertEqual(p._PL_special_verb("shouldn't"), "shouldn't")
        self.assertEqual(p._PL_special_verb('bias'), False)
        self.assertEqual(p._PL_special_verb('news'), False)
        self.assertEqual(p._PL_special_verb('Jess'), False)
        self.assertEqual(p._PL_special_verb(' '), False)
        self.assertEqual(p._PL_special_verb('brushes'), 'brush')
        self.assertEqual(p._PL_special_verb('fixes'), 'fix')
        #TODO: BUG reported upstream to Perl version:
        # "quizzes". she quizzes, I quiz. this does not give the correct answer. Only the 'es' gets chopped off, not the 'zes' so gives 'quizz'
        #self.assertEqual(p._PL_special_verb('quizzes'), 'quiz')
        self.assertEqual(p._PL_special_verb('fizzes'), 'fizz')
        self.assertEqual(p._PL_special_verb('dresses'), 'dress')
        self.assertEqual(p._PL_special_verb('flies'), 'fly')
        self.assertEqual(p._PL_special_verb('canoes'), 'canoe')
        self.assertEqual(p._PL_special_verb('runs'), 'run')

    def test__PL_general_verb(self):
        p = inflect.engine()
        self.assertEqual(p._PL_general_verb('acts'), 'act')
        self.assertEqual(p._PL_general_verb('act'), 'act')
        self.assertEqual(p._PL_general_verb('saw'), 'saw')
        
    def test__PL_special_adjective(self):
        p = inflect.engine()
        self.assertEqual(p._PL_special_adjective('a'), 'some')
        self.assertEqual(p._PL_special_adjective('my'), 'our')
        self.assertEqual(p._PL_special_adjective("John's"), "Johns'")
        # TODO: original can't handle this. should we handle it?
        #self.assertEqual(p._PL_special_adjective("JOHN's"), "JOHNS'")
        # TODO: can't handle capitals
        #self.assertEqual(p._PL_special_adjective("JOHN'S"), "JOHNS'")
        #self.assertEqual(p._PL_special_adjective("TUNA'S"), "TUNA'S")
        self.assertEqual(p._PL_special_adjective("tuna's"), "tuna's")
        self.assertEqual(p._PL_special_adjective("TUNA's"), "TUNA's")
        self.assertEqual(p._PL_special_adjective("bad"), False)

    def test_A(self):
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
                
                    ):
            self.assertEqual(p.A(sing), plur)

        self.assertEqual(p.A('cat',1), 'a cat')
        self.assertEqual(p.A('cat',2), '2 cat')
        
        self.assertEqual(p.A, p.AN)

    def test_NO(self):
        p = inflect.engine()
        self.assertEqual(p.NO('cat'), 'no cats')
        self.assertEqual(p.NO('cat', count=3), '3 cats')
        self.assertEqual(p.NO('cat', count='three'), 'three cats')
        self.assertEqual(p.NO('mouse'), 'no mice')
        
    def test_PART_PRES(self):
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
            self.assertEqual(p.PART_PRES(sing), plur)
            
        #TODO: these don't work, reported upstream to Perl version
        #self.assertEqual(p.PART_PRES('hoes'), 'hoeing')
        #self.assertEqual(p.PART_PRES('alibis'), 'alibiing')
        #self.assertEqual(p.PART_PRES('is'), 'being')

    def test_ORD(self):
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
            self.assertEqual(p.ORD(num), numord)

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
                         'one, ') #TODO: doesn't use default word for 'one' here

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

    def test_NUMWORDS(self):
        p = inflect.engine()
        NUMWORDS = p.NUMWORDS

        for n, word in (
            ('1', 'one'),
            ('10', 'ten'),
            ('100', 'one hundred'),
            ('1000', 'one thousand'),
            ('10000', 'ten thousand'),
            ('100000', 'one hundred thousand'),
            ('1000000', 'one million'),
            ('10000000', 'ten million'),
            ):
            self.assertEqual(NUMWORDS(n), word)
            
        for n, txt in (
            (3, 'three bottles of beer on the wall'),
            (2, 'two bottles of beer on the wall'),
            (1, 'a solitary bottle of beer on the wall'),
            (0, 'no more bottles of beer on the wall'),
            ):
            self.assertEqual("%s%s" % (
                NUMWORDS(n, one='a solitary', zero='no more'),
                p.PL(" bottle of beer on the wall", n)),
                         txt)

        self.assertEqual(NUMWORDS(0, one='one', zero='zero'), 'zero')

        self.assertEqual(NUMWORDS('1234'),
                         'one thousand, two hundred and thirty-four')
        self.assertEqual(NUMWORDS('1234', wantlist=True),
                         ['one thousand', 'two hundred and thirty-four'])
        self.assertEqual(NUMWORDS('1234567', wantlist=True),
                         ['one million',
                          'two hundred and thirty-four thousand',
                          'five hundred and sixty-seven'])
        self.assertEqual(NUMWORDS('1234', andword=''),
                         'one thousand, two hundred thirty-four')
        self.assertEqual(NUMWORDS('1234', andword='plus'),
                         'one thousand, two hundred plus thirty-four')
        self.assertEqual(NUMWORDS('555_1202', group=1, zero='oh'),
                         'five, five, five, one, two, oh, two')
        self.assertEqual(NUMWORDS('555_1202', group=1, one='unity'),
                         'five, five, five, unity, two, oh, two')
        self.assertEqual(NUMWORDS('123.456', group=1, decimal='mark', one='one'),
                         'one, two, three, mark, four, five, six')
        self.assertEqual(NUMWORDS('12345', group=3),
                         'one, two, three, four, five')
        self.assertEqual(NUMWORDS('12345', group=2),
                         'one, two, three, four, five')
        self.assertEqual(NUMWORDS('12345', group=1),
                         'one, two, three, four, five')
        self.assertEqual(NUMWORDS('1234th', group=0, andword='and'),
                         'one thousand, two hundred and thirty-fourth')
        self.assertEqual(NUMWORDS(p.ORD('1234'), group=0),
                         'one thousand, two hundred and thirty-fourth')
        self.assertEqual(NUMWORDS(p.ORD('21')),
                         'twenty-first')
        inflect.STDOUT_ON = False
        self.assertRaises(BadChunkingOptionError, 
                          NUMWORDS, '1234', group=4)
        inflect.STDOUT_ON = True
        self.assertEqual(NUMWORDS('9', threshold=10, group=0),
                         'nine')
        self.assertEqual(NUMWORDS('10', threshold=10),
                         'ten')
        self.assertEqual(NUMWORDS('11', threshold=10),
                         '11')
        self.assertEqual(NUMWORDS('1000', threshold=10),
                         '1,000')
        self.assertEqual(NUMWORDS('123', threshold=10),
                         '123')
        self.assertEqual(NUMWORDS('1234', threshold=10),
                         '1,234')
        self.assertEqual(NUMWORDS('1234.5678', threshold=10),
                         '1,234.5678')



    def test_wordlist(self):
        p = inflect.engine()
        WORDLIST = p.WORDLIST
        self.assertEqual(WORDLIST('apple', 'banana'),
                         'apple and banana')
        self.assertEqual(WORDLIST('apple', 'banana', 'carrot'),
                         'apple, banana, and carrot')
        self.assertEqual(WORDLIST('apple', '1,000', 'carrot'),
                         'apple; 1,000; and carrot')
        self.assertEqual(WORDLIST('apple', 'banana', 'carrot', final_sep=""),
                         'apple, banana and carrot')
        self.assertEqual(WORDLIST('apple', 'banana', 'carrot', conj="or"),
                         'apple, banana, or carrot')


    def test_doc_examples(self):
        p = inflect.engine()
        self.assertEqual(p.PL_N('I'), 'we')
        self.assertEqual(p.PL_V('saw'), 'saw')
        self.assertEqual(p.PL_ADJ('my'), 'our')
        self.assertEqual(p.PL_N('saw'), 'saws')
        self.assertEqual(p.PL('was'), 'were')
        self.assertEqual(p.PL('was',1), 'was')
        self.assertEqual(p.PL_V('was',2), 'were')
        self.assertEqual(p.PL_V('was'), 'were')
        self.assertEqual(p.PL_V('was',1), 'was')

        for errors, txt in ( (0, 'There were no errors'),
                             (1, 'There was 1 error'),
                             (2, 'There were 2 errors'),
                             ):
            self.assertEqual("There %s%s" % (p.PL_V('was',errors), p.NO(" error", errors)),
                                         txt)

            self.assertEqual(p.inflect("There PL_V(was,%d) NO(error,%d)" % (errors, errors)),
                                         txt)



        for num1, num2, txt in (
                            (1, 2, 'I saw 2 saws'),
                            (2, 1, 'we saw 1 saw'),
                                ):
            self.assertEqual("%s%s%s %s%s" % (
                            p.NUM(num1,""),
                            p.PL("I"),
                            p.PL_V(" saw"),
                            p.NUM(num2),
                            p.PL_N(" saw")
                            ),
                            txt)
            
            self.assertEqual(p.inflect(
                'NUM(%d,)PL(I) PL_V(saw) NUM(%d) PL_N(saw)' % (num1, num2)
                            ),
                            txt)

        self.assertEqual(p.A('a cat'), 'a cat')


        for word, txt in (
            ('cat', 'a cat'),
            ('aardvark', 'an aardvark'),
            ('ewe', 'a ewe'),
            ('hour', 'an hour'),
            ):
            self.assertEqual(p.A('%s %s' % (p.NUMWORDS(1, one='a'),word)), txt)

        p.NUM(2)

#TODO: test .inflectrc file code        

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass

