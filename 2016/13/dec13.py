# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/13


from EulerLib.geometry import Point
from queue import PriorityQueue

input = 1358
target = Point(31,39)
start = Point(1,1)
bounds = Point(50,50)
max_flood_steps = 50
grid = []


def is_open_space(pt:Point) -> bool:
    val = pt.x*pt.x + 3*pt.x + 2*pt.x*pt.y + pt.y + pt.y*pt.y + input
    bin = f'{val:b}'
    return bin.count('1') % 2 == 0

def generate_grid(bounds:Point) -> list:
    grid = []
    for y in range(bounds.y):
        row = []
        for x in range(bounds.x):
            pt = Point(x,y)
            if is_open_space(pt):
                row.append('.')
            else:
                row.append('#')
        grid.append(row)
    return grid

def get_path(prev:dict,cur:Point) -> list:
    lst = [cur]
    while cur != start:
        grid[cur.y][cur.x] = 'O'
        cur = prev[cur]
        lst.append(cur)
    grid[cur.y][cur.x] = 'O'
    return lst

def dijkstra() -> int:
    prev = {}
    q = PriorityQueue()
    q.put((0,start.copy()))
    seen = set()
    while not q.empty():
        tup = q.get()
        g = tup[0]
        cur = tup[1]

        if cur in seen:
            continue
        seen.add(cur)

        if cur == target:
            return len(get_path(prev,cur)) - 1

        for pt in cur.get_adjacent_points(lower_bound=Point(0,0),upper_bound=bounds):
            if pt not in seen and grid[pt.y][pt.x] == '.':
                prev[pt] = cur
                q.put((g+1,pt))
    return -1

def flood_fill(fill_char:str) -> int:
    filled = set()
    wall = set()
    next = PriorityQueue()
    next.put((0,start))
    while not next.empty():
        tup = next.get()
        g = tup[0]
        cur = tup[1]
        if cur in wall or cur in filled or g > max_flood_steps:
            continue
        if grid[cur.y][cur.x] != '#':
            filled.add(cur)
            for tup in [(g+1,adj) for adj in cur.get_adjacent_points(lower_bound=Point(0,0),upper_bound=bounds)]:
                next.put(tup)
            grid[cur.y][cur.x] = fill_char
        else:
            wall.add(cur)
    return len(filled)


grid = generate_grid(bounds)
print(f'The length of the path to the target is {dijkstra()} steps')
# for row in grid:
#     print(' '.join(row))
    
grid = generate_grid(bounds)
print(f'There are {flood_fill("*")} locations within {max_flood_steps} steps of the start')
# for row in grid:
#     print(' '.join(row))