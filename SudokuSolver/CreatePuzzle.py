
import random
from past.builtins import range
import numpy as np
import math
import json
import re
import os
random.seed()


class CreatePuzzle():
    def __init__(self, Nd, input, file):
        self.file = file
        self.Index = []
        self.Nd = Nd
        self.input = input
        self.startChar = "_"

    def fileExists(self):
        if os.path.isfile(self.file):
            return True
        return False

    def isLenEqNd(self):
        if len(self.input) == self.Nd:
            return True
        return False

    def is_square(self):
        sqrt = math.sqrt(self.Nd)
        return (sqrt - int(sqrt)) == 0

    def isUnique(self):

        for i in range(len(self.input)):
            for j in range(i + 1, len(self.input)):
                if self.input[i] == self.input[j]:
                    return False
        return True

    def allCharOrallDigits(self):
        if re.match('^[1-9]*$', self.input):
            return True
        if self.input.isalpha():
            return True
        return False


    def Print(self, grid):
        base = int(math.sqrt(self.Nd))
        side = self.Nd
        word = self.startChar + self.input
        def expandLine(line):
            return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]

        # line0 = expandLine("╔═══╤═══╦═══╗")
        # line1 = expandLine("║ . │ . ║ . ║")
        # line2 = expandLine("╟───┼───╫───╢")
        # line3 = expandLine("╠═══╪═══╬═══╣")
        # line4 = expandLine("╚═══╧═══╩═══╝")

        line0 = expandLine("|___|___|___|")
        line1 = expandLine("| . | . | . |")
        line2 = expandLine("|___|___|___|")
        line3 = expandLine("|___|___|___|")
        line4 = expandLine("|___|___|___|")

        nums = [[""] + [word[n] for n in row] for row in grid]
        print(line0)
        for r in range(1, side + 1):
            print(("".join(n + s for n, s in zip(nums[r - 1], line1.split(".")))))
            print(([line2, line3, line4][(r % side == 0) + (r % base == 0)]))

    def load_db(self):
        try:
            with open(self.file) as f:
                data = json.load(f)
            self.Index = data['Index']
        except:
            print("The Json should contain Index Array. Please refer Sudoku_4.json or sudoku_9.json. Exiting !!!!")
            exit()

    def new_game(self):
        try:
            randomGrid = self.Index[random.randint(0, len(self.Index)-1)]
            grid = np.array(list(randomGrid)).reshape((self.Nd, self.Nd)).astype(int)
            self.Print(grid)
            return grid
        except:
            print("Please check whether you passed the correct input file. Exiting !!!!")
            exit()
