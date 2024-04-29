from SAT import *
from DPLL import *
from Backtrack import *
from BruteForce import *
import time #cho việc tính thời gian thực thi thuật toán -> phục vụ việc so sánh

def readInput(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    matrix = []

    for l in lines:
        row = l.strip().split(", ")
        matrix.append(row)
    
    return matrix
      
  
def outputGrid(grid):
    for row in grid:
        line = ''
        for j in range(len(row)):
            line += str(row[j])
            if j != len(row) - 1: line += ', '

        print(line)

    print('\n')


def main():
    choice = -1
    while choice != 0:
        print("\n\n MENU")
        print("1. SAT algorithm")
        print("2. BruteFore algorithm")
        print("3. Backtrack algorithm")
        print("4. DPLL algorithm (without library)")
        print("0. Stop")
        choice = int(input("input algorithm: "))
        if choice > 4 or choice == 0:
            return

        grid = readInput("20x20.txt")
        print('Problem:')
        outputGrid(grid)
        name_algorithm = ''
        if choice == 2:
            name_algorithm = 'BruteForce'
            start = time.time()
            solved_grid = solveBruteForce(grid)
            end = time.time()
        elif choice == 3:
            name_algorithm = 'Backtrack'
            start = time.time()
            solved_grid = solveBackTrack(grid)
            end = time.time()
        elif choice == 4:
            name_algorithm = 'DPLL (without library)'
            start = time.time()
            solved_grid = solve_dpll(grid)
            end = time.time()
        elif choice == 1:
            name_algorithm = 'PYSAT library'
            start = time.time()
            solved_grid = run_tests(grid)
            end = time.time()

        if solved_grid:
            print('\nSolved: ' + name_algorithm)
            outputGrid(solved_grid)
            elapsedTime = (end - start) * 1000
            print("Elapsed time: {:.2f} milliseconds".format(elapsedTime))
        else:
            print('\nNo solution')
            elapsedTime = (end - start) * 1000
            print("Elapsed time: {:.2f} milliseconds".format(elapsedTime))


main()