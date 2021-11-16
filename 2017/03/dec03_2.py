# Written by Cameron Haddock
# Written as a solution for Advent of Code 2017

# https://adventofcode.com/2017/day/3


from fishpy.geometry import Point, Vector
from fishpy.pathfinding.grid import ExpandableGrid


def is_square(n):
    return n**0.5 == int(n**0.5)

def is_odd_square(n):
    return is_square(n) and int(n**0.5)%2 == 1


input = 361527

i = 1
pos = Point(0,0)
step = Vector(1,0)
grid = ExpandableGrid([[1]])

next_val = 1
while next_val < input:
    if is_odd_square(i-1):
        grid.expand_right(1,fill_char=0)
        step = Vector(0,1)
    if is_even_square(i-1):
        
    i += 1
