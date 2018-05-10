import unittest

import input
import gaussian

class test_common(unittest.TestCase):
    def test_read_a(self):
        actual_a = input.get(open('data/matrix_a.in'))
        expected_a = ((2, 2, -1, 1, 3), (-3, 0, 3, 0, -9), (-1, 3, 3, 2, -7), (1, 0, 0, 4, 4))
        self.assertEqual(actual_a, expected_a)
    def test_read_g(self):
        actual_g = input.get(open('data/matrix_g.in'))
        expected_g = ((-7, -6, -6, 6, 144), (7, 6, 8, -13, -170), (4, 17, -16, 10, 21), (-5, 18, 19, 0, -445))
        self.assertEqual(actual_g, expected_g)
    def test_read_l(self):
        actual_l = input.get(open('data/matrix_l.in'))
        expected_l = ((3, -2, -7, -4, 2), (7, -10, -5, 1, 28), (4, 0, -15, -9, -21), (-8, 8, 13, 4, -11))
        self.assertEqual(actual_l, expected_l)

if __name__ == '__main__':
    unittest.main()
