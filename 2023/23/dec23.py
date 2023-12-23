from itertools import pairwise
from queue import Queue

import networkx as nx
from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid
from fishpy.utility import timer

SLOPES = {
    '>': LatticePoint(1, 0),
    '<': LatticePoint(-1, 0),
    'v': LatticePoint(0, 1),
    '^': LatticePoint(0, -1),
}


def get_adjacent_points(pt: LatticePoint, grid: Grid) -> set[LatticePoint]:
    """Returns the adjacent lattice points of a given point"""
    loc = grid[pt]
    if loc.rep == '.':
        potential = pt.get_adjacent_points(lower_bound=grid.bounds[0],
                                           upper_bound=grid.bounds[1])
        return set(filter(lambda pt: pt in grid and grid[pt].rep != '#', potential))
    elif loc.rep in SLOPES:
        return {pt + SLOPES[loc.rep]}
    raise NotImplementedError('How did I get here?')


def find_intersections(grid: Grid) -> set[LatticePoint]:
    """Find all intersection points in the input grid"""
    intersections: set[LatticePoint] = set()
    for cell in grid:
        pos = LatticePoint(cell.x, cell.y)
        sides = 0
        for adj in pos.get_adjacent_points(grid):
            if adj not in grid:
                continue
            if grid[adj].rep in SLOPES:
                sides += 1
        if sides >= 3:
            intersections.add(pos)
    return intersections


def find_next_intersections(start: LatticePoint, intersections: set[LatticePoint], grid: Grid) -> list[tuple[LatticePoint, int]]:
    """
        Use a breadth-first search to find all intersections that can be 
        reached from the starting point without passing through another 
        intersection. This is used to build the digraph
    """

    q: Queue[LatticePoint] = Queue()
    q.put((start, 0))
    seen: set[LatticePoint] = set()
    
    connected_intersections: list[tuple[LatticePoint, int]] = []
    pos: LatticePoint
    while not q.empty():
        pos, distance = q.get()
        if pos in seen:
            continue
        seen.add(pos)
        
        if pos != start and pos in intersections:
            connected_intersections.append((pos, distance))
            continue
        
        for adj in get_adjacent_points(pos, grid):
            if adj in seen:
                continue
            q.put((adj, distance + 1))
    return connected_intersections


def path_length(graph: nx.Graph, edges: list[tuple[int, int]]):
    """Find the length of a given set of edges"""
    length = 0
    for edge in pairwise(edges):
        length += graph.get_edge_data(*edge)['weight']
    return length


@timer
def longest_cyclic_path(graph: nx.Graph, start: int, end: int):
    """Find the longest path between start and end nodes in the graph"""
    longest = 0
    i = 0
    for path in nx.all_simple_paths(graph, source=start, target=end):
        if i % 50000 == 0:
            print(f'Still running, checking path {i}')
        i += 1

        length = path_length(graph, path)
        if length > longest:
            longest = length
    return longest


def main():
    with open('2023/23/input.txt') as f:
        lines = f.read().splitlines()

    grid = Grid.from_list_of_strings(lines)
    start, end = LatticePoint(1, 0), LatticePoint(139, 140)
    intersections = find_intersections(grid) | {start, end}
    
    # Assign each intersection an index to optimize graph operations
    indices = {pt: i for i, pt in enumerate(intersections)}
    
    # Add edges to both graphs
    digraph = nx.DiGraph()
    cyclic_graph = nx.Graph()
    for intersection in intersections:
        for next_, distance in find_next_intersections(intersection, intersections, grid):
            digraph.add_edge(indices[intersection], indices[next_], weight=distance)
            cyclic_graph.add_edge(indices[intersection], indices[next_], weight=distance)

    # Find longest path in a dag for part 1
    path = nx.dag_longest_path(digraph)
    length = path_length(digraph, path)
    print(f'The longest walk with slopes is {length} steps')

    longest = longest_cyclic_path(cyclic_graph, indices[start], indices[end])
    print(f'The longest walk without slopes is {longest} steps')


if __name__ == '__main__':
    main()
