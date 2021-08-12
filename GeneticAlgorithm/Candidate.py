import random
from past.builtins import range
import numpy as np

class Candidate(object):
    """ A candidate solutions to the Sudoku puzzle. """

    def __init__(self, Nd, sqrtVal):
        self.Nd = Nd
        self.sqrtVal = sqrtVal
        self.values = np.zeros((self.Nd, self.Nd))
        self.fitness = None

        return

    def update_fitness(self):
        """ The fitness of a candidate solution is determined by how close it is to being the actual solution to the puzzle.
        The actual solution (i.e. the 'fittest') is defined as a NdxNd grid of numbers in the range [1, Nd]
        where each row, column and sqrtValxsqrtVal block contains the numbers [1, Nd] without any duplicates (see e.g. http://www.sudoku.com/);
        if there are any duplicates then the fitness will be lower. """

        column_count = np.zeros(self.Nd)
        block_count = np.zeros(self.Nd)
        column_sum = 0
        block_sum = 0

        self.values = self.values.astype(int)
        # For each column....
        for j in range(0, self.Nd):
            for i in range(0, self.Nd):
                column_count[self.values[i][j] - 1] += 1

            for k in range(len(column_count)):
                if column_count[k] == 1:
                    column_sum += (1/self.Nd)/self.Nd
            column_count = np.zeros(self.Nd)

        # For each block...
        for i in range(0, self.Nd, self.sqrtVal):
            for j in range(0, self.Nd, self.sqrtVal):
                for k in range(0, self.sqrtVal):
                    for l in range(0, self.sqrtVal):
                        block_count[self.values[i+k][j+l] - 1] += 1

                for k in range(len(block_count)):
                    if block_count[k] == 1:
                        block_sum += (1/self.Nd)/self.Nd
                block_count = np.zeros(self.Nd)

        # Calculate overall fitness.
        if int(column_sum) == 1 and int(block_sum) == 1:
            fitness = 1.0
        else:
            fitness = column_sum * block_sum

        self.fitness = fitness
        return

    def mutate(self, mutation_rate, given):
        """ Mutate a candidate by picking a row, and then picking two values within that row to swap. """

        r = random.uniform(0, 1.1)
        while r > 1:  # Outside [0, 1] boundary - choose another
            r = random.uniform(0, 1.1)

        success = False
        if r < mutation_rate:  # Mutate.
            while not success:
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1

                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while from_column == to_column:
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)

                    # Check if the two places are free to swap
                if given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0:
                    # ...and that we are not causing a duplicate in the rows' columns.
                    if not given.is_column_duplicate(to_column, self.values[row1][from_column]) and not given.is_column_duplicate(from_column, self.values[row2][to_column]) and not given.is_block_duplicate(row2, to_column, self.values[row1][from_column]) and not given.is_block_duplicate(row1, from_column, self.values[row2][to_column]):
                        # Swap values.
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        success = True

        return success
