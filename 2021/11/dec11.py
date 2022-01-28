# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/11


from typing import Dict
from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding import Location

iterations = 100
with open('2021/11/input.txt') as f:
    lines = [[int(char) for char in line] for line in f.read().strip().split()]
    grid = Grid.from_list_of_strings(lines)

flashes = 0
for i in range(1,iterations+1):
    flashed:Dict[Location,bool] = {pt:False for pt in grid}

    for loc in grid:
        loc:Location
        loc.rep += 1

    while True:
        positions = grid.char_positions([10,11,12,13,14,15,16])
        flattened = [grid[position] for value in positions for position in positions[value] if not flashed[grid[position]]]
        if not flattened:
            break
        for loc in flattened:
            flashed[loc] = True
            for adj in loc.get_adjacent_points(diagonals=True,
                                                lower_bound=LatticePoint(0,0),
                                                upper_bound=grid.size):
                grid[adj].rep += 1

    if sum(flashed.values()) == len(flashed):
        # Raise iterations to 230 to get answer to part 2
        print(i)
        break

    for loc in flashed:
        if flashed[loc]:
            flashes += 1
            loc.rep = 0
print(flashes)