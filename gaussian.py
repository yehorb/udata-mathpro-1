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

def __dot_product__(u, v):
    def step(acc, index):
        a, b = u[index], v[index]
        return acc + a * b
    return functools.reduce(step, range(0, len(u)), 0.0)

def __elimination_phase__(matrix):
    def step(matrix, index):
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
    return functools.reduce(step, range(0, len (matrix)), matrix)

def __back_substitution_phase__(reduced_matrix):
    size = len(reduced_matrix) - 1
    def step(xs, index):
        b_element = (reduced_matrix[index])[-1]
        a_element = (reduced_matrix[index])[index]
        if index == size:
            x_element = b_element / a_element
        else:
            row = reduced_matrix[index][index+1:-1]
            x_element = (b_element - __dot_product__(row, xs)) / a_element
        return (x_element,) + xs
    return functools.reduce(step, range(size, -1, -1), ())

import input
import utils

matrix = input.get(open('data/matrix_a.in'))
print(utils.pretty_print(matrix))

reduced_matrix = __elimination_phase__(matrix)
xs = __back_substitution_phase__(reduced_matrix)

print(utils.pretty_print(reduced_matrix))
print(xs)
