import itertools
from pysat.solvers import Solver

#đọc file
def readInput(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    
    #tạo ma trận lưu dữ liệu:
    matrix = []

    for l in lines:
        #tách các phần tử của từng dòng ra bởi dấu ,
        row = l.strip().split(", ")
        matrix.append(row)
    
    return matrix
grid = readInput("input.txt")
print(grid)


def generate_cnf(grid):
    """ Generate CNF from the grid provided """
    n = len(grid)
    m = len(grid[0])
    cnf = []
    var_map = {}
    next_var = 1
    for i in range(n):
        for j in range(m):
            if grid[i][j] != '_':
                num_traps = int(grid[i][j])
                neighbors = [
                    (x, y) for x in range(max(0, i-1), min(n, i+2))
                    for y in range(max(0, j-1), min(m, j+2))
                    if (x, y) != (i, j) and grid[x][y] == '_'
                ]
                # Gán biến cho các hàng xóm
                for x, y in neighbors:
                    if (x, y) not in var_map:
                        var_map[(x, y)] = next_var
                        next_var += 1
                # Tạo mệnh đề cho số bẫy
                if neighbors:
                    # Các mệnh đề cho trường hợp có nhiều hơn num_traps bẫy
                    if len(neighbors) >= num_traps:
                        for comb in itertools.combinations(neighbors, num_traps + 1):
                            cnf.append([-var_map[x, y] for x, y in comb])
                    # Các mệnh đề cho trường hợp có ít hơn num_traps bẫy
                    if len(neighbors) >= (len(neighbors) - num_traps + 1):
                        for comb in itertools.combinations(neighbors, len(neighbors) - num_traps + 1):
                            cnf.append([var_map[x, y] for x, y in comb])
    return cnf, var_map, n, m

def solve_cnf(grid, cnf, var_map, n, m):
    solver = Solver(name='Glucose3')
    for clause in cnf:
        solver.add_clause(clause)
    is_solvable = solver.solve()
    solution = [['_' for _ in range(m)] for _ in range(n)]
    if is_solvable:
        model = solver.get_model()
        for (i, j), var in var_map.items():
            solution[i][j] = 'T' if model[var - 1] > 0 else 'G'
    solver.delete()
    
    #thêm các số trong grid ban đầu vào solution:
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            if solution[i][j] == '_':
                solution[i][j] = grid[i][j]

    return solution

def brute_force(grid):
    """ Implement a brute-force solution """
    # This is a placeholder for the actual brute-force algorithm
    return grid

def backtracking(grid):
    """ Implement a backtracking solution """
    # This is a placeholder for the actual backtracking algorithm
    return grid

def run_tests(grid):
    """ Run tests on various grid sizes """
    test_cases = [
        (grid, 4),
        # Add more test cases with varying sizes
    ]
    results = {}
    for grid, n in test_cases:
        print(n)
        cnf, var_map, n, m = generate_cnf(grid)
        sat_solution = solve_cnf(grid, cnf, var_map, n, m)
        results[(tuple(map(tuple, grid)), n)] = sat_solution
    return results

if __name__ == "__main__":
    test_results = run_tests(grid)
    for test_case, result in test_results.items():
        print("Test Case:", test_case)
        print("SAT Solver Solution:", result)
