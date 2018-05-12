def get_operations(gaussian, lu):
    operations = ''
    if gaussian:
        operations += 'gaussian elimination '
    if lu:
        if operations != '':
            operations += 'and '
        operations += 'LU-decomposition '
    if operations == '':
        operations = 'nothing '
    return operations

def pretty_print(matrix):
    output = ''
    for row in matrix:
        A, B = row[0:-1], row[-1]
        for element in A:
            output += ' {:< 10.2f} '.format(element)
        output += ' | {:< 10.2f} '.format(B)
        output += '\n'
    return output

def transpose(matrix):
    return tuple(zip(*matrix))

def split(matrix_and_b):
    size = len(matrix_and_b)
    length = len(matrix_and_b[0])
    if size != length - 1:
        raise ValueError('invalid matrix format of {0}*{0}, should be {0}*{1}'.format(size, size + 1))
    matrix = tuple(map(lambda r: r[0:-1], matrix_and_b))
    b = tuple(map(lambda r: r[-1], matrix_and_b))
    return matrix, b

def stich(matrix, b):
    if len(matrix[0]) != len(b):
        raise ValueError('cant stich non-uniform objects')
    return tuple(map(lambda row, n: row + n, matrix, b))

def gen_identity(size):
    return tuple([tuple([float(e == i) for e in range(0, size)]) for i in range(0, size)])

def get_zeroes(size):
    return tuple([tuple([0.0] * size) for i in range(0, size)])
