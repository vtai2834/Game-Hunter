import copy

#########################################################################################
# Backtracking
def get_neighbors(grid, row, col): # Get neighbor cells
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))

    return neighbors

# Check if the solveBoard sastisfies the requirment
def is_valid(grid):
    numericCell = 0 # Count the number of cells that contain numerical value

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if str(grid[row][col]).isnumeric():  # If current cell is a number
                numericCell += 1          
                trap_count = 0    

                for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
                    if str(grid[neighbor_row][neighbor_col]) == 'T':  # If neighbor cell is True (Trap)
                        trap_count += 1 # Increase Trap count

                if trap_count != int(grid[row][col]):   # If trap count does not equal the current cell's value
                    return False

    if numericCell == 0: # Return False if theres no numerical data
        return False
       
    return True

# Use recursion for backtracking
def backtrack(grid, row=0, col=0):
    rows, cols = len(grid), len(grid[0])

    if row == rows - 1 and col == cols: # If current cell is the final cell
        return is_valid(grid)   # Check if the solveBoard sasstisfies the requirement

    if col == cols: # If the current cell is the last cell of the row
        return backtrack(grid, row + 1, 0)  # Continue recursion with the next row

    # Try assigning True (trap) and False (gem) to the current cell
    if not str(grid[row][col]).isnumeric():   # If the current cell has Boolean value of '_'
        grid[row][col] = 'T' # Set the current cell to True

    if backtrack(grid, row, col + 1):   # Continue recursion with the next cell
        return True
    
    if not str(grid[row][col]).isnumeric(): # Vice versa
        grid[row][col] = 'G'

    if backtrack(grid, row, col + 1): 
        return True

    return False

# Solve the fird
def solveBackTrack(grid):
    solve_grid = copy.deepcopy(grid)

    if backtrack(solve_grid): # If the grid is solvable
        return solve_grid   # Return solved grid
    else: 
        return grid # Return original grid