from dataclasses import dataclass
from itertools import pairwise

from fishpy.geometry import LatticePoint
from fishpy.pathfinding import Direction, Location
from fishpy.pathfinding.grid import Grid

DIRECTIONS = {
    'U': Direction.NORTH, 'D': Direction.SOUTH,
    'R': Direction.EAST, 'L': Direction.WEST,
    '0': Direction.EAST, '1': Direction.SOUTH,
    '2': Direction.WEST, '3': Direction.NORTH,
}

@dataclass
class Instruction:
    direction: Direction
    distance: int


def size(instructions: list[Instruction]) -> int:
    pos = LatticePoint(0,0)
    corners: list[LatticePoint] = [pos]
    perimeter = 0
    for instruction in instructions:
        pos += instruction.direction * instruction.distance
        perimeter += instruction.distance
        corners.append(pos)

    area = 0
    for p0, p1 in pairwise(corners):
        area += p0.x * p1.y - p1.x * p0.y
    area = abs(area)

    return (area + perimeter) // 2 + 1


def main():
    with open('2023/18/input.txt') as f:
        lines = f.read().splitlines()
    
    instructions: list[Instruction] = []
    instructions_hex: list[Instruction] = []
    for line in lines:
        dir_letter, steps, hex = line.split()
        direction = DIRECTIONS[dir_letter]
        instructions.append(Instruction(direction, int(steps)))
        
        hex = hex.strip('(#)')
        direction = DIRECTIONS[hex[-1]]
        steps = int(hex[:-1], base=16)
        instructions_hex.append(Instruction(direction, steps))

    count = size(instructions)
    print(f'Cubic meters dug out with base instructions: {count}')
    
    hex_count = size(instructions_hex)
    print(f'Cubic meters dug out with hex instructions: {hex_count}')
    

if __name__ == '__main__':
    main()
