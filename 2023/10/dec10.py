from fishpy.geometry import LatticePoint, Vector2D
from fishpy.pathfinding import Location
from fishpy.pathfinding.grid import Grid

UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)

pipes: dict[str, tuple[Vector2D, Vector2D]] = {
    '|': (UP, DOWN),
    'J': (UP, LEFT),
    'L': (UP, RIGHT),
    '7': (DOWN, LEFT),
    'F': (DOWN, RIGHT),
    '-': (LEFT, RIGHT),
    '.': ()
}

def start_char(grid: Grid, pos: LatticePoint) -> str:
    """Find pipe shape hidden by starting 'S' character"""
    down = UP in pipes[grid[pos.up()].rep] if pos.up() in grid else False
    up = DOWN in pipes[grid[pos.down()].rep] if pos.down() in grid else False
    right = LEFT in pipes[grid[pos.right()].rep] if pos.right() in grid else False
    left = RIGHT in pipes[grid[pos.left()].rep] if pos.left() in grid else False
    
    if up and down:
        return '|'
    elif up and left:
        return '7'
    elif up and right:
        return 'L'
    elif down and left:
        return '7'
    elif down and right:
        return 'F'
    elif left and right:
        return '-'
    else:
        raise Exception('Is this real life?')

def neighbors(grid: Grid, pos: LatticePoint) -> tuple[LatticePoint,LatticePoint]:
    """Determine the true neighbors of 'pos' based on it's pipe shape"""
    directions = pipes[grid[pos].rep]
    return pos + directions[0], pos + directions[1]

def loop_cells(grid: Grid, start: LatticePoint) -> set[LatticePoint]:
    """Determine all cells that form the loop"""
    seen: set[LatticePoint] = {start}
    dist = 0
    cur = start
    while True:
        n1, n2 = neighbors(grid, cur)
        cur = n1 if n1 not in seen else n2 if n2 not in seen else start
        if cur == start:
            break
        seen.add(cur)
        dist += 1
    return seen

def cells_within(grid: Grid) -> set[LatticePoint]:
    """
        Return all cells that are enclosed by the loop
        Use a method similar to the ray-casting algorithm to determine if a cell is enclosed
        A cell which has an odd number of walls to its left is enclosed
        
        The main difficulty comes from corners. 
        If two corners go back on each other (LJ or F7), then it counts as 0/2 walls (parity is all that matters)
        If two corners contribute vertically (FJ or L7), then it counts as 1 wall
    """
    within: set[LatticePoint] = set()
    for row in grid.grid:
        walls = 0
        prev_wall = ''
        for cell in row:
            if cell.rep == '-':
                continue
            elif cell.rep == '|':
                walls += 1
            elif cell.rep == '.':
                if walls % 2 == 1:
                    within.add(LatticePoint(cell.x, cell.y))
            else: #cell.rep in 'LJ7F'
                if prev_wall:
                    prev_dirs = pipes[prev_wall]
                    cell_dirs = pipes[cell.rep]
                    if (UP in prev_dirs and DOWN in cell_dirs) or (DOWN in prev_dirs and UP in cell_dirs):
                        walls += 1
                    prev_wall = ''
                else:
                    prev_wall = cell.rep
    
    return within

def main():
    with open('2023/10/input.txt') as f:
        lines = f.read().splitlines()
        
    grid = Grid.from_list_of_strings(lines)
    start = grid.char_positions('S')['S'][0]
    grid[start].rep = start_char(grid, start)
    
    loop: set[LatticePoint] = loop_cells(grid, start)
    print(f'Furthest cell from start is {len(loop) // 2} steps')
    
    # Clear all cells not part of the loop
    grid = grid.conditional_walls(lambda cell: cell not in loop, '.')
    
    contained = cells_within(grid)
    print(f'There are {len(contained)} cells fully contained within the loop')
    



if __name__ == '__main__':
    main()
