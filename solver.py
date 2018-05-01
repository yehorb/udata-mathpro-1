import sys
import argparse
import utils
from input import get

parser = argparse.ArgumentParser(description='Matrice solver 101.', epilog='Happy solving!')
parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='specify where to get data')
parser.add_argument('output', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='specify where to save computation results')
parser.add_argument('-v', '--verbose', action='store_true', help='also write computation steps to output')
parser.add_argument('-g', '--gaussian', action='store_true', help='solve using gaussian elimination with pivoting')
parser.add_argument('-l', '--lu', action='store_true', help='apply LU-decomposition and compute condition number')

args = vars(parser.parse_args())
input, output, verbose, gaussian, lu = args['input'], args['output'], args['verbose'], args['gaussian'], args['lu']

output.write('reading from {}\nwriting to {}\ndoing {}\n'.format(input.name, output.name, utils.get_operations(gaussian, lu)))

matrix = get(input)
output.write('input matrix is\n{}'.format(utils.pretty_print(matrix)))

# Actuall business-logic calls here

input.close()
output.close()
