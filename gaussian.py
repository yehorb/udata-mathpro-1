import sys
import utils
import functools
import itertools
import operator

def elimination(matrix, verbose=False, output=sys.stdout):
    '''
    Executes gaussian elimination process on given matrix. 
    If verbose is true, logs every operation to given output.
    '''
    try:
        output.write('starting gaussian elimination\n')
        output.write('current matrix:\n')
        output.write(utils.pretty_print(matrix))
        reduced_matrix = __elimination_phase__(matrix, verbose, output)
        output.write('reduced matrix:\n')
        output.write(utils.pretty_print(reduced_matrix))
        xs = __back_substitution_phase__(reduced_matrix, verbose, output)
        output.write('solution (x-vector): {}\n'.format(xs))
        output.write('gaussian elimination finished\n')
    except GaussianEliminationError as gee:
        output.write('gaussian elimination error: {}\n'.format(gee))
        sys.exit(65)
    except Exception as ex:
        # TODO Write to output
        print('unexpected exception: {}'.format(ex))
        sys.exit(1)

class GaussianEliminationError(ZeroDivisionError):
    '''
    Raised in case of gaussian elimination process error 
    (e.g. on zero division in elimination/substitution process).
    '''
    pass

# TODO Move these functions to matrix_ops file
def __scale_row__(row, scalar):
    return tuple(map(operator.mul, row, itertools.repeat(scalar)))

# TODO Move these functions to matrix_ops file
def __subtract_rows__(which, what):
    if len(which) != len(what):
        raise ArithmeticError('rows of sizes {}, {}; should be the same'.format(len(which), len(what)))
    def sub(a, b):
        diff = a - b
        return diff if abs(diff) > 1e-12 else 0
    return tuple(tuple(map(sub, which, what)))

# TODO Move these functions to matrix_ops file
def __dot_product__(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ArithmeticError('vectors of sizes {}, {}; should be the same'.format(len(vector_a), len(vector_b)))
    return sum(map(operator.mul, vector_a, vector_b))

# TODO Maybe put scale, subtract and dot-product functions here
def __elimination_phase__(matrix, verbose=False, output=sys.stdout):
    size = len(matrix)
    if verbose:
        output.write('starting elimination phase\n')
    def step(matrix, index):
        # TODO Move these functions to matrix_ops file
        def pivot(matrix):
            leave, sort = matrix[0:index], matrix[index:]
            # TODO Use abs() for largest absolute value
            return leave + tuple(sorted(sort, key=lambda t: (t[index:])[0], reverse=True))
        pivoted_matrix = pivot(matrix)
        if verbose:
            output.write('step {}/{}:\n'.format(index, size - 1))
            output.write(utils.pretty_print(pivoted_matrix))
        pivot_row = pivoted_matrix[index]
        def nullify(element):
            i, row = element
            if i <= index:
                return row
            else:
                if pivot_row[index] == 0:
                    raise GaussianEliminationError('encoutered zero element a[{0}][{0}]'.format(index + 1))
                scale = row[index] / pivot_row[index]
                return __subtract_rows__(row, __scale_row__(pivot_row, scale))
        numbered_rows = enumerate(pivoted_matrix)
        reduced_matrix = map(nullify, tuple(numbered_rows))
        return tuple(reduced_matrix)
    reduced_matrix = functools.reduce(step, range(0, size), matrix)
    if verbose:
        output.write('elimination phase finished\n')
    return reduced_matrix

def __back_substitution_phase__(reduced_matrix, verbose=False, output=sys.stdout):
    size = len(reduced_matrix) - 1
    if verbose:
        output.write('starting back substitution phase\n')
    def step(xs, index):
        b_element = (reduced_matrix[index])[-1]
        a_element = (reduced_matrix[index])[index]
        if a_element == 0:
            raise GaussianEliminationError('encoutered zero element a[{0}][{0}]'.format(index + 1))
        if index == size:
            x_element = b_element / a_element
        else:
            row = (reduced_matrix[index])[index + 1:-1]
            x_element = (b_element - __dot_product__(row, xs)) / a_element
        xss = (x_element,) + xs
        if verbose:
            output.write('step {}/{}:\n'.format(size - index, size))
            output.write('current x\'s: {}\n'.format(xss))
        return xss
    xs = functools.reduce(step, range(size, -1, -1), ())
    if verbose:
        output.write('back substitution phase finished\n')
    return xs
