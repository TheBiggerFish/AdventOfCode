# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/3


from math import prod

from fishpy.geometry import Point, Vector
from fishpy.pathfinding.grid import Grid

input_1 = Vector(3,1)
input_2 = [Vector(1,1),Vector(3,1),Vector(5,1),Vector(7,1),Vector(1,2)]


def trees_in_line(grid:Grid,step:Vector):
    bounds = Point(grid.width,grid.height)
    pos = Point(0,0)
    trees = 0

    while pos.y < grid.height:
        pos %= bounds
        if not grid[pos].is_passible():
            trees += 1
        pos += step
    return trees


with open('2020/03/input.txt') as f:
    grid = Grid.from_list_of_strings([line.strip() for line in f.readlines()])
    print(f'We would encounter {trees_in_line(grid,input_1)} trees')
    print(f'If you multiply together the number of trees encountered on each of the listed slopes, we would encounter {prod([trees_in_line(grid,step) for step in input_2])} trees')
