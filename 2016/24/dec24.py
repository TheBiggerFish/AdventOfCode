# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/24


from fishpy.geometry import Point
from fishpy.mathematics.graphs import PathGraph
from fishpy.pathfinding import Dijkstra
from fishpy.pathfinding.grid import Grid

with open('2016/24/input.txt') as f:
    grid = Grid.from_list_of_strings(f.read().strip().split('\n'))
    nodes = grid.char_positions([str(i) for i in range(8)])

    G = PathGraph()
    for node in nodes:
        G.add_node(node)
        
    validate = lambda pt: grid[pt].is_passible()
    weight = lambda n1,n2: Dijkstra(nodes[n1][0],nodes[n2][0],Point.get_adjacent_points,validate,Point.manhattan_distance).search()
    G.add_weighted_edges_for_complete(weight)
    run1 = G.get_length_of_path(G.complete_travelling_salesman(start='0'))
    run2 = G.get_length_of_path(G.complete_travelling_salesman(start='0',end='0'))

    print(f'Starting from location 0, the fewest number of steps required to visit every non-0 number marked on the map at least once is {run1}')
    print(f'The fewest number of steps required to start at 0 and visit every non-0 number marked on the map at least once, then return to 0 is {run2}')
