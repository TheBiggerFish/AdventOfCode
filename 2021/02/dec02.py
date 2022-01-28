# Written by Cameron Haddock
# Written as a solution for Advent of Code 2021

# https://adventofcode.com/2021/day/2


from typing import Callable

from fishpy.geometry import LatticePoint, Vector2D
from fishpy.geometry.vector2d import DOWN, RIGHT, UP

direction_map = {
    'up': UP,
    'down': DOWN,
    'forward': RIGHT,
}

with open('2021/02/input.txt') as f:
    directions = f.read().rstrip().split('\n')

position = LatticePoint(0,0)
get_vector:Callable[[str],Vector2D] = lambda string: direction_map[string.split()[0]] * int(string.split()[1])
for entry in map(get_vector,directions):
    position += entry

print(f'Final depth of first half: {position.x * (-position.y)}')



aim = 0
position = LatticePoint(0,0)
for entry in directions:
    direction,scale = tuple(entry.split())
    if direction == 'forward':
        position += RIGHT * int(scale)
        position += DOWN * aim * int(scale)
    if direction == 'up':
        aim -= int(scale)
    if direction == 'down':
        aim += int(scale)

print(f'Final depth of second half: {position.x * (-position.y)}')
