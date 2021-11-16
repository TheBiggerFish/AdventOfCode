# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/22


from fishpy.geometry import Point
from fishpy.pathfinding.grid import Grid

input = 'abcdefgh'
bounds = Point(37,27)
# bounds = Point(3,3)
target = Point(bounds.x-1,0)

class Node:
    def __init__(self,id:Point,size:int,used:int):
        self.id = id
        self.size = size
        self.used = used

    @property
    def avail(self):
        return self.size - self.used

    @property
    def used_percent(self):
        return int(self.used * 100 / self.size)

    def full(self):
        return self.used >= self.size

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        if self.id == Point(0,0):
            return ' O'
        elif self.id == target:
            return ' X'
        elif self.used > 90:
            return ' #'
        elif self.used == 0:
            return ' _'
        else:
            return str(self.avail).rjust(2,' ')

    def viable_pair(self,other):
        return self != other and self.used != 0 and self.used <= other.avail

    def print_string(self):
        return f'/dev/grid/node-x{self.id.x}-y{self.id.y}\t{self.size}T\t{self.used}T\t{self.avail}T\t{self.used_percent}%'

    @staticmethod
    def from_string(string:str):
        spl = string.strip().split()

        name = spl[0].split('-')
        x = int(name[1].lstrip('x'))
        y = int(name[2].lstrip('y'))
        pos = Point(x,y)

        size = int(spl[1].strip('T'))
        used = int(spl[2].strip('T'))

        return Node(pos,size,used)

    
with open('2016/22/input.txt') as f:
    lines = [line.strip() for line in f.readlines() if '/dev/grid' in line]
    grid = Grid.blank(bounds)

    for line in lines:
        node = Node.from_string(line.strip())
        grid[node.id] = node
    print(grid)

    count = 0
    for n1 in grid:
        for n2 in grid:
            if n1 != n2 and (n1.viable_pair(n2) or n2.viable_pair(n1)):
                count += 1
    print(count//2)
