from fishpy.geometry import LatticePoint
from fishpy.geometry.d2 import Direction
from fishpy.pathfinding.grid import Grid


def main():
    with open('2023/03/input.txt') as f:
        lines = f.read().splitlines()
        grid = Grid.from_list_of_strings(lines)

    symbols = {cell.rep for cell in grid if not cell.rep.isdigit()}
    symbols.remove('.')
    symbol_pos_nested = grid.char_positions(symbols).values()

    # symbol_pos reflects a complete list of cells containing symbols
    symbol_pos: list[LatticePoint] = [cell
                                      for row in symbol_pos_nested
                                      for cell in row]

    part_numbers: list[int] = []
    gear_ratios: list[int] = []

    for symbol in symbol_pos:
        adj_points = symbol.get_adjacent_points(diagonals=True,
                                                lower_bound=LatticePoint(0, 0),
                                                upper_bound=grid.bounds[1])
        adjacent_numbers: list[int] = []
        used: set[LatticePoint] = set()
        for adj in adj_points:
            adj: LatticePoint
            if adj in used:
                continue
            if grid[adj].rep.isdigit():
                num_string: str = grid[adj].rep
                used.add(adj)

                # Include all digits to left of starting character
                left = adj + Direction.LEFT
                while left in grid and grid[left].rep.isdigit():
                    used.add(left)
                    num_string = grid[left].rep + num_string
                    left = left + Direction.LEFT

                # Include all digits to right of starting character
                right = adj + Direction.RIGHT
                while right in grid and grid[right].rep.isdigit():
                    used.add(right)
                    num_string = num_string + grid[right].rep
                    right = right + Direction.RIGHT

                adjacent_numbers.append(int(num_string))

        part_numbers += adjacent_numbers
        if len(adjacent_numbers) == 2:
            gear_ratios.append(adjacent_numbers[0] * adjacent_numbers[1])

    print(f'Part number sum: {sum(part_numbers)}')
    print(f'Gear ratio sum: {sum(gear_ratios)}')


if __name__ == '__main__':
    main()
