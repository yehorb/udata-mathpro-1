import sys

import utils
import functools

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
        print('unexpected exception: {}'.format(ex))
        sys.exit(1)

class GaussianEliminationError(ZeroDivisionError):
    '''
    Raised in case of gaussian elimination process error 
    (e.g. on zero division in elimination/substitution process).
    '''
    pass

def __scale_row__(row, scalar):
    new_row = map(lambda el: el * scalar, row)
    return tuple(new_row)

def __subtract_rows__(which, what):
    def subtract(i):
        diff = which[i] - what[i]
        return diff if abs(diff) > 1e-12 else 0
    new_row = map(subtract, range(0, len(which)))
    return tuple(new_row)

def __dot_product__(u, v):
    def step(acc, index):
        a, b = u[index], v[index]
        return acc + a * b
    return functools.reduce(step, range(0, len(u)), 0.0)

def __elimination_phase__(matrix, verbose=False, output=sys.stdout):
    size = len(matrix)
    if verbose:
        output.write('starting elimination phase\n')
    def step(matrix, index):
        def pivot(matrix):
            leave, sort = matrix[0:index], matrix[index:]
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
        numbered_rows = zip(range(0, size), pivoted_matrix)
        reduced_matrix = map(nullify, tuple(numbered_rows))
        return tuple(reduced_matrix)
    reduced_matrix = functools.reduce(step, range(0, size), matrix)
    if verbose:
        output.write('elimination phase finished\n')
    return reduced_matrix

def __back_substitution_phase__(reduced_matrix, verbose=False, output=sys.stdout):
    print(reduced_matrix[2][2])
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
