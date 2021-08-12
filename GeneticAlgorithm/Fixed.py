from GeneticAlgorithm.Candidate import Candidate

class Fixed(Candidate):
    """ fixed/given values. """

    def __init__(self, values, Nd, sqrtVal):
        self.values = values
        self.Nd = Nd
        self.sqrtVal = sqrtVal
        return

    def is_row_duplicate(self, row, value):
        """ Check duplicate in a row. """
        for column in range(0, self.Nd):
            if self.values[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check duplicate in a column. """
        for row in range(0, self.Nd):
            if self.values[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        """ Check duplicate in a 3 x 3 block. """
        i = self.sqrtVal * (int(row / self.sqrtVal))
        j = self.sqrtVal * (int(column / self.sqrtVal))

        for k in range(0, self.sqrtVal):
            for l in range(0, self.sqrtVal):
                if self.values[i + k][j + l] == value:
                    return True
                else:
                    return False

    def make_index(self, v):
        if v <= 2:
            return 0
        elif v <= 5:
            return 3
        else:
            return 6

    def no_duplicates(self, Nd):
        for row in range(0, Nd):
            for col in range(0, Nd):
                if self.values[row][col] != 0:

                    cnt1 = list(self.values[row]).count(self.values[row][col])
                    cnt2 = list(self.values[:,col]).count(self.values[row][col])

                    block_values = [y[self.make_index(col):self.make_index(col)+2] for y in
                                    self.values[self.make_index(row):self.make_index(row)+2]]
                    block_values_ = [int(x) for y in block_values for x in y]
                    cnt3 = block_values_.count(self.values[row][col])

                    if cnt1 > 1 or cnt2 > 1 or cnt3 > 1:
                        return False
        return True
