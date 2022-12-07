# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/2

from dataclasses import dataclass
from enum import Enum


class Opcode(Enum):
    ADD = 1
    MULT = 2


@dataclass
class Operation:
    type: Opcode
    bytes: int


ops = {Opcode.ADD: Operation(Opcode.ADD, 4),
       Opcode.MULT: Operation(Opcode.MULT, 4)}


@dataclass
class Instruction:
    operation: Operation
    args: list[int]


class Intcode:
    def __init__(self, program: list[int]):
        self._program = program
        self.index = 0

    def execute_instruction(self):
        op = ops[Opcode(self._program[self.index])]
        ins = Instruction(op, self._program[self.index+1:self.index+4])

    def execute(self):
        pass

    def read(self, index: int) -> int:
        return self._program[index]

    def write(self, index: int, value: int):
        self._program[index] = value


with open('2019/02/input.txt') as f:
    byte_code = f.read().strip().split(',')
    ints = map(int, byte_code)
