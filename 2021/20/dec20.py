# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/20


from fishpy.geometry.point import Point
from fishpy.pathfinding.grid import ExpandableGrid
from fishpy.pathfinding import Location
from fishpy.geometry import LatticePoint


iterations = 50

class InfiniteGrid(ExpandableGrid):
    _adj = [LatticePoint(-1,-1),LatticePoint(0,-1),LatticePoint(1,-1),
            LatticePoint(-1,0),LatticePoint(0,0),LatticePoint(1,0),
            LatticePoint(-1,1),LatticePoint(0,1),LatticePoint(1,1)]

    def get(self,pt:LatticePoint,default:str='.') -> Location:
        if not isinstance(pt,LatticePoint):
            raise TypeError(f'Grid accessor must be of type Point, type {type(pt)} provided')
        if pt not in self:
            return Location(pt.x,pt.y,loc_type=Location.OPEN,rep=default)
        return self.grid[pt.y-self.offset.y][pt.x-self.offset.x]

    def get_pixel_details(self,pt:LatticePoint,which:int) -> str:
        rv = ''
        char = '.' if which%2==0 else '#'
        for adj in InfiniteGrid._adj:
            rv += '1' if self.get(pt + adj,char).rep == '#' else '0'
        return int(rv,2)

with open('2021/20/input.txt') as f:
    pixel_key = f.readline().rstrip()
    f.readline()
    grid = InfiniteGrid.from_list_of_strings(f.read().rstrip().split())
    grid = grid.expand_all(iterations,'.')
    # input(grid.to_string(''))
    for i in range(iterations):
        print(i)
        copy = grid.copy()
        for pt in grid:
            key = grid.get_pixel_details(pt,i)
            copy.get(pt).rep = pixel_key[key]
        grid = copy
        # input(grid.to_string(''))
    # low,high = grid.bounds
    # print(grid.offset)
    print(len(grid.char_positions(['#'])['#']))