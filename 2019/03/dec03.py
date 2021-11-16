# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/3


from fishpy.geometry import LineSegment, Point
from typing import List

dirs = {
    'U':Point(0,-1),
    'D':Point(0,1),
    'L':Point(-1,0),
    'R':Point(1,0)
}

def get_segments(wire_steps) -> List[LineSegment]:
    cur = Point(0,0)
    wire = []
    for step in wire_steps:
        dir = dirs[step[0]]
        distance = int(step[1:])
        next = dir * distance + cur
        wire.append(LineSegment(cur,next))
        cur = next
    return wire

with open('2019/03/input.txt') as f:
    wire1 = get_segments(f.readline().strip().split(','))
    wire2 = get_segments(f.readline().strip().split(','))

    distances = [Point(0,0).manhattan_distance(l1.intersection(l2)) for l1 in wire1 for l2 in wire2 if l1.intersects(l2)]
    print(min(distances))
