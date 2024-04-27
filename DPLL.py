import itertools

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
                # Gán biến cho các hàng xóm
                for x, y in neighbors:
                    if (x, y) not in var_map:
                        var_map[(x, y)] = next_var
                        next_var += 1
                # Tạo mệnh đề cho số bẫy
                if neighbors:
                    # Các mệnh đề cho trường hợp có nhiều hơn num_traps bẫy
                    if len(neighbors) >= num_traps:
                        for comb in itertools.combinations(neighbors, num_traps+1):
                            cnf.append([-var_map[x, y] for x, y in comb])

                    # Các mệnh đề cho trường hợp có ít hơn num_traps bẫy
                    if len(neighbors) >= (len(neighbors) - num_traps+1):
                        for comb in itertools.combinations(neighbors, len(neighbors) - num_traps+1):
                            cnf.append([var_map[x, y] for x, y in comb])

    return cnf, var_map, n, m



def dpll(cnf, assignment):
    # Kiểm tra xem có mệnh đề nào rỗng không, nếu có thì không thể thỏa mãn
    if any(len(clause) == 0 for clause in cnf):
        return False, None
    
    # Kiểm tra xem CNF đã thỏa mãn chưa (không còn mệnh đề nào)
    if not cnf:
        return True, assignment
    
    # Đơn vị truyền thông: Tìm kiếm và xử lý mệnh đề một phần tử
    for clause in cnf:
        if len(clause) == 1:
            literal = clause[0]
            return dpll(
                propagate_unit(cnf, literal),
                update_assignment(assignment, literal)
            )

    # Chọn biến chưa gán
    variable = next((l for clause in cnf for l in clause if abs(l) not in assignment), None)
    # Đệ quy với giá trị True
    new_cnf = propagate_unit(cnf, variable)
    new_assignment = update_assignment(assignment.copy(), variable)
    res, final_assignment = dpll(new_cnf, new_assignment)
    if res:
        return True, final_assignment
    
    # Đệ quy với giá trị False
    new_cnf = propagate_unit(cnf, -variable)
    new_assignment = update_assignment(assignment.copy(), -variable)
    return dpll(new_cnf, new_assignment)

def propagate_unit(cnf, literal):
    """Hàm loại bỏ mệnh đề đã thỏa và loại bỏ literal phủ định khỏi các mệnh đề còn lại"""
    new_cnf = []
    for clause in cnf:
        if literal in clause:
            continue  # Loại bỏ mệnh đề đã thỏa mãn
        if -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clause)
    return new_cnf

def update_assignment(assignment, literal):
    """Cập nhật giá trị biến trong bảng gán"""
    assignment[abs(literal)] = True if literal > 0 else False
    return assignment

# Giải quyết CNF
def solve_dpll(grid):
    # grid = readInput('11x11.txt')
    cnf, var_map, n, m = generate_cnf(grid)
    result, solution = dpll(cnf, {})
    if result:
        for (i, j), var in var_map.items():
            grid[i][j] = 'T' if solution[var] == True else 'G'
        return grid
    else:
        return None