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
                print(neighbors)
                # Gán biến cho các hàng xóm
                for x, y in neighbors:
                    if (x, y) not in var_map:
                        var_map[(x, y)] = next_var
                        next_var += 1
                # Tạo mệnh đề cho số bẫy
                if neighbors:
                    # Các mệnh đề cho trường hợp có nhiều hơn num_traps bẫy
                    if len(neighbors) >= num_traps:
                        print("neighbors1:", neighbors)
                        print("num_traps1:", num_traps)
                        for comb in itertools.combinations(neighbors, num_traps+1):
                            print("comb1:", comb)
                            cnf.append([-var_map[x, y] for x, y in comb])
                            # print (cnf)
                    # Các mệnh đề cho trường hợp có ít hơn num_traps bẫy
                    if len(neighbors) >= (len(neighbors) - num_traps+1):
                        print("neighbors2:", neighbors)
                        print("num_traps2:", num_traps)
                        for comb in itertools.combinations(neighbors, len(neighbors) - num_traps+1):
                            cnf.append([var_map[x, y] for x, y in comb])
                            print("comb2:", comb)
    return cnf, var_map, n, m

def solve_cnf(grid, cnf, var_map, n, m):
    solver = Solver(name='Glucose4')
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

def run_tests(grid):

    cnf, var_map, n, m = generate_cnf(grid)
    sat_solution = solve_cnf(grid, cnf, var_map, n, m)
    return sat_solution
