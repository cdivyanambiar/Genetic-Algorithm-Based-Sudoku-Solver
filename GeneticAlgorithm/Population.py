import math
import random
import operator
from past.builtins import range
import numpy as np
from GeneticAlgorithm.Candidate import Candidate
class Population(object):
    """
    A set of candidate solutions to the Sudoku puzzle.
    These candidates are also known as the chromosomes in the population.
    """
    def __init__(self, Nd, sqrtVal, input, puzzle):
        self.candidates = []
        self.Nd = Nd
        self.sqrtVal = sqrtVal
        self.input = input
        self.puzzle = puzzle
        return

    def seed(self, Nc, given):
        self.candidates = []

        # Determine the legal values that each square can take.
        helper = Candidate(self.Nd, self.sqrtVal)
        helper.values = [[[] for j in range(0, self.Nd)] for i in range(0, self.Nd)]
        for row in range(0, self.Nd):
            for column in range(0, self.Nd):
                for value in range(1, self.Nd+1):
                    if ((given.values[row][column] == 0) and not (given.is_column_duplicate(column, value) or given.is_block_duplicate(row, column, value) or given.is_row_duplicate(row, value))):
                        # Value is available.
                        helper.values[row][column].append(value)
                    elif given.values[row][column] != 0:
                        # Given/known value from file.
                        helper.values[row][column].append(given.values[row][column])
                        break

        # Seed a new population.
        count = 0
        for p in range(0, Nc):
            g = Candidate(self.Nd, self.sqrtVal)
            for i in range(0, self.Nd):  # New row in candidate.
                row = np.zeros(self.Nd)

                # Fill in the givens.
                for j in range(0, self.Nd):  # New column j value in row i.

                    # If value is already given, don't change it.
                    if given.values[i][j] != 0:
                        row[j] = given.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif given.values[i][j] == 0:
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                # If we don't have a valid grid, try again. max iteration 500,000
                ii = 0
                while len(list(set(row))) != self.Nd:
                    ii += 1
                    if ii > 500000:
                        return 0
                    for j in range(0, self.Nd):
                        if given.values[i][j] == 0:
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                g.values[i] = row
            count = count + 1
            print("Population Created @ generation :"+str(count))
            print(type(g.values))
            grid = np.array(list(g.values)).reshape((self.Nd, self.Nd)).astype(int)
            self.puzzle.Print(grid)
            self.candidates.append(g)
        # print(self.candidates[0])
        # Compute the fitness of all candidates in the population.
        self.update_fitness()

        # print("Seeding complete.")

        return 1
    def update_fitness(self):
        """ Update fitness of every candidate/chromosome. """
        for candidate in self.candidates:
            candidate.update_fitness()
        return

    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates = sorted(self.candidates, key=operator.attrgetter('fitness'))
        return