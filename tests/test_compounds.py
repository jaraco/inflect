import unittest
import inflect

class test(unittest.TestCase):
	def test_compound_1(self):
		self.assertEqual(p.singular_noun('hello-out-there'),'hello-out-there')
	def test_compound_2(self):	
		self.assertEqual(p.singular_noun('hello out there'),'hello out there')
	def test_compound_3(self):
		self.assertEqual(p.singular_noun('continue-to-operate'),'continue-to-operate')
	def test_compound_4(self):
		self.assertEqual(p.singular_noun('case of diapers'),'case of diapers')

if __name__ == '__main__':
	p=inflect.engine()
	unittest.main()
	