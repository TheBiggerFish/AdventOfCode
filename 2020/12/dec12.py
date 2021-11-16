# Written by Cameron Haddock
# Written as a solution for Advent of Code 2020

# https://adventofcode.com/2020/day/12


from fishpy.geometry import Point

with open('2020/12/input.txt','r') as input_file:
    steps = [line.strip() for line in input_file]

pos = Point(0,0)
dir = Point(1,0)
for step in steps:
    action = step[0]
    value = int(step[1:])
    if action == 'R':
        while value != 0:
            dir = Point(dir.y,-dir.x)
            value -= 90
    elif action == 'L':
        while value != 0:
            dir = Point(-dir.y,dir.x)
            value -= 90
    elif action == 'F':
        pos += dir*value
    elif action == 'N':
        pos += Point(0,1) * value
    elif action == 'S':
        pos += Point(0,-1) * value
    elif action == 'E':
        pos += Point(1,0) * value
    elif action == 'W':
        pos += Point(-1,0) * value
print('Result 1:',pos.manhattan_distance(Point(0,0)))


ship = Point(0,0)
waypoint = Point(10,1)
for step in steps:
    action = step[0]
    value = int(step[1:])
    diff = waypoint - ship
    if action == 'R':
        while value != 0:
            diff = Point(diff.y,-diff.x)
            value -= 90
        waypoint = ship + diff
    elif action == 'L':
        while value != 0:
            diff = Point(-diff.y,diff.x)
            value -= 90
        waypoint = ship + diff
    elif action == 'F':
        while value != 0:
            ship += diff
            waypoint += diff
            value -= 1
    elif action == 'N':
        waypoint += Point(0,1) * value
    elif action == 'S':
        waypoint += Point(0,-1) * value
    elif action == 'E':
        waypoint += Point(1,0) * value
    elif action == 'W':
        waypoint += Point(-1,0) * value
print('Result 2:',ship.manhattan_distance(Point(0,0)))