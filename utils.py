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

def print_matrix(matrix):
    output = ''
    for row in matrix:
        A, B = row[:-1], row[-1:]
        for element in A:
            output += ' {: 2.2f} '.format(element)
        output += ' |  {: 2.2f}\n'.format(B[0])
    return output