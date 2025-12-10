from fishpy.geometry import LatticePoint, Vector2D
from itertools import combinations
from fishpy.pathfinding.grid import Grid
from fishpy.pathfinding import Location

with open('input.txt') as f:
    lines = f.read().splitlines()
    red_tiles = list(map(lambda s: LatticePoint(*map(int, s.split(','))), lines))

def volume(p1: LatticePoint, p2: LatticePoint) -> int:
    return (abs(p1 - p2) + LatticePoint(1,1)).volume()

def normalize_rectangle(p1: LatticePoint, p2: LatticePoint) -> tuple[LatticePoint, LatticePoint]:
    x_left, x_right = sorted([p1.x, p2.x])
    y_bottom, y_top = sorted([p1.y, p2.y])
    return LatticePoint(x_left, y_bottom), LatticePoint(x_right, y_top)

rectangles = ((*normalize_rectangle(p1, p2), volume(p1, p2)) for p1, p2 in combinations(red_tiles, 2))
largest_rectangles = sorted(rectangles, reverse=True, key=lambda x: x[2])
print(f'Part 1: {largest_rectangles[0][2]}')

# Generate a list of rectangles that are outside the polygon formed by the red tiles. The red tiles are guaranteed to
# form a simple clock-wise polygon, so we can use the cross product to see if an angle is concave. The points of that
# angle can then be used as a boundary to ensure rectangles are strictly inside the polygon
outside_rectangles = []
for i in range(len(red_tiles)):
    p1, p2, p3 = red_tiles[i-2], red_tiles[i-1], red_tiles[i]
    v1, v2 = p2 - p1, p2 - p3
    cross = Vector2D.cross(v1, v2)
    if cross > 0:
        outside_rectangles.append(normalize_rectangle(p1, p3))

for p1, p2, v in largest_rectangles:
    p1, p2 = normalize_rectangle(p1, p2)
    # if the rectangle is overlapping with an outside rectangle (touching is okay), break out and continue
    for o_p1, o_p2 in outside_rectangles:
        if not (p2.x <= o_p1.x or p1.x >= o_p2.x or p2.y <= o_p1.y or p1.y >= o_p2.y):
            break
    else:
        # If we didn't break out of the inner loop, we found a valid rectangle
        break
print(f'Part 2: {v}')
