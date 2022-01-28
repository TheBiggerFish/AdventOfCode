# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/5


from typing import List

from fishpy.geometry import LatticePoint, LineSegment

with open('2021/05/input.txt') as f:
    lines = f.read().rstrip().split('\n')
    straights:List[LineSegment] = []
    diagonals:List[LineSegment] = []
    for line in lines:
        left = line.split(' -> ')[0].split(',')
        right = line.split(' -> ')[1].split(',')
        left_point = LatticePoint(int(left[0]),int(left[1]))
        right_point = LatticePoint(int(right[0]),int(right[1]))
        segment = LineSegment(left_point,right_point)
        if left_point.x == right_point.x or left_point.y == right_point.y:
            straights.append(segment)
        else:
            diagonals.append(segment)

    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for segment in straights:
        for pt in segment.lattice_points_along():
            grid[pt.y][pt.x] += 1
    count_1 = sum(1 for row in grid for col in row if col >= 2)

    for segment in diagonals:
        for pt in segment.lattice_points_along():
            grid[pt.y][pt.x] += 1
    count_2 = sum(1 for row in grid for col in row if col >= 2)

    print(f'There are {count_1} intersection points of orthogonal lines')
    print(f'There are {count_2} intersection points of all lines')
