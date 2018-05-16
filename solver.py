import sys
import argparse

from core.input import get
from core import utils, gaussian, lu, functions

parser = argparse.ArgumentParser(description='Matrice solver 101.', epilog='Happy solving!')
parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='specify where to get data')
parser.add_argument('output', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='specify where to save computation results')
parser.add_argument('-v', '--verbose', action='store_true', help='also write computation steps to output')
parser.add_argument('-g', '--gaussian', action='store_true', help='solve using gaussian elimination')
parser.add_argument('-l', '--lu', action='store_true', help='apply LU-decomposition and compute condition number')

args = vars(parser.parse_args())
input, output, verbose, do_gaussian, do_lu = args['input'], args['output'], args['verbose'], args['gaussian'], args['lu']

output.write(f'reading from {input.name}\n')
output.write(f'writing to {output.name}\n')
output.write(f'doing {utils.get_operations(do_gaussian, do_lu)}\n')

matrix = get(input, output)

if do_gaussian:
    gaussian.elimination(matrix, verbose, output)
if do_lu:
    lu.decomposition(matrix, verbose, output)

if output is not sys.stdout:
    output.close()
