# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/25


from fishpy.geometry import Point
from fishpy.numbers import triangle

def get_diagonal_from_coords(pt:Point) -> int:
    return pt.x + pt.y - 1

def cycle(iter,initial):
    for _ in range(1,iter):
        initial *= 252533
        initial %= 33554393
    return initial


pt = Point(3083,2978)
rt = get_diagonal_from_coords(pt)
print(cycle(triangle(rt-1)+pt.x,20151125))