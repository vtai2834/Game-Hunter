#đọc file
def readInput(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    
    #tạo ma trận lưu dữ liệu:
    matrix = []

    for l in lines:
        #tách các phần tử của từng dòng ra bởi dấu ,
        row = l.strip().split(",")
        matrix.append(row)
    return matrix
matrix = readInput("input.txt")
m = len(matrix)
n = len(matrix[0])
print(matrix)

#tạo các biến logic tương ứng với từng ô trong ma trận:
variables = [[f"x_{i}_{j}" for j in range(n)] for i in range(m)]

#Tạo ràng buộc CNF dựa trên số liệu matrix:
cnf = []
for i in range(m):
    for j in range(n):
        if matrix[i][j] != '_' and matrix[i][j] != ' _':
            num_mines = int(matrix[i][j])
            constraints = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= i + dx < m and 0<= j+dy < n and (dx, dy) != (0, 0):
                        constraints.append(f"{variables[i+dx][j+dy]}")
            clause = " OR ".join(constraints)
            cnf.append(f"({clause}) = {num_mines}")

print(cnf)

#Sử dụng pysat để giải quyết CNF:
from pysat.solvers import Glucose3
solver = Glucose3()
for clause in cnf:
    solver.add_clause(clause.split())

if solver.solve():
    model = solver.get_model()
    for i in range(m):
        for j in range(n):
            if f"x_{i}_{j}" in model:
                print("T", end=" ")
            else:
                print("G", end=" ")
        print()
else:
    print("No solution found")