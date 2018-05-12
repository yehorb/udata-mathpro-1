import sys

def get(file, output=sys.stdout):
    '''
    Reads matrix data from specified file. Logs errors to output.
    '''
    try:
        if file == sys.stdin:
            output.write('print matrix line by line. when finished, enter EOF character from new line (^Z or ^D)\n')
        matrix = __read_from_file__(file)
        return matrix
    except MatrixFormatError as mfe:
        output.write('invalid matrix in file \'{0}\': {1}\n'.format(file.name, mfe))
        sys.exit(65)
    except ValueError as ve:
        output.write('invalid data in file \'{0}\': {1}\n'.format(file.name, ve))
        sys.exit(65)
    except Exception as ex:
        output.write('unexpected exception: {0}\n'.format(ex))
        sys.exit(1)
    finally:
        file.close()

class MatrixFormatError(ValueError):
    '''
    Inapropriate matrix format.
    '''
    pass

def __read_from_file__(file):
    matrix = []
    for line in file:
        matrix.append(__readline__(line))
    matrix_size = len(matrix)
    for idx, row in enumerate(matrix, 1):
        row_size = len(row)
        if  row_size != matrix_size + 1:
            raise MatrixFormatError('row {0} of size {1}; should be {2}'.format(idx, row_size, matrix_size + 1))
    return tuple(matrix)

def __readline__(line):
    return tuple(map(lambda i: int(i), line.split()))
