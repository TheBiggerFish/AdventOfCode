# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/10


import re
from typing import List

from fishpy import physics
from fishpy.geometry import Point, Vector
from fishpy.pathfinding.grid import Grid

input_file = '2018/10/input.txt'

with open(input_file) as f:
    lights:List[physics.Object] = []
    for line in f:
        line = re.split('<|,|>',line)
        pos = Point(int(line[1]),int(line[2]))  
        vel = Vector(int(line[4]),int(line[5]))
        lights.append(physics.Object(pos,vel))
    
    step = 0
    for i in range(10710):
        for light in lights:
            light.step()
        step += 1
        if step % 1000 == 0:
            print(step)
    print(step)
    g = Grid.blank(Point(68,16),offset=Point(184,190)).conditional_walls(lambda obj: obj in {light.position for light in lights},char='#')
    print(g)
