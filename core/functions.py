import sys
import operator
import itertools
import functools

from core import utils
from core import gaussian

def scale_row(row, scalar):
    return tuple(map(operator.mul, row, itertools.repeat(scalar)))

def subtract_rows(row_a, row_b):
    if len(row_a) != len(row_b):
        raise ArithmeticError('rows of sizes {}, {}; should be the same'.format(len(row_a), len(row_b)))
    def sub(a, b):
        diff = a - b
        return diff if abs(diff) > 1e-12 else 0
    return tuple(map(sub, row_a, row_b))

def dot_product(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ArithmeticError('vectors of sizes {}, {}; should be the same'.format(len(vector_a), len(vector_b)))
    return sum(map(operator.mul, vector_a, vector_b))

def mult_matrix(matrix_a, matrix_b):
    '''Multiply square matrices or matrice and vector of same dimension M and N.'''
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError('cant multiply non-uniform matrices')
    b_columns = utils.transpose(matrix_b) if isinstance(matrix_b[0], tuple) else (matrix_b,)
    def step(matrix, index):
        numbered_rows = zip(range(0, len(matrix)), matrix)
        def multiply(element):
            i, row = element
            return tuple(map(lambda column: dot_product(row, column), b_columns)) if i == index else row
        multiplied_matrix = map(multiply, numbered_rows)
        return tuple(multiplied_matrix)
    return functools.reduce(step, range(0, len(matrix_a)), matrix_a)

def forward(lower_matrix, b, verbose=False, output=sys.stdout):
    size = len(lower_matrix)
    if verbose:
        output.write('starting back substitution phase\n')
    def step(xs, index):
        b_element = b[index]
        a_element = (lower_matrix[index])[index]
        if a_element == 0:
            raise gaussian.GaussianEliminationError('encoutered zero element a[{0}][{0}]'.format(index + 1))
        if index == 0:
            x_element = b_element / a_element
        else:
            row = (lower_matrix[index])[:index]
            x_element = (b_element - dot_product(row, xs)) / a_element
        xss = xs + (x_element,)
        if verbose:
            output.write('step {}/{}:\n'.format(size - index, size))
            output.write('current x\'s: {}\n'.format(xss))
        return xss
    xs = functools.reduce(step, range(0, size), ())
    if verbose:
        output.write('forward substitution phase finished\n')
    return xs

def bakckward(upper_matrix, b, verbose=False, output=sys.stdout):
    size = len(upper_matrix) - 1
    if verbose:
        output.write('starting back substitution phase\n')
    def step(xs, index):
        b_element = b[index]
        a_element = (upper_matrix[index])[index]
        if a_element == 0:
            raise gaussian.GaussianEliminationError('encoutered zero element a[{0}][{0}]'.format(index + 1))
        if index == size:
            x_element = b_element / a_element
        else:
            row = (upper_matrix[index])[index + 1:]
            x_element = (b_element - dot_product(row, xs)) / a_element
        xss = (x_element,) + xs
        if verbose:
            output.write('step {}/{}:\n'.format(size - index, size))
            output.write('current x\'s: {}\n'.format(xss))
        return xss
    xs = functools.reduce(step, range(size, -1, -1), ())
    if verbose:
        output.write('back substitution phase finished\n')
    return xs

def pivot_matrix(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError('can\'t calculate pivots for non-square matrix')
    def step(element, index):
        pivots, indexed_matrix = element
        step_indeces, step_matrix = tuple(map(lambda e: e[0], indexed_matrix)), tuple(map(lambda e: e[1][index:], indexed_matrix))
        max_index, _ = max(zip(step_indeces, utils.transpose(step_matrix)[0]), key=lambda e: abs(e[1]))
        index_row = tuple(map(lambda i: float(i == max_index), range(0, len(matrix))))
        next_matrix = tuple(filter(lambda e: e[0] != max_index, indexed_matrix))
        return (pivots + (index_row,), next_matrix)
    pivots, _ = functools.reduce(step, range(0, len(matrix)), ((), tuple(enumerate(matrix))))
    return pivots

def det(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError('can\'t calculate determinant for non-square matrix')
    return functools.reduce(lambda acc, index: acc * matrix[index][index], range(0, len(matrix)), 1)

def infinity_norm(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError('can\'t calculate norm for non-square matrix')
    return max(map(lambda r: sum(map(abs, r)), matrix))
