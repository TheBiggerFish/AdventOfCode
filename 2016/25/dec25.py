# Written by Cameron Haddock
# Written as a solution for Advent of Code 2016

# https://adventofcode.com/2016/day/25

import sys 
from typing import Any,Dict,List
from fishpy.computer import Computer, Instruction, Operand, Operation, ProgramCounter

clock = []
MAX_CLOCK_LENGTH = 8

def cpy_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    if arguments[1] in registers:
        registers[arguments[1]] = int(arg0)
    return pc+1

def inc_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    if arguments[0] in registers:
        registers[arguments[0]] += 1
    return pc+1

def dec_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    if arguments[0] in registers:
        registers[arguments[0]] -= 1
    return pc+1

def jnz_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    arg0,arg1 = arguments[0],arguments[1]
    if arg0 in registers:
        arg0 = registers[arg0]
    if arg1 in registers:
        arg1 = registers[arg1]

    if int(arg0) == 0:
        return pc + 1
    else:
        return pc + int(arg1)

def out_func(arguments:List[str],registers:Dict[str,Any],pc:ProgramCounter) -> ProgramCounter:
    arg0 = arguments[0]
    if arg0 in registers:
        arg0 = registers[arg0]
    clock.append(arg0)
    if len(clock) >= MAX_CLOCK_LENGTH:
        return -1
    return pc+1

ops = {
    'cpy': Operation('cpy',cpy_func,[Operand.REGISTER|Operand.CONSTANT,Operand.REGISTER]),
    'inc': Operation('inc',inc_func,[Operand.REGISTER]),
    'dec': Operation('dec',dec_func,[Operand.REGISTER]),
    'jnz': Operation('jnz',jnz_func,[Operand.REGISTER|Operand.CONSTANT,Operand.REGISTER|Operand.CONSTANT]),
    'out': Operation('out',out_func,[Operand.REGISTER|Operand.CONSTANT])
}

program = []
with open('2016/25/input.txt') as f:
    for line in f:
        cmd = line.strip().split()
        op = ops[cmd[0]]
        args = cmd[1:]
        program.append(Instruction(op,args))
        
for i in range(200):
    comp = Computer(registers={'a':i,'b':0,'c':0,'d':0},initial_pc=0)
    comp.execute(program)
    if clock == [0,1] * (MAX_CLOCK_LENGTH//2):
        print('\nFinal answer:',i)
        break
    if i % 10 == 0:
        print('.',end='')
        sys.stdout.flush()
    clock = []
