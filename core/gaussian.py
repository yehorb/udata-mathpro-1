import sys
import functools

from core import utils
from core import functions

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
        output.write('unexpected exception: {}\n'.format(ex))
        sys.exit(1)

class GaussianEliminationError(ZeroDivisionError):
    '''
    Raised in case of gaussian elimination process error 
    (e.g. on zero division in elimination/substitution process).
    '''
    pass

def __elimination_phase__(matrix, verbose=False, output=sys.stdout):
    if verbose:
        output.write('starting elimination phase\n')
    size = len(matrix)
    m, b = utils.split(matrix)
    pivots = functions.pivot_matrix(m)
    pivoted_m = functions.mult_matrix(pivots, m)
    pivoted_b = functions.mult_matrix(pivots, b)
    pivoted_matrix = utils.stich(pivoted_m, pivoted_b)
    def step(matrix, index):
        if verbose:
            output.write('step {}/{}:\n'.format(index, size - 1))
            output.write(utils.pretty_print(matrix))
        pivot_row = matrix[index]
        def nullify(element):
            i, row = element
            if i <= index:
                return row
            else:
                if pivot_row[index] == 0:
                    raise GaussianEliminationError('encoutered zero element a[{0}][{0}]'.format(index + 1))
                scale = row[index] / pivot_row[index]
                return functions.subtract_rows(row, functions.scale_row(pivot_row, scale))
        reduced_matrix = map(nullify, enumerate(matrix)) 
        return tuple(reduced_matrix)
    reduced_matrix = functools.reduce(step, range(0, size), pivoted_matrix)
    if verbose:
        output.write('elimination phase finished\n')
    return reduced_matrix

def __back_substitution_phase__(matrix, verbose=False, output=sys.stdout):
    data, b = utils.split(matrix)
    return functions.bakckward(data, b, verbose, output)
