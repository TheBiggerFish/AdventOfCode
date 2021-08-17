# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/1


from fishpy.geometry import Point

def turn_left(pt):
    return Point(-pt.y,pt.x)
    
def turn_right(pt):
    return Point(pt.y,-pt.x)

with open('2016/01/input.txt') as in_file:
    directions = in_file.readline().strip().split(', ')
    cur = Point(0,0)
    seen = {cur}
    facing = Point(0,1)
    for dir in directions:
        if dir[0] == 'L':
            facing = turn_left(facing)
        elif dir[0] == 'R':
            facing = turn_right(facing)
        found = False
        for i in range(int(dir[1:])):
            cur = cur + facing
            if cur in seen:
                found = True
                break
            seen.add(cur)
        if found:
            break
    print('The Easter Bunny Headquarters are {} blocks away.'.format(cur.manhattan_distance(Point(0,0))))