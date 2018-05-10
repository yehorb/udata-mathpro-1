# TODO Fix import after moving
from gaussian import __dot_product__, __scale_row__, __subtract_rows__
from input import get
import sys
import utils
import functools

def __transpose__(matrix):
    return tuple(zip(*matrix))

def __shrink__(matrix):
    return matrix if len(matrix) == len(matrix[0]) else tuple(map(lambda i: i[:-1], matrix))

# TODO Move this function to matrix_ops file
def mult_matrix(matrix_a, matrix_b):
    '''Multiply square matrices of same dimension M and N.'''
    # TODO Fix manual matrices shrinking (rename vars)
    # TODO Raise exceptions on non-square matrices
    b_columns = __transpose__(matrix_b)
    def step(matrix, index):
        numbered_rows = zip(range(0, len(matrix)), matrix)
        def multiply(element):
            i, row = element
            return tuple(map(lambda column: __dot_product__(row, column), b_columns)) if i == index else row
        multiplied_matrix = map(multiply, numbered_rows)
        return tuple(multiplied_matrix)
    return functools.reduce(step, range(0, len(matrix_a)), matrix_a)

def pivot(matrix):
    def step(matrix, index):
        leave, sort = matrix[0:index], matrix[index:]
        return leave + tuple(sorted(sort, key=lambda t: abs((t[index:])[0]), reverse=True))
    return functools.reduce(step, range(len(matrix)), matrix)

# TODO Look up and think about better solution
def pivot_matrix(matrix):
    def step(element, index):
        pivots, indexed_matrix = element
        step_indeces, step_matrix = tuple(map(lambda e: e[0], indexed_matrix)), tuple(map(lambda e: e[1][index:], indexed_matrix))
        max_index, _ = max(zip(step_indeces, __transpose__(step_matrix)[0]), key=lambda e: abs(e[1]))
        index_row = tuple(map(lambda i: float(i == max_index), range(0, len(matrix))))
        next_matrix = tuple(filter(lambda e: e[0] != max_index, indexed_matrix))
        return (pivots + (index_row,), next_matrix)
    pivots, _ = functools.reduce(step, range(0, len(matrix)), ((), tuple(enumerate(matrix))))
    return pivots

def lu_decomposition(input_matrix, pivot=None):
    '''Performs an LU Decomposition of matrix (which must be square) into P * matrix = L * U. The function returns P, L and U.'''
    size = len(input_matrix)

    # TODO Generate matrices from otutside
    # Create zero matrices for L and U
    L = [[float(e == i) for e in range(0, size)] for i in range(0, size)]
    U = [[0.0] * size for i in range(size)]

    # Create the pivot matrix pivots and the multipled matrix pivoted_matrix
    matrix = __transpose__(mult_matrix(pivot, input_matrix)) if pivot else __transpose__(input_matrix)

    def step(element, index):
        l, u = element
        print('on step {}'.format(index + 1))
        def transform_u(curr_u, curr_index):
            def set_u_element(element):
                u_index, u_element = element
                print('on calc of u', matrix[index][curr_index], __transpose__(l)[curr_index], curr_u[index])
                return \
                    matrix[index][curr_index] - __dot_product__(__transpose__(l)[curr_index], curr_u[index]) \
                    if u_index == curr_index else u_element
            def set_u_column(element):
                u_index, u_column = element 
                return \
                    tuple(map(set_u_element, enumerate(u_column))) \
                    if u_index == index else u_column
            return tuple( map(set_u_column, enumerate(curr_u)) )
        next_u = functools.reduce(transform_u, range(0, index + 1), u)
        def transform_l(curr_l, curr_index):
            def set_l_element(element):
                l_index, l_element = element
                return \
                    (matrix[index][curr_index] - __dot_product__(__transpose__(curr_l)[curr_index], next_u[index])) / next_u[index][index] \
                    if l_index == curr_index else l_element
            def set_l_column(element):
                l_index, l_column = element 
                return \
                    tuple(map(set_l_element, enumerate(l_column))) \
                    if l_index == index else l_column
            return tuple( map(set_l_column, enumerate(curr_l)) )
        next_l = functools.reduce(transform_l, range(index + 1, size), l)
        return(next_l, next_u)
    
    f_l, f_u = functools.reduce(step, range(0, size), (L, U))
    so_l = __transpose__(f_l)
    so_u = __transpose__(f_u)
    so_a = mult_matrix(so_l, so_u)
    print(utils.pretty_print(so_l))
    print(utils.pretty_print(so_u))
    print(utils.pretty_print(so_a))

a = __shrink__(get(open('data/lu.in')))

# print(utils.pretty_print(a))
# print(utils.pretty_print(pivot_matrix(c)))
# print(utils.pretty_print(mult_matrix(pivot_matrix(c), c)))

print('pivot and transform')
print(utils.pretty_print(a))
lu_decomposition(a)
