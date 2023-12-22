from fishpy.geometry import LatticePoint
from fishpy.pathfinding.grid import Grid

"""
Types and counts of 'Cards', where each 'Card' is a single instance of the input grid

          O S O
        O E 1 E O
      O E 1 0 1 E O
    O E 1 0 1 0 1 E O
    S 1 0 1 C 1 0 1 S
    O E 1 0 1 0 1 E O
      O E 1 0 1 E O
        O E 1 E O 
          O S O

C: center (1) = some large odd number of cycles, stop counting after a while
S: far side (4) = 65 steps in from middle of respective side
O: outer ring odd = 65 steps in from respective corner
E: outer ring even = 131+65 steps in from respective corner
0: cell marked here as even, technically an odd number of steps overall, but only an even number within 'Card'
1: cell marked here as odd, technically an even number of steps overall, but only an odd number within 'Card'

O/E/0/1 cards are counted in terms of rings, where each ring has 4*d entries where d is the manhattan distance of each entry from the central card
"""


def exact_flood_fill(grid: Grid, start: LatticePoint, steps: int) -> set[LatticePoint]:
    """
        Return the set of points that can be reached from start after exactly the input number of steps
        Each iteration, only step out from plots that were new in the last step (on the edge)
    """
    plots: dict[int, set[LatticePoint]] = {0: set(), 1: set()}
    edge_plots: set[LatticePoint] = {start}
    for i in range(1, steps+1):
        new_plots: set[LatticePoint] = set()
        for plot in edge_plots:
            for adj in plot.get_adjacent_points(lower_bound=grid.bounds[0], upper_bound=grid.bounds[1]):
                if grid[adj].rep == '.':
                    new_plots.add(adj)
        edge_plots = new_plots - plots[i%2]
        plots[i%2] |= new_plots
    return plots[steps%2]


def main():
    with open('2023/21/input.txt') as f:
        lines = f.read().splitlines()
    
    grid = Grid.from_list_of_strings(lines)
    start = grid.char_positions('S')['S'].pop()
    grid[start].rep = '.'
    
    near_steps = 64
    plots = exact_flood_fill(grid, start, steps=near_steps)
    print(f'The elf could reach {len(plots)} garden plots after {near_steps} steps')
    
    #65+even=7520, 65+odd=7457
    filled_even = len(exact_flood_fill(grid, start, steps=(65+131+131))) #7520
    filled_odd = len(exact_flood_fill(grid, start, steps=(65+131+131+1))) #7457
    
    far_left = len(exact_flood_fill(grid, LatticePoint(131, 65), steps=131))
    far_right = len(exact_flood_fill(grid, LatticePoint(-1, 65), steps=131))
    far_up = len(exact_flood_fill(grid, LatticePoint(65, 131), steps=131))
    far_down = len(exact_flood_fill(grid, LatticePoint(65, -1), steps=131))

    far_bottom_right_odd = len(exact_flood_fill(grid, LatticePoint(-1,0), steps=65))
    far_top_right_odd = len(exact_flood_fill(grid, LatticePoint(-1,130), steps=65))
    far_bottom_left_odd = len(exact_flood_fill(grid, LatticePoint(131,0), steps=65))
    far_top_left_odd = len(exact_flood_fill(grid, LatticePoint(131,130), steps=65))

    far_bottom_right_even = len(exact_flood_fill(grid, LatticePoint(-1,0), steps=(131 + 65)))
    far_top_right_even = len(exact_flood_fill(grid, LatticePoint(-1,130), steps=(131 + 65)))
    far_bottom_left_even = len(exact_flood_fill(grid, LatticePoint(131,0), steps=(131 + 65)))
    far_top_left_even = len(exact_flood_fill(grid, LatticePoint(131,130), steps=(131 + 65)))
    
    far_steps = 26501365
    options = filled_even # center
    options += far_left + far_right + far_up + far_down
    
    ortho = (far_steps - 65) // 131  #  =202300
    for ring in range(1,ortho):
        if ring%2 == 0:
            options += 4 * ring * filled_even
        else:
            options += 4 * ring * filled_odd

    # Outer ring even
    options += (ortho-1) * (far_bottom_right_even + far_top_right_even + far_bottom_left_even + far_top_left_even)
    # Outer ring odd
    options += ortho * (far_bottom_right_odd + far_top_right_odd + far_bottom_left_odd + far_top_left_odd)
    
    print(f'The elf could reach {options} garden plots after {far_steps} steps')
    
    


if __name__ == '__main__':
    main()
