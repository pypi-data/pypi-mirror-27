import unittest

class Test1(unittest.TestCase):
    def test_2by2(self):
	    self.assertEqual(2*2, 4, "2*2 doesn't equal 4")
    def test_3by3(self):
	    self.assertEqual(3*3, 9, "3*3 doesn't equal 9")
