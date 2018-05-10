import unittest

import input
import lu
import common

class test_lu(unittest.TestCase):
    def test_decomposition_a(self):
        matrix = input.get(open('data/matrix_a.in'))
        matrix, x = common.split(matrix)
        expected_l = ((1.0, 0.0, 0.0, 0.0), (-1.5, 1.0, 0.0, 0.0), (-0.5, 4/3, 1.0, 0.0), (0.5, -1/3, 2.0, 1.0))
        expected_u = ((2.0, 2.0, -1.0, 1.0), (0.0, 3.0, 1.5, 1.5), (0.0, 0.0, 0.5, 0.5), (0.0, 0.0, 0.0, 3.0))
        expected_x = (4.0, -2.0, 1.0, 0.0)
        actual_l, actual_u = lu.lu_decomposition(matrix)
        actual_x = lu.solve(actual_l, actual_u, x)
        self.__compare_matrices__(expected_l, actual_l)
        self.__compare_matrices__(expected_u, actual_u)
        self.__compare_vectors__(expected_x, actual_x)
    def test_decomposition_g(self):
        matrix = input.get(open('data/matrix_g.in'))
        matrix, _ = common.split(matrix)
        with self.assertRaises(ZeroDivisionError):
            _, _ = lu.lu_decomposition(matrix)

    def __compare_vectors__(self, vector_a, vector_b):
        for i in range(0, len(vector_a)):
            self.assertAlmostEqual(vector_a[i], vector_b[i])
    def __compare_matrices__(self, matrix_a, matrix_b):
        for i in range(len(matrix_a)):
            for j in range(len(matrix_a)):
                self.assertAlmostEqual(matrix_a[i][j], matrix_b[i][j])

if __name__ == '__main__':
    unittest.main()
