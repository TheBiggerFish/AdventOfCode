from fishpy.pathfinding.grid import Grid
from fishpy.geometry import LatticePoint

with open("input.txt") as f:
    grid = Grid.from_list_of_strings(f.read().splitlines())

answer1 = 0
answer2 = 0

first_pass = True
changing = True
while changing:
    changing = False

    counting_grid = Grid.blank(grid.size, default_value=0)
    for cell in grid:
        if cell.rep != '@':
            continue
        point = LatticePoint(cell.x, cell.y)
        adj = point.get_adjacent_points(diagonals=True, lower_bound=grid.offset, upper_bound=grid.size)
        for neighbor in adj:
            if grid[neighbor].rep == '@':
                counting_grid[cell].rep += 1

    for cell in counting_grid:
        if grid[cell].rep == "@" and cell.rep < 4:
            if first_pass:
                answer1 += 1
            answer2 += 1
            grid[cell].rep = '.'
            changing = True
    if first_pass:
        print(f'Answer 1: {answer1}')
    first_pass = False

    # print(grid)
    # print('-------------------')
    # print(counting_grid)
print(f'Answer 2: {answer2}')