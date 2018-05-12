import unittest

from core import input, gaussian

class test_gaussian_elimintaion(unittest.TestCase):
    def test_matrix_a(self):
        matrix = input.get(open('data/matrix_a.in'))
        expected_x = (4.0, -2.0, 1.0, 0.0)
        reduced = gaussian.__elimination_phase__(matrix)
        actual_x = gaussian.__back_substitution_phase__(reduced)
        self.__compare_vectors__(expected_x, actual_x)
    def test_matrix_g(self):
        matrix = input.get(open('data/matrix_g.in'))
        expected_x = (0.0, -11.0, -13.0, -0.0)
        reduced = gaussian.__elimination_phase__(matrix)
        actual_x = gaussian.__back_substitution_phase__(reduced)
        self.__compare_vectors__(expected_x, actual_x)
    def test_matrix_l(self):
        matrix = input.get(open('data/matrix_l.in'))
        with self.assertRaises(gaussian.GaussianEliminationError):
            reduced = gaussian.__elimination_phase__(matrix)
            _ = gaussian.__back_substitution_phase__(reduced)
    
    def __compare_vectors__(self, vector_a, vector_b):
        for i in range(0, len(vector_a)):
            self.assertAlmostEqual(vector_a[i], vector_b[i])

if __name__ == '__main__':
    unittest.main()
