# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/17


from fishpy.pathfinding import Location
from fishpy.pathfinding.grid import Grid
from fishpy.geometry import Point2D, Vector2D, LatticePoint
from fishpy.physics import Object
from fishpy.structures import Bounds


with open('2021/17/input.txt') as f:
    x,y = [part.split('..') for part in f.readline().rstrip()[15:].split(', y=')]
    low_p,high_p = Point2D(int(x[0]),int(y[0])),Point2D(int(x[1]),int(y[1]))
    target_bounds = Bounds(low_p,high_p,upper_inclusive=True)

max_height = 0
highest_v = None
total_success = 0
for v_x in range(5,51):
    for v_y in range(-267,268):
        a_x = 1 if v_x < 0 else -1
        object = Object(Point2D(0,0),Vector2D(v_x,v_y),Vector2D(a_x,-1))
        tent_max_height = max_height
        iterations = 0
        while object.position not in target_bounds and iterations < 270*2:
            object.step()
            if object.velocity.x == 0:
                object.acceleration.x = 0
            iterations += 1
            if object.position.y > tent_max_height:
                tent_max_height = object.position.y
        if object.position in target_bounds:
            total_success += 1
            if tent_max_height > max_height:
                max_height = tent_max_height
                highest_v = Vector2D(v_x,v_y)
print(highest_v,max_height)
print(total_success)
