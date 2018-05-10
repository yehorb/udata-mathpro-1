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