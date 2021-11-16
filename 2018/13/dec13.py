# Written by Cameron Haddock
# Written as a solution for Advent of Code 2018

# https://adventofcode.com/2018/day/13


from fishpy.geometry import Point
from fishpy.pathfinding.grid import Grid

input = '2018/13/input.txt'


class Track:
    def __init__(self,pos:Point,size:Point):
        self.pos = pos
        self.size = size
    
    def length(self):
        return self.size.x*2 + self.size.y*2
    
    def get_bot_pos(self,bot_steps):
        pos = self.pos.copy()
        if bot_steps > self.size.x:
            bot_steps -= self.size.x
            pos += Point(self.size.x,0)
        if bot_steps > self.size.y:
            bot_steps -= self.size.y
            pos += Point(0,self.size.y)
        if bot_steps > self.size.x:
            bot_steps -= self.size.x
            pos -= Point(self.size.x,0)
        if bot_steps > self.size.y:
            bot_steps -= self.size.y
            pos -= Point(0,self.size.y)
        return pos

class Bot:
    def __init__(self,dir:str,pos:int,track_length:int):
        self.dir = dir
        self.pos = pos
        self.track_size = track_length

    def step(self):
        if self.dir == 'c':
            self.pos = (self.pos + 1) % self.track_size
        elif self.dir == 'ac':
            self.pos = (self.pos - 1) % self.track_size

with open(input) as f:
    grid = Grid.from_list_of_strings([line.strip('\n') for line in f])
    for loc in grid:
        if loc.rep in '^v<>':
            u = loc.up() in grid and grid[loc.up()].rep in '|+'
            d = loc.down() in grid and grid[loc.down()].rep in '|+'
            l = loc.left() in grid and grid[loc.left()].rep in '-+'
            r = loc.right() in grid and grid[loc.right()].rep in '-+'
            v = u and d
            h = l and r
            if v and h:
                loc.rep = '+'
            elif v:
                loc.rep = '|'
            elif h:
                loc.rep = '-'
            else:
                print(loc)

    print(grid.to_string(''))
