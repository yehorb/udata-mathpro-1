# TODO Fix import after moving
from gaussian import __dot_product__, __scale_row__, __subtract_rows__, bakckward, elimination
from input import get
import sys
import utils
import functools

def decomposition(matrix, verbose=False, output=sys.stdout):
    '''
    Performs an LU decomposition of matrix (which must be square) into matrix = L * U. 
    The function returns L and U.
    If pivoting is enbled, rearanges matrix via pivot matrix.
    '''
    try:
        output.write('starting LU decomposition\n')
        output.write('current matrix:\n')
        op_matrix = __shrink__(matrix)
        output.write(utils.pretty_print(op_matrix))
        l, u = lu_decomposition(op_matrix, None, verbose, output)
        output.write('matrix L:\n')
        output.write(utils.pretty_print(l))
        output.write('matrix U:\n')
        output.write(utils.pretty_print(u))
        output.write('LU decomposition finished\n')
    except Exception as ex:
        # TODO Write to output
        print('unexpected exception: {}'.format(ex))
        sys.exit(1)

# TODO Move this function to matrix_ops file
def __transpose__(matrix):
    return tuple(zip(*matrix))

# TODO Move this function to matrix_ops file
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

def gen_identity(size):
    return tuple([tuple([float(e == i) for e in range(0, size)]) for i in range(0, size)])

def lu_decomposition(input_matrix, pivot=None, verbose=False, output=sys.stdout):
    size = len(input_matrix)

    # TODO Generate matrices from otutside
    # Create zero matrices for L and U
    s_l = gen_identity(size)
    s_u = tuple([tuple([0.0] * size) for i in range(0, size)])

    # If pivot matrix is defined, use it to rearrange matrix.
    matrix = __transpose__(mult_matrix(pivot, input_matrix)) if pivot else __transpose__(input_matrix)
    
    def step(element, index):
        l, u = element
        if verbose:
            output.write('decomposition step {}/{}\n'.format(index, size))
            output.write('matrix l:\n')
            output.write(utils.pretty_print(__transpose__(l)))
            output.write('matrix u:\n')
            output.write(utils.pretty_print(__transpose__(u)))
        def transform_u(curr_u, curr_index):
            def set_u_element(element):
                u_index, u_element = element
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
    f_l, f_u = functools.reduce(step, range(0, size), (s_l, s_u))
    if verbose:
        output.write('all steps done\n')
    return __transpose__(f_l), __transpose__(f_u)

# TODO Move to core
def forward(lower_matrix, x):
    size = len(lower_matrix)
    def step(xs, index):
        b_element = x[index]
        a_element = (lower_matrix[index])[index]
        if a_element == 0:
            raise RuntimeError('encoutered zero element a[{0}][{0}]'.format(index + 1))
        if index == 0:
            x_element = b_element / a_element
        else:
            row = (lower_matrix[index])[:index]
            x_element = (b_element - __dot_product__(row, xs)) / a_element
        xss = xs + (x_element,)
        return xss
    xs = functools.reduce(step, range(0, size), ())
    return xs

def solve_core(matrix_l, matrix_u, x):
    # L * d = x
    d = forward(matrix_l, x)
    # U * x = d
    solution = bakckward(matrix_u, d, verbose=False)
    return solution

def inverse_core(matrix_l, matrix_u):
    i = gen_identity(len(matrix_l))
    return __transpose__(tuple(map(lambda v: solve_core(matrix_l, matrix_u, v), i)))
