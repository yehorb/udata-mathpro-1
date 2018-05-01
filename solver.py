import sys
import argparse
from input import get

def __get_operations__():
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

def __matrix_to_string__(matrix):
    string = ''
    for row in matrix:
        A, B = row[:-1], row[-1:]
        string += '{} | {}\n'.format(A, B)
    return string

parser = argparse.ArgumentParser(description='Matrice solver 101.', epilog='Happy solving!')
parser.add_argument('input', nargs='?', default='matrix.in', type=argparse.FileType('r'), help='specify where to get data (default: %(default)s)')
parser.add_argument('output', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='specify where to save computation results (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true', help='also write computation steps to output')
parser.add_argument('-g', '--gaussian', action='store_true', help='solve using gaussian elimination with pivoting')
parser.add_argument('-l', '--lu', action='store_true', help='apply LU-decomposition and compute condition number')

args = vars(parser.parse_args())
input, output, verbose, gaussian, lu = args['input'], args['output'], args['verbose'], args['gaussian'], args['lu']

output.write('reading from {}\nwriting to {}\ndoing {}\n'.format(input.name, output.name, __get_operations__()))

matrix = get(input)
output.write('input matrix is\n{}'.format(__matrix_to_string__(matrix)))

# Actuall business-logic calls here

input.close()
output.close()
