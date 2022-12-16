from fishpy.geometry import Direction, LatticePoint, Vector2D
from fishpy.pathfinding.grid import Grid

directions = [Direction.UP,
              Direction.UP + Direction.LEFT,
              Direction.UP + Direction.RIGHT]


def draw_grid(lines: list[str], floor: bool = False) -> Grid:
    '''Build the grid based on cave walls'''
    g = Grid.blank(bounds=LatticePoint(400, 162), offset=LatticePoint(300, 0))
    g[source].rep = '+'
    for line in lines:
        points = list(map(lambda x: LatticePoint(*map(int, x.split(','))),
                          line.split('->')))
        for i, point_i in enumerate(points[:-1]):
            diff = points[i+1] - point_i
            count = abs(diff.x or diff.y)
            step = diff // count
            g.draw('#', point_i, step, count)
    if floor:
        start = LatticePoint(g.offset.x, g.bounds[1].y-1)
        g.draw('#', start, Vector2D(1, 0), g.width)
    return g


def fill_sand(g: Grid, source: LatticePoint, n: int) -> int:
    '''Drop n sand particles into the grid from the source node'''
    for i in range(n):
        sand = source.copy()
        while True:
            moved = False
            for dir in directions:
                next_ = sand + dir
                if next_ not in g:
                    return i
                if g[next_].rep == '.':
                    sand = next_
                    moved = True
                    break
            if not moved:
                if sand == source:
                    return i+1
                g[sand].rep = 'o'
                break
    return -1


source = LatticePoint(500, 0)
with open('2022/14/input.txt') as f:
    lines = f.read().splitlines()

g_1 = draw_grid(lines,)
result = fill_sand(g_1, source, 1000)
print(result)

with open('2022/14/output_1.txt', 'w+') as f:
    f.writelines(g_1.to_string(''))

g_2 = draw_grid(lines, True)
result = fill_sand(g_2, source, 2*g_2.height**2)
print(result)

with open('2022/14/output_2.txt', 'w+') as f:
    f.writelines(g_2.to_string(''))
