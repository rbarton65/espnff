import numpy


def square_matrix(X):
    '''Squares a matrix'''
    result = numpy.zeros(shape=(len(X), len(X[0])))

    # iterate through rows of X
    for i in range(len(X)):

        # iterate through columns of X
        for j in range(len(X[0])):

            # iterate through rows of X
            for k in range(len(X)):
                result[i][j] += X[i][k] * X[k][j]

    return result


def add_matrix(X, Y):
    '''Adds two matrices'''
    result = numpy.zeros(shape=(len(X), len(X[0])))

    for i in range(len(X)):

        # iterate through columns
        for j in range(len(X[0])):
            result[i][j] = X[i][j] + Y[i][j]

    return result


def two_step_dominance(X):
    '''Returns result of two step dominance formula'''
    matrix = add_matrix(square_matrix(X), X)
    result = [sum(x) for x in matrix]
    return result
