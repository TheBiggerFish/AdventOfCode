# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/15


from fishpy.geometry.lattice import LatticePoint
from fishpy.geometry.vector2d import Vector2D
from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding import Dijkstra
from fishpy.pathfinding.grid.expandablegrid import ExpandableGrid
from fishpy.pathfinding.location import Location



with open('2021/15/input.txt') as f:
    lines = [[int(char) for char in line] for line in f.read().rstrip().split()]

# Part 1

grid_1 = Grid.from_list_of_strings(lines)
adjacency_function = lambda point: LatticePoint.get_adjacent_points(
    point,lower_bound=grid_1.bounds[0],upper_bound=grid_1.bounds[1])
dijkstra = Dijkstra(LatticePoint(0,0),grid_1.size-LatticePoint(1,1),
            adjacency_function=adjacency_function,
            heuristic_function=LatticePoint.manhattan_distance,
            cost_function=lambda _,new: grid_1[new].rep)
print(dijkstra.search())


# Part 2

grid_2 = ExpandableGrid.blank(LatticePoint(1,1),LatticePoint(0,0))
grid_2_overlay = ExpandableGrid.from_list_of_strings(lines)
grid_2_layout = (5,5)
for grid_x in range(grid_2_layout[0]):
    for grid_y in range(grid_2_layout[1]):
        copy = grid_2_overlay.copy()
        for loc in copy:
            loc:Location
            loc.rep += grid_x + grid_y
            if loc.rep >= 10:
                loc.rep %= 9
                if loc.rep == 0:
                    loc.rep = 1
        grid_2 = grid_2.overlay(copy.shift(Vector2D(grid_x,grid_y)*grid_2_overlay.width))

adjacency_function = lambda point: LatticePoint.get_adjacent_points(
    point,lower_bound=LatticePoint(0,0),upper_bound=grid_2.size)
dijkstra = Dijkstra(LatticePoint(0,0),grid_2.size-LatticePoint(1,1),
            adjacency_function=adjacency_function,
            heuristic_function=LatticePoint.manhattan_distance,
            cost_function=lambda _,new: grid_2[new].rep)
print(dijkstra.search())