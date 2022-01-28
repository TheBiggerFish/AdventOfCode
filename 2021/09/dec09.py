# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/9


from typing import Set
from queue import Queue

from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding import Location
from fishpy.structures import ReversiblePriorityQueue as PriorityQueue


def risk_level(grid:Grid,point:Location) -> int:
    for adj in point.get_adjacent_points(lower_bound=LatticePoint(0,0),upper_bound=grid.size):
        if grid[adj].rep <= point.rep:
            return 0
    return point.rep + 1

def basin_size(grid:Grid,point:Location,seen:Set) -> int:
    q = Queue()
    q.put(point)

    size = 0
    while not q.empty():
        pt:Location = q.get()
        if pt in seen or pt.rep == 9:
            continue
        seen.add(pt)
        size += 1

        for adj in pt.get_adjacent_points(lower_bound=LatticePoint(0,0),upper_bound=grid.size):
            q.put(grid[adj])
    return size


with open('2021/09/input.txt') as f:
    lines = [line.rstrip() for line in f]
    grid_body = [[int(col) for col in line] for line in lines]

    total_risk = 0
    grid = Grid.from_list_of_strings(grid_body)
    # for loc in grid:
    #     total_risk += risk_level(grid,loc)
    # print('The total risk level is',total_risk)

    # seen = set()
    # scores = PriorityQueue(max_=True)
    # for loc in grid:
    #     loc:Location
    #     if loc.rep == 9 or loc in seen:
    #         continue
    #     scores.put(basin_size(grid,loc,seen))

    print(grid.flood_fill(start=Location(0,0,Location.IMPASSABLE,rep=1),predicate_function=lambda pt: pt.rep == 9))
        
    # print('The basin score is',scores.get()*scores.get()*scores.get())
        