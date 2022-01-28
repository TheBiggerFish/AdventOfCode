# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/13


from fishpy.geometry.lattice import LatticePoint
from fishpy.pathfinding.grid import ExpandableGrid
from fishpy.pathfinding import Location


print('loading')
with open('2021/13/input.txt') as f:
    lines = f.read().rstrip().split('\n')
    split = lines.index('')
    locations = [Location(*(int(coord) for coord in line.split(',')),Location.IMPASSABLE,rep='#') for line in lines[:split]]
    folds = [line.split()[-1].split('=') for line in lines[split+1:]]
print('building')
grid = ExpandableGrid.from_list_of_locations(locations)

for fold in folds:
    print('copying')
    copy = grid.copy()
    bound = int(fold[1])
    if fold[0] == 'x':
        print('evaluating x')
        grid = grid.subgrid(upper_bound=LatticePoint(bound,grid.height))
        copy = copy.mirror_x().subgrid(upper_bound=LatticePoint(bound,grid.height))
    else:
        print('evaluating y')
        grid = grid.subgrid(upper_bound=LatticePoint(grid.width,bound))
        copy = copy.mirror_y().subgrid(upper_bound=LatticePoint(copy.width,bound))
    print('overlaying')
    grid = grid.overlay(copy)
    print('counting')
    print(len(grid.char_positions('#')['#']))
print(grid)