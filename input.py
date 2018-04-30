import sys

class MatrixFormatError(Exception):
    """Inapropriate matrix data or size"""
    pass

def get(file):
    """Read matrix data from specified file."""
    try:
        matrix = __read_from_file(file)
        return matrix
    except MatrixFormatError as mfe:
        print('invalid matrix in file \'{0}\': {1}'.format(file, mfe))
        sys.exit(65)
    except ValueError as ve:
        print('invalid data in file \'{0}\': {1}'.format(file, ve))
        sys.exit(65)
    except Exception as ex:
        print('Unexpected exception: {0}'.format(ex))
        sys.exit(1)

def __read_from_file(file):
    with open(file) as data:
        matrix = []
        for line in data:
            matrix.append(__readline(line))
    n = len(matrix)
    for idx, row in enumerate(matrix, 1):
        m = len(row)
        if  m != n + 1:
            raise MatrixFormatError("row {0} of size {1}; should be {2}".format(idx, m, n + 1))
    return matrix

def __readline(line):
    return list(map(lambda i: int(i), line.split()))
