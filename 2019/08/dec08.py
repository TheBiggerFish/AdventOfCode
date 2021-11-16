# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/8

from fishpy.geometry import Point, Vector
from fishpy.pathfinding.grid import Grid

BOUNDS = Vector(25,6)

with open('2019/08/input.txt') as f:
    #Generate layers
    layers = []
    end = False
    while True:
        layer = []
        for y in range(BOUNDS.y):
            row = []
            for x in range(BOUNDS.x):
                if c := f.read(1):
                    row.append(c)
                else:
                    end = True
                    break
            if end:
                break
            layer.append(row)
        if end:
            break
        layers.append(Grid.from_list_of_strings([''.join(row) for row in layer]))


    # Verify image not corrupted
    min = (-1,10**6)
    for i in range(len(layers)):
        zeros = len(layers[i].char_positions(['0'])['0'])
        if zeros < min[1]:
            min = (i,zeros)
    counts = layers[min[0]].char_positions(['1','2'])
    print(len(counts['1']) * len(counts['2']))


    # Decode image
    final = []
    for y in range(BOUNDS.y):
        row = ''
        for x in range(BOUNDS.x):
            pt = Point(x,y)
            which = 0
            while layers[which][pt].rep == '2':
                which += 1
            if layers[which][pt].rep == '1':
                row += '@'
            else:
                row += ' '
        final.append(row)
    final = Grid.from_list_of_strings(final)
    print(final)
