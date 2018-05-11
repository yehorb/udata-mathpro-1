import sys
import functools

import utils
import common
import ops

def decomposition(matrix, verbose=False, output=sys.stdout):
    '''
    Performs an LU decomposition of matrix (which must be square) into matrix = L * U. 
    The function returns L and U.
    If pivoting is enbled, rearanges matrix via pivot matrix.
    '''
    try:
        output.write('starting LU decomposition\n')
        output.write('current matrix:\n')
        op_matrix, b = common.split(matrix)
        output.write(utils.pretty_print(op_matrix))
        l, u = lu_decomposition(op_matrix, None, verbose, output)
        output.write('matrix L:\n')
        output.write(utils.pretty_print(l))
        output.write('matrix U:\n')
        output.write(utils.pretty_print(u))
        output.write('LU decomposition finished\n')
        # TODO Norms, inversed matrix and stuff. It's ready, just add it
    except Exception as ex:
        output.write('unexpected exception: {}\n'.format(ex))
        sys.exit(1)

def lu_decomposition(input_matrix, pivot=None, verbose=False, output=sys.stdout):
    size = len(input_matrix)
    length = len(input_matrix[0])
    if size != length:
        raise ValueError('unable to decompose non-squre matrice')

    s_l = common.gen_identity(size)
    s_u = common.get_zeroes(size)

    matrix = common.transpose(ops.mult_matrix(pivot, input_matrix)) if pivot else common.transpose(input_matrix)
    
    def step(element, index):
        l, u = element
        if verbose:
            output.write('decomposition step {}/{}\n'.format(index, size))
            output.write('matrix l:\n')
            output.write(utils.pretty_print(common.transpose(l)))
            output.write('matrix u:\n')
            output.write(utils.pretty_print(common.transpose(u)))
        def transform_u(curr_u, curr_index):
            def set_u_element(element):
                u_index, u_element = element
                return \
                    matrix[index][curr_index] - ops.dot_product(common.transpose(l)[curr_index], curr_u[index]) \
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
                    (matrix[index][curr_index] - ops.dot_product(common.transpose(curr_l)[curr_index], next_u[index])) / next_u[index][index] \
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
    return common.transpose(f_l), common.transpose(f_u)

def solve(matrix_l, matrix_u, b):
    d = ops.forward(matrix_l, b)
    x = ops.bakckward(matrix_u, d, verbose=False)
    return x

def inverse(matrix_l, matrix_u):
    i = common.gen_identity(len(matrix_l))
    return common.transpose(tuple(map(lambda v: solve(matrix_l, matrix_u, v), i)))
