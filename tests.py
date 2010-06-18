#!/usr/bin/python

import unittest
from re import error as reerror

try:
    import inflect
except ImportError:
    from .. import inflect

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
        self.assertEqual(p.inflect("NUM(1)"), "1")
        self.assertEqual(p.inflect("NUM(1,0)"), "1")
        self.assertEqual(p.inflect("NUM(1,1)"), "1")
        self.assertEqual(p.inflect("NUM(1)   "), "1   ")
        self.assertEqual(p.inflect("   NUM(1)   "), "   1   ")
        self.assertEqual(p.inflect("NUM(3) NUM(1)"), "3 1")

        p.PLmo = lambda mo: "mockPL"
        p.PL_Nmo = lambda mo: "mockPL_N"
        p.PL_Vmo = lambda mo: "mockPL_V"
        p.PL_ADJmo = lambda mo: "mockPL_ADJ"
        p.Amo = lambda mo: "mockA"
        p.NOmo = lambda mo: "mockNO"
        p.ORDmo = lambda mo: "mockORD"
        p.NUMWORDSmo = lambda mo: "mockNUMWORDS"
        p.PART_PRESmo = lambda mo: "mockPART_PRES"

        self.assertEqual(p.inflect("PL(rock)"), "mockPL")
        self.assertEqual(p.inflect("PL(rock)  PL(child)"), "mockPL  mockPL")
        self.assertEqual(p.inflect("NUM(2) PL(rock)  PL(child)"), "2 mockPL  mockPL")

        self.assertEqual(p.inflect("PL(rock) PL_N(rock) PL_V(rocks) PL_ADJ(big) A(ant)"),
                 "mockPL mockPL_N mockPL_V mockPL_ADJ mockA")

        self.assertEqual(p.inflect("AN(rock) NO(0) ORD(3) NUMWORDS(1234) PART_PRES(runs)"),
                 "mockA mockNO mockORD mockNUMWORDS mockPART_PRES")



    def test_user_input_fns(self):
        p = inflect.engine()

        self.assertEqual(p.PL_sb_user_defined, [])
        p.def_noun('VAX','VAXen')
        self.assertEqual(p.PL_sb_user_defined, ['VAX','VAXen'])

        self.assertTrue(p.ud_match('word',p.PL_sb_user_defined)
                        is None)
        self.assertEqual(p.ud_match('VAX',p.PL_sb_user_defined),
                        'VAXen')
        self.assertTrue(p.ud_match('VVAX',p.PL_sb_user_defined)
                        is None)

        p.def_noun('cow','cows|kine')
        self.assertEqual(p.ud_match('cow',p.PL_sb_user_defined),
                        'cows|kine')

        p.def_noun('(.+i)o',r'$1i')
        self.assertEqual(p.ud_match('studio',p.PL_sb_user_defined),
                        'studii')

        p.def_noun('aviatrix','aviatrices')
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        'aviatrices')
        p.def_noun('aviatrix','aviatrixes')
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        'aviatrixes')
        p.def_noun('aviatrix',None)
        self.assertEqual(p.ud_match('aviatrix',p.PL_sb_user_defined),
                        None)

        p.STDOUT_ON = False
        self.assertRaises(reerror, p.def_noun, '(??', None)

        #def_verb
        p.def_verb('will','shall',
                         'will','will',
                         'will','will')
        self.assertEqual(p.ud_match('will',p.PL_v_user_defined),
                         'will')


        #def_adj
        p.def_adj('hir','their')
        self.assertEqual(p.ud_match('hir',p.PL_adj_user_defined),
                        'their')

        #def_a def_an
        p.def_a('h')
        self.assertEqual(p.ud_match('h',p.A_a_user_defined),
                        'a')

        p.def_an('horrendous.*')
        self.assertEqual(p.ud_match('horrendously',p.A_a_user_defined),
                        'an')


    def test_postprocess(self):
        p = inflect.engine()
        self.assertEqual(p.postprocess('cow','cows'),'cows')
        self.assertEqual(p.postprocess('I','we'),'we')
        self.assertEqual(p.postprocess('COW','cows'),'COWS')
        self.assertEqual(p.postprocess('Cow','cows'),'Cows')
        self.assertEqual(p.postprocess('cow','cows|kine'),'cows')
        p.classical()
        self.assertEqual(p.postprocess('cow','cows|kine'),'kine')

    def test_partition_word(self):
        p = inflect.engine()
        self.assertEqual(p.partition_word(' cow '),(' ', 'cow', ' '))
        self.assertEqual(p.partition_word('cow'),('', 'cow', ''))
        self.assertEqual(p.partition_word('   cow'),('   ', 'cow', ''))
        self.assertEqual(p.partition_word('cow   '),('', 'cow', '   '))
        self.assertEqual(p.partition_word('  cow   '),('  ', 'cow', '   '))
        self.assertEqual(p.partition_word(''),('', '', ''))
        #spaces give weird results
        #self.assertEqual(p.partition_word(' '),('', ' ', ''))
        #self.assertEqual(p.partition_word('  '),(' ', ' ', ''))
        #self.assertEqual(p.partition_word('   '),('  ', ' ', ''))

    def test_PL(self):
        p = inflect.engine()
        self.assertEqual(p.PL(''),'')
        self.assertEqual(p.PL('cow'),'cows')
        self.assertEqual(p.PL('thought'),'thoughts')
        self.assertEqual(p.PL('mouse'),'mice')

    def test_PL_N(self):
        p = inflect.engine()
        self.assertEqual(p.PL_N(''),'')
        self.assertEqual(p.PL_N('cow'),'cows')
        self.assertEqual(p.PL_N('thought'),'thoughts')

    def test_PL_V(self):
        p = inflect.engine()
        self.assertEqual(p.PL_V(''),'')
        self.assertEqual(p.PL_V('runs'),'run')
        self.assertEqual(p.PL_V('thought'),'thought')
        self.assertEqual(p.PL_V('eyes'),'eye')

    def test_PL_ADJ(self):
        p = inflect.engine()
        self.assertEqual(p.PL_ADJ(''),'')
        self.assertEqual(p.PL_ADJ('a'),'some')
        self.assertEqual(p.PL_ADJ('this'),'these')
        self.assertEqual(p.PL_ADJ('that'),'those')
        self.assertEqual(p.PL_ADJ('my'),'our')
        self.assertEqual(p.PL_ADJ("cat's"),"cats'")
        self.assertEqual(p.PL_ADJ("child's"),"children's")

    def test_PL_eq(self):
        p = inflect.engine()
        self.assertEqual(p.PL_eq('index','index'),'eq')
        self.assertEqual(p.PL_eq('index','indexes'),'s:p')
        self.assertEqual(p.PL_eq('index','indices'),'s:p')
        self.assertEqual(p.PL_eq('indexes','index'),'p:s')
        self.assertEqual(p.PL_eq('indices','index'),'p:s')
        self.assertEqual(p.PL_eq('indices','indexes'),'p:p')
        self.assertEqual(p.PL_eq('indexes','indices'),'p:p')
        self.assertEqual(p.PL_eq('indices','indices'),'eq')

        self.assertEqual(p.PL_N_eq('index','index'),'eq')
        self.assertEqual(p.PL_N_eq('index','indexes'),'s:p')
        self.assertEqual(p.PL_N_eq('index','indices'),'s:p')
        self.assertEqual(p.PL_N_eq('indexes','index'),'p:s')
        self.assertEqual(p.PL_N_eq('indices','index'),'p:s')
        self.assertEqual(p.PL_N_eq('indices','indexes'),'p:p')
        self.assertEqual(p.PL_N_eq('indexes','indices'),'p:p')
        self.assertEqual(p.PL_N_eq('indices','indices'),'eq')

        self.assertEqual(p.PL_V_eq('runs','runs'),'eq')
        self.assertEqual(p.PL_V_eq('runs','run'),'s:p')
        self.assertEqual(p.PL_V_eq('run','run'),'eq')

        self.assertEqual(p.PL_ADJ_eq('my','my'),'eq')
        self.assertEqual(p.PL_ADJ_eq('my','our'),'s:p')
        self.assertEqual(p.PL_ADJ_eq('our','our'),'eq')

    def test__PL_reg_plurals(self):
        p = inflect.engine()
        self.assertEqual(p._PL_reg_plurals('indexes|indices',
                             'dummy|ind', 'exes','ices'), True)
        self.assertEqual(p._PL_reg_plurals('indexes|robots',
                             'dummy|ind', 'exes','ices'), False)
        self.assertEqual(p._PL_reg_plurals('beaus|beaux',
                             '.*eau', 's','x'), True)


    def test__PL_check_plurals_N(self):
        p = inflect.engine()
        self.assertEqual(p._PL_check_plurals_N('index', 'indices'), False)
        self.assertEqual(p._PL_check_plurals_N('indexes', 'indices'), True)
        self.assertEqual(p._PL_check_plurals_N('indices', 'indexes'), True)
        self.assertEqual(p._PL_check_plurals_N('stigmata', 'stigmas'), True)
        self.assertEqual(p._PL_check_plurals_N('phalanxes', 'phalanges'), True)
        #self.assertEqual(p._PL_check_plurals_N('cats', 'cats'), True)

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
        self.assertEqual(p.get_count(1), 1)
        self.assertEqual(p.get_count(2), 2)
        self.assertEqual(p.get_count(0), 2)
        self.assertEqual(p.get_count(87), 2)
        self.assertEqual(p.get_count(-7), 2)
        self.assertEqual(p.get_count('1'), 1)
        self.assertEqual(p.get_count('2'), 2)
        self.assertEqual(p.get_count('0'), 2)
        self.assertEqual(p.get_count('no'), 2)
        self.assertEqual(p.get_count('zero'), 2)
        self.assertEqual(p.get_count('nil'), 2)
        self.assertEqual(p.get_count('a'), 1)
        self.assertEqual(p.get_count('an'), 1)
        self.assertEqual(p.get_count('one'), 1)
        self.assertEqual(p.get_count('each'), 1)
        self.assertEqual(p.get_count('every'), 1)
        self.assertEqual(p.get_count('this'), 1)
        self.assertEqual(p.get_count('that'), 1)
        self.assertEqual(p.get_count('dummy'), 2)
        self.assertEqual(p.get_count(), '')
        p.NUM(3)
        self.assertEqual(p.get_count(), 2)


    def test__PL_noun(self):
        p = inflect.engine()
        p.NUM(1)
        self.assertEqual(p._PL_noun('cat'), 'cat')
        p.NUM(3)
        self.assertEqual(p._PL_noun(''), '')
        self.assertEqual(p._PL_noun('tuna'), 'tuna')
        self.assertEqual(p._PL_noun('TUNA'), 'TUNA')
        self.assertEqual(p._PL_noun('swordfish'), 'swordfish')
        p.classical('herd')
        self.assertEqual(p._PL_noun('swine'), 'swine')
        p.classical(herd=0)
        self.assertEqual(p._PL_noun('swine'), 'swines')
        self.assertEqual(p._PL_noun('Governor General'), 'Governors General')
        self.assertEqual(p._PL_noun('Governor-General'), 'Governors-General')
        self.assertEqual(p._PL_noun('Major General'), 'Major Generals')
        self.assertEqual(p._PL_noun('Major-General'), 'Major-Generals')
        self.assertEqual(p._PL_noun('son of a gun'), 'sons of guns')
        self.assertEqual(p._PL_noun('son-of-a-gun'), 'sons-of-guns')
        self.assertEqual(p._PL_noun('mother in law'), 'mothers in law')
        self.assertEqual(p._PL_noun('mother-in-law'), 'mothers-in-law')
        self.assertEqual(p._PL_noun('about me'), 'about us')
        #self.assertEqual(p._PL_noun('about ME'), 'about US')
        self.assertEqual(p._PL_noun('I'), 'we')
        self.assertEqual(p._PL_noun('you'), 'you')
        #self.assertEqual(p._PL_noun('YOU'), 'YOU')
        self.assertEqual(p._PL_noun('me'), 'us')
        self.assertEqual(p._PL_noun('child'), 'children')
        self.assertEqual(p._PL_noun('brainchild'), 'brainchilds')
        self.assertEqual(p._PL_noun('human'), 'humans')
        self.assertEqual(p._PL_noun('soliloquy'), 'soliloquies')
        p.classical(persons=1)
        self.assertEqual(p._PL_noun('chairperson'), 'chairpersons')
        p.classical(persons=0)
        self.assertEqual(p._PL_noun('chairperson'), 'chairpeople')
        self.assertEqual(p._PL_noun('chairwoman'), 'chairwomen')
        self.assertEqual(p._PL_noun('goose'), 'geese')
        self.assertEqual(p._PL_noun('tooth'), 'teeth')
        self.assertEqual(p._PL_noun('foot'), 'feet')
        #TODO check spelling protazoon, perceps
        self.assertEqual(p._PL_noun('preceps'), 'preceps')
        self.assertEqual(p._PL_noun('protazoon'), 'protazoa')
        self.assertEqual(p._PL_noun('basis'), 'bases')
        self.assertEqual(p._PL_noun('czech'), 'czechs')
        self.assertEqual(p._PL_noun('codex'), 'codices')
        self.assertEqual(p._PL_noun('radix'), 'radices')
        self.assertEqual(p._PL_noun('bacterium'), 'bacteria')
        self.assertEqual(p._PL_noun('alumnus'), 'alumni')
        self.assertEqual(p._PL_noun('criterion'), 'criteria')
        self.assertEqual(p._PL_noun('alumna'), 'alumnae')

        p.classical()
        self.assertEqual(p._PL_noun('matrix'), 'matrices')
        #TODO is gateau an english word? *ieu word?
        self.assertEqual(p._PL_noun('gateau'), 'gateaux')
        self.assertEqual(p._PL_noun('millieu'), 'millieux')
        self.assertEqual(p._PL_noun('syrinx'), 'syringes')

        self.assertEqual(p._PL_noun('stamen'), 'stamina')
        self.assertEqual(p._PL_noun('apex'), 'apices')
        self.assertEqual(p._PL_noun('appendix'), 'appendices')
        self.assertEqual(p._PL_noun('maximum'), 'maxima')
        self.assertEqual(p._PL_noun('focus'), 'foci')
        self.assertEqual(p._PL_noun('status'), 'status')
        self.assertEqual(p._PL_noun('aurora'), 'aurorae')
        self.assertEqual(p._PL_noun('soma'), 'somata')
        self.assertEqual(p._PL_noun('iris'), 'irides')
        self.assertEqual(p._PL_noun('solo'), 'soli')
        self.assertEqual(p._PL_noun('oxymoron'), 'oxymora')
        self.assertEqual(p._PL_noun('goy'), 'goyim')
        self.assertEqual(p._PL_noun('afrit'), 'afriti')

        p.classical(0)
        p.classical('names')
        # clasical now back to the default mode

        self.assertEqual(p._PL_noun('bias'), 'biases')
        self.assertEqual(p._PL_noun('Jess'), 'Jesses')
        self.assertEqual(p._PL_noun('quiz'), 'quizzes')
        self.assertEqual(p._PL_noun('fox'), 'foxes')

        self.assertEqual(p._PL_noun('shelf'), 'shelves')
        self.assertEqual(p._PL_noun('leaf'), 'leaves')
        self.assertEqual(p._PL_noun('midwife'), 'midwives')
        self.assertEqual(p._PL_noun('scarf'), 'scarves')

        self.assertEqual(p._PL_noun('key'), 'keys')
        self.assertEqual(p._PL_noun('Sally'), 'Sallys')
        self.assertEqual(p._PL_noun('sally'), 'sallies')

        self.assertEqual(p._PL_noun('ado'), 'ados')
        self.assertEqual(p._PL_noun('auto'), 'autos')
        self.assertEqual(p._PL_noun('alto'), 'altos')
        self.assertEqual(p._PL_noun('zoo'), 'zoos')
        self.assertEqual(p._PL_noun('tomato'), 'tomatoes')

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
        #TODO this does not give the correct answer. Only the 'es' gets chopped off, not the 'zes'
        #self.assertEqual(p._PL_special_verb('quizzes'), 'quiz')
        self.assertEqual(p._PL_special_verb('fizzes'), 'fizz')
        self.assertEqual(p._PL_special_verb('dresses'), 'dress')
        self.assertEqual(p._PL_special_verb('flies'), 'fly')
        self.assertEqual(p._PL_special_verb('canoes'), 'canoe')
        # TODO: what matches ^(.*[^s])s$ ?
        #self.assertEqual(p._PL_special_verb('runs'), 'run')

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
        self.assertEqual(p.A('cat'), 'a cat')
        self.assertEqual(p.AN('cat'), 'a cat')
        self.assertEqual(p.A('euphemism'), 'a euphemism')
        self.assertEqual(p.A('Euler number'), 'an Euler number')
        self.assertEqual(p.A('hour'), 'an hour')
        self.assertEqual(p.A('houri'), 'a houri')
        self.assertEqual(p.A('nth'), 'an nth') #TODO: check [fhlmnx]-?th - what does this match?
        #TODO: test user defined cases
        self.assertEqual(p.A('ant'), 'an ant')
        self.assertEqual(p.A('book'), 'a book')
        self.assertEqual(p.A('RSPCA'), 'an RSPCA')
        self.assertEqual(p.A('SONAR'), 'a SONAR')
        self.assertEqual(p.A('FJO'), 'a FJO')
        self.assertEqual(p.A('FJ'), 'an FJ')
        self.assertEqual(p.A('NASA'), 'a NASA')
        self.assertEqual(p.A('UN'), 'a UN')
        self.assertEqual(p.A('yak'), 'a yak')
        self.assertEqual(p.A('yttrium'), 'an yttrium')

    def test_NO(self):
        p = inflect.engine()
        self.assertEqual(p.NO('cat'), 'no cats')
        self.assertEqual(p.NO('cat', count=3), '3 cats')
        self.assertEqual(p.NO('cat', count='three'), 'three cats')
        self.assertEqual(p.NO('mouse'), 'no mice')
        
    def test_PART_PRES(self):
        p = inflect.engine()
        self.assertEqual(p.PART_PRES('runs'), 'running')
        self.assertEqual(p.PART_PRES('dies'), 'dying')
        self.assertEqual(p.PART_PRES('glues'), 'gluing')
        self.assertEqual(p.PART_PRES('eyes'), 'eying')
        self.assertEqual(p.PART_PRES('skis'), 'skiing')
        self.assertEqual(p.PART_PRES('names'), 'naming')
        self.assertEqual(p.PART_PRES('sees'), 'seeing')
        self.assertEqual(p.PART_PRES('hammers'), 'hammering')
        self.assertEqual(p.PART_PRES('bats'), 'batting')
        self.assertEqual(p.PART_PRES('eats'), 'eating')
        
        #TODO: these don't work:
        #self.assertEqual(p.PART_PRES('hoes'), 'hoeing')
        #self.assertEqual(p.PART_PRES('alibis'), 'alibiing')
        #self.assertEqual(p.PART_PRES('is'), 'being')

    def test_ORD(self):
        p = inflect.engine()
        self.assertEqual(p.ORD('1'), '1st')
        self.assertEqual(p.ORD('2'), '2nd')
        self.assertEqual(p.ORD('3'), '3rd')
        self.assertEqual(p.ORD('4'), '4th')
        self.assertEqual(p.ORD('10'), '10th')
        self.assertEqual(p.ORD('28'), '28th')
        self.assertEqual(p.ORD('100'), '100th')
        self.assertEqual(p.ORD('101'), '101st')
        self.assertEqual(p.ORD('1000'), '1000th')
        self.assertEqual(p.ORD('1001'), '1001st')
        self.assertEqual(p.ORD('0'), '0th')
        self.assertEqual(p.ORD('one'), 'first')
        self.assertEqual(p.ORD('two'), 'second')
        self.assertEqual(p.ORD('four'), 'fourth')
        self.assertEqual(p.ORD('twenty'), 'twentieth')
        self.assertEqual(p.ORD('one hundered'), 'one hunderedth')
        self.assertEqual(p.ORD('one hundered and one'), 'one hundered and first')
        self.assertEqual(p.ORD('zero'), 'zeroth')
        self.assertEqual(p.ORD('n'), 'nth') #TODO: bonus!

    def test_millfn(self):
        p = inflect.engine()
        millfn = p.millfn
        self.assertEqual(millfn(1), ' thousand')
        self.assertEqual(millfn(2), ' million')
        self.assertEqual(millfn(3), ' billion')
        self.assertEqual(millfn(0), '')
        self.assertEqual(millfn(11), ' decillion')
        self.assertRaises(NumOutOfRangeError, millfn, 12)
        
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
        #TODO: next 2 seem wrong to me
        self.assertEqual(enword('123456',-1),
                         'one thousand, twenty-three thousand, four hundred and fifty-six, ')
        self.assertEqual(enword('1234567',-1),
                         '1two thousand, thirty-four thousand, five hundred and sixty-seven, ')

    def test_hundfn(self):
        p = inflect.engine()
        NUMWORDS = p.NUMWORDS
        self.assertEqual(NUMWORDS('1234'),
                         'one thousand, two hundred and thirty-four')
        self.assertEqual(NUMWORDS('1234', wantarray=True),
                         ['one thousand', 'two hundred and thirty-four'])
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
        self.assertRaises(BadChunkingOptionError, 
                          NUMWORDS, '1234', group=4)
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


    def test_more(self):
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
        errors = 0
        self.assertEqual("There %s%s" % (p.PL_V('was',errors), p.NO(" error", errors)),
                                         'There were no errors')
        errors = 1
        self.assertEqual("There %s%s" % (p.PL_V('was',errors), p.NO(" error", errors)),
                                         'There was 1 error')
        errors = 2
        self.assertEqual("There %s%s" % (p.PL_V('was',errors), p.NO(" error", errors)),
                                         'There were 2 errors')

        num1 = 1
        num2 = 2
        self.assertEqual("%s%s%s %s%s" % (
                            p.NUM(num1,""),
                            p.PL("I"),
                            p.PL_V(" saw"),
                            p.NUM(num2),
                            p.PL_N(" saw")
                            ),
                            "I saw 2 saws"
                            )
        num1 = 2
        num2 = 1
        self.assertEqual("%s%s%s %s%s" % (
                            p.NUM(num1,""),
                            p.PL("I"),
                            p.PL_V(" saw"),
                            p.NUM(num2),
                            p.PL_N(" saw")
                            ),
                            "we saw 1 saw"
                            )
                         
        num1 = 1
        num2 = 2
        self.assertEqual(p.inflect(
            'NUM(%d,)PL(I) PL_V(saw) NUM(%d) PL_N(saw)' % (num1, num2)
                            ),
                            "I saw 2 saws"
                            )
        num1 = 2
        num2 = 1
        self.assertEqual(p.inflect(
            'NUM(%d,)PL(I) PL_V(saw) NUM(%d) PL_N(saw)' % (num1, num2)
                            ),
                            "we saw 1 saw"
                            )



if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass

