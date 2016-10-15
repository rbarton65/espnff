import unittest

from espnff.utils import (
    square_matrix,
    add_matrix,
    two_step_dominance)

class UtilsTestCase(unittest.TestCase):
    '''Tests for utils'''
    
    def test_square_matrix(self):
        '''Is the logic for square_matrix successful?'''

        matrix1 = matrix1_answer = [[1, 0], [0, 1]]
        self.assertEqual(square_matrix(matrix1), matrix1_answer)

    def test_add_matrix(self):
        '''Is the logic for add_matrix successful?'''

        matrix1 = [[1, 0], [0, 1]]
        matrix1_answer = [[2, 0], [0, 2]]
        self.assertEqual(add_matrix(matrix1, matrix1), matrix1_answer)

    def test_two_step_dominance(self):
        '''Is the logic for two_step_dominance successful?'''

        matrix = [[1, 0], [0, 1]]
        matrix_answer = [2, 2]
        self.assertEqual(two_step_dominance(matrix), matrix_answer)



if __name__ == '__main__':
    unittest.main()
