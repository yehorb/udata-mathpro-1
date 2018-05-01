import sys

def get(file):
    """Read matrix data from specified file."""
    try:
        matrix = __read_from_file__(file)
        return matrix
    except MatrixFormatError as mfe:
        print('invalid matrix in file \'{0}\': {1}'.format(file.name, mfe))
        sys.exit(65)
    except ValueError as ve:
        print('invalid data in file \'{0}\': {1}'.format(file.name, ve))
        sys.exit(65)
    except Exception as ex:
        print('unexpected exception: {0}'.format(ex))
        sys.exit(1)

class MatrixFormatError(Exception):
    """Inapropriate matrix format."""
    pass

def __read_from_file__(file):
    matrix = []
    for line in file:
        matrix.append(__readline__(line))
    matrix_size = len(matrix)
    for idx, row in enumerate(matrix, 1):
        row_size = len(row)
        if  row_size != matrix_size + 1:
            raise MatrixFormatError("row {0} of size {1}; should be {2}".format(idx, row_size, matrix_size + 1))
    return matrix

def __readline__(line):
    return list(map(lambda i: int(i), line.split()))
