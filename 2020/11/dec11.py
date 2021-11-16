# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/11


from fishpy.geometry import Point
from fishpy.pathfinding.grid import Grid

with open('2020/11/input.txt','r') as input_file:
    lines = [line.strip() for line in input_file]
grid1 = Grid.from_list_of_strings(lines,wall_char='')
grid2 = grid1.copy()

while True:
    copy = grid1.copy()
    for pt in copy:
        if pt.rep == '.':
            continue
        count_occupied = 0
        is_empty = pt.rep == 'L'
        for adj in pt.get_adjacent_points(diagonals=True,lower_bound=Point(0,0),upper_bound=grid1.bounds):
            if grid1[adj].rep == '#':
                count_occupied += 1
        if is_empty and count_occupied == 0:
            pt.rep = '#'
        elif not is_empty and count_occupied >= 4:
            pt.rep = 'L'
    if grid1 == copy:
        break
    grid1 = copy

print('Result 1:',len(grid1.char_positions(['#'])['#']))


def get_occupied_in_line(grid:Grid,start:Point):
    count = 0
    for dir in Point(0,0).get_adjacent_points(diagonals=True):
        cur = start
        while cur.in_bounds(lower_bound=Point(0,0),upper_bound=grid.bounds):
            if cur != start:
                if grid[cur].rep == '#':
                    count += 1
                    break
                elif grid[cur].rep == 'L':
                    break
            cur += dir
    return count

while True:
    copy = grid2.copy()
    for pt in copy:
        if pt.rep == '.':
            continue
        is_empty = pt.rep == 'L'
        count_occupied = get_occupied_in_line(grid2,pt)
        if is_empty and count_occupied == 0:
            pt.rep = '#'
        elif not is_empty and count_occupied >= 5:
            pt.rep = 'L'
    if grid2 == copy:
        break
    grid2 = copy

print('Result 2:',len(grid2.char_positions(['#'])['#']))
