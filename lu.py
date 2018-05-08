# TODO Fix import after moving
from gaussian import __dot_product__, __scale_row__, __subtract_rows__
from input import get
import sys
import utils
import functools
import operator

def __transpose__(matrix):
    return tuple(zip(*__shrink__(matrix)))

def __shrink__(matrix):
    return matrix if len(matrix) == len(matrix[0]) else tuple(map(lambda i: i[:-1], matrix))

# TODO Move this function to matrix_ops file
def mult_matrix(matrix_a, matrix_b):
    '''Multiply square matrices of same dimension M and N.'''
    # TODO Fix manual matrices shrinking (rename vars)
    # TODO Raise exceptions on non-square matrices
    b_columns = __transpose__(matrix_b)
    def step(matrix, index):
        numbered_rows = zip(range(0, len(matrix)), matrix)
        def multiply(element):
            i, row = element
            return tuple(map(lambda column: __dot_product__(row, column), b_columns)) if i == index else row
        multiplied_matrix = map(multiply, numbered_rows)
        return tuple(multiplied_matrix)
    return functools.reduce(step, range(0, len(matrix_a)), matrix_a)

a = get(open('data/matrix_a.in'))
b = get(open('data/matrix_l.in'))
a = __shrink__(a)
b = __shrink__(b)
c = mult_matrix(a,b)

def pivot(matrix):
    def step(matrix, index):
        leave, sort = matrix[0:index], matrix[index:]
        return leave + tuple(sorted(sort, key=lambda t: abs((t[index:])[0]), reverse=True))
    return functools.reduce(step, range(len(matrix)), matrix)

# TODO Refactor this shit as i will forget all i wrote ovetnight
def pivot_matrix(matrix):
    def step(element, _):
        pivots, indexed_matrix = element
        step_matrix = tuple(map(operator.itemgetter(1), indexed_matrix))
        pivot = max(__transpose__(step_matrix)[0], key=lambda e: abs(e))
        index = tuple(filter(lambda e: pivot in e[1], indexed_matrix))[0][0]
        index_row = tuple(map(lambda i: float(i == index), range(0, len(matrix))))
        next_matrix = tuple(map(lambda e: (e[0], e[1][1:len(e[1])]), filter(lambda e: pivot not in e[1], indexed_matrix)))
        return (pivots + (index_row,), next_matrix)
    pivots, _ = functools.reduce(step, range(0, len(matrix)), ((), tuple(enumerate(matrix))))
    return pivots

def pivot_matrix_old(M):
    '''Returns the pivoting matrix for M, used in Doolittle's method.'''
    size = len(M)
    # Create an identity matrix, with floating point values                                                                                                                                                                                            
    id_mat = [[float(i == j) for i in range(size)] for j in range(size)]
    # print(utils.pretty_print(id_mat))

    # Rearrange the identity matrix such that the largest element of                                                                                                                                                                                   
    # each column of M is placed on the diagonal of M                                                                                                                                                                                               
    for j in range(size):
        def pick(i):
            a = abs(M[i][j])
            # print(a)
            return a
        row = max(range(j, size), key=pick)
        # print(row)
        if j != row:
            # Swap the rows
            id_mat[j], id_mat[row] = id_mat[row], id_mat[j]
            # print(id_mat)

    return tuple(map(lambda e: tuple(e), id_mat))

print(utils.pretty_print(c))
# print(utils.pretty_print(pivot_matrix_old(c)))
print(utils.pretty_print(pivot_matrix(c)))
print(utils.pretty_print(mult_matrix(pivot_matrix(c), c)))

def lu_decomposition(A):
    """Performs an LU Decomposition of A (which must be square)                                                                                                                                                                                        
    into PA = LU. The function returns P, L and U."""
    n = len(A)

    # Create zero matrices for L and U                                                                                                                                                                                                                 
    L = [[0.0] * n for i in range(n)]
    U = [[0.0] * n for i in range(n)]

    # Create the pivot matrix P and the multipled matrix PA                                                                                                                                                                                            
    P = pivot_matrix(A)
    PA = mult_matrix(P, A)

    # Perform the LU Decomposition                                                                                                                                                                                                                     
    for j in range(n):
        # All diagonal entries of L are set to unity                                                                                                                                                                                                   
        L[j][j] = 1.0

        # LaTeX: u_{ij} = a_{ij} - \sum_{k=1}^{i-1} u_{kj} l_{ik}                                                                                                                                                                                      
        for i in range(j+1):
            s1 = sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j] = PA[i][j] - s1

        # LaTeX: l_{ij} = \frac{1}{u_{jj}} (a_{ij} - \sum_{k=1}^{j-1} u_{kj} l_{ik} )                                                                                                                                                                  
        for i in range(j, n):
            s2 = sum(U[k][j] * L[i][k] for k in range(j))
            L[i][j] = (PA[i][j] - s2) / U[j][j]

    return (P, L, U)
