from fishpy.pathfinding.grid import Grid
from fishpy.geometry import LatticePoint
from functools import reduce

operators = {
    '+': int.__add__,
    '*': int.__mul__,
}

with open('input.txt') as f:
    grid = Grid.from_list_of_strings(f.read().splitlines())

# Split the grid into subgrids based on empty columns, each representing a single operation
cursor = LatticePoint(0, 0)
operation_grids: list[Grid] = []
for i in range(grid.width):
    col = grid.col(i)
    if all(cell.rep == ' ' for cell in col):
        operation_grids.append(grid.subgrid(cursor, LatticePoint(i, grid.height)).shift(-cursor))
        cursor = LatticePoint(i+1, 0)
operation_grids.append(grid.subgrid(cursor, grid.size).shift(-cursor))

# Parse and perform each operation
answer_2 = 0
for operation_grid in operation_grids:
    operands = []
    for x in range(operation_grid.width):
        number = int(''.join(cell.rep for cell in operation_grid.col(x) if cell.rep.isdigit()))
        operands.append(number)
    operator = operation_grid[LatticePoint(0, operation_grid.height-1)].rep
    operation = operators[operator]
    answer_2 += reduce(operation, operands)
print('Answer 2:', answer_2)