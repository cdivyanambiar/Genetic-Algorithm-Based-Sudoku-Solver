"""
This program is to solve sudoku using genetic algorithm.

"""
import sys
import time
import math
from SudokuSolver.CreatePuzzle import CreatePuzzle
from SudokuSolver.Sudoku import Sudoku

if __name__ == '__main__':
    arguments = sys.argv[1:]
    Nd = 4
    input = "1234"
    file = 'Sudoku_4.json'
    if len(arguments) < 3 or len(arguments) > 3:
        print("The arguments passed not correct. Taking default value!!!")
    else:
        Nd = int(arguments[0])
        input = arguments[1]
        file = arguments[2]

    puzzle = CreatePuzzle(Nd, input, file)

    if not puzzle.is_square():
        print("Dimension is wrong. Enter a proper square please. Exiting !!!!")
        exit()

    if not puzzle.isLenEqNd():
        print("Number of character is not equal to " + str(Nd) + ". Exiting !!!! ")
        exit()

    if not puzzle.allCharOrallDigits():
        print("Please enter " + str(Nd) + " Digits OR " + str(
            Nd) + " characters. Combination not allowed.\nAlso 0 not allowed if it is digits. Exiting !!!!")
        exit()

    if not puzzle.isUnique():
        print("The input contain duplicate character. Please enter unique char . Exiting !!!!")
        exit()

    if not puzzle.fileExists():
        print("The file give not exists. Please copy the file where the GA_Sudoku_Solver.py is placed. Exiting !!!!")
        exit()

    sqrtVal = int(math.sqrt(Nd))
    s = Sudoku(Nd, sqrtVal, input, puzzle)
    puzzle.load_db()
    grid = puzzle.new_game()
    s.load(grid)
    start_time = time.time()
    generation, solution = s.solve()
    if (solution):
        if generation == -1:
            print("Invalid inputs")
            str_print = "Invalid input, please try to generate new game"
        elif generation == -2:
            print("No solution found")
            str_print = "No solution found, please try again"
        else:
            puzzle.Print(solution.values)
            # self.sync_board_and_canvas_2()
            time_elapsed = '{0:6.2f}'.format(time.time() - start_time)
            str_print = "Time Elapsed for solution @ generation: " + str(generation) + \
                        "is: " + str(time_elapsed) + "s"
            print(str_print)
