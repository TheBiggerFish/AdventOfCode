# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/17


from hashlib import md5
from fishpy.geometry import Point
from fishpy.pathfinding import Dijkstra,DepthFirstTraversal

input = 'pxxbnzuo'

class State:
    WIDTH = 4
    HEIGHT = 4
    def __init__(self,pos:Point,path:str):
        self.pos = pos
        self.path = path
    
    def __str__(self):
        return f'Point={str(self.pos)}; Path={self.path}'

    def adjacents(self):
        path = self.path
        hash = self.hash
        adj = []
        for pos in self.pos.get_adjacent_points(diagonals=False,lower_bound=Point(0,0),upper_bound=Point(4,4)):
            if self.pos.is_above(pos) and hash[0] in 'bcdef':
                adj.append(State(pos,path+'U'))
            elif self.pos.is_below(pos) and hash[1] in 'bcdef':
                adj.append(State(pos,path+'D'))
            elif self.pos.is_right_of(pos) and hash[2] in 'bcdef':
                adj.append(State(pos,path+'L'))
            elif self.pos.is_left_of(pos) and hash[3] in 'bcdef':
                adj.append(State(pos,path+'R'))
        return adj

    def __eq__(self,other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.path)

    @property
    def hash(self):
        return md5((input + self.path).encode()).hexdigest()[:4]

start = State(Point(0,0),'')
target = State(Point(3,3),'')
d = Dijkstra(start,target,adjacency_function=State.adjacents)
print(d.search())


dft = DepthFirstTraversal(start,target,adjacency_function=State.adjacents,longest_path=True)
dft.execute() #Comment out return to make it work
distances = []
for key in dft.distance:
    if key == target:
        distances.append(dft.distance[key])
print(max(distances))
