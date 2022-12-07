# Written by Cameron Haddock
# Written as a solution for Advent of Code 2019

# https://adventofcode.com/2019/day/2

from fishpy.computer import (ArgList, Computer, Operand, Operation,
                             ProgramCounter)


def add_func(arguments: list[int], memory: list[int],
             pc: ProgramCounter) -> ProgramCounter:
    memory[arguments[2]] = memory[arguments[0]] + memory[arguments[1]]
    return pc+4


def mul_func(arguments: list[int], memory: list[int],
             pc: ProgramCounter) -> ProgramCounter:
    memory[arguments[2]] = memory[arguments[0]] * memory[arguments[1]]
    return pc+4


def halt_func(arguments: list[int], memory: list[int],
              pc: ProgramCounter) -> ProgramCounter:
    return -1


ops = {1: Operation(1, add_func, [Operand.ADDRESS, Operand.ADDRESS, Operand.ADDRESS]),
       2: Operation(2, mul_func, [Operand.ADDRESS, Operand.ADDRESS, Operand.ADDRESS]),
       99: Operation(99, halt_func, [])}


class IntcodeComputer(Computer):
    def __init__(self, program: list[int], initial_pc: ProgramCounter = 0):
        super().__init__({}, initial_pc)
        self.memory = program

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(pc:{self.pc})'

    def write(self, index: int, value: int):
        self.memory[index] = value

    def read(self, index: int) -> int:
        return self.memory[index]

    def execute_step(self) -> bool:
        if self.memory[self.pc] not in ops:
            raise ValueError(f'Instruction {self.memory[self.pc]} not valid')
        op = ops[self.memory[self.pc]]
        args: ArgList = self.memory[self.pc+1:self.pc+4]
        self.pc = op.function(args, self.memory, self.pc)
        return 0 <= self.pc < len(self.memory)

    def execute(self):
        while self.execute_step():
            pass


with open('2019/02/input.txt') as f:
    byte_code = f.read().strip().split(',')
    program = list(map(int, byte_code))
    c = IntcodeComputer(program)
    c.write(1, 12)
    c.write(2, 2)
    c.execute()
    print(c.read(0))
