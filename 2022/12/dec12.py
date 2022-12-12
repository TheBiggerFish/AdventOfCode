from fishpy.geometry import LatticePoint
from fishpy.pathfinding import dijkstra
from fishpy.pathfinding.grid import Grid


def accessible(pt: LatticePoint, neighbor: LatticePoint) -> bool:
    if grid[neighbor].rep == 'E' and grid[pt].rep in 'yz':
        return True
    if grid[pt].rep == 'S' and grid[neighbor].rep in 'ab':
        return True
    plus_one = chr(ord(grid[pt].rep)+1)
    return 'a' <= grid[neighbor].rep <= plus_one


def adjacent(pt: LatticePoint) -> list[LatticePoint]:
    return pt.get_adjacent_points(lower_bound=LatticePoint(0, 0), upper_bound=grid.size)


with open('2022/12/input.txt') as f:
    grid = Grid.from_list_of_strings(f.read().splitlines())
    start = grid.char_positions('S')['S'][0]
    end = grid.char_positions('E')['E'][0]

    cost, prev = dijkstra(start, end,
                          adjacency_function=adjacent,
                          validation_function=accessible,
                          heuristic_function=LatticePoint.manhattan_distance)
    print(f'Best cost from initial start location: {cost}')

    starts = LatticePoint.bounded_filter(grid.char_positions('a')['a'],
                                         lower_bound=LatticePoint(0, 0),
                                         upper_bound=LatticePoint(1, 35))
    print(f'{len(starts)} valid start locations with elevation \'a\'')

    current_best = cost
    for start in starts:
        cost, prev = dijkstra(start, end, max_cost=current_best,
                              adjacency_function=adjacent,
                              validation_function=accessible,
                              heuristic_function=LatticePoint.manhattan_distance)
        if 0 < cost < current_best:
            current_best = cost
    print(f'Best cost from any \'a\' location: {current_best}')
