# Written by Cameron Haddock
# Written as a solution for Advent of Code 2015

# https://adventofcode.com/2015/day/18


import pyglet
from pyglet.gl import glClearColor,glClear,GL_COLOR_BUFFER_BIT
from EulerLib.geometry import Point

width, height = 1000,1000
window = pyglet.window.Window(width=width,height=height,resizable=True)
batch = pyglet.graphics.Batch()
grid = [[pyglet.shapes.Rectangle(x*10+1, y*10+1, 8, 8, color=(0, 0, 0), batch=batch) for x in range(100)] for y in range(100)]
iterations = -1


class Animation:
    def __init__(self,grid):
        self.grid = grid

    def set_point(self,p:Point,value):
        self.grid[p.y][p.x] = value

    def get_point(self,p:Point) -> str:
        return self.grid[p.y][p.x]

    def point_is_on(self,p:Point) -> bool:
        return self.get_point(p) == '#'

    @staticmethod
    def create_from_file(filename):
        with open(filename) as in_file:
            return Animation([list(line.strip()) for line in in_file])

    def __str__(self) -> str:
        return '\n'.join([''.join(line) for line in self.grid])

    @property
    def width(self) -> int:
        return len(self.grid[0])
    
    @property
    def height(self) -> int:
        return len(self.grid)

    def copy(self):
        grid = [['.'] * self.width for _ in range(self.height)]
        new = Animation(grid)
        for x in range(self.width):
            for y in range(self.height):
                p = Point(x,y)
                new.set_point(p,self.get_point(p))
        return new


    def next_state(self,reps=1,corners=False):
        new = self
        for _ in range(reps):
            old = new
            new = new.copy()
            for x in range(self.width):
                for y in range(self.height):
                    p = Point(x,y)
                    adj = p.get_adjacent_points(diagonals=True,lower_bound=Point(0,0),upper_bound=Point(old.width,old.height))
                    num_on = sum([old.point_is_on(neighbor) for neighbor in adj])
                    if old.point_is_on(p):
                        if 2 <= num_on <= 3:
                            new.set_point(p,'#')
                        else:
                            new.set_point(p,'.')
                    else:
                        if num_on == 3:
                            new.set_point(p,'#')
                        else:
                            new.set_point(p,'.')
            if corners:
                new.set_point(Point(0,0),'#')
                new.set_point(Point(new.width-1,0),'#')
                new.set_point(Point(0,new.height-1),'#')
                new.set_point(Point(new.width-1,new.height-1),'#')
        return new
    
    def count_on(self):
        return sum([col=='#' for row in self.grid for col in row])


@window.event
def on_draw():
    window.clear()
    batch.draw()


i = 0
anim = Animation.create_from_file('2015/18/input.txt')
def update(_):
    global anim, i
    if i < iterations or iterations == -1:
        anim = anim.next_state(corners=True)
    
    
        for y in range(100):
            for x in range(100):
                grid[y][x].color = (255,255,0) if anim.point_is_on(Point(x,y)) else (0,0,0)
    i += 1
    print(f'After {i} iterations, there are {anim.count_on()} lights on.')
    

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1)
    pyglet.app.run()