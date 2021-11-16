# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/17


from copy import deepcopy
from sys import stdout

from fishpy.geometry import Point, PointND
from fishpy.pathfinding.grid import Grid, Grid3D

ITERATIONS = 6
with open('2020/17/input.txt','r') as input_file:
    layout = input_file.read().split('\n')[:-1]

g = Grid3D.from_list_of_list_of_strings([layout])
for _ in range(ITERATIONS):
    g.expand_up(1)
    g.expand_down(1)
    g.expand_left(1)
    g.expand_right(1)
    g.expand_in(1)
    g.expand_out(1)

    grid_copy = g.copy()
    for pt in g:
        adj = pt.get_adjacent_points(diagonals=True,lower_bound=g._offset,upper_bound=g._offset+g.bounds)
        count = len([a for a in adj if g[a].rep=='#'])
        if g[pt].rep == '.':
            if count == 3:
                grid_copy[pt].rep = '#'
        else:
            if count not in {2,3}:
                grid_copy[pt].rep = '.'
    g = grid_copy
print('Result 1:',len([str(pt) for pt in g.char_positions('#')['#']]))


g = Grid.from_list_of_strings(layout,offset=Point(-3,-3))
side = len(layout[0]) + ITERATIONS*2
min_,max_ = -side//2+1,side//2+1

mat = [[[[g[Point(x,y)].rep if z==w==0 and Point(x,y) in g else '.' for x in range(min_,max_)] for y in range(min_,max_)] for z in range(min_,max_)] for w in range(min_,max_)]
min_bound,max_bound = PointND([0,0,0,0]),PointND([20,20,20,20])
bounds_function = lambda pt: min_bound <= pt < max_bound


final_count = len(g.char_positions(['#'])['#'])
for i in range(ITERATIONS):
    print(f'Count after {i} rounds is {final_count}')
    mat_copy = deepcopy(mat)
    for i_w in range(side):
        print('.',end='')
        stdout.flush()
        for i_z in range(side):
            for i_y in range(side):
                for i_x in range(side):
                    count = 0
                    for pt in PointND([i_x,i_y,i_z,i_w]).get_adjacent_points(bounds_function):
                        if mat[pt.w][pt.z][pt.y][pt.x] == '#':
                            count += 1
                        if count > 3:
                            break
                    if mat[i_w][i_z][i_y][i_x] == '#' and count not in {2,3}:
                        mat_copy[i_w][i_z][i_y][i_x] = '.'
                        final_count -= 1
                    elif mat[i_w][i_z][i_y][i_x] == '.' and count == 3:
                        mat_copy[i_w][i_z][i_y][i_x] = '#'
                        final_count += 1
    mat = mat_copy
    print()

print('Result 2:',final_count)
