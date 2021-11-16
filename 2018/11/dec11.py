# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/11


from fishpy.geometry import Point
from fishpy.pathfinding import Location
from fishpy.pathfinding.grid import Grid


class FuelCell:
    def __init__(self,pos:Point,grid_serial:int):
        self._pos = pos
        self._grid_serial = grid_serial
        self.rack_id = pos.x + 10
        self.power = (pos.y * self.rack_id + grid_serial) * self.rack_id // 100 % 10 - 5

    def copy(self):
        return FuelCell(self._pos,self._grid_serial)

input = 9798
BOUNDS = Point(300,300)

values = [[FuelCell(Point(x,y),input) for x in range(BOUNDS.x)] for y in range(BOUNDS.y)]
# values = [[Location(x,y,Location.OPEN,rep=FuelCell(Point(x,y),input)) for x in range(BOUNDS.x)] for y in range(BOUNDS.y)]

g = Grid(values)
largest = (0,Point(0,0))
for x in range(BOUNDS.x-3):
    for y in range(BOUNDS.y-3):
        sg = g.subgrid(Point(x,y),Point(x+3,y+3))
        value = 0
        for pos in sg:
            value += pos.power
        current = (value,Point(x,y))
        largest = max(largest,current)
print(largest[1])



starting_size = 1
for s in range(starting_size,20):
    largest = (1,Point(0,0))
    for x in range(BOUNDS.x-s+1):
        for y in range(BOUNDS.y-s+1):
            sg = g.subgrid(Point(x,y),Point(x+s,y+s),reference=True)
            value = 0
            for pos in sg:
                value += pos.power
            current = (value,Point(x,y))
            largest = max(largest,current)
            
    print(s,largest[0],largest[1],f'Creating {(BOUNDS.x-s+1)*(BOUNDS.y-s+1)} of size {s}x{s}={s*s}, total items {(BOUNDS.x-s+1)*(BOUNDS.y-s+1)*s*s}')
