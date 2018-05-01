import functools
import utils

def elimination(matrix, verbose):
    pass

def __scale_row__(row, scalar):
    new_row = map(lambda el: el*scalar, row)
    return tuple(new_row)

def __subtract_rows__(which, what):
    new_row = map(lambda i: which[i] - what[i], range(0, len(which)))
    return tuple(new_row)

def __elimination_phase__(matrix):
    def elimination_step(matrix, index):
        pivot_row = matrix[index]
        def nullify(element):
            i, row = element
            if i <= index:
                return row
            else:
                scale = row[index] / pivot_row[index]
                return __subtract_rows__(row, __scale_row__(pivot_row, scale))
        numbered_rows = zip(range(0, len(matrix)), matrix)
        reduced_matrix = map(nullify, tuple(numbered_rows))
        return tuple(reduced_matrix)
    return functools.reduce(elimination_step, range(0, len (matrix)), matrix)
