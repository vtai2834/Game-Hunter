from itertools import product
##############################################################################################
# Brute-Force
def countTrapsAround(board, x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == 'T':
                count += 1
    return count

def isValid(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y].isdigit():
                expected_count = int(board[x][y])
                if countTrapsAround(board, x, y) != expected_count:
                    return False
    return True

def processBruteFore(grid):
    rows = len(grid)
    cols = len(grid[0])
    indices = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == '_']

    # Mặc định tất cả là đá quý không có số liền kề
    for i, j in indices:
        if all(not grid[x][y].isdigit() for x in range(max(0, i-1), min(rows, i+2)) for y in range(max(0, j-1), min(cols, j+2))):
            grid[i][j] = 'F'
    
    # Chỉ xem xét kết hợp cho các ô chưa được chỉ định còn lại
    remaining_indices = [(i, j) for i, j in indices if grid[i][j] == '_']
    
    for combo in product(['T', 'G'], repeat=len(remaining_indices)):
        # Đặt ô dựa trên trạng thái hiện tại
        for (index, value) in zip(remaining_indices, combo):
            grid[index[0]][index[1]] = value
        
        if isValid(grid):
            return  # Tìm thấy giải pháp hợp lệ đầu tiên thì thoát
        
        else:
            # Đặt lại các ô để kiểm tra sự kết hợp tiếp theo
            for index, value in zip(remaining_indices, combo):
                grid[index[0]][index[1]] = '_'
    
    print("No valid solutions found.")
    
def resetFgrid(grid): # Chuyển F lại thành '_'
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'F':
                grid[i][j] = '_'
        
def solveBruteFore(grid):
    processBruteFore(grid)
    resetFgrid(grid)
    return grid